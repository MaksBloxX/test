# লেসন ৭ · ACL ও NAT — ফিল্টারিং এবং Address Translation

> **নেভিগেশন:** [⬅ লেসন ৬](06-subnetting-vlsm.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৮ ➡](08-troubleshooting.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| ACL দিয়ে ট্রাফিক ফিল্টার, NAT/PAT দিয়ে private IP-কে ইন্টারনেটে পাঠানো | ~৬০ মিনিট | 🟠 Intermediate | নিজে তৈরি (R1 + R2/ISP + ২ PC) |

**Tags:** `#acl` `#standard-acl` `#extended-acl` `#nat` `#pat` `#security` `#wildcard-mask`

---

> 📌 এই লেসনটা ঠিক পাশের কোর্স **লেসন ০৮ (Final Project)**-এর পরের ধাপ। সেখানে শুধু নেটওয়ার্ক চালু করতে শিখেছ; এখানে শিখবে **কে কী করতে পারবে** আর **বাইরে কীভাবে বের হবে**।


## ১. ACL (Access Control List)

### ১. ACL কী?

> **Definition:** An Access Control List (ACL) is a sequential list of permit or deny statements (rules) applied to IP addresses or upper-layer protocols to filter network traffic.

সহজ কথায়, ACL হলো রাউটারের সিকিউরিটি রুলবুক। এটি সিদ্ধান্ত নেয় কোন ডেটা প্যাকেট রাউটারের ইন্টারফেস দিয়ে পাস হতে পারবে এবং কোনটি ড্রপ বা ব্লক হবে।

#### বাস্তব উদাহরণ:
ধরি, তোমার University Network-এ তিনটি ডিপার্টমেন্ট আছে:
* **CSE**
* **EEE**
* **Administration**

তুমি চাও CSE এবং EEE-এর পিসি সাধারণ Web Server ব্যবহার করতে পারবে, কিন্তু Administration সার্ভারে কেবল নির্দিষ্ট এডমিন হোস্ট ছাড়া আর কেউ অ্যাক্সেস করতে পারবে না। ACL দিয়ে এই ধরনের ট্রাফিক ফিল্টারিং করা হয়।

---

### ২. ACL-এর প্রকারভেদ

| ACL Type | রেঞ্জ (Number) | ফিল্টারিং ক্রাইটেরিয়া | কোথায় বসানো উচিত (Best Practice) |
| :--- | :--- | :--- | :--- |
| **Standard ACL** | `1–99` ও `1300–1999` | কেবল **Source IP Address** ফিল্টার করে | **Destination-এর যত কাছে সম্ভব** |
| **Extended ACL** | `100–199` ও `2000–2699` | **Source IP, Destination IP, Protocol (TCP/UDP/ICMP), এবং Port** ফিল্টার করে | **Source-এর যত কাছে সম্ভব** |

> **মূল নীতি:**
> * **Standard ACL:** Source IP-based filtering.
> * **Extended ACL:** Source, Destination, Protocol ও Port-based granular filtering.
> * **Implicit Deny:** প্রতিটি ACL-এর শেষে একটি অদৃশ্য `deny ip any any` থাকে। কোনো রুল ম্যাচ না করলে ট্রাফিক ড্রপ হয়ে যায়।

---

### 🧪 Lab 1: Standard ACL Configuration

#### Objective
Standard ACL ব্যবহার করে নির্দিষ্ট একটি হোস্ট PC0 (`192.168.1.10`)-কে রিমোট নেটওয়ার্কে অ্যাক্সেস করা থেকে ব্লক করা, কিন্তু অন্য সব হোস্টকে অনুমোদন দেওয়া।

#### Topology
```
PC0 [192.168.1.10] ─── SW1 ─── [G0/0] R1 [G0/1] ─── SW2 ─── PC1 [192.168.2.10]
```

#### IP Addressing Plan
| Device | Interface | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **PC0** | NIC | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` |
| **PC1** | NIC | `192.168.2.10` | `255.255.255.0` | `192.168.2.1` |
| **R1** | G0/0 | `192.168.1.1` | `255.255.255.0` | N/A |
| **R1** | G0/1 | `192.168.2.1` | `255.255.255.0` | N/A |

#### Step 1: রাউটার ইন্টারফেস কনফিগার করো
```cisco
enable
configure terminal

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit

interface gigabitEthernet 0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown
exit
```

#### Step 2: Standard ACL তৈরি করো
```cisco
access-list 10 deny host 192.168.1.10
access-list 10 permit any
```
* `access-list 10`: Standard ACL নম্বর (১-৯৯ এর মধ্যে)।
* `deny host 192.168.1.10`: নির্দিষ্ট সোর্স আইপি ব্লক করা হলো।
* `permit any`: বাকি সকল হোস্টের ট্রাফিককে অনুমোদন দেওয়া হলো (এটি না দিলে Implicit Deny-এর কারণে পুরো নেটওয়ার্ক ব্লক হয়ে যেত)।

#### Step 3: ইন্টারফেসে ACL Apply করো
Standard ACL ডেসটিনেশনের যত কাছে সম্ভব প্লেস করতে হয়, তাই R1-এর Outgoing ইন্টারফেস `G0/1`-এ প্রয়োগ করব:
```cisco
interface gigabitEthernet 0/1
 ip access-group 10 out
exit
end
```

#### Step 4: ভেরিফিকেশন ও টেস্ট
1. **PC0 (`192.168.1.10`) থেকে `ping 192.168.2.10` করো:** 
   * ফলাফল: `Destination host unreachable` (ব্লক হয়েছে)।
2. **একই সাবনেটের অন্য পিসি (`192.168.1.11`) থেকে পিং করো:**
   * ফলাফল: `Reply from 192.168.2.10` (সফল)।
3. **রাউটারে ম্যাচ কাউন্টার চেক করো:**
```cisco
show access-lists
show ip interface gigabitEthernet 0/1
```

---

## ২. Extended ACL Configuration

Extended ACL দিয়ে নির্দিষ্ট প্রোটোকল বা সার্ভিস পোর্ট (যেমন HTTP, HTTPS, Ping/ICMP) ফিল্টার করা যায়।

### 🧪 Scenario: HTTP Web Traffic Block করা
ধরি, PC0 যেন PC1-এর ওয়েব সার্ভারে **HTTP (TCP Port 80)** ব্যবহার করতে না পারে, কিন্তু সাধারণ Ping (ICMP) বা অন্যান্য ট্রাফিক ঠিকঠাক চলতে পারে।

```cisco
configure terminal

! Extended ACL Definition
access-list 101 deny tcp host 192.168.1.10 host 192.168.2.10 eq 80
access-list 101 permit ip any any

! Apply close to the source (Inbound on G0/0)
interface gigabitEthernet 0/0
 ip access-group 101 in
exit
end
```

### কমান্ড ব্রেকডাউন:
| কমান্ড অংশ | অর্থ ও কাজ |
| :--- | :--- |
| `access-list 101` | Extended ACL নম্বর (১০০-১৯৯ রেঞ্জ) |
| `deny tcp` | TCP প্রোটোকলের প্যাকেট ড্রপ করবে |
| `host 192.168.1.10` | Source IP (PC0) |
| `host 192.168.2.10` | Destination IP (Server/PC1) |
| `eq 80` | Port 80 (HTTP / `www`) সমান হলে ম্যাচ করবে |
| `permit ip any any` | বাকি সকল প্রোটোকল এবং আইপি ট্রাফিক অ্যালাউ করবে |

---

## ৩. NAT (Network Address Translation)

### ১. NAT কী এবং কেন প্রয়োজন?

> **Definition:** Network Address Translation (NAT) is a method of mapping an IP address space into another by modifying network address information in the IP header while transit across a routing device.

* **সমস্যা:** IPv4 অ্যাড্রেসের সংকট। লোকাল ল্যানে ব্যবহৃত Private IP (RFC 1918 যেমন `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) ইন্টারনেটে রাউটেবল নয়।
* **সমাধান:** NAT প্রাইভেট আইপি অ্যাড্রেসগুলোকে পাবলিক আইপিতে পরিবর্তন করে ইন্টারনেটের সাথে যোগাযোগ সম্ভব করে।

