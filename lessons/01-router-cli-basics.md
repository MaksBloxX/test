# লেসন ০১ · Router CLI Basics ও প্রথম নেটওয়ার্ক ল্যাব

> **নেভিগেশন:** [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · **লেসন ০১** · [পরের লেসন ০২ ➡](02-static-routing.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| Router CLI প্রম্পট, Mode, Basic Commands + প্রথম Ping Lab | ~৪৫ মিনিট | 🟢 Beginner | [lesson-01-router-cli-basics.pkt](../pkt-files/labs/lesson-01-router-cli-basics.pkt) |

**Tags:** `#cli` `#router` `#basic-config` `#ip-addressing` `#ping` `#first-lab`

---

## 🎯 এই লেসনে যা শিখবে

1. Cisco Router-এর **CLI Mode** গুলো (User → Privileged → Global → Interface)
2. সবচেয়ে দরকারি **Basic Commands** এবং তাদের **Shortcut (Abbreviation নিয়ম)**
3. **Complete Router Configuration Formula** (মনে রাখার সিরিয়াল ফর্মুলা)
4. ১ Router + ১ Switch + ২ PC দিয়ে **প্রথম হাতে-কলমে ল্যাব**
5. `ping` দিয়ে **Connectivity Test** ও সমস্যা সমাধান


### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ |
| :--- | :--- |
| **CLI** (*Command Line Interface*) | মাউসের বদলে কমান্ড লিখে Router/Switch কনফিগার করার স্ক্রিন |
| **Default Gateway** | লোকাল LAN থেকে বাইরের নেটওয়ার্কে যাওয়ার দরজা (রাউটারের ইন্টারফেস IP) |
| **NVRAM** | রাউটারের স্থায়ী মেমোরি — `copy run start` দিলে কনফিগ এখানে সেভ থাকে |
| **ICMP (`ping`)** | দুই ডিভাইসের মধ্যে সংযোগ সচল আছে কি না পরীক্ষা করার বার্তা |

> 🔗 **তত্ত্ব ঝালিয়ে নিতে:** [CCNA ০১ · Network Basics](../ccna-fundamentals/01-network-basics.md) · [CCNA ০৪ · IPv4 Addressing](../ccna-fundamentals/04-ipv4-addressing.md)

---

# 🧩 Part A — Router CLI Basic Commands

Router-এ ক্লিক করো → **CLI** tab → **Enter** চাপো।

## ১. CLI Mode গুলো বোঝা (খুব গুরুত্বপূর্ণ)

```text
Router>                ← User EXEC Mode (সীমিত কমান্ড)
Router#                ← Privileged EXEC Mode (show, ping, save)
Router(config)#        ← Global Configuration Mode (নাম, pool, route)
Router(config-if)#     ← Interface Configuration Mode (IP, no shutdown)
```

> **মনে রাখবে:**
> - `>` = User EXEC Mode — এখানে শুধু দেখা/পরীক্ষার কমান্ড
> - `#` = Privileged EXEC Mode — `show`, `ping`, `copy` সব এখানে চলে
> - **R1(config)#** = Global Config Mode, **R1(config-if)#** = Interface Config Mode — IP সেট করতে Interface Mode-এ যেতে হবে

### Mode পরিবর্তনের ধাপসমূহ

**Step 1: User Mode → Privileged Mode**
```text
Router> enable
Router#
```

**Step 2: Privileged → Global Configuration Mode**
```text
Router# configure terminal
Router(config)#
```
**Shortcut:** `conf t`

**Step 3: Router-এর নাম পরিবর্তন**
```text
Router(config)# hostname R1
R1(config)#
```

**Step 4: Interface Configuration Mode**
```text
R1(config)# interface gigabitEthernet 0/0
R1(config-if)#
```
**Shortcut:** `int g0/0`

**Step 5: IP Address সেট করা**
```text
R1(config-if)# ip address 192.168.1.1 255.255.255.0
```
**Formula:** `ip address [IP_ADDRESS] [SUBNET_MASK]`

**Step 6: Interface চালু করা**
```text
R1(config-if)# no shutdown
```
> ⚠️ Router-এর interface সাধারণত *administratively down* থাকে — তাই `no shutdown` না দিলে লিংটি কখনোই সবুজ হবে না।

**Step 7: Configuration Mode থেকে বের হওয়া**
```text
R1(config-if)# exit        ← এক ধাপ পিছনে
R1(config-if)# end         ← সরাসরি Privileged EXEC Mode-এ (দ্রুত পথ)
```

---

## ২. Complete Router Configuration Formula

ধরো, G0/0 Interface-এ `192.168.1.1` দিতে হবে। পুরো কমান্ড একবারে:

```text
Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)# interface g0/0
R1(config-if)# ip address 192.168.1.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# end
R1# copy running-config startup-config
```

| Command | কাজ |
| :--- | :--- |
| `enable` | Privileged Mode-এ প্রবেশ |
| `configure terminal` | Configuration Mode-এ প্রবেশ |
| `hostname R1` | Router-এর নাম পরিবর্তন |
| `interface g0/0` | Interface নির্বাচন |
| `ip address ...` | IP Address সেট করা |
| `no shutdown` | Interface চালু করা |
| `end` | Configuration Mode থেকে সরাসরি বের হওয়া |
| `copy running-config startup-config` | Configuration **স্থায়ীভাবে Save** করা (NVRAM-এ) |

> 💡 `copy running-config startup-config` না দিলে Router Restart দিলেই পুরো কনফিগ মুছে যাবে! *(Destination filename কনফার্ম করতে বললে সরাসরি **Enter** চাপবে)*

---

## ৩. মনে রাখার সিরিয়াল Formula 🧠

```text
ENABLE → CONF T → HOSTNAME → INTERFACE → IP ADDRESS → NO SHUTDOWN → END → SAVE
```

### Prompt Flow (এক নজরে):
```text
Router>  ──enable──►  Router#
Router#  ──conf t──►  Router(config)#
Router(config)#  ──int g0/0──►  Router(config-if)#
Router(config-if)#  ──ip address + no shutdown──►  (interface live ✅)
Router(config-if)#  ──end──►  Router#
Router#  ──copy run start──►  (save ✅)
```

### ⚡ এই শর্টকাটগুলো কেন চলল? (Abbreviation Rule)

উপরে `conf t`, `int g0/0`, `copy run start` — পুরো কমান্ড না লিখেও কাজ হলো। কারণ **IOS-এ যেকোনো কমান্ডের unique prefix টাইপ করলেই চলে** — এতটুকু লিখলে যেন অন্য কোনো কমান্ড না মেলে।

| পুরো কমান্ড | শর্টকাট | প্রমাণ |
| :--- | :--- | :--- |
| `configure terminal` | `conf t` | ✅ সবার চেনা |
| `interface g0/0` | `int g0/0` | ✅ উপরেই ব্যবহার হয়েছে |
| `show interfaces` | `show int` | ✅ **টেস্ট করা — কাজ করে** |
| `interface fastEthernet 0/0` | `interface fas 0/0` | ✅ **টেস্ট করা — কাজ করে** |
| `copy running-config startup-config` | `copy run start` | ✅ উপরেই ব্যবহার হয়েছে |

⚠️ **সাবধান:** prefix যেন **দ্ব্যর্থক** (ambiguous) না হয় — যেমন `show in` চলবে না (`interface`, `inventory` — দুটোই `in` দিয়ে শুরু), কিন্তু `show int` চলে ✅। একইভাবে `fas` দিয়ে শুরু হয় শুধু `fastEthernet`।

> 🧠 সব শর্টকাট এক নজরে → [Cheat-Sheet · ⚡ Shortcut](../reference/cli-command-cheatsheet.md)

---

# 🧪 Part B — প্রথম হাতে-কলমে ল্যাব: PC0 → PC1 Ping

**আমাদের লক্ষ্য:** `PC0` থেকে `PC1`-এ Ping করে Connection Test করা।

## 🧩 Step 1: Network Topology তৈরি করো

১টি Router, ১টি Switch এবং ২টি PC ব্যবহার করব।

```text
             Router0 (R1)
           G0/0 |
                |
             Switch0
              /    \
             /      \
           PC0      PC1
```

### 🖥️ কোন Device নেবে?

Packet Tracer-এর নিচের Device Panel থেকে:

| Device | কোথা থেকে নেবে | Quantity | প্রস্তাবিত মডেল |
| :--- | :--- | :--- | :--- |
| **Router** | Network Devices → Routers | 1 | Cisco 1941 |
| **Switch** | Network Devices → Switches | 1 | Cisco 2960 |
| **PC** | End Devices → PC | 2 | PC-PT |

## 🔌 Step 2: Cable Connection করো

| From | Port | To | Port |
| :--- | :--- | :--- | :--- |
| **Router0** | GigabitEthernet 0/0 | **Switch0** | GigabitEthernet 0/1 |
| **PC0** | FastEthernet0 | **Switch0** | FastEthernet 0/1 |
| **PC1** | FastEthernet0 | **Switch0** | FastEthernet 0/2 |

> **কেবল নিয়ম:** PC ↔ Switch = **Copper Straight-Through**; Router ↔ Switch = **Copper Straight-Through**
> *(সব Connection দেওয়ার পরে কিছুক্ষণ অপেক্ষা করো — Switch-এর Amber বাতি ধীরে ধীরে সবুজ হয়ে যাবে)*

## 🧮 Step 3: IP Address Plan

`192.168.1.0/24` Network ব্যবহার করব:

| Device | Interface | IP Address | Subnet Mask |
| :--- | :--- | :--- | :--- |
| **Router0 (R1)** | G0/0 | `192.168.1.1` | `255.255.255.0` |
| **PC0** | FastEthernet0 | `192.168.1.2` | `255.255.255.0` |
| **PC1** | FastEthernet0 | `192.168.1.3` | `255.255.255.0` |

* **PC-গুলোর Default Gateway:** `192.168.1.1` (Router-এর G0/0)
* **কেন?** Router-এর এই Interface-টি সম্পূর্ণ Subnet-এর জন্য Gateway হিসেবে কাজ করে।

## ⚙️ Step 4: Router Configuration

Router0-তে ক্লিক করো → **CLI** tab। প্রথমবার এই প্রম্পট আসবে:

```text
Would you like to enter the initial configuration dialog? [yes/no]: no
```
`no` লিখে **Enter** চাপো। তারপর:

```text
enable
configure terminal
hostname R1

interface gigabitEthernet 0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
exit

end
copy running-config startup-config
```

### Router Configuration Check
```text
show ip interface brief
```
**Expected Output:**
```text
Interface              IP-Address      Status      Protocol
GigabitEthernet0/0     192.168.1.1     up          up
```
> `up / up` মানে Interface শারীরিকভাবে ও যৌক্তিকভাবে — দুটো দিক থেকেই সক্রিয়। ✅

## 💻 Step 5–6: PC0 ও PC1 Configuration

প্রতিটি PC-তে: **Desktop → IP Configuration → Static**

| Field | PC0 | PC1 |
| :--- | :--- | :--- |
| **IP Address** | `192.168.1.2` | `192.168.1.3` |
| **Subnet Mask** | `255.255.255.0` | `255.255.255.0` |
| **Default Gateway** | `192.168.1.1` | `192.168.1.1` |

## 🧪 Step 7: Ping Test করো

**Test 1 — PC0 → Router:** (PC0-এর Command Prompt)
```cmd
ping 192.168.1.1
```

**Test 2 — PC0 → PC1:**
```cmd
ping 192.168.1.3
```
**সফল রেসপন্স:**
```cmd
Reply from 192.168.1.3: bytes=32 time<1ms TTL=128
```
> **টিপ:** প্রথম প্যাকেটে ARP Resolution-এর কারণে `Request timed out` আসতে পারে — দ্বিতীয়বার Ping করলে ১০০% Success পাবে।

**Test 3 — PC1 → PC0:**
```cmd
ping 192.168.1.2
```

---

# 🔁 Part C — লজিক: এখানে Router-এর কাজ কী?

```text
                   R1 (192.168.1.1)
                        |
                     Switch0
                     /      \
                  PC0        PC1
               .1.2          .1.3
```

* PC0 ও PC1 **একই Subnet** (`192.168.1.0/24`)-এ — তাই প্যাকেট **সরাসরি Switch** হয়ে চলে যায়:
  `PC0 ──► Switch0 ──► PC1` *(Layer 2 ফ্রেম ফরওয়ার্ডিং)*
* Switch কাজ করে **MAC Address Table** দিয়ে (Layer 2) — TTL কমে না, তাই Ping-এ `TTL=128` দেখায়।
* **তাহলে Router কেন?** — লোকাল Subnet-এর **বাইরে** (ইন্টারনেট বা অন্য Remote Subnet) যেতে Default Gateway লাগে। লেসন ০২-এ দুইটি Router জুড়ে সেই কাজটাই করব।

---

# ❌ Troubleshooting: Ping সমস্যা সমাধান

| সমস্যা | সমাধান |
| :--- | :--- |
| **Request timed out** | IP, Subnet Mask ও কেবল কানেকশন নিশ্চিত করো; আবার Ping দাও |
| **Destination host unreachable** | Gateway IP ও Subnet Mask ঠিক আছে কি না যাচাই করো |
| **Interface administratively down** | Interface Mode-ে `no shutdown` চালাও |
| **PC0 → Router Ping হয় না** | PC0-এর Gateway (`192.168.1.1`) ও Router G0/0 IP মিলছে কি না দেখো |
| **লিংক লাইট লাল** | সঠিক কেবল (Straight-Through) ও সঠিক পোর্ট সিলেক্ট হয়েছে কি না দেখো |

---

# ✅ Practical Challenge

1. Router0-এর G0/0-এ `192.168.1.1/24` কনফিগার করে `no shutdown` দাও।
2. PC0 (`192.168.1.2`) ও PC1 (`192.168.1.3`)-এ IP + Gateway বসাও।
3. PC0 থেকে `ping 192.168.1.3` চালিয়ে Connectivity টেস্ট করো।
4. Router-এ `show ip interface brief` চালিয়ে `up/up` নিশ্চিত করো।
5. কনফিগ `copy running-config startup-config` দিয়ে সেভ করো।

---

# 🔮 পরের ধাপ

একটি Router দিয়ে একই LAN-এর কাজ শিখলে। এবার শিখব **দুটি Router, দুটি আলাদা Network** কীভাবে Static Routing দিয়ে যুক্ত করতে হয় → [লেসন ০২ · Static Routing](02-static-routing.md)

---

> **নেভিগেশন:** [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · **লেসন ০১** · [পরের লেসন ০২ ➡](02-static-routing.md)

**এই লেসনের Tags:** `#cli` `#mode` `#hostname` `#ip-address` `#no-shutdown` `#ping` `#troubleshooting`
