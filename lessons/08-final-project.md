# লেসন ০৮ · Final Project — সম্পূর্ণ অফিস নেটওয়ার্ক

> **নেভিগেশন:** [⬅ লেসন ০৭](07-switching.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৯ ➡](09-real-hardware.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| VLAN + Inter-VLAN Routing + DHCP + DNS + HTTP — সব একসাথে | ~৯০ মিনিট | 🔴 Advanced (Capstone) | [lesson-08-final-project.pkt](../pkt-files/labs/lesson-08-final-project.pkt) |

**Tags:** `#final-project` `#capstone` `#vlan` `#inter-vlan` `#dhcp` `#dns` `#http` `#router-on-a-stick`

---

## 🎯 এই প্রজেক্টে যা করবে

এটি একটি **Capstone Project** — লেসন ০১–০৭-এর সব দক্ষতা এক টপোলজিতে ব্যবহার করবে:

1. ✅ Switch-এ **VLAN 10 ও VLAN 20** তৈরি + Access Port Assign (লেসন ০৫)
2. ✅ Router-on-a-Stick **Inter-VLAN Routing** (লেসন ০৬)
3. ✅ Router-এ **DHCP Pool** (প্রতি VLAN-এ আলাদা) (লেসন ০৩)
4. ✅ Server0-তে **DNS** (`www.office.local`) (লেসন ০৪)
5. ✅ Server0-তে **HTTP Website** হোস্ট (লেসন ০৪)
6. ✅ ভিন্ন VLAN-এর PC থেকে **একই ওয়েবসাইট** খোলা


### 🏷️ প্রজেক্টে ব্যবহৃত প্রযুক্তির সমন্বয়

| লেয়ার / সার্ভিস | এই প্রজেক্টে ভূমিকা | পূর্বপাঠ |
| :--- | :--- | :--- |
| **Layer 2 (VLAN + Trunk)** | CSE (`VLAN 10`) ও EEE (`VLAN 20`) আলাদা করা এবং `802.1Q` ট্রাঙ্কে রাউটারে পাঠানো | [লেসন ০৫](05-vlan.md), [০৬](06-trunk-inter-vlan.md) |
| **Layer 3 (ROAS Routing)** | `G0/0.10` ও `G0/0.20` সাবইন্টারফেস দিয়ে দুই বিভাগের মধ্যে যোগাযোগ ঘটানো | [লেসন ০৬](06-trunk-inter-vlan.md) |
| **Layer 7 (DHCP + DNS + HTTP)** | স্বয়ংক্রিয় IP বিতরণ এবং `www.office.local` ডোমেইনে অভ্যন্তরীণ ওয়েবসাইট হোস্ট করা | [লেসন ০৩](03-dhcp.md), [০৪](04-dns-http-server.md) |

> 🔗 **এরপর আরও বড় প্রজেক্ট চাইলে:** [🏆 CCNA লেসন ০৯ · University Network Mega Capstone](../ccna-fundamentals/09-capstone-university-lab.md)

---

# 🧩 ১. Network Topology তৈরি করো

### 📌 প্রয়োজনীয় Device
* **১টি Router:** Cisco 1941
* **১টি Switch:** Cisco Catalyst 2960
* **২টি PC:** PC-PT (PC0, PC1)
* **১টি Server:** Server-PT (Server0)

### 📌 Topology Diagram
```text
                  Router R1
                   G0/0
                     │
                     │ Trunk (802.1Q)
                     │
                  SW1 G0/1
               ______│______
              │      │      │
           Fa0/1   Fa0/2   Fa0/3
              │      │      │
             PC0    PC1   Server0
          VLAN 10 VLAN 20 VLAN 10
       192.168.10.x 192.168.20.x 192.168.10.100
```

### 🔌 Cable Connection (Copper Straight-Through)

| Device 1 | Port | Device 2 | Port |
| :--- | :--- | :--- | :--- |
| **R1** | G0/0 | **SW1** | G0/1 |
| **PC0** | Fa0 | **SW1** | Fa0/1 |
| **PC1** | Fa0 | **SW1** | Fa0/2 |
| **Server0** | Fa0 | **SW1** | Fa0/3 |

---

# 📋 ২. IP Address Plan

| Device | VLAN | IP Address | Subnet Mask | Default Gateway | DNS Server |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **PC0** | 10 | DHCP থেকে পাবে | `255.255.255.0` | `192.168.10.1` | `192.168.10.100` |
| **PC1** | 20 | DHCP থেকে পাবে | `255.255.255.0` | `192.168.20.1` | `192.168.10.100` |
| **Server0** | 10 | `192.168.10.100` (Static) | `255.255.255.0` | `192.168.10.1` | `192.168.10.100` |
| **R1** (G0/0.10) | 10 | `192.168.10.1` | `255.255.255.0` | N/A | N/A |
| **R1** (G0/0.20) | 20 | `192.168.20.1` | `255.255.255.0` | N/A | N/A |

* **Website Domain:** `www.office.local` → `192.168.10.100`

---

# ⚙️ ৩. Switch Configuration (SW1)

```cisco
enable
configure terminal
hostname SW1

! VLAN তৈরি
vlan 10
 name CSE
 exit
vlan 20
 name EEE
 exit

! PC0 → VLAN 10
interface fastEthernet 0/1
 switchport mode access
 switchport access vlan 10
 exit

! PC1 → VLAN 20
interface fastEthernet 0/2
 switchport mode access
 switchport access vlan 20
 exit

! Server0 → VLAN 10
interface fastEthernet 0/3
 switchport mode access
 switchport access vlan 10
 exit

! Router-এর সাথে Trunk
interface gigabitEthernet 0/1
 switchport mode trunk
 exit

end
copy running-config startup-config
```

### 🔍 Switch Verification
```cisco
show vlan brief          ← Fa0/1, Fa0/3 = VLAN10; Fa0/2 = VLAN20
show interfaces trunk    ← G0/1 trunking ✅
```

---

# 🛣️ ৪. Router-on-a-Stick Configuration (R1)

```cisco
enable
configure terminal
hostname R1

! ফিজিক্যাল Interface চালু
interface gigabitEthernet 0/0
 no shutdown
 exit

! VLAN 10 Subinterface (PC0 + Server0-এর Gateway)
interface gigabitEthernet 0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 exit

! VLAN 20 Subinterface (PC1-এর Gateway)
interface gigabitEthernet 0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 exit

end
```

---

# 🎫 ৫. Router-এ DHCP Configure করো

```cisco
configure terminal

! দুই VLAN-এর Static/Server IP সুরক্ষা
ip dhcp excluded-address 192.168.10.1 192.168.10.100
ip dhcp excluded-address 192.168.20.1 192.168.20.10

! VLAN 10-এর Pool
ip dhcp pool VLAN10
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 192.168.10.100
 exit

! VLAN 20-এর Pool
ip dhcp pool VLAN20
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 192.168.10.100
 exit

end
copy running-config startup-config
```

> 💡 **এখানে কী হলো?** — প্রতিটি VLAN-এর নিজস্ব Subnet, Gateway ও Pool। দুই Client-ই DNS হিসেবে `192.168.10.100` পাবে — কারণ ওয়েবসাইটটি VLAN 10-এর সার্ভারে আছে, কিন্তু VLAN 20-এর ইউজারও সেটি ব্যবহার করবে (Inter-VLAN Routing-এর কারণে)।

### 🔍 DHCP Verification
```cisco
show ip dhcp binding
show ip dhcp pool
```

---

# 🖥️ ৬–৮. Server0 Configuration (Static IP + DNS + HTTP)

## Static IP
**Server0 → Desktop → IP Configuration → Static:**
```text
IP Address:      192.168.10.100
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.10.1
DNS Server:      192.168.10.100
```

## DNS Service
**Services → DNS → ON**, তারপর A Record:
| Name | Type | Address |
| :--- | :--- | :--- |
| `www.office.local` | A Record | `192.168.10.100` |
→ **Add** ✅

## HTTP Service
**Services → HTTP/WEB → ON** (HTTPS-ও ON রাখতে পারো)। `index.html`-এ চাইলে:
```html
<html><body><h1>Office Network — Final Project</h1></body></html>
```

---

# 💻 ৯. PC0 ও PC1-তে DHCP চালু করো

প্রতিটি PC: **Desktop → IP Configuration → DHCP**

```text
PC0: 192.168.10.101 (approx)  GW 192.168.10.1  DNS 192.168.10.100
PC1: 192.168.20.11 (approx)  GW 192.168.20.1  DNS 192.168.10.100
```

---

# 🧪 ১০. Connectivity ও Ping Test

| # | Test | Command | Expected |
| :-: | :--- | :--- | :--- |
| 1 | PC0 → Gateway | `ping 192.168.10.1` | Reply ✅ |
| 2 | PC1 → Gateway | `ping 192.168.20.1` | Reply ✅ |
| 3 | **PC0 → PC1 (Inter-VLAN)** | `ping 192.168.20.11` | Reply (TTL=127) ✅ |
| 4 | PC0 → Server0 | `ping 192.168.10.100` | Reply ✅ |
| 5 | PC1 → Server0 (Cross-VLAN) | `ping 192.168.10.100` | Reply (TTL=127) ✅ |

---

# 🌐 ১১. Domain দিয়ে Website খোলো

**PC0 → Desktop → Web Browser:**
```text
www.office.local
```
✅ "Office Network — Final Project" দেখা গেলে **DNS + HTTP + VLAN 10** সফল!

**PC1 → Desktop → Web Browser:**
```text
www.office.local
```
✅ **Cross-VLAN Web Access** — VLAN 20-এর ইউজার VLAN 10-এর সার্ভারে পৌঁছাচ্ছে → **Inter-VLAN Routing + DNS + HTTP** তিনটোই সফল! 🎉

---

# 🔍 ১২. সম্পূর্ণ ভেরিফিকেশন

### Router R1-এ:
```cisco
show ip interface brief      ← G0/0.10 ও G0/0.20 up/up
show ip route                ← C 192.168.10.0/24, C 192.168.20.0/24
show ip dhcp binding         ← দুই Client-এর লিজ
show running-config
```

### Switch SW1-এ:
```cisco
show vlan brief              ← সঠিক Port/VLAN
show interfaces trunk        ← G0/1 trunking
show mac address-table
```

---

# ❌ ১৩. Final Troubleshooting Checklist

1. **PC IP পাচ্ছে না?** → Router-এ Pool + excluded-address, SW1 Trunk, `no shutdown`
2. **Inter-VLAN Ping হয় না?** → `encapsulation dot1Q` VLAN ID মিলছে কি না, PC-দের Gateway ঠিক কি না
3. **নামে সাইট খোলে না?** → PC-তে DNS IP `192.168.10.100`, DNS Service ON, A Record সঠিক
4. **IP দিয়ে সাইট খোলে নামাতে?** → HTTP Service ON, Server0-এর IP Static
5. **সবকিছু ঠিক কিন্তু কাজ করছে না?** → `copy running-config startup-config` করেছ তো? (রিস্টার্টে মুছে যাবে!)
6. **দ্বিতীয় Website (যেমন `www.coffee.xyz`) যোগ করেছ, কিন্তু খোলে না?** → নতুন ডোমেনের **A Record** DNS-এ আছে কি না, ওই IP-তে HTTP ON কি না দেখো → [লেসন ০৪ · একাধিক সার্ভার/ওয়েবসাইট](04-dns-http-server.md)

---

# 💾 ১৪. Final Configuration Save

**উভয় ডিভাইসে (R1 ও SW1):**
```cisco
copy running-config startup-config
```

---

# 🎓 তুমি এখন যা পারো

```text
CLI Modes ─► Static Routing ─► DHCP ─► DNS/Web ─► VLAN ─► Trunk ─► Inter-VLAN ─► STP/Security/EtherChannel ─► সম্পূর্ণ নেটওয়ার্ক ✅
```

### 🏆 এরপর কী শেখা উচিত?
- **Dynamic Routing:** RIP, OSPF, EIGRP
- **ACL (Access Control List)** — ট্রাফিক ফিল্টারিং
- **NAT / PAT** — ইন্টারনেট শেয়ারিং
- **VLAN Routing (L3 Switch)**, **HSRP/VRRP** — Redundancy
- CCNA/CCNP সিলেবাস ধরে এগিয়ে যাও

📖 সব কমান্ড এক জায়গায় দেখতে: [CLI Command Cheat-Sheet](../reference/cli-command-cheatsheet.md)

**পরের ধাপ:** বাস্তব সরঞ্জাম চেনো → [লেসন ০৯ · Real Hardware](09-real-hardware.md) → তারপর [Practice Lab](10-practice-lab.md) ও [Practice List](11-practice-list.md)

---

> **নেভিগেশন:** [⬅ লেসন ০৭](07-switching.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৯ ➡](09-real-hardware.md)

**এই লেসনের Tags:** `#final-project` `#capstone` `#all-in-one` `#office-network`
