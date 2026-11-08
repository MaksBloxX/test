# লেসন ০৩ · Router DHCP Configuration

> **নেভিগেশন:** [⬅ লেসন ০২](02-static-routing.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৪ ➡](04-dns-http-server.md)

| 🎯 লক্ষ্য | ⏱️ সময় | 📊 লেভেল | 🧰 ল্যাব ফাইল |
| :--- | :--- | :--- | :--- |
| Router-এ DHCP Pool কনফিগার করে PC-গুলোতে স্বয়ংক্রিয় IP বিতরণ | ~৪০ মিনিট | 🟢 Beginner | [lesson-03-dhcp.pkt](../pkt-files/labs/lesson-03-dhcp.pkt) |

**Tags:** `#dhcp` `#dhcp-pool` `#excluded-address` `#auto-ip` `#default-router`

---

## 🎯 এই লেসনে যা শিখবে

1. **DHCP কী** এবং কেন এটি দরকার
2. Router-এ **DHCP Pool** তৈরি ও কনফিগার করা
3. **Excluded Address** দিয়ে গুরুত্বপূর্ণ IP সুরক্ষা দেওয়া
4. PC-তে **DHCP অন** করে স্বয়ংক্রিয় IP নেওয়া
5. `show ip dhcp binding` দিয়ে **Lease Table** যাচাই করা


### 🏷️ মূল শব্দকোষ (Quick Glossary)

| শব্দ | সহজ অর্থ |
| :--- | :--- |
| **DHCP** | ক্লায়েন্ট পিসিতে স্বয়ংক্রিয়ভাবে IP, Mask, Gateway ও DNS দেওয়ার প্রোটোকল |
| **DORA Process** | **D**iscover → **O**ffer → **R**equest → **A**ck — ৪ ধাপে IP পাওয়ার প্রক্রিয়া |
| **Excluded Address** | সার্ভার/প্রিন্টার/গেটওয়ের Static IP যেন অন্য কাউকে না দেয় সেজন্য বাদ রাখা রেঞ্জ |
| **APIPA (`169.254.x.x`)** | DHCP সার্ভার খুঁজে না পেলে পিসি নিজে থেকে যে অস্থায়ী লোকাল IP বসিয়ে নেয় |

> 🔗 **সম্পর্কিত প্র্যাকটিস ল্যাব:** [🖨️ Office Shared Printer Network](../Extras/office-shared-printer-lab.md)

---

# 📖 Part 1 — DHCP কী?

**DHCP** = *Dynamic Host Configuration Protocol* — এমন প্রোটোকল যা ডিভাইসগুলোকে স্বয়ংক্রিয়ভাবে **IP Address, Subnet Mask, Default Gateway** ও **DNS Server** প্রদান করে।

ধরো, নেটওয়ার্কে ৫০টি PC আছে। প্রতিটিতে ম্যানুয়ালি IP বসানোর বদলে Router-এ DHCP চালু করলে নিমেষেই সবার IP বরাদ্দ হয়ে যায়।

**DHCP ছাড়া (Manual):** প্রতিটি PC-তে হাতে হাতে IP → ভুল হওয়ার সম্ভাবনা বেশি, সময় বেশি লাগে।

**DHCP সহ (Automatic):**
```text
                 Router (DHCP Server)
                         │
                       Switch
                   ┌─────┼─────┐
                 PC0    PC1    PC2
                Auto   Auto   Auto
                 IP     IP     IP
```

> 💡 **কী যা কী?** — **DHCP** IP বিতরণ করে, **DNS** নামকে IP-তে রূপান্তর করে, **Default Gateway** বাইরের নেটওয়ার্কে যাওয়ার দরজা। (বিস্তারিত [লেসন ০৪](04-dns-http-server.md))

---

# 🧩 Part 2 — Lab Topology

**ডিভাইস:** ১ × Router (1941) · ১ × Switch (2960) · ২ × PC (PC-PT)

```text
            Router R1
              G0/0
                │
              G0/1
           Switch SW1
            /        \
        Fa0/1        Fa0/2
          │            │
         PC0          PC1
       (DHCP)       (DHCP)
```

### 🔌 Connection Table (Copper Straight-Through)

