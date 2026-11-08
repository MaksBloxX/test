#!/usr/bin/env python3
"""
ios_config_generator.py — Cisco Packet Tracer IOS CLI Script Writer / Generator
Generates clean, copy-pasteable Cisco IOS commands with Bangla explanations!

Usage examples:
  python3 scripts/ios_config_generator.py --list
  python3 scripts/ios_config_generator.py router-basic --hostname LAB-R1 --ip 192.168.1.1/24
  python3 scripts/ios_config_generator.py dhcp --pool OFFICE --network 192.168.10.0/24 --dns 192.168.10.100
  python3 scripts/ios_config_generator.py roas --vlans "10:CSE:192.168.10.0/24,20:EEE:192.168.20.0/24" --with-dhcp
  python3 scripts/ios_config_generator.py static-routing
  python3 scripts/ios_config_generator.py vlan-switch
  python3 scripts/ios_config_generator.py port-security --port "fastEthernet 0/1" --max-mac 1
  python3 scripts/ios_config_generator.py etherchannel
  python3 scripts/ios_config_generator.py acl-nat
"""

import argparse
import ipaddress
import sys


def parse_net(cidr: str) -> ipaddress.IPv4Network:
    return ipaddress.IPv4Network(cidr, strict=False)


def parse_iface_ip(cidr: str) -> tuple[str, str]:
    iface = ipaddress.IPv4Interface(cidr)
    return str(iface.ip), str(iface.network.netmask)


def gen_router_basic(args: argparse.Namespace) -> str:
    ip_str, mask_str = parse_iface_ip(args.ip)
    lines = [
        f"! =====================================================",
        f"! Basic Router Configuration — Hostname: {args.hostname}",
        f"! Paste directly into Cisco Packet Tracer Router CLI",
        f"! =====================================================",
        "enable",
        "configure terminal",
        f"hostname {args.hostname}",
        "! ভুল টাইপে DNS খোঁজা বন্ধ রাখা (CLI ফ্রিজ হবে না)",
        "no ip domain-lookup",
        f"enable secret {args.secret}",
        "service password-encryption",
        f'banner motd # Authorized Access Only - {args.hostname} #',
        "!",
        f"! LAN Interface ({args.interface}) কনফিগারেশন",
        f"interface {args.interface}",
        f" ip address {ip_str} {mask_str}",
        " description Connected_to_LAN_Switch",
        " no shutdown",
        " exit",
        "!",
        "end",
        "copy running-config startup-config",
        "",
        "! --- যাচাই কমান্ড (Verification) ---",
        "! show ip interface brief",
        "! show running-config",
    ]
    return "\n".join(lines)


def gen_static_routing(args: argparse.Namespace) -> str:
    lan1 = parse_net(args.lan1)
    lan2 = parse_net(args.lan2)
    wan = parse_net(args.wan)
    r1_lan = str(lan1.network_address + 1)
    r2_lan = str(lan2.network_address + 1)
    r1_wan = str(wan.network_address + 1)
    r2_wan = str(wan.network_address + 2)

    return f"""! =====================================================
! Two-Router Static Routing Configuration (R1 & R2)
! LAN 1: {lan1} | WAN: {wan} | LAN 2: {lan2}
! =====================================================

! ---------------- [ Router R1 CLI ] ----------------
enable
configure terminal
hostname R1
interface gigabitEthernet 0/0
 ip address {r1_lan} {lan1.netmask}
 no shutdown
 exit
interface gigabitEthernet 0/1
 ip address {r1_wan} {wan.netmask}
 no shutdown
 exit
! দূরবর্তী LAN 2-তে যাওয়ার Static Route
ip route {lan2.network_address} {lan2.netmask} {r2_wan}
end
copy running-config startup-config

! ---------------- [ Router R2 CLI ] ----------------
enable
configure terminal
hostname R2
interface gigabitEthernet 0/0
 ip address {r2_lan} {lan2.netmask}
 no shutdown
 exit
interface gigabitEthernet 0/1
 ip address {r2_wan} {wan.netmask}
 no shutdown
 exit
! ফিরতি পথ (LAN 1-এ ফেরার Static Route — বাধ্যতামূলক!)
ip route {lan1.network_address} {lan1.netmask} {r1_wan}
end
copy running-config startup-config

! --- যাচাই কমান্ড ---
! show ip route
! ping {r2_lan}"""


