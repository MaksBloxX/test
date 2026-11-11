#!/usr/bin/env python3
"""Generate/check the v4.0 multi-site build-along IOS snippets and two original SVGs.

No Packet Tracer runtime is invoked. The JSON plan is the authoritative IP/port
inventory. Output is role-separated study material, NOT a tested .pkt or proof
of routing, telephony, NAT, radio association or service delivery.

Usage:
    python3 scripts/capstone_config_generator.py --list
    python3 scripts/capstone_config_generator.py --role HQ1
    python3 scripts/capstone_config_generator.py --write
    python3 scripts/capstone_config_generator.py --check
"""

from __future__ import annotations

import argparse
from ipaddress import ip_address, ip_network, IPv4Network
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "capstone" / "plan.json"
CONFIG_DIR = ROOT / "capstone" / "configs"
SVG_DIR = ROOT / "assets" / "diagrams"
ROLES = ("HQ1", "HQ2", "BR1", "BR2", "ISP", "HQ-SW", "BR1-SW", "BR2-SW", "CME")


def network(raw: str) -> IPv4Network:
    net = ip_network(raw, strict=True)
    if not isinstance(net, IPv4Network):
        raise ValueError("The Phase 5 address plan uses IPv4 only")
    return net


def load_plan() -> dict:
    return json.loads(PLAN.read_text(encoding="utf-8"))


def endpoints(link: dict, device: str) -> tuple[dict, dict]:
    own = [e for e in link["endpoints"] if e["device"] == device]
    other = [e for e in link["endpoints"] if e["device"] != device]
    if len(own) != 1 or len(other) != 1:
        raise ValueError(f"Broken device/peer pairing in {link['name']}: {device}")
    return own[0], other[0]


