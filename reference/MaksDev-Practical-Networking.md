> **নেভিগেশন:** [📚 Reference Library](README.md) · [🏠 রেপো হোম](../README.md) · [📖 IOS Cheat-Sheet](cli-command-cheatsheet.md) · [📥 **PDF সংস্করণ ডাউনলোড করো**](MaksDev-Practical-Networking.pdf)

---

# Practical Networking

## 30 Essential Commands

### বাংলা ব্যবহারিক গাইড

**MaksDev Studio**

Md. Makshedul Islam

Student, EXIM Bank Agricultural University Bangladesh.

### 🖼️ চিত্রে বোঝো: ৩০টি নেটওয়ার্ক কমান্ডের কাজভিত্তিক মানচিত্র

![৩০টি নেটওয়ার্ক কমান্ডের কাজভিত্তিক মানচিত্র — Reachability, IP, Route, DNS, Port, Remote Access, Packet Capture, Firewall ও Performance।](../assets/diagrams/reference-30-command-toolbox.svg)

> **ছবির সারকথা:** Reachability, IP, Route, DNS, Port, Remote Access, Packet Capture, Firewall ও Performance।

---

## শুরু করার আগে

এই বইটি শিক্ষার্থী ও নতুন Linux/Windows ব্যবহারকারীদের জন্য একটি ব্যবহারিক রেফারেন্স। প্রতিটি কমান্ডের কাজ, পাঁচটি উদাহরণ, ফলাফল বোঝার উপায় এবং প্রয়োজনীয় সতর্কতা এক জায়গায় দেওয়া হয়েছে। এটি কোনো বিশ্ববিদ্যালয়ের আনুষ্ঠানিক প্রকাশনা নয়।

### নিরাপদ অনুশীলন

নিজের কম্পিউটার, ভার্চুয়াল মেশিন বা অনুমোদিত ল্যাব ব্যবহার করুন। নেটওয়ার্ক scan, packet capture এবং load test-এর আগে অনুমতি নিন। route, IP ও firewall পরিবর্তনের আগে backup ও recovery access নিশ্চিত করুন।

### উদাহরণ ব্যবহারের নিয়ম

eth0, wlan0, Ethernet, user, hostname, IP ও path আপনার পরিবেশ অনুযায়ী বদলাতে হবে। 192.168.x.x বা 10.x.x.x ব্যক্তিগত নেটওয়ার্কের উদাহরণ; সেগুলো আপনার অনুমোদিত target কি না যাচাই করুন। example.com-এর file/API path কেবল নমুনা।

Linux command-এর sudo প্রয়োজন হলে administrator privilege দেয়। Windows configuration পরিবর্তনের জন্য Run as administrator ব্যবহার করুন। tool ইনস্টল না থাকলে OS-এর trusted package source ব্যবহার করুন। কোডে দেখানো > চিহ্ন output ফাইলে লিখতে পারে; বিদ্যমান ফাইল overwrite হওয়ার বিষয়ে সতর্ক থাকুন।

### বইটি পড়ার উপায়

প্রথমে নিজের interface, IP ও default gateway দেখুন। এরপর IP-তে ping, ডোমেইনের DNS query এবং প্রয়োজনীয় TCP port পরীক্ষা করুন। সমস্যা অস্পষ্ট থাকলে route analysis বা সীমিত packet capture ব্যবহার করুন। সব ক্ষেত্রে শেষ গন্তব্য ও অ্যাপ্লিকেশনের ফল মিলিয়ে সিদ্ধান্ত নিন।

### ব্যবহারের পরামর্শ

কমান্ডের আচরণ OS, সংস্করণ ও driver অনুযায়ী ভিন্ন হতে পারে; installed tool-এর help ও manual-ই চূড়ান্ত নির্দেশনা।

## বিষয়সূচি

### 1. সংযোগ ও নেটওয়ার্ক পরীক্ষা

- 01. `ping`

- 02. `tracert`

- 03. `pathping`

- 04. `mtr`

- 05. `telnet`

### 2. ইন্টারফেস ও IP কনফিগারেশন

- 06. `ipconfig`

- 07. `ifconfig`

- 08. `ip addr`

- 09. `ip link`

- 10. `iwconfig`

### 3. রাউটিং ও ARP টেবিল

- 11. `route`

- 12. `ip route`

- 13. `arp`

### 4. DNS ব্যবস্থাপনা

- 14. `nslookup`

- 15. `dig`

- 16. `host`

- 17. `ipconfig /flushdns`

### 5. কানেকশন ও পোর্ট বিশ্লেষণ

- 18. `netstat`

- 19. `nmap`

### 6. ফাইল ট্রান্সফার ও রিমোট অ্যাক্সেস

- 20. `curl`

- 21. `wget`

- 22. `ssh`

- 23. `scp`

- 24. `sftp`

### 7. প্যাকেট ক্যাপচার ও বিশ্লেষণ

- 25. `tcpdump`

- 26. `wireshark`

### 8. ফায়ারওয়াল ও নেটওয়ার্ক ব্যবস্থাপনা

- 27. `iptables`

- 28. `netsh`

- 29. `netsh advfirewall`

### 9. ইন্টারনেট পারফরম্যান্স পরীক্ষা

- 30. `speedtest-cli`

## 1. সংযোগ ও নেটওয়ার্ক পরীক্ষা

### 01. ping

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

গন্তব্যে ICMP Echo Request পাঠিয়ে সংযোগ, round-trip time এবং packet loss পরীক্ষা করে। নাম দিয়ে পরীক্ষা করলে DNS resolution-ও প্রয়োজন হয়।

#### মূল ব্যবহার

