<div align="center">

# 🌐 Cisco Packet Tracer Lab

### 🇧🇩 বাংলায় ধাপে-ধাপে কমপ্লিট নেটওয়ার্কিং ও CCNA ল্যাব ইকোসিস্টেম

*হাতে-কলমে Packet Tracer-এ নেটওয়ার্ক তৈরি করতে করতে শেখো — প্রথম CLI কমান্ড থেকে শুরু করে সম্পূর্ণ অফিস ও ক্যাম্পাস নেটওয়ার্ক পর্যন্ত!*

![Cisco Packet Tracer](https://img.shields.io/badge/Cisco-Packet%20Tracer-1BA0D7?style=for-the-badge&logo=cisco&logoColor=white)
![Language](https://img.shields.io/badge/Language-Bangla-006A4E?style=for-the-badge)
![Practical Labs](https://img.shields.io/badge/Practical%20Lessons-12%20%2B%205%20Extras-FF6F00?style=for-the-badge)
![CCNA Fundamentals](https://img.shields.io/badge/CCNA%20Theory-9%20Lessons%20%2B%2068%20MCQs-9B59B6?style=for-the-badge)
![PKT Files](https://img.shields.io/badge/.pkt%20Files-18%20Ready%20Labs-2E8B57?style=for-the-badge)
![CLI Tools](https://img.shields.io/badge/Python%20Tools-5%20Scripts-3776AB?style=for-the-badge&logo=python&logoColor=white)

[**🚦 কোথা থেকে শুরু?**](#tracks) · [**📚 ১২টি মূল লেসন**](#lessons) · [**🎓 CCNA ফাউন্ডেশন**](ccna-fundamentals/README.md) · [**📦 ৫টি এক্সট্রা ল্যাব**](#extras) · [**📖 বই ও Cheat-Sheet**](#books) · [**🛠️ স্ক্রিপ্ট ও রাইটার**](#scripts) · [**🗺️ পূর্ণাঙ্গ রোডম্যাপ**](ROADMAP.md)

</div>

---

## ✨ এক নজরে এই রিপোজিটরিতে কী কী আছে?

এটি **EBAUB — Computer Networking Lab** এবং **CCNA (200-301) Practical** প্রস্তুতির একটি স্বয়ংসম্পূর্ণ বাংলা রিসোর্স হাব। এখানে মুখস্থ করার বদলে **কারণ বুঝে হাতে-কলমে বানানোর** ওপর জোর দেওয়া হয়েছে:

| বিভাগ | পরিমাণ | কী পাবে ভেতরে |
| :--- | :---: | :--- |
| **[📚 হাতে-কলমে কোর্স (`lessons/`)](lessons/README.md)** | **১২টি লেসন** | CLI, Static Routing, DHCP, DNS/HTTP, VLAN, Trunk/ROAS, STP/Security/EtherChannel, Office Capstone, Real Hardware ছবি ও ৬টি বাস্তব Problem Solve ব্যাংক |
| **[🎓 CCNA ফাউন্ডেশন (`ccna-fundamentals/`)](ccna-fundamentals/README.md)** | **৯টি অধ্যায় + ৬৮ কুইজ** | নেটওয়ার্ক বেসিক, OSI 7 Layers, MAC/ARP, IPv4, Subnetting (`/24`→`/30`), VLSM, ACL/NAT, Troubleshooting ও University Mega Capstone |
| **[📦 এক্সট্রা ল্যাব (`Extras/`)](Extras/README.md)** | **৫টি পূর্ণাঙ্গ ল্যাব** | FTP Server, Email (SMTP/POP3) Server, Office Shared Printer, IP Subnet Tester এবং ৬টি Network Topologies ভিজ্যুয়াল গাইড |
| **[📖 বই ও রেফারেন্স (`reference/`)](reference/README.md)** | **২টি বাংলা ই-বুক + ১টি চিট-শিট** | *Cisco CLI Cheat-Sheet*, *Practical Networking (30 Linux/Windows Commands)* PDF/MD এবং *OSI: From Search to Screen* (SVG ডায়াগ্রামসহ) PDF/MD |
| **[🧰 রেডিমেড `.pkt` ফাইল (`pkt-files/`)](pkt-files/README.md)** | **১৮টি `.pkt` ফাইল** | ৮টি সিরিয়াল লেসন ল্যাব + ৪টি সার্ভিস/প্র্যাকটিস ল্যাব + ৬টি টপোলজি ফাইল |
| **[🛠️ অটোমেশন স্ক্রিপ্ট (`scripts/`)](scripts/README.md)** | **৫টি Python CLI টুল** | IOS Config রাইটার, Subnet/VLSM ক্যালকুলেটর, নতুন লেসন/প্রবলেম রাইটার, টার্মিনাল কুইজ ট্রেইনার ও রেপো হেলথ চেকার |

> 🧠 **প্রতিটি লেসনের স্ট্যান্ডার্ড গঠন:**
> **ধারণা ও শব্দকোষ (Glossary)** → **ধাপে-ধাপে ল্যাব** → **`show`/`ping` ভেরিফিকেশন** → **প্যাকেট ফ্লো লজিক** → **ট্রাবলশুটিং** → **চেকলিস্ট**

---

<a id="tracks"></a>

## 🚦 কোথা থেকে শুরু করবে? (৩টি শেখার পথ)

তোমার বর্তমান অবস্থা ও হাতে থাকা সময় অনুযায়ী যেকোনো একটি পথ বেছে নাও:

| ট্র্যাক | কাদের জন্য সেরা | কীভাবে এগোবে |
| :--- | :--- | :--- |
| **🅰️ [হাতে-কলমে ল্যাব ট্র্যাক](lessons/01-router-cli-basics.md)**<br>*(Config-First)* | *"আজই Packet Tracer খুলে রাউটার ও নেটওয়ার্ক বানাতে চাই"* — ভার্সিটি ল্যাব চলছে এমন শিক্ষার্থী | সরাসরি **[লেসন ০১](lessons/01-router-cli-basics.md) → [লেসন ০৮](lessons/08-final-project.md)** সিরিয়াল ধরে করো → এরপর [Extra Labs](Extras/README.md) ও [Practice](lessons/10-practice-lab.md) |
| **🅱️ [তত্ত্ব-থেকে-ল্যাব ট্র্যাক](ccna-fundamentals/README.md)**<br>*(Theory-First)* | *"আগে একদম গোড়া থেকে OSI, IP ও Subnetting পরিষ্কার বুঝব, তারপর কমান্ড লিখব"* | **[CCNA ০১](ccna-fundamentals/01-network-basics.md) → [০৯](ccna-fundamentals/09-capstone-university-lab.md)** শেষ করে প্রতিটি অধ্যায়ের লুকানো কুইজ দাও |
| **🏆 [মাস্টার কম্বো ট্র্যাক](ROADMAP.md#student-roadmap)**<br>*(সবচেয়ে কার্যকর!)* | পূর্ণাঙ্গ নেটওয়ার্ক ইঞ্জিনিয়ারিং ও CCNA প্রস্তুতি (৩০ দিনের রুটিন) | **CCNA ০১–০৩** → **লেসন ০১** → **CCNA ০৪–০৬ (Subnetting)** → **লেসন ০২–০৮** → **Extras** → **CCNA ০৭–০৯** |

> ⏱️ **সামনেই ভার্সিটি ল্যাব ফাইনাল বা ভাইভা?** — সরাসরি দেখে নাও আমাদের **[⚡ ৭ দিনের ক্র্যাশ প্ল্যান (ROADMAP.md)](ROADMAP.md#student-roadmap)**!

---

<a id="lessons"></a>

## 📚 মূল কোর্স: ১২টি সিরিয়াল লেসন (`lessons/`)

<table>
<tr>
<th>#</th>
<th>লেসন</th>
<th>কী শিখবে ও হাতে-কলমে কী বানাবে</th>
<th>লেভেল</th>
<th><code>.pkt</code> ল্যাব</th>
</tr>

<tr>
<td><b>০১</b></td>
<td><a href="lessons/01-router-cli-basics.md"><b>🖥️ Router CLI Basics ও প্রথম ল্যাব</b></a></td>
<td>CLI Mode (<code>&gt;</code>, <code>#</code>, <code>config</code>, <code>config-if</code>), কমান্ড শর্টকাট ফর্মুলা এবং ১ Router + ১ Switch + ২ PC দিয়ে প্রথম সফল Ping ল্যাব।</td>
<td>🟢 Beginner</td>
<td><a href="pkt-files/labs/lesson-01-router-cli-basics.pkt"><code>lesson-01.pkt</code></a></td>
</tr>

<tr>
<td><b>০২</b></td>
<td><a href="lessons/02-static-routing.md"><b>🛣️ Two Routers + Static Routing</b></a></td>
<td>দুটি আলাদা LAN (<code>192.168.1.0/24</code> ও <code>2.0/24</code>), <code>/30</code> WAN লিংক এবং <code>ip route</code> দিয়ে দ্বিমুখী Static Routing ও <code>show ip route</code> যাচাই।</td>
<td>🟢 Beginner</td>
<td><a href="pkt-files/labs/lesson-02-static-routing.pkt"><code>lesson-02.pkt</code></a></td>
</tr>

<tr>
<td><b>০৩</b></td>
<td><a href="lessons/03-dhcp.md"><b>🎫 Router DHCP Configuration</b></a></td>
<td>DORA প্রক্রিয়া, <code>ip dhcp pool</code> তৈরি, <code>excluded-address</code> দিয়ে Static IP সুরক্ষা, অটো IP ও <code>show ip dhcp binding</code> যাচাই।</td>
<td>🟢 Beginner</td>
<td><a href="pkt-files/labs/lesson-03-dhcp.pkt"><code>lesson-03.pkt</code></a></td>
</tr>

<tr>
<td><b>০৪</b></td>
<td><a href="lessons/04-dns-http-server.md"><b>🌍 DNS Server ও HTTP Web Server</b></a></td>
<td>Server-এ Static IP, DNS A-Record (<code>www.office.local</code>), HTTP ওয়েবসাইট হোস্টিং, একাধিক সার্ভার/ডোমেইন ও <i>"Host Name Unresolved"</i> সমাধান।</td>
<td>🟡 Beg–Int</td>
<td><a href="pkt-files/labs/lesson-04-dns-http-server.pkt"><code>lesson-04.pkt</code></a></td>
</tr>

<tr>
<td><b>০৫</b></td>
<td><a href="lessons/05-vlan.md"><b>🔀 VLAN Configuration ও Isolation</b></a></td>
<td>সুইচকে ভাগ করে VLAN 10 (CSE) ও VLAN 20 (EEE), <code>interface range</code> লজিক এবং প্রমাণ: একই VLAN Ping ✅, ভিন্ন VLAN Ping ❌।</td>
<td>🟡 Intermediate</td>
<td><a href="pkt-files/labs/lesson-05-vlan.pkt"><code>lesson-05.pkt</code></a></td>
</tr>

<tr>
<td><b>০৬</b></td>
<td><a href="lessons/06-trunk-inter-vlan.md"><b>🔗 Trunk Link ও Inter-VLAN Routing</b></a></td>
<td>802.1Q Trunk (অ্যানিমেটেড GIF সহ) + Router-on-a-Stick (<code>G0/0.10</code>, <code>encapsulation dot1Q</code>) দিয়ে ভিন্ন VLAN-এর মধ্যে সফল যোগাযোগ।</td>
<td>🟡 Intermediate</td>
<td><a href="pkt-files/labs/lesson-06-trunk-inter-vlan.pkt"><code>lesson-06.pkt</code></a></td>
</tr>

<tr>
<td><b>০৭</b></td>
<td><a href="lessons/07-switching.md"><b>⚡ Switching: STP · Port Security · EtherChannel</b></a></td>
<td>সুইচের ৩টি কোর প্রযুক্তি — STP Root Bridge ও লুপ প্রতিরোধ, Sticky MAC Port Security (<code>err-disabled</code>) এবং LACP EtherChannel (<code>Po1 SU</code>)।</td>
<td>🟠 Int–Adv</td>
<td><a href="pkt-files/labs/lesson-07-switching.pkt"><code>lesson-07.pkt</code></a></td>
</tr>

<tr>
<td><b>০৮</b></td>
<td><a href="lessons/08-final-project.md"><b>🎓 Final Project — সম্পূর্ণ অফিস নেটওয়ার্ক</b></a></td>
<td><b>Capstone:</b> VLAN + Trunk + Router-on-a-Stick + প্রতি VLAN-এ আলাদা DHCP Pool + DNS + HTTP Web Server — সব একসাথে! 🎉</td>
<td>🔴 Advanced</td>
<td><a href="pkt-files/labs/lesson-08-final-project.pkt"><code>lesson-08.pkt</code></a></td>
</tr>

<tr>
<td><b>০৯</b></td>
<td><a href="lessons/09-real-hardware.md"><b>📷 Real Network Hardware ও Datacenter Rack</b></a></td>
<td>বাস্তব Router (1941/4331), Switch (2960/2950), Hub, T568A/B কেবল পেয়ার, Console, SFP/Fiber, Crimping Kit ও <b>১০-অংশের Datacenter Rack Blueprint</b>!</td>
<td>🟢 সবার জন্য</td>
<td><i>ছবিসহ গাইড</i></td>
</tr>

<tr>
<td><b>১০</b></td>
<td><a href="lessons/10-practice-lab.md"><b>🧪 Practice Lab (১০টি টাস্ক — সমাধানসহ)</b></a></td>
<td>৬টি Simple + ৪টি Small Hard ল্যাব চ্যালেঞ্জ। সমাধান টগলে লুকানো — আগে নিজে চেষ্টা করো, আটকে গেলে খুলে শেখো।</td>
<td>🟢→🟠</td>
<td><i>নিজে বানাবে</i></td>
</tr>

<tr>
<td><b>১১</b></td>
<td><a href="lessons/11-practice-list.md"><b>📝 Practice List (২০টি টাস্ক — সমাধান ছাড়া)</b></a></td>
<td>Basic থেকে ৪৫-মিনিটের Exam Simulation পর্যন্ত ২০টি হোমওয়ার্ক চ্যালেঞ্জ (Progress Tracker সহ)।</td>
<td>🟢→🔴</td>
<td><i>নিজে বানাবে</i></td>
</tr>

<tr>
<td><b>১২</b></td>
<td><a href="lessons/12-problem-solve.md"><b>🛠️ Problem Solve — ৬টি বাস্তব ট্রাবলশুটিং ব্যাংক</b></a></td>
<td>VLAN পোর্ট ভুল, একমুখী Static Route, ROAS পিং ব্যর্থ, DHCP <code>169.254.x.x</code> APIPA, <code>err-disabled</code> পোর্ট রিকভারি ও Trunk VLAN মিসিং সমাধান!</td>
<td>🟢→🔴</td>
<td><i>ভাঙা সিনারিও</i></td>
</tr>
</table>

---

<a id="extras"></a>

## 📦 এক্সট্রা প্র্যাকটিক্যাল ল্যাবসমূহ (`Extras/`)

মূল পাঠ্যক্রমের পাশাপাশি বাস্তব সার্ভার ও অফিস নেটওয়ার্কের **৫টি বিশেষ হ্যান্ডস-অন ল্যাব** (ভাইভা প্রশ্নোত্তরসহ):

| # | ল্যাব গাইড | প্রোটোকল / বিষয় | `.pkt` ফাইল |
| :---: | :--- | :--- | :--- |
| **০১** | [🌐 **FTP Server Configuration Lab**](Extras/ftp-server-lab.md) | TCP Port `21`/`20`, ইউজার পারমিশন (`RWDNL`), `put`/`get` ফাইল ট্রান্সফার | [`FTP-Server.pkt`](pkt-files/practice/FTP-Server.pkt) |
| **০২** | [📧 **Email Server Configuration Lab**](Extras/email-server-lab.md) | Inter-Subnet `SMTP` (Port 25) ও `POP3` (Port 110) ইমেইল আদান-প্রদান | [`Email-Server.pkt`](pkt-files/practice/Email-Server.pkt) |
| **০৩** | [🖨️ **Office Shared Printer Network Lab**](Extras/office-shared-printer-lab.md) | অফিস DHCP LAN + `excluded-address` + Static IP নেটওয়ার্ক প্রিন্টার | [`office-shared-printer-network.pkt`](pkt-files/practice/office-shared-printer-network.pkt) |
| **০৪** | [🧮 **IP Subnet Tester Lab**](Extras/ip-subnet-tester-lab.md) | `/24` বনাম `/26` সাবনেট সীমানা ও নিষিদ্ধ Broadcast/Network IP পরীক্ষা | [`ip-subnet-tester.pkt`](pkt-files/practice/ip-subnet-tester.pkt) |
| **০৫** | [🕸️ **6 Network Topologies Visual Guide**](Extras/network-topologies-lab.md) | Bus, Star, Ring, Mesh ($\frac{N(N-1)}{2}$), Tree ও Hybrid — Simulation পরীক্ষা | [`pkt-files/topologies/*.pkt`](pkt-files/README.md) |

---

<a id="books"></a>

## 📖 বাংলা নেটওয়ার্কিং ই-বুক ও রেফারেন্স লাইব্রেরি (`reference/`)

| রিসোর্স | বিবরণ | অনলাইনে পড়ো | PDF ডাউনলোড |
| :--- | :--- | :---: | :---: |
| **[⚡ Cisco CLI Command Cheat-Sheet](reference/cli-command-cheatsheet.md)** | সব লেসনের কমান্ড, CLI Shortcut নিয়ম, OSPF/RIP, SSH, ACL/NAT এবং **কমন IOS Error সমাধান** এক পাতায়! | [📄 **পড়ো**](reference/cli-command-cheatsheet.md) | — |
| **[📘 Practical Networking: 30 Essential Commands](reference/MaksDev-Practical-Networking.md)** | Linux, Windows ও macOS-এর ৩০টি অপরিহার্য নেটওয়ার্কিং কমান্ড (`ping`, `mtr`, `dig`, `nmap`, `ssh`, `tcpdump`, `wireshark`, `iptables`...) — প্রতিটির ৫টি উদাহরণসহ পূর্ণাঙ্গ বাংলা বই! | [📄 **পড়ো**](reference/MaksDev-Practical-Networking.md) | [📥 **PDF**](reference/MaksDev-Practical-Networking.pdf) |
| **[📕 OSI: From Search to Screen (Illustrated)](reference/OSI-Illustrated.md)** | ব্রাউজারে সার্চ লেখা থেকে স্ক্রিনে পেজ আসা পর্যন্ত ৭টি লেয়ারের পূর্ণ গল্প — ২৪টি অধ্যায় ও ৬টি কাস্টম SVG ভেক্টর ডায়াগ্রামসহ! | [📄 **পড়ো**](reference/OSI-Illustrated.md) | [📥 **PDF**](reference/OSI-Illustrated.pdf) |

---

<a id="scripts"></a>

## 🛠️ Python CLI অটোমেশন ও রাইটার স্ক্রিপ্ট (`scripts/`)

কোনো বাড়তি প্যাকেজ ইনস্টল ছাড়াই (`Python 3` থাকলেই চলবে!) টার্মিনালে চালাতে পারবে এই ৫টি টুল — বিস্তারিত গাইড: **[`scripts/README.md`](scripts/README.md)**

```bash
# ১. 🧮 যেকোনো IP/Subnet বিশ্লেষণ অথবা স্বয়ংক্রিয় VLSM অ্যাড্রেস প্ল্যান তৈরি করো!
python3 scripts/subnet_calculator.py 192.168.1.65/26
python3 scripts/subnet_calculator.py --vlsm 192.168.10.0/24 --departments "CSE:55,EEE:25,Admin:10,WAN:2"

# ২. ⚡ Packet Tracer-এ সরাসরি পেস্ট করার জন্য Cisco IOS CLI কনফিগ জেনারেট করো!
python3 scripts/ios_config_generator.py roas --vlans "10:CSE:192.168.10.0/24,20:EEE:192.168.20.0/24" --with-dhcp

# ৩. 🎯 টার্মিনালেই দাও CCNA-এর ৬৮টি আসল MCQ ও CLI শর্টকাট কুইজ পরীক্ষা!
python3 scripts/quiz_trainer.py --count 5

# ৪. ✍️ রেপোর হুবহু স্টাইলে নতুন লেসন, Extra Lab বা Problem Solve কেস জেনারেট করো!
python3 scripts/lab_writer.py lesson --num 13 --slug ospf-routing --title "OSPF Dynamic Routing"

# ৫. 🩺 পুরো রিপোজিটরির সব মার্কডাউন লিংক, ছবি ও .pkt নামকরণের স্বাস্থ্য পরীক্ষা করো!
python3 scripts/repo_doctor.py --strict
```

---

<a id="path"></a>

## 🗺️ ভিজ্যুয়াল লার্নিং ম্যাপ ও পূর্ণাঙ্গ রোডম্যাপ

```text
  🟢 Stage 1: Foundation      🟡 Stage 2: Services         🟠 Stage 3: VLAN & Switch     🔴 Stage 4: Mastery
┌────────────────────────┐  ┌─────────────────────────┐  ┌──────────────────────────┐  ┌─────────────────────────┐
│ • CCNA 01–06 (Theory)  │  │ • 03 Router DHCP        │  │ • 05 VLAN Isolation      │  │ • 08 Office Capstone 🎓 │
│ • 01 Router CLI Basics │─►│ • 04 DNS + HTTP Web     │─►│ • 06 802.1Q Trunk + ROAS │─►│ • CCNA 07–09 Capstone 🏆│
│ • 02 Static Routing    │  │ • Extras: FTP, Email,   │  │ • 07 STP, Port Security, │  │ • 10–11 Practice (30x)  │
│ • 09 Real Hardware 📷  │  │   Shared Printer 🖨️     │  │      LACP EtherChannel   │  │ • 12 Problem Bank 🛠️    │
└────────────────────────┘  └─────────────────────────┘  └──────────────────────────┘  └─────────────────────────┘
```

👉 **৩০ দিনের দৈনিক স্টাডি রুটিন, CCNA 200-301 সিলেবাস ম্যাপিং এবং রেপোর ভবিষ্যৎ উন্নয়ন পরিকল্পনা (Phase 1–5) দেখতে খোলো:**
### 🗺️ [**পূর্ণাঙ্গ রোডম্যাপ দেখো (`ROADMAP.md`) ➡**](ROADMAP.md)

---

<a id="structure"></a>

## 🗂️ ফাইল স্ট্রাকচার (Repository Architecture)

```text
Cisco-Packet-Tracer-Lab/
├── 📄 README.md                        ← 🏠 মূল ল্যান্ডিং পেজ (তুমি এখন এখানে!)
├── 📄 ROADMAP.md                       ← 🗺️ ৩০ দিনের স্টাডি প্ল্যান + Phase 1–5 উন্নয়ন রোডম্যাপ
├── 📄 CONTRIBUTING.md                  ← 🤝 নতুন লেসন বা ল্যাব যুক্ত করার নিয়মাবলি
├── 📄 RENAME-MAP.md                    ← 📁 পুরনো → নতুন ফাইল ম্যাপ ও v2.0 চেঞ্জলগ
│
├── 📁 lessons/                         ← 📚 ১২টি সিরিয়াল প্র্যাকটিক্যাল লেসন
│   ├── README.md                       ← লেসন সূচি ও প্রোগ্রেস ট্র্যাকার
│   ├── 01-router-cli-basics.md … 08-final-project.md
│   ├── 09-real-hardware.md             ← 📷 আসল রাউটার/সুইচ/কেবল + Datacenter Rack Blueprint
│   ├── 10-practice-lab.md              ← 🧪 ১০টি টাস্ক (সমাধানসহ)
│   ├── 11-practice-list.md             ← 📝 ২০টি টাস্ক (সমাধান ছাড়া)
│   ├── 12-problem-solve.md             ← 🛠️ ৬টি বাস্তব ট্রাবলশুটিং কেস ব্যাংক
│   └── 📁 images/                      ← হার্ডওয়্যার ছবি ও 802.1Q অ্যানিমেটেড GIF
│
├── 📁 ccna-fundamentals/               ← 🎓 তত্ত্ব-আগে CCNA কোর্স (০১–০৯ + ৬৮টি কুইজ)
│   ├── README.md
│   └── 01-network-basics.md … 09-capstone-university-lab.md
│
├── 📁 Extras/                          ← 📦 ৫টি বাড়তি বাস্তব সার্ভিস ও টপোলজি ল্যাব
│   ├── README.md
│   ├── ftp-server-lab.md               ← FTP আপলোড/ডাউনলোড (Port 21/20)
│   ├── email-server-lab.md             ← SMTP ও POP3 ইমেইল সার্ভার
│   ├── office-shared-printer-lab.md    ← DHCP অফিস LAN + শেয়ার্ড প্রিন্টার
│   ├── ip-subnet-tester-lab.md         ← হাতে-কলমে /26 সাবনেটিং পরীক্ষা
│   └── network-topologies-lab.md       ← ৬টি টপোলজির Simulation গাইড
│
├── 📁 reference/                       ← 📖 চিট-শিট ও ২টি পূর্ণাঙ্গ বাংলা নেটওয়ার্কিং বই
│   ├── README.md
│   ├── cli-command-cheatsheet.md       ← সব Cisco IOS কমান্ড ও এরর রেফারেন্স
│   ├── MaksDev-Practical-Networking.*  ← ৩০টি Linux/Windows কমান্ডের বই (.md + .pdf)
│   ├── OSI-Illustrated.*               ← ৭ লেয়ারের ইলাস্ট্রেটেড বই (.md + .pdf)
│   └── 📁 images/                      ← ৬টি কাস্টম SVG ডায়াগ্রাম
│
├── 📁 pkt-files/                       ← 🧰 ১৮টি প্রস্তুত Packet Tracer (.pkt) ফাইল
│   ├── README.md                       ← সম্পূর্ণ .pkt ক্যাটালগ
│   ├── 📁 labs/                        ← lesson-01 … lesson-08 (.pkt)
│   ├── 📁 practice/                    ← FTP, Email, Printer, Subnet-Tester (.pkt)
│   └── 📁 topologies/                  ← bus, star, ring, mesh, tree, hybrid (.pkt)
│
└── 📁 scripts/                         ← 🛠️ ৫টি Python 3 অটোমেশন ও রাইটার টুল
    ├── README.md
    ├── lab_writer.py                   ← নতুন লেসন / ল্যাব / প্রবলেম রাইটার
    ├── ios_config_generator.py         ← Cisco IOS CLI কনফিগ জেনারেটর
    ├── subnet_calculator.py            ← Subnetting, VLSM ও ড্রিল ক্যালকুলেটর
    ├── quiz_trainer.py                 ← টার্মিনাল CCNA MCQ ও ফ্ল্যাশকার্ড ট্রেইনার
    └── repo_doctor.py                  ← লিংক ও রিপোজিটরি স্বাস্থ্য পরীক্ষক
```

---

<a id="usage"></a>

## 🚀 কীভাবে শুরু করবে (Quick Start)

1. **[Cisco Packet Tracer](https://www.netacad.com/courses/packet-tracer)** ডাউনলোড ও ইনস্টল করো (ফ্রি NetAcad অ্যাকাউন্ট দিয়ে)।
2. রিপোজিটরিটি নিজের পিসিতে ক্লোন করো (যাতে `.pkt` ফাইল ও স্ক্রিপ্টগুলো অফলাইনেও চালাতে পারো):
   ```bash
   git clone https://github.com/MaksBloxX/Cisco-Packet-Tracer-Lab.git
   cd Cisco-Packet-Tracer-Lab
   ```
3. **[🚦 শেখার পথ](#tracks)** থেকে তোমার পছন্দের ট্র্যাক বেছে নাও এবং প্রতিটি লেসনের সাথে দেওয়া `.pkt` ফাইল খুলে হাতে-কলমে অনুশীলন করো।
4. প্রতিটি লেসন শেষে **✅ Final Checklist** পূরণ করো এবং সন্দেহ হলে টার্মিনালে `subnet_calculator.py` বা `quiz_trainer.py` চালিয়ে নিজেকে যাচাই করো!

---

<a id="contribute"></a>

## 🤝 অবদান রাখো (Contribute)

নতুন ল্যাব, ট্রাবলশুটিং কেস বা বানান সংশোধন পাঠাতে চাও? আমাদের **[🤝 Contributing Guide (`CONTRIBUTING.md`)](CONTRIBUTING.md)** দেখো — `lab_writer.py` ও `repo_doctor.py` ব্যবহার করে মাত্র কয়েক মিনিটেই PR প্রস্তুত করতে পারবে! পুরনো ফাইলের নাম ও v2.0 আপডেটের সম্পূর্ণ তালিকা দেখতে খোলো **[📁 Rename Map ও Changelog (`RENAME-MAP.md`)](RENAME-MAP.md)**।

---

<div align="center">

**Created & Maintained for Bangla Networking Learners 🇧🇩**

**⭐ রিপোজিটরিটি উপকারে এলে একটি Star দিতে ভুলবে না — তোমার একটি Star আমাদের নতুন লেসন লিখতে উৎসাহ দেয়!**

*Happy Networking! 🌐🚀*

</div>