def validate_plan(plan: dict) -> None:
    """Reject collisions, unrouteable hosts and an inaccurate four-circuit plan."""
    if plan["version"] != "4.0" or set(plan["models"]) != set(ROLES):
        raise ValueError("Expected all nine distinct v4.0 device roles")
    if len(plan["hq_vlans"]) != 4 or set(plan["branch_vlans"]) != {"BR1", "BR2"}:
        raise ValueError("Expected four HQ VLANs and two branch sites")
    if len(plan["wan_links"]) != 4 or len(plan["isp_links"]) != 2:
        raise ValueError("Four independent private WAN circuits and two ISP uplinks are required")
    if {v["id"] for v in plan["hq_vlans"]} != {10, 20, 40, 99}:
        raise ValueError("HQ VLAN IDs differ from the tested lesson layout")
    nets: list[tuple[str, IPv4Network]] = []
    used_addresses: dict[str, str] = {}
    used_ports: dict[tuple[str, str], str] = {}

    def add_ip(value: str, owner: str, within: IPv4Network) -> None:
        address = ip_address(value)
        if address not in within.hosts():
            raise ValueError(f"{owner} {value} is not a usable address in {within}")
        if value in used_addresses:
            raise ValueError(f"Duplicate {value} used by {owner} and {used_addresses[value]}")
        used_addresses[value] = owner

    for group in [plan["hq_vlans"], *plan["branch_vlans"].values()]:
        for vlan in group:
            net = network(vlan["network"])
            nets.append((vlan["name"], net))
            if net.prefixlen != 24:
                raise ValueError(f"Campus VLAN must be /24: {net}")
            for key in ("vip", "HQ1", "HQ2") if "vip" in vlan else ("gateway",):
                add_ip(vlan[key], f"{vlan['name']} {key}", net)
            if "vip" in vlan and vlan["vip"] != str(net.network_address + 1):
                raise ValueError(f"HSRP VIP should be the .1 gateway in {vlan['name']}")
    if set(v["id"] for v in plan["branch_vlans"]["BR1"]) != {10, 20}:
        raise ValueError("BR1 needs data and optional voice networks")
    if set(v["id"] for v in plan["branch_vlans"]["BR2"]) != {10, 30}:
        raise ValueError("BR2 needs separate data and Wi-Fi networks")

    private_pairs: set[tuple[str, str]] = set()
    isp_pairs: set[tuple[str, str]] = set()
    for family, links in (("wan", plan["wan_links"]), ("ISP", plan["isp_links"])):
        for link in links:
            net = network(link["network"])
            if net.prefixlen != 30 or len(link["endpoints"]) != 2:
                raise ValueError(f"{link['name']} must be one two-end /30 point-to-point link")
            nets.append((link["name"], net))
            a, b = link["endpoints"]
            pair = tuple(sorted((a["device"], b["device"])))
            if family == "wan":
                private_pairs.add(pair)
            else:
                isp_pairs.add(pair)
            for end in (a, b):
                key = end["device"], end["interface"]
                if key in used_ports:
                    raise ValueError(f"{key} is connected to both {link['name']} and {used_ports[key]}")
                used_ports[key] = link["name"]
                add_ip(end["ip"], f"{link['name']} {end['device']}", net)
            if family == "wan" and sum(bool(e.get("dce")) for e in (a, b)) != 1:
                raise ValueError(f"{link['name']} needs one declared DCE end")
    if private_pairs != {("BR1", "HQ1"), ("BR1", "HQ2"),
                         ("BR2", "HQ1"), ("BR2", "HQ2")}:
        raise ValueError("Each branch must have one independent link to each HQ gateway")
    if isp_pairs != {("HQ1", "ISP"), ("HQ2", "ISP")}:
        raise ValueError("ISP links must be external and separately cabled")

    outside = plan["outside_test"]
    public_net = network(outside["network"])
    nets.append(("outside TEST PC LAN", public_net))
    add_ip(outside["isp_ip"], "ISP outside test interface", public_net)
    loopback = network(outside["loopback"])
    if loopback.prefixlen != 32:
        raise ValueError("The simulated Internet test target is one loopback")
    nets.append(("ISP test loopback", loopback))
    if (outside["pc_ip"] != plan["clients"]["EXT-PC"]["ip"]
            or outside["pc_gateway"] != outside["isp_ip"]
            or plan["clients"]["EXT-PC"]["gateway"] != outside["isp_ip"]):
        raise ValueError("External PC address and default gateway must match the ISP test LAN")

    for i, (name, left) in enumerate(nets):
        for other_name, right in nets[i + 1:]:
            if left.overlaps(right):
                raise ValueError(f"Address overlap between {name} {left} and {other_name} {right}")
    for name, srv in plan["services"].items():
        dmz = next(v for v in plan["hq_vlans"] if v["id"] == srv["vlan"] == 40)
        add_ip(srv["ip"], f"DMZ {name}", network(dmz["network"]))
        if srv["gateway"] != dmz["vip"]:
            raise ValueError(f"{name} should use the HSRP DMZ VIP as its gateway")
    expected_client_vlans = {"HQ-PC": ("HQ", 10), "HQ-ADMIN-PC": ("HQ", 99),
                             "BR1-PC": ("BR1", 10), "BR2-PC": ("BR2", 10),
                             "BR2-LAPTOP": ("BR2", 30)}
    if set(plan["clients"]) != set(expected_client_vlans) | {"EXT-PC"}:
        raise ValueError("Expected the five enterprise clients and one external test PC")
    for name, client in plan["clients"].items():
        matches = [net for _, net in nets if ip_address(client["ip"]) in net]
        if len(matches) != 1:
            raise ValueError(f"{name} address does not belong to exactly one subnet")
        add_ip(client["ip"], name, matches[0])
        if ip_address(client["gateway"]) not in matches[0]:
            raise ValueError(f"{name} gateway is outside its IP subnet")
        if name == "EXT-PC":
            if client["vlan"] is not None or matches[0] != public_net:
                raise ValueError("External test PC cannot belong to a campus VLAN")
            continue
        site, vlan_id = expected_client_vlans[name]
        vlans = plan["hq_vlans"] if site == "HQ" else plan["branch_vlans"][site]
        vlan = next(v for v in vlans if v["id"] == vlan_id)
        gateway = vlan["vip"] if site == "HQ" else vlan["gateway"]
        if (client["vlan"] != vlan_id or matches[0] != network(vlan["network"])
                or client["gateway"] != gateway
                or client["dns"] != plan["services"]["DNS"]["ip"]):
            raise ValueError(f"{name} must use its declared VLAN, gateway and internal DNS")
    wifi_vlan = next(v for v in plan["branch_vlans"]["BR2"] if v["id"] == 30)
    voice_vlan = next(v for v in plan["hq_vlans"] if v["id"] == 20)
    add_ip(plan["wifi"]["lan_ip"], "BR2 access point", network(wifi_vlan["network"]))
    add_ip(plan["voice"]["ip"], "2811 CME", network(voice_vlan["network"]))
    if plan["wifi"]["dhcp"] != "disabled" or not plan["wifi"]["uplink"].startswith("LAN"):
        raise ValueError("WRT300N must bridge a LAN port with DHCP off, not perform second NAT")
    if plan["voice"]["ip"] != plan["voice"]["option150"] or plan["voice"]["gateway"] != voice_vlan["vip"]:
        raise ValueError("Phone option 150 must reach 2811 CME; the gateway is HSRP, not CME")
    if plan["public_web"]["inside_ip"] != plan["services"]["WEB"]["ip"]:
        raise ValueError("Public web port mapping must point to the DMZ web host")
    for hq in ("HQ1", "HQ2"):
        external_ip = endpoints(next(link for link in plan["isp_links"] if any(e["device"] == hq for e in link["endpoints"])), hq)[0]["ip"]
        if plan["public_web"][hq] != external_ip:
            raise ValueError(f"{hq} published web IP does not match its outside interface")
    expected_trunks = {"HQ-SW": {"HQ1", "HQ2"}, "BR1-SW": {"BR1"}, "BR2-SW": {"BR2"}}
    if set(plan["switches"]) != set(expected_trunks):
        raise ValueError("Expected exactly HQ-SW, BR1-SW and BR2-SW")
    for name, switch in plan["switches"].items():
        site = "HQ" if name == "HQ-SW" else name.split("-")[0]
        ids = {v["id"] for v in (plan["hq_vlans"] if site == "HQ" else plan["branch_vlans"][site])}
        port_names = [p["interface"] for p in switch["trunks"] + switch["access"]]
        if len(port_names) != len(set(port_names)):
            raise ValueError(f"A physical port is used twice on {name}")
        if any(set(p["vlans"]) != ids for p in switch["trunks"]):
            raise ValueError(f"Every {name} trunk must carry its intended VLANs")
        peers = [p["peer"].split(" ", 1) for p in switch["trunks"]]
        if (len(peers) != len(expected_trunks[name])
                or any(len(p) != 2 for p in peers)
                or {device for device, _ in peers} != expected_trunks[name]):
            raise ValueError(f"{name} must trunk once to each expected campus router")
        for router, port in peers:
            key = router, port
            if key in used_ports:
                raise ValueError(f"{key} is used by {used_ports[key]} and the {name} VLAN trunk")
            used_ports[key] = f"{name} VLAN trunk"
        if any(p["vlan"] not in ids or (p.get("voice_vlan") and p["voice_vlan"] not in ids)
               for p in switch["access"]):
            raise ValueError(f"Switch access/voice port refers to an absent VLAN on {name}")