```text
ping 8.8.8.8
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. IP দিয়ে সংযোগ পরীক্ষা

```text
ping 8.8.8.8
```

2. ডোমেইন দিয়ে সংযোগ পরীক্ষা

```text
ping google.com
```

3. চারটি প্যাকেট পাঠান

```text
ping -c 4 192.168.1.1
```

4. অর্ধ সেকেন্ড ব্যবধানে অনুরোধ

```text
ping -i 0.5 10.0.0.1
```

5. অনুমোদিত ল্যাবে flood পরীক্ষা

```text
sudo ping -f 192.168.1.1
```

#### ফলাফল কীভাবে বুঝবেন

time বা RTT কম হলে সাড়া দ্রুত। packet loss ধারাবাহিকভাবে থাকলে সংযোগ পরীক্ষা করুন। উত্তর না পাওয়া মানেই সার্ভার বন্ধ নয়; ICMP ব্লক থাকতে পারে।

#### মনে রাখুন

এখানকার -c, -i ও -f Linux-এর অপশন। Windows-এ চারটি অনুরোধের জন্য ping -n 4 ব্যবহার করুন। Flood পরীক্ষা শুধু নিজের বিচ্ছিন্ন ল্যাবে; উৎপাদন নেটওয়ার্কে নয়।

### 02. tracert

**প্ল্যাটফর্ম:** Windows

Windows-এ প্যাকেট কোন কোন রাউটার পেরিয়ে গন্তব্যে যায় তা দেখায়। প্রতিটি hop-এর উত্তর দিতে কত সময় লাগে সেটিও পাওয়া যায়।

#### মূল ব্যবহার

```text
tracert google.com
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ডোমেইনের পথ দেখুন

```text
tracert google.com
```

2. নাম resolve না করে পথ দেখুন

```text
tracert -d 8.8.8.8
```

3. সর্বোচ্চ ১০টি hop

```text
tracert -h 10 example.com
```

4. প্রতি উত্তরের সময়সীমা ৫০০ ms

```text
tracert -w 500 192.168.1.1
```

5. IPv6 দিয়ে পরীক্ষা

```text
tracert -6 ipv6.google.com
```

#### ফলাফল কীভাবে বুঝবেন

প্রতিটি সারিতে একটি hop ও probe-এর সময় থাকে। * মানে নির্ধারিত সময়ে উত্তর আসেনি; সেটি একাই প্যাকেট ফরওয়ার্ডিং ব্যর্থতার প্রমাণ নয়।

#### মনে রাখুন

ফরোয়ার্ড ও রিটার্ন পথ ভিন্ন হতে পারে। মাঝের কোনো hop ধীর দেখালেও শেষ গন্তব্যের ফলাফল মিলিয়ে বিচার করুন।

### 03. pathping

**প্ল্যাটফর্ম:** Windows

Windows-এর এই টুল প্রথমে পথ বের করে, তারপর hop-ভিত্তিক probe পাঠিয়ে loss-এর পরিসংখ্যান সংগ্রহ করে।

#### মূল ব্যবহার

```text
pathping google.com
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. পথ ও packet loss পরীক্ষা

```text
pathping google.com
```

2. সর্বোচ্চ ১৫টি hop

```text
pathping -h 15 8.8.8.8
```

3. প্রতি hop-এ ৫০টি query

```text
pathping -q 50 example.com
```

4. IPv6 ব্যবহার

```text
pathping -6 ipv6.google.com
```

5. DNS resolution বাদ দিন

```text
pathping -n 192.168.1.1
```

#### ফলাফল কীভাবে বুঝবেন

রিপোর্টে source-to-hop ও link/node loss দেখুন। মাঝের রাউটার নিজের ICMP উত্তর সীমিত করতে পারে; শেষ গন্তব্য পর্যন্ত loss থাকছে কি না দেখুন।

#### মনে রাখুন

রিপোর্ট তৈরি হতে কয়েক মিনিট লাগতে পারে। একবারের ফলকে স্থায়ী নেটওয়ার্ক সমস্যার সিদ্ধান্ত হিসেবে নেবেন না।

### 04. mtr

**প্ল্যাটফর্ম:** Linux

Linux-এ ping ও traceroute-এর ধারণা একসঙ্গে ব্যবহার করে। সময়ের সঙ্গে hop-ভিত্তিক latency ও loss পর্যবেক্ষণে সুবিধা হয়।

#### মূল ব্যবহার

```text
mtr google.com
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. লাইভ route পর্যবেক্ষণ

```text
mtr google.com
```

2. ১০ cycle শেষে রিপোর্ট

```text
mtr -r -c 10 google.com
```

3. প্রশস্ত রিপোর্ট

```text
mtr -rw google.com
```

4. নাম resolve না করা

```text
mtr -n 8.8.8.8
```

5. TCP probe দিয়ে পরীক্ষা

```text
mtr --tcp google.com
```

#### ফলাফল কীভাবে বুঝবেন

Loss%, Snt, Last, Avg, Best ও Wrst তুলনা করুন। শেষ গন্তব্যে loss না থাকলে মাঝের hop-এর loss প্রায়ই ICMP rate limiting-এর ফল।

#### মনে রাখুন

TCP probe সব বাধা অতিক্রম করে না। প্রয়োজন হলে --port দিয়ে অনুমোদিত সার্ভিসের পোর্ট নির্বাচন করুন; কিছু probe-এ বাড়তি privilege লাগে।

### 05. telnet

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

একটি নির্দিষ্ট TCP পোর্টে সংযোগ স্থাপন করা যায় কি না দ্রুত দেখতে কাজে লাগে। পুরোনো remote-login protocol হিসেবেও ব্যবহৃত হতো।

#### মূল ব্যবহার