| Device 1 | Port | Device 2 | Port |
| :--- | :--- | :--- | :--- |
| **R1** | GigabitEthernet 0/0 | **SW1** | GigabitEthernet 0/1 |
| **PC0** | FastEthernet 0 | **SW1** | FastEthernet 0/1 |
| **PC1** | FastEthernet 0 | **SW1** | FastEthernet 0/2 |

### 📋 Plan

| Parameter | Value |
| :--- | :--- |
| **Network** | `192.168.1.0/24` |
| **Router Gateway IP** | `192.168.1.1` |
| **Excluded IP Range** | `192.168.1.1` – `192.168.1.10` |
| **DHCP Pool Name** | `OFFICE` |
| **Client IP Range** | `192.168.1.11` থেকে শুরু |

---

# ⚙️ Part 3 — Router Configuration (ধাপে ধাপে)

## Step 1: Gateway Interface Configure

```cisco
enable
configure terminal
hostname R1

interface gigabitEthernet 0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit
```
> এই `192.168.1.1`-ই ক্লায়েন্টদের **Default Gateway** হবে।

## Step 2: গুরুত্বপূর্ণ IP Exclude করো

```cisco
ip dhcp excluded-address 192.168.1.1 192.168.1.10
```

> **❓ কেন Exclude?** — Gateway, প্রিন্টার বা সার্ভারের **Static IP**-এর সাথে ক্লায়েন্টের IP কনফ্লিক্ট যেন না হয়। `.1`–`.10` বাদ দিলে ক্লায়েন্ট `.11` থেকে IP পাবে।

## Step 3: DHCP Pool তৈরি করো

```cisco
ip dhcp pool OFFICE
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 exit

end
copy running-config startup-config
```

### 💡 প্রতিটি Command-এর কাজ

| Command | কাজ |
| :--- | :--- |
| `ip dhcp pool OFFICE` | `OFFICE` নামে DHCP Pool তৈরি |
| `network 192.168.1.0 255.255.255.0` | কোন সাবনেটের IP বিতরণ হবে তা নির্ধারণ |
| `default-router 192.168.1.1` | ক্লায়েন্টের Default Gateway |
| `ip dhcp excluded-address [START] [END]` | সংরক্ষিত IP রেঞ্জ (বাদ পড়বে) |
| `copy running-config startup-config` | NVRAM-এ সেভ |

> **DHCP Pool কী?** — IP বিতরণের নিয়মগুলো রাখা একটি কনফিগারেশন ব্লক। নাম যেকোনো দেওয়া যায় (`LAB`, `HOME`…)।

---

# 💻 Part 4 — PC-তে DHCP চালু করো

প্রতিটি PC-তে: **Desktop → IP Configuration → DHCP** রেডিও বাটনে ক্লিক করো।

কিছুক্ষণেই **DHCP request successful** সহ স্বয়ংক্রিয়ভাবে তথ্য আসবে:

```text
PC0:  IP 192.168.1.11   Mask 255.255.255.0   Gateway 192.168.1.1
PC1:  IP 192.168.1.12   Mask 255.255.255.0   Gateway 192.168.1.1
```

*(`.11` থেকে শুরু হওয়ার কারণ: `.1`–`.10` Exclude করা আছে)*

---

# 🔍 Part 5 — Verification

## ১. PC-তে `ipconfig`
```shell
ipconfig
```
- [x] PC0 ও PC1-এর IP **ভিন্ন**
- [x] দুটোই `192.168.1.0/24`-এর অন্তর্ভুক্ত
- [x] উভয়ে Gateway `192.168.1.1`

## ২. Router-এ DHCP Binding Table
```cisco
show ip dhcp binding
```
**Expected Output:**
```text
IP address       Client-ID/Hardware address      Lease expiration        Type
192.168.1.11     0001.42A1.B2C3                  --                      Automatic
192.168.1.12     0002.16B4.C5D6                  --                      Automatic
```
> **DHCP Binding কী?** — কোন IP কোন ক্লায়েন্টের MAC-এ **লিজ** হিসেবে বরাদ্দ হয়েছে তার টেবিল।

## ৩. অতিরিক্ত কমান্ড
```cisco
show ip dhcp pool        ← পুলের পরিসংখ্যান
show ip dhcp conflict    ← IP কনফ্লিক্ট হয়েছে কি না
show ip interface brief  ← interface up/up কি না
```

