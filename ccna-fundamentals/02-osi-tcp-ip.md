# লেসন ২ · OSI Model ও TCP/IP Model

> **নেভিগেশন:** [⬅ লেসন ১](01-network-basics.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৩ ➡](03-mac-ethernet-arp.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| OSI-র ৭টি লেয়ার, TCP/IP মডেল, PDU ও Encapsulation — কোন ডিভাইস কোন লেয়ারে কাজ করে | ~৫০ মিনিট | 🟢 Beginner | PT Simulation Mode (নিজে তৈরি) |

**Tags:** `#osi` `#tcp-ip` `#encapsulation` `#pdu` `#layer` `#troubleshooting`

---

> 📌 এই লেসনটা মুখস্থ করার নয়, **ছবি মনে রাখার**। লেয়ারের নাম মনে থাকলে troubleshooting-এ "সমস্যা কোন স্তরে" সেটা নিজেই ধরতে পারবে।


## ১. OSI Model পরিচিতি

### ১. What is the OSI Model?

> **Definition:** The Open Systems Interconnection (OSI) Model is a conceptual reference framework developed by ISO that explains how data travels between devices across a network using seven distinct layers.

সহজ বাংলায়: OSI Model হলো একটি আদর্শ তাত্ত্বিক রেফারেন্স ফ্রেমওয়ার্ক। এটি ব্যাখ্যা করে কীভাবে একটি ডিভাইস থেকে অন্য ডিভাইসে ডেটা পাঠানোর সময় ডেটা বিভিন্ন ধাপে প্রক্রিয়াজাত হয়ে অপর প্রান্তে পৌঁছায়।

### ২. The 7 Layers of the OSI Model

OSI মডেলের লেয়ারগুলো নিচ (Layer 1) থেকে উপরে (Layer 7) সাজানো থাকে:

| Layer No. | Layer Name | Main Function / দায়িত্ব | প্রোটোকল / ডিভাইসের উদাহরণ | 
| ----- | ----- | ----- | ----- | 
| **Layer 7** | **Application** | ব্যবহারকারীর জন্য নেটওয়ার্ক সার্ভিস ইন্টারফেস প্রদান | HTTP, HTTPS, DNS, SMTP, FTP, SSH | 
| **Layer 6** | **Presentation** | ডেটা ফরম্যাটিং, এনকোডিং, কম্প্রেশন ও এনক্রিপশন | TLS/SSL, JPEG, ASCII, UTF-8 | 
| **Layer 5** | **Session** | অ্যাপ্লিকেশনের মধ্যে কমিউনিকেশন সেশন স্থাপন ও নিয়ন্ত্রণ | NetBIOS, RPC, Session Management | 
| **Layer 4** | **Transport** | End-to-End ডেটা ট্রান্সফার, সিকোয়েন্সিং ও পোর্ট ম্যানেজমেন্ট | TCP, UDP | 
| **Layer 3** | **Network** | লজিক্যাল অ্যাড্রেসিং (IP) ও নেটওয়ার্ক পাথ নির্ধারণ (Routing) | IPv4, IPv6, ICMP, Routers | 
| **Layer 2** | **Data Link** | ফিজিক্যাল অ্যাড্রেসিং (MAC) ও লোকাল লিঙ্ক ফ্রেম ডেলিভারি | Ethernet, Switch, ARP | 
| **Layer 1** | **Physical** | কাঁচা বিট (Bits) ফিজিক্যাল মিডিয়ামে সিগন্যাল আকারে পাঠানো | Cables (Cat6, Fiber), Hub, Repeaters | 

## ২. প্রতিটি Layer-এর বিস্তারিত আলোচনা

### Layer 7: Application Layer

* **কাজ:** ব্যবহারকারীর অ্যাপ্লিকেশন সফটওয়্যারকে সরাসরি নেটওয়ার্ক সার্ভিস ব্যবহার করার সুযোগ দেয়।

* **মূল প্রোটোকল:**

  * **HTTP / HTTPS (Port 80/443):** ওয়েব ব্রাউজিং

  * **DNS (Port 53):** ডোমেন নেম থেকে আইপিতে রূপান্তর

  * **DHCP (Port 67/68):** স্বয়ংক্রিয় আইপি বরাদ্দ

  * **SMTP (Port 25):** ইমেইল পাঠানো

### Layer 6: Presentation Layer

* **কাজ:** ডেটার রূপ (Syntax & Semantics) নির্ধারণ করে।

  1. **Translation:** ডেটা ফরম্যাট কনভার্সন (যেমন ASCII থেকে UTF-8)।

  2. **Encryption / Decryption:** ডেটার নিরাপত্তা নিশ্চিত করা (যেমন TLS/SSL)।

  3. **Compression:** ব্যান্ডউইথ সাশ্রয়ে ডেটার সাইজ ছোট করা।

### Layer 5: Session Layer

* **কাজ:** দুটি ডিভাইসের অ্যাপ্লিকেশনের মধ্যে যোগাযোগ স্থাপন (Establish), সচল রাখা (Maintain), চেকপয়েন্ট সিঙ্ক্রোনাইজেশন এবং সংযোগ বিচ্ছিন্ন (Terminate) করা।

### Layer 4: Transport Layer

* **কাজ:** প্রসেস-টু-প্রসেস (Process-to-Process) বা এন্ড-টু-এন্ড যোগাযোগ সম্পন্ন করা। ডেটাকে ছোট ছোট অংশে বিভক্ত (Segmentation) করে পোর্ট নাম্বারের মাধ্যমে সঠিক অ্যাপ্লিকেশনে পৌঁছে দেয়।

#### TCP vs UDP তুলনা:

| Feature | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) | 
| ----- | ----- | ----- | 
| **Connection Type** | Connection-Oriented (3-Way Handshake) | Connectionless | 
| **Reliability** | গ্যারান্টিযুক্ত (Ack ও Retransmission আছে) | গ্যারান্টি নেই (Best-effort delivery) | 
| **Data Ordering** | ক্রমানুসারে পৌঁছায় (Sequencing) | কোনো সিকোয়েন্সিং নেই | 
| **Speed / Overhead** | ধীরগতির ও তুলনামূলক বেশি হেডার ওভারহেড | দ্রুতগতির ও অত্যন্ত হালকা | 
| **ব্যবহারের ক্ষেত্র** | Web (HTTP/HTTPS), File Transfer (FTP), Mail | Video Streaming, VoIP, DNS Queries | 