### ২. NAT-এর প্রকারভেদ
1. **Static NAT:** একটি Private IP-এর জন্য একটি ফিক্সড Public IP (সাধারণত ওয়েব বা মেইল সার্ভারে ব্যবহৃত হয়)।
2. **Dynamic NAT:** একাধিক Private IP-কে একটি নির্দিষ্ট Public IP Pool থেকে ডায়নামিকালি আইপি দেয়।
3. **PAT (Port Address Translation / NAT Overload):** একটিমাত্র Public IP Address এবং ভিন্ন ভিন্ন **Source Port Number** ব্যবহার করে হাজার হাজার প্রাইভেট হোস্টকে ইন্টারনেটের সাথে যুক্ত করে। এটিই বাসাবাড়ি ও কর্পোরেট অফিসে সবচেয়ে বেশি ব্যবহৃত হয়।

---

### 🧪 Lab 2: PAT (NAT Overload) Configuration

#### Topology
```
[LAN] PC0 ─── SW1 ─── [G0/0] R1 [G0/1] ─── (WAN) ─── ISP Router ─── Internet/Server
```

#### Addressing Plan
| Device / Interface | IP Address | Subnet Mask | ভূমিকা |
| :--- | :--- | :--- | :--- |
| **PC0** | `192.168.1.10` | `255.255.255.0` | Inside Local Host |
| **R1 G0/0** | `192.168.1.1` | `255.255.255.0` | Inside Gateway |
| **R1 G0/1** | `203.0.113.2` | `255.255.255.252 (/30)` | Outside Public Interface |
| **ISP G0/0** | `203.0.113.1` | `255.255.255.252 (/30)` | ISP Next-Hop Gateway |
| **ISP Loopback/Server** | `198.51.100.1` | `255.255.255.0` | Remote Internet Destination |

