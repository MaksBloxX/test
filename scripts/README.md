# 🛠️ Automation & Helper Scripts (`scripts/`)

> **নেভিগেশন:** [🏠 রেপো হোম](../README.md) · [📚 মূল লেসন](../lessons/README.md) · [🎓 CCNA Fundamentals](../ccna-fundamentals/README.md) · [📖 CLI Cheat-Sheet](../reference/cli-command-cheatsheet.md) · [🗺️ রোডম্যাপ](../ROADMAP.md)

এই ফোল্ডারে রয়েছে **৫টি জিরো-ডিপেন্ডেন্সি Python 3 টুল** — যা **শিক্ষার্থী** (Subnetting হিসাব, IOS কমান্ড প্রস্তুতি, CCNA কুইজ অনুশীলন) এবং **রেপো মেইনটেইনার/লেখক** (নতুন লেসন বা প্রবলেম লেখা ও লিংক অডিট করা) উভয়ের কাজকে ১০ গুণ সহজ করে দেয়!

> 💡 **প্রয়োজনীয়তা:** শুধুমাত্র `Python 3.10+` — আলাদা কোনো `pip install` লাগবে না!

---

## 📋 স্ক্রিপ্ট তালিকা (এক নজরে)

| স্ক্রিপ্ট ফাইল | কার জন্য | মূল কাজ |
| :--- | :---: | :--- |
| [`lab_writer.py`](lab_writer.py) | ✍️ লেখক / কন্ট্রিবিউটর | রেপোর হুবহু স্টাইলে নতুন **Lesson**, **Extra Lab**, বা **Problem Solve** মার্কডাউন তৈরি করে |
| [`ios_config_generator.py`](ios_config_generator.py) | 👨‍🎓 শিক্ষার্থী / ল্যাব | রাউটার/সুইচের রেডিমেড **Cisco IOS CLI কমান্ড** (বাংলা কমেন্টসহ) জেনারেট করে |
| [`subnet_calculator.py`](subnet_calculator.py) | 🧮 শিক্ষার্থী / পরীক্ষা | **IPv4 Subnetting**, **VLSM Address Plan** টেবিল এবং **Exam Drill** প্রশ্ন তৈরি করে |
| [`quiz_trainer.py`](quiz_trainer.py) | 🎯 শিক্ষার্থী | CCNA-এর **৬৮টি আসল MCQ** এবং **Cisco CLI শর্টকাট ফ্ল্যাশকার্ড** টার্মিনালে অনুশীলন করায় |
| [`repo_doctor.py`](repo_doctor.py) | 🩺 মেইনটেইনার / CI | পুরো রেপোর ব্রোকেন লিংক, ছবি, `.pkt` নামকরণ ও মার্কডাউন স্বাস্থ্য পরীক্ষা করে |

---

## 🚀 কীভাবে চালাবে (কপি-পেস্ট উদাহরণ)

### ১. 🧮 `subnet_calculator.py` — Subnetting, VLSM ও প্র্যাকটিস ড্রিল

```bash
# যেকোনো IP/CIDR-এর পূর্ণ বিশ্লেষণ (Network, Broadcast, Usable Range, Wildcard, Binary)
python3 scripts/subnet_calculator.py 192.168.1.65/26

# একটি /24 নেটওয়ার্ককে সমান /26 সাবনেটে ভাগ করা
python3 scripts/subnet_calculator.py --split 192.168.1.0/24 --new-prefix 26

# VLSM অটো-প্ল্যানার (বড় বিভাগ থেকে ছোট ক্রমে সাজিয়ে Markdown Table বানিয়ে দেবে!)
python3 scripts/subnet_calculator.py --vlsm 192.168.10.0/24 --departments "CSE:55,EEE:25,Admin:10,WAN:2"

# পরীক্ষার প্রস্তুতির জন্য ৫টি র‍্যান্ডম Subnetting প্রশ্ন ও উত্তর তৈরি
python3 scripts/subnet_calculator.py --drill 5
```

---

### ২. ⚡ `ios_config_generator.py` — Cisco IOS CLI কমান্ড রাইটার

```bash
# কী কী টেমপ্লেট আছে তা দেখা
python3 scripts/ios_config_generator.py --list

# Router-on-a-Stick + প্রতি VLAN-এ DHCP সহ পূর্ণ Switch ও Router কনফিগ তৈরি!
python3 scripts/ios_config_generator.py roas --vlans "10:CSE:192.168.10.0/24,20:EEE:192.168.20.0/24" --with-dhcp

# দুটি রাউটারের দ্বিমুখী Static Routing স্ক্রিপ্ট
python3 scripts/ios_config_generator.py static-routing --lan1 192.168.1.0/24 --lan2 192.168.2.0/24 --wan 10.0.0.0/30

# কমেন্ট ছাড়া ফাইল হিসেবে সেভ করতে চাইলে
python3 scripts/ios_config_generator.py dhcp --pool LAB --network 192.168.5.0/24 --no-comments --save-to my-dhcp.txt
```

---

### ৩. ✍️ `lab_writer.py` — নতুন লেসন, ল্যাব ও প্রবলেম রাইটার

```bash
# নতুন সিরিয়াল লেসনের (যেমন লেসন ১৩) পূর্ণাঙ্গ বাংলা টেমপ্লেট তৈরি
python3 scripts/lab_writer.py lesson --num 13 --slug ospf-routing \
    --title "OSPF Dynamic Routing (Single-Area)" --level "🟠 Intermediate"

# Extras/ ফোল্ডারে নতুন প্র্যাকটিক্যাল ল্যাব গাইড তৈরি
python3 scripts/lab_writer.py extra --slug syslog-ntp-lab \
    --title "Syslog ও NTP Server Configuration" --pkt "Syslog-NTP.pkt"

# লেসন ১২ (Problem Solve Bank)-এ সরাসরি নতুন সমস্যা যোগ করা (--append)
python3 scripts/lab_writer.py problem --num 7 \
    --title "OSPF Neighbor তৈরি হচ্ছে না (Area Mismatch)" --append
```

---

### ৪. 🎯 `quiz_trainer.py` — ইন্টারেক্টিভ CCNA কুইজ ও CLI ফ্ল্যাশকার্ড

```bash
# কোন লেসনে কয়টি কুইজ আছে দেখা
python3 scripts/quiz_trainer.py --list

# ইন্টারেক্টিভ ৫টি র‍্যান্ডম CCNA MCQ পরীক্ষা দাও!
python3 scripts/quiz_trainer.py --count 5

# শুধু Subnetting (লেসন ০৫)-এর কুইজ অনুশীলন করো
python3 scripts/quiz_trainer.py --lesson 5 --count 7

# Cisco IOS কমান্ড শর্টকাট ফ্ল্যাশকার্ড মোড
python3 scripts/quiz_trainer.py --mode cli --count 5
```

---

### ৫. 🩺 `repo_doctor.py` — রিপোজিটরি হেলথ ও লিংক চেকার

নতুন লেসন বা ছবি যোগ করার পর `git push` দেওয়ার আগে একবার চালিয়ে দেখে নাও সব লিংক ঠিক আছে কি না:

```bash
python3 scripts/repo_doctor.py --strict
```

---

> **নেভিগেশন:** [🏠 রেপো হোম](../README.md) · [🗺️ রোডম্যাপ](../ROADMAP.md) · [🤝 কীভাবে কন্ট্রিবিউট করবে](../CONTRIBUTING.md)
