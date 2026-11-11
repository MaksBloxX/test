"""v4.0 offline plan/config/content regression tests, NOT Packet Tracer tests.

These cannot prove IOS command acceptance, OSPF adjacencies, HSRP failover,
CME registration, HTTP port forwarding, ACL packet behavior or a working .pkt.
"""

from __future__ import annotations

from copy import deepcopy
from ipaddress import ip_address, ip_network
import json
from pathlib import Path
import re
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from capstone_config_generator import (ROLES, diagrams, endpoints, load_plan, network,
                                        render_all, role_config, validate_plan)  # noqa: E402


class PhaseFiveOfflineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = load_plan()
        validate_plan(cls.plan)
        cls.roles = {role: role_config(role, cls.plan) for role in ROLES}

    def test_four_private_wans_and_two_distinct_isp_links(self) -> None:
        p = self.plan
        self.assertEqual(4, len(p["wan_links"]))
        self.assertEqual(2, len(p["isp_links"]))
        seen_ports = set()
        for link in p["wan_links"] + p["isp_links"]:
            net = network(link["network"])
            self.assertEqual(30, net.prefixlen)
            self.assertEqual(2, len(link["endpoints"]))
            for end in link["endpoints"]:
                self.assertIn(ip_address(end["ip"]), net)
                self.assertNotIn((end["device"], end["interface"]), seen_ports)
                seen_ports.add((end["device"], end["interface"]))
        for branch in ("BR1", "BR2"):
            peers = {end["device"] for link in p["wan_links"]
                     for end in link["endpoints"] if branch in {e["device"] for e in link["endpoints"]}}
            self.assertEqual({branch, "HQ1", "HQ2"}, peers)
        for role in ("HQ1", "HQ2", "BR1", "BR2"):
            self.assertEqual(2, self.roles[role].count("no passive-interface Serial"))
            self.assertNotIn("198.51.100.0 0.0.0.3 area 0", self.roles[role])
            self.assertNotIn("203.0.113.0 0.0.0.255 area 0", self.roles[role])
        self.assertNotIn("router ospf", self.roles["ISP"])
        self.assertNotRegex(self.roles["ISP"], r"(?m)^ip route 10\.")

    def test_hsrp_default_gateways_vlan_membership_and_cme_source_are_consistent(self) -> None:
        p = self.plan
        for vlan in p["hq_vlans"]:
            group = vlan["id"]
            net = ip_network(vlan["network"])
            self.assertEqual(vlan["vip"], str(net.network_address + 1))
            for role, priority in (("HQ1", 120), ("HQ2", 100)):
                text = self.roles[role]
                self.assertIn(f"standby {group} ip {vlan['vip']}", text)
                self.assertIn(f"standby {group} priority {priority}", text)
                self.assertIn(f"ip address {vlan[role]} {net.netmask}", text)
                self.assertIn(f"network {net.network_address} {net.hostmask} area 0", text)
        cme = self.roles["CME"]
        self.assertIn("hostname CME", cme)
        self.assertIn("interface FastEthernet0/0", cme)
        self.assertIn("ip source-address 10.10.20.10 port 2000", cme)
        self.assertIn("default-router 10.10.20.1", cme)
        self.assertIn("option 150 ip 10.10.20.10", cme)
        self.assertIn("number 1001", cme)
        self.assertIn("number 1002", cme)
        self.assertIn("number 2001", cme)
        self.assertNotIn("encapsulation dot1Q", cme)
        self.assertEqual(2, self.roles["HQ-SW"].count("switchport trunk allowed vlan 10,20,40,99"))
        self.assertIn("switchport voice vlan 20", self.roles["HQ-SW"])
        self.assertNotIn("interface GigabitEthernet0/0.99", self.roles["BR1"])

    def test_pat_public_web_and_backup_defaults_have_distinct_endpoints(self) -> None:
        for role, outside in (("HQ1", "198.51.100.1"), ("HQ2", "198.51.100.5")):
            text = self.roles[role]
            self.assertEqual(6, text.count(" ip nat inside\n"))  # four HQ VLANs and two private serials
            self.assertIn("ip nat inside source list 1 interface GigabitEthernet0/1 overload", text)
            self.assertIn("ip nat inside source static tcp 10.10.40.20 80 " + outside + " 80", text)
            self.assertIn("ip nat outside", text)
            self.assertEqual(2, text.count("clock rate 64000"))
        for branch, primary, backup in (("BR1", "10.255.11.1", "10.255.12.1"),
                                        ("BR2", "10.255.21.1", "10.255.22.1")):
            text = self.roles[branch]
            self.assertIn(f"ip route 0.0.0.0 0.0.0.0 {primary}\n", text)
            self.assertIn(f"ip route 0.0.0.0 0.0.0.0 {backup} 20\n", text)
            self.assertNotIn("ip nat outside", text)
        self.assertNotEqual(self.plan["public_web"]["HQ1"], self.plan["public_web"]["HQ2"])

    def test_acl_order_wifi_policy_and_wrt_bridge_are_explicit(self) -> None:
        br2 = self.roles["BR2"]
        pos = [br2.index(s) for s in (
            "deny ip 10.30.30.0 0.0.0.255 10.10.99.0 0.0.0.255",
            "permit udp 10.30.30.0 0.0.0.255 host 10.10.40.10 eq 53",
            "permit tcp 10.30.30.0 0.0.0.255 host 10.10.40.10 eq 53",
            "permit tcp 10.30.30.0 0.0.0.255 host 10.10.40.20 eq 80",
            "deny ip 10.30.30.0 0.0.0.255 10.10.40.0 0.0.0.255",
            "permit ip 10.30.30.0 0.0.0.255 any")]
        self.assertEqual(pos, sorted(pos), "ACL permit rules must precede broad DMZ deny")
        self.assertIn("ip access-group BR2_WIFI_IN in", br2)
        self.assertIn("deny ip 10.20.10.0 0.0.0.255 10.10.99.0 0.0.0.255", self.roles["BR1"])
        self.assertEqual("disabled", self.plan["wifi"]["dhcp"])
        self.assertIn("LAN", self.plan["wifi"]["uplink"])
        self.assertIn("WRT300N Ethernet 1 LAN port (not Internet)", self.roles["BR2-SW"])

    def test_bad_address_or_cabling_mutation_is_rejected(self) -> None:
        bad = deepcopy(self.plan)
        bad["hq_vlans"][0]["HQ1"] = bad["hq_vlans"][0]["vip"]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate_plan(bad)
        bad = deepcopy(self.plan)
        bad["wan_links"][1]["network"] = bad["wan_links"][0]["network"]
        with self.assertRaises(ValueError):
            validate_plan(bad)
        bad = deepcopy(self.plan)
        bad["wan_links"][2]["endpoints"][0]["interface"] = "Serial0/0/0"
        with self.assertRaises(ValueError):
            validate_plan(bad)
        bad = deepcopy(self.plan)
        bad["public_web"]["HQ2"] = bad["public_web"]["HQ1"]
        with self.assertRaises(ValueError):
            validate_plan(bad)
        bad = deepcopy(self.plan)
        bad["wifi"]["dhcp"] = "enabled"
        with self.assertRaises(ValueError):
            validate_plan(bad)

    def test_trunk_remap_and_gateway_validation_follow_cable_inventory(self) -> None:
        changed = deepcopy(self.plan)
        changed["switches"]["HQ-SW"]["trunks"][0]["peer"] = "HQ1 GigabitEthernet0/2"
        validate_plan(changed)
        self.assertIn("interface GigabitEthernet0/2.40", role_config("HQ1", changed))
        self.assertIn("description to HQ1 GigabitEthernet0/2", role_config("HQ-SW", changed))
        bad = deepcopy(changed)
        bad["switches"]["HQ-SW"]["trunks"][0]["peer"] = "HQ1 GigabitEthernet0/1"
        with self.assertRaises(ValueError):
            validate_plan(bad)  # would reuse HQ1's ISP outside interface
        bad = deepcopy(self.plan)
        bad["clients"]["BR2-LAPTOP"]["gateway"] = "10.30.30.254"
        with self.assertRaises(ValueError):
            validate_plan(bad)  # usable address, but not BR2's actual routed gateway
        bad = deepcopy(self.plan)
        bad["clients"]["EXT-PC"]["gateway"] = "203.0.113.254"
        with self.assertRaises(ValueError):
            validate_plan(bad)  # must use the ISP's address, not just any host in /24

    def test_generated_configs_and_accessible_diagrams_match_plan(self) -> None:
        rendered = render_all(self.plan)
        self.assertEqual(11, len(rendered))  # nine role configs + two original SVGs
        for path, text in rendered.items():
            with self.subTest(path=path.name):
                self.assertEqual(path.read_text(encoding="utf-8"), text)
                if path.suffix == ".svg":
                    root = ET.fromstring(text)
                    self.assertEqual("{http://www.w3.org/2000/svg}svg", root.tag)
                    self.assertTrue(root.attrib.get("role") == "img")
                    self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"))
                    self.assertIn("not", text.lower())
                else:
                    self.assertIn("not executed in Packet Tracer", text)
                    self.assertIn("copy running-config startup-config", text)
        topology = diagrams(self.plan)["capstone-v4-sites.svg"]
        for required in ("HQ1", "HQ2", "BR1", "BR2", "ISP", "11.0", "22.0", "198.51.100"):
            self.assertIn(required, topology)

    def test_v4_navigation_catalogues_and_ci_checks_are_wired(self) -> None:
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for page in ("capstone/README.md", "en/capstone/README.md", "capstone/VERIFICATION.md",
                     "pkt-files/capstone/README.md"):
            self.assertIn(page, nav)
            self.assertIn(page, (ROOT / "PORTAL.md").read_text(encoding="utf-8"))
        for name in ("capstone-v4-sites.svg", "capstone-v4-paths.svg"):
            self.assertIn(name, (ROOT / "assets/diagrams/README.md").read_text(encoding="utf-8"))
        self.assertIn("capstone_config_generator.py --check",
                      (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8"))
        self.assertIn("capstone_config_generator.py --check",
                      (ROOT / ".github/workflows/repo-check.yml").read_text(encoding="utf-8"))
        self.assertIn("count < 96", (ROOT / "scripts/portal_docs.py").read_text(encoding="utf-8"))
        self.assertIn("capstone/README.md", (ROOT / "pkt-files/README.md").read_text(encoding="utf-8"))
        self.assertIn("[ ] **Native Packet Tracer `.pkt`", (ROOT / "ROADMAP.md").read_text(encoding="utf-8"))

    def test_guides_evidence_and_pkt_absence_are_candid(self) -> None:
        bangla = (ROOT / "capstone/README.md").read_text(encoding="utf-8")
        english = (ROOT / "en/capstone/README.md").read_text(encoding="utf-8")
        worksheet = (ROOT / "capstone/VERIFICATION.md").read_text(encoding="utf-8")
        howto = (ROOT / "pkt-files/capstone/README.md").read_text(encoding="utf-8")
        self.assertIn("../en/capstone/README.md", bangla)
        self.assertIn("../../capstone/README.md", english)
        self.assertIn("four private WAN circuits", english)
        self.assertIn("four private WAN circuits total", english)
        self.assertIn("নতুন native `.pkt`", bangla)
        self.assertIn("Not a Packet Tracer recording", english)
        self.assertIn("asymmetric NAT", bangla)
        self.assertIn("stateful NAT path", english)
        self.assertIn("Destination filename [startup-config]?", english)
        self.assertIn("Expected", worksheet)
        self.assertIn("Actual", worksheet)
        self.assertIn("______________________________", worksheet)
        self.assertIn("এখানে এখন নতুন `.pkt` নেই", howto)
        self.assertEqual(0, len(list((ROOT / "pkt-files/capstone").glob("*.pkt"))))
        self.assertEqual(18, len(list((ROOT / "pkt-files").rglob("*.pkt"))))
        for id_ in ("N01", "N20", "F01", "F08"):
            self.assertIn(id_, worksheet)
        for path in ("capstone/README.md", "capstone/VERIFICATION.md", "en/capstone/README.md",
                     "pkt-files/capstone/README.md"):
            self.assertIn("capstone-v4-", (ROOT / path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
