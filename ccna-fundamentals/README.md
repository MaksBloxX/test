# 🎓 CCNA Fundamentals — তত্ত্ব থেকে শুরু

> **কোর্সের ধরন:** ধারণা (theory) আগে → তারপর ল্যাব
> **লেসন:** ৯টা · **কুইজ:** ৬৮টা (সবই ▸ টগলে লুকানো) · **ভাষা:** বাংলা + English টেকনিক্যাল শব্দ · [৯টি English companion](../en/ccna-fundamentals/README.md) (মূল সব কুইজ আক্ষরিক অনুবাদ নয়)

---

### 🖼️ চিত্রে বোঝো: ৯টি CCNA অধ্যায়ের ভিজ্যুয়াল মানচিত্র

![৯টি CCNA অধ্যায়ের ভিজ্যুয়াল মানচিত্র — নেটওয়ার্কের ভিত্তি → OSI/MAC/IP → Subnetting/VLSM → ACL/NAT → Campus Capstone।](../assets/diagrams/ccna-course-map.svg)

> **ছবির সারকথা:** নেটওয়ার্কের ভিত্তি → OSI/MAC/IP → Subnetting/VLSM → ACL/NAT → Campus Capstone।

---

## 📌 এই কোর্সটা কার জন্য

এই রেপোতে **দুটো কোর্স** আছে:

| | 🅰️ [হাতে-কলমে কোর্স](../lessons/01-router-cli-basics.md) | 🅱️ **CCNA Fundamentals** (এই কোর্স) |
|---|---|---|
| শুরু হয় | Router-এর CLI দিয়ে | "নেটওয়ার্ক আসলে কী?" দিয়ে |
| ধরন | config-first — সোজা ল্যাব | theory-first — আগে ধারণা |
| লেসন | ০১–১৮ | ০১–০৯ |
| কে পড়বে | "আজই PT-তে নেটওয়ার্ক বানাব" | "আগে বুঝব, তারপর বানাব" |
| শেষ হয় | Final Project + OSPF/WLC/SSH + [SVI/HSRP/IPv6](../lessons/README.md) | University Capstone |

👉 **সেরা পথ:** এই কোর্সের ০১–০৪ → হাতে-কলমে ০১–০২ → এখানে ০৫–০৬ → হাতে-কলমে ০৩–০৮ ও ১৩–১৮ → এখানে ০৭–০৯।
সময় কম থাকলে অন্তত **০১–০৫** পড়ো—subnetting বোঝা জরুরি। টার্মিনালে কুইজ দিতে চালাও: `python3 scripts/quiz_trainer.py --count 5` (এই কোর্সের **৬৮টি** + practical-এর **১৮টি** = মোট **৮৬টি**!)।

---

## 🗺️ কোর্স ম্যাপ

```
ভিত্তি (Foundation)
  01 Network Basics      → নেটওয়ার্ক, টপোলজি, Switch/Router
  02 OSI + TCP/IP        → ৭ লেয়ার, encapsulation
  03 MAC + Ethernet+ ARP → Layer 2 কীভাবে কাজ করে
  04 IPv4 Addressing     → ঠিকানা, private/public, special

সাবনেটিং (যেখানে বেশি মানুষ আটকায়)
  05 Subnetting Basics   → subnet mask, block size, /24 → /26
  06 VLSM                → ভিন্ন ভিন্ন চাহিদা অনুযায়ী subnet

প্র্যাকটিস (নেটওয়ার্ক চালানো ও রক্ষা করা)
  07 ACL + NAT           → কে কী পারবে, বাইরে কীভাবে যাবে
  08 Troubleshooting     → ৭ কমান্ড, ৬ ল্যাব

🏆 09 Capstone           → University Network — সব একসাথে
```

---

## 📚 লেসন তালিকা

| # | লেসন | যা শিখবে | লেভেল | কুইজ |
|:--:|:---|:---|:--:|:--:|
| ০১ | [নেটওয়ার্ক কী? টপোলজি, Switch ও Router](01-network-basics.md) | LAN/MAN/WAN, star/bus/ring, node/host/client-server | 🟢 Beginner | ১০ |
| ০২ | [OSI Model ও TCP/IP Model](02-osi-tcp-ip.md) | ৭ লেয়ার, PDU, encapsulation, TCP vs UDP | 🟢 Beginner | ১০ |
| ০৩ | [MAC Address, Ethernet ও ARP](03-mac-ethernet-arp.md) | MAC গঠন, frame, ARP request/reply, MAC table | 🟡 Beginner–Intermediate | ১০ |
| ০৪ | [IPv4 Addressing Fundamentals](04-ipv4-addressing.md) | octet, subnet mask, private/public, APIPA, loopback | 🟢 Beginner | ১০ |
| ০৫ | [Subnetting Basics](05-subnetting-basics.md) | 2^n / 2^h−2, block size, network ও broadcast | 🟡 Beginner–Intermediate | ৭ |
| ০৬ | [Subnetting Practice — VLSM](06-subnetting-vlsm.md) | বড় থেকে ছোট, CIDR বাছাই, address plan | 🟠 Intermediate | ৭ |
| ০৭ | [ACL ও NAT](07-acl-nat.md) | standard/extended ACL, wildcard, NAT, PAT | 🟠 Intermediate | ৫ |
| ০৮ | [Network Troubleshooting](08-troubleshooting.md) | ৭ কমান্ড, ৬টা ভাঙা ল্যাব, bottom-up | 🟡 Intermediate | ৫ |
| ০৯ | [🏆 Capstone — University Network](09-capstone-university-lab.md) | VLAN+trunk+ROAS+DHCP relay+DNS+NAT+ACL | 🔴 Advanced | ৪ |