---

### Configuration Steps (R1-এ):

#### Step 1: Inside ও Outside Interface নির্ধারণ করো
```cisco
enable
configure terminal

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 ip nat inside
 no shutdown
exit

interface gigabitEthernet 0/1
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
 no shutdown
exit
```

#### Step 2: কোন সাবনেট NAT হবে তা Standard ACL দিয়ে নির্বাচন করো
```cisco
access-list 1 permit 192.168.1.0 0.0.0.255
```
*(এখানে `0.0.0.255` হলো Wildcard Mask, যা পুরো `192.168.1.0/24` নেটওয়ার্ককে ম্যাচ করে)*

#### Step 3: NAT Overload (PAT) সক্রিয় করো
```cisco
ip nat inside source list 1 interface gigabitEthernet 0/1 overload
```
* `inside source list 1`: ACL 1-এ যাদের পারমিট দেওয়া হয়েছে তাদের অনুবাদ করবে।
* `interface gigabitEthernet 0/1`: ট্রাফিকের সোর্স আইপি হিসেবে G0/1 ইন্টারফেসের পাবলিক আইপি বসাবে।
* `overload`: পোর্ট নাম্বার ট্র্যাক করে একই আইপিতে একাধিক কানেকশন পরিচালনা (PAT) করবে।

#### Step 4: ISP-র দিকে Default Route দাও
```cisco
ip route 0.0.0.0 0.0.0.0 203.0.113.1
end
```

#### Step 5: NAT ভেরিফিকেশন ও ট্রাবলশুটিং
PC0 থেকে ISP সার্ভারের আইপি (`198.51.100.1`)-এ পিং করো। এরপর R1-এ কমান্ড চালাও:

```cisco
show ip nat translations
show ip nat statistics
```

#### Output Example:
```
Pro  Inside global         Inside local          Outside local        Outside global
icmp 203.0.113.2:1         192.168.1.10:1        198.51.100.1:1       198.51.100.1:1
```
> **ব্যাখ্যা:** পিসির Private IP `192.168.1.10` রাউটার পার হওয়ার সময় Public IP `203.0.113.2`-তে অনুবাদ হয়ে বাইরে পাঠানো হয়েছে।

---

## ৪. ACL বনাম NAT তুলনা

