#!/usr/bin/env python3
"""
subnet_calculator.py — IPv4 Subnetting, VLSM Planner & Exam Drill Tool
Cisco-Packet-Tracer-Lab Helper Script (Bangla + English)

Usage examples:
  # 1) Detailed single-subnet analysis (supports host IP or network IP!)
  python3 scripts/subnet_calculator.py 192.168.1.65/26

  # 2) Split a parent network into smaller equal subnets
  python3 scripts/subnet_calculator.py --split 192.168.1.0/24 --new-prefix 26

  # 3) VLSM Planner (auto-sorts largest department first + generates Markdown table!)
  python3 scripts/subnet_calculator.py --vlsm 192.168.10.0/24 \
      --departments "CSE:55,EEE:25,Admin:10,WAN:2"

  # 4) Subnetting Practice Drill Generator (exam preparation!)
  python3 scripts/subnet_calculator.py --drill 5
"""

import argparse
import ipaddress
import math
import random
import sys


def to_dotted_binary(ip: ipaddress.IPv4Address) -> str:
    return ".".join(f"{b:08b}" for b in ip.packed)


def analyze_cidr(cidr_str: str) -> None:
    iface = ipaddress.IPv4Interface(cidr_str)
    net = iface.network
    prefix = net.prefixlen
    host_bits = 32 - prefix
    total_addrs = net.num_addresses

    if prefix == 32:
        usable = 1
        first_host = last_host = str(net.network_address)
    elif prefix == 31:
        usable = 2
        first_host = str(net.network_address)
        last_host = str(net.broadcast_address)
    else:
        usable = max(0, total_addrs - 2)
        first_host = str(net.network_address + 1)
        last_host = str(net.broadcast_address - 1)

    # Magic block size in the interesting octet
    mask_octets = [int(x) for x in str(net.netmask).split(".")]
    interesting_octet = next((o for o in mask_octets if o < 255), 255)
    block_size = 256 - interesting_octet if prefix < 32 else 1

    print("=" * 66)
    print(f"🧮 IPv4 Subnet বিশ্লেষণ (Input: {cidr_str})")
    print("=" * 66)
    print(f"  • প্রদত্ত IP ঠিকানা      : {iface.ip}")
    print(f"  • Network ID           : {net.network_address}/{prefix}")
    print(f"  • Subnet Mask          : {net.netmask}  (/{prefix})")
    print(f"  • Wildcard Mask (ACL)  : {net.hostmask}")
    print(f"  • Broadcast Address    : {net.broadcast_address}")
    print(f"  • প্রথম Usable Host     : {first_host}")
    print(f"  • শেষ Usable Host       : {last_host}")
    print(f"  • Host Bits (h)        : 32 - {prefix} = {host_bits} bits")
    print(f"  • মোট ঠিকানা (2^h)      : {total_addrs}")
    print(f"  • ব্যবহারযোগ্য হোস্ট      : {usable}  (সূত্র: 2^{host_bits} - 2)")
    print(f"  • Magic Block Size     : {block_size}  (256 - {interesting_octet})")
    print(f"  • ঠিকানার ধরন           : {'Private (RFC 1918)' if net.is_private else 'Public / Special'}")
    print("-" * 66)
    print("🔬 Binary রূপ (Network বনাম Host অংশ):")
    print(f"  IP Binary   : {to_dotted_binary(iface.ip)}")
    print(f"  Mask Binary : {to_dotted_binary(net.netmask)}")
    print(f"  Net Binary  : {to_dotted_binary(net.network_address)}")
    print("=" * 66)


def split_network(parent_str: str, new_prefix: int) -> None:
    parent = ipaddress.IPv4Network(parent_str, strict=False)
    if new_prefix <= parent.prefixlen or new_prefix > 30:
        raise ValueError(f"নতুন prefix (/{new_prefix}) অবশ্যই /{parent.prefixlen + 1} থেকে /30 এর মধ্যে হতে হবে।")
    borrowed = new_prefix - parent.prefixlen
    subs = list(parent.subnets(new_prefix=new_prefix))
    print(f"\n📐 `{parent}` কে `/{new_prefix}`-এ ভাগ করার ফলাফল:")
    print(f"• ধার নেওয়া বিট (n) = {borrowed} → মোট সাবনেট = 2^{borrowed} = {len(subs)} টি\n")
    print("| # | Network ID | First Host | Last Host | Broadcast IP | Usable Hosts |")
    print("| :---: | :--- | :--- | :--- | :--- | :---: |")
    for idx, s in enumerate(subs, 1):
        fh = s.network_address + 1
        lh = s.broadcast_address - 1
        print(f"| {idx} | `{s}` | `{fh}` | `{lh}` | `{s.broadcast_address}` | {s.num_addresses - 2} |")


