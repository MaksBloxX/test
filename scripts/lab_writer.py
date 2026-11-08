#!/usr/bin/env python3
"""
lab_writer.py — Markdown Lesson, Extra-Lab & Troubleshooting Problem Writer
Cisco-Packet-Tracer-Lab Repository Helper Tool

Usage examples:
  # 1) Create a new serial lesson template (or preview with --stdout)
  python3 scripts/lab_writer.py lesson --num 13 --slug ospf-routing \
      --title "OSPF Dynamic Routing (Single-Area)" --level "🟠 Intermediate" --time "~৫৫ মিনিট"

  # 2) Create a new Extra Lab guide in Extras/
  python3 scripts/lab_writer.py extra --slug syslog-ntp-lab \
      --title "Syslog ও NTP Server Configuration" --pkt "Syslog-NTP.pkt"

  # 3) Generate (or --append) a new Problem block for lessons/12-problem-solve.md
  python3 scripts/lab_writer.py problem --num 7 \
      --title "OSPF Neighbor তৈরি হচ্ছে না (Area/Timer Mismatch)" --stdout
"""

import argparse
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BANGLA_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def to_bn(num: int, width: int = 2) -> str:
    return f"{num:0{width}d}".translate(BANGLA_DIGITS)


def find_lesson_by_num(num: int) -> str | None:
    lessons_dir = os.path.join(REPO_ROOT, "lessons")
    if not os.path.isdir(lessons_dir):
        return None
    prefix = f"{num:02d}-"
    for fn in sorted(os.listdir(lessons_dir)):
        if fn.startswith(prefix) and fn.endswith(".md"):
            return fn
    return None


