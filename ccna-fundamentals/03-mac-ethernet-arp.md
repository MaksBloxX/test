# লেসন ৩ · MAC Address, Ethernet Frame ও ARP

> **নেভিগেশন:** [⬅ লেসন ২](02-osi-tcp-ip.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৪ ➡](04-ipv4-addressing.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| MAC address, Ethernet frame-এর গঠন, ARP কীভাবে IP থেকে MAC বের করে — Layer 2-এর পুরো গল্প | ~৪৫ মিনিট | 🟡 Beginner–Intermediate | নিজে তৈরি (২ PC + ১ Switch) |

**Tags:** `#mac-address` `#ethernet` `#arp` `#frame` `#broadcast` `#layer-2` `#mac-table`

---

> 📌 এই লেসনটা ঠিক পাশের কোর্স **লেসন ০৭ (Switching)**-এর ভিত। Switch কীভাবে MAC টেবিল বানায়, ARP কেন দরকার — সব এখানেই পরিষ্কার হবে।


## ১. MAC Address কী?

### ১. What is a MAC Address?

> **Definition:** A Media Access Control (MAC) address is a physical link-layer address used to identify a network interface card (NIC) on a local network segment.

সহজ বাংলায়: MAC Address হলো নেটওয়ার্ক ইন্টারফেসের একটি স্থায়ী ফিজিক্যাল ঠিকানা, যা Ethernet-এর মতো Local Network Technology-তে ফ্রেম সরাসরি সঠিক ডিভাইসে পৌঁছে দিতে ব্যবহৃত হয়।

#### উদাহরণ:

একটি PC-এর নেটওয়ার্ক কনফিগারেশন:

* **IP Address:** `192.168.1.10` (Logical Address — Layer 3)

* **MAC Address:** `00:1A:2B:3C:4D:5E` (Physical Link-Layer Address — Layer 2)

> **মনে রাখবে:** MAC Address নির্দিষ্ট Network Interface-এর সাথে হার্ডওয়্যার লেভেলে যুক্ত থাকে। একটি ডিভাইসে একাধিক ইন্টারফেস (যেমন: LAN Port ও Wi-Fi) থাকলে প্রতিটির জন্য আলাদা MAC Address থাকবে।

### ২. MAC Address-এর গঠন

একটি আদর্শ Ethernet MAC Address হলো **48 bits** বা **6 bytes**-এর। এটি হেক্সাডেসিমাল (Hexadecimal) ফরম্যাটে লেখা হয়।

**উদাহরণ:** `00:1A:2B:3C:4D:5E`

প্রতিটি জোড়া Hexadecimal ডিজিট ১টি Byte (বা 8 bits) নির্দেশ করে:

| Part | Value (Hex) | Size (Bits) | বিবরণ | 
| ----- | ----- | ----- | ----- | 
| **Byte 1** | `00` | 8 bits | OUI (Vendor Identifier) | 
| **Byte 2** | `1A` | 8 bits | OUI (Vendor Identifier) | 
| **Byte 3** | `2B` | 8 bits | OUI (Vendor Identifier) | 
| **Byte 4** | `3C` | 8 bits | Device Identifier (NIC Specific) | 
| **Byte 5** | `4D` | 8 bits | Device Identifier (NIC Specific) | 
| **Byte 6** | `5E` | 8 bits | Device Identifier (NIC Specific) | 

$$
\text{Total Size} = 6 \times 8 = 48 \text{ bits}
$$

#### OUI বনাম Device Identifier:

* **প্রথম ২৪ বিট (OUI — Organizationally Unique Identifier):** IEEE কর্তৃক নির্মাতা প্রতিষ্ঠানকে (যেমন: Cisco, Intel, Realtek) বরাদ্দ করা ইউনিক কোড।

* **শেষ ২৪ বিট (Device / Vendor Assigned):** নির্মাতা প্রতিষ্ঠান প্রতিটি নেটওয়ার্ক কার্ডের জন্য এই অংশটি পৃথকভাবে নির্ধারণ করে।

### ৩. MAC Address-এর প্রকারভেদ

| Type | অর্থ / উদ্দেশ্য | উদাহরণ | 
| ----- | ----- | ----- | 
| **Unicast** | একটি নির্দিষ্ট ডেস্টিনেশন ইন্টারফেসের জন্য | `00:1A:2B:3C:4D:5E` | 
| **Multicast** | নির্দিষ্ট কোনো সাবস্ক্রাইবড গ্রুপের জন্য | `01:00:5E:00:00:01` | 
| **Broadcast** | লোকাল ব্রডকাস্ট ডোমেইনের সব সচল ডিভাইসের জন্য | `FF:FF:FF:FF:FF:FF` | 

> **Broadcast MAC Address:** `FF:FF:FF:FF:FF:FF`
>
> সব বিট $1$ থাকলে সেটি ব্রডকাস্ট অ্যাড্রেস হয়। ARP Request এই ব্রডকাস্ট ফ্রেম ব্যবহার করেই পাঠানো হয়।

## ২. Ethernet ও Ethernet Frame

### ১. What is Ethernet?

> **Definition:** Ethernet is a widely adopted standard family of wired networking technologies (IEEE 802.3) used for Local Area Networks (LANs).

Ethernet কপার ক্যাবল বা ফাইবার অপটিক ক্যাবল এবং সুইচের মাধ্যমে পিসি, সার্ভার ও রাউটারকে লোকাল নেটওয়ার্কে যুক্ত করে।

```
PC0 ─────── [Layer 2 Switch] ─────── PC1

```

### ২. Ethernet Frame Structure

Ethernet-এ ডেটা স্থানান্তরের Layer 2 PDU-কে **Ethernet Frame** বলা হয়।

#### Standard Ethernet II Frame Format:

| Field | Size | কাজ / বিবরণ | 
| ----- | ----- | ----- | 
| **Preamble** | 7 Bytes | রিসিভারের সাথে ক্লক ও বিট সিনক্রোনাইজেশন | 
| **SFD (Start Frame Delimiter)** | 1 Byte | ফ্রেমের মূল বডির শুরু নির্দেশ করে (`10101011`) | 
| **Destination MAC** | 6 Bytes | পরবর্তী হপ বা চূড়ান্ত ডেস্টিনেশনের MAC অ্যাড্রেস | 
| **Source MAC** | 6 Bytes | যে ইন্টারফেস ফ্রেম পাঠাচ্ছে তার MAC অ্যাড্রেস | 
| **EtherType / Length** | 2 Bytes | ভেতরে কোন Layer 3 প্রোটোকল আছে (যেমন: `0x0800` = IPv4, `0x0806` = ARP) | 
| **Payload** | 46–1500 Bytes | উচ্চ স্তরের এনক্যাপসুলেটেড ডেটা (যেমন: IP Packet) | 
| **FCS (Frame Check Sequence)** | 4 Bytes | CRC-32 অ্যালগরিদম দিয়ে এরর বা ক্ষতি শনাক্তকরণ | 

```
+-------------------------------------------------------------------------+
| Preamble | SFD | Dest MAC | Source MAC | EtherType | Payload (IP Packet) | FCS |
| (7B)     | (1B)| (6B)     | (6B)       | (2B)      | (46 - 1500 Bytes)   | (4B)|
+-------------------------------------------------------------------------+

```

### ৩. Switch কীভাবে MAC Address শেখে?

সুইচ ফ্রেমের **Source MAC Address** লক্ষ্য করে নিজস্ব **MAC Address Table** আপডেট করে এবং **Destination MAC Address** দেখে ফরওয়ার্ডিং সিদ্ধান্ত নেয়।

```
PC0 [MAC: AAAA] ── (Fa0/1) [ SW1 ] (Fa0/2) ── PC1 [MAC: BBBB]

```

1. **Learning:** পিসি থেকে কোনো ফ্রেম ঢুকলে সুইচ ফ্রেমটির **Source MAC** দেখে এবং পোর্ট নম্বর সহ টেবিলে রেকর্ড করে।

2. **Looking up:** এরপর সুইচ ফ্রেমের **Destination MAC** টেবিলের সাথে মিলিয়ে দেখে:

   * টেবিলে পাওয়া গেলে সরাসরি সংশ্লিষ্ট নির্দিষ্ট পোর্টে পাঠায় (**Forwarding**)।

   * টেবিলে না পাওয়া গেলে ইনকামিং পোর্ট বাদে একই VLAN-এর সব পোর্টে ফ্রেম ছড়িয়ে দেয় (**Flooding**)।

#### MAC Address Table-এর রূপ:

| VLAN | MAC Address | Type | Port | 
| ----- | ----- | ----- | ----- | 
| 1 | `AAAA.AAAA.AAAA` | Dynamic | FastEthernet0/1 | 
| 1 | `BBBB.BBBB.BBBB` | Dynamic | FastEthernet0/2 | 

## ৩. ARP — IP থেকে MAC

### ১. What is ARP?

> **Definition:** Address Resolution Protocol (ARP) resolves and maps a known Layer 3 IPv4 address to an unknown Layer 2 physical MAC address on a local network segment.

একই সাবনেটে কোনো ডিভাইসের IP জানা থাকলে কিন্তু তার MAC Address জানা না থাকলে ARP ব্যবহার করে সেই MAC বের করা হয়।

### ২. ARP কীভাবে ধাপে ধাপে কাজ করে?

```
PC0 [192.168.1.10]                                  PC1 [192.168.1.20]
        |                                                   |
        |--- 1. ARP Cache Check ----------------------------|
        |                                                   |
        |--- 2. ARP Request (Broadcast: FF:FF:FF:FF:FF:FF) ─► (Everyone receives)
        |                                                   |
        |◄── 3. ARP Reply (Unicast to PC0) ─────────────────|
        |                                                   |
        |--- 4. Update ARP Cache & Send Ethernet Frame ────►|

```

* **Step 1 (Cache Check):** PC0 প্রথমে তার লোকাল মেমোরিতে থাকা **ARP Cache** পরীক্ষা করে দেখে ডেস্টিনেশন আইপির MAC সংরক্ষিত আছে কি না।

* **Step 2 (ARP Request):** ক্যাশে না থাকলে PC0 একটি ব্রডকাস্ট ফ্রেম পাঠায়:

  * *"Who has 192.168.1.20? Tell 192.168.1.10"*

  * Destination MAC: `FF:FF:FF:FF:FF:FF`

* **Step 3 (ARP Reply):** সুইচ এই রিকোয়েস্ট সব ডিভাইসে পাঠায়। কেবল PC1 নিজের আইপি চিনতে পেরে সরাসরি PC0-এর MAC ঠিকানায় **Unicast Reply** দেয়:

  * *"192.168.1.20 is at BBBB.BBBB.BBBB"*

* **Step 4 (Cache Update):** PC0 তার ARP Cache-এ এই ম্যাপিং সংরক্ষণ করে এবং মূল ডেটা ফ্রেম তৈরি করে পাঠিয়ে দেয়।

> **Note:** IPv6-এ ARP ব্যবহার করা হয় না; সেখানে বিকল্প হিসেবে **NDP (Neighbor Discovery Protocol)** ব্যবহৃত হয়।

## ৪. MAC Address বনাম IP Address

| Feature | MAC Address | IP Address | 
| ----- | ----- | ----- | 
| **Full Form** | Media Access Control | Internet Protocol | 
| **OSI Layer** | **Layer 2 (Data Link Layer)** | **Layer 3 (Network Layer)** | 
| **Address Nature** | Physical / Hardware Address (স্থায়ী) | Logical / Software Address (পরিবর্তনশীল) | 
| **Size** | 48 bits (6 Bytes) | IPv4: 32 bits (4 Bytes) / IPv6: 128 bits | 
| **Format** | Hexadecimal (`00:1A:2B:3C:4D:5E`) | Dotted Decimal (`192.168.1.10`) | 
| **প্রধান ভূমিকা** | লোকাল লিঙ্কে নোড-টু-নোড ফ্রেম ডেলিভারি | বিভিন্ন নেটওয়ার্কের মাঝে এন্ড-টু-এন্ড প্যাকেট রাউটিং | 
| **Addressing Scope** | লোকাল লিঙ্ক অতিক্রম করতে পারে না | রাউটারের মাধ্যমে গ্লোবালি রাউট হয় | 

> **গুরুত্বপূর্ণ প্যাকেট রাউটিং নিয়ম:**
>
> যখন ট্রাফিক ভিন্ন কোনো নেটওয়ার্কের দিকে যায়, ফ্রেমের **Destination IP** থাকে চূড়ান্ত রিমোট সার্ভারের, কিন্তু **Destination MAC** হয় লোকাল **Default Gateway (Router)**-এর।

## ৫. Packet Tracer Lab

### Topology:

```
PC0 [192.168.1.10] ──── (Fa0/1) [ Switch0 ] (Fa0/2) ──── PC1 [192.168.1.20]

```

### Step-by-Step Execution:

1. **IP Configuration:**

   * **PC0:** IP: `192.168.1.10` | Mask: `255.255.255.0`

   * **PC1:** IP: `192.168.1.20` | Mask: `255.255.255.0`

2. **MAC Address চেক করা (PC0 Command Prompt):**

   ```
   ipconfig /all
   
   ```

   *(Physical Address ফিল্ড থেকে MAC নোট করো)*

3. **প্রাথমিক ARP Cache চেক করা:**

   ```
   arp -a
   
   ```

   *(কোনো এন্ট্রি না থাকার সম্ভাবনা বেশি)*

4. **Ping পাঠানো:**

   ```
   ping 192.168.1.20
   
   ```

   *(ARP রেজোলিউশনের কারণে প্রথম প্যাকেটটি টাইমআউট হতে পারে, পরবর্তীগুলো সফল হবে)*

5. **আপডেটেড ARP Cache দেখা:**

   ```
   arp -a
   
   ```

   *(এখন `192.168.1.20`-এর ফিজিক্যাল MAC অ্যাড্রেস প্রদর্শিত হবে)*

6. **Switch-এ MAC Address Table দেখা (Switch CLI):**

   ```
   enable
   show mac address-table
   
   ```

## ৬. Quick Revision Cheat-Sheet

* **MAC Address Size:** 48 bits (6 Bytes / 12 Hexadecimal Digits)।

* **OUI:** প্রথম ২৪ বিট (নির্মাতা কোম্পানির পরিচিতি)।

* **Ethernet Broadcast MAC:** `FF:FF:FF:FF:FF:FF`।

* **Ethernet Frame PDU:** Layer 2।

* **ARP-এর কাজ:** IPv4 অ্যাড্রেস থেকে MAC অ্যাড্রেস বের করা।

* **ARP Request:** Broadcast (`FF:FF:FF:FF:FF:FF`)।

* **ARP Reply:** Unicast।

* **IPv6-এ ARP-এর বিকল্প:** NDP (Neighbor Discovery Protocol)।

* **রিমোট নেটওয়ার্কের ফ্রেম:** প্রথম ফ্রেমের Destination MAC হয় লোকাল Default Gateway-এর।

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** How many bits are in a typical Ethernet MAC address?

- **A.** 16 bits
- **B.** 32 bits
- **C.** 48 bits
- **D.** 128 bits

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. 48 bits**

**🧠 কেন:**

A typical Ethernet MAC address is 48 bits long, or 6 bytes.

**উদাহরণ:**
```text
MAC Address: 00:1A:2B:3C:4D:5E
```
এখানে ৬টি Hexadecimal Byte রয়েছে:
$$6 \times 8 = 48\text{ bits}$$

> **মনে রাখবে:**
> - **MAC Address:** সাধারণত 48 bits
> - **IPv4 Address:** 32 bits
> - **IPv6 Address:** 128 bits

---

</details>

---

**প্রশ্ন ২.** Which OSI Layer is associated with a MAC address?

- **A.** Physical
- **B.** Data Link
- **C.** Network
- **D.** Transport

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Data Link**

**🧠 কেন:**

A MAC address is a link-layer address used for communication over technologies such as Ethernet. সহজভাবে, MAC Address OSI Model-এর **Layer 2: Data Link Layer**-এর সঙ্গে সম্পর্কিত।

| OSI Layer | Address / Function |
| :--- | :--- |
| **Layer 2 — Data Link** | MAC Address |
| **Layer 3 — Network** | IP Address |
| **Layer 4 — Transport** | TCP/UDP Port |

**Example:**
```text
IP Address:  192.168.1.10
MAC Address: 00:1A:2B:3C:4D:5E
```
IP Address দিয়ে Network-Level Delivery হয়, আর MAC Address Local Link-এ Frame Delivery-তে ব্যবহৃত হয়।

---

</details>

---

**প্রশ্ন ৩.** What is the PDU of the Ethernet Data Link Layer?

- **A.** Segment
- **B.** Packet
- **C.** Frame
- **D.** Bits

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. Frame**

**🧠 কেন:**

An Ethernet frame is the Protocol Data Unit (PDU) of the Data Link Layer.

**OSI Model-এর PDU-গুলো:**

| Layer | PDU |
| :--- | :--- |
| **Application** | Data |
| **Transport** | TCP Segment / UDP Datagram |
| **Network** | Packet |
| **Data Link** | Frame |
| **Physical** | Bits |

> **মনে রাখবে:**
> - Layer 4 $\rightarrow$ Segment / Datagram
> - Layer 3 $\rightarrow$ Packet
> - Layer 2 $\rightarrow$ Frame
> - Layer 1 $\rightarrow$ Bits

**উদাহরণ:** PC যখন Ethernet-এর মাধ্যমে Switch-এ Data পাঠায়, তখন সেটি **Frame** আকারে পাঠানো হয়।

---

</details>

---

**প্রশ্ন ৪.** What is the primary purpose of ARP in IPv4 networks?

- **A.** Find a domain name
- **B.** Discover the MAC address associated with an IPv4 address
- **C.** Assign an IP address automatically
- **D.** Select the best route

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Discover the MAC address associated with an IPv4 address**

**🧠 কেন:**

ARP (Address Resolution Protocol) discovers the MAC address associated with an IPv4 address on the local network.

**ধরো:**
- PC0-এর IP: `192.168.1.10`
- PC1-এর IP: `192.168.1.20`

PC0 যদি PC1-এর MAC Address না জানে, তাহলে ARP Request পাঠায়:
```text
"Who has 192.168.1.20? Tell 192.168.1.10"
```
PC1 Reply দিয়ে নিজের MAC Address জানায়।

| Protocol | কাজ |
| :--- | :--- |
| **ARP** | IPv4 Address থেকে MAC Address খুঁজে বের করা |
| **DNS** | Domain Name Resolve করা |
| **DHCP** | স্বয়ংক্রিয়ভাবে IP Configuration দেওয়া |
| **ICMP** | Network Diagnostic ও Error Reporting |

---

</details>

---

**প্রশ্ন ৫.** How is an ARP Request usually sent on Ethernet?

- **A.** Unicast
- **B.** Broadcast
- **C.** Anycast
- **D.** Multicast only

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Broadcast**

**🧠 কেন:**

An ARP Request is normally sent in an Ethernet broadcast frame.

- **Broadcast MAC Address:** `FF:FF:FF:FF:FF:FF`

PC0 জানতে চায়: *"Who has 192.168.1.20?"*  
যেহেতু PC0 এখনো PC1-এর MAC Address জানে না, তাই একই Layer 2 Broadcast Domain-এর সব Device-এর কাছে Broadcast Request পাঠায়। PC1 নিজের IP Address চিনতে পেরে সাধারণত **Unicast ARP Reply** পাঠায়।

> **মনে রাখবে:**
> - **ARP Request** $\rightarrow$ সাধারণত Broadcast
> - **ARP Reply** $\rightarrow$ সাধারণত Unicast

---

</details>

---

**প্রশ্ন ৬.** How does a switch typically learn MAC addresses?

- **A.** By examining the Source MAC Address of incoming frames
- **B.** By examining only the Destination IP Address
- **C.** By using DNS
- **D.** By assigning an IP address to every device

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. By examining the Source MAC Address of incoming frames**

**🧠 কেন:**

A switch learns MAC addresses by examining the **Source MAC Address** of incoming Ethernet frames and associating each address with the incoming port and VLAN.

**উদাহরণ:**
```text
PC0 ── Fa0/1 ── SW1 ── Fa0/2 ── PC1
```
PC0 থেকে Frame এলে Switch Source MAC Address দেখে শেখে যে PC0-এর MAC Address `Fa0/1` Port-এ পাওয়া যায়।

**MAC Address Table:**
| MAC Address | Port |
| :--- | :--- |
| `AAAA.AAAA.AAAA` | Fa0/1 |
| `BBBB.BBBB.BBBB` | Fa0/2 |

Switch এরপর Destination MAC Address দেখে Frame Forward করে।

**Cisco Command:**
```bash
show mac address-table
```
*এই Command দিয়ে Switch-এর শেখা MAC Address Table দেখতে পারবে।*

> **গুরুত্বপূর্ণ:** Switch MAC Address শেখে **Source MAC** দেখে, Destination MAC দেখে নয়।

---

</details>

---

**প্রশ্ন ৭.** What is the Ethernet broadcast MAC address?

- **A.** `00:00:00:00:00:00`
- **B.** `FF:FF:FF:FF:FF:FF`
- **C.** `192.168.1.255`
- **D.** `127.0.0.1`

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. `FF:FF:FF:FF:FF:FF`**

**🧠 কেন:**

The Ethernet broadcast MAC address is `FF:FF:FF:FF:FF:FF`। এটি একই Layer 2 Broadcast Domain-এর সব Device-এর কাছে Frame পৌঁছানোর জন্য ব্যবহৃত হয়।

**অন্যান্য অপশনগুলো:**
- `192.168.1.255` হলো `192.168.1.0/24` Subnet-এর IPv4 Directed Broadcast Address।
- `127.0.0.1` হলো IPv4 Loopback Address।
- `00:00:00:00:00:00` হলো MAC Address-এর একটি বিশেষ মান (unspecified/unknown); এটি Ethernet Broadcast Address নয়।

> **মনে রাখবে:** Ethernet Broadcast MAC = ছয়টি `FF` Byte (`FF:FF:FF:FF:FF:FF`)।

---

</details>

---

**প্রশ্ন ৮.** If a PC sends an IPv4 packet to a destination on another subnet, which MAC address does it normally use for the first Ethernet frame?

- **A.** The remote PC's MAC address
- **B.** The DNS Server's MAC address
- **C.** The Default Gateway's MAC address
- **D.** The Switch's management MAC address

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. The Default Gateway's MAC address**

**🧠 কেন:**

When a PC sends an IPv4 packet to a destination outside its local subnet, it normally sends the first Ethernet frame to its **Default Gateway's MAC address**.

**উদাহরণ:**
```text
PC0:
IP:      192.168.1.10/24
Gateway: 192.168.1.1

Destination PC:
IP:      192.168.2.20/24 (অন্য Subnet)
```

PC0-এর প্রথম Ethernet Frame-এ থাকবে:
- **Source MAC:** PC0-এর MAC Address
- **Destination MAC:** Default Gateway-এর MAC Address

কিন্তু IP Packet-এর ভেতরে থাকবে:
- **Source IP:** `192.168.1.10`
- **Destination IP:** `192.168.2.20`

Router Packet গ্রহণ করে Routing Table অনুযায়ী পরবর্তী Network-এর দিকে Forward করবে।

> **মনে রাখবে:** Remote Network-এ যাওয়ার সময় IP Packet-এর Destination IP এবং Ethernet Frame-এর Destination MAC Address একই ডিভাইসের হয় না।

---

</details>

---

**প্রশ্ন ৯.** Which protocol is used for address resolution in IPv6 instead of ARP?

- **A.** DHCPv6
- **B.** NDP
- **C.** DNS
- **D.** FTP

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. NDP**

**🧠 কেন:**

IPv6 uses the **Neighbor Discovery Protocol (NDP)** for functions that include neighbor address resolution. NDP, IPv6-এর Internet Control Message Protocol (ICMPv6)-এর Message ব্যবহার করে কাজ করে।

| Protocol | Purpose |
| :--- | :--- |
| **ARP** | IPv4 Address থেকে MAC Address Resolve করা |
| **NDP** | IPv6 Neighbor Discovery ও Address Resolution |
| **DHCPv6** | IPv6 Configuration ও State Assignment |
| **DNS** | Domain Name Resolution |

> **মনে রাখবে:**
> - IPv4 $\rightarrow$ **ARP**
> - IPv6 $\rightarrow$ **NDP**

---

</details>

---

**প্রশ্ন ১০.** Which command on a Cisco switch displays the MAC Address Table?

- **A.** `show ip route`
- **B.** `show vlan brief`
- **C.** `show mac address-table`
- **D.** `show ip interface brief`

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. `show mac address-table`**

**🧠 কেন:**

The command `show mac address-table` displays the MAC addresses learned by a Cisco switch.

```text
Switch> enable
Switch# show mac address-table
```

Output-এ সাধারণত নিচের তথ্যগুলো প্রদর্শিত হয়:
- VLAN
- MAC Address
- Entry Type (Dynamic / Static)
- Interface / Port

| Command | কাজ |
| :--- | :--- |
| `show mac address-table` | Switch-এর MAC Address Table দেখা |
| `show vlan brief` | VLAN ও Port Assignment দেখা |
| `show ip route` | Router-এর Routing Table দেখা |
| `show ip interface brief` | IP Interface Status ও সংক্ষেপ দেখা |

---

</details>

---

## 🎯 Lesson C-এর ৫টি গুরুত্বপূর্ণ বিষয়

1. **MAC Address:** সাধারণ Ethernet MAC Address হলো 48 bits (বা 6 Bytes)।
2. **Ethernet Frame:** Data Link Layer-এর PDU হলো Frame।
3. **ARP:** IPv4 Local Network-এ IP থেকে MAC Address Resolve করতে সাহায্য করে।
4. **Switch Learning:** Switch Incoming Frame-এর **Source MAC Address** দেখে MAC Table শেখে।
5. **Default Gateway:** Destination অন্য Subnet-এ হলে PC প্রথম Ethernet Frame পাঠায় Gateway-এর MAC Address-এ।

---

---

# 🔁 এক নজরে লজিক

```
একই নেটওয়ার্কে ডেটা পাঠাতে দুটো ঠিকানা লাগে:
   IP  → কোথায় যাবে (লজিক্যাল, বদলায়)     [Layer 3]
   MAC → পরের hop কে (ফিজিক্যাল, স্থির)     [Layer 2]

কিন্তু টেবিলে শুধু IP থাকে, MAC থাকে না →
   ARP Request (broadcast) : "192.168.1.20 কার? MAC বলো"
   ARP Reply (unicast)     : "আমার, MAC = 00:1A:2B:3C:4D:5E"
   ↓
Switch সেই MAC টেবিল মনে রাখে → পরেরবার আর broadcast করতে হয় না
```

# ❌ যেখানে অনেকে আটকায়

| ভুল ধারণা | আসল কথা |
|---|---|
| MAC আর IP একই জিনিস | MAC = hardware ঠিকানা (স্থির), IP = logical ঠিকানা (বদলায়) |
| ARP সব নেটওয়ার্কে কাজ করে | ARP শুধু **লোকাল subnet**-এ; দূরের নেটওয়ার্কে গেলে gateway-এর MAC-এ পাঠায় |
| Broadcast MAC কোনো ডিভাইসের | `FF:FF:FF:FF:FF:FF` = সবার জন্য, কারো নিজের না |
| IPv6-তেও ARP আছে | নেই — IPv6-তে **NDP** (Neighbor Discovery) কাজটা করে |

# ✅ নিজে যাচাই করো

- [ ] MAC address ৪৮ বিট কেন, বলতে পারি
- [ ] `arp -a` আর `show mac address-table` — কোনটা কোথায় চালাতে হয়, জানি
- [ ] ভিন্ন subnet-এ ping করলে প্রথম ফ্রেম কার MAC-এ যায়, বলতে পারি
- [ ] Broadcast MAC আর unicast MAC চিনতে পারি

# 🔮 পরের ধাপ

Layer 3-এ ঠিকানাটা আসলে কেমন — IPv4 address, private/public, special address →
[লেসন ০৪ · IPv4 Addressing](04-ipv4-addressing.md)

---

> **নেভিগেশন:** [⬅ লেসন ২](02-osi-tcp-ip.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৪ ➡](04-ipv4-addressing.md)

**এই লেসনের Tags:** `#mac-address` `#ethernet` `#arp` `#frame` `#broadcast` `#mac-table`
