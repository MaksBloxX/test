# 🧰 Packet Tracer (`.pkt`) Files — সম্পূর্ণ ল্যাব ক্যাটালগ

> **নেভিগেশন:** [🏠 রেপো হোম](../README.md) · [📚 মূল লেসন](../lessons/README.md) · [📦 Extra Labs](../Extras/README.md) · [📖 CLI Cheat-Sheet](../reference/cli-command-cheatsheet.md)

এই ফোল্ডারে মোট **১৮টি প্রস্তুত Cisco Packet Tracer (`.pkt`) ফাইল** তিনটি সাবফোল্ডারে গুছিয়ে রাখা হয়েছে। প্রতিটি ফাইল ডাউনলোড করে সরাসরি **Cisco Packet Tracer (v8.0 বা তদূর্ধ্ব প্রস্তাবিত)** সফটওয়্যারে ওপেন করে অনুশীলন করতে পারবে।

---

## ১. 📁 `labs/` — সিরিয়াল লেসনের ল্যাব ফাইল (৮টি)

| `.pkt` ফাইল | সংশ্লিষ্ট লেসন গাইড | মূল বিষয়বস্তু |
| :--- | :--- | :--- |
| [`lesson-01-router-cli-basics.pkt`](labs/lesson-01-router-cli-basics.pkt) | [লেসন ০১ · Router CLI Basics](../lessons/01-router-cli-basics.md) | ১ Router + ১ Switch + ২ PC প্রথম Ping ল্যাব |
| [`lesson-02-static-routing.pkt`](labs/lesson-02-static-routing.pkt) | [লেসন ০২ · Static Routing](../lessons/02-static-routing.md) | ২ Router + `/30` WAN + দ্বিমুখী `ip route` |
| [`lesson-03-dhcp.pkt`](labs/lesson-03-dhcp.pkt) | [লেসন ০৩ · Router DHCP](../lessons/03-dhcp.md) | `ip dhcp pool`, `excluded-address`, Auto IP |
| [`lesson-04-dns-http-server.pkt`](labs/lesson-04-dns-http-server.pkt) | [লেসন ০৪ · DNS ও HTTP Server](../lessons/04-dns-http-server.md) | `www.office.local` A Record + ওয়েব সার্ভার |
| [`lesson-05-vlan.pkt`](labs/lesson-05-vlan.pkt) | [লেসন ০৫ · VLAN Isolation](../lessons/05-vlan.md) | VLAN 10 (CSE) ও VLAN 20 (EEE) বিভাজন |
| [`lesson-06-trunk-inter-vlan.pkt`](labs/lesson-06-trunk-inter-vlan.pkt) | [লেসন ০৬ · Trunk ও Inter-VLAN](../lessons/06-trunk-inter-vlan.md) | 802.1Q Trunk + Router-on-a-Stick (`dot1Q`) |
| [`lesson-07-switching.pkt`](labs/lesson-07-switching.pkt) | [লেসন ০৭ · Switching Technologies](../lessons/07-switching.md) | STP, Port Security ও LACP EtherChannel |
| [`lesson-08-final-project.pkt`](labs/lesson-08-final-project.pkt) | [লেসন ০৮ · Final Project](../lessons/08-final-project.md) | সম্পূর্ণ অফিস নেটওয়ার্ক (Capstone) |

---

## ২. 📁 `practice/` — এক্সট্রা প্র্যাকটিক্যাল ল্যাব ফাইল (৪টি)

| `.pkt` ফাইল | সংশ্লিষ্ট গাইড | মূল বিষয়বস্তু |
| :--- | :--- | :--- |
| [`FTP-Server.pkt`](practice/FTP-Server.pkt) | [🌐 FTP Server Lab](../Extras/ftp-server-lab.md) | FTP ফাইল আপলোড (`put`) ও ডাউনলোড (`get`) |
| [`Email-Server.pkt`](practice/Email-Server.pkt) | [📧 Email Server Lab](../Extras/email-server-lab.md) | SMTP ও POP3 ইমেইল সার্ভার কনফিগারেশন |
| [`office-shared-printer-network.pkt`](practice/office-shared-printer-network.pkt) | [🖨️ Office Shared Printer Lab](../Extras/office-shared-printer-lab.md) | DHCP LAN + Static IP শেয়ার্ড নেটওয়ার্ক প্রিন্টার |
| [`ip-subnet-tester.pkt`](practice/ip-subnet-tester.pkt) | [🧮 IP Subnet Tester Lab](../Extras/ip-subnet-tester-lab.md) | সাবনেট সীমানা (`/24`, `/26`, `/30`) পরীক্ষা |

---

## ৩. 📁 `topologies/` — ৬টি নেটওয়ার্ক টপোলজি ফাইল (৬টি)

সমন্বিত গাইড: **[🕸️ 6 Network Topologies Visual & Simulation Guide](../Extras/network-topologies-lab.md)**

| `.pkt` ফাইল | টপোলজির ধরন | বৈশিষ্ট্য |
| :--- | :--- | :--- |
| [`bus-topology.pkt`](topologies/bus-topology.pkt) | 🚌 Bus Topology | একক ব্যাকবোন লাইন |
| [`star-topology.pkt`](topologies/star-topology.pkt) | ⭐ Star Topology | কেন্দ্রীয় Switch ভিত্তিক আধুনিক ল্যান |
| [`ring-topology.pkt`](topologies/ring-topology.pkt) | 💍 Ring Topology | বৃত্তাকার সংযোগ ও STP Blocking পোর্ট |
| [`mesh-topology.pkt`](topologies/mesh-topology.pkt) | 🕸️ Mesh Topology | সর্বোচ্চ Redundancy ($\frac{N(N-1)}{2}$ কেবল) |
| [`tree-topology.pkt`](topologies/tree-topology.pkt) | 🌳 Tree Topology | Core → Department শাখা-প্রশাখা গঠন |
| [`hybrid-topology.pkt`](topologies/hybrid-topology.pkt) | 🧬 Hybrid Topology | একাধিক টপোলজির বাস্তব সংমিশ্রণ |

---

## 📌 নতুন `.pkt` যোগ করার নামকরণ নিয়ম

* সিরিয়াল লেসনের জন্য: `pkt-files/labs/lesson-NN-<slug>.pkt` (যেমন: `lesson-12-problem-solve.pkt`)
* বাড়তি প্র্যাকটিস ল্যাবের জন্য: `pkt-files/practice/<lab-name>.pkt` + `Extras/<lab-name>-lab.md`

---

> **নেভিগেশন:** [🏠 রেপো হোম](../README.md) · [📚 মূল লেসন](../lessons/README.md) · [📦 Extra Labs](../Extras/README.md)