def interface(name: str, commands: list[str]) -> list[str]:
    return [f"interface {name}", *(f" {command}" for command in commands), "exit"]


def block(head: str, commands: list[str]) -> list[str]:
    return [head, *(f" {command}" for command in commands), "exit"]


def peer_link(links: list[dict], role: str) -> list[tuple[dict, dict, dict]]:
    return [(link, *endpoints(link, role)) for link in links if any(e["device"] == role for e in link["endpoints"])]


def campus_trunk(plan: dict, role: str) -> tuple[str, str]:
    """Derive the router's VLAN trunk and switch port from the cable inventory."""
    switch = "HQ-SW" if role.startswith("HQ") else f"{role}-SW"
    matches = [port for port in plan["switches"][switch]["trunks"]
               if port["peer"].startswith(role + " ")]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {role} VLAN trunk in {switch}")
    return matches[0]["peer"].split(" ", 1)[1], matches[0]["interface"]


def ospf(role: str, vlans: list[dict], links: list[tuple[dict, dict, dict]]) -> list[str]:
    router_ids = {"HQ1": "1.1.1.1", "HQ2": "2.2.2.2", "BR1": "3.3.3.3", "BR2": "4.4.4.4"}
    commands = [f"router-id {router_ids[role]}", "passive-interface default"]
    commands.extend(f"no passive-interface {end['interface']}" for _, end, _ in links)
    for vlan in vlans:
        net = network(vlan["network"])
        commands.append(f"network {net.network_address} {net.hostmask} area 0")
    for link, _, _ in links:
        net = network(link["network"])
        commands.append(f"network {net.network_address} {net.hostmask} area 0")
    return block("router ospf 10", commands)


