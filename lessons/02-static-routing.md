# লেসন ০২ · Two Routers + Static Routing

> **নেভিগেশন:** [⬅ লেসন ০১](01-router-cli-basics.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৩ ➡](03-dhcp.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| দুটি Router ও দুটি আলাদা LAN-এর মধ্যে Static Routing | ~৫০ মিনিট | 🟢 Beginner | [lesson-02-static-routing.pkt](../pkt-files/labs/lesson-02-static-routing.pkt) |

**Tags:** `#static-routing` `#ip-route` `#two-routers` `#wan-link` `#next-hop` `#end-to-end-ping`

---

## 🎯 এই লেসনে যা শিখবে

1. দুটি ভিন্ন সাবনেটের LAN Network তৈরি করা
2. Router Interface-এ IP Address ও Subnet Mask সেট করা
3. `ip route` কমান্ড দিয়ে **Static Routing** কনফিগার করা
4. `show ip route` দিয়ে Routing Table ভেরিফাই করা
5. PC0 → PC1 **End-to-End Ping** দিয়ে যোগাযোগ নিশ্চিত করা


### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ |
| :--- | :--- |
| **Static Route** | অ্যাডমিন নিজে হাতে `ip route` লিখে রাউটারকে যে পথ শেখায় |
| **Next-Hop IP** | গন্তব্যে যেতে পরের রাউটারের যে ইন্টারফেসে প্যাকেটটি পাঠাতে হবে তার IP |
| **Routing Table (`show ip route`)** | রাউটারের মানচিত্র — `C` = সরাসরি যুক্ত, `S` = স্ট্যাটিক রুট |
| **`/30` Point-to-Point Link** | `255.255.255.252` মাস্ক — মাত্র ২টি ব্যবহারযোগ্য IP থাকে (দুই রাউটারের সংযোগে আদর্শ) |

> 🔗 **তত্ত্ব ঝালিয়ে নিতে:** [CCNA ০৫ · Subnetting Basics](../ccna-fundamentals/05-subnetting-basics.md) · [CCNA ০৬ · VLSM](../ccna-fundamentals/06-subnetting-vlsm.md)

---

# 📖 Part 1 — ধারণা: Static Routing কী?

Router শুধু **সরাসরি কানেক্টেড** নেটওয়ার্ক চেনে। দূরবর্তী সাবনেটে প্যাকেট পাঠাতে হলে তাকে **পথ (Route)** শেখাতে হবে — এটাই Static Routing।

**Formula:**
```text
ip route [DESTINATION_NETWORK] [SUBNET_MASK] [NEXT_HOP_IP]
```

| অংশ | অর্থ | উদাহরণ |
| :--- | :--- | :--- |
| `ip route` | Static Route তৈরি করে | `ip route` |
| `DESTINATION_NETWORK` | প্যাকেট কোথায় যাবে (Network ID) | `192.168.2.0` |
| `SUBNET_MASK` | Destination-এর Mask | `255.255.255.0` |
| `NEXT_HOP_IP` | পরের Router-এর Interface IP | `10.0.0.2` |

> ⚠️ **মনে রাখবে:** রাউটিং **দ্বিমুখী (two-way)** হতে হয়। একদিকের Route দিলে Ping পৌঁছালেও রিপ্লাই ফিরতে পারবে না — তাই দুই Router-এই Route লাগবে।

---

# 🧩 Part 2 — Topology তৈরি করো

**ডিভাইস:** ২ × Router (1941) · ২ × Switch (2960) · ২ × PC (PC-PT)

```text
 Network A                                      Network B
192.168.1.0/24                                192.168.2.0/24

     PC0 (192.168.1.10)                        PC1 (192.168.2.10)
        |                                          |
     Switch0                                    Switch1
        |                                          |
   R1 G0/0 (192.168.1.1)                R2 G0/0 (192.168.2.1)
        |                                          |
   R1 G0/1 (10.0.0.1) ──── 10.0.0.0/30 ──── R2 G0/1 (10.0.0.2)
```

* **R1** = Network A-এর গেটওয়ে, **R2** = Network B-এর গেটওয়ে
* R1–R2 মাঝে **Point-to-Point WAN Link** (`10.0.0.0/30`) — এই /30 Subnet-এ মাত্র ২টি usable IP: `.1` ও `.2`

### 🔌 Connection Table

| Device 1 | Port | Device 2 | Port | Cable Type |
| :--- | :--- | :--- | :--- | :--- |
| **PC0** | FastEthernet0 | **SW1** | Fa0/1 | Copper Straight-Through |
| **SW1** | G0/1 | **R1** | G0/0 | Copper Straight-Through |
| **R1** | G0/1 | **R2** | G0/1 | Copper Cross-Over |
| **R2** | G0/0 | **SW2** | G0/1 | Copper Straight-Through |
| **SW2** | Fa0/1 | **PC1** | FastEthernet0 | Copper Straight-Through |

> 💡 দুটি Router-এর সরাসরি Ethernet লিঙ্কে স্ট্যান্ডার্ড কেবল **Cross-Over**। তবে আধুনিক রাউটারের **Auto-MDIX** সাপোর্ট থাকায় Packet Tracer-এ Straight-Through দিলেও চলে।

### 📋 Network Planning Table

| Network ID | Subnet Mask | উদ্দেশ্য |
| :--- | :--- | :--- |
| `192.168.1.0/24` | `255.255.255.0` | PC0-এর লোকাল LAN (Network A) |
| `10.0.0.0/30` | `255.255.255.252` | Router-to-Router Point-to-Point Link |
| `192.168.2.0/24` | `255.255.255.0` | PC1-এর লোকাল LAN (Network B) |

### 📋 Full Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **PC0** | Fa0 | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` |
| **R1** | G0/0 | `192.168.1.1` | `255.255.255.0` | N/A |
| **R1** | G0/1 | `10.0.0.1` | `255.255.255.252` | N/A |
| **R2** | G0/1 | `10.0.0.2` | `255.255.255.252` | N/A |
| **R2** | G0/0 | `192.168.2.1` | `255.255.255.0` | N/A |
| **PC1** | Fa0 | `192.168.2.10` | `255.255.255.0` | `192.168.2.1` |

> 📌 PC-এর Gateway সবসময় **নিজের LAN-এর Router Interface IP** হবে — PC0-এর জন্য `192.168.1.1`, PC1-এর জন্য `192.168.2.1`।

---

# ⚙️ Part 3 — Router Configuration

## R1 Configuration

```cisco
enable
configure terminal
hostname R1

! LAN Interface (PC0 সাইড)
interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

! WAN Interface (R2 সাইড)
interface gigabitEthernet 0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
 exit

end
copy running-config startup-config
```

**Verification:** `show ip interface brief` → দুটো Interface-ই **up/up** হতে হবে।

## R2 Configuration

```cisco
enable
configure terminal
hostname R2

! LAN Interface (PC1 সাইড)
interface gigabitEthernet 0/0
 ip address 192.168.2.1 255.255.255.0
 no shutdown
 exit

! WAN Interface (R1 সাইড)
interface gigabitEthernet 0/1
 ip address 10.0.0.2 255.255.255.252
 no shutdown
 exit

end
copy running-config startup-config
```

---

# 💻 Part 4 — PC Configuration

### 🖥️ PC0 (Network A)
**Desktop → IP Configuration → Static**
```text
IP Address:      192.168.1.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
```

### 🖥️ PC1 (Network B)
```text
IP Address:      192.168.2.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.2.1
```

---

# 🛣️ Part 5 — Static Route Configure করো

## R1-এ Static Route

R1-কে বলতে হবে: `192.168.2.0/24`-এ যেতে হলে প্যাকেট পাঠাও R2-এর কাছে (`10.0.0.2`):

```cisco
enable
configure terminal
ip route 192.168.2.0 255.255.255.0 10.0.0.2
end
copy running-config startup-config
```

## R2-এ Static Route

R2-কে বলতে হবে: `192.168.1.0/24`-এ যেতে হলে প্যাকেট পাঠাও R1-এর কাছে (`10.0.0.1`):

```cisco
enable
configure terminal
ip route 192.168.1.0 255.255.255.0 10.0.0.1
end
copy running-config startup-config
```

---

# 🔍 Part 6 — Routing Table Verify করো

উভয় রাউটারে `show ip route` চালাও:

### R1-এ দেখবে:
```text
C    10.0.0.0/30 is directly connected, GigabitEthernet0/1
C    192.168.1.0/24 is directly connected, GigabitEthernet0/0
S    192.168.2.0/24 [1/0] via 10.0.0.2
```

### R2-এ দেখবে:
```text
C    10.0.0.0/30 is directly connected, GigabitEthernet0/1
C    192.168.2.0/24 is directly connected, GigabitEthernet0/0
S    192.168.1.0/24 [1/0] via 10.0.0.1
```

| কোড | অর্থ |
| :--- | :--- |
| `C` | Directly Connected Route (নিজের Interface থেকে জানা) |
| `S` | Static Route (আমরা যোগ করেছি) |
| `via` | Next-Hop Router-এর IP |

---

# 🧪 Part 7 — Ping Test (ধাপে ধাপে)

**১. Router-to-Router (R1 থেকে):**
```cisco
ping 10.0.0.2          → Success rate is 100 percent (5/5) ✅
ping 192.168.2.1       → R2-এর LAN Gateway পর্যন্ত পৌঁছাতে পারছে ✅
```

**২. End-to-End (PC0 → PC1):**
PC0 → Desktop → Command Prompt:
```text
ping 192.168.2.10
```
**Expected Result:**
```text
Request timed out.
Reply from 192.168.2.10: bytes=32 time<1ms TTL=126
Reply from 192.168.2.10: bytes=32 time<1ms TTL=126
Reply from 192.168.2.10: bytes=32 time<1ms TTL=126
```
*(প্রথম প্যাকেটে ARP ও Route Lookup-এর কারণে একটি Timeout আসতে পারে — পুনরায় Ping করলে ৪/৪ সাকসেস)*

> 💡 `TTL=126` কেন? PC থেকে যাওয়া প্যাকেটের TTL ১২৮ থেকে শুরু; **২টি Router** পার হয়ে ২ কমেছে → ১২৬।

**৩. ফিরতি Ping (PC1 → PC0):**
```text
ping 192.168.1.10
```

---

# 🔁 Part 8 — লজিক: Packet কীভাবে চলাচল করে?

```text
PC0 (192.168.1.10)
     │  1. Gateway-তে পাঠায়
     ▼
R1 LAN (192.168.1.1)
     │  2. Static Route দেখে Next-Hop 10.0.0.2-এ পাঠায়
     ▼
R1 WAN (10.0.0.1) ── 3. Point-to-Point Link ──► R2 WAN (10.0.0.2)
                                                    │  4. LAN ইন্টারফেসে ফরওয়ার্ড
                                                    ▼
                                            R2 LAN (192.168.2.1)
                                                    │  5. Switch হয়ে গন্তব্যে
                                                    ▼
                                            PC1 (192.168.2.10)
```
*(রিপ্লাই প্যাকেট ঠিক বিপরীত পথে: R2 → R1 → PC0)*

---

# ❌ Troubleshooting: Ping ব্যর্থ হলে?

1. **Interface up/up কি না?** — উভয় রাউটারে `show ip interface brief`
2. **সরাসরি Link কাজ করছে?** — R1 থেকে `ping 10.0.0.2` (ফেইল হলে কেবল, IP, `no shutdown` চেক)
3. **Route আছে?** — `show ip route`-এ `S` এন্ট্রি সঠিক Next-Hop সহ আছে কি না দেখো
4. **PC IP/Gateway মিলছে?** — `ipconfig` দিয়ে যাচাই (PC0 GW `192.168.1.1`, PC1 GW `192.168.2.1`)
5. **দুই দিকেই Route আছে?** — একদিকের Route = ফেরত পথ নেই = Ping Fail

---

# 🧠 Quick Cheat-Sheet

| উদ্দেশ্য | কমান্ড |
| :--- | :--- |
| Static Route কনফিগার | `ip route [DEST_NET] [MASK] [NEXT_HOP]` |
| Routing Table দেখা | `show ip route` |
| Interface IP Status | `show ip interface brief` |
| Connectivity Test | `ping [IP]` |
| Configuration Save | `copy running-config startup-config` |

---

# ✅ Final Checklist

| Task | Configuration | Expected Result |
| :--- | :--- | :--- |
| PC0 / PC1 IP | `192.168.1.10/24` / `192.168.2.10/24` | Static IP সেট ✅ |
| R1 / R2 LAN IP | `192.168.1.1` / `192.168.2.1` | Gateway প্রস্তুত ✅ |
| WAN Link | `10.0.0.0/30` (.1 ↔ .2) | up/up ✅ |
| R1 Static Route | `192.168.2.0 255.255.255.0 10.0.0.2` | `S` রুট যুক্ত ✅ |
| R2 Static Route | `192.168.1.0 255.255.255.0 10.0.0.1` | `S` রুট যুক্ত ✅ |
| Final Ping | PC0 → `ping 192.168.2.10` | **Reply আসবে** ✅ |

---

# 🔮 পরের ধাপ

Static Route মুখস্থ করার বদলে চাইলে Dynamic Routing (RIP, OSPF) দিয়েও রুট শেখানো যায় (লেসন ০৮-এর Cheat-Sheet-এ আছে)। এবার শিখব নেটওয়ার্কে স্বয়ংক্রিয়ভাবে IP বিতরণের জন্য **DHCP** → [লেসন ০৩ · DHCP Configuration](03-dhcp.md)

---

> **নেভিগেশন:** [⬅ লেসন ০১](01-router-cli-basics.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৩ ➡](03-dhcp.md)

**এই লেসনের Tags:** `#static-routing` `#ip-route` `#next-hop` `#routing-table` `#wan` `#two-routers`
