# 📧 Extra Lab ০২ · Email Server Configuration (SMTP ও POP3)

> **নেভিগেশন:** [⬅ FTP Server Lab](ftp-server-lab.md) · [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [পরের ল্যাব: Shared Printer ➡](office-shared-printer-lab.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| দুটি আলাদা LAN সাবনেটের মাঝে SMTP ও POP3 দিয়ে ইমেইল পাঠানো ও গ্রহণ করা | ~৪০ মিনিট | 🟡 Intermediate | [`Email-Server.pkt`](../pkt-files/practice/Email-Server.pkt) |

**Tags:** `#email-server` `#smtp` `#pop3` `#inter-subnet` `#port-25` `#port-110` `#ccna-lab`

---

## 🎯 এই ল্যাবে যা শিখবে

1. Cisco Packet Tracer-এ একটি পূর্ণাঙ্গ **Email Server (SMTP + POP3)** কনফিগার করা
2. আলাদা দুটি LAN সাবনেটের (`192.168.10.0/24` ও `192.168.20.0/24`) মধ্যে রাউটারের মাধ্যমে মেইল রাউটিং বোঝা
3. ইমেইল সার্ভারে ডোমেইন (`university.com`) ও ইউজার মেইলবক্স তৈরি করা
4. PC-র Mail Client কনফিগার করে **Send** ও **Receive** যাচাই করা
5. ধাপে ধাপে ইমেইল ট্রাবলশুটিং ও CCNA Viva প্রশ্নের উত্তর শেখা

### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ | পোর্ট ও প্রোটোকল |
| :--- | :--- | :--- |
| **SMTP** (*Simple Mail Transfer Protocol*) | ক্লায়েন্ট থেকে সার্ভারে বা এক সার্ভার থেকে অন্য সার্ভারে ইমেইল **পাঠানোর (Push)** প্রোটোকল | `TCP 25` / `587` |
| **POP3** (*Post Office Protocol v3*) | সার্ভারের মেইলবক্স থেকে নিজের পিসিতে ইমেইল **ডাউনলোড (Pull)** করার প্রোটোকল | `TCP 110` / `995` |
| **IMAP** (*Internet Message Access Protocol*) | সার্ভারে মেইল রেখেই একাধিক ডিভাইসে ইনবক্স সিঙ্ক করার আধুনিক প্রোটোকল | `TCP 143` / `993` |
| **Mail Client (MUA)** | পিসির ইমেইল অ্যাপ (যেমন Outlook, Thunderbird বা PT-র Email ট্যাব) | Client App |

---

## ১. Network Topology

### প্রয়োজনীয় ডিভাইসসমূহ
* **2 × PC:** `PC0` ও `PC1`
* **2 × Switch:** Switch 2960 (`SW1` ও `SW2`)
* **1 × Router:** Cisco 1941 (`Router2`)
* **1 × Server:** Generic `Server-PT` (`Email Server`)
* **কেবল:** সব কানেকশনে **Copper Straight-Through** কেবল ব্যবহার করো

### Topology Diagram

```text
          LAN 1 (192.168.10.0/24)                LAN 2 (192.168.20.0/24)
                 [ PC0 ]                                [ PC1 ]
                .10.3/24                               .20.2/24
                    │                                      │
                 [ SW1 ]                                [ SW2 ]──── [ Email Server ]
                    │                                      │           .20.3/24
               G0/0 (.10.1)                           G0/1 (.20.1)   (SMTP + POP3)
                    └──────────── [ Router2 ] ─────────────┘
```

---

## ২. IP Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | DNS Server |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Router2** | `GigabitEthernet0/0` | `192.168.10.1` | `255.255.255.0` | — | — |
| **Router2** | `GigabitEthernet0/1` | `192.168.20.1` | `255.255.255.0` | — | — |
| **PC0 (makshedul)** | `FastEthernet0` | `192.168.10.3` | `255.255.255.0` | `192.168.10.1` | `192.168.20.3` |
| **PC1 (antor)** | `FastEthernet0` | `192.168.20.2` | `255.255.255.0` | `192.168.20.1` | `192.168.20.3` |
| **Email Server** | `FastEthernet0` | `192.168.20.3` | `255.255.255.0` | `192.168.20.1` | `192.168.20.3` |

> 🔁 **লজিক:** `PC0` আছে `192.168.10.0/24` নেটওয়ার্কে, আর `Email Server` ও `PC1` আছে `192.168.20.0/24` নেটওয়ার্কে। দুটি সাবনেটই সরাসরি `Router2`-এর সাথে যুক্ত (`Connected` রুট), তাই `Router2` স্বয়ংক্রিয়ভাবে Inter-Subnet Routing করবে।

---

## ৩. Router2 Configuration

`Router2`-এর **CLI** ওপেন করে নিচের কমান্ডগুলো দাও:

```cisco
enable
configure terminal
hostname Router2

! LAN 1 Interface (Connecting to PC0 via SW1)
interface gigabitEthernet 0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
 exit

! LAN 2 Interface (Connecting to PC1 & Email Server via SW2)
interface gigabitEthernet 0/1
 ip address 192.168.20.1 255.255.255.0
 no shutdown
 exit

end
copy running-config startup-config
```

### 🔍 স্ট্যাটাস ভেরিফিকেশন
```cisco
Router2# show ip interface brief
```
> নিশ্চিত করো `GigabitEthernet0/0` এবং `GigabitEthernet0/1` দুটোরই Status ও Protocol **`up / up`** দেখাচ্ছে।

---

## ৪. End-Device IP Configuration

### 💻 PC0 (`makshedul`) Setup
* যাও: **PC0 → Desktop → IP Configuration → Static**
```text
IP Address:      192.168.10.3
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.10.1
DNS Server:      192.168.20.3
```

### 💻 PC1 (`antor`) Setup
* যাও: **PC1 → Desktop → IP Configuration → Static**
```text
IP Address:      192.168.20.2
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.20.1
DNS Server:      192.168.20.3
```

### 🖥️ Email Server IP Setup
* যাও: **Email Server → Desktop → IP Configuration → Static**
```text
IP Address:      192.168.20.3
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.20.1
DNS Server:      192.168.20.3
```

---

## ৫. Server-এ Email Service কনফিগারেশন

সার্ভারে ক্লিক করে **Services → EMAIL** ট্যাবে যাও:

```text
+-------------------------------------------------------+
|                 EMAIL SERVICE SETUP                   |
+-------------------------------------------------------+
|  SMTP Service:   (*) On    ( ) Off                    |
|  POP3 Service:   (*) On    ( ) Off                    |
|                                                       |
|  Domain Name:    [ university.com   ]  [ Set ]        |
+-------------------------------------------------------+
```

### ধাপসমূহ:
1. **Service Toggle:** **SMTP Service** এবং **POP3 Service** দুটোই `On` করো।
2. **Domain Name:** বক্সে `university.com` লিখে পাশে থাকা **`Set`** বাটনে অবশ্যই ক্লিক করো! *(⚠️ `Set` না চাপলে ডোমেইন সেভ হবে না!)*
3. **User Accounts তৈরি:** নিচের তথ্য দিয়ে `[ + ]` বাটনে ক্লিক করো:

| User | Username | Password | Action | সম্পূর্ণ Email Address |
| :--- | :--- | :--- | :---: | :--- |
| **PC0 User** | `pc0` | `1234` | ক্লিক **`[ + ]`** | `pc0@university.com` |
| **PC1 User** | `pc1` | `1234` | ক্লিক **`[ + ]`** | `pc1@university.com` |

---

## ৬. PC-গুলোতে Email Client কনফিগারেশন

এখানে DNS ছাড়া সরাসরি Email Server-এর IP (`192.168.20.3`) দিয়ে Incoming ও Outgoing Mail Server সেট করব *(চাইলে DNS সার্ভারে `mail.university.com` A-Record যোগ করে নামও ব্যবহার করা যায়)*।

### 📧 PC0 Mail Client
* যাও: **PC0 → Desktop → Email → Configure Mail**
```text
Your Name:              PC0 (Makshedul)
Email Address:          pc0@university.com
Incoming Mail Server:   192.168.20.3
Outgoing Mail Server:   192.168.20.3
Username:               pc0
Password:               1234
```
*নিচে **Save** বাটনে ক্লিক করো।*

### 📧 PC1 Mail Client
* যাও: **PC1 → Desktop → Email → Configure Mail**
```text
Your Name:              PC1 (Antor)
Email Address:          pc1@university.com
Incoming Mail Server:   192.168.20.3
Outgoing Mail Server:   192.168.20.3
Username:               pc1
Password:               1234
```
*নিচে **Save** বাটনে ক্লিক করো।*

---

## ৭. Testing ও Packet Flow লজিক

### ধাপ ১: PC0 থেকে ইমেইল পাঠানো (SMTP Push)
1. **PC0 → Desktop → Email → Compose**-এ ক্লিক করো।
2. তথ্য পূরণ করো:
   * **To:** `pc1@university.com`
   * **Subject:** `Test Email from PC0`
   * **Message Body:** `Hello PC1, this is my first email from Cisco Packet Tracer lab!`
3. **Send** বাটনে ক্লিক করো → নিচে স্ট্যাটাস দেখাবে: **`Send Success`** ✅

### ধাপ ২: PC1-এ ইমেইল গ্রহণ করা (POP3 Pull)
1. **PC1 → Desktop → Email**-এ যাও।
2. **Receive** বাটনে ক্লিক করো।
3. ইনবক্সে `pc0@university.com` থেকে আসা মেইলটি দেখা যাবে — ডাবল ক্লিক করে পড়ে দেখো! 🎉

### 🔁 পর্দার আড়ালে কী ঘটল? (Packet Flow)
```text
১. [PC0 (192.168.10.3)] ──(TCP 25: SMTP)──► [Router2] ──► [Email Server (192.168.20.3)]
   (PC0 মেইলটি লিখে রাউটার পার হয়ে সার্ভারের pc1 মেইলবক্সে জমা রাখল)

২. [PC1 (192.168.20.2)] ──(TCP 110: POP3 Request)──────► [Email Server (192.168.20.3)]
   [PC1 (192.168.20.2)] ◄─(TCP 110: Mail Downloaded)──── [Email Server (192.168.20.3)]
   (PC1 যখন Receive চাপল, POP3 প্রোটোকলে সার্ভার থেকে মেইলটি নিজের ইনবক্সে নামিয়ে আনল)
```

---

## ৮. ❌ Troubleshooting Checklist

যদি ইমেইল আদান-প্রদান ব্যর্থ হয়, নিচের ক্রমে পরীক্ষা করো:

| সমস্যা | সম্ভাব্য কারণ | সমাধান |
| :--- | :--- | :--- |
| `Server not found / Timeout` | রাউটার ইন্টারফেস বন্ধ বা Gateway ভুল | PC0 থেকে `ping 192.168.10.1` ও `ping 192.168.20.3` দিয়ে লেয়ার ৩ সংযোগ চেক করো |
| রাউটার পোর্ট লাল | `no shutdown` দেওয়া হয়নি | `Router2`-এর `G0/0` ও `G0/1`-এ `no shutdown` চালাও |
| `Send Failed` | সার্ভারে ডোমেইন `Set` করা হয়নি বা SMTP Off | Server → Services → EMAIL-এ গিয়ে `Set` বাটন চাপো এবং SMTP/POP3 `On` নিশ্চিত করো |
| `Authentication Failed` | Username/Password বা `@university.com` ভুল | ক্লায়েন্টের `Configure Mail`-এ ইউজারনেম (`pc0`/`pc1`) ও পাসওয়ার্ড (`1234`) হুবহু মেলাও |

---

## ৯. 🎓 CCNA Viva / Interview Questions

<details>
<summary><b>Q1. What is the difference between SMTP, POP3, and IMAP?</b></summary>

* **SMTP (Port 25/587):** শুধুমাত্র মেইল **পাঠানোর (sending/relaying)** কাজে ব্যবহৃত হয়।
* **POP3 (Port 110/995):** সার্ভার থেকে ক্লায়েন্টে মেইল **ডাউনলোড** করে (ডিফল্টভাবে সার্ভার থেকে মুছে দেয়)।
* **IMAP (Port 143/993):** মেইল সার্ভারেই সংরক্ষিত রাখে এবং ফোন/ল্যাপটপ সব ডিভাইসে ফোল্ডার সিঙ্ক করে।
</details>

<details>
<summary><b>Q2. Why do both SMTP and POP3 use TCP instead of UDP?</b></summary>

ইমেইলের কোনো অক্ষর বা অ্যাটাচমেন্ট হারিয়ে গেলে চলবে না। **TCP** নির্ভরযোগ্য (Reliable), ক্রমানুসারী ডেলিভারি এবং Error Recovery নিশ্চিত করে — তাই SMTP ও POP3 উভয়ই TCP ব্যবহার করে।
</details>

<details>
<summary><b>Q3. Why was Router2 mandatory in this topology?</b></summary>

`PC0` (`192.168.10.0/24`) এবং `Email Server` (`192.168.20.0/24`) দুটি ভিন্ন IP সাবনেটে অবস্থিত। Layer 2 সুইচ ভিন্ন সাবনেটে ফ্রেম পাঠাতে পারে না — তাই সাবনেট পারাপারের জন্য Layer 3 Router (`Router2`) অপরিহার্য।
</details>

---

## ✅ Final Checklist

| কাজ | যাচাই | অবস্থা |
| :--- | :--- | :---: |
| Router2 `G0/0` ও `G0/1` কনফিগার | `show ip interface brief` → দুটোই `up/up` | ☐ |
| PC0 থেকে Email Server পিং | `ping 192.168.20.3` → Reply (TTL=127) | ☐ |
| Email Server-এ Domain `university.com` | **Set** বাটন চাপা হয়েছে + SMTP/POP3 **On** | ☐ |
| ইউজার `pc0` ও `pc1` তৈরি | User List-এ দুটি নামই দৃশ্যমান | ☐ |
| PC0 → PC1 ইমেইল টেস্ট | PC0-এ `Send Success` ও PC1-এ `Receive`-এ মেইল প্রাপ্তি | ☐ |

---

> **নেভিগেশন:** [⬅ FTP Server Lab](ftp-server-lab.md) · [📦 Extra Labs সূচি](README.md) · [🏠 হোম](../README.md) · [পরের ল্যাব: Shared Printer ➡](office-shared-printer-lab.md)

**Tags:** `#email-lab` `#smtp` `#pop3` `#packet-tracer` `#inter-vlan-mail` `#viva-prep`