| Feature | ACL (Access Control List) | NAT (Network Address Translation) |
| :--- | :--- | :--- |
| **Primary Purpose** | ট্রাফিক পারমিট বা ড্রপ করে নিরাপত্তা নিশ্চিত করা | প্রাইভেট ও পাবলিক আইপি রূপান্তর করা |
| **Header Modification** | প্যাকেটের কোনো হেডার বা আইপি পরিবর্তন করে না | আইপি হেডার ও পোর্ট নাম্বার পরিবর্তন করে |
| **Security Role** | সরাসরি সিকিউরিটি ফিল্টার হিসেবে কাজ করে | একা সিকিউরিটি দেয় না (কেবল প্রাইভেট আইপি হাইড রাখে) |
| **Placement** | ট্রাফিকের সোর্স বা ডেস্টিনেশন ইন্টারফেসে (In/Out) | রাউটারের Inside ও Outside ইন্টারফেসের মাঝে |

---

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** ACL-এর একদম শেষে যে নিয়মটা লেখা থাকে না, কিন্তু কাজ করে — সেটা কী?

- **A.** `permit ip any any` — সব পাস
- **B.** `deny ip any any` — বাকি সব ব্লক (implicit deny)
- **C.** কোনো নিয়ম নেই, সব পাস হয়
- **D.** শুধু ICMP ব্লক

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. deny ip any any (implicit deny)**

**🧠 কেন:**

প্রতিটা ACL-এর শেষে Cisco নিজেই একটা অদৃশ্য `deny ip any any` বসায়। তাই **যে ট্রাফিক পার্মিট করবে, সেটা আগে লিখতে হবে** — নইলে সব ব্লক হয়ে যাবে। এজন্যই ACL-এ শেষে `permit` লিখতে হয়।

</details>

---

**প্রশ্ন ২.** Standard ACL আর Extended ACL-এর মূল পার্থক্য কী?

- **A.** Standard শুধু source IP দেখে; Extended source+destination+protocol+port দেখে
- **B.** Standard শুধু destination দেখে
- **C.** দুটোই একই, শুধু নাম আলাদা
- **D.** Extended শুধু hostname দেখে

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. Standard শুধু source IP দেখে; Extended source+destination+protocol+port দেখে**

**🧠 কেন:**

Standard (1–99) = শুধু **source IP** → তাই গন্তব্যের যত কাছে বসানো হয়।
Extended (100–199) = **source + destination + protocol + port** → তাই source-এর যত কাছে বসানো হয়, আগেই ব্লক হয়ে যায়।

</details>

---

**প্রশ্ন ৩.** Extended ACL কোথায় বসানো সবচেয়ে ভালো?

- **A.** destination-এর একদম কাছে
- **B.** source-এর যত কাছে সম্ভব
- **C.** যেকোনো জায়গায়, পার্থক্য নেই
- **D.** শুধু loopback-এ

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. source-এর যত কাছে সম্ভব**

**🧠 কেন:**

Extended ACL বিস্তারিত মিলিয়ে দেখে, তাই source-এর কাছেই বসালে অপ্রয়োজনীয় ট্রাফিক নেটওয়ার্কের ভেতরে ঢোকার আগেই ব্লক হয় — ব্যান্ডউইথ বাঁচে।

</details>

---

**প্রশ্ন ৪.** NAT-এ `overload` শব্দটা কী বোঝায়?

- **A.** সবাই একই IP পায়, তাই ক্র্যাশ করে
- **B.** একটাই public IP, পোর্ট নম্বর দিয়ে অনেক private host আলাদা করা হয় (PAT)
- **C.** NAT বন্ধ হয়ে যায়
- **D.** শুধু UDP কাজ করে

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. একটাই public IP, পোর্ট দিয়ে অনেক host আলাদা (PAT)**

**🧠 কেন:**

`ip nat inside source list 1 interface g0/0 overload` — `overload` মানেই **PAT**: এক public IP-তে অনেক private host, প্রত্যেকের জন্য আলাদা port number ব্যবহার করে। এজন্য একই সাইটে ১০০টা PC-ও একটা public IP-তে ইন্টারনেট পায়।

</details>

---

**প্রশ্ন ৫.** NAT চালু করার পর বাইরে থেকে ভেতরের কোনো PC-তে সরাসরি ping করা যাচ্ছে না — কেন?

