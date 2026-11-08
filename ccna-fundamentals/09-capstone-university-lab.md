# লেসন ৯ · Capstone — University Network Mega Lab

> **নেভিগেশন:** [⬅ লেসন ৮](08-troubleshooting.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [🅰️ হাতে-কলমে কোর্স](../lessons/01-router-cli-basics.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| সব লেসন একসাথে — সম্পূর্ণ ক্যাম্পাস নেটওয়ার্ক ডিজাইন, কনফিগ ও টেস্ট | ~২–৩ ঘণ্টা | 🔴 Advanced | নিজে তৈরি (from scratch) |

**Tags:** `#capstone` `#vlan` `#trunk` `#roas` `#dhcp-relay` `#dns` `#static-route` `#nat` `#acl` `#project`

---

> 🏆 এটা শেখার লেসন না — **পরীক্ষার** লেসন। আগের ৮টা লেসনের সবটুকু এখানে একসাথে লাগবে। কনফিগ দেখে মুখস্থ কোরো না; আগে নিজে করার চেষ্টা করো, আটকালে দেখো।


## ১. Project Scenario

ধরি, তোমার University-তে তিনটি Department আছে:
- **CSE Department** — VLAN 10
- **EEE Department** — VLAN 20
- **Administration** — VLAN 30

এছাড়া রয়েছে একটি **Server Room** (VLAN 40), যেখানে DHCP, DNS ও Web Server থাকবে।

সব Department যেন নিজেদের Network থেকে Server Access করতে পারে, কিন্তু ACL-এর মাধ্যমে কিছু Traffic নিয়ন্ত্রণ করা হবে।

### Network Topology (Logical Overview)

```text
                  INTERNET / ISP
                        |
                     [ISP/R2]
                        | (WAN: 203.0.113.0/30)
                       R1 (Main Campus Router)
                        | (Trunk: Router-on-a-Stick)
                       SW1 (Core Switch)
                  /     |     \          \
                 /      |      \          \
           VLAN 10   VLAN 20   VLAN 30    VLAN 40
             CSE       EEE      ADMIN     SERVERS
              |         |         |          |
            PC0/1     PC2/3     PC4/5     Server0/1
```

---

## ২. Required Devices

Packet Tracer থেকে নিচের Device-গুলো নাও:

| Device | Model / Type | Quantity | Purpose |
| :--- | :--- | :--- | :--- |
| **Router** | Cisco 2911 | 2 | Campus Routing (R1) ও ISP Simulation (R2) |
| **Switch** | Cisco 2960 | 1 | VLAN ও LAN Connectivity (SW1) |
| **PC** | Generic Desktop | 6 | Department Clients (প্রতি VLAN-এ ২টি করে) |
| **Server** | Generic Server | 2 | DHCP, DNS ও Web Services |
| **Cable** | Copper Straight-Through / Serial | প্রয়োজনমতো | Device Connection |

- **Router R1:** Main Campus Router
- **Router R2:** ISP Router (Static Routing ও NAT Practice করার জন্য)

---

## ৩. IP Addressing Plan

### VLAN & Subnet Plan

| VLAN | Department | Network | Gateway | Usable Host Range |
| :--- | :--- | :--- | :--- | :--- |
| **VLAN 10** | CSE | 192.168.10.0/24 | 192.168.10.1 | 192.168.10.2 - 192.168.10.254 |
| **VLAN 20** | EEE | 192.168.20.0/24 | 192.168.20.1 | 192.168.20.2 - 192.168.20.254 |
| **VLAN 30** | Administration | 192.168.30.0/24 | 192.168.30.1 | 192.168.30.2 - 192.168.30.254 |
| **VLAN 40** | Servers | 192.168.40.0/24 | 192.168.40.1 | 192.168.40.2 - 192.168.40.254 |

### WAN Link

| Device | Interface | IP Address | Subnet Mask |
| :--- | :--- | :--- | :--- |
| **R1** | G0/0 | 203.0.113.2 | 255.255.255.252 (/30) |
| **R2 (ISP)** | G0/0 | 203.0.113.1 | 255.255.255.252 (/30) |

### Server Addressing Plan

| Server | IP Address | Subnet Mask | Default Gateway | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Server0** | 192.168.40.10 | 255.255.255.0 | 192.168.40.1 | DHCP + DNS Server |
| **Server1** | 192.168.40.20 | 255.255.255.0 | 192.168.40.1 | Web (HTTP) Server |

> **Note:** `203.0.113.0/24` হলো RFC 5737 অনুযায়ী Documentation-এর জন্য Reserved Block। এখানে ISP Link Simulation-এ ব্যবহার করা হচ্ছে।

---

## ৪. Step 1 — Switch (SW1) VLAN Configuration

SW1-এ CLI Open করো:

```ios
enable
configure terminal
hostname SW1

! Create VLANs
vlan 10
 name CSE
exit

vlan 20
 name EEE
exit

vlan 30
 name ADMIN
exit

vlan 40
 name SERVERS
exit
end
```

### VLAN Verification

```ios
show vlan brief
```

### Access Port Assignment

- **Fa0/1 – Fa0/2:** CSE (VLAN 10)
- **Fa0/3 – Fa0/4:** EEE (VLAN 20)
- **Fa0/5 – Fa0/6:** Administration (VLAN 30)
- **Fa0/7:** Server VLAN (VLAN 40)

```ios
configure terminal

interface range fastEthernet 0/1-2
 switchport mode access
 switchport access vlan 10
exit

interface range fastEthernet 0/3-4
 switchport mode access
 switchport access vlan 20
exit

interface range fastEthernet 0/5-6
 switchport mode access
 switchport access vlan 30
exit

interface fastEthernet 0/7
 switchport mode access
 switchport access vlan 40
exit

end
```

---

## ৫. Step 2 — Trunk Configuration

SW1 থেকে Router R1-এর সংযোগ Port-কে Trunk Mode-এ নিয়ে যেতে হবে:
- **Port:** SW1 `Fa0/24` → R1 `G0/1`

```ios
configure terminal

interface fastEthernet 0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40
exit

end
```

### Trunk Verification

```ios
show interfaces trunk
```

---

## ৬. Step 3 — Inter-VLAN Routing (Router-on-a-Stick)

Campus Router **R1**-এ সাব-ইন্টারফেস কনফিগার করো:

```ios
enable
configure terminal
hostname R1

! Turn on physical interface
interface gigabitEthernet 0/1
 no shutdown
exit

! Subinterface for VLAN 10
interface gigabitEthernet 0/1.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
exit

! Subinterface for VLAN 20
interface gigabitEthernet 0/1.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
exit

! Subinterface for VLAN 30
interface gigabitEthernet 0/1.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
exit

! Subinterface for VLAN 40
interface gigabitEthernet 0/1.40
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
exit

end
```

### Interface Status Check

```ios
show ip interface brief
```

---

## ৭. Step 4 — DHCP Server & Relay Agent Configuration

### 7.1 Server0-তে Static IP বসাও:
- **Desktop → IP Configuration:**
  - IP Address: `192.168.40.10`
  - Subnet Mask: `255.255.255.0`
  - Default Gateway: `192.168.40.1`
  - DNS Server: `192.168.40.10`

### 7.2 Services → DHCP-এ যাও এবং Service `ON` করো:

- **Pool: CSE**
  - Pool Name: `CSE`
  - Default Gateway: `192.168.10.1`
  - DNS Server: `192.168.40.10`
  - Start IP Address: `192.168.10.100`
  - Subnet Mask: `255.255.255.0`
  - Maximum Users: `100`
  - *(Click **Add**)*

- **Pool: EEE**
  - Pool Name: `EEE`
  - Default Gateway: `192.168.20.1`
  - DNS Server: `192.168.40.10`
  - Start IP Address: `192.168.20.100`
  - Subnet Mask: `255.255.255.0`
  - Maximum Users: `100`
  - *(Click **Add**)*

- **Pool: ADMIN**
  - Pool Name: `ADMIN`
  - Default Gateway: `192.168.30.1`
  - DNS Server: `192.168.40.10`
  - Start IP Address: `192.168.30.100`
  - Subnet Mask: `255.255.255.0`
  - Maximum Users: `100`
  - *(Click **Add**)*

### 7.3 DHCP Relay Configuration (R1-এ)

DHCP Broadcast মেসেজ বিভিন্ন সাবনেট পেরিয়ে Server0 (`192.168.40.10`) পর্যন্ত পৌঁছাতে `ip helper-address` ব্যবহার করা হয়:

```ios
configure terminal

interface gigabitEthernet 0/1.10
 ip helper-address 192.168.40.10
exit

interface gigabitEthernet 0/1.20
 ip helper-address 192.168.40.10
exit

interface gigabitEthernet 0/1.30
 ip helper-address 192.168.40.10
exit

end
```

---

## ৮. Step 5 — DNS ও Web Server Configuration

### 8.1 DNS Server Configuration (Server0)
1. **Services → DNS**-এ যাও।
2. DNS Service **ON** করো।
3. Resource Record যোগ করো:
   - **Name:** `www.university.local`
   - **Type:** `A Record`
   - **Address:** `192.168.40.20`
   - *(Click **Add**)*

### 8.2 Web Server Configuration (Server1)
1. **Desktop → IP Configuration:**
   - IP Address: `192.168.40.20`
   - Subnet Mask: `255.255.255.0`
   - Default Gateway: `192.168.40.1`
   - DNS Server: `192.168.40.10`
2. **Services → HTTP**-এ যাও।
3. HTTP ও HTTPS Service **ON** করো (প্রয়োজনে `index.html` এডিট করে কাস্টম মেসেজ দিতে পারো)।

### Test Web Access:
- যে কোনো Department-এর PC-তে DHCP মোড সিলেক্ট করো যাতে IP পায়।
- PC-এর **Desktop → Web Browser** ওপেন করো।
- URL বক্সে টাইপ করো: `http://www.university.local`

---

## ৯. Step 6 — Static Routing ও ISP Connection

### 9.1 R1 WAN Interface & Default Route

```ios
configure terminal

interface gigabitEthernet 0/0
 ip address 203.0.113.2 255.255.255.252
 no shutdown
exit

! Default Route toward ISP
ip route 0.0.0.0 0.0.0.0 203.0.113.1
end
```

### 9.2 R2 (ISP Router) Configuration

```ios
enable
configure terminal
hostname ISP

interface gigabitEthernet 0/0
 ip address 203.0.113.1 255.255.255.252
 no shutdown
exit

! Return Routes back to Campus Subnets
ip route 192.168.10.0 255.255.255.0 203.0.113.2
ip route 192.168.20.0 255.255.255.0 203.0.113.2
ip route 192.168.30.0 255.255.255.0 203.0.113.2
ip route 192.168.40.0 255.255.255.0 203.0.113.2
end
```

---

## ১০. Step 7 — NAT Overload (PAT)

Private আইপিগুলোকে পাবলিক আইপিতে রূপান্তর করতে R1-এ NAT Overload কনফিগার করো:

```ios
configure terminal

! Define Internal Subnets via Standard ACL
access-list 1 permit 192.168.10.0 0.0.0.255
access-list 1 permit 192.168.20.0 0.0.0.255
access-list 1 permit 192.168.30.0 0.0.0.255
access-list 1 permit 192.168.40.0 0.0.0.255

! Define Inside Interfaces
interface gigabitEthernet 0/1.10
 ip nat inside
exit

interface gigabitEthernet 0/1.20
 ip nat inside
exit

interface gigabitEthernet 0/1.30
 ip nat inside
exit

interface gigabitEthernet 0/1.40
 ip nat inside
exit

! Define Outside Interface
interface gigabitEthernet 0/0
 ip nat outside
exit

! Configure NAT Overload
ip nat inside source list 1 interface gigabitEthernet 0/0 overload
end
```

### NAT Verification

```ios
show ip nat translations
show ip nat statistics
```

---

## ১১. Step 8 — ACL Security (Traffic Filtering)

**Policy:** CSE Department (`192.168.10.0/24`) Administration Department (`192.168.30.0/24`)-এ প্রবেশ করতে পারবে না, কিন্তু ইন্টারনেটে ও সার্ভার রুমে যেতে পারবে।

### R1-এ Extended ACL Configuration

```ios
configure terminal

ip access-list extended CSE-BLOCK-ADMIN
 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
 permit ip any any
exit

! Apply ACL on CSE Subinterface (Inbound)
interface gigabitEthernet 0/1.10
 ip access-group CSE-BLOCK-ADMIN in
exit

end
```

### ACL Verification

```ios
show access-lists
show ip interface gigabitEthernet 0/1.10
```

---

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** একই switch-এ চারটা VLAN — CSE, EEE, Admin, Server। এদের মধ্যে যোগাযোগ করাতে কী লাগবে?

- **A.** আরও switch
- **B.** Inter-VLAN Routing (Router-on-a-Stick বা L3 switch)
- **C.** শুধু trunk
- **D.** কিছুই না, নিজে থেকেই হবে

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Inter-VLAN Routing (ROAS বা L3 switch)**

**🧠 কেন:**

প্রতিটা VLAN আলাদা subnet, তাই আলাদা নেটওয়ার্ক। gateway দরকার — একটাই router-এর একাধিক subinterface (ROAS), প্রতিটা VLAN-এর জন্য `.1` ঠিকানা।

</details>

---

**প্রশ্ন ২.** DHCP server Server VLAN-এ, ক্লায়েন্ট campus VLAN-এ — router কীভাবে DHCP-কে কাজ করতে দেয়?

- **A.** `ip helper-address` দিয়ে DHCP relay
- **B.** switch-এ DNS চালু করে
- **C.** সব VLAN-এ আলাদা DHCP server বসিয়ে
- **D.** NAT দিয়ে

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. ip helper-address (DHCP relay)**

**🧠 কেন:**

DHCP Discover হলো broadcast, আর broadcast router পার হয় না। VLAN-এর gateway interface-এ `ip helper-address 192.168.40.10` দিলে router ওই broadcast-কে unicast করে DHCP server-এ পৌঁছে দেয়।

</details>

---

**প্রশ্ন ৩.** Extended ACL কোথায় বসাবে — Server-এর কাছে নাকি ক্লায়েন্টের কাছে?

- **A.** Server-এর ইন্টারফেসে
- **B.** ক্লায়েন্ট যে ইন্টারফেস থেকে আসছে, তার যত কাছে
- **C.** যেকোনো এক জায়গায়
- **D.** switch-এর trunk-এ

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. source-এর যত কাছে**

**🧠 কেন:**

Extended ACL নির্দিষ্ট (source+dest+port) মেলায়, তাই যত আগে ব্লক হয় তত ভালো — নেটওয়ার্কে অপ্রয়োজনীয় ট্রাফিক ঘোরে না।

</details>

---

**প্রশ্ন ৪.** NAT-এ `overload` না দিলে কী হতো?

- **A.** কিছুই বদলাত না
- **B.** প্রত্যেক private host-এর জন্য একটা আলাদা public IP লাগত
- **C.** ইন্টারনেট স্পিড বাড়ত
- **D.** ACL কাজ করত না

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. প্রত্যেক host-এর জন্য আলাদা public IP**

**🧠 কেন:**

`overload` = PAT, অর্থাৎ port number দিয়ে একই public IP শেয়ার। এটা না দিলে NAT pool-এ যতগুলো IP আছে ততগুলো host-ই একসাথে বাইরে যেতে পারত।

</details>

---

## ১২. Final Testing Checklist

| Test Case | Command / Action | Expected Result |
| :--- | :--- | :--- |
| **DHCP Verification** | PC Desktop → IP Config → DHCP | সঠিক Subnet অনুযায়ী IP, Gateway ও DNS পাবে |
| **Gateway Reachability** | `ping 192.168.x.1` | Reply from Gateway (Successful) |
| **DNS & Web Browsing** | PC Browser → `http://www.university.local` | ওয়েব পেজ প্রদর্শিত হবে |
| **ACL Enforcement** | CSE PC থেকে Admin PC-তে `ping 192.168.30.x` | Destination Host Unreachable / Request Timed Out |
| **Server Access from CSE** | CSE PC থেকে Server-এ `ping 192.168.40.10` | Successful |
| **ISP WAN Ping** | R1 থেকে `ping 203.0.113.1` | `!!!!!` (Successful) |
| **NAT Translations** | PC থেকে ISP IP পিং করার পর R1-এ: `show ip nat translations` | Translation টেবিল এন্ট্রি তৈরি হবে |

---

## ১৩. Troubleshooting Commands

### Switch (SW1):
```ios
show vlan brief
show interfaces trunk
show mac address-table
```

### Router (R1 & ISP):
```ios
show ip interface brief
show ip route
show access-lists
show ip nat translations
show running-config
```

### PC Command Prompt:
```cmd
ipconfig /all
ping 192.168.10.1
nslookup www.university.local
```

---

## ১৪. Configuration Save Command

প্রতিটি ডিভাইসে কনফিগারেশন সংরক্ষণ করতে:

```ios
copy running-config startup-config
```
*(বা সংক্ষেপে `write` চাপুন)*

---

# 🔁 পুরো প্রজেক্টের লজিক

```
১. কাগজে ঠিকানা পরিকল্পনা      (VLAN → subnet → gateway)
২. Layer 2 চালু                 (VLAN, access port, trunk)
৩. Layer 3 গেটওয়ে              (ROAS-এ প্রতিটা VLAN-এর জন্য subinterface)
৪. সেবা                         (DHCP pool + relay, DNS, HTTP)
৫. বাইরে যাওয়ার পথ             (static route + default route)
৬. বাইরের ঠিকানা               (NAT overload / PAT)
৭. নিয়ন্ত্রণ                    (ACL)
৮. যাচাই                        (ping, traceroute, browser, show কমান্ড)
```

# ✅ ফাইনাল চেকলিস্ট

- [ ] প্রতিটা VLAN-এর PC IP পাচ্ছে (DHCP)
- [ ] VLAN-এর ভেতরে ping হচ্ছে
- [ ] VLAN থেকে VLAN-এ ping হচ্ছে (ROAS)
- [ ] `www.university.edu` ব্রাউজারে খুলছে (DNS + HTTP)
- [ ] বাইরের নেটওয়ার্কে ping যাচ্ছে (static route)
- [ ] বাইরে থেকে NAT হয়ে ট্রাফিক যাচ্ছে (`show ip nat translations`)
- [ ] Admin VLAN-এ ACL কাজ করছে (ব্লক হয়েছে)
- [ ] `show running-config` নিয়ে সেভ করেছি

# 🎓 শেষ কথা

এই লেসন পারলে তুমি আসলে **ছোট একটা ক্যাম্পাস নেটওয়ার্ক নিজে বানাতে পারো** — এটাই CCNA-র আসল লক্ষ্য।
এখন প্র্যাকটিস চালিয়ে যাও: [🅰️ হাতে-কলমে কোর্স](../lessons/01-router-cli-basics.md) · [📝 প্র্যাকটিস লিস্ট](../lessons/11-practice-list.md) · [🔧 Problem Solve](../lessons/12-problem-solve.md)

---

> **নেভিগেশন:** [⬅ লেসন ৮](08-troubleshooting.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [🅰️ হাতে-কলমে কোর্স](../lessons/01-router-cli-basics.md)

**এই লেসনের Tags:** `#capstone` `#vlan` `#roas` `#dhcp-relay` `#nat` `#acl` `#project`