**মোট কুইজ: ৬৮টা** — প্রতিটার উত্তর ও ব্যাখ্যা ▸ চেপে খুলতে হয়।

---

## ❓ কুইজ কীভাবে ব্যবহার করবে

প্রতিটা লেসনের শেষে **✅ অনুশীলন কুইজ** আছে। প্রশ্ন আর অপশন খোলা থাকে — **উত্তর বন্ধ**।

1. প্রশ্ন পড়ো → কাগজে নিজের উত্তর লিখো (মনে মনে নয়, লিখে ফেলো)
2. `✅ উত্তর ও ব্যাখ্যা দেখো` — ▸ ত্রিভুজে ক্লিক করো
3. ভুল হলে **🧠 কেন** অংশটা মন দিয়ে পড়ো — এটাই আসল শেখা
4. লেসনের `✅ নিজে যাচাই করো` চেকলিস্টে টিক দাও

> 💡 **টিপ:** উত্তর না দেখে ৩০ সেকেন্ড ভাবো। না পারলে ৫ মিনিট লেসনে ফিরে যাও, তারপর দেখো। নিজে ভেঙে পাওয়া জ্ঞান মুখস্থের চেয়ে ১০ গুণ টেকে।

---

## 🧭 স্টাডি প্ল্যান (তিন সপ্তাহ)

| সপ্তাহ | পড়ো | সাথে ল্যাব |
|---|---|---|
| **১ম** | ০১ + ০২ + ০৩ | ৩ PC + ১ Switch LAN, PT Simulation-এ ping-এর লেয়ার দেখা |
| **২য়** | ০৪ + ০৫ + ০৬ | কাগজে ১০টা subnetting প্রবলেম, PT-তে যাচাই |
| **৩য়** | ০৭ + ০৮ + ০৯ | ACL/NAT ল্যাব, ইচ্ছাকৃত ভাঙা ল্যাব ঠিক করা, capstone |

প্রতিদিন ১টা লেসন = **৯ দিনে কোর্স শেষ**, কিন্তু ল্যাব না করলে অর্ধেকই থাকবে। ল্যাবই আসল।

---

## ✅ কোর্স প্রোগ্রেস

- [ ] লেসন ০১ — Network Basics
- [ ] লেসন ০২ — OSI ও TCP/IP
- [ ] লেসন ০৩ — MAC, Ethernet, ARP
- [ ] লেসন ০৪ — IPv4 Addressing
- [ ] লেসন ০৫ — Subnetting Basics
- [ ] লেসন ০৬ — VLSM
- [ ] লেসন ০৭ — ACL ও NAT
- [ ] লেসন ০৮ — Troubleshooting
- [ ] লেসন ০৯ — Capstone সম্পূর্ণ (সব চেকলিস্ট পাস)

---

## 🔗 এক নজরে সংযোগ (ল্যাব, বই ও স্ক্রিপ্ট)

| এখানে শিখলে | হাতে-কলমে ল্যাব, বই ও টুলসে কাজে লাগবে |
|---|---|
| ০১ Network Basics | [লেসন ০১ · Router CLI Basics](../lessons/01-router-cli-basics.md) · [🕸️ 6 Topologies Lab](../Extras/network-topologies-lab.md) |
| ০২ OSI + ০৩ MAC/ARP | [লেসন ০৭ · Switching](../lessons/07-switching.md) · [📕 OSI: From Search to Screen (বই)](../reference/OSI-Illustrated.md) |
| ০৪–০৬ IPv4 + Subnetting | [লেসন ০২ · Static Routing](../lessons/02-static-routing.md) · [🧮 IP Subnet Tester Lab](../Extras/ip-subnet-tester-lab.md) · [`subnet_calculator.py`](../scripts/subnet_calculator.py) |
| ০৭ ACL/NAT | [লেসন ০৮ · Final Project](../lessons/08-final-project.md) · [`ios_config_generator.py`](../scripts/ios_config_generator.py) |
| ০৮ Troubleshooting | [লেসন ১২ · Problem Solve](../lessons/12-problem-solve.md) · [📘 Practical Networking: 30 Commands](../reference/MaksDev-Practical-Networking.md) |
| ০৯ Capstone + ৬৮ কুইজ | [লেসন ১০ · Practice Lab](../lessons/10-practice-lab.md) · [লেসন ১১ · Practice List](../lessons/11-practice-list.md) · [`quiz_trainer.py`](../scripts/quiz_trainer.py) |

---

> **নেভিগেশন:** [🏠 রেপো হোম](../README.md) · [🅰️ হাতে-কলমে কোর্স](../lessons/README.md) · [📦 Extra Labs](../Extras/README.md) · [📖 CLI Cheat-Sheet](../reference/cli-command-cheatsheet.md) · [🗺️ রোডম্যাপ](../ROADMAP.md)

**কোর্সের Tags:** `#ccna` `#fundamentals` `#subnetting` `#osi` `#acl` `#nat` `#troubleshooting`
