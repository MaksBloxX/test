# 🔧 Troubleshooting Fault-Injection Scripts (`pkt-files/troubleshooting/`)

> **নেভিগেশন:** [🧰 সব .pkt ক্যাটালগ](../README.md) · [🕵️ Broken Labs Challenge গাইড](../../Extras/broken-labs-challenge.md) · [🛠️ লেসন ১২ · Problem Bank](../../lessons/12-problem-solve.md) · [🏠 রেপো হোম](../../README.md)

এই ফোল্ডারে রয়েছে **৬টি বাস্তবধর্মী ভাঙা কনফিগারেশন স্ক্রিপ্ট (`.ios`)**। এগুলো তোমার চালু থাকা Packet Tracer ল্যাবের রাউটার/সুইচে পেস্ট করলেই লুকানো বাগ তৈরি হবে — যা দেখে তুমি বাস্তব পরীক্ষার মতো ট্রাবলশুটিং অনুশীলন করতে পারবে!

> ⚠️ **স্পয়লার সতর্কতা:** চ্যালেঞ্জের মজা নষ্ট না করতে ফাইলগুলোর ভেতরের কোড আগে থেকে না পড়ে সরাসরি কপি-পেস্ট করো, তারপর **[🕵️ Broken Network Detective Challenge](../../Extras/broken-labs-challenge.md)** গাইড দেখে সমাধান করো!

---

### 🖼️ চিত্রে বোঝো: `.pkt` ল্যাবের সঙ্গে `.ios` ফল্ট স্ক্রিপ্ট

![`.pkt` ল্যাবের সঙ্গে `.ios` ফল্ট স্ক্রিপ্ট — `.ios` কোনো `.pkt` প্রজেক্ট নয়; চলমান ল্যাবের ঠিক ডিভাইসের CLI-তে কমান্ড পেস্ট করো।](../../assets/diagrams/pkt-fault-script-workflow.svg)

> **ছবির সারকথা:** `.ios` কোনো `.pkt` প্রজেক্ট নয়; চলমান ল্যাবের ঠিক ডিভাইসের CLI-তে কমান্ড পেস্ট করো।

---

## 📂 ৬টি ফল্ট স্ক্রিপ্ট তালিকা

| কেস | স্ক্রিপ্ট ফাইল | কোন `.pkt`/টপোলজিতে পেস্ট করবে | কোন ডিভাইসে |
| :---: | :--- | :--- | :---: |
| **০১** | [`broken-01-static-routing.ios`](broken-01-static-routing.ios) | [`lesson-02-static-routing.pkt`](../labs/lesson-02-static-routing.pkt) | `R2` CLI |
| **০২** | [`broken-02-dhcp-starvation.ios`](broken-02-dhcp-starvation.ios) | [`lesson-03-dhcp.pkt`](../labs/lesson-03-dhcp.pkt) | `R1` CLI |
| **০৩** | [`broken-03-roas-vlan.ios`](broken-03-roas-vlan.ios) | [`lesson-06-trunk-inter-vlan.pkt`](../labs/lesson-06-trunk-inter-vlan.pkt) | `R1` CLI |
| **০৪** | [`broken-04-etherchannel-stp.ios`](broken-04-etherchannel-stp.ios) | [`lesson-07-switching.pkt`](../labs/lesson-07-switching.pkt) | `SW1` ও `SW2` CLI |
| **০৫** | [`broken-05-ospf-adjacency.ios`](broken-05-ospf-adjacency.ios) | [লেসন ১৩ · OSPF টপোলজি](../../lessons/13-dynamic-routing-ospf.md) | `R2` CLI |
| **০৬** | [`broken-06-ssh-lockout.ios`](broken-06-ssh-lockout.ios) | [লেসন ১৫ · SSH টপোলজি](../../lessons/15-ssh-syslog-ntp.md) | `R1` CLI |

---

> **নেভিগেশন:** [🧰 সব .pkt ক্যাটালগ](../README.md) · [🕵️ Broken Labs Challenge গাইড](../../Extras/broken-labs-challenge.md) · [🏠 রেপো হোম](../../README.md)
