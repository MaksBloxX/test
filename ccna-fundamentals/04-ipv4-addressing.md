# লেসন ৪ · IPv4 Addressing — Public, Private ও Special Address

> 🌐 **English:** [Read this guide in English](../en/ccna-fundamentals/04-ipv4-addressing.md) · [English track index](../en/README.md)

> **নেভিগেশন:** [⬅ লেসন ৩](03-mac-ethernet-arp.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৫ ➡](05-subnetting-basics.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| IPv4 address-এর গঠন, subnet mask, network/host ভাগ, private-public আর special address | ~৪৫ মিনিট | 🟢 Beginner | নিজে তৈরি (২ PC + ১ Router বা Switch) |

**Tags:** `#ipv4` `#subnet-mask` `#private-ip` `#public-ip` `#apipa` `#octet` `#class`

---

### 🖼️ চিত্রে বোঝো: একটি IPv4 ঠিকানার Network ও Host অংশ

![একটি IPv4 ঠিকানার Network ও Host অংশ — `192.168.10.25/24`-এ প্রথম ২৪ বিট Network, শেষ ৮ বিট Host—.0 Network আর .255 Broadcast।](../assets/diagrams/ccna-04-ipv4-address.svg)

> **ছবির সারকথা:** `192.168.10.25/24`-এ প্রথম ২৪ বিট Network, শেষ ৮ বিট Host—.0 Network আর .255 Broadcast।

---

> 📌 এখান থেকে সংখ্যা আসবে। ভয় পেয়ো না — সব IPv4 কেবল **৪টা সংখ্যা**, প্রতিটা ০–২৫৫। এই লেসন শেষ হলে `192.168.10.25/24` দেখে নিজেই বলতে পারবে কোনটা নেটওয়ার্ক, কোনটা হোস্ট।


## ১. What is an IP Address?

* **Definition:** An IP address is a logical address assigned to a device on a network to identify it and enable communication.
* **বাংলায়:** নেটওয়ার্কে থাকা প্রতিটি ডিভাইসকে শনাক্ত করতে এবং তাদের মধ্যে ডেটা আদান-প্রদান করতে IP Address ব্যবহার করা হয়।

**উদাহরণ:**
* **PC-0:** `192.168.1.10`
* **PC-1:** `192.168.1.20`
* **Router:** `192.168.1.1`

এখানে প্রতিটি IP Address আলাদা ডিভাইসকে শনাক্ত করছে।

> **মনে রাখবে:**
> * **MAC Address:** সাধারণ Ethernet নেটওয়ার্কে Layer 2 (Data Link Layer)-তে ব্যবহৃত হয়।
> * **IP Address:** Layer 3 (Network Layer)-তে এন্ড-টু-এন্ড ডেলিভারির জন্য ব্যবহৃত হয়।
> * **Port Number:** Transport Layer (Layer 4)-এ নির্দিষ্ট অ্যাপ্লিকেশন বা সার্ভিস শনাক্ত করতে ব্যবহৃত হয়।

---

## ২. What is IPv4?

* **Definition:** IPv4 (Internet Protocol version 4) is a 32-bit logical addressing system used to identify devices on an IP network.

একটি IPv4 Address মোট **32 bits**-এর হয়। এতে ৪টি অংশ থাকে, প্রতিটি অংশকে **Octet** বলা হয়।

### Example: `192.168.1.10`

| Octet | Value | Binary Equivalent |
| :--- | :--- | :--- |
| **1st Octet** | 192 | `11000000` (8 bits) |
| **2nd Octet** | 168 | `10101000` (8 bits) |
| **3rd Octet** | 1 | `00000001` (8 bits) |
| **4th Octet** | 10 | `00001010` (8 bits) |

প্রতিটি Octet হলো $8\text{ bits}$।  
সুতরাং:
$$4 \times 8 = 32\text{ bits}$$

একটি Octet-এর decimal value সাধারণত **0 থেকে 255** পর্যন্ত হতে পারে ($2^8 = 256$ combinations)।

**উদাহরণ:**
* `192.168.1.10` — ✅ Valid IPv4 format
* `10.0.0.5` — ✅ Valid IPv4 format
* `256.168.1.10` — ❌ Invalid (কারণ 256 একটি Octet-এর সর্বোচ্চ সীমা 255 ছাড়িয়ে গেছে)

---

## ৩. IPv4 Address vs Subnet Mask

IP Address-এর পাশাপাশি সবসময় Subnet Mask ব্যবহার করা হয়।

* **Subnet Mask Definition:** A subnet mask identifies which part of an IPv4 address represents the network and which part represents the host.
* **সহজ কথায়:** IP Address-এর কতটুকু অংশ Network এবং কতটুকু অংশ Host—তা নির্ধারণ করতে Subnet Mask ব্যবহার করা হয়।

### Example:
* **IP Address:** `192.168.1.10`
* **Subnet Mask:** `255.255.255.0`
* **Prefix / CIDR:** `/24` (অর্থাৎ প্রথম 24 bits Network-এর জন্য সংরক্ষিত)

| Part | Value | বিট সংখ্যা |
| :--- | :--- | :--- |
| **Network part** | `192.168.1` | 24 bits |
| **Host part** | `.10` | 8 bits |
| **Subnet Mask** | `255.255.255.0` | `/24` |

এই উদাহরণে:
* **Network Address:** `192.168.1.0` (নেটওয়ার্কের নিজস্ব পরিচিতি)
* **Broadcast Address:** `192.168.1.255` (ঐ নেটওয়ার্কের সবাইকে মেসেজ পাঠানোর অ্যাড্রেস)
* **Usable Host Range:** `192.168.1.1` থেকে `192.168.1.254`

---

## ৪. Network Part vs Host Part

একটি IP Address দুটি মৌলিক অংশে বিভক্ত থাকে:
1. **Network Part:** কোন নেটওয়ার্কে ডিভাইসটি অবস্থান করছে তা বোঝায় (রাস্তার নামের মতো)।
2. **Host Part:** ঐ নির্দিষ্ট নেটওয়ার্কের মধ্যে নির্দিষ্ট ডিভাইসটিকে নির্দেশ করে (বাড়ি নম্বরের মতো)।

| Device | IP Address | Subnet Mask | Network ID | Host ID |
| :--- | :--- | :--- | :--- | :--- |
| **PC-0** | `192.168.1.10/24` | 255.255.255.0 | `192.168.1.0` | `.10` |
| **PC-1** | `192.168.1.20/24` | 255.255.255.0 | `192.168.1.0` | `.20` |
| **PC-2** | `192.168.2.10/24` | 255.255.255.0 | `192.168.2.0` | `.10` |

* **PC-0 এবং PC-1** একই Subnet-এ (`192.168.1.0/24`) আছে, তাই তারা Layer 2 Switch দিয়ে সরাসরি যোগাযোগ করতে পারে।
* **PC-2** ভিন্ন Network-এ (`192.168.2.0/24`) আছে। তাই PC-0 বা PC-1 এর সাথে PC-2 এর যোগাযোগ করাতে হলে একটি **Router (Layer 3 device)** এবং **Default Gateway** প্রয়োজন হবে।

---

## ৫. Private IPv4 vs Public IPv4

IPv4 Address মূলত দুই ধরনের: **Private** এবং **Public**।

### A. Private IPv4 Address (RFC 1918)
Private IP সাধারণত বাসা-বাড়ি, স্কুল, অফিস এবং লোকাল ল্যানে (LAN) বিনামূল্যে ব্যবহৃত হয়। এগুলো সরাসরি ইন্টারনেটে রাউট (Routable) হয় না।

| Class | Private IP Range | সাবনেট মাস্ক | ব্যবহারের ক্ষেত্র |
| :--- | :--- | :--- | :--- |
| **Class A** | `10.0.0.0` – `10.255.255.255` | `255.0.0.0` (`/8`) | বৃহৎ এন্টারপ্রাইজ নেটওয়ার্ক |
| **Class B** | `172.16.0.0` – `172.31.255.255` | `255.240.0.0` (`/12`) | মাঝারি প্রতিষ্ঠান |
| **Class C** | `192.168.0.0` – `192.168.255.255` | `255.255.0.0` (`/16`) | ছোট অফিস ও হোম রাউটার |

> **মনে রাখবে:** `172.` দিয়ে শুরু হলেই Private নয়; দ্বিতীয় Octet অবশ্যই **16 থেকে 31** এর মধ্যে হতে হবে। (যেমন: `172.16.5.1` Private, কিন্তু `172.32.1.1` Public)।

### B. Public IPv4 Address
Public IP ইন্টারনেটে সরাসরি যোগাযোগের জন্য বিশ্বব্যাপী অনন্য (Globally Unique) এবং Routable। এগুলো IANA / ISP থেকে বরাদ্দ নিতে হয়।

---

## ৬. Special IPv4 Addresses

| Address / Range | নাম | উদ্দেশ্য / কাজ |
| :--- | :--- | :--- |
| `127.0.0.1` | **Loopback Address** | নিজের ডিভাইসের নিজস্ব TCP/IP stack ও NIC কার্ড ঠিক আছে কি না তা পরীক্ষা করতে ব্যবহৃত হয় (`ping 127.0.0.1`)। |
| `0.0.0.0` | **Unspecified / Default Route** | ডিভাইস আইপি পাওয়ার আগে নিজের সোর্স হিসেবে ব্যবহার করে অথবা রাউটারে Default Route (`0.0.0.0 0.0.0.0`) নির্দেশ করে। |
| `255.255.255.255` | **Limited Broadcast** | স্থানীয় ব্রডকাস্ট ডোমেইনের সমস্ত হোস্টের উদ্দেশ্যে পাঠানো ব্রডকাস্ট (রাউটার পার হতে পারে না)। |
| `169.254.0.0/16` | **APIPA / Link-Local** | DHCP সার্ভার না পাওয়া গেলে উইন্ডোজ বা অন্যান্য ওএস স্বয়ংক্রিয়ভাবে এই রেঞ্জ থেকে আইপি বরাদ্দ করে। |

---

## 🧪 ৭. Practical Lab — Cisco Packet Tracer

### টপোলজি সেটআপ:
* $1 \times$ **Cisco 2960 Switch**
* $2 \times$ **PC (PC-0 ও PC-1)**
* তারের সংযোগ: **Copper Straight-Through Cable** (PC-0 $\rightarrow$ Switch Port Fa0/1, PC-1 $\rightarrow$ Switch Port Fa0/2)

```
[PC-0: 192.168.1.10] ──── (Fa0/1) [Switch 2960] (Fa0/2) ──── [PC-1: 192.168.1.20]
```

### কনফিগারেশন ধাপসমূহ:

1. **PC-0 Setup:**
   * ক্লিক: `Desktop` $\rightarrow$ `IP Configuration`
   * IP Address: `192.168.1.10`
   * Subnet Mask: `255.255.255.0`
   * Default Gateway: ফাঁকা রাখো (একই সাবনেটের জন্য গেটওয়ে প্রয়োজন নেই)

2. **PC-1 Setup:**
   * ক্লিক: `Desktop` $\rightarrow$ `IP Configuration`
   * IP Address: `192.168.1.20`
   * Subnet Mask: `255.255.255.0`
   * Default Gateway: ফাঁকা রাখো

### টেস্টিং (Ping Test):
PC-0-তে গিয়ে `Command Prompt` ওপেন করে টাইপ করো:
```cmd
ping 192.168.1.20
```

* **ফলাফল:** PC-1 থেকে ৪টি রিপ্লাই (`Reply from 192.168.1.20: bytes=32 time<1ms TTL=128`) পাওয়া যাবে।  
*(নোট: একদম প্রথমবার Ping করার সময় ARP টেবিল খালি থাকার কারণে ১টি প্যাকেট লস্ট বা টাইমআউট হতে পারে, দ্বিতীয়বারে 100% সাকসেস আসবে।)*

---

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** IPv4 Address কত bits-এর?

- **A.** 8 bits
- **B.** 16 bits
- **C.** 32 bits
- **D.** 64 bits

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. 32 bits**

**🧠 কেন:**

IPv4 অ্যাড্রেস মোট 32 বিটের একটি বাইনারি নম্বর, যা ৪টি Octet-এ বিভক্ত থাকে।

</details>

---

**প্রশ্ন ২.** IPv4 Address-এ কয়টি Octet থাকে?

- **A.** 2
- **B.** 4
- **C.** 6
- **D.** 8

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. 4**

**🧠 কেন:**

IPv4-এ ৪টি সেগমেন্ট বা Octet থাকে, যেমন: `192` . `168` . `1` . `10`। প্রতিটি Octet-এ ৮টি করে বিট থাকে।

</details>

---

**প্রশ্ন ৩.** একটি IPv4 Octet-এর সর্বোচ্চ decimal value কত?

- **A.** 128
- **B.** 200
- **C.** 255
- **D.** 256

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. 255**

**🧠 কেন:**

প্রতিটি Octet-এ ৮টি বিট থাকে। সবকয়টি বিট ১ হলে মান হয়:
$$2^7 + 2^6 + 2^5 + 2^4 + 2^3 + 2^2 + 2^1 + 2^0 = 255$$
তাই এর রেঞ্জ ০ থেকে ২৫৫ পর্যন্ত।

</details>

---

**প্রশ্ন ৪.** নিচের কোনটি valid IPv4 Address?

- **A.** 192.168.1.256
- **B.** 192.168.1.10
- **C.** 192.300.1.10
- **D.** 192.168.1

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. 192.168.1.10**

**🧠 কেন:**

অপশন B সম্পূর্ণ সঠিক। A এবং C তে ২৫৫ এর বেশি ভ্যালু (২৫৬ ও ৩০০) রয়েছে, এবং D তে কেবল ৩টি অকটেট আছে।

</details>

---

**প্রশ্ন ৫.** 255.255.255.0 কোনটির উদাহরণ?

- **A.** MAC Address
- **B.** Subnet Mask
- **C.** Port Number
- **D.** DNS Name

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Subnet Mask**

**🧠 কেন:**

`255.255.255.0` একটি স্ট্যান্ডার্ড Class C সাবনেট মাস্ক (CIDR `/24`), যা নেটওয়ার্ক ও হোস্ট অংশ আলাদা করে।

</details>

---

**প্রশ্ন ৬.** 192.168.1.10/24-এর Network Address কোনটি?

- **A.** 192.168.1.10
- **B.** 192.168.1.1
- **C.** 192.168.1.0
- **D.** 192.168.1.255

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. 192.168.1.0**

**🧠 কেন:**

`/24` প্রিফিক্সে প্রথম তিনটি অকটেট নেটওয়ার্কের জন্য নির্ধারিত (`192.168.1`) এবং হোস্টের অংশ শূন্য (`.0`) বসালে নেটওয়ার্ক অ্যাড্রেস `192.168.1.0` পাওয়া যায়।

</details>

---

**প্রশ্ন ৭.** নিচের কোনটি Private IPv4 Address?

- **A.** 8.8.8.8
- **B.** 192.168.1.10
- **C.** 1.1.1.1
- **D.** 200.1.1.1

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. 192.168.1.10**

**🧠 কেন:**

`192.168.0.0 – 192.168.255.255` হলো Class C Private IP রেঞ্জ। বাকিগুলো পাবলিক আইপি (যেমন: 8.8.8.8 গুগলের DNS)।

</details>

---

**প্রশ্ন ৮.** 127.0.0.1 সাধারণত কী বোঝায়?

- **A.** Broadcast
- **B.** Loopback
- **C.** Public DNS
- **D.** Default Gateway

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Loopback**

**🧠 কেন:**

`127.0.0.1` হলো IPv4 Loopback Address, যা নিজের লোকাল পিসির নেটওয়ার্ক প্রোটোকল স্ট্যাক টেস্ট করতে ব্যবহৃত হয়।

</details>

---

**প্রশ্ন ৯.** 192.168.1.10/24 এবং 192.168.1.20/24—এরা কি একই subnet-এ আছে?

- **A.** হ্যাঁ
- **B.** না
- **C.** শুধু Router থাকলে
- **D.** শুধু Public IP হলে

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. হ্যাঁ**

**🧠 কেন:**

উভয়েরই নেটওয়ার্ক প্রিফিক্স `/24` এবং প্রথম তিনটি অকটেট অভিন্ন (`192.168.1.x`), তাই তারা একই সাবনেটের অন্তর্ভুক্ত।

</details>

---

**প্রশ্ন ১০.** একটি PC-এর IP Address 169.254.10.20। এটি কী নির্দেশ করতে পারে?

- **A.** PC অবশ্যই Internet-এ connected
- **B.** PC একটি Class A Private IP পেয়েছে
- **C.** DHCP থেকে IP না পেয়ে PC স্বয়ংক্রিয়ভাবে Link-local (APIPA) Address নিয়েছে
- **D.** PC-এর MAC Address পরিবর্তিত হয়েছে

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. DHCP থেকে IP না পেয়ে PC স্বয়ংক্রিয়ভাবে Link-local (APIPA) Address নিয়েছে**

**🧠 কেন:**

`169.254.x.x` হলো APIPA (Automatic Private IP Addressing) রেঞ্জ। নেটওয়ার্কে DHCP সার্ভার অনুপস্থিত থাকলে বা আইপি দিতে ব্যর্থ হলে কম্পিউটার নিজে নিজে এই অ্যাড্রেস গ্রহণ করে।

</details>

---

## 🏆 Final Summary Sheet

| Topic | Key Concept | Quick Rule |
| :--- | :--- | :--- |
| **IPv4 Size** | 32 bits, 4 Octets | $4 \times 8 = 32\text{ bits}$ |
| **Octet Range** | $0 - 255$ | ২৫৫ এর বেশি কখনো হবে না |
| **Subnet Mask** | Network vs Host Boundary | `/24` মানে $255.255.255.0$ |
| **Private IP Ranges** | Class A: $10.x.x.x$<br>Class B: $172.16.x.x - 172.31.x.x$<br>Class C: $192.168.x.x$ | ল্যানে বিনামূল্যে ব্যবহারযোগ্য, ইন্টারনেটে সরাসরি রাউটেবল নয় |
| **Diagnostic Tools** | `ping`, `ipconfig` | নেটওয়ার্ক সংযোগ ও আইপি চেক করার প্রাথমিক টুলস |

---

# 🔁 এক নজরে লজিক

```
IP address = 32 bit = 4 octet  (192 . 168 . 1 . 10)
                ↓
Subnet mask ঠিক করে: বাঁদিকের কয়টা বিট নেটওয়ার্ক, ডানদিকের কয়টা হোস্ট
                ↓
/24  →  255.255.255.0  →  প্রথম ৩ octet নেটওয়ার্ক, শেষটা হোস্ট
                ↓
নেটওয়ার্ক ঠিকানা = হোস্ট বিট সব 0
ব্রডকাস্ট        = হোস্ট বিট সব 1
মাঝের সব          = ব্যবহারযোগ্য হোস্ট
                ↓
Private (ঘরে ব্যবহার): 10.x / 172.16–31.x / 192.168.x
169.254.x.x  = DHCP পায়নি (APIPA)  ← দেখলেই বোঝো IP সমস্যা
```

# ❌ যেখানে অনেকে আটকায়

| ভুল | আসল কথা |
|---|---|
| `192.168.1.255` সবসময় broadcast | /24-এ হ্যাঁ, কিন্তু /16-এ এটা সাধারণ হোস্ট |
| Private IP ইন্টারনেটে কাজ করে | করে না — NAT ছাড়া বাইরে রাউট হয় না |
| 127.0.0.1 = নিজের IP | না, এটা **loopback** (নিজের মেশিনকে বোঝানোর ঠিকানা) |
| 0.0.0.0 একটা হোস্ট | না, "any/unspecified" বোঝায় |

# ✅ নিজে যাচাই করো

- [ ] ৪টা octet আর প্রতিটার রেঞ্জ বলতে পারি
- [ ] `/24` মানে subnet mask কী, বলতে পারি
- [ ] private IP-র তিনটা রেঞ্জ বলতে পারি
- [ ] `169.254.x.x` দেখলে কী বুঝব, বলতে পারি
- [ ] একটা IP + mask দেখে নেটওয়ার্ক ঠিকানা বের করতে পারি

# 🔮 পরের ধাপ

এখন আসল কাজ — **একটা নেটওয়ার্ককে ভেঙে কয়টা subnet বানানো যায়**, আর প্রতিটায় কত হোস্ট বসবে →
[লেসন ০৫ · Subnetting Basics](05-subnetting-basics.md)

---

> **নেভিগেশন:** [⬅ লেসন ৩](03-mac-ethernet-arp.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৫ ➡](05-subnetting-basics.md)

**এই লেসনের Tags:** `#ipv4` `#subnet-mask` `#private-ip` `#apipa` `#octet` `#loopback`