def build_lesson_markdown(args: argparse.Namespace) -> str:
    nn_en = f"{args.num:02d}"
    nn_bn = to_bn(args.num, 2)
    prev_fn = find_lesson_by_num(args.num - 1)
    next_fn = find_lesson_by_num(args.num + 1)

    nav_parts = []
    if prev_fn:
        nav_parts.append(f"[⬅ লেসন {to_bn(args.num - 1, 2)}]({prev_fn})")
    nav_parts.append("[📚 লেসন সূচি](README.md)")
    nav_parts.append("[🏠 হোম](../README.md)")
    if next_fn:
        nav_parts.append(f"[পরের লেসন {to_bn(args.num + 1, 2)} ➡]({next_fn})")
    nav_line = " · ".join(nav_parts)

    pkt_name = f"lesson-{nn_en}-{args.slug}.pkt"
    tags_list = [t.strip().lstrip("#") for t in args.tags.split(",") if t.strip()]
    tags_str = " ".join(f"`#{t}`" for t in tags_list)

    return f"""# লেসন {nn_bn} · {args.title}

> **নেভিগেশন:** {nav_line}

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| {args.goal or args.title + ' হাতে-কলমে কনফিগার ও যাচাই করা'} | {args.time} | {args.level} | [`{pkt_name}`](../pkt-files/labs/{pkt_name}) |

**Tags:** {tags_str}

---

## 🎯 এই লেসনে যা শিখবে

1. **{args.title}**-এর মূল ধারণা এবং বাস্তব নেটওয়ার্কে কেন এটি প্রয়োজন
2. Packet Tracer-এ প্রয়োজনীয় Topology ও IP Plan তৈরি করা
3. ধাপে ধাপে Cisco IOS CLI কমান্ড দিয়ে কনফিগার করা
4. `show` ও `ping` কমান্ড দিয়ে ভেরিফিকেশন সম্পন্ন করা
5. কমন ভুল ও ট্রাবলশুটিং কৌশল শেখা

### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ |
| :--- | :--- |
| **Term 1** | এখানে প্রথম নতুন টেকনিক্যাল শব্দের এক লাইনের সহজ বাংলা ব্যাখ্যা লেখো |
| **Term 2** | এখানে দ্বিতীয় টেকনিক্যাল শব্দের সহজ বাংলা ব্যাখ্যা লেখো |
| **Term 3** | এখানে তৃতীয় টেকনিক্যাল শব্দের সহজ বাংলা ব্যাখ্যা লেখো |

> 🔗 **তত্ত্ব ঝালিয়ে নিতে:** [🎓 CCNA Fundamentals](../ccna-fundamentals/README.md) · [📖 CLI Cheat-Sheet](../reference/cli-command-cheatsheet.md)

---

# 📖 Part 1 — ধারণা (Concept)

এখানে সহজ বাংলায় উদাহরণসহ মূল ধারণাটি ব্যাখ্যা করো — আগে **"কেন দরকার"**, তারপর **"কীভাবে কাজ করে"**।

```text
   [ PC0 ] ──── [ SW1 ] ──── [ R1 ] ════════ [ R2 ] ──── [ SW2 ] ──── [ PC1 ]
  192.168.1.0/24                     10.0.0.0/30                    192.168.2.0/24
```

---

# 🧩 Part 2 — Topology ও IP Addressing Plan

### 🔌 Cable Connection Table

| Device 1 | Port | Device 2 | Port | Cable Type |
| :--- | :--- | :--- | :--- | :--- |
| **PC0** | `FastEthernet0` | **SW1** | `Fa0/1` | Copper Straight-Through |
| **SW1** | `G0/1` | **R1** | `G0/0` | Copper Straight-Through |
| **R1** | `G0/1` | **R2** | `G0/1` | Copper Cross-Over |

### 📋 IP Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | `G0/0` | `192.168.1.1` | `255.255.255.0` | N/A |
| **PC0** | `Fa0` | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` |

---

# ⚙️ Part 3 — Step-by-Step CLI Configuration

### Router `R1` Configuration

```cisco
enable
configure terminal
hostname R1

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

! এখানে মূল কনফিগারেশন কমান্ড যোগ করো

end
copy running-config startup-config
```

| Command | কাজ |
| :--- | :--- |
| `enable` → `configure terminal` | Global Configuration Mode-এ প্রবেশ |
| `interface g0/0` + `no shutdown` | ইন্টারফেস সচল করা |
| `copy running-config startup-config` | NVRAM-এ স্থায়ীভাবে কনফিগ সেভ করা |

---

# 🔍 Part 4 — Verification (`show` ও `ping`)

```cisco
R1# show ip interface brief
R1# show ip route
```

**PC0 Command Prompt:**
```cmd
C:\\> ping 192.168.1.1
```

---

# 🔁 Part 5 — পর্দার আড়ালে প্যাকেট ফ্লো লজিক

```text
১. PC0 প্যাকেট তৈরি করে Default Gateway (R1)-এ পাঠায়
২. R1 টেবিল দেখে পরবর্তী ধাপে ফরওয়ার্ড করে
৩. গন্তব্য থেকে একই পথে Echo Reply ফিরে আসে ✅
```

---

# ❌ Part 6 — Troubleshooting (কমন ভুল ও সমাধান)

| সমস্যা | সম্ভাব্য কারণ | সমাধান |
| :--- | :--- | :--- |
| লিংক লাইট লাল হয়ে আছে | ইন্টারফেস বন্ধ (`shutdown`) বা কেবল ভুল | পোর্টে ঢুকে `no shutdown` চালাও |
| `Request timed out` | ফিরতি রুট বা Default Gateway মিসিং | উভয় প্রান্তে `ipconfig` ও `show ip route` মেলাও |

---

# ✅ Final Checklist

| কাজ | যাচাই কমান্ড | অবস্থা |
| :--- | :--- | :---: |
| সব ইন্টারফেসে IP ও `no shutdown` | `show ip interface brief` → `up/up` | ☐ |
| মূল ফিচার কনফিগার সম্পন্ন | `show running-config` | ☐ |
| End-to-End Ping সফল | `ping ...` → ১০০% Reply | ☐ |
| কনফিগারেশন NVRAM-এ সেভ করা | `copy run start` | ☐ |

---

> **নেভিগেশন:** {nav_line}

**এই লেসনের Tags:** {tags_str}
"""


