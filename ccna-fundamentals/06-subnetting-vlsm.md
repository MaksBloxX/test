# লেসন ৬ · Subnetting Practice — VLSM ও ভিন্ন Host চাহিদা

> 🌐 **English:** [Read this guide in English](../en/ccna-fundamentals/06-subnetting-vlsm.md) · [English track index](../en/README.md)

> **নেভিগেশন:** [⬅ লেসন ৫](05-subnetting-basics.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৭ ➡](07-acl-nat.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| VLSM দিয়ে ভিন্ন ভিন্ন হোস্ট চাহিদা অনুযায়ী subnet বণ্টন — বড় থেকে ছোট ক্রমে | ~৫০ মিনিট | 🟠 Intermediate | নিজে তৈরি (কাগজ + PT-এ যাচাই) |

**Tags:** `#vlsm` `#subnetting` `#host-requirement` `#cidr` `#address-planning` `#summarization`

---

### 🖼️ চিত্রে বোঝো: চাহিদা অনুযায়ী VLSM IP ভাগ

![চাহিদা অনুযায়ী VLSM IP ভাগ — ১০০, ৫০, ২০, ২ হোস্টের জন্য যথাক্রমে `/25`, `/26`, `/27`, `/30` ব্লক বরাদ্দ।](../assets/diagrams/ccna-06-vlsm-plan.svg)

> **ছবির সারকথা:** ১০০, ৫০, ২০, ২ হোস্টের জন্য যথাক্রমে `/25`, `/26`, `/27`, `/30` ব্লক বরাদ্দ।

---

> 📌 VLSM-এর একটাই নিয়ম মনে রাখো: **সবচেয়ে বড় চাহিদা আগে**। বড় subnet আগে বসালে ঠিকানা নষ্ট হয় না, আর ব্লকগুলো পাশাপাশি বসে যায়।


## ১. What Is Subnetting?

### Definition
**Subnetting** is the process of dividing a larger IP network into smaller logical networks called subnets.

> **বাংলায়:** একটি বড় Network Block-কে একাধিক ছোট ছোট যৌক্তিক নেটওয়ার্কে (Subnet) ভাগ করার প্রক্রিয়াকে Subnetting বলে।

### বাস্তব উদাহরণ
ধরো, একটি প্রতিষ্ঠানে তিনটি আলাদা বিভাগ আছে:
* **CSE Department:** 50 Hosts
* **EEE Department:** 25 Hosts
* **Administration:** 10 Hosts

সব ডিভাইসকে একটি একক ব্রডকাস্ট ডোমেইনে (`192.168.1.0/24`) না রেখে প্রতিটি বিভাগের জন্য আলাদা Subnet তৈরি করা হয়:

```
                  Main Network
                 192.168.1.0/24
                       |
        +--------------+--------------+
        |              |              |
     CSE Lab        EEE Lab         Admin
    (50 Hosts)     (25 Hosts)     (10 Hosts)
```

**সুবিধা:**
1. Broadcast ট্রাফিক সীমাবদ্ধ রাখা যায় (Network Performance বৃদ্ধি পায়)।
2. Security ও Access Control প্রয়োগ করা সহজ হয়।
3. আইপি অ্যাড্রেসের অপচয় রোধ হয়।

> **মনে রাখবে:** এখানে **Host** বলতে PC, Server, Router Interface, Printer বা যেকোনো আইপি ব্যবহারকারী ডিভাইসকে বোঝায়।

---

## ২. Understand the Basic Formula

Subnetting-এর সবচেয়ে গুরুত্বপূর্ণ হিসাব হলো: একটি Subnet-এ কতগুলো Host বিট ($h$) লাগবে।

### Formula: Usable Host Calculation
$$2^h - 2 \ge \text{Required Hosts}$$

* $h$ = Host Bits সংখ্যা
* $2^h$ = ঐ ব্লকের মোট IP সংখ্যা (Total Addresses)
* $-2$ = Network Address এবং Broadcast Address বাদ দেওয়ার পর ব্যবহারযোগ্য IP

### কেন $2$ বাদ দেওয়া হয়?
প্রতিটি সাধারণ IPv4 Subnet-এ:
1. **প্রথম Address ($h=0$):** Network Address হিসেবে সাবনেটকে চিহ্নিত করতে ব্যবহৃত হয়।
2. **সর্বশেষ Address ($h=1$):** Directed Broadcast Address হিসেবে সাবনেটের সবাইকে বার্তা পাঠাতে ব্যবহৃত হয়।
3. তাই Host-এর জন্য বরাদ্দযোগ্য IP সংখ্যা হয়:
   $$\boxed{2^h - 2}$$

### Host Capacity Reference Table

| Host Bits ($h$) | Total Addresses ($2^h$) | Usable Hosts ($2^h - 2$) | CIDR Prefix ($32 - h$) | Subnet Mask |
| :---: | :---: | :---: | :---: | :--- |
| **2** | 4 | 2 | `/30` | 255.255.255.252 |
| **3** | 8 | 6 | `/29` | 255.255.255.248 |
| **4** | 16 | 14 | `/28` | 255.255.255.240 |
| **5** | 32 | 30 | `/27` | 255.255.255.224 |
| **6** | 64 | 62 | `/26` | 255.255.255.192 |
| **7** | 128 | 126 | `/25` | 255.255.255.128 |
| **8** | 256 | 254 | `/24` | 255.255.255.0 |

> 💡 **বাংলা টিপ:** Host Bits ($h$) যত বাড়বে, একটি সাবনেটে হোস্ট সংখ্যা তত বাড়বে। উল্টোভাবে, Prefix যত বড় হবে (যেমন `/30`), হোস্টের সংখ্যা তত কমবে।

---

## ৩. How to Choose a Subnet Mask

ধরা যাক, তোমার একটি নেটওয়ার্কে **50টি Host** প্রয়োজন।

### ধাপসমূহ:
1. **সূত্র প্রয়োগ:**
   $$2^h - 2 \ge 50$$
2. **মান পরীক্ষা:**
   * $h = 5 \implies 2^5 - 2 = 32 - 2 = 30$ (❌ ৫০-এর জন্য যথেষ্ট নয়)
   * $h = 6 \implies 2^6 - 2 = 64 - 2 = 62$ (✅ ৫০-এর জন্য যথেষ্ট)
3. **Prefix নির্ণয়:**
   $$\text{Prefix} = 32 - h = 32 - 6 = \mathbf{/26}$$
4. **Subnet Mask বের করা:**
   * `/26` = প্রথম ২৬টি বিট `1` এবং শেষ ৬টি বিট `0`
   * Binary: `11111111.11111111.11111111.11000000`
   * Decimal: `255.255.255.192`

### Final Summary Table:
| Parameter | Value |
| :--- | :--- |
| **Required Hosts** | 50 |
| **Host Bits ($h$)** | 6 |
| **Total Addresses** | 64 |
| **Usable Hosts** | 62 |
| **CIDR Notation** | `/26` |
| **Subnet Mask** | `255.255.255.192` |

---

## ৪. What Is VLSM?

### Definition
**VLSM (Variable Length Subnet Mask)** allows a network designer to divide an IP address space into subnets of different sizes according to the individual host requirements of each network segment.

> **বাংলায়:** প্রতিটি সাবনেটের প্রয়োজনীয় হোস্ট সংখ্যার ওপর ভিত্তি করে ভিন্ন ভিন্ন সাইজের সাবনেট মাস্ক (যেমন `/25`, `/26`, `/30`) ব্যবহার করার কৌশলকে VLSM বলে।

### কেন VLSM জরুরি?
ধরা যাক একটি নেটওয়ার্কে:
* CSE Lab: 100 Hosts
* EEE Lab: 50 Hosts
* Office: 20 Hosts
* Router Point-to-Point Link: 2 Hosts

যদি সবার জন্য ফিক্সড `/25` (১২৬ হোস্ট) ব্যবহার করা হতো, তবে রাউটার লিংকের জন্য ১২৪টি আইপি অপচয় হতো! VLSM ব্যবহারে রাউটার লিংকের জন্য ঠিক `/30` (২ হোস্ট) দেওয়া যায়, ফলে আইপির অপচয় সর্বনিম্ন হয়।

---

## ৫. VLSM Solving Rules (The CCNA Gold Standard)

CCNA পরীক্ষায় VLSM সমস্যা সমাধানের ৩টি প্রধান ধাপ:

```
[ধাপ ১: হোস্ট রিকোয়ারমেন্ট তালিকাভুক্ত করা]
                   ↓
[ধাপ ২: বড় থেকে ছোট ক্রমে সাজানো (Descending Order)]
                   ↓
[ধাপ ৩: প্রতিটি ব্লকের জন্য সঠিক Prefix ও সাবনেট সীমানা বের করা]
```

### কেন বড় থেকে ছোট সাজাতে হবে?
সবচেয়ে বড় সাবনেট আগে বসালে মেমোরি বা অ্যাড্রেস স্পেস প্রাকৃতিক ব্লকে (যেমন ১২৮, ৬৪, ৩২) সুন্দরভাবে বিভক্ত হয় এবং সাবনেট ওভারল্যাপ (Overlap) হওয়ার ঝুঁকি থাকে না।

---

## ৬. Complete VLSM Example

**Given Major Network:** `192.168.1.0/24`

### Requirements (Sorted from Largest to Smallest):
1. **CSE Lab:** 100 Hosts
2. **EEE Lab:** 50 Hosts
3. **Office:** 20 Hosts
4. **Router Link:** 2 Hosts

---

### Step-by-Step Allocation:

#### 1. CSE Lab (100 Hosts)
* $2^h - 2 \ge 100 \implies h = 7$ ($2^7 - 2 = 126 \ge 100$)
* Prefix: $32 - 7 = \mathbf{/25}$ (Block size = 128)
* **Network Address:** `192.168.1.0/25`
* **Subnet Mask:** `255.255.255.128`
* **First Usable IP:** `192.168.1.1`
* **Last Usable IP:** `192.168.1.126`
* **Broadcast Address:** `192.168.1.127`

#### 2. EEE Lab (50 Hosts)
* পরবর্তী অব্যবহৃত আইপি শুরু: `192.168.1.128`
* $2^h - 2 \ge 50 \implies h = 6$ ($2^6 - 2 = 62 \ge 50$)
* Prefix: $32 - 6 = \mathbf{/26}$ (Block size = 64)
* **Network Address:** `192.168.1.128/26`
* **Subnet Mask:** `255.255.255.192`
* **First Usable IP:** `192.168.1.129`
* **Last Usable IP:** `192.168.1.190`
* **Broadcast Address:** `192.168.1.191`

#### 3. Office (20 Hosts)
* পরবর্তী অব্যবহৃত আইপি শুরু: `192.168.1.192`
* $2^h - 2 \ge 20 \implies h = 5$ ($2^5 - 2 = 30 \ge 20$)
* Prefix: $32 - 5 = \mathbf{/27}$ (Block size = 32)
* **Network Address:** `192.168.1.192/27`
* **Subnet Mask:** `255.255.255.224`
* **First Usable IP:** `192.168.1.193`
* **Last Usable IP:** `192.168.1.222`
* **Broadcast Address:** `192.168.1.223`

#### 4. Router Link (2 Hosts)
* পরবর্তী অব্যবহৃত আইপি শুরু: `192.168.1.224`
* $2^h - 2 \ge 2 \implies h = 2$ ($2^2 - 2 = 2 \ge 2$)
* Prefix: $32 - 2 = \mathbf{/30}$ (Block size = 4)
* **Network Address:** `192.168.1.224/30`
* **Subnet Mask:** `255.255.255.252`
* **First Usable IP:** `192.168.1.225`
* **Last Usable IP:** `192.168.1.226`
* **Broadcast Address:** `192.168.1.227`

---

### Master VLSM Table

| Subnet Name | Needed | Prefix | Network ID | Subnet Mask | First Usable | Last Usable | Broadcast |
| :--- | :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| **CSE Lab** | 100 | `/25` | `192.168.1.0` | `255.255.255.128` | `192.168.1.1` | `192.168.1.126` | `192.168.1.127` |
| **EEE Lab** | 50 | `/26` | `192.168.1.128` | `255.255.255.192` | `192.168.1.129` | `192.168.1.190` | `192.168.1.191` |
| **Office** | 20 | `/27` | `192.168.1.192` | `255.255.255.224` | `192.168.1.193` | `192.168.1.222` | `192.168.1.223` |
| **WAN Link** | 2 | `/30` | `192.168.1.224` | `255.255.255.252` | `192.168.1.225` | `192.168.1.226` | `192.168.1.227` |

* **Unassigned IP Space:** `192.168.1.228` থেকে `192.168.1.255` (ভবিষ্যত সম্প্রসারণের জন্য খালি রাখা হয়েছে)।

---

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

নিচের scenario টা কাগজে লিখে **আগে নিজে সমাধান করো** — তারপর ▸ চেপে ধাপে ধাপে সমাধানের সাথে মিলাও।

> **Scenario:** `192.168.10.0/24` কে ভাগ করতে হবে — **CSE = 60 host**, **EEE = 25 host**, **Office = 10 host**।

**প্রশ্ন ১.** কোন Department-এর জন্য আগে subnet বরাদ্দ করবে?

<details>
<summary>✅ <b>ধাপে ধাপে সমাধান দেখো</b></summary>

* **উত্তর:** **CSE Department**
* **কারণ:** VLSM-এর নিয়ম হলো সর্বদা সবচেয়ে বড় হোস্ট রিকোয়ারমেন্ট আগে বরাদ্দ করতে হয় ($60 > 25 > 10$)।

</details>

---

**প্রশ্ন ২.** CSE-এর 60 Hosts-এর জন্য কোন CIDR Prefix প্রয়োজন?

<details>
<summary>✅ <b>ধাপে ধাপে সমাধান দেখো</b></summary>

* **উত্তর:** **/26**
* **ব্যাখ্যা:** $2^6 - 2 = 62 \ge 60$। হোস্ট বিট $h=6$। প্রিফিক্স $= 32 - 6 = \mathbf{/26}$।

</details>

---

**প্রশ্ন ৩.** EEE-এর 25 Hosts-এর জন্য কোন CIDR Prefix প্রয়োজন?

<details>
<summary>✅ <b>ধাপে ধাপে সমাধান দেখো</b></summary>

* **উত্তর:** **/27**
* **ব্যাখ্যা:** $2^5 - 2 = 30 \ge 25$। হোস্ট বিট $h=5$। প্রিফিক্স $= 32 - 5 = \mathbf{/27}$।

</details>

---

**প্রশ্ন ৪.** Office-এর 10 Hosts-এর জন্য কোন CIDR Prefix প্রয়োজন?

<details>
<summary>✅ <b>ধাপে ধাপে সমাধান দেখো</b></summary>

* **উত্তর:** **/28**
* **ব্যাখ্যা:** $2^4 - 2 = 14 \ge 10$। হোস্ট বিট $h=4$। প্রিফিক্স $= 32 - 4 = \mathbf{/28}$।

</details>

---

**প্রশ্ন ৫.** CSE-এর Network Address, First Usable, Last Usable এবং Broadcast Address কত?

<details>
<summary>✅ <b>ধাপে ধাপে সমাধান দেখো</b></summary>

* **Network Address:** `192.168.10.0/26`
* **First Usable IP:** `192.168.10.1`
* **Last Usable IP:** `192.168.10.62`
* **Broadcast Address:** `192.168.10.63`

</details>

---

**প্রশ্ন ৬.** EEE-এর Network Address কত হবে, যদি CSE-এর subnet আগে বরাদ্দ করা হয়?

<details>
<summary>✅ <b>ধাপে ধাপে সমাধান দেখো</b></summary>

* **উত্তর:** `192.168.10.64/27`
* **ব্যাখ্যা:** CSE-এর ব্রডকাস্ট অ্যাড্রেস হলো `192.168.10.63`। এর ঠিক পরের আইপি অ্যাড্রেসটিই (`192.168.10.64`) পরবর্তী সাবনেটের Network Address হবে।

</details>

---

**প্রশ্ন ৭.** তিনটি subnet বরাদ্দ করার পর Address Block overlap করছে কি না, কীভাবে যাচাই করবে?

<details>
<summary>✅ <b>ধাপে ধাপে সমাধান দেখো</b></summary>

* **উত্তর:** প্রতিটি সাবনেটের পরিসীমা (Network Address থেকে Broadcast Address পর্যন্ত) পাশাপাশি রেখে পরীক্ষা করতে হবে:
  * **CSE:** `192.168.10.0` – `192.168.10.63` (মোট ৬৪টি আইপি)
  * **EEE:** `192.168.10.64` – `192.168.10.95` (মোট ৩২টি আইপি)
  * **Office:** `192.168.10.96` – `192.168.10.111` (মোট ১৬টি আইপি)
  * **ফলাফল:** কোনো সাবনেটের শেষের অ্যাড্রেস পরের সাবনেটের শুরুর অ্যাড্রেসকে অতিক্রম বা স্পর্শ করেনি; প্রতিটি ব্লক আলাদা ও সুরক্ষিত।

---

</details>

---

## 🎯 Lesson E Summary Sheet

| Concept | Key Point to Remember | Formula / Rule |
| :--- | :--- | :--- |
| **Subnetting** | বড় নেটওয়ার্ককে ছোট লজিক্যাল ভাগে ভাগ করা | Performance & Security বৃদ্ধি |
| **Host Formula** | মোট হোস্ট থেকে ২ বাদ দিতে হয় | $2^h - 2 \ge \text{Hosts}$ |
| **VLSM Rule** | সাজাও: Largest $\rightarrow$ Smallest | আইপি অপচয় রোধের সর্বোত্তম পদ্ধতি |
| **Block Size** | প্রতিটি সাবনেটের মোট আইপি সংখ্যা | $2^h$ (যেমন: /26 এর ব্লক সাইজ ৬৪) |
| **Next Network** | পূর্বের Broadcast Address + 1 | $\text{Next Network} = \text{Prev Broadcast} + 1$ |

---

# 🔁 এক নজরে লজিক

```
ধাপ ১: চাহিদা বড় → ছোট সাজাও   (60 > 25 > 10)
ধাপ ২: প্রতিটার জন্য h বের করো  2^h − 2 ≥ host
ধাপ ৩: prefix = 32 − h
ধাপ ৪: ব্লক সাইজ ধরে ধরে পরপর বসাও, আগের broadcast-এর পরের ঠিকানা থেকে শুরু
ধাপ ৫: শেষে যাচাই — কোনো ব্লক overlap করছে কি না
```

> ⚠️ **সবচেয়ে বড় ভুল:** ছোট subnet আগে বসানো → পরে বড় subnet-এর জায়গা থাকে না, গোটা ব্লক নষ্ট হয়।

# ✅ নিজে যাচাই করো

- [ ] চাহিদা দেখে `/26` না `/27` লাগবে — বের করতে পারি
- [ ] VLSM-এ কেন বড় আগে, বলতে পারি
- [ ] পরপর ব্লক বসিয়ে overlap হচ্ছে কি না যাচাই করতে পারি
- [ ] একটা /24 কে ৩টা ভিন্ন সাইজের subnet-এ ভাগ করতে পারি

# 🔮 পরের ধাপ

এখন তত্ত্ব শেষ। এবার **ট্রাফিক নিয়ন্ত্রণ ও ঠিকানা রূপান্তর** — ACL দিয়ে কে কোথায় যাবে ঠিক করা, NAT দিয়ে private IP-কে বাইরে পাঠানো →
[লেসন ০৭ · ACL ও NAT](07-acl-nat.md)

---

> **নেভিগেশন:** [⬅ লেসন ৫](05-subnetting-basics.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৭ ➡](07-acl-nat.md)

**এই লেসনের Tags:** `#vlsm` `#subnetting` `#host-requirement` `#address-plan` `#cidr`
