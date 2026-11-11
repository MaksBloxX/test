#!/usr/bin/env python3
"""
ios_config_generator.py — Cisco Packet Tracer IOS CLI Script Writer / Generator (v3.0)
Generates clean, copy-pasteable Cisco IOS commands with Bangla explanations!
Phase 3 presets are scoped to ONE --role/device per invocation; no .pkt is generated.

Usage examples:
  python3 scripts/ios_config_generator.py --list
  python3 scripts/ios_config_generator.py ospf --router-id 1.1.1.1 --networks "192.168.1.0/24,10.0.12.0/30"
  python3 scripts/ios_config_generator.py ripv2 --networks "192.168.1.0,10.0.0.0"
  python3 scripts/ios_config_generator.py ssh-hardening --hostname R1 --domain office.local
  python3 scripts/ios_config_generator.py broken-lab --case 5
  python3 scripts/ios_config_generator.py roas --vlans "10:CSE:192.168.10.0/24,20:EEE:192.168.20.0/24" --with-dhcp
  python3 scripts/ios_config_generator.py svi-switch
  python3 scripts/ios_config_generator.py hsrp --role R2
  python3 scripts/ios_config_generator.py ospfv3 --role R1
  python3 scripts/ios_config_generator.py voip-cme --role SW1
  python3 scripts/ios_config_generator.py dhcp-snooping --role SW1
"""

import argparse
import ipaddress
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def parse_net(cidr: str) -> ipaddress.IPv4Network:
    return ipaddress.IPv4Network(cidr, strict=False)


def parse_iface_ip(cidr: str) -> tuple[str, str]:
    iface = ipaddress.IPv4Interface(cidr)
    return str(iface.ip), str(iface.network.netmask)


