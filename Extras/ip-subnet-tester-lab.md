# 🧮 Extra Lab ০৪ · IP Subnet Tester Lab (হাতে-কলমে Subnetting প্রমাণ)

> **নেভিগেশন:** [⬅ Shared Printer Lab](office-shared-printer-lab.md) · [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [পরের ল্যাব: 6 Topologies ➡](network-topologies-lab.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| কাগজে করা Subnetting হিসাব (`/24`, `/26`, `/30`) Packet Tracer-এ সরাসরি Ping দিয়ে সত্যতা যাচাই করা | ~৩৫ মিনিট | 🟡 Intermediate | [`ip-subnet-tester.pkt`](../pkt-files/practice/ip-subnet-tester.pkt) |

**Tags:** `#subnetting` `#subnet-tester` `#cidr` `#block-size` `#vlsm` `#hands-on-proof`

---

## 🎯 এই ল্যাবে যা শিখবে

অনেকেই খাতায় Subnetting অঙ্ক করে, কিন্তু মনের ভেতর প্রশ্ন থেকে যায়: *"একই সুইচে লাগানো দুটো পিসিতে শুধু Subnet Mask বদলে দিলেই কি সত্যিই যোগাযোগ বন্ধ হয়ে যায়?"* — এই ল্যাবটি সেই প্রশ্নের **সরাসরি ব্যবহারিক প্রমাণ (Lab Proof)**!

1. একই ফিজিক্যাল Switch-এ থেকেও ভিন্ন সাবনেটের PC কেন সরাসরি কথা বলতে পারে না তা চোখে দেখা
2. `/26` (`255.255.255.192`, Block Size = `64`)-এর সাবনেট সীমানা পরীক্ষা করা
3. Network Address ও Broadcast Address পিসিতে বসাতে গেলে Cisco Packet Tracer কী এরর দেয় তা দেখা
4. রেপোর [`scripts/subnet_calculator.py`](../scripts/subnet_calculator.py) টুলের সাথে নিজের ফলাফল মিলিয়ে নেওয়া

> 📚 **তত্ত্ব ঝালিয়ে নিতে:** [CCNA লেসন ০৫ · Subnetting Basics](../ccna-fundamentals/05-subnetting-basics.md) এবং [CCNA লেসন ০৬ · VLSM](../ccna-fundamentals/06-subnetting-vlsm.md)

---

## ১. টেস্ট টপোলজি (এক সুইচ, চার PC)

`pkt-files/practice/ip-subnet-tester.pkt` ফাইলটি খোলো অথবা নিচের সহজ টপোলজিটি বানাও:

```text
                        [ Switch 2960 ]
           ┌───────────────┼───────────────┬───────────────┐
         Fa0/1           Fa0/2           Fa0/3           Fa0/4
           │               │               │               │
        [ PC0 ]         [ PC1 ]         [ PC2 ]         [ PC3 ]
      Subnet A        Subnet A        Subnet B        Subnet B
     192.168.1.10    192.168.1.50    192.168.1.65    192.168.1.120
         /26             /26             /26             /26
```

---

## ২. `/26` সাবনেট হিসাব (Block Size = 64)

`192.168.1.0/24`-কে `/26` (`255.255.255.192`) দিয়ে ভাগ করলে ম্যাজিক ব্লক সাইজ হয় `256 - 192 = 64`:

| Subnet নাম | Network ID | Usable Host Range | Broadcast IP | এই ল্যাবে কারা আছে |
| :--- | :--- | :--- | :--- | :--- |
| **Subnet A (১ম)** | `192.168.1.0/26` | `192.168.1.1` – `192.168.1.62` | `192.168.1.63` | **PC0** (`.10`), **PC1** (`.50`) |
| **Subnet B (২য়)** | `192.168.1.64/26` | `192.168.1.65` – `192.168.1.126` | `192.168.1.127` | **PC2** (`.65`), **PC3** (`.120`) |
| **Subnet C (৩য়)** | `192.168.1.128/26` | `192.168.1.129` – `192.168.1.190` | `192.168.1.191` | — |
| **Subnet D (৪র্থ)** | `192.168.1.192/26` | `192.168.1.193` – `192.168.1.254` | `192.168.1.255` | — |

---

## ৩. চারটি মজার পরীক্ষা (Experiments)

### 🧪 Experiment 1: `/26` মাস্কে কে কাকে Ping পায়?
চারটি PC-তেই Subnet Mask বসাও **`255.255.255.192`** (`/26`), কোনো Default Gateway দিও না:
* **PC0:** `192.168.1.10` · **PC1:** `192.168.1.50`
* **PC2:** `192.168.1.65` · **PC3:** `192.168.1.120`

এবার PC0 থেকে পরীক্ষা করো:
1. `ping 192.168.1.50` (PC1) → **✅ Reply!** (কারণ `.10` ও `.50` দুটোই `0–63` ব্লকে!)
2. `ping 192.168.1.65` (PC2) → **❌ Request timed out!**

> 🧠 **কেন Ping গেল না? সুইচ তো একই!**
> পিং পাঠানোর আগেই PC0 নিজের IP (`192.168.1.10`) এবং গন্তব্যের IP (`192.168.1.65`)-এর সাথে নিজের Subnet Mask (`255.255.255.192`) **AND** করে দেখে। PC0 বুঝতে পারে `.65` তার নিজের সাবনেটের বাইরে! তাই সে সুইচে সরাসরি ARP Request-ই পাঠায় না — সে খোঁজে **Default Gateway (Router)**। Gateway না থাকায় প্যাকেট পিসির ভেতরেই ড্রপ হয়ে যায়!

---

### 🧪 Experiment 2: শুধু Subnet Mask `/24` করে দিলেই জাদু!
এবার চারটি PC-র IP হুবহু এক রেখে শুধু Subnet Mask বদলে **`255.255.255.0`** (`/24`) করে দাও।
* আবার PC0 থেকে `ping 192.168.1.65` দাও → **✅ সাথে সাথে Reply!**
* কারণ `/24`-এ `.1` থেকে `.254` সবাই একই পরিবারে চলে এসেছে!

---

### 🧪 Experiment 3: নিষিদ্ধ ঠিকানা (Network ও Broadcast IP) বসানোর চেষ্টা!
আবার Mask `255.255.255.192` (`/26`) রেখে PC1-এ নিচের IP দুটি বসিয়ে দেখো কী ঘটে:
1. IP বসাও `192.168.1.63` (Subnet A-র Broadcast IP) → Packet Tracer সাথে সাথে পপ-আপ এরর দেবে: **`Invalid IP for this subnet mask entered!`**
2. IP বসাও `192.168.1.64` (Subnet B-র Network ID) → আবারও **`Invalid IP for this subnet mask entered!`**

> 💡 `/24` থাকলে `.63` আর `.64` বৈধ হোস্ট ছিল, কিন্তু `/26` করার সাথে সাথে `.63` হয়ে গেছে Broadcast আর `.64` হয়ে গেছে পরের সাবনেটের Network ID!

---

### 🧪 Experiment 4: Router যুক্ত করে দুই `/26` সাবনেট জোড়া লাগানো
একটি **Cisco 1941 Router** নিয়ে সুইচে (বা দুটি সুইচে/Subinterface-এ) যুক্ত করে:
* Subnet A Gateway: `192.168.1.1 /26`
* Subnet B Gateway: `192.168.1.65 /26` (তখন PC2-কে দাও `.66`)
এখন PC0 থেকে PC2-এ পিং দিলে রাউটার হয়ে সফলভাবে Reply আসবে (`TTL=127`)!

---

## ৪. 🛠️ Python Script দিয়ে নিমেষে মিলিয়ে নাও!

এই রিপোজিটরির বিল্ট-ইন সাবনেট ক্যালকুলেটর চালিয়ে যেকোনো প্রশ্ন ১ সেকেন্ডে যাচাই করতে পারো:

```bash
python3 scripts/subnet_calculator.py 192.168.1.65/26
```

অথবা নিজে অনুশীলনের জন্য ৫টি নতুন প্রশ্ন তৈরি করতে:
```bash
python3 scripts/subnet_calculator.py --drill 5
```

---

## ✅ Final Checklist

| পরীক্ষা | যা প্রমাণ করলে | অবস্থা |
| :--- | :--- | :---: |
| `/26` মাস্কে `.10` → `.50` Ping | একই সাবনেট ব্লকে (`1–62`) পিং সফল ✅ | ☐ |
| `/26` মাস্কে `.10` → `.65` Ping | একই সুইচে থেকেও ভিন্ন সাবনেটে পিং ব্যর্থ ❌ | ☐ |
| `.63` ও `.64` বসানোর চেষ্টা (`/26`-এ) | Broadcast ও Network ID হোস্টে বসানো যায় না তা প্রমাণিত ✅ | ☐ |
| Mask `/24`-এ পরিবর্তন | সব ৪টি পিসি একই সাবনেটে এসে পিং সফল ✅ | ☐ |

---

> **নেভিগেশন:** [⬅ Shared Printer Lab](office-shared-printer-lab.md) · [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [পরের ল্যাব: 6 Topologies ➡](network-topologies-lab.md)

**Tags:** `#subnet-tester` `#cidr` `#slash-26` `#network-id` `#broadcast-ip` `#ccna-subnetting`