```text
telnet example.com 80
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. HTTP পোর্ট পরীক্ষা

```text
telnet example.com 80
```

2. SSH পোর্ট পরীক্ষা

```text
telnet 192.168.1.100 22
```

3. SMTP পোর্ট পরীক্ষা

```text
telnet mail.example.com 25
```

4. পুরোনো Telnet সার্ভারে সংযোগ

```text
telnet 192.168.1.50
```

5. MySQL পোর্ট পরীক্ষা

```text
telnet db.example.com 3306
```

#### ফলাফল কীভাবে বুঝবেন

সংযোগ খুলে ফাঁকা স্ক্রিন বা banner দেখা গেলে TCP সংযোগ হয়েছে। Connection refused ও timeout আলাদা সমস্যা নির্দেশ করতে পারে।

#### মনে রাখুন

Telnet লগইন এনক্রিপ্টেড নয়। পোর্টে সংযোগ হলেই অ্যাপ্লিকেশন সুস্থ বা TLS সঠিক—এমন নয়। বের হতে Ctrl+] চাপুন, তারপর quit লিখুন।

## 2. ইন্টারফেস ও IP কনফিগারেশন

### 06. ipconfig

**প্ল্যাটফর্ম:** Windows

Windows কম্পিউটারের IP, subnet mask, gateway ও DNS-সংক্রান্ত তথ্য দেখায়। DHCP lease release বা renew-ও করা যায়।

#### মূল ব্যবহার

```text
ipconfig
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. সাধারণ IP তথ্য

```text
ipconfig
```

2. বিস্তারিত adapter তথ্য

```text
ipconfig /all
```

3. DHCP lease ছেড়ে দিন

```text
ipconfig /release
```

4. DHCP lease নবায়ন

```text
ipconfig /renew
```

5. DNS cache দেখুন

```text
ipconfig /displaydns
```

#### ফলাফল কীভাবে বুঝবেন

IPv4 Address, Default Gateway, DHCP Enabled ও DNS Servers দেখুন। 169.254.x.x ঠিকানা অনেক সময় DHCP lease না পাওয়ার ইঙ্গিত দেয়।

#### মনে রাখুন

/release নেটওয়ার্ক বিচ্ছিন্ন করতে পারে। রিমোট সেশনে না চালিয়ে স্থানীয় recovery access রাখুন। প্রয়োজনমতো Administrator terminal ব্যবহার করুন।

### 07. ifconfig

**প্ল্যাটফর্ম:** Linux

পুরোনো Linux net-tools প্যাকেজের কমান্ড। ইন্টারফেসের অবস্থা দেখা, IP বসানো ও MAC পরিবর্তনে ব্যবহার করা হয়।

#### মূল ব্যবহার

```text
ifconfig
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. সক্রিয় ইন্টারফেস

```text
ifconfig
```

2. সব ইন্টারফেস

```text
ifconfig -a
```

3. ইন্টারফেস চালু

```text
sudo ifconfig eth0 up
```

4. IPv4 ও netmask নির্ধারণ

```text
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0
```

5. MAC ঠিকানা পরিবর্তন

```text
sudo ifconfig eth0 hw ether 00:11:22:33:44:55
```

#### ফলাফল কীভাবে বুঝবেন

inet-এ IPv4, ether-এ MAC এবং RX/TX অংশে ট্রাফিকের counter দেখুন। সব ইন্টারফেস দেখতে -a প্রয়োজন হতে পারে।

#### মনে রাখুন

আধুনিক Linux-এ ip ব্যবহার করাই ভালো। MAC বদলাতে ইন্টারফেস down করতে হতে পারে। পরিবর্তন সাধারণত reboot-এর পর স্থায়ী থাকে না।

### 08. ip addr

**প্ল্যাটফর্ম:** Linux

আধুনিক Linux-এ ইন্টারফেসে থাকা IPv4 ও IPv6 ঠিকানা দেখে এবং প্রয়োজনমতো ঠিকানা যোগ বা বাদ দেয়।

#### মূল ব্যবহার

```text
ip addr show
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. সব ঠিকানা

```text
ip addr show
```

2. নির্দিষ্ট ইন্টারফেস

```text
ip addr show eth0
```

3. ঠিকানা যোগ

```text
sudo ip addr add 192.168.1.200/24 dev eth0
```

4. ঠিকানা মুছুন

```text
sudo ip addr del 192.168.1.200/24 dev eth0
```

5. শুধু IPv4

```text
ip -4 addr show
```

#### ফলাফল কীভাবে বুঝবেন

inet হলো IPv4 ও prefix length; inet6 হলো IPv6। scope ও dynamic চিহ্ন দেখে ঠিকানার ধরন বোঝা যায়।

#### মনে রাখুন

ইন্টারফেসের নাম eth0 নাও হতে পারে। ভুল ঠিকানা বা prefix দিলে সংযোগ নষ্ট হতে পারে। ip দিয়ে করা পরিবর্তন সাধারণত অস্থায়ী।

### 09. ip link

**প্ল্যাটফর্ম:** Linux

Linux-এর data-link স্তরে ইন্টারফেসের administrative state, MAC ও অন্যান্য link বৈশিষ্ট্য নিয়ন্ত্রণ করে।

#### মূল ব্যবহার

```text
ip link show
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ইন্টারফেসের অবস্থা

```text
ip link show
```

2. ইন্টারফেস চালু

```text
sudo ip link set eth0 up
```

3. ইন্টারফেস বন্ধ

```text
sudo ip link set eth0 down
```

4. MAC পরিবর্তন

```text
sudo ip link set dev eth0 address 00:11:22:33:44:55
```

5. ইন্টারফেসের পরিসংখ্যান

```text
ip -s link show eth0
```

#### ফলাফল কীভাবে বুঝবেন

UP মানে প্রশাসনিকভাবে চালু; LOWER_UP সাধারণত link carrier থাকার ইঙ্গিত। RX/TX error ও dropped counter নজরে রাখুন।

#### মনে রাখুন

নিজের remote connection বহনকারী ইন্টারফেস down করবেন না। MAC পরিবর্তনের আগে down করা বা driver-specific প্রস্তুতি লাগতে পারে।

### 10. iwconfig

**প্ল্যাটফর্ম:** Linux

পুরোনো Linux Wireless Extensions-ভিত্তিক টুল। SSID, channel, transmission power ও wireless mode-সংক্রান্ত তথ্য দেখায় বা পরিবর্তন করে।

#### মূল ব্যবহার

```text
iwconfig
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ওয়্যারলেস তথ্য