def gen_router_basic(args: argparse.Namespace) -> str:
    ip_str, mask_str = parse_iface_ip(args.ip)
    lines = [
        "! =====================================================",
        f"! Basic Router Configuration — Hostname: {args.hostname}",
        "! Paste directly into Cisco Packet Tracer Router CLI",
        "! =====================================================",
        "enable",
        "configure terminal",
        f"hostname {args.hostname}",
        "! ভুল টাইপে DNS খোঁজা বন্ধ রাখা (CLI ফ্রিজ হবে না)",
        "no ip domain-lookup",
        f"enable secret {args.secret}",
        "service password-encryption",
        f"banner motd # Authorized Access Only - {args.hostname} #",
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
        "! মূল ফিজিক্যাল পোর্টে কোনো IP বসবে না, শুধু no shutdown!",
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


def gen_ospf(args: argparse.Namespace) -> str:
    nets = [parse_net(x.strip()) for x in args.networks.split(",") if x.strip()]
    lines = [
        "! =====================================================",
        f"! Single-Area OSPFv2 Configuration — {args.hostname} (Area {args.area})",
        "! Wildcard Masks স্বয়ংক্রিয়ভাবে হিসাব করা হয়েছে!",
        "! =====================================================",
        "enable",
        "configure terminal",
        f"hostname {args.hostname}",
        f"router ospf {args.process_id}",
        f" router-id {args.router_id}",
    ]
    if args.passive:
        lines.append(f" passive-interface {args.passive}")
    for n in nets:
        lines.append(f" network {n.network_address} {n.hostmask} area {args.area}")
    lines.extend([
        " exit",
        "end",
        "copy running-config startup-config",
        "",
        "! --- যাচাই কমান্ড ---",
        "! show ip ospf neighbor",
        "! show ip route ospf",
        "! show ip protocols",
    ])
    return "\n".join(lines)


def gen_ripv2(args: argparse.Namespace) -> str:
    nets = [x.strip() for x in args.networks.split(",") if x.strip()]
    lines = [
        "! =====================================================",
        f"! RIPv2 Dynamic Routing Configuration — {args.hostname}",
        "! =====================================================",
        "enable",
        "configure terminal",
        f"hostname {args.hostname}",
        "router rip",
        " version 2",
        " no auto-summary",
    ]
    if args.passive:
        lines.append(f" passive-interface {args.passive}")
    for n in nets:
        lines.append(f" network {n}")
    lines.extend([
        " exit",
        "end",
        "copy running-config startup-config",
        "",
        "! --- যাচাই কমান্ড ---",
        "! show ip route rip",
        "! show ip protocols",
    ])
    return "\n".join(lines)


def gen_ssh_hardening(args: argparse.Namespace) -> str:
    ip_str, mask_str = parse_iface_ip(args.ip)
    return f"""! =====================================================
! SSHv2 + Device Hardening + NTP + Syslog — {args.hostname}
! =====================================================
enable
configure terminal
hostname {args.hostname}
ip domain-name {args.domain}
no ip domain-lookup

interface {args.interface}
 ip address {ip_str} {mask_str}
 no shutdown
 exit

enable secret {args.secret}
username {args.user} secret {args.user_pass}
service password-encryption
banner motd # WARNING: Authorized Admins Only! All activity logged. #

! RSA 2048-bit চাবি ও SSHv2 সক্রিয়করণ (প্রম্পট এলে 2048 লিখবে)
crypto key generate rsa
2048
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

line console 0
 login local
 logging synchronous
 exec-timeout 5 0
 exit

line vty 0 4
 transport input ssh
 login local
 logging synchronous
 exec-timeout 5 0
 exit

! NTP ও Syslog সার্ভার যুক্তকরণ
ntp server {args.server_ip}
service timestamps log datetime msec
logging host {args.server_ip}
logging trap informational

end
copy running-config startup-config

! --- যাচাই কমান্ড ---
! PC থেকে: ssh -l {args.user} {ip_str}
! রাউটারে: show ip ssh | show ntp status"""


def phase3_script(title: str, role: str, config: str, checks: list[str], note: str = "") -> str:
    """One device per output: never silently concatenate two devices' CLI."""
    header = (f"! [v3.0] {title} | ONLY {role} CLI\n"
              f"! নিজে Packet Tracer-এ পোর্ট/IP পরীক্ষা করে {role}-তে পেস্ট করো; .pkt তৈরি হয় না।\n")
    if note:
        header += f"! সতর্কতা: {note}\n"
    tail = "\n".join("! " + check for check in checks)
    return (header + "enable\nconfigure terminal\n" + config.strip() +
            "\nend\ncopy running-config startup-config\n\n! --- যাচাই কমান্ড ---\n" + tail)


def gen_svi_switch(args: argparse.Namespace) -> str:
    return phase3_script("Lesson 16: 3560 SVI inter-VLAN", "SW1", """
hostname SW1
vlan 10
 name CSE
exit
vlan 20
 name EEE
exit
interface range fastEthernet 0/1 - 2
 switchport mode access
 switchport access vlan 10
 no shutdown
exit
interface range fastEthernet 0/3 - 4
 switchport mode access
 switchport access vlan 20
 no shutdown
exit
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit
ip routing
""", ["show vlan brief", "show ip interface brief", "show ip route",
        "PC0 192.168.10.10 gateway .10.1 -> PC2 192.168.20.10 gateway .20.1"])


def gen_hsrp(args: argparse.Namespace) -> str:
    if args.role == "R3":
        return phase3_script("Lesson 17: upstream return routes", "R3", """
hostname R3
interface gigabitEthernet 0/0
 ip address 10.0.13.2 255.255.255.252
 no shutdown
exit
interface gigabitEthernet 0/1
 ip address 10.0.23.2 255.255.255.252
 no shutdown
exit
interface loopback 0
 ip address 198.51.100.10 255.255.255.255
exit
ip route 192.168.50.0 255.255.255.0 10.0.13.1
ip route 192.168.50.0 255.255.255.0 10.0.23.1
""", ["show ip route 192.168.50.0", "198.51.100.10 is a test loopback, NOT Internet"])
    lan_ip = "192.168.50.2" if args.role == "R1" else "192.168.50.3"
    wan_id = "13" if args.role == "R1" else "23"
    priority = "120" if args.role == "R1" else "100"
    return phase3_script("Lesson 17: HSRP gateway", args.role, f"""
hostname {args.role}
interface gigabitEthernet 0/0
 ip address {lan_ip} 255.255.255.0
 standby 1 ip 192.168.50.1
 standby 1 priority {priority}
 standby 1 preempt
 no shutdown
exit
interface gigabitEthernet 0/1
 ip address 10.0.{wan_id}.1 255.255.255.252
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 10.0.{wan_id}.2
""", ["show standby brief", "show ip route", "PC0 gateway must be virtual 192.168.50.1"])


def gen_ipv6_static(args: argparse.Namespace) -> str:
    if args.role == "R1":
        lan, local, wan, target, via = "10", "1", "1", "20", "2"
    else:
        lan, local, wan, target, via = "20", "2", "2", "10", "1"
    return phase3_script("Lesson 18: IPv6 SLAAC + static stage", args.role, f"""
hostname {args.role}
ipv6 unicast-routing
interface gigabitEthernet 0/0
 ipv6 address 2001:db8:{lan}::1/64
 ipv6 address fe80::{local} link-local
 no shutdown
exit
interface gigabitEthernet 0/1
 ipv6 address 2001:db8:12::{wan}/64
 no shutdown
exit
ipv6 route 2001:db8:{target}::/64 2001:db8:12::{via}
""", ["show ipv6 interface brief", "show ipv6 route",
        "PC0 auto IPv6, PC1 static 2001:db8:20::10/64, gateway fe80::2"])


def gen_ospfv3(args: argparse.Namespace) -> str:
    if args.role == "R1":
        remote, next_hop, rid = "20", "2", "1.1.1.1"
    else:
        remote, next_hop, rid = "10", "1", "2.2.2.2"
    return phase3_script("Lesson 18: OSPFv3 stage (after IPv6 static)", args.role, f"""
no ipv6 route 2001:db8:{remote}::/64 2001:db8:12::{next_hop}
ipv6 router ospf 10
 router-id {rid}
exit
interface gigabitEthernet 0/0
 ipv6 ospf 10 area 0
exit
interface gigabitEthernet 0/1
 ipv6 ospf 10 area 0
exit
""", ["show ipv6 ospf neighbor", "show ipv6 route (remote LAN code O)",
        "ping 2001:db8:20::10 from PC0"],
        "আগে ipv6-static --role ... চালানো থাকতে হবে; static route সরানো হয়।")


def gen_voip_cme(args: argparse.Namespace) -> str:
    if args.role == "SW1":
        return phase3_script("Extra 07: voice+data VLAN", "SW1", """
hostname SW1
vlan 10
 name DATA
exit
vlan 20
 name VOICE
exit
interface gigabitEthernet 0/1
 switchport mode trunk
 no shutdown
exit
interface fastEthernet 0/1
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 spanning-tree portfast
 no shutdown
exit
interface fastEthernet 0/2
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 spanning-tree portfast
 no shutdown
exit
""", ["show interfaces trunk", "show vlan brief", "Phone ports are access+voice, not trunks"])
    return phase3_script("Extra 07: 2811 CME and DHCP option 150", "R1", """
hostname R1
interface fastEthernet 0/0
 no ip address
 no shutdown
exit
interface fastEthernet 0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
exit
interface fastEthernet 0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
exit
ip dhcp excluded-address 192.168.20.1 192.168.20.20
ip dhcp pool VOICE
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 option 150 ip 192.168.20.1
exit
telephony-service
 max-ephones 2
 max-dn 2
 ip source-address 192.168.20.1 port 2000
 auto assign 1 to 2
exit
ephone-dn 1
 number 1001
exit
ephone-dn 2
 number 1002
exit
""", ["show ip dhcp binding", "Check phone screens for actual extension order",
                 "Call the other extension (1001 <-> 1002)"])


def gen_dhcp_snooping(args: argparse.Namespace) -> str:
    if args.role == "R1":
        return phase3_script("Extra 08: legitimate DHCP server", "R1", """
hostname R1
interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit
ip dhcp excluded-address 192.168.1.1 192.168.1.20
ip dhcp excluded-address 192.168.1.254
ip dhcp pool SAFE_LAN
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
exit
""", ["show ip dhcp binding", "RogueServer DHCP must start OFF"])
    return phase3_script("Extra 08: VLAN 1 DHCP Snooping", "SW1", """
hostname SW1
ip dhcp snooping
ip dhcp snooping vlan 1
no ip dhcp snooping information option
interface gigabitEthernet 0/1
 ip dhcp snooping trust
 no shutdown
exit
interface fastEthernet 0/1
 switchport mode access
 switchport access vlan 1
 no shutdown
exit
interface fastEthernet 0/2
 switchport mode access
 switchport access vlan 1
 no shutdown
exit
interface fastEthernet 0/3
 switchport mode access
 switchport access vlan 1
 no shutdown
exit
""", ["show ip dhcp snooping", "show ip dhcp snooping binding",
                 "Never trust PC or RogueServer ports"])


def gen_dai(args: argparse.Namespace) -> str:
    return phase3_script("Extra 08: DAI policy (optional emulator feature)", "SW1", """
ip arp inspection vlan 1
interface gigabitEthernet 0/1
 ip arp inspection trust
exit
""", ["show ip arp inspection", "show ip arp inspection interfaces",
        "show ip arp inspection statistics", "Rollback: no ip arp inspection vlan 1"],
        "শুধু DHCP Snooping binding নিশ্চিত হওয়ার পরে। PT DAI traffic drop নাও করতে পারে।")


def gen_broken_lab(args: argparse.Namespace) -> str:
    files = {
        1: ("broken-01-static-routing.ios", "R2 CLI (lesson-02-static-routing.pkt)"),
        2: ("broken-02-dhcp-starvation.ios", "R1 CLI (lesson-03-dhcp.pkt)"),
        3: ("broken-03-roas-vlan.ios", "R1 CLI (lesson-06-trunk-inter-vlan.pkt)"),
        4: ("broken-04-etherchannel-stp.ios", "SW1 & SW2 CLI (lesson-07-switching.pkt)"),
        5: ("broken-05-ospf-adjacency.ios", "R2 CLI (লেসন ১৩ · OSPF টপোলজি)"),
        6: ("broken-06-ssh-lockout.ios", "R1 CLI (লেসন ১৫ · SSH টপোলজি)"),
    }
    fn, target = files[args.case]
    path = os.path.join(REPO_ROOT, "pkt-files", "troubleshooting", fn)
    body = open(path, encoding="utf-8").read().strip()
    return (
        f"! 🕵️ Mystery Broken Lab — Case {args.case:02d}\n"
        f"! নিচের লাইনগুলো না পড়ে সরাসরি পেস্ট করো: {target}\n"
        f"! তারপর 'show' কমান্ড দিয়ে নিজে বাগ খুঁজে ঠিক করো!\n\n{body}"
    )


PRESETS_INFO = [
    ("router-basic", "Hostname, passwords, banner ও LAN interface কনফিগ (লেসন ০১)"),
    ("static-routing", "দুটি রাউটারের পূর্ণ দ্বিমুখী Static Route কনফিগ (লেসন ০২)"),
    ("dhcp", "Excluded IP সহ Router DHCP Pool কনফিগ (লেসন ০৩–০৪)"),
    ("vlan-switch", "Switch VLAN, Access Range ও Trunk পোর্ট কনফিগ (লেসন ০৫–০৬)"),
    ("roas", "Router-on-a-Stick Inter-VLAN + ঐচ্ছিক DHCP কনফিগ (লেসন ০৬, ০৮)"),
    ("port-security", "Sticky MAC Port Security ও Recovery কনফিগ (লেসন ০৭)"),
    ("etherchannel", "LACP EtherChannel (Port-channel 1) কনফিগ (লেসন ০৭)"),
    ("acl-nat", "PAT (NAT Overload) ও Extended ACL টেমপ্লেট (CCNA ০৭)"),
    ("ospf", "[v2.5] অটো Wildcard Mask সহ Single-Area OSPFv2 কনফিগ (লেসন ১৩)"),
    ("ripv2", "[v2.5] RIPv2 ডায়নামিক রাউটিং কনফিগ (লেসন ১৩)"),
    ("ssh-hardening", "[v2.5] SSHv2 + RSA + Hardening + NTP + Syslog কনফিগ (লেসন ১৫)"),
    ("broken-lab", "[v2.5] ট্রাবলশুটিং অনুশীলনের জন্য ৬টি রহস্যময় ভাঙা কনফিগ (Case 1–6)"),
    ("svi-switch", "[v3.0] 3560 SVI + ip routing: লেসন ১৬ (SW1)"),
    ("hsrp", "[v3.0] Virtual gateway + return path: লেসন ১৭ (--role R1/R2/R3)"),
    ("ipv6-static", "[v3.0] IPv6 SLAAC + দ্বিমুখী static route: লেসন ১৮ (--role R1/R2)"),
    ("ospfv3", "[v3.0] Static সরিয়ে OSPFv3: লেসন ১৮ (--role R1/R2)"),
    ("voip-cme", "[v3.0] 2811 CME + voice VLAN: Extra ০৭ (--role R1/SW1)"),
    ("dhcp-snooping", "[v3.0] বৈধ DHCP + L2 trust: Extra ০৮ (--role R1/SW1)"),
    ("dai", "[v3.0] DHCP binding-এর পরে ঐচ্ছিক DAI: Extra ০৮ (--role SW1)"),
]


def strip_comments(cfg: str) -> str:
    return "\n".join(l for l in cfg.splitlines() if not l.strip().startswith("!"))


def main() -> int:
    if "--list" in sys.argv:
        print(f"🛠️  উপলব্ধ Cisco IOS কনফিগারেশন টেমপ্লেটসমূহ (v3.0 — মোট {len(PRESETS_INFO)}টি):\n")
        for name, desc in PRESETS_INFO:
            print(f"  • {name:16s} — {desc}")
        print("\nউদাহরণ: python3 scripts/ios_config_generator.py hsrp --role R1")
        return 0

    parser = argparse.ArgumentParser(
        description="Cisco Packet Tracer IOS CLI Configuration Generator (v3.0)"
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

    p9 = sub.add_parser("ospf", help="Single-Area OSPFv2 routing")
    p9.add_argument("--hostname", default="R1")
    p9.add_argument("--process-id", type=int, default=1)
    p9.add_argument("--router-id", default="1.1.1.1")
    p9.add_argument("--area", type=int, default=0)
    p9.add_argument("--passive", default="gigabitEthernet 0/0")
    p9.add_argument("--networks", default="192.168.1.0/24,10.0.12.0/30,10.0.13.0/30")

    p10 = sub.add_parser("ripv2", help="RIPv2 dynamic routing")
    p10.add_argument("--hostname", default="R1")
    p10.add_argument("--passive", default="gigabitEthernet 0/0")
    p10.add_argument("--networks", default="192.168.1.0,10.0.0.0")

    p11 = sub.add_parser("ssh-hardening", help="SSHv2 + Hardening + NTP + Syslog")
    p11.add_argument("--hostname", default="R1")
    p11.add_argument("--domain", default="office.local")
    p11.add_argument("--interface", default="gigabitEthernet 0/0")
    p11.add_argument("--ip", default="192.168.1.1/24")
    p11.add_argument("--secret", default="EnablePass123!")
    p11.add_argument("--user", default="admin")
    p11.add_argument("--user-pass", default="AdminPass123!")
    p11.add_argument("--server-ip", default="192.168.1.100")

    p12 = sub.add_parser("broken-lab", help="Fault-injection broken config for detective practice")
    p12.add_argument("--case", type=int, choices=[1, 2, 3, 4, 5, 6], default=1)

    sub.add_parser("svi-switch", help="Lesson 16: multilayer 3560 SW1 SVI routing")
    hsrp = sub.add_parser("hsrp", help="Lesson 17: one HSRP/router role per call")
    hsrp.add_argument("--role", choices=["R1", "R2", "R3"], default="R1")
    ip6 = sub.add_parser("ipv6-static", help="Lesson 18: IPv6 interface and static routes")
    ip6.add_argument("--role", choices=["R1", "R2"], default="R1")
    ospf3 = sub.add_parser("ospfv3", help="Lesson 18: remove static, enable OSPFv3")
    ospf3.add_argument("--role", choices=["R1", "R2"], default="R1")
    voip = sub.add_parser("voip-cme", help="Extra 07: 2811 CME or voice VLAN switch")
    voip.add_argument("--role", choices=["R1", "SW1"], default="R1")
    snoop = sub.add_parser("dhcp-snooping", help="Extra 08: legit DHCP or access switch")
    snoop.add_argument("--role", choices=["R1", "SW1"], default="SW1")
    dai = sub.add_parser("dai", help="Extra 08: optional DAI after bindings are learned")
    dai.add_argument("--role", choices=["SW1"], default="SW1")

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
        "ospf": gen_ospf,
        "ripv2": gen_ripv2,
        "ssh-hardening": gen_ssh_hardening,
        "broken-lab": gen_broken_lab,
        "svi-switch": gen_svi_switch,
        "hsrp": gen_hsrp,
        "ipv6-static": gen_ipv6_static,
        "ospfv3": gen_ospfv3,
        "voip-cme": gen_voip_cme,
        "dhcp-snooping": gen_dhcp_snooping,
        "dai": gen_dai,
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