#### গুরুত্বপূর্ণ Well-Known Port Numbers:

* `20/21`: FTP

* `22`: SSH

* `23`: Telnet

* `25`: SMTP

* `53`: DNS

* `67/68`: DHCP

* `80`: HTTP

* `443`: HTTPS

### Layer 3: Network Layer

* **কাজ:** হোস্ট-টু-হোস্ট (Host-to-Host) ডেলিভারি, লজিক্যাল অ্যাড্রেসিং এবং সেরা রুট নির্ধারণ (Path Determination)।

* **PDU:** **Packet**

* **ডিভাইস:** **Router**, Layer 3 Switch

* **অ্যাড্রেস:** IP Address (IPv4: 32-bit, IPv6: 128-bit)

### Layer 2: Data Link Layer

* **কাজ:** একই লোকাল নেটওয়ার্কে নোড-টু-নোড (Hop-to-Hop) ফ্রেম ডেলিভারি এবং এরর ডিটেকশন (FCS/CRC)।

* **PDU:** **Frame**

* **ডিভাইস:** **Layer 2 Switch**, Bridge, NIC

* **অ্যাড্রেস:** ফিজিক্যাল MAC Address (48-bit / 6-byte)

### Layer 1: Physical Layer

* **কাজ:** বাইনারি ডেটা বা বিট (Bits)-কে ইলেকট্রিক্যাল, অপটিক্যাল বা রেডিও তরঙ্গে রূপান্তর করে ফিজিক্যাল মিডিয়ামে ট্রান্সমিট করা।

* **PDU:** **Bits**

* **উপাদান:** কপার ক্যাবল (Cat5e/Cat6), অপটিক্যাল ফাইবার, কানেক্টর (RJ45), ওয়্যারলেস অ্যান্টেনা।