```text
iwconfig
```

2. SSID নির্ধারণ

```text
sudo iwconfig wlan0 essid "MyNetwork"
```

3. চ্যানেল নির্ধারণ

```text
sudo iwconfig wlan0 channel 6
```

4. ট্রান্সমিশন পাওয়ার

```text
sudo iwconfig wlan0 txpower 20
```

5. Ad-Hoc mode

```text
sudo iwconfig wlan0 mode Ad-Hoc
```

#### ফলাফল কীভাবে বুঝবেন

ESSID, Mode, Frequency, Tx-Power ও Link Quality দেখুন। সব driver একই তথ্য বা পরিবর্তন সমর্থন করে না।

#### মনে রাখুন

এটি দিয়ে শুধু ESSID বসানো WPA/WPA2 সংযোগের পূর্ণ পদ্ধতি নয়। আধুনিক সিস্টেমে iw বা NetworkManager ব্যবহার করুন; স্থানীয় radio-power বিধি মেনে চলুন।

## 3. রাউটিং ও ARP টেবিল

### 11. route

**প্ল্যাটফর্ম:** Linux

পুরোনো Linux routing table দেখা এবং static route যোগ বা বাদ দেওয়ার টুল। নতুন সিস্টেমে ip route বেশি উপযোগী।

#### মূল ব্যবহার

```text
route -n
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. রাউটিং টেবিল

```text
route -n
```

2. নেটওয়ার্ক route যোগ

```text
sudo route add -net 10.0.0.0 netmask 255.0.0.0 gw 192.168.1.1
```

3. route মুছুন

```text
sudo route del -net 10.0.0.0 netmask 255.0.0.0
```

4. default gateway যোগ

```text
sudo route add default gw 192.168.1.254
```

5. hostname ছাড়াই টেবিল

```text
route -n
```

#### ফলাফল কীভাবে বুঝবেন

Destination, Gateway, Genmask ও Iface কলাম মিলিয়ে দেখুন। default route সাধারণত 0.0.0.0 destination হিসেবে থাকে।

#### মনে রাখুন

এখানে Linux-এর syntax দেখানো হয়েছে; Windows-এর route ভিন্ন। gateway অবশ্যই পৌঁছানো যায় এমন হতে হবে। source-এর একই display command দুইভাবে দেখানো হয়েছে।

### 12. ip route

**প্ল্যাটফর্ম:** Linux

Linux kernel কোন গন্তব্যে কোন gateway ও interface ব্যবহার করবে তা দেখা ও পরিবর্তন করা যায়। নির্দিষ্ট IP-এর জন্য route নির্বাচনও দেখা যায়।

#### মূল ব্যবহার

```text
ip route show
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. বর্তমান route

```text
ip route show
```

2. নেটওয়ার্ক route যোগ

```text
sudo ip route add 10.0.0.0/24 via 192.168.1.1
```

3. route মুছুন

```text
sudo ip route del 10.0.0.0/24
```

4. default gateway বদলান

```text
sudo ip route replace default via 192.168.1.254
```

5. নির্দিষ্ট IP-এর নির্বাচিত পথ

```text
ip route get 8.8.8.8
```

#### ফলাফল কীভাবে বুঝবেন

default, via, dev ও src ক্ষেত্র দেখুন। ip route get বাস্তব প্যাকেট না পাঠিয়েই route selection-এর ফল জানায়।

#### মনে রাখুন

default route বদলালে রিমোট অ্যাক্সেস বন্ধ হতে পারে। VPN বা policy routing থাকলে শুধু main table দেখেই সব বোঝা যাবে না।

### 13. arp

**প্ল্যাটফর্ম:** Linux

লোকাল IPv4 নেটওয়ার্কে IP ঠিকানার সঙ্গে MAC ঠিকানার সম্পর্ক ARP cache-এ থাকে। এই টুল সেই mapping দেখে ও পরিবর্তন করে।

#### মূল ব্যবহার

```text
arp -a
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ARP table দেখুন

```text
arp -a
```

2. একটি entry মুছুন

```text
sudo arp -d 192.168.1.1
```

3. static mapping যোগ

```text
sudo arp -s 192.168.1.50 00:11:22:33:44:55
```

4. ইন্টারফেস অনুযায়ী table

```text
arp -i eth0 -a
```

5. ইন্টারফেসের dynamic neighbor cache পরিষ্কার

```text
sudo ip neigh flush dev eth0
```

#### ফলাফল কীভাবে বুঝবেন

একই LAN-এর প্রতিবেশী IP ও MAC মিলিয়ে দেখুন। দূরের সার্ভারের বদলে প্রায়ই gateway-এর MAC দেখা স্বাভাবিক।

#### মনে রাখুন

IPv6-এ ARP নয়, Neighbor Discovery ব্যবহৃত হয়। শেষ উদাহরণে আধুনিক ip neigh ব্যবহার করা হয়েছে; flush-এর পর mapping আবার শেখা হয়, permanent entry সাধারণত বাদ থাকে।

## 4. DNS ব্যবস্থাপনা

### 14. nslookup

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

ডোমেইনের IP, IP-এর reverse name বা নির্দিষ্ট ধরনের DNS record খুঁজতে পারে। Windows ও বহু Unix-সদৃশ সিস্টেমে পাওয়া যায়।

#### মূল ব্যবহার

```text
nslookup example.com
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ডোমেইনের IP