def hq_config(role: str, plan: dict) -> list[str]:
    priority = 120 if role == "HQ1" else 100
    trunk_port, switch_port = campus_trunk(plan, role)
    lines = interface(trunk_port, [f"description 802.1Q trunk to HQ-SW {switch_port}",
                                   "no ip address", "no shutdown"])
    for vlan in plan["hq_vlans"]:
        net = network(vlan["network"])
        group = vlan["id"]
        lines += interface(f"{trunk_port}.{group}", [
            f"description {vlan['name']} HSRP group {group}", f"encapsulation dot1Q {group}",
            f"ip address {vlan[role]} {net.netmask}", f"standby {group} ip {vlan['vip']}",
            f"standby {group} priority {priority}", f"standby {group} preempt", "ip nat inside",
            "no shutdown"])
    wan = peer_link(plan["wan_links"], role)
    for link, end, other in wan:
        net = network(link["network"])
        commands = [f"description Private point-to-point to {other['device']} {other['interface']}",
                    f"ip address {end['ip']} {net.netmask}", "ip nat inside", "no shutdown"]
        if end.get("dce"):
            commands.insert(2, "clock rate 64000")
        lines += interface(end["interface"], commands)
    external = peer_link(plan["isp_links"], role)
    if len(external) != 1:
        raise ValueError(f"Expected exactly one external ISP interface for {role}")
    link, end, isp = external[0]
    lines += interface(end["interface"], [f"description ISP test link to {isp['interface']}",
                                              f"ip address {end['ip']} {network(link['network']).netmask}",
                                              "ip nat outside", "no shutdown"])
    lines += [f"ip route 0.0.0.0 0.0.0.0 {isp['ip']}"]
    lines += ospf(role, plan["hq_vlans"], wan)
    lines += ["! NAT overload is only for traffic leaving the ISP interface; ISP does not run private OSPF.",
              "access-list 1 permit 10.0.0.0 0.255.255.255",
              f"ip nat inside source list 1 interface {end['interface']} overload",
              "! Only HTTP is intentionally published. DNS, mail and FTP are private DMZ services.",
              f"ip nat inside source static tcp {plan['public_web']['inside_ip']} 80 {end['ip']} 80"]
    return lines


def acl_for_branch(role: str, plan: dict) -> list[str]:
    data = next(v for v in plan["branch_vlans"][role] if v["id"] == 10)
    source = network(data["network"])
    admin = network(next(v for v in plan["hq_vlans"] if v["id"] == 99)["network"])
    commands = ["remark Block this branch DATA subnet from HQ ADMIN; other destinations remain allowed",
                f"deny ip {source.network_address} {source.hostmask} {admin.network_address} {admin.hostmask}",
                f"permit ip {source.network_address} {source.hostmask} any"]
    result = block(f"ip access-list extended {role}_DATA_IN", commands)
    if role == "BR2":
        wifi = network(next(v for v in plan["branch_vlans"]["BR2"] if v["id"] == 30)["network"])
        dmz = network(next(v for v in plan["hq_vlans"] if v["id"] == 40)["network"])
        dns = plan["services"]["DNS"]["ip"]
        web = plan["services"]["WEB"]["ip"]
        result += block("ip access-list extended BR2_WIFI_IN", [
            "remark Wi-Fi cannot reach HQ ADMIN",
            f"deny ip {wifi.network_address} {wifi.hostmask} {admin.network_address} {admin.hostmask}",
            "remark Permit only DNS and HTTP to the service VLAN from Wi-Fi",
            f"permit udp {wifi.network_address} {wifi.hostmask} host {dns} eq 53",
            f"permit tcp {wifi.network_address} {wifi.hostmask} host {dns} eq 53",
            f"permit tcp {wifi.network_address} {wifi.hostmask} host {web} eq 80",
            f"deny ip {wifi.network_address} {wifi.hostmask} {dmz.network_address} {dmz.hostmask}",
            f"permit ip {wifi.network_address} {wifi.hostmask} any"])
    return result


