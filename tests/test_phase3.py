"""Offline regression checks for the illustrated v3.0 build-along labs.

These tests validate CLI text, quizzes and SVG assets; they do NOT simulate IOS,
prove Packet Tracer traffic behavior, or generate native .pkt projects.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "scripts" / "ios_config_generator.py"


def config(preset: str, role: str | None = None) -> str:
    cmd = [sys.executable, str(CLI), preset]
    if role is not None:
        cmd += ["--role", role]
    return subprocess.run(cmd, cwd=ROOT, text=True, check=True, capture_output=True).stdout


class PhaseThreeRegressionTests(unittest.TestCase):
    def test_cli_catalog_and_scoped_roles(self) -> None:
        out = subprocess.run([sys.executable, str(CLI), "--list"], cwd=ROOT,
                             text=True, check=True, capture_output=True).stdout
        for name in ("svi-switch", "hsrp", "ipv6-static", "ospfv3", "voip-cme",
                     "dhcp-snooping", "dai"):
            self.assertIn(name, out)
        self.assertIn("19টি", out)
        for preset, roles in (("hsrp", ("R1", "R2", "R3")),
                              ("ipv6-static", ("R1", "R2")),
                              ("ospfv3", ("R1", "R2")),
                              ("voip-cme", ("R1", "SW1")),
                              ("dhcp-snooping", ("R1", "SW1"))):
            for role in roles:
                with self.subTest(preset=preset, role=role):
                    text = config(preset, role)
                    self.assertIn(f"ONLY {role} CLI", text)
                    self.assertEqual(1, text.count("copy running-config startup-config"))
                    self.assertIn("enable\nconfigure terminal", text)

    def test_invalid_role_is_rejected(self) -> None:
        bad = subprocess.run([sys.executable, str(CLI), "hsrp", "--role", "SW1"],
                             cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(0, bad.returncode)
        self.assertIn("invalid choice", bad.stderr)

    def test_svi_matches_two_vlans_and_gateways(self) -> None:
        txt = config("svi-switch")
        for expected in ("ip routing", "interface vlan 10", "interface vlan 20",
                         "ip address 192.168.10.1 255.255.255.0",
                         "ip address 192.168.20.1 255.255.255.0",
                         "switchport access vlan 10", "switchport access vlan 20"):
            self.assertIn(expected, txt)
        self.assertNotIn("switchport mode trunk", txt)

    def test_hsrp_both_wan_paths_and_return_routes(self) -> None:
        r1, r2, r3 = (config("hsrp", role) for role in ("R1", "R2", "R3"))
        for txt in (r1, r2):
            self.assertIn("standby 1 ip 192.168.50.1", txt)
            self.assertIn("standby 1 preempt", txt)
        self.assertIn("standby 1 priority 120", r1)
        self.assertIn("standby 1 priority 100", r2)
        self.assertIn("10.0.13.2", r1)
        self.assertIn("10.0.23.2", r2)
        self.assertIn("ip route 192.168.50.0 255.255.255.0 10.0.13.1", r3)
        self.assertIn("ip route 192.168.50.0 255.255.255.0 10.0.23.1", r3)
        self.assertIn("ip address 198.51.100.10 255.255.255.255", r3)

    def test_ipv6_static_first_ospfv3_removes_static(self) -> None:
        r1, r2 = (config("ipv6-static", role) for role in ("R1", "R2"))
        self.assertIn("ipv6 address 2001:db8:10::1/64", r1)
        self.assertIn("ipv6 address fe80::1 link-local", r1)
        self.assertIn("ipv6 address 2001:db8:20::1/64", r2)
        self.assertIn("ipv6 address fe80::2 link-local", r2)
        self.assertIn("ipv6 route 2001:db8:20::/64 2001:db8:12::2", r1)
        self.assertIn("ipv6 route 2001:db8:10::/64 2001:db8:12::1", r2)
        for role, route, rid in (("R1", "2001:db8:20::/64 2001:db8:12::2", "1.1.1.1"),
                                  ("R2", "2001:db8:10::/64 2001:db8:12::1", "2.2.2.2")):
            txt = config("ospfv3", role)
            self.assertIn("no ipv6 route " + route, txt)
            self.assertIn("ipv6 router ospf 10", txt)
            self.assertIn("router-id " + rid, txt)
            self.assertEqual(2, txt.count("ipv6 ospf 10 area 0"))

    def test_voice_router_and_switch_are_separate(self) -> None:
        r1, sw = config("voip-cme", "R1"), config("voip-cme", "SW1")
        for expected in ("interface fastEthernet 0/0.20", "option 150 ip 192.168.20.1",
                         "ip source-address 192.168.20.1 port 2000", "number 1001", "number 1002"):
            self.assertIn(expected, r1)
        self.assertEqual(2, sw.count("switchport voice vlan 20"))
        self.assertIn("switchport mode trunk", sw)
        self.assertNotIn("telephony-service", sw)
        self.assertNotIn("switchport voice vlan", r1)

    def test_security_dai_is_separate_and_discloses_pt_limit(self) -> None:
        sw = config("dhcp-snooping", "SW1")
        dai = config("dai", "SW1")
        self.assertIn("ip dhcp snooping vlan 1", sw)
        self.assertIn("interface gigabitEthernet 0/1\n ip dhcp snooping trust", sw)
        self.assertEqual(1, sw.count("ip dhcp snooping trust"))
        self.assertNotIn("ip arp inspection vlan 1", sw)
        self.assertIn("binding", dai)
        self.assertIn("PT DAI", dai)
        self.assertIn("ip arp inspection vlan 1", dai)
        self.assertEqual(1, dai.count("ip arp inspection trust\n"))

    def test_quiz_bank_and_flashcards(self) -> None:
        spec = importlib.util.spec_from_file_location("quiz_trainer", ROOT / "scripts" / "quiz_trainer.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        questions = module.load_all_quizzes("all")
        self.assertEqual(86, len(questions))
        self.assertEqual(79, sum(q["type"] == "mcq" for q in questions))
        self.assertEqual(7, sum(q["type"] == "open" for q in questions))
        self.assertEqual(22, len(module.CLI_FLASHCARDS))
        for number in (16, 17, 18):
            q = module.load_all_quizzes("practical", number)
            self.assertEqual(3, len(q), number)
            self.assertTrue(all(p["type"] == "mcq" for p in q))

    def test_each_new_guide_has_two_accessible_local_svgs(self) -> None:
        chapters = {
            "lessons/16-multilayer-switch-svi.md": "lesson-16-",
            "lessons/17-hsrp-gateway-redundancy.md": "lesson-17-",
            "lessons/18-ipv6-slaac-routing.md": "lesson-18-",
            "Extras/voip-ip-telephony-lab.md": "extra-07-",
            "Extras/dhcp-snooping-dai-lab.md": "extra-08-",
        }
        for guide, prefix in chapters.items():
            with self.subTest(guide=guide):
                txt = (ROOT / guide).read_text(encoding="utf-8")
                svgs = list((ROOT / "assets/diagrams").glob(prefix + "*.svg"))
                self.assertEqual(2, len(svgs))
                self.assertEqual(2, txt.count("../assets/diagrams/" + prefix))
                for image in svgs:
                    svg = ET.parse(image).getroot()
                    ns = "{http://www.w3.org/2000/svg}"
                    self.assertEqual("svg", svg.tag.rsplit("}", 1)[-1])
                    self.assertTrue(svg.find(ns + "title").text)
                    self.assertTrue(svg.find(ns + "desc").text)
                self.assertIn("ছবির সারকথা", txt)
                self.assertIn("`.pkt`", txt)


if __name__ == "__main__":
    unittest.main()