## ৩. PDU ও Encapsulation / Decapsulation

নেটওয়ার্কের প্রতিটি লেয়ারের ডেটা ইউনিটকে **Protocol Data Unit (PDU)** বলে।

| Layer | PDU Name | 
| ----- | ----- | 
| **Layers 7, 6, 5** | Data / Payload | 
| **Layer 4** | Segment (TCP) / Datagram (UDP) | 
| **Layer 3** | Packet | 
| **Layer 2** | Frame | 
| **Layer 1** | Bits | 

### ডেটা প্রবাহের রূপান্তর:

```
Sender (Encapsulation: Top-Down)            Receiver (Decapsulation: Bottom-Up)
[ Application Data ]                   ───► [ Application Data ]
         ↓                                              ↑
[ L4 Header | Data ] (Segment)         ───► [ L4 Header | Data ]
         ↓                                              ↑
[ L3 Header | L4 Header | Data ] (Packet) ─►[ L3 Header | L4 Header | Data ]
         ↓                                              ↑
[ L2 Frame Header | Packet | FCS ] (Frame) ─►[ L2 Frame Header | Packet | FCS ]
         ↓                                              ↑
1 0 1 1 0 0 1 0 1 1 0 (Bits)            ───► 1 0 1 1 0 0 1 0 1 1 0 (Bits)

```

* **Encapsulation:** ডেটা যখন উপরের লেয়ার থেকে নিচে নামে এবং প্রতিটি লেয়ার তার নিজস্ব হেডার যুক্ত করে।

* **Decapsulation:** রিসিভার ডিভাইসে বিটগুলো গ্রহণ করে নিচ থেকে উপরে উঠার সময় প্রতিটি লেয়ার সংশ্লিষ্ট হেডার খুলে ফেলে।

## ৪. TCP/IP Model (DoD Model)

বাস্তব ইন্টারনেটে OSI মডেলের বদলে ব্যবহারিক **TCP/IP Model** ব্যবহৃত হয়।

### ৪-লেয়ার TCP/IP মডেলের বিবরণ:

| Layer No. | Layer Name | মূল কাজ | প্রোটোকলের উদাহরণ | 
| ----- | ----- | ----- | ----- | 
| **Layer 4** | **Application** | ব্যবহারকারীর নেটওয়ার্ক সার্ভিস নিয়ন্ত্রণ | HTTP, HTTPS, DNS, DHCP, SSH | 
| **Layer 3** | **Transport** | এন্ড-টু-এন্ড নির্ভরযোগ্য বা অনির্ভরযোগ্য ট্রান্সপোর্ট | TCP, UDP | 
| **Layer 2** | **Internet** | আইপি অ্যাড্রেসিং এবং প্যাকেটের রুট নির্ধারণ | IPv4, IPv6, ICMP, ARP | 
| **Layer 1** | **Network Access** | লোকাল লিঙ্ক ডেলিভারি এবং ফিজিক্যাল ট্রান্সমিশন | Ethernet, Wi-Fi, PPP | 

## ৫. OSI Model বনাম TCP/IP Model ম্যাপিং

```
OSI Reference Model (7 Layers)          TCP/IP Protocol Model (4 Layers)
┌─────────────────────────┐
│ 7. Application          │
├─────────────────────────┼───────►  4. Application Layer
│ 6. Presentation         │
├─────────────────────────┤
│ 5. Session              │
├─────────────────────────┼───────►  3. Transport Layer
│ 4. Transport            │
├─────────────────────────┼───────►  2. Internet Layer
│ 3. Network              │
├─────────────────────────┼───────►  1. Network Access Layer
│ 2. Data Link            │          (Link / Network Interface Layer)
├─────────────────────────┤
│ 1. Physical             │
└─────────────────────────┘

```

## ৬. বাস্তব উদাহরণ — ওয়েব ব্রাউজিং কীভাবে ঘটে?

ব্রাউজারে `https://example.com` টাইপ করলে নিচের প্রক্রিয়াগুলো ঘটে:

1. **DNS Query (Layer 7):** ব্রাউজার DNS সার্ভারকে অনুরোধ পাঠায় `example.com`-এর আইপি অ্যাড্রেস পাওয়ার জন্য।

2. **TCP 3-Way Handshake (Layer 4):** ব্রাউজার ওয়েব সার্ভারের পোর্ট 443-এর সঙ্গে সিনক্রোনাইজেশন করে কানেকশন খোলে (`SYN` → `SYN-ACK` → `ACK`)।

3. **TLS Encryption (Layer 6/Application):** HTTPS নিরাপত্তার জন্য TLS হ্যান্ডশেক সম্পন্ন হয়।

4. **IP Packetization & Routing (Layer 3):** ডেটা প্যাকেট আকারে তৈরি হয় এবং রাউটারগুলোর মাধ্যমে সঠিক গন্তব্যে রাউট হয়।

5. **Frame Encapsulation (Layer 2):** প্রতিটি লোকাল লিঙ্কে পরবর্তী হপের MAC অ্যাড্রেস বসিয়ে ফ্রেম তৈরি করা হয়।

6. **Physical Signal Transmission (Layer 1):** ফ্রেমটি ফিজিক্যাল মিডিয়ামে আলোক বা ইলেকট্রিক্যাল বিট পালস হিসেবে পরিবাহিত হয়।

7. **Server Processing & Reply:** সার্ভার প্যাকেটটি ডিক্যাপসুলেট করে প্রসেস করে এবং ওয়েব পেজের ডেটা রিটার্ন পাঠায়।

## ৭. Packet Tracer Simulation

### টপোলজি ও কনফিগারেশন:

```
PC0 [192.168.1.10/24] ───── Switch0 ───── PC1 [192.168.1.20/24]

```

### Simulation Mode-এ পর্যবেক্ষণ:

1. Packet Tracer-এর ডান পাশের নিচে **Simulation Mode** (Shift+S) অন করো।

2. **Edit Filters**-এ গিয়ে কেবল `ICMP` এবং `ARP` সিলেক্ট করো।

3. PC0 এর Command Prompt থেকে কমান্ড দাও:

   ```
   ping 192.168.1.20
   
   ```

4. **Capture / Forward** বাটনে ক্লিক করে দেখো:

   * প্রথমে PC1-এর MAC অ্যাড্রেস জানার জন্য কীভাবে একটি **ARP Broadcast** সুইচের মাধ্যমে যায়।

   * ARP রিপ্লাই পাওয়ার পর কীভাবে **ICMP Unicast Packet** তৈরি হয় এবং সফলভাবে পৌঁছায়।

## ৮. শর্টকাট ও কুইক রিভিশন

### OSI লেয়ার ক্রমানুসারে মনে রাখার টেকনিক:

* **Top to Bottom (7 to 1):** **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing

* **Bottom to Top (1 to 7):** **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** How many layers are in the OSI Model?

- **A.** 4
- **B.** 5
- **C.** 7
- **D.** 8

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. 7**

**🧠 কেন:**

The Open Systems Interconnection (OSI) Model has **seven** distinct layers that describe how network communication functions:

| Layer No. | Layer Name | 
| ----- | ----- | 
| **7** | Application | 
| **6** | Presentation | 
| **5** | Session | 
| **4** | Transport | 
| **3** | Network | 
| **2** | Data Link | 
| **1** | Physical | 

> **Key Rule:** OSI = **7 Layers**, TCP/IP = সাধারণত **4 Layers** (প্রচলিত মডেল)।

</details>

---

**প্রশ্ন ২.** Which OSI Layer is responsible for routing?

- **A.** Physical
- **B.** Data Link
- **C.** Network
- **D.** Transport

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. Network**

**🧠 কেন:**

**Network Layer (Layer 3)** লজিক্যাল অ্যাড্রেসিং (IP Addressing) এবং বিভিন্ন নেটওয়ার্কের মধ্যে প্যাকেট রাউটিং করার দায়িত্ব পালন করে।