def branch_config(role: str, plan: dict) -> list[str]:
    switch = f"{role}-SW"
    trunk_port, switch_port = campus_trunk(plan, role)
    lines = interface(trunk_port, [f"description 802.1Q trunk to {switch} {switch_port}",
                                   "no ip address", "no shutdown"])
    for vlan in plan["branch_vlans"][role]:
        net = network(vlan["network"])
        commands = [f"description {vlan['name']}", f"encapsulation dot1Q {vlan['id']}",
                    f"ip address {vlan['gateway']} {net.netmask}", "no shutdown"]
        if vlan["id"] == 10:
            commands.insert(-1, f"ip access-group {role}_DATA_IN in")
        if role == "BR2" and vlan["id"] == 30:
            commands.insert(-1, "ip access-group BR2_WIFI_IN in")
        lines += interface(f"{trunk_port}.{vlan['id']}", commands)
    wan = peer_link(plan["wan_links"], role)
    if len(wan) != 2:
        raise ValueError(f"{role} must have two separate HQ uplinks")
    for link, end, other in wan:
        commands = [f"description Private serial to {other['device']} {other['interface']}",
                    f"ip address {end['ip']} {network(link['network']).netmask}", "no shutdown"]
        lines += interface(end["interface"], commands)
    default1 = next(other["ip"] for _, _, other in wan if other["device"] == "HQ1")
    default2 = next(other["ip"] for _, _, other in wan if other["device"] == "HQ2")
    lines += ["! Primary external route follows HQ1; the higher-distance HQ2 route is backup.",
              f"ip route 0.0.0.0 0.0.0.0 {default1}",
              f"ip route 0.0.0.0 0.0.0.0 {default2} 20"]
    lines += ospf(role, plan["branch_vlans"][role], wan)
    lines += acl_for_branch(role, plan)
    if role == "BR1":
        voice_vlan = next(v for v in plan["branch_vlans"]["BR1"] if v["id"] == 20)
        start, stop = plan["voice"]["branch_dhcp_exclude"]
        lines += ["! Optional BR1 voice phone: registration to HQ 2811 must be observed in your PT version.",
                  f"ip dhcp excluded-address {start} {stop}"]
        lines += block("ip dhcp pool BR1_VOICE", [
            f"network {voice_vlan['network'].split('/')[0]} {network(voice_vlan['network']).netmask}",
            f"default-router {voice_vlan['gateway']}", f"option 150 ip {plan['voice']['option150']}"])
    return lines


def switch_config(role: str, plan: dict) -> list[str]:
    switch = plan["switches"][role]
    site = "HQ" if role == "HQ-SW" else role.split("-")[0]
    vlans = plan["hq_vlans"] if site == "HQ" else plan["branch_vlans"][site]
    lines = []
    for vlan in vlans:
        lines += block(f"vlan {vlan['id']}", [f"name {vlan['name']}"])
    for trunk in switch["trunks"]:
        lines += interface(trunk["interface"], [f"description to {trunk['peer']}",
                                                  "switchport mode trunk",
                                                  "switchport trunk allowed vlan " + ",".join(map(str, trunk["vlans"])),
                                                  "no shutdown"])
    for port in switch["access"]:
        commands = [f"description {port['peer']}", "switchport mode access",
                    f"switchport access vlan {port['vlan']}"]
        if port.get("voice_vlan"):
            commands.append(f"switchport voice vlan {port['voice_vlan']}")
        commands += ["spanning-tree portfast", "no shutdown"]
        lines += interface(port["interface"], commands)
    return lines


def isp_config(plan: dict) -> list[str]:
    lines = []
    for link, end, other in peer_link(plan["isp_links"], "ISP"):
        lines += interface(end["interface"], [f"description Simulated outside link to {other['device']}",
                                                 f"ip address {end['ip']} {network(link['network']).netmask}",
                                                 "no shutdown"])
    outside = plan["outside_test"]
    lines += interface(outside["isp_interface"], ["description EXT-PC outside test segment",
                                                 f"ip address {outside['isp_ip']} {network(outside['network']).netmask}",
                                                 "no shutdown"])
    loop = network(outside["loopback"])
    lines += interface("Loopback0", ["description Documentation-only Internet-like test endpoint",
                                     f"ip address {loop.network_address} {loop.netmask}"])
    lines += ["! No OSPF, NAT or private 10/8 route on ISP: HQ edge PAT must be observable."]
    return lines


