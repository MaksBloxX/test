# লেসন ০৫ · VLAN Configuration ও VLAN Isolation

> 🌐 **English:** [Read this guide in English](../en/lessons/05-vlan.md) · [English track index](../en/README.md)

> **নেভিগেশন:** [⬅ লেসন ০৪](04-dns-http-server.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৬ ➡](06-trunk-inter-vlan.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| একটি Switch-এ VLAN তৈরি, Port Assign ও VLAN Isolation প্রমাণ | ~৪৫ মিনিট | 🟡 Intermediate | [lesson-05-vlan.pkt](../pkt-files/labs/lesson-05-vlan.pkt) |

**Tags:** `#vlan` `#switch` `#broadcast-domain` `#isolation` `#access-port` `#interface-range` `#vlan-10-20`

---

### 🖼️ চিত্রে বোঝো: একটি সুইচে দুটি বিচ্ছিন্ন VLAN

![একটি সুইচে দুটি বিচ্ছিন্ন VLAN — VLAN 10-এর PC-গুলো নিজেদের মধ্যে কথা বলে; VLAN 20-তে যেতে হলে রাউটার লাগবে।](../assets/diagrams/lesson-05-vlan-isolation.svg)

> **ছবির সারকথা:** VLAN 10-এর PC-গুলো নিজেদের মধ্যে কথা বলে; VLAN 20-তে যেতে হলে রাউটার লাগবে।

![VLAN isolation টপোলজি, কনফিগারেশন ও যাচাইয়ের ছয় ধাপ দেখানো ৩০ সেকেন্ডের শিক্ষামূলক GIF; Packet Tracer রেকর্ডিং নয়।](../assets/gifs/05-vlan.gif)

> 🎞️ **৩০ সেকেন্ডে মনে রাখো:** এটি উপরের ডায়াগ্রামের ওপর ভিত্তি করে বানানো ছয় ধাপের ভিজ্যুয়াল সারাংশ; বাস্তব Packet Tracer run, packet capture বা ফলের প্রমাণ নয়। [সব GIF-এর topic search name ও গুরুত্ব](../GIF-CATALOG.md) দেখো।


---

## 🎯 এই লেসনে যা শিখবে

1. **VLAN কী** এবং কেন এটি নেটওয়ার্ক নিরাপত্তা ও পারফরম্যান্সের জন্য দরকার
2. Switch-এ `vlan` কমান্ড দিয়ে **VLAN তৈরি** করা
3. `switchport access vlan` দিয়ে **Port Assign** করা
4. `show vlan brief` দিয়ে **ভেরিফিকেশন**
5. **একই VLAN = Ping ✅**, **ভিন্ন VLAN = Ping ❌** — Isolation প্রমাণ
6. **`interface range`** দিয়ে একসাথে একাধিক পোর্ট Assign — আর PC বাড়লে/ফাঁকা পোর্ট রাখলে রেঞ্জ কীভাবে বদলাবে


### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ |
| :--- | :--- |
| **VLAN** (*Virtual LAN*) | একটি ফিজিক্যাল সুইচকে সফটওয়্যার দিয়ে একাধিক আলাদা লজিক্যাল গ্রুপে ভাগ করা |
| **Broadcast Domain** | যতদূর পর্যন্ত একটি ব্রডকাস্ট মেসেজ ছড়াতে পারে — প্রতিটি VLAN একেকটি আলাদা Broadcast Domain |
| **Access Port** | সুইচের যে পোর্টে PC/Printer/Server লাগে এবং শুধুমাত্র **একটি** নির্দিষ্ট VLAN বহন করে |
| **VLAN Isolation** | রাউটার ছাড়া এক VLAN-এর পিসি অন্য VLAN-এর পিসির সাথে কথা বলতে না পারার নিরাপত্তা বৈশিষ্ট্য |

> 🔗 **তত্ত্ব ঝালিয়ে নিতে:** [CCNA ০৩ · MAC, Ethernet ও ARP](../ccna-fundamentals/03-mac-ethernet-arp.md)

---

# 📖 Part 1 — VLAN কী?

**VLAN** = *Virtual Local Area Network* — একটি ফিজিক্যাল সুইচকে সফটওয়্যারের মাধ্যমে একাধিক **আলাদা লজিক্যাল সুইচে** ভাগ করা।

### 🔹 VLAN ছাড়া (সবাই এক Broadcast Domain):
```text
              Switch (সব এক নেটওয়ার্ক)
   ┌───────┬───────────┬───────┐
  PC0     PC1         PC2     PC3    ← সবার ট্রাফিক একসাথে, একটি ভুল ব্রডকাস্ট = সবাই ক্ষতিগ্রস্ত
```

### 🔹 VLAN সহ (আলাদা আলাদা Broadcast Domain):
```text
              Switch
   ┌───────┬───────────┬───────┐
  PC0     PC1         PC2     PC3
[── VLAN 10 ──]     [── VLAN 20 ──]
    CSE গ্রুপ           EEE গ্রুপ
```

## 🧠 VLAN কেন ব্যবহার করা হয়?

| সুবিধা | ব্যাখ্যা |
| :--- | :--- |
| **🔒 নিরাপত্তা** | VLAN 10-এর ইউজার VLAN 20-এর তথ্য দেখতে পারবে না |
| **📡 Broadcast Control** | ব্রডকাস্ট ট্রাফিক নিজের VLAN-এই সীমাবদ্ধ থাকে |
| **⚙️ সহজ ব্যবস্থাপনা** | ইউজারকে ঘর বদলানোর দরকার নেই — শুধু Port-এর VLAN বদলালেই হবে |
| **🚀 পারফরম্যান্স** | ছোট ছোট গ্রুপে ট্রাফিক ভাগ হয়ে নেটওয়ার্ক দ্রুত চলে |

---

# 🧩 Part 2 — Lab Setup

**ডিভাইস:** ১ × Switch (2960) · ৪ × PC (PC-PT)

```text
                         Switch0
       ┌─────────────┬─────────────┬─────────────┐
     Fa0/1         Fa0/2         Fa0/3         Fa0/4
       │             │             │             │
      PC0           PC1           PC2           PC3
 192.168.10.1  192.168.10.2  192.168.20.1  192.168.20.2
```

| VLAN | নাম | Port | Subnet | PC |
| :---: | :--- | :--- | :--- | :--- |
| **10** | CSE | Fa0/1, Fa0/2 | `192.168.10.0/24` | PC0, PC1 |
| **20** | EEE | Fa0/3, Fa0/4 | `192.168.20.0/24` | PC2, PC3 |

### 🔌 Cable: সবক্ষেত্রে **Copper Straight-Through** (PC ↔ Switch)

---

# ⚙️ Part 3 — Switch Configuration

## Step 1: VLAN তৈরি করো

```cisco
enable
configure terminal
hostname SW1

vlan 10
 name CSE
 exit

vlan 20
 name EEE
 exit
```

**যাচাই:**
```cisco
show vlan brief
```
```text
VLAN Name                             Status    Ports
10   CSE                              active
20   EEE                              active
```

## Step 2: Port-গুলো VLAN-এ Assign করো

**VLAN 10 (CSE) — Fa0/1 ও Fa0/2:**
```cisco
interface range fastEthernet 0/1 - 2
 switchport mode access
 switchport access vlan 10
 exit
```

**VLAN 20 (EEE) — Fa0/3 ও Fa0/4:**
```cisco
interface range fastEthernet 0/3 - 4
 switchport mode access
 switchport access vlan 20
 exit

end
copy running-config startup-config
```

> 💡 `switchport mode access` = এই পোর্টটি শুধুমাত্র একটি VLAN-এর End Device-এর জন্য (PC, Printer)।

### 🔢 `interface range fastEthernet 0/1 - 2` — এই সংখ্যাগুলো মানে কী?

কমান্ডটাকে টুকরো করে দেখি:

| অংশ | মানে |
| :--- | :--- |
| `interface range` | একসাথে **একাধিক পোর্ট** সিলেক্ট করে সবগুলোতে একই কনফিগ বসানো |
| `fastEthernet` | পোর্টের টাইপ — সুইচের সাধারণ পোর্ট (সংক্ষেপে `Fa` — টাইপে `fas` বা `fa` লিখলেই চলে ✅) |
| `0/` | Slot/Module 0 — ছোট সুইচে সবসময় এটাই |
| `1 - 2` | পোর্ট **1** থেকে পোর্ট **2** পর্যন্ত → অর্থাৎ **Fa0/1 ও Fa0/2** দুটোই |

**কেন এখানে `1 - 2` লেখা?** — কারণ এই lab-এ VLAN 10-এর ২টা PC ঠিক **Fa0/1** ও **Fa0/2**-তে লাগানো আছে (উপরে Part 2-এর Connection Table দেখো)।

> 🧠 **লজিক:** `interface range`-এর সংখ্যা আসে **তোমার টোপোলজি থেকে** — ওই VLAN-এর ডিভাইসগুলো কোন কোন পোর্টে লাগানো, ঠিক সেই হিসাবে রেঞ্জ লিখবে। এলোমেলো সংখ্যা দেওয়ার দরকার নেই।

> ⚡ **Shortcut:** পুরো `fastEthernet` লিখতে হয় না — `interface range fas 0/1 - 2` লিখলেই একই কাজ ✅ **টেস্ট করা**। আর `interface` = `int`। কেন এসব ছোট করে লেখা যায় — [লেসন ০১](01-router-cli-basics.md)-এর ⚡ Shortcut সেকশন বা [Cheat-Sheet](../reference/cli-command-cheatsheet.md) দেখো।

### 📈 মানুষ/PC বাড়লে রেঞ্জ কীভাবে বদলাবে

ধরো, CSE department-এ ২টার বদলে **৫ জন** লাগবে, EEE-তেও **৫ জন**:

| পরিস্থিতি | VLAN 10 (CSE) | VLAN 20 (EEE) |
| :--- | :--- | :--- |
| **এই lab:** 2 PC + 2 PC | `interface range fastEthernet 0/1 - 2` | `interface range fastEthernet 0/3 - 4` |
| **5 + 5 জন**, সবাই পাশাপাশি | `interface range fastEthernet 0/1 - 5` | `interface range fastEthernet 0/6 - 10` |
| **5 + 5 জন**, মাঝে পোর্ট ফাঁকা রেখে | `interface range fastEthernet 0/1 - 5` | `interface range fastEthernet 0/8 - 12` |

* সারি ২: CSE-র ৫ জন → `0/1` থেকে `0/5` পর্যন্ত; তারপর EEE-র ৫ জন শুরু হয়েছে `0/6` থেকে → `0/6 - 10`
* সারি ৩: `0/6` ও `0/7` ছেড়ে দিয়ে (ফাঁকা রেখে) EEE শুরু হলে `0/8` থেকে → রেঞ্জ `0/8 - 12`

> ✅ **ফাঁকা পোর্ট রাখা সম্পূর্ণ ঠিক!** যে পোর্টে কিছু লাগানো নেই, সেটা নিজে থেকেই Default VLAN 1-এ পড়ে থাকে — কোনো সমস্যা করে না। পরে দরকার হলে ওই ফাঁকা পোর্টেও নতুন ডিভাইস লাগিয়ে Assign করা যাবে।

> 📌 পোর্টগুলো একেবারে পাশাপাশি না থাকলে **কমা** দিয়েও এক range-এ দেওয়া যায়:
> ```cisco
> interface range fastEthernet 0/8 - 10, fastEthernet 0/12
> ```
> এতে Fa0/8, Fa0/9, Fa0/10 ও Fa0/12 — চারটে পোর্ট একসাথে সিলেক্ট হবে (Fa0/11 বাদ)।

### 🧠 নতুন PC বসালে মনে রাখার ৩ ধাপ

1. **পোর্ট ঠিক করো** — নতুন PC-টা সুইচের কোন পোর্টে লাগাচ্ছো (যেমন `Fa0/5`)
2. **Assign করো** — ওই পোর্টটাকে সঠিক VLAN-এ বসাও:
   ```cisco
   interface fastEthernet 0/5
    switchport mode access
    switchport access vlan 10
   ```
   *(একটা পোর্টের জন্য `interface fastEthernet 0/5` — `range` লাগবে না; একাধিক হলে `interface range`)*
3. **যাচাই করো** — `show vlan brief` দিয়ে দেখো পোর্টটা সঠিক VLAN-এ দেখাচ্ছে কি না

**Port Assignment যাচাই:**
```cisco
show vlan brief
```
```text
10   CSE                              active    Fa0/1, Fa0/2
20   EEE                              active    Fa0/3, Fa0/4
```

---

# 💻 Part 4 — PC IP Configuration (Static)

### 🔹 VLAN 10 (CSE): `192.168.10.0/24`
| PC | IP | Mask | Gateway |
| :--- | :--- | :--- | :--- |
| PC0 | `192.168.10.1` | `255.255.255.0` | `192.168.10.254` *(রাউটার নেই তাই ঐচ্ছিক)* |
| PC1 | `192.168.10.2` | `255.255.255.0` | `192.168.10.254` |

### 🔹 VLAN 20 (EEE): `192.168.20.0/24`
| PC | IP | Mask | Gateway |
| :--- | :--- | :--- | :--- |
| PC2 | `192.168.20.1` | `255.255.255.0` | `192.168.20.254` |
| PC3 | `192.168.20.2` | `255.255.255.0` | `192.168.20.254` |

> 📌 **গুরুত্বপূর্ণ:** ভিন্ন VLAN = ভিন্ন Subnet। VLAN 10 → `10.x`, VLAN 20 → `20.x` — এই নিয়মটা মনে রাখলে পরে Inter-VLAN Routing-এ কোনো সমস্যা হবে না।

---

# 🧪 Part 5 — Ping Test ও Isolation প্রমাণ

### Test 1: একই VLAN (PC0 → PC1) ✅
```cmd
ping 192.168.10.2
```
👉 **Reply from 192.168.10.2** — সফল! কারণ দুজনই VLAN 10-এ।

### Test 2: একই VLAN (PC2 → PC3) ✅
```cmd
ping 192.168.20.2
```
👉 **Reply** — সফল! দুজনই VLAN 20-এ।

### Test 3: ভিন্ন VLAN (PC0 → PC2) ❌
```cmd
ping 192.168.20.1
```
👉 **Request timed out / Destination host unreachable** — ইচ্ছাকৃতভাবে ব্যর্থ!

> ❓ **কেন ব্যর্থ?** — VLAN 10 ও VLAN 20 আলাদা Broadcast Domain। সুইচ এক VLAN-এর ফ্রেম অন্য VLAN-এ পাঠাবে না। এই আলাদাত্বটাই **VLAN Isolation**। দুই VLAN-এর মধ্যে যোগাযোগ করতে হলে **Router** (Inter-VLAN Routing) লাগবে — যা [লেসন ০৬](06-trunk-inter-vlan.md)-এ শিখব।

---

# 🔍 Part 6 — Verification Commands

| Command | কাজ |
| :--- | :--- |
| `show vlan brief` | সব VLAN ও তাদের Port দেখা |
| `show interfaces switchport` | নির্দিষ্ট Port-এর Mode/VLAN দেখা |
| `show mac address-table` | কোন MAC কোন পোর্টে শেখা হয়েছে |
| `show running-config` | পুরো কনফিগ দেখা |

---

# 🧠 Quick Cheat-Sheet

| কাজ | কমান্ড |
| :--- | :--- |
| VLAN তৈরি | `vlan [ID]` + `name [NAME]` |
| Port-এ VLAN Assign | `switchport mode access` + `switchport access vlan [ID]` |
| একসাথে একাধিক Port | `interface range fa0/1 - 2` |
| ছাড়া (skip) দিয়ে Port একসাথে | `interface range fa0/8 - 10, fa0/12` |
| VLAN তালিকা | `show vlan brief` |
| সেভ | `copy running-config startup-config` |

---

# ❌ Troubleshooting

| সমস্যা | সমাধান |
| :--- | :--- |
| একই VLAN-এও Ping হয় না | PC-র IP একই Subnet-এ কি না, কেবল সঠিক কি না দেখো |
| Port ভুল VLAN-এ | `show vlan brief` দিয়ে Port Assignment মেলাও |
| নতুন PC-এর পোর্ট কাজ করছে না | পোর্টটা `interface range` রেঞ্জের ভেতরে আছে কি না দেখো — রেঞ্জের বাইরে থাকলে আলাদা করে Assign করো |
| `switchport` কমান্ড কাজ করছে না | সুইচ হলেই চলবে (L3 Switch/Router-এ ভিন্ন সিনট্যাক্স) |
| ভিন্ন VLAN-এ Ping হয়ে যাচ্ছে | VLAN Assign ভুল হয়েছে — পোর্টগুলো আবার চেক করো |

---

# ✅ Final Checklist

| Task | Expected Result |
| :--- | :--- |
| VLAN 10 (CSE) + VLAN 20 (EEE) তৈরি | ✅ |
| Fa0/1–2 → VLAN 10, Fa0/3–4 → VLAN 20 | ✅ |
| PC0↔PC1 Ping (সমান VLAN) | ✅ Success |
| PC2↔PC3 Ping (সমান VLAN) | ✅ Success |
| PC0→PC2 Ping (ভিন্ন VLAN) | ❌ Fail (Isolation প্রমাণিত) |
| `show vlan brief` | সঠিক Port Assignment দেখাচ্ছে ✅ |

---

# 🔮 পরের ধাপ

VLAN-এর Isolation বুঝেছ। এবার জানো **একাধিক সুইচে কীভাবে VLAN বহন করতে হয় (Trunk Link)** এবং **Router দিয়ে কীভাবে ভিন্ন VLAN-গুলোকে যোগাযোগ করাতে হয় (Inter-VLAN Routing)** → [লেসন ০৬ · Trunk ও Inter-VLAN Routing](06-trunk-inter-vlan.md)

---

> **নেভিগেশন:** [⬅ লেসন ০৪](04-dns-http-server.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৬ ➡](06-trunk-inter-vlan.md)

**এই লেসনের Tags:** `#vlan` `#vlan-isolation` `#access-port` `#interface-range` `#broadcast-domain` `#show-vlan-brief`
