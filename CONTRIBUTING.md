# 🤝 কীভাবে কন্ট্রিবিউট করবে (Contributing Guide)

> **নেভিগেশন:** [🏠 রেপো হোম](README.md) · [🗺️ রোডম্যাপ](ROADMAP.md) · [🛠️ স্ক্রিপ্ট গাইড](scripts/README.md)

**Cisco Packet Tracer Lab** রিপোজিটরিতে অবদান রাখার আগ্রহের জন্য ধন্যবাদ! বানান সংশোধন, নতুন ট্রাবলশুটিং সমস্যা, নতুন `.pkt` ল্যাব বা নতুন লেসন — যেকোনো গঠনমূলক অবদান স্বাগতম।

---

## 🎯 কী কী যোগ বা উন্নত করতে পারো?

1. **🐛 ভুল বা টাইপো সংশোধন:** কোনো CLI কমান্ড, IP টেবিল বা বাংলা বানানে অসঙ্গতি পেলে ঠিক করা।
2. **🛠️ নতুন Problem Solve কেস:** ল্যাব করতে গিয়ে যে সমস্যায় আটকেছিলে তার সমাধান [`lessons/12-problem-solve.md`](lessons/12-problem-solve.md)-এ যোগ করা।
3. **📦 নতুন Extra Lab:** যেমন `Syslog + NTP`, `VoIP IP Phone`, `Wireless WLC`, বা `SSH Hardening` ল্যাব গাইড ও `.pkt` ফাইল।
4. **🚀 রোডম্যাপের পরবর্তী লেসন:** [`ROADMAP.md`](ROADMAP.md)-এর Phase 2 বা Phase 3 থেকে যেকোনো টপিক বেছে নেওয়া।

---

## ⚡ দ্রুত কাজের নিয়ম (Helper Script ব্যবহার করে)

### ১. রিপোজিটরি Fork ও Clone করো
```bash
git clone https://github.com/<your-username>/Cisco-Packet-Tracer-Lab.git
cd Cisco-Packet-Tracer-Lab
git checkout -b feat/my-new-lab
```

### ২. `lab_writer.py` দিয়ে স্ট্যান্ডার্ড ফরম্যাটে ফাইল তৈরি করো
যাতে রেপোর সব ফাইলের নেভিগেশন ও গঠন একই রকম থাকে:

```bash
# নতুন সিরিয়াল লেসন বানাতে:
python3 scripts/lab_writer.py lesson --num 13 --slug ospf-routing --title "OSPF Dynamic Routing"

# নতুন Extra Lab বানাতে:
python3 scripts/lab_writer.py extra --slug voip-phone-lab --title "VoIP IP Phone Configuration" --pkt "VoIP-Lab.pkt"

# লেসন ১২-তে নতুন সমস্যা যোগ করতে:
python3 scripts/lab_writer.py problem --num 7 --title "তোমার সমস্যার শিরোনাম" --append
```

### ৩. লেখার স্টাইল গাইড (Style Checklist)
* **ভাষা:** সহজ, প্রাঞ্জল বাংলা + প্রমিত ইংরেজি টেকনিক্যাল শব্দ (`Router`, `Subnet Mask`, `Trunk`, `Default Gateway`)।
* **CLI কোড ব্লক:** সিসকো কমান্ডের জন্য ` ```cisco `, পিসি প্রম্পটের জন্য ` ```cmd `, এবং টপোলজি ডায়াগ্রামের জন্য ` ```text ` ব্যবহার করো।
* **`.pkt` নামকরণ:** সিরিয়াল লেসনের ফাইল হলে `pkt-files/labs/lesson-NN-<slug>.pkt` নামে রাখো।
* **ভেরিফিকেশন:** প্রতিটি ল্যাবে অবশ্যই `show` এবং `ping` কমান্ডের Expected Output ও একটি `✅ Final Checklist` রাখো।

### ৪. PR পাঠানোর আগে অটোমেটিক অডিট চালাও!
```bash
python3 scripts/repo_doctor.py --strict
```
যদি `✅ 0 Broken Links / Code Fence Errors!` দেখায়, তবে নিশ্চিন্তে Commit করে Pull Request খুলে দাও! 🎉
