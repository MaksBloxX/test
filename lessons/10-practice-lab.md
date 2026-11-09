# লেসন ১০ · Practice Lab — ৬০% Simple + ৪০% Hard (সমাধানসহ)

> 🌐 **English:** [Read this guide in English](../en/lessons/10-practice-lab.md) · [English track index](../en/README.md)

> **নেভিগেশন:** [⬅ লেসন ০৯](09-real-hardware.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ১১ ➡](11-practice-list.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 pkt ফাইল |
| :--- | :--- | :--- | :--- |
| ১০টি ল্যাব টাস্ক — ৬টি Simple + ৪টি Small Hard — **পুরো সমাধানসহ** | ~২–৩ ঘণ্টা | 🟢→🟠 | নিজে তৈরি করবে (`practice-lab.pkt`) |

**Tags:** `#practice` `#lab` `#solution` `#self-study` `#challenge`

---

### 🖼️ চিত্রে বোঝো: ১০টি ল্যাব অনুশীলনের নিয়ম

![১০টি ল্যাব অনুশীলনের নিয়ম — নিজে Topology বানাও → কনফিগার করো → Ping/Show দিয়ে যাচাই করো → শেষে লুকানো সমাধান খোলো।](../assets/diagrams/lesson-10-practice-cycle.svg)

> **ছবির সারকথা:** নিজে Topology বানাও → কনফিগার করো → Ping/Show দিয়ে যাচাই করো → শেষে লুকানো সমাধান খোলো।

![Ten independent practice tasks টপোলজি, কনফিগারেশন ও যাচাইয়ের ছয় ধাপ দেখানো ৩০ সেকেন্ডের শিক্ষামূলক GIF; Packet Tracer রেকর্ডিং নয়।](../assets/gifs/10-practice-lab.gif)

> 🎞️ **৩০ সেকেন্ডে মনে রাখো:** এটি উপরের ডায়াগ্রামের ওপর ভিত্তি করে বানানো ছয় ধাপের ভিজ্যুয়াল সারাংশ; বাস্তব Packet Tracer run, packet capture বা ফলের প্রমাণ নয়। [সব GIF-এর topic search name ও গুরুত্ব](../GIF-CATALOG.md) দেখো।


---

## 📌 এই লেসনটা কীভাবে ব্যবহার করবে (গুরুত্বপূর্ণ!)

```text
১। টাস্কের Requirement পড়ো
২। প্রথমে নিজে চেষ্টা করো (লেসন ০১–০৮ দেখতে পারো, সমাধান নয়!)
৩। কাজ শেষে "✅ যাচাই" লাইনের মতো ফল মিলিয়ে দেখো
৪। না পারলে 💡 Hint দেখো → তারপরও না পারলে 🔽 সমাধান খুলে দেখো
৫। সমাধান দেখার পর বুঝে আবার নিজে লিখে দেখো
```

> 🎯 **লক্ষ্য:** মুখস্থ নয় — **বুঝে নিজে করা**। সমাধান এখানে আছে যাতে আটকে গেলে সাহায্য পাও, কিন্তু চেষ্টা ছাড়া খোলো না!

> 🛠️ **বোনাস টিপ:** নিজের হাতে সমাধান করার পর চাইলে [`scripts/ios_config_generator.py`](../scripts/ios_config_generator.py) এবং [`scripts/subnet_calculator.py`](../scripts/subnet_calculator.py) চালিয়ে নিজের কনফিগ যাচাই করতে পারো!

---

# 🟢 SIMPLE PART (৬০% — টাস্ক ০১–০৬)

---

## টাস্ক ০১ · Basic LAN + Ping (লেসন ০১)

**🎯 কাজ:** ১ Router (1941) + ১ Switch (2960) + ২ PC — PC0→PC1 Ping সফল করো।

| Device | IP | Mask | Gateway |
| :--- | :--- | :--- | :--- |
| R1 (G0/0) | `192.168.1.1` | `255.255.255.0` | — |
| PC0 | `192.168.1.2` | `255.255.255.0` | `192.168.1.1` |
| PC1 | `192.168.1.3` | `255.255.255.0` | `192.168.1.1` |

**✅ যাচাই:** `ping 192.168.1.3` → Reply আসবে

<details>
<summary>🔽 সমাধান (চেষ্টার পরে খোলো)</summary>

**কেবল:** Router G0/0 ↔ Switch G0/1 (Straight-Through), PC0 ↔ Switch Fa0/1, PC1 ↔ Switch Fa0/2

**R1 CLI:**
```cisco
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

**PC0:** IP `192.168.1.2` / Mask `255.255.255.0` / GW `192.168.1.1`
**PC1:** IP `192.168.1.3` / Mask `255.255.255.0` / GW `192.168.1.1`

**Verify:** `show ip interface brief` → G0/0 up/up; PC0 থেকে `ping 192.168.1.3` ✅

⚠️ **কমন ভুল:** `no shutdown` দিতে ভুলে যাওয়া → লিংক লাইট লাল থাকবে।

</details>

---

## টাস্ক ০২ · Two Routers Static Routing (লেসন ০২)

**🎯 কাজ:** দুই LAN (`192.168.1.0/24`, `192.168.2.0/24`) কে Static Route দিয়ে যুক্ত করো।

```text
PC0(192.168.1.10) — SW1 — R1(10.0.0.1) ══ (10.0.0.0/30) ══ R2(10.0.0.2) — SW2 — PC1(192.168.2.10)
```

**✅ যাচাই:** PC0 থেকে `ping 192.168.2.10` → Reply (TTL=126)

<details>
<summary>🔽 সমাধান</summary>

**R1:**
```cisco
enable
configure terminal
hostname R1
interface g0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit
interface g0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
 exit
ip route 192.168.2.0 255.255.255.0 10.0.0.2
end
copy running-config startup-config
```

**R2:**
```cisco
enable
configure terminal
hostname R2
interface g0/0
 ip address 192.168.2.1 255.255.255.0
 no shutdown
 exit
interface g0/1
 ip address 10.0.0.2 255.255.255.252
 no shutdown
 exit
ip route 192.168.1.0 255.255.255.0 10.0.0.1
end
copy running-config startup-config
```

**PC0:** `192.168.1.10/24` GW `192.168.1.1` · **PC1:** `192.168.2.10/24` GW `192.168.2.1`

**Verify:** দুই রাউটারে `show ip route` → `S` রুট আছে; PC0 থেকে `ping 192.168.2.10` ✅

⚠️ **কমন ভুল:** একদিকের Route দিয়ে ফিরতি Route দেওয়া ভুলে যাওয়া — রাউটিং সবসময় **দ্বিমুখী**।

</details>

---

## টাস্ক ০৩ · DHCP Server (লেসন ০৩)

**🎯 কাজ:** Router-এ DHCP Pool `LAB` তৈরি করো — `.1`–`.10` Exclude, ক্লায়েন্ট স্বয়ংক্রিয়ভাবে IP পাবে।

**Network:** `192.168.5.0/24`, Gateway `192.168.5.1`

**✅ যাচাই:** PC `ipconfig`-এ `.11` থেকে IP; `show ip dhcp binding`-এ এন্ট্রি

<details>
<summary>🔽 সমাধান</summary>

```cisco
enable
configure terminal
hostname R1
interface g0/0
 ip address 192.168.5.1 255.255.255.0
 no shutdown
 exit

ip dhcp excluded-address 192.168.5.1 192.168.5.10

ip dhcp pool LAB
 network 192.168.5.0 255.255.255.0
 default-router 192.168.5.1
 exit

end
copy running-config startup-config
```

**PC:** IP Configuration → **DHCP** → `DHCP request successful` → IP `192.168.5.11` ✅

⚠️ **কমন ভুল:** `excluded-address`-এ `.1` বাদ রাখা ভুলে গিয়ে DHCP থেকে Gateway IP-ই ক্লায়েন্ট পেয়ে কনফ্লিক্ট হওয়া।

</details>

---

## টাস্ক ০৪ · VLAN Create + Assign (লেসন ০৫)

**🎯 কাজ:** এক Switch-এ **VLAN 10 (CSE)** ও **VLAN 20 (EEE)** — Fa0/1-2 → VLAN10, Fa0/3-4 → VLAN20। ভিন্ন VLAN-এ Ping ব্যর্থ হতে হবে।

| PC | IP |
| :--- | :--- |
| PC0, PC1 (VLAN 10) | `192.168.10.1`, `192.168.10.2` |
| PC2, PC3 (VLAN 20) | `192.168.20.1`, `192.168.20.2` |

**✅ যাচাই:** PC0→PC1 ✅ Reply · PC2→PC3 ✅ Reply · PC0→PC2 ❌ Fail

<details>
<summary>🔽 সমাধান</summary>

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

interface range fastEthernet 0/1 - 2
 switchport mode access
 switchport access vlan 10
 exit

interface range fastEthernet 0/3 - 4
 switchport mode access
 switchport access vlan 20
 exit

end
copy running-config startup-config
```

**Verify:** `show vlan brief` → Fa0/1, Fa0/2 = VLAN 10 · Fa0/3, Fa0/4 = VLAN 20 ✅

⚠️ **কমন ভুল:** `interface range fa0/1 - 2` লেখায় স্পেস ভুল হলে কমান্ড কাজ করে না।

</details>

---

## টাস্ক ০৫ · DNS + HTTP Server (লেসন ০৪)

**🎯 কাজ:** Server0-তে Static IP + DNS (`www.office.local` → `192.168.1.100`) + HTTP। PC থেকে ডোমেনে সাইট খুলতে হবে।

**✅ যাচাই:** PC-এর Browser-এ `www.office.local` লিখলে ওয়েবপেজ দেখাবে

<details>
<summary>🔽 সমাধান</summary>

**Server0 (Static):** IP `192.168.1.100` / Mask `255.255.255.0` / GW `192.168.1.1` / DNS `192.168.1.100`

**Server0 → Services → DNS:** Service **ON** → Add Record:
| Name | Type | Address |
| :--- | :--- | :--- |
| `www.office.local` | A Record | `192.168.1.100` |

**Server0 → Services → HTTP:** ON (index.html চাইলে লিখতে পারো)

**PC:** IP Configuration → **DHCP** (Router-এ DHCP Pool-এ `dns-server 192.168.1.100` আছে নিশ্চিত করো — না থাকলে Static-এ DNS `192.168.1.100` দাও)

**Test:** PC → Web Browser → `www.office.local` ✅

⚠️ **কমন ভুল:** PC-তে DNS IP দিতে ভুলে যাওয়া — IP দিয়ে সাইট খোলে, নাম দিলে খোলে না।

</details>

---

## টাস্ক ০৬ · Trunk Link — দুই সুইচ (লেসন ০৬)

**🎯 কাজ:** SW1 ↔ SW2 মাঝে Trunk (802.1Q) — একই VLAN-এর PC দুই সুইচে থাকলেও Ping হবে।

```text
SW1: Fa0/1=PC0 (VLAN10, 192.168.10.1)  Fa0/2=PC1 (VLAN20, 192.168.20.1)
SW2: Fa0/1=PC2 (VLAN10, 192.168.10.2)  Fa0/2=PC3 (VLAN20, 192.168.20.2)
SW1 G0/1 ═══ Trunk ═══ SW2 G0/1
```

**✅ যাচাই:** PC0→PC2 ✅ (VLAN 10 cross-switch) · PC0→PC1 ❌ (ভিন্ন VLAN)

<details>
<summary>🔽 সমাধান</summary>

**উভয় সুইচে (SW1 ও SW2) VLAN তৈরি:**
```cisco
enable
configure terminal
vlan 10
 name CSE
 exit
vlan 20
 name EEE
 exit
```

**Access Ports (SW1):**
```cisco
interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit
interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit
```
*(SW2-তেও একই ভাবে Fa0/1→VLAN10, Fa0/2→VLAN20)*

**Trunk (উভয় সুইচে):**
```cisco
interface gigabitEthernet 0/1
 switchport mode trunk
 exit
end
copy running-config startup-config
```

**Verify:** `show interfaces trunk` → Gig0/1 trunking, Encapsulation 802.1q ✅

⚠️ **কমন ভুল:** এক সুইচে Trunk দিলে অন্য সুইচে দিতে ভুলে যাওয়া — **দুই পাশেই** `switchport mode trunk` লাগবে।

</details>

---

# 🟠 SMALL HARD PART (৪০% — টাস্ক ০৭–১০)

---

## টাস্ক ০৭ · Inter-VLAN Routing (Router-on-a-Stick) (লেসন ০৬)

**🎯 কাজ:** এক Router + এক Switch + দুই VLAN — Subinterface দিয়ে ভিন্ন VLAN-এর PC যোগাযোগ করবে।

```text
R1 G0/0 —Trunk— SW1 Fa0/1=PC0(VLAN10) Fa0/2=PC1(VLAN20)
VLAN 10: PC0 192.168.10.10/24  GW=192.168.10.254
VLAN 20: PC1 192.168.20.10/24  GW=192.168.20.254
```

**✅ যাচাই:** PC0 থেকে `ping 192.168.20.10` → Reply (TTL=127)

<details>
<summary>🔽 সমাধান</summary>

**SW1:**
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

interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit
interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit

interface g0/1
 switchport mode trunk
 exit
end
copy running-config startup-config
```

**R1:**
```cisco
enable
configure terminal
hostname R1

interface g0/0
 no shutdown
 exit

interface g0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.254 255.255.255.0
 exit

interface g0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.254 255.255.255.0
 exit

end
copy running-config startup-config
```

**PC0:** `192.168.10.10/24` GW `192.168.10.254` · **PC1:** `192.168.20.10/24` GW `192.168.20.254`

**Verify:**
* `show ip interface brief` → G0/0.10, G0/0.20 up/up
* PC0 → `ping 192.168.20.10` → Reply TTL=127 ✅ (1 Router hop)

⚠️ **কমন ভুল:**
* `encapsulation dot1Q 10`-এর সংখ্যা ও Subinterface-এর `.10` মিলতে হবে
* ফিজিক্যাল `g0/0`-তে `no shutdown` না দিলে কোনো Subinterfaceই কাজ করবে না
* PC-দের Gateway উল্টোপাল্টা দেওয়া

</details>

---

## টাস্ক ০৮ · Port Security + Violation Test (লেসন ০৭)

**🎯 কাজ:** একটি Access Port-এ Port Security চালু করো — শুধু **১টি** MAC অনুমোদিত (sticky)। ভিন্ন PC লাগালে পোর্ট err-disabled হবে, তারপর Recovery করবে।

**✅ যাচাই:** `show port-security address`-এ ১টি Sticky MAC · ভিন্ন PC লাগালে পোর্ট down (err-disabled)

<details>
<summary>🔽 সমাধান</summary>

**SW1 Fa0/1-এ:**
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
end
copy running-config startup-config
```

**Learn Test:** PC0 লাগাও → `show port-security address` → Sticky MAC এন্ট্রি ✅

**Violation Test:** PC0 খুলে অন্য PC লাগাও → `show interfaces fa0/1` → `err-disabled` দেখাবে

**Recovery:**
```cisco
enable
configure terminal
interface fastEthernet 0/1
 shutdown
 no shutdown
 exit
end
```

⚠️ **কমন ভুল:**
* `switchport mode access` আগে না দিয়ে port-security দিলে কমান্ড reject হবে
* Sticky MAC আগে থেকে শেখা থাকলে নতুন PC err-disable হবে — আগে `show port-security address` দেখে clear করো (`clear port-security address`)

</details>

---

## টাস্ক ০৯ · EtherChannel (LACP) + STP Root (লেসন ০৭)

**🎯 কাজ:** SW1 ↔ SW2 মাঝে **২টি লিংক** জুড়ে একটি EtherChannel (LACP) বানাও + SW1-কে Root Bridge করো।

**✅ যাচাই:** `show etherchannel summary` → `Po1(SU) LACP` + `show spanning-tree` → SW1 = root

<details>
<summary>🔽 সমাধান</summary>

**SW1:**
```cisco
enable
configure terminal
hostname SW1

interface range gigabitEthernet 0/1 - 2
 channel-group 1 mode active
 exit

interface port-channel 1
 switchport mode trunk
 exit

spanning-tree vlan 1 root primary

end
copy running-config startup-config
```

**SW2:** (একই কমান্ড — `hostname SW2` সহ)
```cisco
enable
configure terminal
hostname SW2

interface range gigabitEthernet 0/1 - 2
 channel-group 1 mode active
 exit

interface port-channel 1
 switchport mode trunk
 exit

end
copy running-config startup-config
```

**Verify:**
```cisco
show etherchannel summary
! Group 1  Po1(SU)  LACP  Gig0/1(P) Gig0/2(P)

show spanning-tree
! SW1-এ: This bridge is the root
```

⚠️ **কমন ভুল:**
* দুই পাশে mode ভিন্ন হলে (active/active বা active/passive) চলবে, কিন্তু দুই পাশেই `passive` হলে চ্যানেল তৈরি হবে না
* দুটি লিংকের গতি/ডুপ্লেক্স ভিন্ন হলে EtherChannel হবে না

</details>

---

## টাস্ক ১০ · Mini Final — সব একসাথে (লেসন ০৮-এর চেয়ে একটু বেশি)

**🎯 কাজ:** ২ VLAN + Router-on-a-Stick + **প্রতি VLAN-এ আলাদা DHCP Pool** + DNS + HTTP:

```text
VLAN 10 (192.168.10.0/24): PC0 (DHCP), Server0 192.168.10.100 (Static)
VLAN 20 (192.168.20.0/24): PC1 (DHCP)
R1 Subinterfaces: G0/0.10 = 192.168.10.1, G0/0.20 = 192.168.20.1
DNS: www.office.local → 192.168.10.100
DHCP: প্রতি VLAN-এ আলাদা Pool (VLAN10, VLAN20), .1–.10 Exclude
```

**✅ যাচাই (সব একসাথে):**
1. PC0 ও PC1 — দুটোই DHCP থেকে সঠিক VLAN-এর IP পাচ্ছে
2. PC0 → PC1 Inter-VLAN Ping → Reply (TTL=127)
3. PC1 (VLAN 20) থেকে `www.office.local` খুলছে → **Cross-VLAN Web Access** ✅

<details>
<summary>🔽 সম্পূর্ণ সমাধান</summary>

**SW1:**
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

interface fa0/1
 switchport mode access
 switchport access vlan 10
 exit

interface fa0/2
 switchport mode access
 switchport access vlan 20
 exit

interface fa0/3
 switchport mode access
 switchport access vlan 10
 exit

interface g0/1
 switchport mode trunk
 exit

end
copy running-config startup-config
```
*(Fa0/1 = PC0, Fa0/2 = PC1, Fa0/3 = Server0)*

**R1:**
```cisco
enable
configure terminal
hostname R1

interface g0/0
 no shutdown
 exit

interface g0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 exit

interface g0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 exit

! Exclusions (দুই VLAN-ই সুরক্ষিত)
ip dhcp excluded-address 192.168.10.1 192.168.10.100
ip dhcp excluded-address 192.168.20.1 192.168.20.10

ip dhcp pool VLAN10
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 192.168.10.100
 exit

ip dhcp pool VLAN20
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 192.168.10.100
 exit

end
copy running-config startup-config
```

**Server0 (Static):**
```text
IP: 192.168.10.100   Mask: 255.255.255.0
Gateway: 192.168.10.1   DNS: 192.168.10.100
```
**Server0 → Services → DNS (ON):** `www.office.local` (A Record) → `192.168.10.100`
**Server0 → Services → HTTP (ON)**

**PC0:** DHCP → `192.168.10.101` (approx, কারণ `.1`–`.100` Exclude) · **PC1:** DHCP → `192.168.20.11` (approx)

**Final Verify:**
```text
PC0 → ping 192.168.20.11        → Reply (TTL=127) ✅
PC0 → ping 192.168.10.100       → Reply ✅
PC1 → Browser → www.office.local → ওয়েবপেজ ✅ (VLAN 20 থেকে VLAN 10-এর সার্ভার!)
```

⚠️ **কমন ভুল:**
* দুই VLAN-এর DHCP Pool-এ `default-router` উল্টোপাল্টা দেওয়া (VLAN20 Pool-এ VLAN10-এর Gateway)
* Server0-কে DHCP-তে রেখে দেওয়া — সার্ভারের IP সবসময় **Static**
* `dns-server` লাইন ভুলে যাওয়া → নামে সাইট খোলবে না

</details>

---

# 📊 Score Card

| টাস্ক | লেভেল | কোন লেসন | নিজে পেরেছ? |
| :--- | :--- | :--- | :---: |
| ০১ Basic LAN + Ping | 🟢 | ০১ | ☐ |
| ০২ Static Routing | 🟢 | ০২ | ☐ |
| ০৩ DHCP Server | 🟢 | ০৩ | ☐ |
| ০৪ VLAN + Isolation | 🟢 | ০৫ | ☐ |
| ০৫ DNS + HTTP | 🟢 | ০৪ | ☐ |
| ০৬ Trunk Link | 🟢 | ০৬ | ☐ |
| ০৭ Inter-VLAN Routing | 🟠 | ০৬ | ☐ |
| ০৮ Port Security | 🟠 | ০৭ | ☐ |
| ০৯ EtherChannel + STP | 🟠 | ০৭ | ☐ |
| ১০ Mini Final | 🟠 | ০৪+০৬+০৮ | ☐ |

> 🏆 **৮/১০+ পারলে** তুমি Lab পরীক্ষার জন্য প্রস্তুত! এবার [লেসন ১১ · Practice List](11-practice-list.md) — যেখানে **কোনো সমাধান নেই**, সম্পূর্ণ নিজে।

---

> **নেভিগেশন:** [⬅ লেসন ০৯](09-real-hardware.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ১১ ➡](11-practice-list.md)

**এই লেসনের Tags:** `#practice-lab` `#solutions` `#simple` `#hard` `#self-check`
