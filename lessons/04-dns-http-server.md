# লেসন ০৪ · DNS Server ও HTTP Web Server

> **নেভিগেশন:** [⬅ লেসন ০৩](03-dhcp.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৫ ➡](05-vlan.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| Packet Tracer-এ DNS + HTTP Server সেটআপ, DHCP সহ সম্পূর্ণ নেটওয়ার্ক | ~৫০ মিনিট | 🟡 Beginner–Intermediate | [lesson-04-dns-http-server.pkt](../pkt-files/labs/lesson-04-dns-http-server.pkt) |

**Tags:** `#dns` `#http` `#web-server` `#dhcp` `#domain` `#server-config`

---

## 🎯 এই লেসনে যা শিখবে

1. **DNS কী** এবং Domain Name কীভাবে IP-তে রূপান্তর হয়
2. Server-এ **Static IP** সেট করা (সার্ভারের IP কখনো DHCP নয়!)
3. DNS Service-এ **A Record** (Name → IP) যোগ করা
4. **HTTP Service** চালু করে ছোট ওয়েবসাইট হোস্ট করা
5. PC থেকে **ডোমেন নাম দিয়ে** ওয়েবসাইট খোলা (DHCP + DNS একসাথে)
6. **"Host Name Unresolved"** এররের ধাপে ধাপে সমাধান (Troubleshooting)


### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ |
| :--- | :--- |
| **DNS** (*Domain Name System*) | মানুষের চেনা নাম (`www.office.local`) থেকে কম্পিউটারের IP খুঁজে বের করার ফোনবুক (`UDP/TCP 53`) |
| **A Record** | DNS সার্ভারে একটি Domain Name-এর বিপরীতে তার IPv4 ঠিকানা লিখে রাখার এন্ট্রি |
| **HTTP / HTTPS** | ব্রাউজারে ওয়েবপেজ (`index.html`) দেখানোর প্রোটোকল (`TCP Port 80 / 443`) |
| **Host Name Unresolved** | ব্রাউজারের এরর — যার মানে DNS নামটিকে IP-তে অনুবাদ করতে পারেনি |

> 🔗 **তত্ত্ব ও চিত্রসহ বই:** [📕 OSI: From Search to Screen](../reference/OSI-Illustrated.md) · [📦 Extra: FTP ও Email Server](../Extras/README.md)

---

# 📖 Part 1 — DNS কী?

**DNS** = *Domain Name System* — মানুষের বোঝার উপযোগী **Domain Name** (`www.google.com`) কে মেশিনের উপযোগী **IP Address**-এ রূপান্তর (Resolve) করে।

* **DNS ছাড়া:** `192.168.1.100` — এই আইপি মুখস্থ করে টাইপ করতে হতো
* **DNS সহ:** `www.office.local` — সহজ নাম; DNS ব্যাকগ্রাউন্ডে আইপি বের করে দেয়

### 💡 তিনটি সার্ভিসের পার্থক্য

| সার্ভিস | কী করে | মনে রাখার ট্রিক |
| :--- | :--- | :--- |
| **DNS** | নাম → IP খুঁজে বের করে | "ফোনবুক" 📖 |
| **DHCP** | Client-কে স্বয়ংক্রিয় IP/Gateway দেয় | "IP বিতরণকারী" 🎫 |
| **Default Gateway** | বাইরের নেটওয়ার্কে যাওয়ার দরজা | "প্রধান ফটক" 🚪 |

---

# 🧩 Part 2 — Network Topology

১টি Router, ১টি Switch, ২টি PC, ১টি Server:

```text
                    Router R1
                  192.168.1.1
                        │
                     Switch0
                  ┌─────┼─────┐
                 PC0  Server0  PC1
                DHCP   DNS/Web  DHCP
                      192.168.1.100
```

### 📋 Addressing Table (`192.168.1.0/24`)

| Device | IP Address | Subnet Mask | Default Gateway | DNS Server | কাজ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** (G0/0) | `192.168.1.1` | `255.255.255.0` | N/A | N/A | Gateway + DHCP Server |
| **Server0** (Fa0) | `192.168.1.100` **(Static)** | `255.255.255.0` | `192.168.1.1` | `192.168.1.100` (নিজে) | DNS + HTTP Server |
| **PC0** | DHCP | `255.255.255.0` | `192.168.1.1` | `192.168.1.100` | Client |
| **PC1** | DHCP | `255.255.255.0` | `192.168.1.1` | `192.168.1.100` | Client |

> 📌 **নিয়ম:** সার্ভারের IP সবসময় **Static** — যাতে কখনো তার IP বদলে না যায়।

**Domain:** `www.office.local` → `192.168.1.100`

### 🔌 Connection Table (Copper Straight-Through)

| From | Port | To | Port |
| :--- | :--- | :--- | :--- |
| **R1** | G0/0 | **Switch0** | G0/1 |
| **Server0** | Fa0 | **Switch0** | Fa0/1 |
| **PC0** | Fa0 | **Switch0** | Fa0/2 |
| **PC1** | Fa0 | **Switch0** | Fa0/3 |

---

# ⚙️ Part 3 — Router Configuration (Gateway + DHCP)

```cisco
enable
configure terminal
hostname R1

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

! সার্ভারের Static IP সুরক্ষিত রাখতে Exclude
ip dhcp excluded-address 192.168.1.1 192.168.1.100

ip dhcp pool OFFICE
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 192.168.1.100
 exit

end
copy running-config startup-config
```

> 💡 **নতুন কমান্ড:** `dns-server 192.168.1.100` — DHCP ক্লায়েন্টরা স্বয়ংক্রিয়ভাবে DNS Server হিসেবে `192.168.1.100` পাবে। `ip dhcp excluded-address` `.1` থেকে `.100` পর্যন্ত দিয়েছি যাতে সার্ভারের `.100`-ও সুরক্ষিত থাকে।

---

# 🖥️ Part 4 — Server0 Configuration

## Step 1: Static IP

**Server0 → Desktop → IP Configuration → Static:**

```text
IP Address:      192.168.1.100
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
DNS Server:      192.168.1.100
```

## Step 2: DNS Service চালু

**Server0 → Services → DNS:**
1. **DNS Service** = **ON** করো
2. **A Record** যোগ করো:

| Field | Value |
| :--- | :--- |
| **Name** | `www.office.local` |
| **Type** | A Record |
| **Address** | `192.168.1.100` |
3. **Add** ক্লিক করো ✅

## Step 3: HTTP Web Service চালু

**Server0 → Services → HTTP (or WEB):**
1. **HTTP** ও **HTTPS** = **ON** (সাধারণত ডিফল্ট ON থাকে)
2. **index.html** ফাইলটি সম্পাদনা করে চাইলে নিজের টেক্সট বসাতে পারো:

```html
<html><body><h1>Welcome to Office Network!</h1></body></html>
```

---

# 💻 Part 5 — PC Configuration

PC0 ও PC1 দুটোতেই: **Desktop → IP Configuration → DHCP**

```text
PC0: IP 192.168.1.101 (approx)  Gateway 192.168.1.1  DNS 192.168.1.100
PC1: IP 192.168.1.102 (approx)  Gateway 192.168.1.1  DNS 192.168.1.100
```
*(নির্দিষ্ট IP ভিন্ন হতে পারে — `ipconfig` দিয়ে দেখে নাও)*

---

# 🧪 Part 6 — DNS ও Web Testing

## Test 1: Server-এ Ping
PC0 → Command Prompt:
```text
ping 192.168.1.100
```
✅ Reply আসলে Connectivity ঠিক আছে।

## Test 2: ব্রাউজারে ডোমেন টেস্ট
PC0 → **Desktop → Web Browser**, Address Bar-এ:
```text
www.office.local
```
✅ **"Welcome to Office Network!"** (বা index.html-এর কনটেন্ট) দেখা গেলে DNS + HTTP দুটোই সফল!

## Test 3: PC1 থেকেও একইভাবে
```text
www.office.local
```
✅ দুই Client-ই একই সার্ভারে পৌঁছাচ্ছে।

---

# 🌐 Part 7 — একাধিক সার্ভার ও একাধিক ওয়েবসাইট

## A. দুইটি সার্ভার যোগ করলে (Server0 + Server1)

ধরো, Server0-এ **Office Website**, Server1-এ **Coffee Website** চালাতে চাও:

```text
                 Router R1 (192.168.1.1)
                       │
                    Switch0
                 ┌─────┼─────┐
               PC0   Server0  Server1
             (DHCP)  .100      .99
                    DNS+HTTP   HTTP
                    Office     Coffee
```

### 📋 IP Plan

| Device | IP Address | Gateway | DNS Server | Service |
| :--- | :--- | :--- | :--- | :--- |
| **Server0** | `192.168.1.100` (Static) | `192.168.1.1` | `192.168.1.100` | DNS + HTTP |
| **Server1** | `192.168.1.99` (Static) | `192.168.1.1` | `192.168.1.100` | HTTP |
| **PC0** | DHCP | `192.168.1.1` | `192.168.1.100` | Client |

> 💡 **মনে রাখো:** DNS Server ও Web Server একই ডিভাইসে থাকতে বাধ্যতামূলক নয়। এখানে DNS আছে Server0-তে, তাই **সবাই (Server1 সহ) DNS = `192.168.1.100`** ব্যবহার করবে।

### Step 1 — দুই সার্ভারে Static IP দাও

**Server0** → Desktop → IP Configuration → **Static:**
```text
IP Address:      192.168.1.100
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
DNS Server:      192.168.1.100
```

**Server1** → Desktop → IP Configuration → **Static:**
```text
IP Address:      192.168.1.99
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
DNS Server:      192.168.1.100
```

### Step 2 — Router-এ দুই সার্ভারের IP বাদ রাখো

সার্ভারের Static IP যেন DHCP ক্লায়েন্টকে না দেয় — Router CLI-তে:

```cisco
enable
configure terminal
ip dhcp excluded-address 192.168.1.1 192.168.1.10
ip dhcp excluded-address 192.168.1.99 192.168.1.100
end
copy running-config startup-config
```
*(`.1`–`.10` = Gateway ও অন্য Static Device; `.99`–`.100` = দুই সার্ভার)*

### Step 3 — দুই সার্ভারে HTTP চালু করো

* **Server0** → Services → HTTP → **ON** (`index.html`-এ চাইলে Office লেখা দাও)
* **Server1** → Services → HTTP → **ON** (`index.html`-এ Coffee লেখা দাও)

### Step 4 — DNS-এ দুই Website-এর Record (Server0-তে)

Server0 → Services → DNS → **ON** → দুটি A Record:

| Name | Type | Address | কোন সার্ভারের সাইট |
| :--- | :--- | :--- | :--- |
| `www.office.local` | A Record | `192.168.1.100` | Server0 |
| `www.coffee.xyz` | A Record | `192.168.1.99` | Server1 |

### Step 5 — PC0 থেকে টেস্ট

```text
ipconfig                  → DNS Server: 192.168.1.100 দেখাবে
ping 192.168.1.99         → Reply ✅
http://www.office.local   → Office Website ✅
http://www.coffee.xyz     → Coffee Website ✅
```

---

## B. একটি সার্ভারে ২ বা ততোধিক ওয়েবসাইট

**একটি DNS Server-এ যত খুশি Website-এর Record রাখা যায়** — প্রতিটি ওয়েবসাইটের জন্য আলাদা DNS Server লাগে না।

যদি **সব সাইট একটাই সার্ভারে** (যেমন `192.168.1.100`) রাখতে চাও — DNS-এ একের পর এক Record যোগ করো:

| Name | Type | Address |
| :--- | :--- | :--- |
| `www.office.local` | A Record | `192.168.1.100` |
| `www.coffee.xyz` | A Record | `192.168.1.100` |
| `www.shop.xyz` | A Record | `192.168.1.100` |

> 📌 **Packet Tracer-এর বাস্তবতা:** এক সার্ভারে একটাই `index.html` থাকে — তাই একই IP-তে সব ডোমেন গেলে **একই ওয়েবসাইট দেখাবে**। আলাদা আলাদা সাইট দেখাতে হলে **আলাদা সার্ভার (আলাদা IP) নাও** — ঠিক যেমন **A** অংশে দুই সার্ভারে দুই সাইট করা হয়েছে।

### 🧠 নতুন যেকোনো Website যোগ করতে মাত্র ২টি কাজ

1. **DNS-এ একটি A Record** (নাম → সঠিক IP)
2. **ওই IP-তে HTTP Service ON**

⚠️ **সবচেয়ে কমন ভুল:** Record-টি ভুল সার্ভারের DNS-এ যোগ করা। মনে রাখো — **ক্লায়েন্ট যে DNS-এর IP পায় (এখানে `.100`), সেই DNS-এই সব Website-এর Record থাকতে হবে।**

---

# 🔁 Part 8 — লজিক: DHCP + DNS একসাথে কীভাবে কাজ করে?

```text
১. PC0 DHCP-তে IP চায় → Router দেয়: IP + Gateway + DNS=192.168.1.100
২. PC0-এর ব্রাউজারে www.office.local টাইপ
৩. PC0 → DNS Server (192.168.1.100): "www.office.local এর IP কী?"
৪. DNS Server → PC0: "192.168.1.100"
৫. PC0 → HTTP Server (192.168.1.100): "index.html দাও"
৬. HTTP Server → PC0: 📄 "Welcome to Office Network!"
```

> 🧠 **মনে রাখো:** DNS শুধু **নাম থেকে IP** দেয় — আসল ওয়েবপেজটা **HTTP Server** পাঠায়। তাই দুটো Service-ই ON করতে হয়।

---

# ❌ Troubleshooting

| সমস্যা | কী চেক করবে |
| :--- | :--- |
| `ping 192.168.1.100` হয় না | Server-এর Static IP, কেবল, `no shutdown` |
| IP টাইপ করলে সাইট খোলে, নাম দিলে না | DNS Service ON? A Record সঠিক? PC-তে DNS IP `192.168.1.100`? |
| DNS Request Failed | `www.office.local` স্পেলিং মেলাও (`.local` বাদ যায় না) |
| PC-তে DNS IP আসছে না | Router-এর DHCP Pool-এ `dns-server 192.168.1.100` আছে কি না |
| Website খুলতে চাইলে ভুল পেজ | HTTP Service ON কি না, `index.html` আছে কি না দেখো |
| দ্বিতীয় Website (নতুন ডোমেন) খোলে না | DNS-এ ওই ডোমেনের A Record যোগ করা হয়েছে কি না (উপরে Part 7 দেখো) |
| **Host Name Unresolved** (ব্রাউজারে এরর) | নিচের **ধাপে ধাপে সমাধান** দেখো |

## 🧯 "Host Name Unresolved" — ধাপে ধাপে সমাধান

**Host Name Unresolved** মানে: PC আপনার দেওয়া **Domain Name-কে IP-তে Resolve করতে পারছে না** — অর্থাৎ সমস্যা Website-এ নয়, **DNS Configuration**-এ।

ধরো, Part 7-এর সেটআপে `http://www.coffee.xyz` লিখলে ব্রাউজারে এই এরর দেখাচ্ছে:

| Device | IP | Service |
| :--- | :--- | :--- |
| **Server0** | `192.168.1.100` | DNS + Office Website |
| **Server1** | `192.168.1.99` | Coffee Website |
| **Router** | `192.168.1.1` | DHCP + Gateway |

### Step 1 — Server0-তে DNS Record পরীক্ষা করো

Server0 → **Services → DNS**, নিশ্চিত করো:

* DNS Service: **On**
* এই দুটি A Record আছে:

| Name | Type | Address |
| :--- | :--- | :--- |
| `www.office.local` | A Record | `192.168.1.100` |
| `www.coffee.xyz` | A Record | `192.168.1.99` |

`www.coffee.xyz` না থাকলে নিচের তথ্য দিয়ে **Add** করো:

```text
Name:    www.coffee.xyz
Type:    A Record
Address: 192.168.1.99
```

> ⚠️ শুধু Server1-এ IP সেট করলেই Domain কাজ করবে না — **DNS-এও Record থাকতে হবে।**

### Step 2 — Server0-এর IP Configuration পরীক্ষা করো

Server0 → **Desktop → IP Configuration:**

```text
IP Address:      192.168.1.100
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
DNS Server:      192.168.1.100
```

### Step 3 — Server1-এর Configuration পরীক্ষা করো

Server1 → **Desktop → IP Configuration:**

```text
IP Address:      192.168.1.99
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
DNS Server:      192.168.1.100
```

তারপর Server1 → **Services → HTTP → On** (Coffee Website-এর জন্য)।

### Step 4 — PC0-এর DNS পরীক্ষা করো

PC0 → **Desktop → IP Configuration** → **DHCP** সিলেক্ট করো। তারপর **Command Prompt:**

```text
ipconfig
```

নিশ্চিত করো — **DNS Server: 192.168.1.100** দেখাচ্ছে। DNS IP অন্য কিছু দেখালে বা একেবারে না থাকলে Router-এর DHCP Pool পরীক্ষা করো:

```cisco
enable
show running-config
```

Pool-এর ভেতরে এই Configuration থাকতে হবে:

```cisco
ip dhcp pool OFFICE
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 192.168.1.100
```

> 📌 `dns-server` কমান্ডটা DHCP Pool-এর ভেতরেই থাকতে হবে — না থাকলে PC-তে DNS Server-এর IP আসবেই না।

### Step 5 — PC0 থেকে Ping Test

```text
ping 192.168.1.100     → Reply উচিত (DNS Server)
ping 192.168.1.99      → Reply উচিত (Coffee Server)
```

* ✅ **Ping সফল, কিন্তু Domain কাজ করছে না** → সমস্যা DNS-এ: A Record বা PC-এর DNS Configuration দেখো (Step 1 ও Step 4)
* ❌ **Ping ব্যর্থ** → সমস্যা Connection-এ: IP, Cable, Switch Port, Server Configuration দেখো

### Step 6 — ব্রাউজারে আবার চেষ্টা করো

PC0 → **Desktop → Web Browser:**

```text
http://www.office.local
http://www.coffee.xyz
```

দুটি Domain-এর A Record সঠিক থাকলে এবং সংশ্লিষ্ট HTTP Service চালু থাকলে দুটো Website-ই খুলবে।

> 🧠 **লজিক:** "Host Name Unresolved" এলে সমস্যা ৩টা জায়গায় যেকোনো একটাতে হতে পারে — **(১)** DNS-এ ওই নামের A Record নেই, **(২)** PC-তে DNS Server-এর IP ঠিক নেই (DHCP Pool-এ `dns-server` নেই), **(৩)** DNS Service ON নেই। উপরের ধাপগুলো ঠিক এই ৩টা জায়গা পরপর চেক করে — তাই যেকোনো DNS সমস্যায় এই ক্রমেই যাও।

---

# ✅ Final Checklist

| Task | Expected Result |
| :--- | :--- |
| Server0 Static IP `192.168.1.100` | ✅ |
| DNS ON + A Record (`www.office.local` → `192.168.1.100`) | ✅ |
| HTTP ON | ✅ |
| Router DHCP Pool-এ `dns-server 192.168.1.100` | ✅ |
| PC0/PC1 DHCP-তে IP + DNS পাচ্ছে | ✅ |
| ব্রাউজারে `www.office.local` খুলছে | ✅ |

---

# 🔮 পরের ধাপ

একই সুইচে সবাই এক নেটওয়ার্কে আছে। এবার শিখব **VLAN** — একটি সুইচকে ভাগ করে আলাদা আলাদা সুরক্ষিত গ্রুপ বানানো → [লেসন ০৫ · VLAN](05-vlan.md)

---

> **নেভিগেশন:** [⬅ লেসন ০৩](03-dhcp.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৫ ➡](05-vlan.md)

**এই লেসনের Tags:** `#dns` `#a-record` `#http` `#web-browser` `#static-ip` `#server`