def gen_dhcp(args: argparse.Namespace) -> str:
    net = parse_net(args.network)
    gw = args.gateway or str(net.network_address + 1)
    ex_end = str(net.network_address + args.exclude_count)
    dns_line = f"\n dns-server {args.dns}" if args.dns else ""

    return f"""! =====================================================
! Router DHCP Server Configuration — Pool: {args.pool}
! Network: {net} | Gateway: {gw}
! =====================================================
enable
configure terminal
hostname R1

interface {args.interface}
 ip address {gw} {net.netmask}
 no shutdown
 exit

! Gateway, Server ও Printer-এর Static IP সুরক্ষিত রাখা
ip dhcp excluded-address {gw} {ex_end}

ip dhcp pool {args.pool}
 network {net.network_address} {net.netmask}
 default-router {gw}{dns_line}
 exit

end
copy running-config startup-config

! --- যাচাই কমান্ড ---
! show ip dhcp binding
! show ip dhcp pool"""


def parse_vlan_specs(spec_str: str) -> list[tuple[int, str, ipaddress.IPv4Network]]:
    items = []
    for part in spec_str.split(","):
        vid_s, name, cidr = [x.strip() for x in part.strip().split(":")]
        items.append((int(vid_s), name, parse_net(cidr)))
    return items


def gen_vlan_switch(args: argparse.Namespace) -> str:
    vlans = parse_vlan_specs(args.vlans)
    lines = [
        "! =====================================================",
        f"! Switch VLAN & Trunk Configuration — {args.hostname}",
        "! =====================================================",
        "enable",
        "configure terminal",
        f"hostname {args.hostname}",
        "!",
    ]
    port_start = 1
    for vid, name, _ in vlans:
        port_end = port_start + 1
        lines.extend([
            f"vlan {vid}",
            f" name {name}",
            " exit",
            f"interface range fastEthernet 0/{port_start} - {port_end}",
            " switchport mode access",
            f" switchport access vlan {vid}",
            " spanning-tree portfast",
            " exit",
            "!",
        ])
        port_start += 2

    lines.extend([
        f"! Uplink Trunk Port ({args.trunk_port})",
        f"interface {args.trunk_port}",
        " switchport mode trunk",
        " exit",
        "end",
        "copy running-config startup-config",
        "",
        "! --- যাচাই কমান্ড ---",
        "! show vlan brief",
        "! show interfaces trunk",
    ])
    return "\n".join(lines)


def gen_roas(args: argparse.Namespace) -> str:
    vlans = parse_vlan_specs(args.vlans)
    sw_cfg = gen_vlan_switch(
        argparse.Namespace(hostname="SW1", vlans=args.vlans, trunk_port="gigabitEthernet 0/1")
    )
    r_lines = [
        "",
        "! =====================================================",
        f"! Router-on-a-Stick (ROAS) Configuration — R1 ({args.parent_if})",
        "! =====================================================",
        "enable",
        "configure terminal",
        "hostname R1",
        "!",
        f"! মূল ফিজিক্যাল পোর্টে কোনো IP বসবে না, শুধু no shutdown!",
        f"interface {args.parent_if}",
        " no shutdown",
        " exit",
        "!",
    ]
    short_if = args.parent_if
    for vid, name, net in vlans:
        gw = str(net.network_address + 1)
        r_lines.extend([
            f"! Subinterface for VLAN {vid} ({name})",
            f"interface {short_if}.{vid}",
            f" encapsulation dot1Q {vid}",
            f" ip address {gw} {net.netmask}",
            " exit",
            "!",
        ])
        if args.with_dhcp:
            ex_end = str(net.network_address + 10)
            r_lines.extend([
                f"ip dhcp excluded-address {gw} {ex_end}",
                f"ip dhcp pool VLAN_{vid}_{name.upper()}",
                f" network {net.network_address} {net.netmask}",
                f" default-router {gw}",
                " exit",
                "!",
            ])

    r_lines.extend([
        "end",
        "copy running-config startup-config",
        "",
        "! --- যাচাই কমান্ড ---",
        "! show ip interface brief",
        "! show ip route",
    ])
    return sw_cfg + "\n" + "\n".join(r_lines)