- **A.** NAT ভাঙা
- **B.** ভেতরের IP বাইরে থেকে অজানা, আর NAT-এ static entry নেই
- **C.** ping বন্ধ করা আছে সবসময়
- **D.** ACL লাগানো যায় না

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. ভেতরের IP বাইরে থেকে অজানা**

**🧠 কেন:**

NAT-এর কাজই হলো ভেতরের ঠিকানা লুকানো। বাইরে থেকে আসতে হলে **static NAT / port forwarding** লাগবে, নইলে destination ঠিকানাটাই অজানা থেকে যায়।

</details>

---

## 🎯 Practical Challenge Tasks

1. **Topology Setup:** Packet Tracer-এ দুটি রাউটার (Campus ও ISP) ও দুটি সুইচ সংযোগ করো।
2. **Access Control:**
   * একটি Standard ACL তৈরি করো যেন কেবল নির্দিষ্ট একটি আইপি ব্লক হয়।
   * একটি Extended ACL তৈরি করে Web (HTTP port 80) ড্রপ করো কিন্তু ICMP (Ping) চালু রাখো।
3. **PAT Execution:**
   * রাউটারে `ip nat inside` ও `ip nat outside` চিহ্নিত করো।
   * `overload` কিওয়ার্ড ব্যবহার করে ইন্টারনেটের সাথে যোগাযোগ স্থাপন করো।
4. **Verification:**
   * `show ip nat translations` দিয়ে সক্রিয় অনুবাদ টেবিল পর্যবেক্ষণ করো।
   * `show access-lists` দিয়ে ম্যাচ হওয়া প্যাকেটের সংখ্যা পরীক্ষা করো।

```cisco
! Useful Verification Commands
show access-lists
show ip interface brief
show ip route
show ip nat translations
show ip nat statistics
```

---

# 🔁 এক নজরে লজিক

```
ACL = ওপর থেকে নিচে পড়া রুলের তালিকা
      ↓ প্রথম যে রুল মেলে, সেটাই কাজ করে (তারপর আর দেখে না)
      ↓ শেষে implicit deny → তাই অন্তত একটা permit লাগবে

Standard (1–99)   : শুধু SOURCE      → destination-এর কাছে বসাও
Extended (100–199): source+dest+port → source-এর কাছে বসাও

NAT:
  inside local  → ভেতরের আসল IP
  inside global → বাইরে যে IP দেখায়
  overload      → এক public IP, পোর্ট দিয়ে সবার আলাদা (PAT)
```

# ❌ যেখানে অনেকে আটকায়

| ভুল | আসল কথা |
|---|---|
| ACL লিখলেই কাজ করবে | ইন্টারফেসে `ip access-group … in/out` না দিলে কিছুই হয় না |
| রুলের ক্রম যেকোনো | **জোরে ভুল** — নির্দিষ্ট রুল আগে, সাধারণ রুল পরে |
| NAT মানেই নিরাপত্তা | না, NAT ঠিকানা বদলায়; ফিল্টার করে ACL |
| wildcard mask = subnet mask | উল্টো! `/24` → wildcard `0.0.0.255` |

# ✅ নিজে যাচাই করো

- [ ] ACL-এর implicit deny বুঝি, আর কেন শেষে permit লাগে বলতে পারি
- [ ] Standard vs Extended — কোনটা কোথায় বসাব, বলতে পারি
- [ ] `0.0.0.255` wildcard-টা `/24`-এর জন্য কেন, বলতে পারি
- [ ] `show access-lists` আর `show ip nat translations` দিয়ে যাচাই করতে পারি
- [ ] PAT-এ overload কী করে, বলতে পারি

# 🔮 পরের ধাপ

কিছু ভাঙবে — সেটাই স্বাভাবিক। এখন শিখো **ভাঙা নেটওয়ার্ক কীভাবে ধাপে ধাপে খুঁজে বের করে ঠিক করতে হয়** →
[লেসন ০৮ · Network Troubleshooting](08-troubleshooting.md)

---

> **নেভিগেশন:** [⬅ লেসন ৬](06-subnetting-vlsm.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৮ ➡](08-troubleshooting.md)

**এই লেসনের Tags:** `#acl` `#extended-acl` `#wildcard-mask` `#nat` `#pat` `#overload` `#security`