```text
nslookup example.com
```

2. reverse lookup

```text
nslookup 8.8.8.8
```

3. নির্দিষ্ট DNS server

```text
nslookup example.com 1.1.1.1
```

4. MX record

```text
nslookup -type=MX google.com
```

5. interactive mode

```text
nslookup
```

#### ফলাফল কীভাবে বুঝবেন

Server অংশে ব্যবহৃত resolver এবং Name/Address অংশে উত্তর দেখুন। NXDOMAIN ও timeout এক নয়; প্রথমটি নাম না থাকার DNS উত্তর।

#### মনে রাখুন

ডোমেইনের একাধিক IP থাকা স্বাভাবিক। reverse lookup-এর জন্য PTR record থাকতে হয়; না থাকলেও IP ব্যবহারযোগ্য হতে পারে।

### 15. dig

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

DNS query-এর বিস্তারিত উত্তর দেখায়। record type, resolver এবং সংক্ষিপ্ত output বেছে নিয়ে DNS সমস্যা বিশ্লেষণ করা যায়।

#### মূল ব্যবহার

```text
dig example.com
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. A record query

```text
dig example.com
```

2. MX record query

```text
dig example.com MX
```

3. নির্দিষ্ট resolver

```text
dig @8.8.8.8 example.com
```

4. reverse DNS query

```text
dig -x 8.8.8.8
```

5. সংক্ষিপ্ত উত্তর

```text
dig +short example.com
```

#### ফলাফল কীভাবে বুঝবেন

status, ANSWER SECTION, TTL ও Query time দেখুন। NOERROR হলেও উত্তর শূন্য হলে ওই record type নাও থাকতে পারে।

#### মনে রাখুন

+short সুবিধাজনক, কিন্তু debugging-এর সময় পূর্ণ output দেখুন। public resolver-কে query করলে আপনার DNS প্রশ্ন সেই সেবায় যায়।

### 16. host

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

সংক্ষিপ্ত DNS lookup-এর জন্য সহজ টুল। A/AAAA, MX, NS ও reverse lookup দ্রুত দেখা যায়।

#### মূল ব্যবহার

```text
host example.com
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ডোমেইনের ঠিকানা

```text
host example.com
```

2. reverse lookup

```text
host 8.8.8.8
```

3. নির্দিষ্ট resolver

```text
host example.com 1.1.1.1
```

4. MX record

```text
host -t MX google.com
```

5. NS record

```text
host -t NS example.com
```

#### ফলাফল কীভাবে বুঝবেন

has address, mail is handled by এবং name server ধরনের লাইনে record-এর ফল পাওয়া যায়। output-এ দেখানো record type খেয়াল করুন।

#### মনে রাখুন

সব OS-এ আগে থেকে ইনস্টল থাকে না। একাধিক resolver-এর উত্তর cache ও DNS propagation-এর কারণে আলাদা হতে পারে।

### 17. ipconfig /flushdns

**প্ল্যাটফর্ম:** Windows

Windows-এর স্থানীয় DNS resolver cache পরিষ্কার করে। পুরোনো cached উত্তর থাকলে পরের lookup-এ resolver-এর কাছে নতুন প্রশ্ন করার সুযোগ তৈরি হয়।

#### মূল ব্যবহার

```text
ipconfig /flushdns
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. DNS cache পরিষ্কার

```text
ipconfig /flushdns
```

2. পরিষ্কারের পরে cache দেখুন

```text
ipconfig /flushdns && ipconfig /displaydns
```

3. পরিষ্কারের পরে lease renew

```text
ipconfig /flushdns && ipconfig /renew
```

4. PowerShell থেকে elevated command

```text
Start-Process cmd -ArgumentList "/c ipconfig /flushdns" -Verb RunAs
```

5. পরিষ্কারের পরে ping

```text
ipconfig /flushdns && ping example.com
```

#### ফলাফল কীভাবে বুঝবেন

Successfully flushed বার্তা সফলতার ইঙ্গিত। /displaydns দিয়ে cache দেখুন; hosts file বা চলমান অ্যাপের কারণে entry আবার দেখা যেতে পারে।

#### মনে রাখুন

এখানে && উদাহরণগুলো cmd.exe-এর জন্য। এটি একটির পর আরেকটি চালায়, একই সঙ্গে নয়। browser বা বাইরের DNS server-এর cache এতে পরিষ্কার হয় না।

## 5. কানেকশন ও পোর্ট বিশ্লেষণ

### 18. netstat

**প্ল্যাটফর্ম:** Linux

সংযোগ, listening socket, interface counter ও route দেখতে ব্যবহৃত হয়। Linux-এ আধুনিক বিকল্প হিসেবে ss-ও প্রচলিত।

#### মূল ব্যবহার

```text
netstat -an
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. সব socket সংখ্যায়

```text
netstat -an
```

2. TCP socket

```text
netstat -at
```

3. listening port ও process

```text
netstat -tulpn
```

4. interface counter

```text
netstat -i
```

5. routing table

```text
netstat -r
```

#### ফলাফল কীভাবে বুঝবেন

Local Address, Foreign Address ও State দেখুন। LISTEN সেবা অপেক্ষমাণ থাকার ইঙ্গিত; ESTABLISHED সক্রিয় TCP connection। UDP-তে একই state মডেল নেই।

#### মনে রাখুন

এখানকার অপশন Linux-এর। -tulpn শুধু listening TCP/UDP socket দেখায়; process তথ্যের জন্য sudo লাগতে পারে। -i মূলত packet/error counter দেখায়।

### 19. nmap

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

অনুমোদিত নেটওয়ার্কে host discovery, port status ও service identification করতে ব্যবহার করা হয়। পর্যবেক্ষণের গভীরতা অনুযায়ী scan-এর প্রভাব বদলায়।

