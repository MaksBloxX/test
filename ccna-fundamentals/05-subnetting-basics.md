# লেসন ৫ · Subnetting Basics — Subnet Mask থেকে /26

> 🌐 **English:** [Read this guide in English](../en/ccna-fundamentals/05-subnetting-basics.md) · [English track index](../en/README.md)

> **নেভিগেশন:** [⬅ লেসন ৪](04-ipv4-addressing.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৬ ➡](06-subnetting-vlsm.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| Subnet mask থেকে subnet ভাগ করা, হোস্ট ও broadcast বের করা — /24 → /26 পর্যন্ত হাতে-কলমে | ~৬০ মিনিট | 🟡 Beginner–Intermediate | নিজে তৈরি (কাগজ + PT-তে যাচাই) |

**Tags:** `#subnetting` `#subnet-mask` `#cidr` `#network-address` `#broadcast` `#block-size`

---

### 🖼️ চিত্রে বোঝো: একটি `/24` থেকে চারটি `/26`

![একটি `/24` থেকে চারটি `/26` — প্রতি ব্লকে ৬৪টি ঠিকানা; প্রথমটি Network, শেষটি Broadcast, মাঝের ৬২টি Host।](../assets/diagrams/ccna-05-subnet-26.svg)

> **ছবির সারকথা:** প্রতি ব্লকে ৬৪টি ঠিকানা; প্রথমটি Network, শেষটি Broadcast, মাঝের ৬২টি Host।

---

> 📌 Subnetting = **মুখস্থ নয়, পদ্ধতি**। নিচের ৩টা ধাপ বারবার করো — "কয়টা বিট ধার নিলাম? ব্লক সাইজ কত? নেটওয়ার্ক ঠিকানা কত?" — উত্তর নিজে থেকেই বের হবে।


## ১. IP Address কী?

### Definition

> **An IP address** is a logical address assigned to a device on a network to identify it and enable communication.

সহজভাবে, Network-এ প্রতিটি ডিভাইসকে আলাদাভাবে শনাক্ত করতে IP Address ব্যবহার করা হয়।

### Example: Device Addressing

| Device | IP Address | 
| ----- | ----- | 
| **PC0** | `192.168.1.10` | 
| **PC1** | `192.168.1.20` | 
| **PC2** | `192.168.1.30` | 
| **Printer** | `192.168.1.40` | 

*এখানে প্রতিটি ডিভাইসের IP Address ইউনিক (আলাদা)।*

### IPv4 Address-এর গঠন

উদাহরণ: `192.168.1.10`

* IPv4 Address-এ মোট **32 bits** থাকে।

* এটি চারটি অংশে বিভক্ত, যেগুলোকে **Octet** বলে।

| Octet 1 | Octet 2 | Octet 3 | Octet 4 | 
| ----- | ----- | ----- | ----- | 
| `192` | `168` | `1` | `10` | 
| 8 bits | 8 bits | 8 bits | 8 bits | 

> 💡 **মনে রাখবে:**
>
> * $1 \text{ Octet} = 8 \text{ bits}$
>
> * $4 \text{ Octets} = 32 \text{ bits}$
>
> * প্রতিটি Octet-এর ডেসিমাল মান $0$ থেকে $255$ পর্যন্ত হতে পারে ($2^8 = 256$ টি মান)।

## ২. Subnet Mask কী?

### Definition

> **A subnet mask** separates the network portion of an IP address from the host portion.

সহজভাবে, Subnet Mask বুঝতে সাহায্য করে একটি IP Address-এর কোন অংশ Network-এর জন্য এবং কোন অংশ নির্দিষ্ট Host-এর জন্য বরাদ্দ।

### Example

* **IP Address:** `192.168.1.10`

* **Subnet Mask:** `255.255.255.0`

* **CIDR Notation:** `/24`

এখানে `/24` মানে প্রথম ২৪টি bit হলো Network Portion এবং বাকি ৮টি bit হলো Host Portion:

```
Network Portion (24 bits)        Host Portion (8 bits)
─────────────────────────        ─────────────────────
       192.168.1                          .10

```

এই IP Address-এর **Network Address** হলো:

$$
\text{Network Address: } 192.168.1.0/24
$$

> ⚠️ **Important:** `192.168.1.10` হলো নির্দিষ্ট একটি Host IP, কিন্তু `192.168.1.0` হলো সম্পূর্ণ সাবনেটের Network Address (যা কোনো একক হোস্টে বসানো যায় না)।

### Common Subnet Masks Reference

| CIDR | Subnet Mask | Host Bits ($h$) | Usable Hosts ($2^h - 2$) | 
| ----- | ----- | ----- | ----- | 
| **/24** | `255.255.255.0` | 8 | 254 | 
| **/25** | `255.255.255.128` | 7 | 126 | 
| **/26** | `255.255.255.192` | 6 | 62 | 
| **/27** | `255.255.255.224` | 5 | 30 | 
| **/28** | `255.255.255.240` | 4 | 14 | 
| **/29** | `255.255.255.248` | 3 | 6 | 
| **/30** | `255.255.255.252` | 2 | 2 | 

*এগুলো CCNA সাবনেটিং ও রাউটার পয়েন্ট-টু-পয়েন্ট লিঙ্কের জন্য অতিপ্রয়োজনীয় মান।*

## ৩. Network, Host ও Broadcast Address

ধরো একটি আইপি অ্যাড্রেস দেওয়া হলো: `192.168.1.10/24`

এই সাবনেটের গুরুত্বপূর্ণ অ্যাড্রেসসমূহ:

| Type | Address | বিবরণ | 
| ----- | ----- | ----- | 
| **Network Address** | `192.168.1.0` | সাবনেটের নিজস্ব পরিচয় (প্রথম অ্যাড্রেস) | 
| **First Usable Host** | `192.168.1.1` | প্রথম ডিভাইসে ব্যবহারযোগ্য আইপি | 
| **Last Usable Host** | `192.168.1.254` | শেষ ডিভাইসে ব্যবহারযোগ্য আইপি | 
| **Broadcast Address** | `192.168.1.255` | সাবনেটের সব ডিভাইসে মেসেজ পাঠানোর আইপি | 

### কেন 254 usable hosts?

`/24`-এ Host Portion-এ $8\text{ bits}$ থাকে ($32 - 24 = 8$)।

$$
\text{Total Addresses} = 2^h
$$

$$
\text{Usable Hosts} = 2^h - 2
$$

এখানে $h = 8$:

$$
2^8 - 2 = 256 - 2 = 254
$$

> 📌 **নোট:** Network Address এবং Broadcast Address কখনোই হোস্ট ডিভাইসে (PC, Server, Printer) অ্যাসাইন করা যায় না। তাই সর্বদা $2$ বিয়োগ করতে হয়।

## ৪. Subnetting কী?

### Definition

> **Subnetting** is the process of dividing a larger network into smaller logical networks called subnets.

সহজ কথায়, একটি বড় Network-কে ভেঙে কয়েকটি ছোট লজিক্যাল নেটওয়ার্কে ভাগ করার প্রক্রিয়াকেই **Subnetting** বলে।

### Example

তোমার কাছে একটি নেটওয়ার্ক আছে: `192.168.1.0/24`। তুমি এটিকে দুটি সমান সাবনেটে ভাগ করতে চাও:

| Subnet | Network Address | Usable Host Range | Broadcast Address | 
| ----- | ----- | ----- | ----- | 
| **Subnet 1** | `192.168.1.0/25` | `192.168.1.1` – `192.168.1.126` | `192.168.1.127` | 
| **Subnet 2** | `192.168.1.128/25` | `192.168.1.129` – `192.168.1.254` | `192.168.1.255` | 

* **আগে:** একটি `/24` নেটওয়ার্কে ২৫৪টি usable host ছিল।

* **এখন:** দুটি `/25` সাবনেট পাওয়া গেল, প্রতিটিতে ১২৬টি করে usable host রয়েছে।

> 💡 **নিয়ম:** সাবনেট সংখ্যা ($2^n$) যত বাড়ে, প্রতিটি সাবনেটে ব্যবহারযোগ্য হোস্টের সংখ্যা ($2^h - 2$) তত কমে যায়।

## ৫. Subnetting-এর Shortcut Formula

### Formula 1: Number of Subnets

$$
\text{Number of Subnets} = 2^n
$$


*(এখানে* $n$ *হলো Network Portion-এর জন্য Host Portion থেকে ধার নেওয়া bit-এর সংখ্যা)*

### Formula 2: Usable Hosts Per Subnet

$$
\text{Usable Hosts} = 2^h - 2
$$


*(এখানে* $h$ *হলো Host Portion-এ অবশিষ্ট থাকা bit-এর সংখ্যা)*

### Example Walkthrough: /24 থেকে /26

* বেস প্রিফিক্স: `/24`, নতুন প্রিফিক্স: `/26`

* ধার নেওয়া বিট ($n$):
  

  $$
  26 - 24 = 2
  $$

* মোট সাবনেট সংখ্যা:
  

  $$
  2^n = 2^2 = 4
  $$

* অবশিষ্ট হোস্ট বিট ($h$):
  

  $$
  32 - 26 = 6
  $$

* প্রতিটি সাবনেটে ব্যবহারযোগ্য হোস্ট:
  

  $$
  2^h - 2 = 2^6 - 2 = 64 - 2 = 62
  $$

👉 অর্থাৎ, একটি `/24` নেটওয়ার্ককে `/26` করলে **৪টি সাবনেট** তৈরি হবে এবং প্রতিটিতে **৬২টি** করে ব্যবহারযোগ্য আইপি থাকবে।

## ৬. Practical Example: /24 থেকে /26

* **মূল নেটওয়ার্ক:** `192.168.1.0/24`

* **টার্গেট:** `/26`

* **/26-এর Subnet Mask:** `255.255.255.192`

### Block Size (Magic Number) বের করার নিয়ম:

$$
\text{Block Size} = 256 - \text{Interesting Octet Value}
$$

$$
256 - 192 = 64
$$

তাই প্রতিটি সাবনেট শুরু হবে প্রতি **৬৪** ব্যবধান পর পর:

| Subnet | Network Address | First Host | Last Host | Broadcast Address | 
| ----- | ----- | ----- | ----- | ----- | 
| **1** | `192.168.1.0/26` | `.1` | `.62` | `192.168.1.63` | 
| **2** | `192.168.1.64/26` | `.65` | `.126` | `192.168.1.127` | 
| **3** | `192.168.1.128/26` | `.129` | `.190` | `192.168.1.191` | 
| **4** | `192.168.1.192/26` | `.193` | `.254` | `192.168.1.255` | 

```
Network Address Progression (Block Size = 64):
0 ──────────► 64 ──────────► 128 ──────────► 192

```

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** IPv4 Address কত Bit-এর?

- **A.** 8 bits
- **B.** 16 bits
- **C.** 32 bits
- **D.** 64 bits

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. 32 bits**

**🧠 কেন:**

IPv4 Address মোট **32 bits**-এর হয়। এটি ৪টি Octet-এ বিভক্ত এবং প্রতিটি Octet-এ ৮টি করে bit থাকে।

**উদাহরণ:**

```
IP Address: 192.168.1.10

  192     .    168    .     1     .    10
 8 bits       8 bits      8 bits      8 bits

Total = 8 + 8 + 8 + 8 = 32 bits

```

> 💡 **মনে রাখবে:**
>
> * $\text{IPv4} = 32\text{ bits}$ (4 Octets)
>
> * $\text{IPv6} = 128\text{ bits}$ (16 Octets / 8 Heptets)

</details>

---

**প্রশ্ন ২.** /24-এর Subnet Mask কোনটি?

- **A.** 255.0.0.0
- **B.** 255.255.0.0
- **C.** 255.255.255.0
- **D.** 255.255.255.128

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. 255.255.255.0**

**🧠 কেন:**

`/24` মানে প্রথম ২৪টি bit Network Portion-এর জন্য অন ($1$) রাখা হয়েছে।

**Binary Representation:**

```
11111111 . 11111111 . 11111111 . 00000000

```

প্রতিটি Octet-এর Decimal মান:

* $11111111_2 = 255_{10}$

* $00000000_2 = 0_{10}$

তাই:

* **CIDR:** `/24`

* **Subnet Mask:** `255.255.255.0`

#### 📌 Shortcut Reference:

| CIDR | Subnet Mask | Class Default | 
| ----- | ----- | ----- | 
| **/8** | `255.0.0.0` | Class A Default | 
| **/16** | `255.255.0.0` | Class B Default | 
| **/24** | `255.255.255.0` | Class C Default |

</details>

---

**প্রশ্ন ৩.** 192.168.1.10/24-এর Network Address কোনটি?

- **A.** 192.168.1.10
- **B.** 192.168.1.0
- **C.** 192.168.1.255
- **D.** 192.168.0.10

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. 192.168.1.0**

**🧠 কেন:**

`/24`-এ প্রথম ৩টি Octet হলো Network Portion এবং শেষ Octet হলো Host Portion:

```
Network Portion (24 bits)        Host Portion (8 bits)
─────────────────────────        ─────────────────────
       192.168.1                          .10

```

Network Address বের করতে Host Portion-এর সব bit শূন্য ($0$) করতে হয়:

* **Host IP:** `192.168.1.10`

* **Network Address:** `192.168.1.0`

* **Broadcast Address:** `192.168.1.255`

</details>

---

**প্রশ্ন ৪.** /26-এ মোট কতটি Usable Host পাওয়া যায়?

- **A.** 30
- **B.** 62
- **C.** 126
- **D.** 254

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. 62**

**🧠 কেন:**

IPv4-এ মোট $32\text{ bits}$ থাকে।

* Host Bits ($h$):
  

  $$
  h = 32 - 26 = 6
  $$

* Usable Hosts বের করার সূত্র:
  

  $$
  \text{Usable Hosts} = 2^h - 2
  $$

  $$
  = 2^6 - 2 = 64 - 2 = 62
  $$

> ⚠️ **কেন** $2$ **বাদ দেওয়া হয়?**
> ১. **Network Address** (সাবনেটের প্রথম অ্যাড্রেস)
> ২. **Broadcast Address** (সাবনেটের শেষ অ্যাড্রেস)
> এই দুটি অ্যাড্রেস কোনো নির্দিষ্ট হোস্টে বসানো যায় না।

</details>

---

**প্রশ্ন ৫.** /24-কে /26 করলে কয়টি Subnet পাওয়া যাবে?

- **A.** 2
- **B.** 4
- **C.** 8
- **D.** 16

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. 4**

**🧠 কেন:**

* পূর্বের Prefix: `/24`

* নতুন Prefix: `/26`

* ধার নেওয়া bit-এর সংখ্যা ($n$):
  

  $$
  n = 26 - 24 = 2
  $$

* সাবনেট সংখ্যা বের করার সূত্র:
  

  $$
  \text{Number of Subnets} = 2^n = 2^2 = 4
  $$

#### সাবনেট চার্ট:

| Subnet No | Network Address | Usable Host Range | Broadcast | 
| ----- | ----- | ----- | ----- | 
| **1** | `192.168.1.0/26` | `.1` – `.62` | `.63` | 
| **2** | `192.168.1.64/26` | `.65` – `.126` | `.127` | 
| **3** | `192.168.1.128/26` | `.129` – `.190` | `.191` | 
| **4** | `192.168.1.192/26` | `.193` – `.254` | `.255` |

</details>

---

**প্রশ্ন ৬.** /26-এর Block Size কত?

- **A.** 32
- **B.** 64
- **C.** 128
- **D.** 192

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. 64**

**🧠 কেন:**

`/26`-এর Subnet Mask হলো `255.255.255.192`।

$$
\text{Block Size} = 256 - \text{Relevant Mask Octet}
$$

$$
\text{Block Size} = 256 - 192 = 64
$$

তাই Network Address-গুলো প্রতি **৬৪** ব্যবধানে পরিবর্তিত হয়:

$$
0 \rightarrow 64 \rightarrow 128 \rightarrow 192
$$

</details>

---

**প্রশ্ন ৭.** 192.168.1.128/26-এর Broadcast Address কোনটি?

- **A.** 192.168.1.127
- **B.** 192.168.1.128
- **C.** 192.168.1.190
- **D.** 192.168.1.191

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: D. 192.168.1.191**

**🧠 কেন:**

* বর্তমান Network Address: `192.168.1.128`

* Block Size: $64$

* পরবর্তী Network Address: $128 + 64 = 192$ (`192.168.1.192`)

$$
\text{Broadcast Address} = \text{পরবর্তী Network Address} - 1
$$

$$
192 - 1 = 191
$$

সুতরাং, Broadcast Address হলো `192.168.1.191`।

</details>

---

## 🧠 পরীক্ষার জন্য ৪টি গোল্ডেন ফর্মুলা

| কী বের করবে? | Formula | বর্ণনা | 
| ----- | ----- | ----- | 
| **Host Bits (**$h$**)** | $32 - \text{Prefix}$ | মোট ৩২ বিট থেকে CIDR বিয়োগ | 
| **Usable Hosts** | $2^h - 2$ | প্রতিটি সাবনেটে ব্যবহারযোগ্য আইপি | 
| **Subnet সংখ্যা** | $2^n$ | $n = \text{ধার নেওয়া নেটওয়ার্ক বিট}$ | 
| **Block Size (Magic Number)** | $256 - \text{Relevant Mask Octet}$ | সাবনেটগুলোর পারস্পরিক ব্যবধান | 

## ✍️ প্র্যাকটিস প্রবলেম সমাধান (Self-Test Solution)

### Problem Statement:

> **Network:** `192.168.10.0/24` কে **/27**-এ ভাগ করা হলো।

#### সমাধান ধাপসমূহ:

* মূল প্রিফিক্স = `/24`, নতুন প্রিফিক্স = `/27`

* ধার নেওয়া বিট: $n = 27 - 24 = 3$

* অবশিষ্ট হোস্ট বিট: $h = 32 - 27 = 5$

* **/27 Subnet Mask:** `255.255.255.224` (যেহেতু $128 + 64 + 32 = 224$)

### প্রশ্নগুলোর চূড়ান্ত উত্তর:

1. **কতটি Subnet পাওয়া যাবে?**
   

   $$
   \text{Subnets} = 2^n = 2^3 = \mathbf{8}\text{ টি}
   $$

2. **প্রতিটি Subnet-এ কতটি Usable Host থাকবে?**
   

   $$
   \text{Usable Hosts} = 2^h - 2 = 2^5 - 2 = 32 - 2 = \mathbf{30}\text{ টি}
   $$

3. **Block Size কত?**
   

   $$
   \text{Block Size} = 256 - 224 = \mathbf{32}
   $$

   
   *(সাবনেটগুলো ৩২ ব্যবধানে এগিয়ে যাবে:* $0, 32, 64, 96, 128, 160, 192, 224$*)*

4. **প্রথম Subnet-এর Broadcast Address কী?**

   * প্রথম সাবনেট: `192.168.10.0/27`

   * পরবর্তী সাবনেট: `192.168.10.32/27`

   * ব্রডকাস্ট অ্যাড্রেস $= 32 - 1 =$ **`192.168.10.31`**

5. **দ্বিতীয় Subnet-এর Network Address কী?**

   * প্রথম সাবনেট শুরু $= 0$

   * দ্বিতীয় সাবনেট শুরু $= 0 + 32 =$ **`192.168.10.32/27`**

---

# 🔁 এক নজরে লজিক

```
১. চাহিদা দেখো → কয়টা subnet বা কয়টা host?
২. subnet লাগলে: 2^n ≥ subnet   |   host লাগলে: 2^h − 2 ≥ host
৩. prefix = 32 − h
৪. ব্লক সাইজ = 256 − (শেষ অক্টেটের মান)
৫. ব্লক সাইজ ধরে ধরে গুনো → network address, broadcast, usable range
```

| Prefix | Mask | Block | Usable host |
|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |

# ✅ নিজে যাচাই করো

- [ ] `2^n ≥ subnet` আর `2^h − 2 ≥ host` — কখন কোনটা, বলতে পারি
- [ ] /26-এর mask, block size, usable host — মুখে বলতে পারি
- [ ] `192.168.1.130/26`-এর network ও broadcast বের করতে পারি
- [ ] কাগজে না লিখে মাথায় একটা সহজ subnet বের করতে পারি

# 🔮 পরের ধাপ

সব subnet সমান সাইজের না হলেও হয় — বড় দরকারে বড়, ছোট দরকারে ছোট (VLSM) →
[লেসন ০৬ · Subnetting Practice: VLSM](06-subnetting-vlsm.md)

---

> **নেভিগেশন:** [⬅ লেসন ৪](04-ipv4-addressing.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৬ ➡](06-subnetting-vlsm.md)

**এই লেসনের Tags:** `#subnetting` `#cidr` `#subnet-mask` `#block-size` `#broadcast` `#usable-host`
