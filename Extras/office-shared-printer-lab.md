# 🖨️ Extra Lab ০৩ · Office Shared Printer Network

> **নেভিগেশন:** [⬅ Email Server Lab](email-server-lab.md) · [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [পরের ল্যাব: IP Subnet Tester ➡](ip-subnet-tester-lab.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| একটি অফিস LAN-এ DHCP ইউজারদের সাথে Static IP যুক্ত Shared Network Printer কনফিগার করা | ~৩০ মিনিট | 🟢 Beginner | [`office-shared-printer-network.pkt`](../pkt-files/practice/office-shared-printer-network.pkt) |

**Tags:** `#shared-printer` `#office-lan` `#dhcp-exclusion` `#static-ip` `#printer-pt` `#beginner-lab`

---

## 🎯 এই ল্যাবে যা শিখবে

1. বাস্তব অফিসে একটি **Network Printer (`Printer-PT`)** কেন সব পিসির সাথে সুইচের মাধ্যমে শেয়ার করা হয়
2. ক্লায়েন্ট পিসিগুলো **DHCP** ব্যবহার করলেও প্রিন্টারে কেন **Static IP** দেওয়া বাধ্যতামূলক
3. `ip dhcp excluded-address` দিয়ে প্রিন্টারের IP কনফ্লিক্ট থেকে রক্ষা করা
4. সব অফিস পিসি থেকে প্রিন্টারের সাথে সংযোগ (`ping` ও ARP Table) যাচাই করা

### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ | বাস্তব নিয়ম |
| :--- | :--- | :--- |
| **Network Printer** | যে প্রিন্টারের নিজস্ব NIC (RJ-45 / Wi-Fi) ও IP থাকে — কোনো নির্দিষ্ট পিসি চালু না থাকলেও সবাই প্রিন্ট দিতে পারে | অফিসে স্ট্যান্ডার্ড |
| **Static IP Reservation** | সার্ভার বা প্রিন্টারের জন্য নির্দিষ্ট অপরিবর্তনীয় IP রাখা যেন ইউজারদের প্রিন্টার সংযোগ ভেঙে না যায় | যেমন `.1.10` |
| **IP Conflict** | দুটি ডিভাইসে একই IP পড়ে গেলে নেটওয়ার্ক অকেজো হয়ে যাওয়া | `excluded-address` দিয়ে রোধ করা হয় |

---

## ১. Network Topology ও IP Plan

### Topology Diagram

```text
                       [ Router R1 ]
                     G0/0: 192.168.1.1
                       (DHCP Server)
                             │
                     [ Switch 2960 ]
              ┌──────────┬───┴───────┬────────────┐
            Fa0/1      Fa0/2       Fa0/3        Fa0/10
              │          │           │            │
           [ PC0 ]    [ PC1 ]     [ PC2 ]   [ Printer0 ]
            DHCP       DHCP        DHCP      192.168.1.10
           (.1.11)    (.1.12)     (.1.13)     (Static IP)
```

### 📋 IP Addressing Table (`192.168.1.0/24`)

| Device | Interface | IP Mode | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Router (R1)** | `G0/0` | Static | `192.168.1.1` | `255.255.255.0` | — |
| **Office Printer** | `FastEthernet0` | **Static** | **`192.168.1.10`** | `255.255.255.0` | `192.168.1.1` |
| **PC0 (HR)** | `FastEthernet0` | DHCP | `192.168.1.11` | `255.255.255.0` | `192.168.1.1` |
| **PC1 (Accounts)** | `FastEthernet0` | DHCP | `192.168.1.12` | `255.255.255.0` | `192.168.1.1` |
| **PC2 (Manager)** | `FastEthernet0` | DHCP | `192.168.1.13` | `255.255.255.0` | `192.168.1.1` |

> 💡 **কেন প্রিন্টারে DHCP নয়?** — প্রিন্টার DHCP-তে থাকলে রিস্টার্টের পর তার IP `.11` থেকে বদলে `.25` হয়ে যেতে পারে! তখন অফিসের সব পিসিতে প্রিন্টার "Offline" দেখাবে। তাই সার্ভার ও প্রিন্টার সবসময় **Static IP**-তে থাকে।

---

## ২. ধাপে ধাপে কনফিগারেশন

### Step 1: ডিভাইস ও কেবল সংযোগ
1. **End Devices → Printer-PT** থেকে একটি প্রিন্টার নাও।
2. সব ডিভাইস (`R1`, `PC0–PC2`, `Printer0`) সুইচের সাথে **Copper Straight-Through** কেবল দিয়ে যুক্ত করো।

### Step 2: Router R1 কনফিগারেশন (Gateway + DHCP)
```cisco
enable
configure terminal
hostname R1

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

! Gateway (.1) থেকে Printer (.10) পর্যন্ত IP সুরক্ষিত রাখো
ip dhcp excluded-address 192.168.1.1 192.168.1.10

ip dhcp pool OFFICE_LAN
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 exit

end
copy running-config startup-config
```

### Step 3: Network Printer (`Printer-PT`) কনফিগারেশন
Packet Tracer-এ প্রিন্টারের ভেতরে `Desktop` ট্যাব থাকে না — `Config` ট্যাব থেকে IP বসাতে হয়:

1. **`Printer0`**-তে ক্লিক করো → **`Config`** ট্যাবে যাও।
2. বাম পাশের **GLOBAL → Settings**-এ ক্লিক করো:
   * **Display Name:** `Office-LaserJet`
   * **Gateway/DNS IPv4:** `Static` সিলেক্ট করে **Default Gateway:** `192.168.1.1` দাও।
3. বাম পাশের **INTERFACE → FastEthernet0**-এ ক্লিক করো:
   * **Port Status:** ✅ `On` নিশ্চিত করো
   * **IP Configuration:** `Static`
   * **IPv4 Address:** `192.168.1.10`
   * **Subnet Mask:** `255.255.255.0`

### Step 4: অফিস PC-গুলোতে DHCP চালু করো
`PC0`, `PC1`, `PC2` প্রতিটিতে গিয়ে **Desktop → IP Configuration → DHCP** অন করো। দেখবে `.11`, `.12`, `.13` থেকে IP পেয়েছে (`.10` প্রিন্টারের জন্য নিরাপদ রয়েছে!)।

---

## ৩. 🔍 Verification ও Simulation Test

### ১. সব PC থেকে প্রিন্টারে Ping
যেকোনো PC-র **Command Prompt** খুলে:
```cmd
C:\> ping 192.168.1.10
C:\> arp -a
```
* `Reply from 192.168.1.10: bytes=32 time<1ms TTL=128` আসবে।
* `arp -a` দিলে প্রিন্টারের IP (`192.168.1.10`)-এর পাশে তার ফিজিক্যাল MAC Address দেখতে পাবে!

### ২. Packet Tracer PDU (Add Simple PDU) টেস্ট
উপরের টুলবার থেকে **✉️ Add Simple PDU (`P`)** আইকনটি নিয়ে প্রথমে `PC0`-এ ক্লিক করো, তারপর `Printer0`-তে ক্লিক করো → ডান নিচে **`Successful`** দেখাবে! একইভাবে `PC1 → Printer0` এবং `PC2 → Printer0` পরীক্ষা করো।

---

## ৪. ❌ Troubleshooting

| সমস্যা | সম্ভাব্য কারণ | সমাধান |
| :--- | :--- | :--- |
| `Printer0 has no functional ports` | প্রিন্টারের পোর্ট বন্ধ বা কেবল ভুল | `Printer0 → Config → FastEthernet0` → **Port Status: `On`** টিক দাও |
| Duplicate IP ওয়ার্নিং দেখাচ্ছে | `excluded-address` দেওয়া হয়নি | রাউটারে `ip dhcp excluded-address 192.168.1.1 192.168.1.10` দিয়ে PC-গুলোতে আবার Static → DHCP টগল করো |
| অন্য VLAN থেকে প্রিন্টারে Ping যায় না | প্রিন্টারে Default Gateway বসানো হয়নি | `Printer0 → Config → Settings`-এ গিয়ে Default Gateway `192.168.1.1` বসাও |

---

## ৫. 🎓 Viva Questions

<details>
<summary><b>Q1. USB Shared Printer বনাম Network Printer-এর পার্থক্য কী?</b></summary>

USB Shared Printer একটি নির্দিষ্ট পিসির সাথে লাগানো থাকে — ওই পিসি বন্ধ থাকলে অফিসের কেউ প্রিন্ট করতে পারে না। কিন্তু **Network Printer** সরাসরি Switch-এ RJ-45 কেবল দিয়ে যুক্ত থাকে এবং নিজস্ব IP ব্যবহার করে — তাই যেকোনো সময় যেকোনো অনুমোদিত পিসি বা অন্য VLAN থেকেও সরাসরি প্রিন্ট করা যায়।
</details>

<details>
<summary><b>Q2. প্রিন্টার একই LAN-এ থাকলে Default Gateway কেন দিতে হয়?</b></summary>

একই LAN (`192.168.1.0/24`) থেকে প্রিন্ট করতে Gateway না দিলেও চলে; কিন্তু ভবিষ্যতে যদি অন্য কোনো ডিপার্টমেন্ট/VLAN (যেমন `192.168.20.0/24`) থেকে এই শেয়ার্ড প্রিন্টারে প্রিন্ট পাঠাতে হয়, তখন প্রিন্টারের রিপ্লাই ফেরত পাঠাতে **Default Gateway** অপরিহার্য!
</details>

---

## ✅ Final Checklist

| কাজ | যাচাই | অবস্থা |
| :--- | :--- | :---: |
| Router-এ `.1`–`.10` Excluded | `show running-config` | ☐ |
| Printer0-এ Static IP `192.168.1.10` ও Gateway `192.168.1.1` | `Config` ট্যাবে যাচাই | ☐ |
| PC0, PC1, PC2-এ স্বয়ংক্রিয় DHCP IP (`.11+`) | `ipconfig` | ☐ |
| সব PC থেকে `ping 192.168.1.10` | ১০০% Reply (`TTL=128`) | ☐ |

---

> **নেভিগেশন:** [⬅ Email Server Lab](email-server-lab.md) · [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [পরের ল্যাব: IP Subnet Tester ➡](ip-subnet-tester-lab.md)

**Tags:** `#office-network` `#shared-printer` `#dhcp` `#static-ip` `#packet-tracer`