#### মূল ব্যবহার

```text
nmap 192.168.1.1
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. সাধারণ ১০০০ TCP port

```text
nmap 192.168.1.1
```

2. subnet-এ host discovery

```text
nmap -sn 192.168.1.0/24
```

3. নির্দিষ্ট port-এ SYN scan

```text
sudo nmap -sS -p 22,80,443 192.168.1.1
```

4. service version শনাক্ত

```text
nmap -sV 192.168.1.1
```

5. অনুমোদিত vulnerability script

```text
nmap --script vuln 192.168.1.1
```

#### ফলাফল কীভাবে বুঝবেন

open মানে সেবা শুনছে, closed মানে পৌঁছানো গেছে কিন্তু listener নেই, filtered মানে filtering-এর কারণে সিদ্ধান্ত সীমিত। version detection অনুমানও হতে পারে।

#### মনে রাখুন

শুধু নিজের বা লিখিত অনুমতিপ্রাপ্ত target-এ চালান। vuln-category script intrusive হতে পারে; scope, maintenance window ও backup যাচাই করুন।

## 6. ফাইল ট্রান্সফার ও রিমোট অ্যাক্সেস

### 20. curl

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

URL ব্যবহার করে ডেটা নেয় বা পাঠায়। ওয়েব পেজ, download, HTTP header ও API request পরীক্ষা করার জন্য কার্যকর।

#### মূল ব্যবহার

```text
curl https://example.com
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ওয়েব পেজ আনুন

```text
curl https://example.com
```

2. নাম দিয়ে download

```text
curl -o output.zip https://example.com/file.zip
```

3. redirect অনুসরণ

```text
curl -L http://example.com
```

4. JSON POST request

```text
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com/endpoint
```

5. HEAD দিয়ে header দেখুন

```text
curl -I https://example.com
```

#### ফলাফল কীভাবে বুঝবেন

ডিফল্টভাবে response body দেখা যায়। -I দিয়ে header-এ HTTP status দেখুন। transfer সফল হলেই HTTP 404/500-কে curl সবসময় failure ধরে না; প্রয়োজনে --fail ব্যবহার করুন।

#### মনে রাখুন

JSON উদাহরণের quoting POSIX shell-এর জন্য। গোপন token command history-তে রাখবেন না। -I হলো HEAD request; server GET-এর চেয়ে ভিন্ন আচরণ করতে পারে।

### 21. wget

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

ফাইল download, resume এবং website mirroring-এর কাজে ব্যবহৃত non-interactive টুল। স্ক্রিপ্ট ও দীর্ঘ download-এ সুবিধাজনক।

#### মূল ব্যবহার

```text
wget https://example.com/file.zip
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ফাইল download

```text
wget https://example.com/file.zip
```

2. নতুন filename

```text
wget -O newname.zip https://example.com/file.zip
```

3. background download

```text
wget -b https://example.com/largefile.iso
```

4. অসমাপ্ত download চালু

```text
wget -c https://example.com/largefile.iso
```

5. অনুমোদিত site mirror

```text
wget --mirror -p --convert-links -P ./local_dir https://example.com
```

#### ফলাফল কীভাবে বুঝবেন

progress, HTTP status, saved filename ও wget-log দেখুন। resume কাজ করতে server-এর range support ও অপরিবর্তিত remote file প্রয়োজন হতে পারে।

#### মনে রাখুন

mirror করার আগে অনুমতি, robots policy, storage ও server load বিবেচনা করুন। উদাহরণের URL কেবল placeholder; বাস্তব archive সেখানে নাও থাকতে পারে।

### 22. ssh

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

এনক্রিপ্টেড সংযোগে remote login, command execution ও port forwarding দেয়। সঠিক host identity যাচাই করা নিরাপত্তার গুরুত্বপূর্ণ অংশ।

#### মূল ব্যবহার

```text
ssh user@192.168.1.100
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. remote login

```text
ssh user@192.168.1.100
```

2. নির্দিষ্ট private key

```text
ssh -i ~/.ssh/id_rsa user@example.com
```

3. একটি remote command

```text
ssh user@192.168.1.100 "uptime"
```

4. local port forwarding

```text
ssh -L 8080:localhost:80 user@remote-server
```

5. বিস্তারিত debug output

```text
ssh -v user@192.168.1.100
```

#### ফলাফল কীভাবে বুঝবেন

প্রথমবার host key fingerprint যাচাই করুন। Permission denied authentication সমস্যার, আর timeout সাধারণত connectivity বা filtering সমস্যার ইঙ্গিত।

#### মনে রাখুন

private key শেয়ার করবেন না। -L উদাহরণে localhost দূরের server-এর loopback বোঝায়। remote username স্পষ্টভাবে user দেওয়া আছে; এটি স্বয়ংক্রিয় current user নয়।

### 23. scp

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

SSH-এর মাধ্যমে local ও remote machine-এর মধ্যে ফাইল কপি করে। আধুনিক OpenSSH-এ scp সাধারণত SFTP protocol ব্যবহার করে।

#### মূল ব্যবহার

```text
scp file.txt user@192.168.1.100:/home/user/
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. local থেকে remote

```text
scp file.txt user@192.168.1.100:/home/user/
```

2. remote থেকে local

```text
scp user@192.168.1.100:/home/user/file.txt .
```

3. folder recursive copy

```text
scp -r myfolder/ user@192.168.1.100:/var/www/
```

4. private key নির্বাচন

```text
scp -i ~/.ssh/id_rsa file.txt user@example.com:/tmp/
```

5. bandwidth সীমা

```text
scp -l 800 file.txt user@192.168.1.100:/tmp/
```

#### ফলাফল কীভাবে বুঝবেন

progress, transfer rate ও error দেখুন। কাজ শেষে remote path বা local file যাচাই করুন; গুরুত্বপূর্ণ ফাইলের hash তুলনা করা ভালো।

#### মনে রাখুন

-r recursive copy করে; -l-এর unit Kbit/s। path ও permission ঠিক আছে কি না দেখুন। SSH-এর port বদলাতে scp-তে বড় হাতের -P ব্যবহৃত হয়।

### 24. sftp

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

SSH transport-এর ওপর interactive file transfer session চালায়। local ও remote directory আলাদা রেখে upload ও download করা যায়।

#### মূল ব্যবহার

```text
sftp user@192.168.1.100
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. server-এ সংযোগ