def cme_config(plan: dict) -> list[str]:
    voice = plan["voice"]
    hq_voice = next(v for v in plan["hq_vlans"] if v["id"] == 20)
    lines = interface(voice["interface"], ["description HQ-SW FastEthernet0/4 access VLAN20 (NOT a trunk)",
                                           f"ip address {voice['ip']} {network(hq_voice['network']).netmask}",
                                           "no shutdown"])
    lines += [f"ip route 0.0.0.0 0.0.0.0 {voice['gateway']}",
              f"ip dhcp excluded-address {' '.join(voice['hq_dhcp_exclude'])}"]
    lines += block("ip dhcp pool HQ_VOICE", [
        f"network {network(hq_voice['network']).network_address} {network(hq_voice['network']).netmask}",
        f"default-router {voice['gateway']}", f"option 150 ip {voice['option150']}"])
    lines += block("telephony-service", ["max-ephones 3", "max-dn 3",
                                          f"ip source-address {voice['ip']} port 2000", "auto assign 1 to 3"])
    for idx, number in enumerate([*voice["hq_extensions"], voice["branch_optional_extension"]], 1):
        lines += block(f"ephone-dn {idx}", [f"number {number}"])
    lines += ["! Auto-assigned extension order follows registration. Read phone screens before dialing.",
              "! create cnf-files may be optional/unsupported in some Packet Tracer versions."]
    return lines


def role_config(role: str, plan: dict) -> str:
    if role not in ROLES:
        raise ValueError(f"Unknown role {role!r}; choose one of {', '.join(ROLES)}")
    config = (hq_config(role, plan) if role in ("HQ1", "HQ2") else
              branch_config(role, plan) if role in ("BR1", "BR2") else
              switch_config(role, plan) if role.endswith("-SW") else
              isp_config(plan) if role == "ISP" else cme_config(plan))
    lines = [f"! v4.0 build-along for {role} (not executed in Packet Tracer)",
             "! Cable exactly as in capstone/plan.json; adjust interface labels if your PT module differs.",
             "! For serial clock rate, the HQ cable end MUST be DCE (show controllers serial).",
             "enable", "configure terminal", f"hostname {role}", "no ip domain-lookup"]
    lines.extend(config)
    lines += ["end", "copy running-config startup-config", ""]
    return "\n".join(lines)