def plan_vlsm(base_str: str, dept_str: str) -> None:
    base = ipaddress.IPv4Network(base_str, strict=False)
    reqs: list[tuple[str, int]] = []
    for item in dept_str.split(","):
        if ":" not in item:
            raise ValueError(f"ভুল ফরম্যাট '{item}' — এভাবে লেখো: 'CSE:55,EEE:25,WAN:2'")
        name, count_s = item.strip().split(":", 1)
        reqs.append((name.strip(), int(count_s.strip())))

    # VLSM golden rule: always allocate largest host requirement first!
    reqs.sort(key=lambda x: x[1], reverse=True)

    current_ip = int(base.network_address)
    base_end = int(base.broadcast_address)
    allocations = []

    for name, needed in reqs:
        if needed <= 0:
            raise ValueError("Host সংখ্যা কমপক্ষে ১ হতে হবে।")
        host_bits = max(2, math.ceil(math.log2(needed + 2)))
        prefix = 32 - host_bits
        block_size = 1 << host_bits

        # Align current_ip to block boundary if needed
        if current_ip % block_size != 0:
            current_ip = ((current_ip // block_size) + 1) * block_size

        sub = ipaddress.IPv4Network((ipaddress.IPv4Address(current_ip), prefix))
        if int(sub.broadcast_address) > base_end:
            raise ValueError(
                f"❌ `{base}` নেটওয়ার্কে জায়গা শেষ! '{name} ({needed} hosts)'-এর জন্য বড় বেস নেটওয়ার্ক নাও।"
            )
        allocations.append((name, needed, sub))
        current_ip = int(sub.broadcast_address) + 1

    print(f"\n🎯 VLSM Address Plan — Base Network: `{base}`")
    print("*(বড় চাহিদা থেকে ছোট চাহিদা অনুযায়ী স্বয়ংক্রিয়ভাবে সাজানো হয়েছে)*\n")
    print("| বিভাগ (Dept) | চাহিদা | বরাদ্দকৃত Subnet | Subnet Mask | Gateway (.1) | Usable Range | Broadcast | ক্ষমতা |")
    print("| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :---: |")
    for name, needed, sub in allocations:
        gw = sub.network_address + 1
        fh = sub.network_address + 1
        lh = sub.broadcast_address - 1
        cap = sub.num_addresses - 2
        print(
            f"| **{name}** | {needed} | `{sub}` | `{sub.netmask}` | `{gw}` | `{fh}` – `{lh}` | `{sub.broadcast_address}` | {cap} |"
        )


def generate_drills(count: int, seed: int | None = None) -> None:
    rng = random.Random(seed)
    prefixes = [25, 26, 27, 28, 29, 30]
    print(f"\n🧠 Subnetting অনুশীলন ড্রিল ({count}টি প্রশ্ন — আগে খাতায় করো, তারপর নিচে উত্তর মেলাও!)\n")
    answers = []
    for i in range(1, count + 1):
        pfx = rng.choice(prefixes)
        third = rng.randint(1, 250)
        fourth = rng.randint(1, 254)
        ip_str = f"192.168.{third}.{fourth}/{pfx}"
        iface = ipaddress.IPv4Interface(ip_str)
        net = iface.network
        print(
            f"প্রশ্ন {i}: `{ip_str}` ঠিকানাটির Network ID, Broadcast IP, Subnet Mask ও Usable Host সংখ্যা বের করো।"
        )
        answers.append(
            f"উত্তর {i} (`{ip_str}`): Network=`{net.network_address}/{pfx}` | "
            f"First=`{net.network_address + 1}` | Last=`{net.broadcast_address - 1}` | "
            f"Broadcast=`{net.broadcast_address}` | Mask=`{net.netmask}` | Usable={net.num_addresses - 2}"
        )

    print("\n" + "-" * 66)
    print("✅ উত্তরমালা (Solutions):")
    print("-" * 66)
    for ans in answers:
        print(" •", ans)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="IPv4 Subnetting, VLSM Planner & Practice Drill CLI (Bangla)"
    )
    parser.add_argument("cidr", nargs="?", help="IP/CIDR to analyze (e.g. 192.168.1.65/26)")
    parser.add_argument("--split", metavar="CIDR", help="Parent network to split (e.g. 192.168.1.0/24)")
    parser.add_argument("--new-prefix", type=int, help="Target prefix length for --split (e.g. 26)")
    parser.add_argument("--vlsm", metavar="BASE_CIDR", help="Base network for VLSM planning")
    parser.add_argument(
        "--departments",
        help="Comma-separated 'Name:HostCount' list (e.g. 'CSE:55,EEE:25,Admin:10,WAN:2')",
    )
    parser.add_argument("--drill", type=int, metavar="N", help="Generate N practice subnetting questions")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed for --drill")

    args = parser.parse_args()
    try:
        if args.vlsm:
            if not args.departments:
                parser.error("--vlsm এর সাথে --departments দেওয়া আবশ্যক")
            plan_vlsm(args.vlsm, args.departments)
        elif args.split:
            if not args.new_prefix:
                parser.error("--split এর সাথে --new-prefix দেওয়া আবশ্যক")
            split_network(args.split, args.new_prefix)
        elif args.drill:
            generate_drills(args.drill, args.seed)
        elif args.cidr:
            analyze_cidr(args.cidr)
        else:
            parser.print_help()
    except ValueError as exc:
        print(f"❌ ত্রুটি: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