```text
sftp user@192.168.1.100
```

2. ফাইল upload

```text
put localfile.txt /remote/path/
```

3. ফাইল download

```text
get remotefile.txt /local/path/
```

4. remote file list

```text
ls
```

5. folder download

```text
get -r /remote/folder/
```

#### ফলাফল কীভাবে বুঝবেন

sftp> prompt পাওয়া গেলে session প্রস্তুত। pwd remote ও lpwd local directory দেখায়। put upload এবং get download করে।

#### মনে রাখুন

put, get ও ls কমান্ডগুলো SFTP prompt-এর ভেতরে লিখতে হবে। recursive download-এ storage ও permission আগে পরীক্ষা করুন। বের হতে bye লিখুন।

## 7. প্যাকেট ক্যাপচার ও বিশ্লেষণ

### 25. tcpdump

**প্ল্যাটফর্ম:** Linux

terminal থেকেই packet capture ও packet header বিশ্লেষণ করা যায়। GUI ছাড়া server-এ সীমিত diagnostic capture নিতে বিশেষভাবে কাজে লাগে।

#### মূল ব্যবহার

```text
tcpdump -D
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. ইন্টারফেসের তালিকা

```text
tcpdump -D
```

2. ১০টি packet দেখুন

```text
sudo tcpdump -i eth0 -c 10 -nn
```

3. DNS traffic filter

```text
sudo tcpdump -i eth0 -nn port 53
```

4. ১০০ packet ফাইলে রাখুন

```text
sudo tcpdump -i eth0 -c 100 -w capture.pcap
```

5. pcap ফাইল পড়ুন

```text
tcpdump -nn -r capture.pcap
```

#### ফলাফল কীভাবে বুঝবেন

সময়, source, destination, protocol ও port দেখুন। শেষে captured, received by filter ও dropped by kernel counter পরীক্ষা করুন। -nn নাম ও service resolution বন্ধ রাখে।

#### মনে রাখুন

capture-এ ব্যক্তিগত বা সংবেদনশীল তথ্য থাকতে পারে। অনুমতি নিয়ে সীমিত packet count ও filter ব্যবহার করুন। pcap নিরাপদে রাখুন; eth0 নিজের interface দিয়ে বদলান।

### 26. wireshark

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

গ্রাফিক্যাল packet analyzer। packet list, protocol tree ও raw bytes একসঙ্গে দেখে ট্রাফিকের গঠন এবং protocol-level আচরণ বোঝা যায়।

#### মূল ব্যবহার

```text
wireshark
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. GUI খুলুন

```text
wireshark
```

2. পুরোনো capture খুলুন

```text
wireshark capture.pcap
```

3. তাৎক্ষণিক capture

```text
wireshark -i eth0 -k
```

4. পোর্ট ৪৪৩ capture filter

```text
wireshark -i eth0 -k -f "port 443"
```

5. ফাইলে HTTP request display filter

```text
wireshark -r capture.pcap -Y "http.request"
```

#### ফলাফল কীভাবে বুঝবেন

capture filter সংগ্রহের আগেই traffic সীমিত করে; display filter সংগৃহীত packet-এর কোনগুলো দেখা যাবে তা ঠিক করে। http.request সাধারণত plaintext HTTP request দেখায়।

#### মনে রাখুন

GUI চালু করতে desktop session প্রয়োজন। capture privilege আলাদাভাবে configure করুন; পুরো GUI root হিসেবে চালানো এড়িয়ে চলুন। TLS-encrypted HTTP সাধারণত সরাসরি পড়া যায় না।

## 8. ফায়ারওয়াল ও নেটওয়ার্ক ব্যবস্থাপনা

### 27. iptables

**প্ল্যাটফর্ম:** Linux

Linux firewall-এর rule chain পরিচালনা করে। incoming traffic-এর জন্য INPUT chain এবং rule-এর ক্রম বিশেষ গুরুত্বপূর্ণ।

#### মূল ব্যবহার

```text
sudo iptables -L -n -v --line-numbers
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. rule ও line number

```text
sudo iptables -L -n -v --line-numbers
```

2. source IP block

```text
sudo iptables -A INPUT -s 192.168.1.50 -j DROP
```

3. SSH traffic অনুমোদন

```text
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

4. দ্বিতীয় rule মুছুন

```text
sudo iptables -D INPUT 2
```

5. INPUT chain flush

```text
sudo iptables -F INPUT
```

#### ফলাফল কীভাবে বুঝবেন

-L -n -v output-এ policy, target, source/destination ও packet/byte counter দেখুন। আগে মিলে যাওয়া rule পরের rule-এর ফল বদলে দিতে পারে।

#### মনে রাখুন

পরিবর্তনের আগে sudo iptables-save দিয়ে backup নিন। -A শেষে rule যোগ করে; আগে DROP থাকলে পরে ACCEPT কাজ নাও করতে পারে। -F default policy বদলায় না, ফলে lockout-ও হতে পারে।

### 28. netsh

**প্ল্যাটফর্ম:** Windows

Windows-এর network configuration পরিচালনার command-line utility। wireless profile, IP setup ও firewall status দেখা বা পরিবর্তন করা যায়।

#### মূল ব্যবহার