def gen_port_security(args: argparse.Namespace) -> str:
    return f"""! =====================================================
! Switch Port Security Configuration ({args.port})
! =====================================================
enable
configure terminal

interface {args.port}
 switchport mode access
 switchport port-security
 switchport port-security maximum {args.max_mac}
 switchport port-security mac-address sticky
 switchport port-security violation {args.violation}
 exit

end
copy running-config startup-config

! --- যাচাই ও Recovery কমান্ড ---
! show port-security interface {args.port}
! show port-security address
! (যদি err-disabled হয়: interface {args.port} -> shutdown -> no shutdown)"""


def gen_etherchannel(args: argparse.Namespace) -> str:
    return f"""! =====================================================
! LACP EtherChannel Configuration (SW1 & SW2)
! Ports: {args.port_range} -> Port-channel 1 (Trunk)
! =====================================================
! (SW1 এবং SW2 — উভয় সুইচেই নিচের কমান্ড চালাও)

enable
configure terminal

interface range {args.port_range}
 channel-group 1 mode active
 exit

interface port-channel 1
 switchport mode trunk
 exit

end
copy running-config startup-config

! --- যাচাই কমান্ড ---
! show etherchannel summary   (Po1-এর পাশে '(SU)' দেখাতে হবে)"""


def gen_acl_nat(args: argparse.Namespace) -> str:
    return f"""! =====================================================
! PAT (NAT Overload) + Extended ACL Template
! Inside LAN: {args.inside_net} | Inside IF: g0/0 | Outside IF: g0/1
! =====================================================
enable
configure terminal
hostname EDGE-R1

interface gigabitEthernet 0/0
 ip nat inside
 exit

interface gigabitEthernet 0/1
 ip nat outside
 exit

! NAT-এর জন্য প্রাইভেট নেটওয়ার্ক চিহ্নিত করা
access-list 1 permit 192.168.10.0 0.0.0.255

! PAT Overload সক্রিয় করা
ip nat inside source list 1 interface gigabitEthernet 0/1 overload

! উদাহরণ Extended ACL: একটি নির্দিষ্ট হোস্টের HTTP ব্লক রেখে বাকি সব চালু
ip access-list extended LAN_FILTER
 deny tcp host 192.168.10.50 any eq 80
 permit ip any any
 exit

interface gigabitEthernet 0/0
 ip access-group LAN_FILTER in
 exit

end
copy running-config startup-config

! --- যাচাই কমান্ড ---
! show ip nat translations
! show access-lists"""


PRESETS_INFO = [
    ("router-basic", "Hostname, passwords, banner ও LAN interface কনফিগ (লেসন ০১)"),
    ("static-routing", "দুটি রাউটারের পূর্ণ দ্বিমুখী Static Route কনফিগ (লেসন ০২)"),
    ("dhcp", "Excluded IP সহ Router DHCP Pool কনফিগ (লেসন ০৩–০৪)"),
    ("vlan-switch", "Switch VLAN, Access Range ও Trunk পোর্ট কনফিগ (লেসন ০৫–০৬)"),
    ("roas", "Router-on-a-Stick Inter-VLAN + ঐচ্ছিক DHCP কনফিগ (লেসন ০৬, ০৮)"),
    ("port-security", "Sticky MAC Port Security ও Recovery কনফিগ (লেসন ০৭)"),
    ("etherchannel", "LACP EtherChannel (Port-channel 1) কনফিগ (লেসন ০৭)"),
    ("acl-nat", "PAT (NAT Overload) ও Extended ACL টেমপ্লেট (CCNA ০৭)"),
]