def build_extra_lab_markdown(args: argparse.Namespace) -> str:
    tags_list = [t.strip().lstrip("#") for t in args.tags.split(",") if t.strip()]
    tags_str = " ".join(f"`#{t}`" for t in tags_list)
    pkt_file = args.pkt or f"{args.slug}.pkt"

    return f"""# 🧪 Extra Lab · {args.title}

> **নেভিগেশন:** [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [📖 Cheat-Sheet](../reference/cli-command-cheatsheet.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| {args.goal or args.title + ' হাতে-কলমে সেটআপ ও পরীক্ষা করা'} | {args.time} | {args.level} | [`{pkt_file}`](../pkt-files/practice/{pkt_file}) |

**Tags:** {tags_str}

---

## 🎯 এই ল্যাবে যা শিখবে

1. **{args.title}**-এর বাস্তব ব্যবহার ও প্রোটোকল পোর্টসমূহ
2. Topology তৈরি ও IP Addressing সেটআপ
3. Server / Router কনফিগারেশন ও ক্লায়েন্ট থেকে টেস্ট
4. ট্রাবলশুটিং ও CCNA Viva প্রশ্নোত্তর

### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ | পোর্ট / নোট |
| :--- | :--- | :--- |
| **Protocol** | প্রোটোকলের সংক্ষিপ্ত কাজ লেখো | TCP/UDP Port |

---

## ১. Network Topology ও IP Plan

```text
       [ PC0 ] ──── [ Switch 2960 ] ──── [ Router 1941 ] ──── [ Server0 ]
     192.168.1.2                           .1.1 / .2.1        192.168.2.100
```

| Device | Interface | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **Router (R1)** | `G0/0` | `192.168.1.1` | `255.255.255.0` | — |
| **Router (R1)** | `G0/1` | `192.168.2.1` | `255.255.255.0` | — |
| **Server0** | `Fa0` | `192.168.2.100` | `255.255.255.0` | `192.168.2.1` |
| **PC0** | `Fa0` | `192.168.1.2` | `255.255.255.0` | `192.168.1.1` |

---

## ২. ধাপে ধাপে কনফিগারেশন

### Router Configuration
```cisco
enable
configure terminal
hostname R1
interface g0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit
interface g0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown
 exit
end
copy running-config startup-config
```

### Server ও Client Setup
1. **Server0 → Services** ট্যাবে গিয়ে সার্ভিসটি **On** করো।
2. **PC0 → Desktop** থেকে ক্লায়েন্ট টেস্ট করো।

---

## ৩. ❌ Troubleshooting

| সমস্যা | সম্ভাব্য কারণ | সমাধান |
| :--- | :--- | :--- |
| `Connection timed out` | Gateway বা রাউটার পোর্ট ডাউন | `ping` ও `show ip int br` চেক করো |
| সার্ভিস কাজ করছে না | Server-এ Service টগল `Off` | `Services` ট্যাবে গিয়ে `On` করো |

---

## ৪. 🎓 CCNA Viva Questions

<details>
<summary><b>Q1. এই সার্ভিসটি OSI মডেলের কোন লেয়ারে এবং কোন পোর্টে কাজ করে?</b></summary>

এখানে উত্তর ও ব্যাখ্যা লেখো।
</details>

---

## ✅ Final Checklist

| কাজ | যাচাই | অবস্থা |
| :--- | :--- | :---: |
| Router ও Server IP কনফিগার | `ping 192.168.2.100` সফল | ☐ |
| মূল সার্ভিস চালু ও ক্লায়েন্ট টেস্ট | ১০০% কার্যকর | ☐ |

---

> **নেভিগেশন:** [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [📖 Cheat-Sheet](../reference/cli-command-cheatsheet.md)

**Tags:** {tags_str}
"""