```text
netsh wlan show profiles
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. wireless profile

```text
netsh wlan show profiles
```

2. configuration export

```text
netsh interface ip dump > C:\backup\netconfig.txt
```

3. firewall reset

```text
netsh advfirewall reset
```

4. static IP নির্ধারণ

```text
netsh interface ip set address "Ethernet" static 192.168.1.100 255.255.255.0 192.168.1.1
```

5. firewall profile দেখুন

```text
netsh advfirewall show allprofiles
```

#### ফলাফল কীভাবে বুঝবেন

interface নাম, IP, gateway ও firewall profile মিলিয়ে দেখুন। export command ফাইলে configuration script রাখে; এটি সব Windows network state-এর পূর্ণ backup নয়।

#### মনে রাখুন

পরিবর্তনে Administrator terminal লাগতে পারে। C:\backup directory আগে তৈরি করুন। static IP দেওয়ার আগে conflict পরীক্ষা করুন; firewall reset custom rule সরিয়ে দেয়।

### 29. netsh advfirewall

**প্ল্যাটফর্ম:** Windows

Windows Defender Firewall-এর profile ও rule পরিচালনার জন্য netsh-এর বিশেষ context। নির্দিষ্ট port-এর inbound access নিয়ন্ত্রণ করা যায়।

#### মূল ব্যবহার

```text
netsh advfirewall show allprofiles
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. profile status

```text
netsh advfirewall show allprofiles
```

2. সব profile-এ firewall চালু

```text
netsh advfirewall set allprofiles state on
```

3. TCP 8080 inbound rule

```text
netsh advfirewall firewall add rule name="Allow 8080" dir=in action=allow protocol=TCP localport=8080
```

4. নাম দিয়ে rule মুছুন

```text
netsh advfirewall firewall delete rule name="Allow 8080"
```

5. default firewall configuration

```text
netsh advfirewall reset
```

#### ফলাফল কীভাবে বুঝবেন

Domain, Private ও Public profile-এর state এবং rule-এর direction, action, protocol ও localport পরীক্ষা করুন। firewall ছাড়াও application listener থাকা দরকার।

#### মনে রাখুন

rule যোগে least privilege অনুসরণ করুন। reset করলে custom exception হারাতে পারে। একই নামের একাধিক rule থাকলে delete command একাধিক matching rule মুছতে পারে।

## 9. ইন্টারনেট পারফরম্যান্স পরীক্ষা

### 30. speedtest-cli

**প্ল্যাটফর্ম:** Linux / macOS / Windows — ইনস্টলেশনভেদে

Speedtest.net ব্যবহার করে download, upload ও latency-এর আনুমানিক পরীক্ষা করে। এটি Python-ভিত্তিক third-party speedtest-cli; official Ookla speedtest আলাদা program।

#### মূল ব্যবহার

```text
speedtest-cli
```

#### পাঁচটি ব্যবহারিক উদাহরণ

1. সাধারণ speed test

```text
speedtest-cli
```

2. সংক্ষিপ্ত ফল

```text
speedtest-cli --simple
```

3. server list

```text
speedtest-cli --list
```

4. নির্দিষ্ট server

```text
speedtest-cli --server 1234
```

5. shareable result URL

```text
speedtest-cli --share
```

#### ফলাফল কীভাবে বুঝবেন

Ping, Download ও Upload ফল দেখুন। server, Wi-Fi signal, VPN, CPU ও একই সময়ে অন্য download-এর কারণে ফল বদলাতে পারে।

#### মনে রাখুন

পরীক্ষায় ডেটা খরচ হয়। একই server ও কাছাকাছি পরিবেশে একাধিক ফল তুলনা করুন। --server 1234 কেবল উদাহরণ; --list থেকে বৈধ ID নিন। service compatibility বদলাতে পারে।

## শেষকথা ও যোগাযোগ

বইটি পড়ার জন্য ধন্যবাদ। নেটওয়ার্কিং শেখার সবচেয়ে কার্যকর পথ হলো ধারণা বোঝা, নিরাপদ ল্যাবে অনুশীলন করা এবং নিজের পর্যবেক্ষণ লিখে রাখা। ছোট ছোট পরীক্ষা থেকেই বড় সমস্যার সমাধান করার দক্ষতা তৈরি হয়।

এই বইয়ের কমান্ডগুলো নিজের ল্যাবে প্রয়োগ করুন। কী পরীক্ষা করছেন, কী ফল আশা করছেন এবং বাস্তবে কী পেলেন—এই তিনটি বিষয় নোট করুন। ভুল হলে কারণ খুঁজুন, প্রয়োজনীয় পরিবর্তন করুন এবং আবার পরীক্ষা করুন।

### সঙ্গে থাকুন

নিচের লিংকগুলো দিয়ে আমার প্রোফাইল ও ল্যাব রিপোজিটরিতে যেতে পারবেন। শেখার অভিজ্ঞতা, গঠনমূলক পরামর্শ ও মতামত জানাতে LinkedIn-এ যোগাযোগ করতে পারেন।

- [GitHub — MaksBloxX](https://github.com/MaksBloxX)
- [GitHub Repo — Cisco Packet Tracer Lab](https://github.com/MaksBloxX/Cisco-Packet-Tracer-Lab)
- [LinkedIn — Md. Makshedul Islam](https://www.linkedin.com/in/md-makshedul-islam-765130406)

### শেখা চলুক, অনুশীলন চলুক।

Md. Makshedul Islam

Student, EXIM Bank Agricultural University Bangladesh.

**MaksDev Studio**

---

> **নেভিগেশন:** [📚 Reference Library](README.md) · [🏠 রেপো হোম](../README.md) · [📥 **PDF ডাউনলোড**](MaksDev-Practical-Networking.pdf) · [পরের বই: OSI Illustrated ➡](OSI-Illustrated.md)
