# লেসন ০৭ · Switching Technologies: STP, Port Security ও EtherChannel

> **নেভিগেশন:** [⬅ লেসন ০৬](06-trunk-inter-vlan.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৮ ➡](08-final-project.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| সুইচের ৩টি গুরুত্বপূর্ণ প্রযুক্তি: STP · Port Security · EtherChannel | ~৬০ মিনিট | 🟠 Intermediate–Advanced | [lesson-07-switching.pkt](../pkt-files/labs/lesson-07-switching.pkt) |

**Tags:** `#stp` `#port-security` `#etherchannel` `#lacp` `#root-bridge` `#loop-prevention`

---

## 🎯 এই লেসনে যা শিখবে

| Lab | প্রযুক্তি | সমস্যার সমাধান |
| :---: | :--- | :--- |
| 1 | **STP** (Spanning Tree Protocol) | নেটওয়ার্ক লুপ ঠেকায় 🔄❌ |
| 2 | **Port Security** | অনুমতি ছাড়া ডিভাইস প্রবেশ ঠেকায় 🔒 |
| 3 | **EtherChannel** (LACP) | একাধিক লিংক জুড়ে গতি ও নির্ভরযোগ্যতা বাড়ায় ⚡ |


### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ |
| :--- | :--- |
| **Broadcast Storm** | সুইচে লুপ থাকলে ব্রডকাস্ট ফ্রেম অনন্তকাল ঘুরে পুরো নেটওয়ার্ক অচল করে দেওয়া |
| **STP & Root Bridge** | লুপ ঠেকানোর প্রোটোকল; সবচেয়ে কম Bridge ID ওয়ালা সুইচকে বলা হয় **Root Bridge** |
| **Sticky MAC & `err-disabled`** | প্রথম সংযুক্ত পিসির MAC চিনে রাখা; অন্য পিসি লাগালে পোর্ট লক (`err-disabled`) হয়ে যাওয়া |
| **EtherChannel (`LACP`)** | ২–৮টি ফিজিক্যাল কেবলকে বেঁধে একটি দ্রুত ও নিরাপদ লজিক্যাল লিংক (`Port-channel`) বানানো |

> 🔗 **ট্রাবলশুটিং কেস:** [🛠️ Problem ০৫ (`err-disabled` পোর্ট সচল করা)](12-problem-solve.md#problem-05)

---

# 🟢 Lab 1 — STP: Spanning Tree Protocol

## 1. STP কী? ও Network Loop কী?

**STP** = *Spanning Tree Protocol* (IEEE 802.1D / 802.1w) — সুইচ নেটওয়ার্কে **লুপ (Loop)** তৈরি হওয়া ঠেকায়।

### ❓ Network Loop কী?
দুটি সুইচের মাঝে **দুই বা ততোধিক পাথ** থাকলে একটি ব্রডকাস্ট ফ্রেম চিরকাল ঘুরতে থাকে:

```text
     SW1 ═══════════ SW2        ← দুটি লিংক = লুপ!
      ║               ║
      ╚═══════════════╝
```
**ফল:** Broadcast Storm 💥 → সুইচ হ্যাং → সম্পূর্ণ নেটওয়ার্ক ডাউন।

### 🛡️ STP কীভাবে লুপ ঠেকায়?
STP সব পাথ বিশ্লেষণ করে **সবচেয়ে ভালো পাথটি চালু (Forwarding)** রাখে এবং বাকিগুলোকে **বন্ধ (Blocking)** করে দেয়। দরকার পড়লে (লিংক ভাঙলে) ব্লক করা পাথ আবার চালু হয়।

## 2. গুরুত্বপূর্ণ পরিভাষা

| টার্ম | অর্থ |
| :--- | :--- |
| **Root Bridge** | সমগ্র STP ট্রি-র "মূল" — সবচেয়ে কম Bridge ID (BID)-এর সুইচ |
| **Bridge ID (BID)** | Priority + MAC Address — যার কম, সে Root |
| **Root Port** | প্রতিটি Non-Root সুইচে Root Bridge-এর দিকে সবচেয়ে ভালো পোর্ট |
| **Designated Port** | প্রতিটি সেগমেন্টে ট্রাফিক ফরোয়ার্ড করা পোর্ট |
| **Blocking Port** | লুপ এড়াতে বন্ধ রাখা পোর্ট (অতিরিক্ত পাথ) |

> 👑 **Root Bridge নির্বাচন:** সবচেয়ে কম **Priority** (ডিফল্ট 32768) — টাই হলে সবচেয়ে কম MAC Address।

## 3. STP Practical Lab

### 📐 Topology (তিনটি সুইচে লুপ তৈরি করো):
```text
        SW1 ──────── SW2
         \           /
          \         /
           \       /
            SW3
```
কেবল: সব সুইচ↔সুইচ = **Copper Cross-Over** (বা Automatic)

### Step 1: STP স্ট্যাটাস দেখো
```cisco
show spanning-tree
```
দেখবে একটি পোর্ট `Altn BLK` (Blocking) — সেটাই লুপ ভেঙেছে।

### Step 2: SW1-কে Root Bridge বানাও
```cisco
! SW1-এ
enable
configure terminal
spanning-tree vlan 1 root primary
end
```
*(চাইলে নির্দিষ্ট Priority দিতে পারো: `spanning-tree vlan 1 priority 4096`)*

### Step 3: ভেরিফিকেশন
```cisco
show spanning-tree
```
```text
SW1 → This bridge is the root   ✅
SW2, SW3 → Root ID হিসেবে SW1-এর BID দেখাবে
```

### 📋 STP Commands
| Command | কাজ |
| :--- | :--- |
| `show spanning-tree` | STP স্ট্যাটাস, Root Bridge, Port State |
| `spanning-tree vlan 1 root primary` | নিজেকে Root বানাও |
| `spanning-tree vlan 1 priority [VAL]` | Priority সেট (4096-এর গুণিতক) |
| `show spanning-tree interface fa0/1` | নির্দিষ্ট পোর্টের স্টেট |

---

# 🔐 Lab 2 — Port Security

## 1. Port Security কী?

সুইচের পোর্টে **শুধুমাত্র অনুমোদিত MAC Address**-এর ডিভাইস যুক্ত হতে পারবে — এই নিয়মটাই Port Security। অন্য কেউ তার দিয়ে যুক্ত হলে পোর্ট **err-disabled** হয়ে যায় (বা লগ হয়)।

## 2. Configuration

### 📌 Topology: SW1 Fa0/1 — PC0 (বাকি পোর্টে অন্য PC পরীক্ষার জন্য)

```cisco
enable
configure terminal

interface fastEthernet 0/1
 switchport mode access
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 switchport port-security violation shutdown
 exit
```

### 💡 প্রতিটি কমান্ডের কাজ

| Command | কাজ |
| :--- | :--- |
| `switchport mode access` | Access পোর্ট (Port Security-এর জন্য বাধ্যতামূলক) |
| `switchport port-security` | Port Security **চালু** |
| `maximum 1` | সর্বোচ্চ ১টি MAC অনুমোদিত |
| `mac-address sticky` | প্রথম যে MAC আসবে তাকে নিজে থেকেই মনে রাখবে |
| `violation shutdown` | নিয়ম ভাঙলে পোর্ট বন্ধ (err-disable) |

## 3. Violation Mode (৩ প্রকার)

| Mode | আচরণ | ব্যবহার |
| :--- | :--- | :--- |
| **protect** | অনুমতি ছাড়া ফ্রেম নিঃশব্দে ফেলে দেয় | নীরব সুরক্ষা |
| **restrict** | ফেলে দেয় + SNMP/লগে সতর্কতা | সতর্কতাসহ সুরক্ষা |
| **shutdown** | পোর্ট err-disable (সবচেয়ে কঠোর) ⚠️ | সর্বোচ্চ নিরাপত্তা |

## 4. Learn, Test ও Recovery

### Step 1: PC0-এর MAC শেখাও
PC0 সংযুক্ত করো → `sticky` নিজেই শিখে নেবে। যাচাই:
```cisco
show port-security interface fastEthernet 0/1
show port-security address
```

### Step 2: অন্য PC দিয়ে Violation Test
PC0 খুলে ভিন্ন MAC-এর PC লাগাও → পোর্ট **err-disabled** হবে:
```cisco
show interfaces fastEthernet 0/1
! দেখবে: FastEthernet0/1 is down, line protocol is down (err-disabled)
```

### Step 3: পোর্ট পুনরায় চালু (Recovery)
```cisco
enable
configure terminal
interface fastEthernet 0/1
 shutdown
 no shutdown
 exit
end
```
*(পুরো সুইচ Recovery: `errdisable recovery cause psecure-violation` + `errdisable recovery interval 30`)*

---

# ⚡ Lab 3 — EtherChannel (LACP)

## 1. EtherChannel কী?

একাধিক ফিজিক্যাল লিংককে **একটি লজিক্যাল লিংকে** পরিণত করা — যেন গতি যোগ হয় এবং একটি লিংক ভাঙলেও বাকিগুলো চলতে থাকে।

### 🔹 EtherChannel ছাড়া:
```text
SW1 ═══════ SW2   (একটি লিংক: 1 Gbps, ভাঙলে ডাউন)
```
### 🔹 EtherChannel সহ:
```text
SW1 ═══╗ ╔══ SW2
SW1 ═══╣ ╠══ SW2   (3 লিংক = একটি লজিক্যাল লিংক: মিলিত ব্যান্ডউইথ + Redundancy)
SW1 ═══╝ ╚══ SW2
```

## 2. Protocols

| Protocol | Mode | বৈশিষ্ট্য |
| :--- | :--- | :--- |
| **PAgP** | `auto` / `desirable` | Cisco proprietary |
| **LACP** | `active` / `passive` | IEEE 802.3ad (সবচেয়ে বেশি ব্যবহৃত) ✅ |

## 3. EtherChannel Practical Lab (LACP)

### 📐 Topology: SW1 ↔ SW2 মাঝে **২টি** (বা ৩টি) Parallel Link

### Step 1: SW1 Configuration
```cisco
enable
configure terminal

interface range gigabitEthernet 0/1 - 2
 channel-group 1 mode active
 exit

interface port-channel 1
 switchport mode trunk
 exit

end
copy running-config startup-config
```

### Step 2: SW2 Configuration
```cisco
enable
configure terminal

interface range gigabitEthernet 0/1 - 2
 channel-group 1 mode active
 exit

interface port-channel 1
 switchport mode trunk
 exit

end
copy running-config startup-config
```

> 💡 দুই পাশেই `active` (LACP) — এক পাশ `active` অন্য পাশ `passive` হলেও চলে; কিন্তু দুই পাশেই `passive` হলে চ্যানেল তৈরি হবে না।

### Step 3: Verification
```cisco
show etherchannel summary
```
**Expected Output:**
```text
Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)         LACP      Gig0/1(P)   Gig0/2(P)
```

| ফ্ল্যাগ | অর্থ |
| :--- | :--- |
| **S** | Layer 2 |
| **U** | In use (ব্যবহৃত হচ্ছে) ✅ |
| **P** | Bundled in port-channel |
| **D** | Down / **I** | Stand-alone |

**অন্যান্য কমান্ড:**
```cisco
show etherchannel port-channel
show interfaces port-channel 1
```

---

# 📊 তিনটি ফিচারের তুলনামূলক পর্যালোচনা

| ফিচার | কী সমস্যা সমাধান করে | কোথায় ব্যবহার |
| :--- | :--- | :--- |
| **STP** | লুপ ও Broadcast Storm | যেকোনো সুইচ নেটওয়ার্কে |
| **Port Security** | অননুমোদিত প্রবেশ | Access Port (PC/Printer) |
| **EtherChannel** | ব্যান্ডউইথ ও Redundancy | সুইচ↔সুইচ / সুইচ↔Router আপলিংক |

---

# 🧪 Practical Action Plan (পুরো ল্যাব এক নজরে)

1. **STP:** ৩ সুইচে লুপ তৈরি করো → `show spanning-tree` → SW1 root primary → Blocking পোর্ট পরিবর্তন লক্ষ করো
2. **Port Security:** Fa0/1-এ sticky + maximum 1 → ভিন্ন PC লাগাও → err-disable → recovery করো
3. **EtherChannel:** ২টি লিংকে channel-group 1 mode active → `show etherchannel summary`-এ `SU` দেখো

---

# ❌ Troubleshooting

| সমস্যা | সমাধান |
| :--- | :--- |
| STP-তে Root বদলায়নি | Priority ঠিক আছে কি না (`show spanning-tree`), VLAN 1 ব্যবহার হচ্ছে কি না |
| Port Security কাজ করছে না | `switchport mode access` আগে দিতে হবে; পোর্টে আগে থেকে MAC শেখা আছে কি না |
| err-disabled পোর্ট আর চলছে না | `shutdown` → `no shutdown` দিয়ে Recovery |
| EtherChannel তৈরি হয়নি | দুই পাশের mode মিলছে কি না (active/active বা active/passive), সমান গতি/ডুপ্লেক্স |
| Po1 দেখাচ্ছে `D` | ফিজিক্যাল পোর্টগুলো আলাদা সুইচে লাগানো আছে কি না দেখো |

---

# ✅ Final Checklist

| Lab | Verification | Expected |
| :--- | :--- | :--- |
| STP | `show spanning-tree` | SW1 = root, একটি পোর্ট Blocking ✅ |
| Port Security | `show port-security address` | Sticky MAC এন্ট্রি ✅ |
| Violation | ভিন্ন PC লাগানো | err-disabled ✅ |
| EtherChannel | `show etherchannel summary` | Po1(SU), LACP, 2 ports ✅ |

---

# 🔮 পরের ধাপ

তুমি এখন পর্যন্ত CLI, Routing, DHCP, DNS, VLAN, Trunk, Inter-VLAN, STP, Security ও EtherChannel — সব শিখেছ! এবার **ফাইনাল প্রজেক্টে** এই সব একসাথে জুড়ে একটি সম্পূর্ণ অফিস নেটওয়ার্ক তৈরি করো → [লেসন ০৮ · Final Project](08-final-project.md)

---

> **নেভিগেশন:** [⬅ লেসন ০৬](06-trunk-inter-vlan.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৮ ➡](08-final-project.md)

**এই লেসনের Tags:** `#stp` `#root-bridge` `#port-security` `#sticky-mac` `#err-disable` `#etherchannel` `#lacp`