```
Network A (192.168.1.0/24)          Network B (192.168.2.0/24)
           PC0                                 PC1
             \                                 /
              +------------ [Router] ---------+

```

Router সাধারণত Layer 3-এ কাজ করে এবং IP Address ব্যবহার করে প্যাকেট এক নেটওয়ার্ক থেকে অন্য নেটওয়ার্কে ফরোয়ার্ড করে।

> **Quick Summary:**
>
> * Layer 2 = MAC Address (Local Link)
>
> * Layer 3 = IP Address & Path Routing

</details>

---

**প্রশ্ন ৩.** Which device typically operates at Layer 2?

- **A.** Layer 2 Switch
- **B.** Router
- **C.** Repeater
- **D.** Modem

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. Layer 2 Switch**

**🧠 কেন:**

একটি সাধারণ **Layer 2 Switch** তার **MAC Address Table** ব্যবহার করে Ethernet ফ্রেম সুইচ বা ফরোয়ার্ড করে।

```
PC0 ────── [Layer 2 Switch] ────── PC1

```

Switch আগত ফ্রেমের Source MAC অ্যাড্রেস থেকে পোর্ট ম্যাপিং শেখে এবং Destination MAC অ্যাড্রেস অনুসারে সঠিক পোর্টে ফ্রেম পাঠায়।

> **Layer vs Devices:**
>
> * **Layer 1:** Hub, Repeater, Physical Cables
>
> * **Layer 2:** Standard Switch, Bridge, NIC
>
> * **Layer 3:** Router, Multilayer Switch (L3 Switch)

</details>

---

**প্রশ্ন ৪.** Which protocol provides reliable, ordered byte-stream delivery?

- **A.** UDP
- **B.** TCP
- **C.** ARP
- **D.** ICMP

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. TCP**

**🧠 কেন:**

**TCP (Transmission Control Protocol)** হ্যান্ডশেক (Three-Way Handshake), সিকোয়েন্সিং এবং অ্যাকনলেজমেন্ট (ACK) ও রি-ট্রান্সমিশনের মাধ্যমে ডেটার নির্ভরযোগ্য ও ক্রমানুসারে ডেলিভারি নিশ্চিত করে।

#### TCP vs UDP তুলনা:

| Feature | TCP | UDP | 
| ----- | ----- | ----- | 
| **Delivery Guarantee** | Reliable (Ack & Retransmission) | Unreliable (Best-effort delivery) | 
| **Data Stream** | Ordered Byte Stream | Independent Datagrams | 
| **Connection Type** | Connection-Oriented | Connectionless | 
| **Protocol Overhead** | তুলনামূলক বেশি (20-60 bytes) | তুলনামূলক কম (8 bytes) | 
| **Example Use** | Web (HTTP/HTTPS), Email, FTP | DNS Query, Streaming, VoIP | 

> **Key Rule:** TCP = **Reliable, Ordered Byte Stream**।

</details>

---

**প্রশ্ন ৫.** What is the PDU of the Data Link Layer?

- **A.** Bits
- **B.** Segment
- **C.** Packet
- **D.** Frame

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: D. Frame**

**🧠 কেন:**

OSI মডেলের বিভিন্ন লেয়ারে ডেটার একক বা **Protocol Data Unit (PDU)** ভিন্ন নামে পরিচিত:

| Layer No. | OSI Layer | PDU Name | 
| ----- | ----- | ----- | 
| **7, 6, 5** | Application, Presentation, Session | **Data / Payload** | 
| **4** | Transport | **Segment** (TCP) / **Datagram** (UDP) | 
| **3** | Network | **Packet** | 
| **2** | Data Link | **Frame** | 
| **1** | Physical | **Bits** | 

```
Application Data ──► Segment (L4) ──► Packet (L3) ──► Frame (L2) ──► Bits (L1)

```

</details>

---

**প্রশ্ন ৬.** Which TCP/IP Layer corresponds to the OSI Application, Presentation, and Session Layers?

- **A.** Internet
- **B.** Transport
- **C.** Application
- **D.** Network Access

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. Application**

**🧠 কেন:**

