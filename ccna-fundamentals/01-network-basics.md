# লেসন ১ · নেটওয়ার্ক কী? টপোলজি, Switch ও Router

> 🌐 **English:** [Read this guide in English](../en/ccna-fundamentals/01-network-basics.md) · [English track index](../en/README.md)

> **নেভিগেশন:** [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ২ ➡](02-osi-tcp-ip.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| নেটওয়ার্ক কী, LAN/WAN, টপোলজি আর Switch ও Router-এর কাজ — একদম বেসিক থেকে পরিষ্কার ধারণা | ~৪০ মিনিট | 🟢 Beginner | নিজে তৈরি (৩ PC + ১ Switch) |

**Tags:** `#network` `#lan` `#wan` `#topology` `#switch` `#router` `#client-server`

---

### 🖼️ চিত্রে বোঝো: LAN ও WAN-এ সুইচ-রাউটারের ভূমিকা

![LAN ও WAN-এ সুইচ-রাউটারের ভূমিকা — একই নেটওয়ার্কে Switch ফ্রেম পাঠায়; ভিন্ন নেটওয়ার্কে Router প্যাকেট পাঠায়।](../assets/diagrams/ccna-01-lan-wan.svg)

> **ছবির সারকথা:** একই নেটওয়ার্কে Switch ফ্রেম পাঠায়; ভিন্ন নেটওয়ার্কে Router প্যাকেট পাঠায়।

---

> 📌 এই লেসনটা কোর্সের **ভিত্তি**। এখানে কোনো কনফিগ নেই — শুধু ধারণা। ধারণা পরিষ্কার থাকলে পরে কমান্ড মুখস্থ করতে হবে না, বুঝে লিখতে পারবে।


## ১. What Is a Computer Network?

### English Definition

> **A computer network** is a group of interconnected devices that communicate and share data or resources with each other.

### বাংলা ব্যাখ্যা

একাধিক Computer, Laptop, Server বা অন্য Network Device যখন একে অপরের সঙ্গে সংযুক্ত হয়ে Data আদান-প্রদান করে, তখন তাকে **Computer Network** বলে।

### Example

ধরো, তোমাদের University Computer Lab-এ ২০টি Computer আছে। সব Computer একটি Switch-এর সঙ্গে যুক্ত।

তখন তারা Network-এর মাধ্যমে:

* File Share করতে পারবে।

* Network Printer ব্যবহার করতে পারবে।

* Server থেকে Data নিতে পারবে।

* Internet ব্যবহার করতে পারবে, যদি Internet Connection থাকে।

### Network Diagram

```
     PC0          PC1
      |            |
      |            |
      +----[SW1]---+
             |
             |
          Server0

```

**এখানে:**

* `PC0` ও `PC1` হলো End Devices।

* `SW1` হলো Switch।

* `Server0` Network Service দিতে পারে।

* Cable-গুলো Device-গুলোর মধ্যে Connection তৈরি করেছে।

> 💡 **মনে রাখবে:** শুধু Cable দিয়ে Computer যুক্ত করলেই সব ধরনের Communication নিশ্চিত হয় না। সঠিক IP Configuration, VLAN ও অন্যান্য Network Settings-ও প্রয়োজন হতে পারে।

## ২. Why Do We Need a Computer Network?

Computer Network ব্যবহারের পাঁচটি গুরুত্বপূর্ণ কারণ আছে:

| Purpose | Explanation | Example | 
| ----- | ----- | ----- | 
| **Resource Sharing** | একই Resource একাধিক User ব্যবহার করতে পারে | Network Printer | 
| **File Sharing** | এক Device থেকে অন্য Device-এ File পাঠানো | University File Server | 
| **Communication** | Device ও User-এর মধ্যে যোগাযোগ | Email, Chat | 
| **Centralized Management** | একটি কেন্দ্র থেকে Data ও Service পরিচালনা | Office Server | 
| **Internet Access** | একাধিক Device Internet ব্যবহার করতে পারে | Home Wi-Fi | 

### Real-Life Example

ধরো, তোমার CSE Department-এ একটি Server আছে। সেখানে শিক্ষার্থীদের Assignment ও Study Materials রাখা হয়।

শিক্ষার্থীরা নিজেদের Computer থেকে সেই Server Access করতে পারে। এতে প্রতিটি শিক্ষার্থীর Computer-এ আলাদাভাবে সব File Copy করে রাখতে হয় না। এটাই Network-এর একটি গুরুত্বপূর্ণ সুবিধা।

## ৩. Types of Computer Networks

এখন চারটি গুরুত্বপূর্ণ Network Type শিখি।

### A. LAN — Local Area Network

#### Definition

> A **Local Area Network (LAN)** connects devices within a limited geographical area, such as a home, office, or computer lab.

#### বাংলা ব্যাখ্যা

LAN হলো ছোট বা সীমিত এলাকার Network। যেমন: একটি বাড়ি, অফিস বা University Computer Lab।

#### Diagram

```
       PC0        PC1
        |          |
        +--[SW1]---+
             |
          Server0

```

#### Examples

* University Computer Lab

* Office Network

* Home Wired Network

#### LAN-এর বৈশিষ্ট্য

* সীমিত এলাকায় ব্যবহৃত হয়।

* Ethernet Cable বা Wireless Connection ব্যবহার করতে পারে।

* সাধারণত প্রতিষ্ঠানের নিজস্ব Network Infrastructure-এর মাধ্যমে পরিচালিত হয়।

* File ও Resource Sharing করা যায়।

> 🛠️ **Practical Example:** তুমি Packet Tracer-এ দুটি PC একটি Switch-এর সঙ্গে যুক্ত করে একই Subnet-এ Ping সফল করলে, সেটি একটি Basic LAN-এর উদাহরণ।

### B. WAN — Wide Area Network

#### Definition

> A **Wide Area Network (WAN)** connects networks across large geographical areas.

#### বাংলা ব্যাখ্যা

WAN বৃহৎ ভৌগোলিক এলাকায় বিভিন্ন Network-কে সংযুক্ত করে।

#### Diagram

```
   Office A LAN                 Office B LAN
        |                            |
     Router A                     Router B
        |                            |
        +--------- WAN --------------+

```

ধরো, একটি Bank-এর ঢাকা, চট্টগ্রাম ও রাজশাহীতে তিনটি Branch আছে। তাদের Network-গুলো WAN Connection-এর মাধ্যমে সংযুক্ত হতে পারে।

#### Examples

* বিভিন্ন শহরের Office Network সংযোগ।

* Branch Office-এর Network।

* Internet হলো বৃহৎ বৈশ্বিক Network of Networks।

#### WAN-এর বৈশিষ্ট্য

* বৃহৎ ভৌগোলিক এলাকা জুড়ে বিস্তৃত।

* বিভিন্ন LAN-কে সংযুক্ত করতে পারে।

* Router ও বিভিন্ন WAN Technology ব্যবহার করা হতে পারে।

* Connection ISP বা অন্য Network Provider-এর মাধ্যমে আসতে পারে।

> 💡 **মনে রাখবে:** WAN মানেই শুধু Satellite Connection নয়। Fiber, Leased Line এবং বিভিন্ন Provider Network-ও WAN সংযোগ দিতে পারে।

### C. MAN — Metropolitan Area Network

#### Definition

> A **Metropolitan Area Network (MAN)** connects networks across a city or metropolitan area.

#### বাংলা ব্যাখ্যা

MAN সাধারণত একটি শহর বা Metropolitan Area-এর মধ্যে বিভিন্ন Network-কে সংযুক্ত করে।

#### Example

ধরো, একটি প্রতিষ্ঠানের একটি শহরের মধ্যে পাঁচটি Office আছে। সেগুলোর Network একটি City-Wide Network-এর মাধ্যমে সংযুক্ত করা হলো। এটি MAN-এর একটি উদাহরণ হতে পারে।

```
     Office A
         |
         |
    City Network
      /     \
     /       \
Office B    Office C

```

> 💡 **মনে রাখবে:** LAN, MAN ও WAN-এর মধ্যে পার্থক্য বোঝার একটি সহজ উপায় হলো তাদের Coverage Area। তবে বাস্তবে এই সীমাগুলো সবসময় কঠোরভাবে নির্ধারিত নয়।

### D. WLAN — Wireless Local Area Network

#### Definition

> A **Wireless Local Area Network (WLAN)** connects devices within a local area using wireless communication, typically Wi-Fi.

#### বাংলা ব্যাখ্যা

WLAN হলো এমন একটি Local Area Network, যেখানে Device-গুলো সাধারণত Wi-Fi-এর মতো Wireless Technology দিয়ে সংযুক্ত হয়।

#### Diagram

```
       Laptop   ))) 
                  \
       Mobile   )) [Wi-Fi AP]
                  /
       PC       )))

```

*(এখানে `)))` Wireless Connection বোঝাচ্ছে)*

#### Examples

* Home Wi-Fi Network

* University Wi-Fi

* Office Wireless Network

#### WLAN-এর বৈশিষ্ট্য

* সাধারণত Wi-Fi ব্যবহার করে।

* Wireless Access Point বা Wireless Router ব্যবহৃত হতে পারে।

* Cable ছাড়াই উপযুক্ত Device Network-এ যুক্ত হতে পারে।

* সঠিক Security Configuration গুরুত্বপূর্ণ।

#### LAN vs WLAN

| Feature | Wired LAN | WLAN | 
| ----- | ----- | ----- | 
| **Connection** | Ethernet Cable | Wireless, সাধারণত Wi-Fi | 
| **Mobility** | Cable-এর সীমাবদ্ধতা আছে | Wireless Coverage-এর মধ্যে চলাচল করা যায় | 
| **Device** | Switch, Ethernet NIC | Access Point, Wireless NIC | 
| **Example** | Computer Lab-এর Wired PC | Campus Wi-Fi | 

> ⭐ **গুরুত্বপূর্ণ:** WLAN-ও LAN-এর একটি ধরন। LAN মানেই Wired Network নয়।

## ৪. LAN vs MAN vs WAN vs WLAN

**এক নজরে পার্থক্য:**

| Feature | LAN | MAN | WAN | WLAN | 
| ----- | ----- | ----- | ----- | ----- | 
| **Full Form** | Local Area Network | Metropolitan Area Network | Wide Area Network | Wireless Local Area Network | 
| **Coverage** | সীমিত এলাকা | শহর বা Metropolitan Area | বৃহৎ ভৌগোলিক এলাকা | স্থানীয় Wireless Coverage | 
| **Example** | Computer Lab | City-Wide Network | Branch Office Network | Home Wi-Fi | 
| **Technology** | Ethernet/Wi-Fi | বিভিন্ন Network Technology | বিভিন্ন WAN Technology | সাধারণত Wi-Fi | 

### Exam Tip 🎯

প্রশ্নে যদি বলা হয়:

* **Computer Lab** $\rightarrow$ LAN

* **Home Wi-Fi** $\rightarrow$ WLAN

* **একটি শহরের বিভিন্ন Office** $\rightarrow$ MAN হতে পারে

* **বিভিন্ন শহরের Branch Office** $\rightarrow$ WAN হতে পারে

*তবে প্রশ্নের সম্পূর্ণ Context পড়ে উত্তর দেবে।*

## ৫. What Is a Network Node?

### Definition

> A **network node** is a device or connection point that can send, receive, or forward information in a network.

### বাংলা ব্যাখ্যা

Network-এর সঙ্গে যুক্ত এমন Device বা Connection Point, যা Data পাঠাতে, গ্রহণ করতে বা Forward করতে পারে, তাকে **Network Node** বলা হয়।

### Examples

* Computer

* Server

* Router

* Switch

* Network Printer

*Network-এর ধরন ও প্রসঙ্গ অনুযায়ী Node-এর ব্যবহার কিছুটা ভিন্ন হতে পারে।*

## ৬. What Is a Host?

### Definition

> A **host** is a network-connected device that can send or receive network communications.

### Examples

* PC0

* PC1

* Server0

* Laptop

* Network-enabled Printer

```
PC0 ───── Switch ───── PC1

```

এখানে `PC0` ও `PC1` হলো Host। Switch মূলত Frame Forward করে, তাই একে সাধারণত End Host বলা হয় না।

### Host vs Network Device

| Host | Network Infrastructure Device | 
| ----- | ----- | 
| Data তৈরি বা গ্রহণ করে | Data Forward বা Network পরিচালনা করতে পারে | 
| PC, Laptop, Server | Switch, Router, Access Point | 
| সাধারণত User Application চালায় | সাধারণত Network Connectivity প্রদান করে | 

## ৭. What Is a Client and a Server?

এটি তোমার আগের DNS ও HTTP Practical-এর সঙ্গে সরাসরি সম্পর্কিত।

### Client

> A **client** is a device or application that requests a service or resource from a server.

**উদাহরণ:**

* PC0 থেকে Website খোলা।

* Browser থেকে Server-এর কাছে HTTP Request পাঠানো।

### Server

> A **server** is a device or application that provides services or resources to clients.

**উদাহরণ:**

* **Web Server:** Website সরবরাহ করে।

* **DNS Server:** Domain Name Resolve করে।

* **DHCP Server:** IP Configuration প্রদান করে।

### Practical Example

```
PC0 (Client)
     |
     | HTTP Request
     v
Server0 (Web Server)
     |
     | HTTP Response
     v
PC0 Browser

```

তুমি যখন Browser-এ লিখো: `http://www.office.local`

তখন PC0-এর Browser Web Server-এর কাছে Request পাঠায়। Server0 সঠিকভাবে Configure থাকলে Webpage পাঠায়।

> ⭐ **গুরুত্বপূর্ণ:** একটি Computer একই সঙ্গে Client এবং Server—দুই ভূমিকাতেই কাজ করতে পারে। ভূমিকা নির্ভর করে সেটি কোন Service ব্যবহার করছে বা প্রদান করছে তার ওপর।

## ৮. Network Topology কী?

### Definition

> **Network topology** describes how network devices and connections are arranged, physically or logically.

### বাংলা ব্যাখ্যা

Network-এ Device-গুলো কীভাবে সংযুক্ত ও সাজানো আছে, সেটাই Network Topology।

**দুটি গুরুত্বপূর্ণ ধারণা:**

1. **Physical Topology:** Cable ও Device বাস্তবে কীভাবে সংযুক্ত।

2. **Logical Topology:** Network-এ Data কীভাবে প্রবাহিত হয় বা Devices কীভাবে যোগাযোগ করে।

### A. Star Topology

সব Device একটি Central Device-এর সঙ্গে যুক্ত থাকে।

```
        PC0
         |
PC1 --- SW1 --- PC2
         |
       Server

```

* **সুবিধা:** Manage করা সহজ; একটি PC-এর Cable নষ্ট হলেও সাধারণত অন্য PC-গুলো কাজ করতে পারে।

* **অসুবিধা:** Central Switch নষ্ট হলে তার সঙ্গে যুক্ত Device-গুলোর Communication ব্যাহত হতে পারে।

* **Practical:** Packet Tracer-এর Switch-কেন্দ্রিক অধিকাংশ Basic LAN মূলত Star Topology-এর উদাহরণ।

### B. Bus Topology

একটি প্রধান Backbone Cable-এর সঙ্গে Device-গুলো যুক্ত থাকে।

```
PC0 ---- PC1 ---- PC2 ---- PC3

```

এটি পুরোনো Ethernet Network-এ ব্যবহৃত হতো। আধুনিক Switched Ethernet LAN-এ এই ধরনের Physical Bus সাধারণত ব্যবহৃত হয় না।

### C. Ring Topology

Device-গুলো একটি বৃত্তাকার পথে যুক্ত থাকে।

```
PC0 ------ PC1
 |          |
 |          |
PC3 ------ PC2

```

কিছু Ring Technology-তে Data নির্দিষ্ট Ring Path দিয়ে চলাচল করে। তবে এই Diagram কেবল ধারণা বোঝানোর জন্য; সব Ring Network একইভাবে কাজ করে না।

### D. Mesh Topology

Device-গুলোর মধ্যে একাধিক Connection থাকে।

```
     R1 -------- R2
       |\        /|
       | \      / |
       |  \    /  |
       |   \  /   |
       |    \/    |
       |    /\    |
       |   /  \   |
       |  /    \  |
       | /      \ |
     R3 -------- R4

```

* **সুবিধা:** Redundant Path থাকে; কোনো একটি Link নষ্ট হলেও বিকল্প Path ব্যবহার করা সম্ভব।

* **অসুবিধা:** Cable, Port ও Configuration বেশি প্রয়োজন হয়; খরচ ও Complexity অনেক বেশি।

### Topology Comparison

| Topology | Structure | Main Advantage | Main Disadvantage | 
| ----- | ----- | ----- | ----- | 
| **Star** | Central Switch | সহজে Manage করা যায় | Central Device Failure-এর প্রভাব | 
| **Bus** | Shared Backbone | ঐতিহাসিকভাবে সহজ | Backbone Failure-এর প্রভাব | 
| **Ring** | Circular Path | নির্দিষ্ট Ring Design-এ সুশৃঙ্খল Traffic Flow | Link/Node Failure-এর প্রভাব Design-এর ওপর নির্ভরশীল | 
| **Mesh** | Multiple Links | Redundancy | বেশি খরচ ও Complexity | 

## Switch কী? (খুব দরকারি ধারণা)

> **Definition:** A network switch is a device that connects multiple devices within a LAN and forwards Ethernet frames based on MAC addresses.

সহজভাবে, **Switch** একই Local Area Network (LAN)-এর PC, Printer ও Server-কে পরস্পরের সঙ্গে সংযুক্ত করে।

### উদাহরণ:
একটি অফিসে বা ল্যাবে:
* `PC0`
* `PC1`
* `PC2`
* `Server`

এই চারটি ডিভাইসকে একটি সাধারণ Layer 2 Switch-এর সঙ্গে ক্যাবল দিয়ে যুক্ত করে একটি লোকাল নেটওয়ার্ক গড়ে তোলা যায়।

---

### Switch কীভাবে কাজ করে?

1. ধরো, `PC0` থেকে `PC1`-এ ডেটা পাঠানো হলো।
2. `PC0` একটি Ethernet Frame পাঠায়।
3. Switch আগত ফ্রেমটি থেকে প্রেরকের **Source MAC Address** লক্ষ্য করে এবং তার নিজস্ব **MAC Address Table**-এ সেটি কোন পোর্টে এসেছে তা লিখে রাখে (Address Learning)।
4. এরপর Switch ফ্রেমটির **Destination MAC Address** পরীক্ষা করে:
   * **জানা থাকলে:** নির্দিষ্ট ডেস্টিনেশন পোর্টে সরাসরি পাঠিয়ে দেয় (Forwarding)।
   * **অজানা থাকলে:** যে পোর্টে এসেছে সেটি বাদে একই VLAN-এর বাকি সকল সচল পোর্টে ফ্রেমটির কপি ছড়িয়ে দেয় (Flooding / Unknown Unicast Flooding)।

> **মনে রাখবে:** Switch সাধারণত OSI Model-এর **Layer 2 (Data Link Layer)**-এ কাজ করে এবং MAC Address ব্যবহার করে ফ্রেম ফরোয়ার্ড করে।

---

## Router কী?

> **Definition:** A router is a network device that forwards IP packets between different networks using routing information.

সহজভাবে, **Router** দুটি বা ততোধিক ভিন্ন নেটওয়ার্ক বা সাবনেটের মধ্যে যোগাযোগ স্থাপন করে।

### উদাহরণ:

```
Network A (LAN 1)              Network B (LAN 2)
192.168.1.0/24                 192.168.2.0/24
      |                              |
     PC0                            PC1
      |                              |
   Switch 0                       Switch 1
      \                              /
       +---------- [Router] --------+
```

`PC0` ও `PC1` দুটি সম্পূর্ণ আলাদা IP Network-এ অবস্থান করছে। সাধারণ Layer 2 Switch কখনো দুটি ভিন্ন সাবনেটের মধ্যে ট্রাফিক পাঠাতে পারে না; এজন্য মাঝখানে একটি **Router** বা Layer 3 Switch থাকা বাধ্যতামূলক।

---

### Switch বনাম Router

| Feature | Switch | Router |
| :--- | :--- | :--- |
| **Main Purpose** | LAN-এর ভেতরের ডিভাইস কানেক্ট করা | বিভিন্ন ভিন্ন নেটওয়ার্ককে সংযুক্ত করা |
| **Addressing Used** | MAC Address | IP Address |
| **Primary OSI Layer** | Layer 2 (Data Link) | Layer 3 (Network) |
| **Data Unit** | Frame | Packet |
| **Domain Scope** | Collision Domain আলাদা করে | Collision ও Broadcast Domain উভয়ই আলাদা করে |
| **Example** | একই VLAN বা ল্যানের PC থেকে PC | এক ডিপার্টমেন্ট বা ব্রাঞ্চ থেকে অন্য ব্রাঞ্চ |

---

## 🧪 ৯. Packet Tracer Practical — Build Your First LAN

### Objective

দুটি PC-কে একটি Switch-এর মাধ্যমে সংযুক্ত করে সফল Ping নিশ্চিত করা।

### Required Devices

* $1 \times$ Cisco 2960 Switch

* $2 \times$ PC

### Topology

```
PC0 ───────── SW1 ───────── PC1

```

### Step 1: Cable Connection

| Device | Port | Connected To | Port | 
| ----- | ----- | ----- | ----- | 
| **PC0** | FastEthernet0 | **SW1** | Fa0/1 | 
| **PC1** | FastEthernet0 | **SW1** | Fa0/2 | 

*(Copper Straight-Through Cable ব্যবহার করো)*

### Step 2: PC0-তে IP Set করো

* Path: `PC0 → Desktop → IP Configuration → Static`

  * **IP Address:** `192.168.1.10`

  * **Subnet Mask:** `255.255.255.0`

  * **Default Gateway:** *Leave Blank*

### Step 3: PC1-তে IP Set করো

* Path: `PC1 → Desktop → IP Configuration → Static`

  * **IP Address:** `192.168.1.20`

  * **Subnet Mask:** `255.255.255.0`

  * **Default Gateway:** *Leave Blank*

*(এখানে Gateway প্রয়োজন নেই, কারণ দুটি PC একই Subnet-এ রয়েছে এবং আমরা শুধু Local Communication পরীক্ষা করছি)*

### Step 4: Ping Test

PC0 থেকে Command Prompt খুলে চালাও:

```
ping 192.168.1.20

```

**Expected Result:**

```
Reply from 192.168.1.20: bytes=32 time<1ms TTL=128

```

*(প্রথম Ping-এ Timeout হলে দ্বিতীয়বার চেষ্টা করো)*

### Step 5: কীভাবে কাজ করছে?

1. PC0 বুঝতে পারে Destination `192.168.1.20` তার নিজের Subnet-এর মধ্যে।

2. PC0 প্রয়োজন হলে ARP ব্যবহার করে PC1-এর MAC Address খুঁজে বের করে।

3. PC0 একটি Ethernet Frame তৈরি করে।

4. Switch Destination MAC Address দেখে Frame Forward করে।

5. PC1 Frame গ্রহণ করে এবং Ping-এর উত্তর পাঠায়।

> এই ছোট Lab-এ তুমি LAN, Host, Switch, IPv4 Address, MAC Address, ARP ও ICMP—বেশ কয়েকটি গুরুত্বপূর্ণ ধারণার ব্যবহার দেখতে পাবে।

---

## ✅ অনুশীলন কুইজ — নিজে চেষ্টা করো

প্রতিটা প্রশ্নের উত্তর **আগে নিজে ভাবো** — কাগজে লিখে ফেলো। তারপর ▸ চেপে উত্তর ও ব্যাখ্যা মিলিয়ে নাও। ভুল হলেও সমস্যা নেই, ভুল থেকেই শেখা হয়।

**প্রশ্ন ১.** What is a LAN?

- **A.** A network that covers a limited geographical area
- **B.** A network that always covers the entire world
- **C.** A device that forwards packets
- **D.** A wireless encryption protocol

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. A network that covers a limited geographical area**

**🧠 কেন:**

LAN (Local Area Network) একটা ছোট এলাকা জুড়ে থাকে — এক বিল্ডিং, অফিস বা ক্যাম্পাস। WAN হলে দেশ/মহাদেশ জুড়ে যেত।

</details>

---

**প্রশ্ন ২.** Which device primarily forwards Ethernet frames using MAC addresses?

- **A.** Router
- **B.** Switch
- **C.** Modem
- **D.** DNS Server

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Switch**

**🧠 কেন:**

Switch **MAC address** দেখে ফ্রেম ফরওয়ার্ড করে, তাই এটা Layer 2-এর ডিভাইস। Router দেখে IP (Layer 3), Hub কোনো কিছু না দেখে সবাইকে পাঠায়।

</details>

---

**প্রশ্ন ৩.** Which type of network connects networks over large geographical areas?

- **A.** LAN
- **B.** WLAN
- **C.** WAN
- **D.** PAN

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. WAN**

**🧠 কেন:**

WAN (**Wide Area Network**) বড় ভৌগোলিক এলাকা জুড়ে নেটওয়ার্ক জোড়ে — ইন্টারনেট নিজেই সবচেয়ে বড় WAN।

</details>

---

**প্রশ্ন ৪.** What is the primary role of a server?

- **A.** To provide services or resources to clients
- **B.** To replace every network switch
- **C.** To assign a MAC address to every router
- **D.** To eliminate the need for IP addresses

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. To provide services or resources to clients**

**🧠 কেন:**

Server হলো কেন্দ্রীয় কম্পিউটার — এক জায়গা থেকে সেবা (DHCP, DNS, Web, File) দেয়, আর client শুধু সেই সেবা ব্যবহার করে।

</details>

---

**প্রশ্ন ৫.** Which topology commonly uses a central switch to connect end devices?

- **A.** Ring
- **B.** Bus
- **C.** Star
- **D.** Mesh

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: C. Star**

**🧠 কেন:**

**Star topology**-তে সব ডিভাইস এক কেন্দ্রীয় Switch/Hub-এ জোড়া লাগে। একটা কেবল কাটলে বাকিরা অক্ষত থাকে।

</details>

---

**প্রশ্ন ৬.** Which protocol is commonly used by the ping command?

- **A.** HTTP
- **B.** ICMP
- **C.** DHCP
- **D.** DNS

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. ICMP**

**🧠 কেন:**

ping কমান্ড **ICMP** (Echo Request / Echo Reply) ব্যবহার করে — তাই ping কাজ করে মানে IP লেয়ারে কানেক্টিভিটি আছে।

</details>

---

**প্রশ্ন ৭.** What does WLAN stand for?

- **A.** Wide Local Area Network
- **B.** Wireless Local Area Network
- **C.** Wired Long Area Network
- **D.** World Link Access Network

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. Wireless Local Area Network**

**🧠 কেন:**

WLAN = **Wireless Local Area Network** — অর্থাৎ Wi-Fi দিয়ে বানানো LAN।

</details>

---

**প্রশ্ন ৮.** Which statement about a router is correct?

- **A.** It only forwards frames based on destination MAC addresses
- **B.** It forwards IP packets between networks using routing information
- **C.** It is always required for two hosts on the same subnet to communicate
- **D.** It is a type of network cable

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. It forwards IP packets between networks using routing information**

**🧠 কেন:**

Router **ভিন্ন ভিন্ন নেটওয়ার্কের** মাঝে প্যাকেট ফরওয়ার্ড করে, আর সেটা করার জন্য IP address ও routing table ব্যবহার করে।

</details>

---

**প্রশ্ন ৯.** Two PCs have IP addresses 192.168.1.10/24 and 192.168.1.20/24. Are they in the same IPv4 subnet?

- **A.** Yes
- **B.** No
- **C.** Only if a DNS Server is configured
- **D.** Only if they have different gateways

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: A. Yes**

**🧠 কেন:**

হ্যাঁ — `192.168.1.10/24` আর `192.168.1.20/24` দুটোরই নেটওয়ার্ক অংশ `192.168.1.0`। একই subnet-এ থাকলে যোগাযোগের জন্য router লাগে না।

</details>

---

**প্রশ্ন ১০.** Which is an example of a WLAN?

- **A.** Two PCs connected to a switch using Ethernet cables
- **B.** A group of devices connected through Wi-Fi in a home
- **C.** Two routers connected by a fiber link between cities
- **D.** A single standalone computer

<details>
<summary>✅ <b>উত্তর ও ব্যাখ্যা দেখো</b></summary>

**✅ উত্তর: B. A group of devices connected through Wi-Fi in a home**

**🧠 কেন:**

বাসার Wi-Fi রাউটারে ল্যাপটপ-মোবাইল তার ছাড়া যুক্ত হওয়া = WLAN-এর সবচেয়ে পরিচিত উদাহরণ।

</details>

---

## 🎯 Homework

**Packet Tracer-এ একটি Basic LAN তৈরি করো:**

* ১টি Switch

* ৩টি PC

* তিনটি PC একই `192.168.1.0/24` Subnet-এ থাকবে।

* PC0 থেকে PC1 এবং PC2-তে Ping পরীক্ষা করবে।

### IP Plan

| Device | IP Address | Subnet Mask | 
| ----- | ----- | ----- | 
| **PC0** | 192.168.1.10 | 255.255.255.0 | 
| **PC1** | 192.168.1.20 | 255.255.255.0 | 
| **PC2** | 192.168.1.30 | 255.255.255.0 | 

> *তিনটি PC একই Subnet-এ থাকায় এই Basic Local Communication-এর জন্য Router বা Default Gateway প্রয়োজন হবে না।*

---

# 🔁 এক নজরে লজিক

```
নেটওয়ার্ক = ডিভাইস + কেবল + ঠিকানা
   ↓
ছোট এলাকা  → LAN / WLAN
বড় এলাকা  → MAN → WAN (ইন্টারনেট)
   ↓
কানেক্ট করার ধরন → Topology (Star সবচেয়ে বেশি চলে)
   ↓
কে কী করে:
  Hub     = না বুঝে সবাইকে পাঠায়
  Switch  = MAC দেখে ঠিক জায়গায় পাঠায় (Layer 2)
  Router  = IP দেখে অন্য নেটওয়ার্কে পাঠায় (Layer 3)
```

# ✅ নিজে যাচাই করো

- [ ] LAN আর WAN-এর পার্থক্য এক লাইনে বলতে পারি
- [ ] Star topology-তে কেন কেন্দ্রীয় switch দরকার, বলতে পারি
- [ ] Switch আর Router-এর কাজ আলাদা করে বলতে পারি
- [ ] তিনটা PC একই /24 subnet-এ থাকলে router লাগে না — কেন, বলতে পারি

# 🔮 পরের ধাপ

এখন জানব **ডেটা এক ডিভাইস থেকে আরেকটায় যাওয়ার সময় কোন কোন স্তর (layer) পার হয়** — OSI মডেল ও TCP/IP →
[লেসন ০২ · OSI Model ও TCP/IP](02-osi-tcp-ip.md)

---

> **নেভিগেশন:** [📘 কোর্স সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ২ ➡](02-osi-tcp-ip.md)

**এই লেসনের Tags:** `#network-basics` `#lan-wan` `#topology` `#switch` `#router` `#client-server`