def strip_comments(cfg: str) -> str:
    return "\n".join(l for l in cfg.splitlines() if not l.strip().startswith("!"))


def main() -> int:
    if "--list" in sys.argv:
        print("🛠️  উপলব্ধ Cisco IOS কনফিগারেশন টেমপ্লেটসমূহ:\n")
        for name, desc in PRESETS_INFO:
            print(f"  • {name:16s} — {desc}")
        print("\nউদাহরণ: python3 scripts/ios_config_generator.py roas --with-dhcp")
        return 0

    parser = argparse.ArgumentParser(
        description="Cisco Packet Tracer IOS CLI Configuration Generator"
    )
    parser.add_argument("--no-comments", action="store_true", help="Remove '!' comment lines")
    parser.add_argument("--save-to", default="", help="Save generated CLI script to a file")

    sub = parser.add_subparsers(dest="preset", required=True)

    p1 = sub.add_parser("router-basic", help="Basic router setup")
    p1.add_argument("--hostname", default="R1")
    p1.add_argument("--interface", default="gigabitEthernet 0/0")
    p1.add_argument("--ip", default="192.168.1.1/24")
    p1.add_argument("--secret", default="cisco123")

    p2 = sub.add_parser("static-routing", help="Two-router static routing")
    p2.add_argument("--lan1", default="192.168.1.0/24")
    p2.add_argument("--lan2", default="192.168.2.0/24")
    p2.add_argument("--wan", default="10.0.0.0/30")

    p3 = sub.add_parser("dhcp", help="Router DHCP pool")
    p3.add_argument("--pool", default="OFFICE")
    p3.add_argument("--network", default="192.168.1.0/24")
    p3.add_argument("--interface", default="gigabitEthernet 0/0")
    p3.add_argument("--gateway", default="")
    p3.add_argument("--dns", default="192.168.1.100")
    p3.add_argument("--exclude-count", type=int, default=10)

    p4 = sub.add_parser("vlan-switch", help="Switch VLANs + Trunk")
    p4.add_argument("--hostname", default="SW1")
    p4.add_argument("--vlans", default="10:CSE:192.168.10.0/24,20:EEE:192.168.20.0/24")
    p4.add_argument("--trunk-port", default="gigabitEthernet 0/1")

    p5 = sub.add_parser("roas", help="Router-on-a-Stick Inter-VLAN routing")
    p5.add_argument("--parent-if", default="gigabitEthernet 0/0")
    p5.add_argument("--vlans", default="10:CSE:192.168.10.0/24,20:EEE:192.168.20.0/24")
    p5.add_argument("--with-dhcp", action="store_true", help="Include per-VLAN DHCP pools")

    p6 = sub.add_parser("port-security", help="Switch Port Security")
    p6.add_argument("--port", default="fastEthernet 0/1")
    p6.add_argument("--max-mac", type=int, default=1)
    p6.add_argument("--violation", choices=["shutdown", "restrict", "protect"], default="shutdown")

    p7 = sub.add_parser("etherchannel", help="LACP EtherChannel")
    p7.add_argument("--port-range", default="gigabitEthernet 0/1 - 2")

    p8 = sub.add_parser("acl-nat", help="PAT Overload + Extended ACL")
    p8.add_argument("--inside-net", default="192.168.10.0/24")

    args = parser.parse_args()
    dispatch = {
        "router-basic": gen_router_basic,
        "static-routing": gen_static_routing,
        "dhcp": gen_dhcp,
        "vlan-switch": gen_vlan_switch,
        "roas": gen_roas,
        "port-security": gen_port_security,
        "etherchannel": gen_etherchannel,
        "acl-nat": gen_acl_nat,
    }
    output = dispatch[args.preset](args)
    if args.no_comments:
        output = strip_comments(output)

    if args.save_to:
        with open(args.save_to, "w", encoding="utf-8") as fh:
            fh.write(output + "\n")
        print(f"✅ CLI কনফিগ ফাইল সেভ হয়েছে: {args.save_to}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