প্রচলিত ৪-লেয়ারবিশিষ্ট TCP/IP মডেলে OSI মডেলের উপরের ৩টি লেয়ারের (Application, Presentation ও Session) কাজ এককভাবে **Application Layer**-এর অধীনে পরিচালিত হয়।

#### Layer Mapping:

| OSI Model (7 Layers) | TCP/IP Model (4 Layers) | 
| ----- | ----- | 
| **Application (L7)** | **Application** | 
| **Presentation (L6)** | **Application** | 
| **Session (L5)** | **Application** | 
| **Transport (L4)** | **Transport** | 
| **Network (L3)** | **Internet** | 
| **Data Link (L2)** | **Network Access** | 
| **Physical (L1)** | **Network Access** |

</details>

---

**প্রশ্ন ৭.** Which address is associated with the OSI Network Layer?

- **A.** MAC Address
- **B.** IP Address
- **C.** Port Number
- **D.** Hostname

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. IP Address**

**🧠 কেন:**

**IP Address (IPv4 / IPv6)** হলো একটি লজিক্যাল অ্যাড্রেস, যা OSI Network Layer (Layer 3)-এর সাথে সম্পর্কিত এবং ভিন্ন নেটওয়ার্কের মধ্যে এন্ড-টু-এন্ড কমিউনিকেশনে ব্যবহৃত হয়।

| Address Type | সংশ্লিষ্ট লেয়ার | ব্যবহারগত ক্ষেত্র | 
| ----- | ----- | ----- | 
| **MAC Address** | **Layer 2** | লোকাল নেটওয়ার্কে ফ্রেম ডেলিভারি | 
| **IP Address** | **Layer 3** | গ্লোবাল/লজিক্যাল নেটওয়ার্ক রাউটিং | 
| **Port Number** | **Layer 4** | নির্দিষ্ট অ্যাপ্লিকেশন প্রসেস শনাক্তকরণ | 
| **Hostname / URL** | **Layer 7** | মানুষের পাঠযোগ্য ডোমেন নাম |

</details>

---

**প্রশ্ন ৮.** What is Encapsulation?

- **A.** Deleting a Network
- **B.** Adding Protocol Information as Data Moves Down the Stack
- **C.** Assigning a MAC Address
- **D.** Turning Off a Router

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Adding Protocol Information as Data Moves Down the Stack**

**🧠 কেন:**

**Encapsulation** হলো এমন একটি প্রক্রিয়া যেখানে ডেটা উপরের লেয়ার থেকে নিচে নামার সময় প্রতিটি লেয়ার তার নিজস্ব হেডার (এবং Layer 2-এ ট্রেলার) যুক্ত করে।

```
Application Data
      ↓
[TCP Header] + [Data]                    (Segment)
      ↓
[IP Header] + [TCP Segment]              (Packet)
      ↓
[Frame Header] + [IP Packet] + [FCS]     (Frame)
      ↓
0100101010011000101010100101010          (Bits over medium)

```

> **বিপরীত প্রক্রিয়া:** রিসিভিং ডিভাইসে নিচ থেকে উপরে উঠার সময় হেডার রিমুভ করাকে **Decapsulation** বলে।

</details>

---

**প্রশ্ন ৯.** Which protocol is commonly used to resolve domain names?

- **A.** DNS
- **B.** DHCP
- **C.** FTP
- **D.** SSH

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. DNS**

**🧠 কেন:**

**DNS (Domain Name System)** মানুষের পাঠযোগ্য ডোমেন নামকে (যেমন `example.com`) মেশিনের ব্যবহারযোগ্য আইপি অ্যাড্রেসে (যেমন `93.184.216.34`) রূপান্তর করে।

| Protocol | পূর্ণরূপ | প্রধান কাজ | 
| ----- | ----- | ----- | 
| **DNS** | Domain Name System | Hostname থেকে IP Address Resolution | 
| **DHCP** | Dynamic Host Configuration Protocol | ক্লায়েন্টকে অটোমেটিক IP, Subnet Mask, Gateway প্রদান | 
| **FTP** | File Transfer Protocol | নেটওয়ার্কে ফাইল আদান-প্রদান | 
| **SSH** | Secure Shell | সুরক্ষিত ও এনক্রিপ্টেড রিমোট সিএলআই অ্যাক্সেস |