def diagrams(plan: dict) -> dict[str, str]:
    """Concept diagrams from the same JSON data as the IOS snippets."""
    from diagram_generator import Art, BLUE, TEAL, VIOLET, AMBER, NAVY

    a = Art("v4.0 | two branches, resilient HQ and an ISP test edge",
            "Four independent /30 serial circuits; HQ HSRP protects private VLAN gateways.",
            "build-along map", "Illustration only. Exact port pairings and host masks are in capstone/plan.json; no .pkt was opened.", 1000)
    a.zone(38,143,495,510,"HQ: HQ1 + HQ2 + shared VLANs",BLUE)
    a.zone(551,143,530,205,"BR1: wired data + optional remote voice",TEAL)
    a.zone(551,368,530,285,"BR2: wired data + bridged Wi-Fi",VIOLET)
    a.zone(38,680,1043,250,"Public documentation/test networks, not the Internet",AMBER)
    a.node("HQ1",155,288,"router","HQ1 / 2911",f"outside {plan['public_web']['HQ1']}",BLUE,186)
    a.node("HQ2",410,288,"router","HQ2 / 2911",f"outside {plan['public_web']['HQ2']}",BLUE,186)
    a.node("HQS",281,467,"switch","HQ-SW / 2960","dual 802.1Q trunks",TEAL,218)
    a.edge("HQ1","HQS","trunk")
    a.edge("HQ2","HQS","trunk")
    a.pill(282,380,"HSRP .1: VLAN 10,20,40,99",VIOLET,width=295)
    a.callout(64,560,211,68,"Voice / CME 2811",[f"{plan['voice']['ip']}  |  1001 / 1002"],TEAL)
    dmz_octets = "  ".join(f"{name} .{plan['services'][name]['ip'].rsplit('.', 1)[1]}"
                           for name in ("DNS", "WEB", "MAIL", "FTP"))
    a.callout(296,560,211,68,"DMZ farm",[dmz_octets],BLUE)
    a.node("BR1",705,260,"router","BR1 / 2911","10.20.10.0/24 data",TEAL,229)
    a.node("BR2",705,490,"router","BR2 / 2911","10.30.10.0/24 data",VIOLET,229)
    a.pill(939,277,"BR1 voice: 10.20.20.0/24",TEAL,width=247)
    a.pill(943,475,"BR2 Wi-Fi: 10.30.30.0/24",VIOLET,width=250)
    a.pill(941,525,"WRT LAN port; DHCP OFF",VIOLET,width=256)
    # A WAN box represents four distinct serial cables, not a transit router.
    a.callout(550,571,510,68,"Four separate serial /30 links (NOT through the ISP)",[
        "HQ1-BR1: 11.0   HQ2-BR1: 12.0   HQ1-BR2: 21.0   HQ2-BR2: 22.0"],VIOLET)
    a.line(533,283,565,283,VIOLET,4,"10 6")
    a.line(533,420,565,420,VIOLET,4,"10 6")
    a.node("ISP",341,802,"cloud","ISP / 2911","no private OSPF",AMBER,211)
    a.node("EXT",805,802,"pc","EXT-PC",plan["outside_test"]["pc_ip"],BLUE,225)
    a.edge("ISP","EXT","wired",plan["outside_test"]["network"],-28)
    a.pill(200,901,f"HQ1 -> ISP {plan['isp_links'][0]['network']}",AMBER,width=320)
    a.pill(560,901,f"HQ2 -> ISP {plan['isp_links'][1]['network']}",AMBER,width=320)
    a.pill(920,901,"ISP test: 192.0.2.100/32",BLUE,width=320)

    b = Art("v4.0 | test the paths, then create your own .pkt",
            "Expected tests are study predictions until you run Packet Tracer yourself.",
            "verification plan", "Web public IP changes after HQ1 power-off: use HQ2 .5; no automatic public IP failover.", 895)
    rows = [
        ("01 | Private services", "BR1-PC -> OSPF -> HQ DMZ Web/DNS/Mail/FTP", "Use 10.10.40.x; ISP does not route the private LANs.", BLUE),
        ("02 | Wi-Fi and ACL", f"BR2 laptop: DNS {plan['services']['DNS']['ip']} + HTTP {plan['services']['WEB']['ip']} allowed",
         "HQ ADMIN 10.10.99.10 and other DMZ ports denied; check ACL counters.", VIOLET),
        ("03 | PAT to test ISP", f"BR1/HQ client -> HQ1 PAT {plan['public_web']['HQ1']} -> ISP Lo0 {plan['outside_test']['loopback']}",
         "Test the documentation-only loopback; not public Internet access.", TEAL),
        ("04 | HQ1 powered OFF", "HQ2 HSRP active + branch floating defaults + HQ2 PAT",
         f"Retest private routes, outside ping and public HTTP on {plan['public_web']['HQ2']}.", AMBER),
        ("05 | Voice evidence", f"HQ phones: option 150 -> CME {plan['voice']['ip']}",
         "Verify screens 1001/1002, then ring/answer; no real PSTN audio.", BLUE),
    ]
    for idx, (title, first, second, color) in enumerate(rows):
        top = 140 + idx * 136
        b.callout(48,top,1024,113,title,[first,second],color)
    return {"capstone-v4-sites.svg": a.render(), "capstone-v4-paths.svg": b.render()}


def render_all(plan: dict) -> dict[Path, str]:
    content = {CONFIG_DIR / (role + ".txt"): role_config(role, plan) for role in ROLES}
    content.update({SVG_DIR / name: data for name, data in diagrams(plan).items()})
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--role", choices=ROLES, help="Print one device role's study configuration")
    action.add_argument("--list", action="store_true", help="List all nine available roles")
    action.add_argument("--write", action="store_true", help="Regenerate nine role snippets plus two SVGs")
    action.add_argument("--check", action="store_true", help="Fail if JSON plan, configs or SVGs disagree")
    args = parser.parse_args()
    try:
        plan = load_plan()
        validate_plan(plan)
        if args.list:
            print("v4.0 build-along roles (not tested .pkt files):", ", ".join(ROLES))
            return 0
        if args.role:
            print(role_config(args.role, plan), end="")
            return 0
        output = render_all(plan)
        stale = [p.relative_to(ROOT).as_posix() for p, text in output.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        if args.check:
            if stale:
                raise ValueError("Missing or stale generated materials: " + ", ".join(stale))
            print("Checked nine role-separated IOS snippets and two illustrated SVGs against the validated v4.0 address plan.")
            return 0
        for path, text in output.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        print(f"Generated {len(ROLES)} role-separated IOS study snippets and two original SVGs; no Packet Tracer runtime was used.")
        return 0
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        print(f"Capstone plan error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