## ৪. Ping Test
PC0-এর Command Prompt থেকে:
```text
ping 192.168.1.1     ← Gateway ✅
ping 192.168.1.12    ← PC1 ✅
```
```text
Reply from 192.168.1.12: bytes=32 time<1ms TTL=128
```

---

# 🔁 Part 6 — লজিক: DHCP কীভাবে কাজ করে? (DORA)

```text
PC0 ──1. Discover (সবাইকে জিজ্ঞেস: কে IP দেবে?)──►  Router DHCP
PC0 ◄──2. Offer (Router: এই IPটা নাও 192.168.1.11)──  Router DHCP
PC0 ──3. Request (ঠিক আছে, ওটাই চাই)──►             Router DHCP
PC0 ◄──4. Ack (অনুমোদিত ✅)──                        Router DHCP
```
**D**iscover → **O**ffer → **R**equest → **A**ck — এই ৪ ধাপেই সম্পূর্ণ IP বরাদ্দ।

---

# ❌ Troubleshooting

| সমস্যা | সমাধান |
| :--- | :--- |
| PC `169.254.x.x` (APIPA) দেখাচ্ছে | DHCP Request Router-এ পৌঁছায়নি — কেবল, সুইচ পোর্ট, interface up চেক করো |
| IP আসছে কিন্তু Ping হয় না | Gateway ও `no shutdown` আবার যাচাই করো |
| ভুল IP রেঞ্জ আসছে | `show ip dhcp binding` ও Pool-এর `network` কমান্ড মেলাও |
| Duplicate IP Error | `ip dhcp excluded-address` সঠিক আছে কি না দেখো |
| লিঙ্ক লাইট কমলা | কিছুক্ষণ অপেক্ষা করো (STP Listening/Learning), তারপর সবুজ হবে |

---

# 🧠 DHCP Cheat-Sheet

| Command | কাজ |
| :--- | :--- |
| `ip dhcp pool [NAME]` | নতুন Pool তৈরি |
| `network [NET_ID] [MASK]` | বিতরণের নেটওয়ার্ক রেঞ্জ |
| `default-router [GW_IP]` | ক্লায়েন্টের Gateway |
| `dns-server [DNS_IP]` | ক্লায়েন্টের DNS *(লেসন ০৪-এ ব্যবহার)* |
| `ip dhcp excluded-address [START] [END]` | সংরক্ষিত IP রেঞ্জ |
| `show ip dhcp pool` | পুল পরিসংখ্যান |
| `show ip dhcp binding` | লিজ টেবিল |

---

# ✅ Final Checklist

| Task | Command / Action | Expected Result |
| :--- | :--- | :--- |
| Gateway | `ip address 192.168.1.1 255.255.255.0` | Interface কনফিগ ✅ |
| Exclude | `ip dhcp excluded-address 192.168.1.1 192.168.1.10` | `.1`–`.10` বাদ ✅ |
| Pool | `ip dhcp pool OFFICE` + `network` + `default-router` | পুল প্রস্তুত ✅ |
| PC0 / PC1 | IP Configuration → **DHCP** | `.11` / `.12` স্বয়ংক্রিয় ✅ |
| Binding | `show ip dhcp binding` | দুই এন্ট্রি দৃশ্যমান ✅ |
| Ping | PC0 → `ping 192.168.1.12` | 100% Reply ✅ |

---

# 🔮 পরের ধাপ

এখন পর্যন্ত PC-রা IP পেল স্বয়ংক্রিয়ভাবে। এবার শিখব **DNS** — নাম দিয়ে ওয়েবসাইট খোলার সাথে **HTTP Web Server** চালু করা → [লেসন ০৪ · DNS ও Web Server](04-dns-http-server.md)

---

> **নেভিগেশন:** [⬅ লেসন ০২](02-static-routing.md) · [📚 লেসন সূচি](README.md) · [🏠 হোম](../README.md) · [পরের লেসন ০৪ ➡](04-dns-http-server.md)

**এই লেসনের Tags:** `#dhcp` `#pool` `#excluded-address` `#dora` `#lease` `#auto-configuration`