</details>

---

**প্রশ্ন ১০.** Which OSI Layer transmits raw bits over a physical medium?

- **A.** Application
- **B.** Network
- **C.** Data Link
- **D.** Physical

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: D. Physical**

**🧠 কেন:**

**Physical Layer (Layer 1)** ডেটাকে বৈদ্যুতিক ভোল্টেজ, অপটিক্যাল লাইট পালস অথবা ওয়্যারলেস রেডিও সিগন্যালে রূপান্তর করে কাঁচা বিট (Bits: 0 ও 1) আকারে ফিজিক্যাল মিডিয়ামে ট্রান্সমিট করে।

* **Physical Layer Components:** Cat6 কপার কেবল, ফাইবার অপটিক, RJ45 কানেক্টর, ওয়্যারলেস অ্যান্টেনা, এনকোডিং এবং ভোল্টেজ স্ট্যান্ডার্ড।

</details>

---

## 📌 পরীক্ষার আগে মনে রাখার মতো ৭টি মূল বিষয়:

1. **OSI Model:** ৭টি তাত্ত্বিক লেয়ার নিয়ে গঠিত।

2. **TCP/IP Model:** আধুনিক ইন্টারনেটে ব্যবহৃত ৪টি ব্যবহারিক লেয়ার নিয়ে গঠিত।

3. **Layer 2 (Data Link):** MAC Address এবং Ethernet Frame নিয়ে কাজ করে।

4. **Layer 3 (Network):** IP Address এবং Routing নিয়ে কাজ করে।

5. **Layer 4 (Transport):** TCP (Reliable) এবং UDP (Fast/Connectionless) প্রোটোকল পরিচালনা করে।

6. **Encapsulation:** ডেটা টপ-ডাউন যাওয়ার সময় হেডার যোগ হওয়া; **Decapsulation** হলো রিসিভারে হেডার খোলা।

7. **DNS বনাম DHCP:** DNS নামকে আইপিতে রূপান্তর করে; DHCP স্বয়ংক্রিয়ভাবে আইপি অ্যাড্রেস বরাদ্দ দেয়।

---

---

# 🔁 এক নজরে লজিক

```
উপরের দিক (৭–৫)  = অ্যাপ্লিকেশন যা চায়
মাঝের (৪)        = ভাগ করে পাঠানো, নির্ভরযোগ্যতা (TCP/UDP)
নিচের (৩–১)      = পথ ঠিক করা, ফ্রেম বানানো, বিট পাঠানো

Encapsulation:  Data → Segment → Packet → Frame → Bits
                                                        ↓
কোন সমস্যা হলে ওই লেয়ার থেকেই শুরু করো —
"কেবল লাগানো? (1) → MAC/switch? (2) → IP/ping? (3) → পোর্ট? (4) → সেবা? (7)"
```

# ✅ নিজে যাচাই করো

- [ ] ৭টা লেয়ারের নাম ক্রমে বলতে পারি (APSTNDP)
- [ ] কোন লেয়ারে IP, কোন লেয়ারে MAC — বলতে পারি
- [ ] Segment / Packet / Frame — কোনটা কোন লেয়ারের PDU, জানি
- [ ] TCP আর UDP-র পার্থক্য এক লাইনে বলতে পারি
- [ ] PT-তে একটা ping-এর প্রতিটা লেয়ার ধরে ধরে দেখাতে পারি

# 🔮 পরের ধাপ

OSI-র Layer 2-এ **কী দিয়ে ডিভাইস চেনা হয়** — MAC address, Ethernet frame আর ARP →
[লেসন ০৩ · MAC, Ethernet ও ARP](03-mac-ethernet-arp.md)

---

> **নেভিগেশন:** [⬅ লেসন ১](01-network-basics.md) · [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ৩ ➡](03-mac-ethernet-arp.md)

**এই লেসনের Tags:** `#osi` `#tcp-ip` `#encapsulation` `#pdu` `#layer-2` `#layer-3`
