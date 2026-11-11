# লেসন ৮ · Network Troubleshooting — ৭ কমান্ড + ৬ ল্যাব

> 🌐 **English:** [Read this guide in English](../en/ccna-fundamentals/08-troubleshooting.md) · [English track index](../en/README.md)

> **নেভিগেশন:** [⬅ লেসন ৭](07-acl-nat.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৯ ➡](09-capstone-university-lab.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| ৭টা কমান্ড আর ৬টা ল্যাব দিয়ে ভাঙা নেটওয়ার্ক ধাপে ধাপে খুঁজে বের করা ও ঠিক করা | ~৫৫ মিনিট | 🟡 Intermediate | যেকোনো আগের pkt (ইচ্ছাকৃতভাবে ভেঙে) |

**Tags:** `#troubleshooting` `#ping` `#traceroute` `#show-ip-route` `#gateway` `#vlan` `#bottom-up`

---

### 🖼️ চিত্রে বোঝো: চার ধাপে নেটওয়ার্ক ত্রুটি শনাক্ত

![চার ধাপে নেটওয়ার্ক ত্রুটি শনাক্ত — নিজের IP → লোকাল গেটওয়ে → রিমোট হপ → শেষ সার্ভিস; প্রথম ব্যর্থতা খুঁজে বের করো।](../assets/diagrams/ccna-08-troubleshoot-tests.svg)

> **ছবির সারকথা:** নিজের IP → লোকাল গেটওয়ে → রিমোট হপ → শেষ সার্ভিস; প্রথম ব্যর্থতা খুঁজে বের করো।

---

> 📌 Troubleshooting মানে অনুমান নয় — **বাদ দিয়ে যাওয়া**। "কী কী ঠিক আছে" এক এক করে বাদ দিলে ভাঙা জিনিসটা নিজে থেকেই ধরা পড়ে।


## ১. Network Troubleshooting কী?

> **Definition:** Network troubleshooting is the systematic process of identifying, diagnosing, and resolving network problems.

সহজ কথায়, নেটওয়ার্ক সঠিকভাবে কাজ না করলে সমস্যার মূল কারণ শনাক্ত করে সমাধান করাই হলো **Network Troubleshooting**।

### বাস্তব উদাহরণ
ধরি, University Lab-এ:
- PC0 থেকে PC1-এ Ping হচ্ছে না।
- PC কোনোভাবেই Internet Access করতে পারছে না।
- VLAN 10-এর কোনো PC Server Room-এর সার্ভার রিচ করতে পারছে না।
- Router-এর Interface "Down" দেখাচ্ছে।

---

## ২. Troubleshooting-এর ৭টি গুরুত্বপূর্ণ Command

CCNA ল্যাব ও বাস্তব নেটওয়ার্কে নিচের কমান্ডগুলো সবচেয়ে বেশি ব্যবহৃত হয়:

| Command | কাজ / বিবরণ | রান করার স্থান |
| :--- | :--- | :--- |
| `ping <ip-address>` | অপর প্রান্তের ডিভাইস Reachable কি না (ICMP Echo) পরীক্ষা করা | PC / Router / Switch |
| `tracert` (Windows) / `traceroute` (IOS) | ডেস্টিনেশনে যাওয়ার পথে কোন কোন Hop/Router পার হচ্ছে তা দেখা | PC / Router |
| `ipconfig` / `ipconfig /all` | পিসির IP, Subnet Mask, Gateway এবং DNS ভেরিফাই করা | PC Command Prompt |
| `show ip interface brief` | রাউটার বা সুইচের ইন্টারফেস, আইপি ও Layer 1/2 স্ট্যাটাস দেখা | Cisco IOS CLI |
| `show running-config` | সুইচে বা রাউটারে রানিং কনফিগারেশন চেক করা | Cisco IOS CLI |
| `show ip route` | রাউটারের Routing Table চেক করা | Cisco Router CLI |
| `show mac address-table` | সুইচের কোন পোর্টে কোন ম্যাক অ্যাড্রেস সংযুক্ত তা দেখা | Cisco Switch CLI |

### কমান্ডের ব্যবহারগত পার্থক্য:

**PC Command Prompt:**
```shell
ipconfig /all
ping 192.168.1.1
tracert 192.168.2.10
```

**Router / Switch CLI:**
```text
show ip interface brief
show running-config
show ip route
```

---

## 🧪 Lab 1: Ping দিয়ে Network পরীক্ষা

### Objective
দুটি PC-এর মধ্যে বেসিক Layer 3 Connectivity পরীক্ষা করা।

### Topology
```text
PC0 [192.168.1.10/24] ───── SW1 ───── PC1 [192.168.1.20/24]
```

### IP Configuration Plan
| Device | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- |
| **PC0** | `192.168.1.10` | `255.255.255.0` | N/A |
| **PC1** | `192.168.1.20` | `255.255.255.0` | N/A |

### Step 1: PC0 থেকে টেস্ট করা
1. Cisco Packet Tracer-এ **PC0 → Desktop → Command Prompt** ওপেন করো।
2. কমান্ড চালাও:
```shell
ping 192.168.1.20
```

#### Successful Output:
```text
Pinging 192.168.1.20 with 32 bytes of data:
Reply from 192.168.1.20: bytes=32 time<1ms TTL=128
Reply from 192.168.1.20: bytes=32 time<1ms TTL=128
Reply from 192.168.1.20: bytes=32 time<1ms TTL=128
```
> **অর্থ:** PC0 সফলভাবে PC1 থেকে ICMP Echo Reply পাচ্ছে।

#### Failed Output:
```text
Request timed out.
Request timed out.
```
> **Troubleshooting Steps (যদি Ping ফেইল করে):**
> 1. দুটি PC-এর IP Address চেক করো।
> 2. Subnet Mask এক সাবনেটের কি না (`255.255.255.0`) নিশ্চিত হও।
> 3. ক্যাবল ঠিক আছে কি না এবং সুইচের পোর্ট লিঙ্ক লাইট সবুজ (Green) কি না চেক করো।
> 4. ফায়ারওয়াল বা ACL ট্রাফিক ড্রপ করছে কি না দেখো।

---

## 🧪 Lab 2: IP Address / Subnet ভুল হলে কী হবে?

### দৃশ্যপট
- **PC0 Configuration:** `192.168.1.10 / 255.255.255.0` (Network: `192.168.1.0/24`)
- **PC1 Configuration:** `192.168.2.20 / 255.255.255.0` (Network: `192.168.2.0/24`)

```text
PC0 [192.168.1.10] ───── [Layer 2 Switch] ───── PC1 [192.168.2.20]
```

### ফলাফল ও ব্যাখ্যা
PC0 থেকে PC1-এ পিং করলে ফেইল করবে (`Destination host unreachable` বা `Request timed out`)।

* **কারণ:** PC0 নিজের Subnet Mask দিয়ে বুঝতে পারে PC1 অন্য নেটওয়ার্কের হোস্ট। যেহেতু এখানে কোনো Router নেই এবং কোনো Default Gateway কনফিগার করা নেই, তাই Layer 2 Switch ভিন্ন সাবনেটের মধ্যে প্যাকেট পাঠাতে পারবে না।
* **Solution:** একই LAN-এ যোগাযোগ করতে হলে PC1-এর IP পরিবর্তন করে একই নেটওয়ার্কে আনতে হবে:
  * New IP: `192.168.1.20`
  * Subnet Mask: `255.255.255.0`

---

## 🧪 Lab 3: Router Interface Down Troubleshooting

### Problem
রাউটারে `show ip interface brief` দিলে দেখাচ্ছে:
```text
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES manual administratively down down
```
> **কারণ:** সিসকো রাউটারের ইন্টারফেস ডিফল্টভাবে শাটডাউন অবস্থায় থাকে।

### Solution
রাউটার সিএলআই-তে গিয়ে ইন্টারফেস চালু করো:
```text
enable
configure terminal
interface gigabitEthernet 0/0
 no shutdown
end
```

### Interface Status Matrix
| Status (Layer 1) | Protocol (Layer 2) | সমস্যা ও সম্ভাব্য কারণ |
| :--- | :--- | :--- |
| **up** | **up** | সম্পূর্ণ কার্যকর (Healthy) |
| **administratively down** | **down** | ইন্টারফেসে `shutdown` কমান্ড দেওয়া আছে |
| **down** | **down** | ক্যাবল খোলা, কাটা বা বিপরীত প্রান্তের ডিভাইস বন্ধ |
| **up** | **down** | Layer 2 প্রোটোকল/ইনক্যাপসুলেশন মিসম্যাচ, ক্লক রেট বা স্পিড সমস্যা |

---

## 🧪 Lab 4: Default Gateway ভুল হলে কী হবে?

### Topology
```text
PC0 ────── SW1 ────── [G0/0] R1 [G0/1] ────── SW2 ────── PC1
```

### Addressing Plan
| Device | Interface | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **PC0** | NIC | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` |
| **R1** | G0/0 | `192.168.1.1` | `255.255.255.0` | N/A |
| **R1** | G0/1 | `192.168.2.1` | `255.255.255.0` | N/A |
| **PC1** | NIC | `192.168.2.10` | `255.255.255.0` | `192.168.2.1` |

### দৃশ্যপট ও সমস্যা
ধরো, PC0-তে ভুল করে গেটওয়ে দেওয়া হয়েছে: `192.168.1.254`।
- PC0 একই ল্যানের হোস্টদের সাথে কথা বলতে পারলেও রিমোট নেটওয়ার্কের PC1 (`192.168.2.10`) কে রিচ করতে পারবে না।

### Solution
PC0-এর Desktop → IP Configuration-এ গিয়ে গেটওয়ে সংশোধন করো:
```text
Default Gateway: 192.168.1.1
```
যাচাই করার স্টেপ:
```shell
ping 192.168.1.1      :: নিজের গেটওয়ে চেক করা
ping 192.168.2.10     :: রিমোট পিসি চেক করা
```

---

## 🧪 Lab 5: Routing Table পরীক্ষা (`show ip route`)

রাউটার R1-এ সরাসরি কানেক্টেড নেটওয়ার্ক দেখার কমান্ড:
```text
show ip route
```

### Expected Output:
```text
Gateway of last resort is not set

C    192.168.1.0/24 is directly connected, GigabitEthernet0/0
L    192.168.1.1/32 is directly connected, GigabitEthernet0/0
C    192.168.2.0/24 is directly connected, GigabitEthernet0/1
L    192.168.2.1/32 is directly connected, GigabitEthernet0/1
```

### Route Code Cheat Sheet
| Code | প্রোটোকল / টাইপ |
| :---: | :--- |
| **C** | Connected (সরাসরি ইন্টারফেসে যুক্ত সাবনেট) |
| **L** | Local (ইন্টারফেসে বসানো নির্দিষ্ট আইপি, /32) |
| **S** | Static Route |
| **O** | OSPF Dynamic Routing |
| **R** | RIP |
| **D** | EIGRP |
| **\*** | Candidate Default |

> **নোট:** রাউটিং টেবিলে যদি নির্দিষ্ট ডেসটিনেশন নেটওয়ার্কের কোনো রুট না থাকে, তবে রাউটার প্যাকেট ড্রপ করবে। সমাধান: Static Route, Default Route অথবা Dynamic Routing কনফিগার করা।

---

## 🧪 Lab 6: VLAN ও Trunk Troubleshooting

### লক্ষণ:
PC0 (VLAN 10) এবং PC1 (VLAN 20) একই সুইচে থাকা সত্ত্বেও পিং পাচ্ছে না।

### চেকলিস্ট ও কমান্ড:
1. **VLAN আছে কি না ও পোর্ট অ্যাসাইন ঠিক আছে কি না:**
   ```text
   show vlan brief
   ```
2. **রাউটার বা সুইচের ট্রাঙ্ক পোর্ট ঠিক আছে কি না:**
   ```text
   show interfaces trunk
   ```
3. **Inter-VLAN Routing (Router-on-a-Stick):**
   * রাউটারে সাব-ইন্টারফেস করা হয়েছে কি না?
   * `encapsulation dot1Q <vlan-id>` সঠিক কি না?
   * প্রতিটি সাব-ইন্টারফেস আইপি সংশ্লিষ্ট VLAN-এর পিসির গেটওয়ে হিসেবে বসানো আছে কি না?

---

## 🧠 Network Troubleshooting-এর Golden Method (Bottom-Up)

যেকোনো নেটওয়ার্ক ফল্ট ফিক্স করার জন্য এই ৭টি ধাপ ক্রমানুসারে অনুসরণ করো:

```text
Step 1: Physical Layer     ── Cable Connected? Link Light Green? Interface Up?
Step 2: IP Configuration   ── IP, Subnet Mask, Gateway ঠিক আছে?
Step 3: Local Loopback     ── ping 127.0.0.1 (TCP/IP Stack ঠিক আছে কি না)
Step 4: Self IP Ping       ── ping <নিজের-IP> (NIC কার্ড ঠিক আছে কি না)
Step 5: Gateway Ping       ── ping <Default-Gateway> (রাউটার কানেক্টিভিটি ঠিক আছে?)
Step 6: Remote Ping        ── ping <Remote-IP> (Routing সচল আছে?)
Step 7: ACL & Firewall     ── show access-lists (কোনো রুল ট্রাফিক ড্রপ করছে?)
```

---

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** একটা PC-তে `ipconfig` দিয়ে `169.254.10.5` দেখছ — প্রথমে কী সন্দেহ করবে?

- **A.** কেবল কাটা
- **B.** DHCP থেকে IP পায়নি (APIPA)
- **C.** DNS সার্ভার নষ্ট
- **D.** NAT কাজ করছে না

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. DHCP থেকে IP পায়নি (APIPA)**

**🧠 কেন:**

`169.254.x.x` = APIPA — অর্থাৎ PC DHCP server-এ পৌঁছাতে পারেনি। চেক করো: DHCP pool আছে কি, VLAN/port ঠিক আছে কি, আর server-এ ping যায় কি না। DNS নয় — DNS সমস্যায় IP ঠিক থাকত।

</details>

---

**প্রশ্ন ২.** `ping` ফেল করছে, কিন্তু `show ip interface brief`-এ সব interface **up/up**। পরের ধাপে কী দেখবে?

- **A.** সোজা কেবল বদলাব
- **B.** IP, subnet mask, default gateway — তিনটা মিলছে কি না দেখব
- **C.** রাউটার রিবুট করব
- **D.** সব ACL মুছে ফেলব

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. IP / mask / gateway মিলছে কি না**

**🧠 কেন:**

up/up মানে ফিজিক্যাল আর ডেটা-লিংক ঠিক আছে। তাহলে সমস্যা Layer 3-এ — হয় IP ভুল subnet-এ, নাহয় gateway ভুল/নেই, নাহয় routing নেই। `show ip route` দেখলেই বোঝা যায়।

</details>

---

**প্রশ্ন ৩.** `show ip route`-এ `C` আর `S` অক্ষর দুটো কী বোঝায়?

- **A.** C = connected, S = static
- **B.** C = static, S = connected
- **C.** C = Cisco, S = server
- **D.** দুটোই একই

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. C = connected, S = static**

**🧠 কেন:**

`C` = directly connected (ইন্টারফেসে IP দেওয়াই), `S` = static route (হাতে `ip route` দিয়ে লেখা)। এছাড়া `O` = OSPF, `R` = RIP, `S*` = default route।

</details>

---

**প্রশ্ন ৪.** একই switch-এ দুটো PC — একটা VLAN 10-এ, আরেকটা VLAN 20-এ। ping হবে?

- **A.** হবে, কারণ একই switch
- **B.** হবে না — ভিন্ন VLAN মানে ভিন্ন নেটওয়ার্ক, router/ROAS লাগবে
- **C.** শুধু switch রিবুট করলে হবে
- **D.** শুধু কেবল বদলালে হবে

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. হবে না — router/ROAS দরকার**

**🧠 কেন:**

VLAN = আলাদা broadcast domain। দুই VLAN-এর মাঝে যোগাযোগ করতে হলে **Inter-VLAN Routing** (router-on-a-stick বা L3 switch) লাগবে — একই switch-এ থাকা মানে কিছু না।

</details>

---

**প্রশ্ন ৫.** Bottom-Up troubleshooting পদ্ধতি মানে কী?

- **A.** Layer 7 থেকে নিচে নামা
- **B.** Layer 1 (কেবল/পোর্ট) থেকে শুরু করে ওপরে ওঠা
- **C.** শুধু ACL চেক করা
- **D.** রাউটার বদলানো

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Layer 1 থেকে ওপরে ওঠা**

**🧠 কেন:**

সহজে ধরা যায় এমন জিনিস আগে: কেবল লাগানো? পোর্টে light? link up? তারপর MAC, তারপর IP, তারপর সেবা। বেশিরভাগ সমস্যা Layer 1–2-এই ধরা পড়ে।

</details>

---

## 🎯 Final Practical Challenge

### Topology
```text
PC0 ────── SW1 ────── [G0/0] R1 [G0/1] ────── SW2 ────── PC1
```

### Addressing Table
| Device | Interface | IP Address | Subnet Mask | Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **PC0** | NIC | `192.168.10.10` | `255.255.255.0` | `192.168.10.1` |
| **R1** | G0/0 | `192.168.10.1` | `255.255.255.0` | N/A |
| **R1** | G0/1 | `192.168.20.1` | `255.255.255.0` | N/A |
| **PC1** | NIC | `192.168.20.10` | `255.255.255.0` | `192.168.20.1` |

### Tasks:
1. রাউটার R1-এর G0/0 ও G0/1 কনফিগার করো (`no shutdown` সহ)।
2. PC0 থেকে PC1-এ পিং করে সাকসেসফুল করো।
3. PC1-এর Gateway ভুল করে `192.168.20.254` দাও এবং PC0 থেকে পিং করে ফেইল পর্যবেক্ষণ করো।
4. পুনরায় গেটওয়ে ঠিক করে কানেক্টিভিটি পুনরুদ্ধার করো।
5. রাউটারে নিচের কমান্ডগুলো পরীক্ষা করো:
   ```text
   show ip interface brief
   show ip route
   ```

### 💥 Bonus Challenge:
রাউটারের `G0/0` ইন্টারফেসে গিয়ে `shutdown` কমান্ড দাও:
```text
configure terminal
interface gigabitEthernet 0/0
 shutdown
end
```
**প্রশ্ন ও সমাধান:**
* **প্রশ্ন:** PC0 থেকে PC1-এ পিং ফেইল হলো কেন?
* **উত্তর:** রাউটারের G0/0 ইন্টারফেসটি Administratively Down হয়ে যাওয়ায় PC0 তার গেটওয়ে পর্যন্ত প্যাকেট পাঠাতে পারছে না।
* **সমাধান:** `interface gigabitEthernet 0/0`-তে গিয়ে `no shutdown` কমান্ড চালাতে হবে।

---

---

# 🔁 এক নজরে লজিক

```
Layer 1 → কেবল, পোর্ট, link light            (সবচেয়ে বেশি সমস্যা এখানে)
Layer 2 → MAC table, VLAN, trunk
Layer 3 → IP, mask, gateway, routing table
Layer 4+ → port, DNS, HTTP service

প্রতিটা ধাপে প্রশ্ন: "এখানে ঠিক আছে?" → হ্যাঁ হলে পরের ধাপে যাও
```

# 🧰 কমান্ড চিট-শিট

| কী জানতে চাও | কমান্ড |
|---|---|
| IP / mask / gateway ঠিক আছে? | `ipconfig` (PC), `show ip interface brief` (router/switch) |
| পথ আছে কি? | `traceroute 8.8.8.8` |
| routing table-এ কী আছে? | `show ip route` |
| VLAN বসেছে কি? | `show vlan brief` |
| trunk ঠিক আছে? | `show interfaces trunk` |
| MAC শেখা হয়েছে? | `show mac address-table` |
| ACL ব্লক করছে? | `show access-lists` |
| NAT হচ্ছে? | `show ip nat translations` |

# ✅ নিজে যাচাই করো

- [ ] `169.254.x.x` দেখলেই কী করব, জানি
- [ ] up/up কিন্তু ping fail — পরের ধাপ বলতে পারি
- [ ] `C`, `S`, `O` রুটের অর্থ বলতে পারি
- [ ] VLAN-এ isolate কেন হয়, বলতে পারি
- [ ] bottom-up কেন সবচেয়ে দ্রুত, বলতে পারি

# 🔮 পরের ধাপ

সবকিছু একসাথে — **VLAN + trunk + ROAS + DHCP relay + DNS + static route + NAT + ACL** নিয়ে একটা সম্পূর্ণ ক্যাম্পাস নেটওয়ার্ক →
[লেসন ০৯ · Capstone: University Network](09-capstone-university-lab.md)

---

> **নেভিগেশন:** [⬅ লেসন ৭](07-acl-nat.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৯ ➡](09-capstone-university-lab.md)

**এই লেসনের Tags:** `#troubleshooting` `#ping` `#traceroute` `#show-ip-route` `#vlan` `#bottom-up`