def build_problem_markdown(args: argparse.Namespace) -> str:
    nn_en = f"{args.num:02d}"
    nn_bn = to_bn(args.num, 2)
    return f"""
---

<a id="problem-{nn_en}"></a>

# 🛠️ Problem {nn_bn} — {args.title}

## ❌ সমস্যা

এখানে লেখো ল্যাবে কী সমস্যা হচ্ছে এবং কোন ভুল আউটপুট দেখাচ্ছে:

```text
! এখানে ভুল অবস্থার show আউটপুট বা এরর মেসেজ বসাও
```

## 🎯 চাইছি (Expected Output)

ঠিক কোন আউটপুট বা সংযোগ সচল করতে চাই তা ১–২ লাইনে লেখো।

## ✅ সমাধান (Router / Switch CLI)

```cisco
enable
configure terminal

! এখানে সমাধানের CLI কমান্ড লেখো

end
copy running-config startup-config
```

| কমান্ড | কাজ |
| :--- | :--- |
| `কমান্ড ১` | এই লাইনটি ঠিক কী সমস্যার সমাধান করল |

## 🔍 যাচাই

```cisco
! এখানে যাচাই করার show বা ping কমান্ড বসাও
```

## 🧠 লজিক — কেন এটা কাজ করল?

এখানে ২–৩ লাইনে মূল কারণটা ব্যাখ্যা করো যেন শিক্ষার্থী পরের বার নিজেই সমস্যাটি ধরতে পারে।
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cisco-Packet-Tracer-Lab Markdown Lesson / Extra-Lab / Problem Writer CLI"
    )
    sub = parser.add_subparsers(dest="kind", required=True)

    # Lesson subcommand
    p_les = sub.add_parser("lesson", help="Generate a standardized Bangla Lesson markdown file")
    p_les.add_argument("--num", type=int, required=True, help="Lesson number (e.g. 13)")
    p_les.add_argument("--slug", required=True, help="Kebab-case filename slug (e.g. ospf-routing)")
    p_les.add_argument("--title", required=True, help="Lesson title in Bangla/English")
    p_les.add_argument("--goal", default="", help="One-line lesson goal")
    p_les.add_argument("--time", default="~৪৫ মিনিট", help="Estimated study time")
    p_les.add_argument("--level", default="🟡 Intermediate", help="Difficulty badge")
    p_les.add_argument("--tags", default="cisco,packet-tracer,lab", help="Comma-separated tags")
    p_les.add_argument("--out", default="", help="Custom output path")
    p_les.add_argument("--force", action="store_true", help="Overwrite existing file")
    p_les.add_argument("--stdout", action="store_true", help="Print to stdout instead of writing file")

    # Extra-lab subcommand
    p_ext = sub.add_parser("extra", help="Generate a standardized Extra Lab guide in Extras/")
    p_ext.add_argument("--slug", required=True, help="Kebab-case slug (e.g. syslog-ntp-lab)")
    p_ext.add_argument("--title", required=True, help="Extra Lab title")
    p_ext.add_argument("--goal", default="", help="One-line goal")
    p_ext.add_argument("--time", default="~৪০ মিনিট", help="Estimated time")
    p_ext.add_argument("--level", default="🟡 Intermediate", help="Difficulty badge")
    p_ext.add_argument("--pkt", default="", help="Associated .pkt filename in pkt-files/practice/")
    p_ext.add_argument("--tags", default="extra-lab,packet-tracer,ccna", help="Comma-separated tags")
    p_ext.add_argument("--out", default="", help="Custom output path")
    p_ext.add_argument("--force", action="store_true", help="Overwrite existing file")
    p_ext.add_argument("--stdout", action="store_true", help="Print to stdout instead of writing file")

    # Problem subcommand
    p_prb = sub.add_parser("problem", help="Generate or append a Problem Solve entry")
    p_prb.add_argument("--num", type=int, required=True, help="Problem number (e.g. 7)")
    p_prb.add_argument("--title", required=True, help="Problem title")
    p_prb.add_argument(
        "--append",
        action="store_true",
        help="Append directly before footer in lessons/12-problem-solve.md",
    )
    p_prb.add_argument("--stdout", action="store_true", help="Print generated Markdown to stdout")

    args = parser.parse_args()

    if args.kind == "lesson":
        md = build_lesson_markdown(args)
        if args.stdout:
            print(md)
            return 0
        slug = re.sub(r"[^a-z0-9-]+", "-", args.slug.lower()).strip("-")
        out_path = args.out or os.path.join(REPO_ROOT, "lessons", f"{args.num:02d}-{slug}.md")
        if os.path.exists(out_path) and not args.force:
            print(f"❌ ফাইল আগে থেকেই আছে: {out_path} (--force দিলে ওভাররাইট হবে)", file=sys.stderr)
            return 1
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"✅ নতুন লেসন তৈরি হয়েছে: {out_path}")
        return 0

    if args.kind == "extra":
        md = build_extra_lab_markdown(args)
        if args.stdout:
            print(md)
            return 0
        slug = re.sub(r"[^a-z0-9-]+", "-", args.slug.lower()).strip("-")
        out_path = args.out or os.path.join(REPO_ROOT, "Extras", f"{slug}.md")
        if os.path.exists(out_path) and not args.force:
            print(f"❌ ফাইল আগে থেকেই আছে: {out_path} (--force দিলে ওভাররাইট হবে)", file=sys.stderr)
            return 1
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"✅ নতুন Extra Lab গাইড তৈরি হয়েছে: {out_path}")
        return 0

    if args.kind == "problem":
        block = build_problem_markdown(args)
        if args.stdout or not args.append:
            print(block.lstrip())
            if not args.append:
                print("\n💡 টিপ: সরাসরি ১২ নম্বর লেসনে যোগ করতে `--append` ফ্ল্যাগ ব্যবহার করো।")
            return 0
        target = os.path.join(REPO_ROOT, "lessons", "12-problem-solve.md")
        content = open(target, encoding="utf-8").read()
        marker = "\n---\n\n# 🔮"
        if marker in content:
            updated = content.replace(marker, block + marker, 1)
        else:
            updated = content.rstrip() + "\n" + block + "\n"
        open(target, "w", encoding="utf-8").write(updated)
        print(f"✅ Problem {to_bn(args.num, 2)} সফলভাবে যুক্ত হয়েছে: {target}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
