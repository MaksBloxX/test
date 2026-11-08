# 🗺️ পূর্ণাঙ্গ রোডম্যাপ (Master Learning & Repository Roadmap)

> **নেভিগেশন:** [🏠 রেপো হোম](README.md) · [📚 মূল লেসন (০১–১২)](lessons/README.md) · [🎓 CCNA Fundamentals (০১–০৯)](ccna-fundamentals/README.md) · [📦 Extra Labs](Extras/README.md) · [📚 বই ও চিট-শিট](reference/README.md) · [🛠️ স্ক্রিপ্টসমূহ](scripts/README.md)

এই রোডম্যাপটি **দুটি প্রধান অংশে** সাজানো হয়েছে:
1. **[Part A — 👨‍🎓 শিক্ষার্থীদের শেখার রোডম্যাপ](#student-roadmap):** শূন্য থেকে শুরু করে ৩০ দিনে পুরো নেটওয়ার্কিং ও Packet Tracer আয়ত্ত করার দৈনিক পরিকল্পনা + ৭ দিনের ভার্সিটি ল্যাব ফাইনাল ক্র্যাশ প্ল্যান।
2. **[Part B — 🚀 রেপোজিটরি উন্নয়নের রোডম্যাপ](#repo-roadmap):** এই প্রজেক্টটিকে বাংলাদেশের সেরা ওপেন-সোর্স নেটওয়ার্কিং ল্যাব প্ল্যাটফর্মে পরিণত করার **Phase 1 → Phase 5** মাস্টার প্ল্যান।

---

<a id="student-roadmap"></a>

# 👨‍🎓 Part A — শিক্ষার্থীদের শেখার পূর্ণাঙ্গ রোডম্যাপ

## 🧭 ১. এক নজরে শেখার ৬টি ধাপ (Skill Progression)

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: ভিত্তি ও প্রথম CLI (দিন ১–৫)                                         │
│   • নেটওয়ার্ক, টপোলজি, OSI 7 Layers, MAC ও ARP বোঝা                          │
│   • Router CLI মোড চেনা এবং প্রথম LAN তৈরি করে Ping সফল করা                    │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: IPv4, Subnetting ও Static Routing (দিন ৬–১২)                        │
│   • IPv4 ঠিকানা, /24 থেকে /30 হিসাব, Magic Block Size ও VLSM প্ল্যানিং          │
│   • দুটি রাউটারের মাঝে /30 WAN লিংক ও দ্বিমুখী Static Route কনফিগার             │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: নেটওয়ার্ক সার্ভিসসমূহ — DHCP, DNS, Web, FTP, Email, Printer (দিন ১৩–১৮)│
│   • স্বয়ংক্রিয় IP বিতরণ (DHCP), নাম থেকে IP (DNS), ওয়েবসাইট হোস্টিং (HTTP)      │
│   • বাস্তব অফিসের FTP ফাইল সার্ভার, SMTP/POP3 ইমেইল ও শেয়ার্ড প্রিন্টার         │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: VLAN, Trunk ও Enterprise Switching (দিন ১৯–২৩)                      │
│   • সুইচ ভাগ করে VLAN তৈরি, 802.1Q Trunk ও Router-on-a-Stick রাউটিং         │
│   • STP লুপ প্রতিরোধ, Port Security (Sticky MAC) ও LACP EtherChannel          │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 5: Security (ACL/NAT), Hardware ও Troubleshooting (দিন ২৪–২৭)          │
│   • Standard/Extended ACL ফিল্টারিং ও PAT/NAT দিয়ে ইন্টারনেট সংযোগ             │
│   • বাস্তব রাউটার/সুইচ/কেবল/র‍্যাক চেনা এবং ভাঙা নেটওয়ার্ক মেরামত করা             │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 6: চূড়ান্ত প্রজেক্ট ও পরীক্ষা প্রস্তুতি (দিন ২৮–৩০)                         │
│   • Office Capstone + University Mega Capstone + ৩০টি প্র্যাকটিস চ্যালেঞ্জ      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📅 ২. ৩০ দিনের কমপ্লিট স্টাডি প্ল্যান (প্রতিদিন ৬০–৯০ মিনিট)

> 💡 **সেরা কৌশল:** অন্ধভাবে কমান্ড মুখস্থ না করে আমরা **তত্ত্ব (CCNA)** এবং **হাতে-কলমে ল্যাব (Lessons + Extras)** পরপর মিলিয়ে পড়ব!

### 🟢 সপ্তাহ ১: নেটওয়ার্কের ভিত্তি ও প্রথম CLI ল্যাব (দিন ১–৭)

| দিন | কী পড়বে / করবে | সংযুক্ত ফাইল / টুল | লক্ষ্য |
| :---: | :--- | :--- | :--- |
| **দিন ০১** | নেটওয়ার্ক কী, LAN/WAN, Switch বনাম Router | [CCNA ০১ · Network Basics](ccna-fundamentals/01-network-basics.md) | ১০টি কুইজ পাস |
| **দিন ০২** | ৬টি টপোলজি Simulation Mode-এ চালানো | [🕸️ 6 Topologies Lab](Extras/network-topologies-lab.md) | Mesh সূত্র যাচাই |
| **দিন ০৩** | OSI 7 Layers ও TCP/IP Encapsulation | [CCNA ০২ · OSI Model](ccna-fundamentals/02-osi-tcp-ip.md) + [📕 OSI বই (অধ্যায় ১–৬)](reference/OSI-Illustrated.md) | ৭ লেয়ারের কাজ মুখস্থ নয়, বোঝা |
| **দিন ০৪** | MAC Address, Ethernet Frame ও ARP | [CCNA ০৩ · MAC & ARP](ccna-fundamentals/03-mac-ethernet-arp.md) | `arp -a` ও MAC Table বোঝা |
| **দিন ০৫** | **প্রথম হাতে-কলমে CLI ল্যাব!** | [লেসন ০১ · Router CLI Basics](lessons/01-router-cli-basics.md) + [`lesson-01.pkt`](pkt-files/labs/lesson-01-router-cli-basics.pkt) | PC0 → PC1 Ping সফল ✅ |
| **দিন ০৬** | বাস্তব ডিভাইস, কেবল পেয়ার (T568B) ও র‍্যাক চেনা | [লেসন ০৯ · Real Hardware](lessons/09-real-hardware.md) | বাস্তব পোর্ট ও কেবল চেনা |
| **দিন ০৭** | **রিভিশন ও কুইজ পরীক্ষা** | `python3 scripts/quiz_trainer.py --count 15` | সপ্তাহ ১ ঝালিয়ে নেওয়া |

### 🟡 সপ্তাহ ২: IPv4, Subnetting মাস্টারি ও Static Routing (দিন ৮–১৪)

| দিন | কী পড়বে / করবে | সংযুক্ত ফাইল / টুল | লক্ষ্য |
| :---: | :--- | :--- | :--- |
| **দিন ০৮** | IPv4 গঠন, Private/Public IP, Loopback, APIPA | [CCNA ০৪ · IPv4 Addressing](ccna-fundamentals/04-ipv4-addressing.md) | ১০টি কুইজ পাস |
| **দিন ০৯** | Subnetting সূত্র ($2^n$, $2^h-2$, Block Size) | [CCNA ০৫ · Subnetting Basics](ccna-fundamentals/05-subnetting-basics.md) | খাতায় `/25`, `/26`, `/27` ভাগ করা |
| **দিন ১০** | Packet Tracer-এ সাবনেটিং প্রমাণ + ড্রিল | [🧮 IP Subnet Tester Lab](Extras/ip-subnet-tester-lab.md) + `subnet_calculator.py --drill 5` | কেন `/26`-এ `.65` পিং পায় না তা দেখা |
| **দিন ১১** | VLSM — বড় থেকে ছোট বিভাগ অনুযায়ী IP প্ল্যান | [CCNA ০৬ · VLSM](ccna-fundamentals/06-subnetting-vlsm.md) + `subnet_calculator.py --vlsm` | যেকোনো অফিসের IP চার্ট বানানো |
| **দিন ১২** | **দুই রাউটার ও Static Routing ল্যাব** | [লেসন ০২ · Static Routing](lessons/02-static-routing.md) + [`lesson-02.pkt`](pkt-files/labs/lesson-02-static-routing.pkt) | দ্বিমুখী `ip route` ও `/30` লিংক |
| **দিন ১৩** | রাউটিং ট্রাবলশুটিং (Return Route মিসিং কেস) | [লেসন ১২ · Problem ০২](lessons/12-problem-solve.md#problem-02) | না দেখে ২ রাউটার ল্যাব আবার বানানো |
| **দিন ১৪** | **সপ্তাহ ২ পরীক্ষা** | খাতায় ৫টি VLSM অঙ্ক + `quiz_trainer.py --lesson 5` | ১০০% সাবনেটিং আত্মবিশ্বাস |

### 🟠 সপ্তাহ ৩: নেটওয়ার্ক সার্ভিস ও VLAN / Inter-VLAN (দিন ১৫–২১)

| দিন | কী পড়বে / করবে | সংযুক্ত ফাইল / টুল | লক্ষ্য |
| :---: | :--- | :--- | :--- |
| **দিন ১৫** | Router DHCP Server ও DORA প্রক্রিয়া | [লেসন ০৩ · DHCP](lessons/03-dhcp.md) + [🖨️ Shared Printer Lab](Extras/office-shared-printer-lab.md) | Auto IP + প্রিন্টার Static IP |
| **দিন ১৬** | DNS (`A Record`) ও HTTP Web Server | [লেসন ০৪ · DNS & HTTP](lessons/04-dns-http-server.md) | `www.office.local` ব্রাউজারে খোলা |
| **দিন ১৭** | FTP ফাইল সার্ভার ও SMTP/POP3 ইমেইল সার্ভার | [🌐 FTP Lab](Extras/ftp-server-lab.md) + [📧 Email Lab](Extras/email-server-lab.md) | `put`/`get` ও ইমেইল আদান-প্রদান |
| **দিন ১৮** | Switch VLAN তৈরি ও Isolation প্রমাণ | [লেসন ০৫ · VLAN](lessons/05-vlan.md) + [Problem ০১](lessons/12-problem-solve.md#problem-01) | একই VLAN ✅, ভিন্ন VLAN ❌ |
| **দিন ১৯** | 802.1Q Trunk ও Router-on-a-Stick (ROAS) | [লেসন ০৬ · Trunk & Inter-VLAN](lessons/06-trunk-inter-vlan.md) | ভিন্ন VLAN-এ সফল Ping (`TTL=127`) |
| **দিন ২০** | STP, Port Security ও LACP EtherChannel | [লেসন ০৭ · Switching](lessons/07-switching.md) | Root Bridge, Sticky MAC, `Po1(SU)` |
| **দিন ২১** | **Mini-Capstone: সম্পূর্ণ অফিস নেটওয়ার্ক!** | [লেসন ০৮ · Final Project](lessons/08-final-project.md) | সব প্রযুক্তি এক টপোলজিতে! |

### 🔴 সপ্তাহ ৪: সিকিউরিটি, ট্রাবলশুটিং ও চূড়ান্ত প্রস্তুতি (দিন ২২–৩০)

| দিন | কী পড়বে / করবে | সংযুক্ত ফাইল / টুল | লক্ষ্য |
| :---: | :--- | :--- | :--- |
| **দিন ২২–২৩** | ACL ট্রাফিক ফিল্টারিং ও NAT/PAT ইন্টারনেট সংযোগ | [CCNA ০৭ · ACL ও NAT](ccna-fundamentals/07-acl-nat.md) | নির্দিষ্ট ট্রাফিক ব্লক ও PAT কনফিগ |
| **দিন ২৪** | পদ্ধতিগত নেটওয়ার্ক ট্রাবলশুটিং (Bottom-Up) | [CCNA ০৮ · Troubleshooting](ccna-fundamentals/08-troubleshooting.md) + [লেসন ১২ (সব ৬টি কেস)](lessons/12-problem-solve.md) | যেকোনো ভাঙা ল্যাব ৫ মিনিটে ধরা |
| **দিন ২৫** | বাস্তব Windows/Linux নেটওয়ার্কিং কমান্ড | [📘 Practical Networking: 30 Commands](reference/MaksDev-Practical-Networking.md) | নিজের পিসির টার্মিনালে অনুশীলন |
| **দিন ২৬–২৭** | ১০টি সমাধানসহ প্র্যাকটিস ল্যাব | [লেসন ১০ · Practice Lab](lessons/10-practice-lab.md) | না দেখে ৬ Simple + ৪ Hard সমাধান |
| **দিন ২৮–২৯** | ২০টি সমাধান ছাড়া চ্যালেঞ্জ (আসল পরীক্ষা!) | [লেসন ১১ · Practice List](lessons/11-practice-list.md) | টাইমার ধরে ৪৫ মিনিটে ল্যাব সম্পন্ন |
| **দিন ৩০** | **🏆 গ্র্যান্ড ফিনালে — University Mega Capstone!** | [CCNA ০৯ · University Capstone](ccna-fundamentals/09-capstone-university-lab.md) | সম্পূর্ণ ক্যাম্পাস নেটওয়ার্ক জয়! 🎉 |

---

## ⚡ ৩. ৭ দিনের ভার্সিটি ল্যাব পরীক্ষা ও ভাইভা ক্র্যাশ প্ল্যান (Exam Week!)

পরীক্ষার আগে সময় মাত্র ১ সপ্তাহ থাকলে এই ক্রমটি অনুসরণ করো:

* **Day 1:** [লেসন ০১ (CLI)](lessons/01-router-cli-basics.md) + [লেসন ০২ (Static Routing)](lessons/02-static-routing.md) হাতে-কলমে ১ বার করে বানানো।
* **Day 2:** [CCNA ০৫ (Subnetting)](ccna-fundamentals/05-subnetting-basics.md) + `python3 scripts/subnet_calculator.py --drill 10`।
* **Day 3:** [লেসন ০৩ (DHCP)](lessons/03-dhcp.md) + [লেসন ০৪ (DNS + Web)](lessons/04-dns-http-server.md) একসাথে অনুশীলন।
* **Day 4:** [লেসন ০৫ (VLAN)](lessons/05-vlan.md) + [লেসন ০৬ (Trunk + ROAS)](lessons/06-trunk-inter-vlan.md) হাতে-কলমে।
* **Day 5:** [লেসন ০৭ (STP + Port Security + EtherChannel)](lessons/07-switching.md) + [🌐 FTP](Extras/ftp-server-lab.md) / [📧 Email](Extras/email-server-lab.md) ভাইভা প্রশ্ন।
* **Day 6:** [লেসন ০৮ (Final Project)](lessons/08-final-project.md) না দেখে ৪৫ মিনিটে সম্পন্ন করা + [লেসন ০৯ (Real Hardware ছবি)](lessons/09-real-hardware.md) দেখা।
* **Day 7:** [📖 CLI Cheat-Sheet](reference/cli-command-cheatsheet.md) + [লেসন ১২ (Problem Solve)](lessons/12-problem-solve.md) রিভিশন!

---

## 🎯 ৪. Cisco CCNA (200-301) সিলেবাস কাভারেজ ম্যাপ

| CCNA 200-301 অফিসিয়াল ডোমেইন | পরীক্ষার গুরুত্ব | এই রেপোতে বর্তমান কাভারেজ | কোথায় আছে / পরবর্তী ধাপ |
| :--- | :---: | :---: | :--- |
| **1.0 Network Fundamentals** | 20% | ✅ **৯০% প্রস্তুত** | CCNA ০১–০৬, লেসন ০১, ০৯, Topologies Lab *(বাকি: IPv6)* |
| **2.0 Network Access (Switching/VLAN/WLAN)** | 20% | ✅ **৮০% প্রস্তুত** | লেসন ০৫–০৭ (VLAN, Trunk, STP, EtherChannel) *(বাকি: WLC Wireless)* |
| **3.0 IP Connectivity (Routing)** | 25% | 🟡 **৫৫% প্রস্তুত** | লেসন ০২, ০৬ (Static, ROAS), Cheat-Sheet *(পরবর্তী: OSPF পূর্ণ ল্যাব, FHRP)* |
| **4.0 IP Services (DHCP/DNS/NAT/NTP/Syslog)** | 10% | ✅ **৮০% প্রস্তুত** | লেসন ০৩–০৪, CCNA ০৭, FTP/Email Labs *(বাকি: NTP, Syslog, SNMP ল্যাব)* |
| **5.0 Security Fundamentals** | 15% | ✅ **৭০% প্রস্তুত** | লেসন ০৭ (Port Security), CCNA ০৭ (ACL), Cheat-Sheet SSH *(বাকি: DHCP Snooping, DAI)* |
| **6.0 Automation & Programmability** | 10% | 🟡 **৪০% প্রস্তুত** | `scripts/` Python নেটওয়ার্ক অটোমেশন টুলস *(বাকি: REST API, JSON/YAML তত্ত্ব)* |

---

<a id="repo-roadmap"></a>

# 🚀 Part B — রেপোজিটরি উন্নয়নের পূর্ণাঙ্গ রোডম্যাপ (Phase 1 → Phase 5)

এই রেপোজিটরিটিকে ধাপে ধাপে কীভাবে আরও সমৃদ্ধ করা হবে তার সুস্পষ্ট পরিকল্পনা নিচে দেওয়া হলো:

---

## ✅ Phase 1 — v2.0: ডকুমেন্টেশন, ইকোসিস্টেম ও অটোমেশন আপগ্রেড *(সম্পন্ন!)*

- [x] সব ফোল্ডারে (`lessons/`, `ccna-fundamentals/`, `Extras/`, `reference/`, `pkt-files/`, `scripts/`) পরিষ্কার ইনডেক্স `README.md` ও নেভিগেশন যুক্ত করা
- [x] লেসন ০১–০৮ প্রতিটিতে **🏷️ মূল শব্দকোষ (Quick Glossary)** এবং CCNA তত্ত্বের ক্রস-লিংক সংযোজন
- [x] লেসন ০৯-এ **Datacenter Rack Infrastructure Blueprint** (`data-central-rack.jpg`)-এর ১০টি অংশের পূর্ণাঙ্গ বাংলা বিশ্লেষণ যোগ করা
- [x] লেসন ১২ (Problem Solve Bank) ১টি সমস্যা থেকে বাড়িয়ে **৬টি বাস্তব ট্রাবলশুটিং কেস**-এ উন্নীত করা
- [x] আনলিংকড `.pkt` ফাইলগুলোর জন্য ৩টি নতুন Extra Lab গাইড তৈরি (`Office Shared Printer`, `IP Subnet Tester`, `6 Network Topologies`)
- [x] রেফারেন্স ফোল্ডারের **২টি পূর্ণাঙ্গ বাংলা বই** (`Practical Networking` ও `OSI Illustrated`) মূল `README.md`-তে যুক্ত করা
- [x] **৫টি Python CLI অটোমেশন ও রাইটার স্ক্রিপ্ট** তৈরি (`lab_writer.py`, `ios_config_generator.py`, `subnet_calculator.py`, `quiz_trainer.py`, `repo_doctor.py`)
- [x] স্বয়ংক্রিয় লিংক ও স্বাস্থ্য পরীক্ষার জন্য **GitHub Actions CI** (`.github/workflows/repo-check.yml`) সংযোজন

---

## 🔜 Phase 2 — v2.5: Dynamic Routing, Wireless ও Broken `.pkt` প্যাক *(স্বল্পমেয়াদি লক্ষ্য)*

| আইটেম | প্রস্তাবিত ফাইল | কী যোগ হবে |
| :--- | :--- | :--- |
| **লেসন ১৩ · Dynamic Routing (RIPv2 & OSPFv2)** | `lessons/13-dynamic-routing-ospf.md` + `.pkt` | ৩টি রাউটারে `router ospf 1`, Wildcard Mask, Router-ID, `show ip ospf neighbor` ও লিংক ফেলওভার পরীক্ষা |
| **লেসন ১৪ · Wireless LAN ও Enterprise WLC** | `lessons/14-wireless-lan.md` + `.pkt` | Home Wireless Router (WPA2-PSK) বনাম Cisco WLC-2504 + Lightweight AP কনফিগারেশন |
| **লেসন ১৫ · SSH, Device Hardening ও Syslog/NTP** | `lessons/15-ssh-syslog-ntp.md` + `.pkt` | Telnet বন্ধ করে RSA/SSH রিমোট লগইন, পাসওয়ার্ড এনক্রিপশন, NTP ঘড়ি সিঙ্ক ও Syslog সার্ভারে লগ সংগ্রহ |
| **Broken `.pkt` Troubleshooting Pack** | `pkt-files/troubleshooting/broken-01..06.pkt` | ইচ্ছাকৃতভাবে ভুল করা ৬টি `.pkt` ফাইল — শিক্ষার্থী ডাউনলোড করে `lessons/12-problem-solve.md`-এর সমস্যাগুলো নিজে ঠিক করবে! |

---

## 🏗️ Phase 3 — v3.0: Enterprise Layer-3, Redundancy ও IPv6 *(মধ্যমেয়াদি লক্ষ্য)*

- [ ] **লেসন ১৬ · Multilayer Switch (L3 SVI Routing):** Cisco `3560/3650` সুইচে `ip routing` ও `interface vlan 10/20` দিয়ে রাউটার ছাড়াই দ্রুতগতির Inter-VLAN Routing
- [ ] **লেসন ১৭ · Gateway Redundancy (HSRP):** দুটি রাউটারে `standby 1 ip` দিয়ে Virtual Gateway তৈরি — মূল রাউটার বন্ধ হলেও ইন্টারনেট কাটবে না!
- [ ] **লেসন ১৮ · IPv6 Addressing & Routing Lab:** `2001:db8::/64`, Link-Local (`fe80::`), SLAAC অটো-কনফিগারেশন ও IPv6 Static/OSPFv3 পিং ল্যাব
- [ ] **Extra Lab ০৬ · VoIP IP Telephony:** Cisco `2811` রাউটারে `telephony-service` + সুইচে `switchport voice vlan` + দুটি `7960 IP Phone`-এ রিং বাজানো!
- [ ] **Extra Lab ০৭ · Layer-2 Security:** `DHCP Snooping` + `Dynamic ARP Inspection (DAI)` দিয়ে Man-in-the-Middle আক্রমণ প্রতিরোধ

---

## 🌐 Phase 4 — v3.5: সার্চেবল ওয়েব পোর্টাল, অ্যানিমেশন ও দ্বিভাষিক সংস্করণ *(দীর্ঘমেয়াদি লক্ষ্য)*

- [ ] **GitHub Pages ওয়েবসাইট (MkDocs Material):** পুরো রেপোটিকে একটি সুন্দর ও দ্রুত ওয়েবসাইটে প্রকাশ করা — যেখানে থাকবে Dark/Light Mode, বাংলা+ইংরেজি ইনস্ট্যান্ট সার্চ বার এবং প্রতিটি কমান্ড বক্সে ১-ক্লিক `Copy` বাটন!
- [ ] **৩০-সেকেন্ডের GIF / Video Walkthrough:** প্রতিটি ল্যাবের টপোলজি ও ভেরিফিকেশনের সংক্ষিপ্ত স্ক্রিন-রেকর্ডিং বা অ্যানিমেটেড GIF
- [ ] **English Parallel Track (`en/`):** আন্তর্জাতিক শিক্ষার্থীদের জন্য প্রতিটি লেসনের ইংরেজি অনুবাদ

---

## 🏆 Phase 5 — v4.0: Mega ISP & Multi-Campus Enterprise Capstone

- [ ] **মাস্টার প্রজেক্ট:** ২টি শাখা অফিস + ১টি হেড অফিস + ১টি ISP ক্লাউড + DMZ সার্ভার ফার্ম (`Web + DNS + Email + FTP`) + `OSPF` + `HSRP` + `VoIP` + `Wi-Fi` + `PAT` + `Extended ACL` — একটি সম্পূর্ণ বাস্তব কোম্পানির সমতুল্য নেটওয়ার্ক সিমুলেশন!

---

## 🛠️ লেখক/মেইনটেইনার কীভাবে ২ মিনিটে নতুন লেসন যোগ করবে?

নতুন কোনো ফেজের কাজ শুরু করতে আর শূন্য থেকে ফাইল সাজাতে হবে না! টার্মিনালে চালাও:

```bash
# ১. নতুন লেসনের রেডিমেড বাংলা মার্কডাউন ফাইল তৈরি করো
python3 scripts/lab_writer.py lesson --num 13 --slug dynamic-routing-ospf \
    --title "Dynamic Routing — RIPv2 ও Single-Area OSPF" --level "🟠 Intermediate"

# ২. ফাইলটি সম্পাদনা করো এবং pkt-files/labs/lesson-13-dynamic-routing-ospf.pkt যোগ করো

# ৩. পুশ করার আগে সব লিংক ও ফরম্যাট অটোমেটিক পরীক্ষা করে নাও!
python3 scripts/repo_doctor.py --strict
```

---

> **নেভিগেশন:** [🏠 রেপো হোম](README.md) · [📚 মূল লেসন](lessons/README.md) · [🎓 CCNA Fundamentals](ccna-fundamentals/README.md) · [🛠️ স্ক্রিপ্টসমূহ](scripts/README.md) · [🤝 কন্ট্রিবিউট গাইড](CONTRIBUTING.md)
