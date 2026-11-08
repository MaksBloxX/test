# 📦 Extra Practical Labs — বাড়তি প্র্যাকটিক্যাল ল্যাবসমূহ

> **নেভিগেশন:** [🏠 রেপো হোম](../README.md) · [📚 মূল লেসন (০১–১২)](../lessons/README.md) · [🎓 CCNA Fundamentals](../ccna-fundamentals/README.md) · [📖 CLI Cheat-Sheet](../reference/cli-command-cheatsheet.md)

মূল ১২টি সিরিয়াল লেসনের বাইরে বাস্তব অফিস ও পরীক্ষার (CCNA / University Lab Viva) জন্য গুরুত্বপূর্ণ **৫টি বিশেষ প্র্যাকটিক্যাল ল্যাব** এখানে সাজানো হয়েছে। প্রতিটি ল্যাবের সাথে সরাসরি `.pkt` ফাইল যুক্ত আছে!

---

## 📋 ল্যাব তালিকা (ক্লিক করলেই গাইডে যাবে)

| # | ল্যাব গাইড | যা শিখবে | লেভেল | সংযুক্ত `.pkt` ফাইল |
| :---: | :--- | :--- | :---: | :--- |
| **০১** | [🌐 **FTP Server Configuration Lab**](ftp-server-lab.md) | আলাদা সাবনেটে FTP Server সেটআপ, ইউজার পারমিশন (`RWDNL`), `put`/`get`/`rename`/`delete` দিয়ে ফাইল আপলোড ও ডাউনলোড | 🟢→🟡 | [`FTP-Server.pkt`](../pkt-files/practice/FTP-Server.pkt) |
| **০২** | [📧 **Email Server Configuration Lab**](email-server-lab.md) | দুই LAN সাবনেটের মাঝে SMTP ও POP3 সার্ভিস কনফিগার, ডোমেন সেটআপ ও PC0 ↔ PC1 ইমেইল আদান-প্রদান | 🟡 Intermediate | [`Email-Server.pkt`](../pkt-files/practice/Email-Server.pkt) |
| **০৩** | [🖨️ **Office Shared Printer Network Lab**](office-shared-printer-lab.md) | অফিস LAN-এ Static IP নেটওয়ার্ক প্রিন্টার, DHCP Excluded Range সুরক্ষা ও সব PC থেকে শেয়ার্ড প্রিন্টার অ্যাক্সেস | 🟢 Beginner | [`office-shared-printer-network.pkt`](../pkt-files/practice/office-shared-printer-network.pkt) |
| **০৪** | [🧮 **IP Subnet Tester Lab**](ip-subnet-tester-lab.md) | `/24`, `/25`, `/26`, `/30` সাবনেট সীমানা Packet Tracer-এ সরাসরি পরীক্ষা — কখন সুইচেই Ping হয় আর কখন Router লাগে | 🟡 Intermediate | [`ip-subnet-tester.pkt`](../pkt-files/practice/ip-subnet-tester.pkt) |
| **০৫** | [🕸️ **6 Network Topologies Visual Lab**](network-topologies-lab.md) | Bus, Star, Ring, Mesh, Tree ও Hybrid — ৬টি টপোলজি Simulation Mode-এ প্যাকেট চালিয়ে তুলনা ও কেবল সূত্র যাচাই | 🟢 সবার জন্য | [`pkt-files/topologies/*.pkt`](../pkt-files/topologies/) |

---

## 🧭 কোন ল্যাবটি কখন করবে?

* **লেসন ০১ ও CCNA ০১ পড়ার সাথে:** [🕸️ 6 Network Topologies Lab](network-topologies-lab.md) খুলে Simulation Mode-এ প্যাকেট চলাচল দেখো।
* **লেসন ০৩ (DHCP) শেষ করার পর:** [🖨️ Office Shared Printer Network Lab](office-shared-printer-lab.md) অনুশীলন করো।
* **CCNA ০৫–০৬ (Subnetting) পড়ার পর:** [🧮 IP Subnet Tester Lab](ip-subnet-tester-lab.md) দিয়ে নিজের হিসাব Packet Tracer-এ প্রমাণ করো।
* **লেসন ০৪ (DNS/HTTP) শেষ করার পর:** [🌐 FTP Server Lab](ftp-server-lab.md) এবং [📧 Email Server Lab](email-server-lab.md) সম্পন্ন করো — এতে Application Layer-এর সব প্রধান প্রোটোকল (`HTTP`, `DNS`, `DHCP`, `FTP`, `SMTP`, `POP3`) হাতের মুঠোয় চলে আসবে!

---

> **নেভিগেশন:** [🏠 রেপো হোম](../README.md) · [📚 মূল লেসন (০১–১২)](../lessons/README.md) · [🧰 সব .pkt ফাইল](../pkt-files/README.md) · [📖 CLI Cheat-Sheet](../reference/cli-command-cheatsheet.md)

**Tags:** `#extra-labs` `#ftp` `#email` `#smtp` `#pop3` `#shared-printer` `#subnet-tester` `#topologies`
