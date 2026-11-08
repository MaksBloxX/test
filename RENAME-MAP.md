# 📁 RENAME-MAP — পুরনো নাম → নতুন নাম

> **নেভিগেশন:** [🏠 হোম](README.md)
>
> এই ফাইলে দেওয়া আছে রিপোজিটরি রিস্ট্রাকচারের সময় কোন পুরনো ফাইলের নাম/লোকেশন কোথায় গেছে। লিংক বা বুকমার্ক ভেঙে থাকলে এখান থেকে মেলাও।

## 🧭 কেন পরিবর্তন করা হলো?

| সমস্যা | সমাধান |
| :--- | :--- |
| সব ফাইল root-এ এলোমেলো | `lessons/`, `reference/`, `pkt-files/` ফোল্ডারে সাজানো হয়েছে |
| ফাইলের নামে Space, `#`, `—` (em-dash) — লিংক ভাঙে | `kebab-case` স্বচ্ছ নাম (কোনো special character নেই) |
| নম্বরিং এলোমেলো (`#1.2`, `#2.1`, `#2`) | সিরিয়াল `01` → `08` |
| প্রতিটি Lesson + তার Practical আলাদা ফাইলে একই কনটেন্ট (**Duplicate**) | একটিমাত্র সম্পূর্ণ লেসনে **Merge** (ধারণা → ল্যাব → ভেরিফিকেশন → ট্রাবলশুটিং) |
| `Mash_topology.pkt` — ভুল বানান (সঠিক: **Mesh**) | `mesh-topology.pkt` |
| Lesson 8 আসলে Lesson নয়, Command Encyclopedia | `reference/cli-command-cheatsheet.md` |

---

## 📝 Markdown ফাইল (লেসন)

| পুরনো নাম (root-এ) | নতুন নাম | নোট |
| :--- | :--- | :--- |
| `Router CLI CMD Formula #1.md` | [`lessons/01-router-cli-basics.md`](lessons/01-router-cli-basics.md) | এর সাথে `Basic Network Lab #1.2.md` **Merge** |
| `Basic Network Lab #1.2.md` | [`lessons/01-router-cli-basics.md`](lessons/01-router-cli-basics.md) | ↑ এর সাথে Merge (Duplicate দূর) |
| `Two Routers + Static Routing #2.md` | [`lessons/02-static-routing.md`](lessons/02-static-routing.md) | এর সাথে `Integrated Practical Lab #2.1.md` **Merge** |
| `Integrated Practical Lab #2.1.md` | [`lessons/02-static-routing.md`](lessons/02-static-routing.md) | ↑ Merge (Duplicate দূর) |
| `Router DHCP Config #3.md` | [`lessons/03-dhcp.md`](lessons/03-dhcp.md) | এর সাথে `#3.1` **Merge** |
| `Integrated Practical Lab #3.1.md` | [`lessons/03-dhcp.md`](lessons/03-dhcp.md) | ↑ Merge (Duplicate দূর) |
| `DNS Server Address #4.md` | [`lessons/04-dns-http-server.md`](lessons/04-dns-http-server.md) | এর সাথে `#4.1` **Merge** |
| `Integrated Practical Lab #4.1.md` | [`lessons/04-dns-http-server.md`](lessons/04-dns-http-server.md) | ↑ Merge (Duplicate দূর) |
| `VLAN Config #5.md` | [`lessons/05-vlan.md`](lessons/05-vlan.md) | এর সাথে `#5.1` **Merge** |
| `Integrated Practical Lab #5.1.md` | [`lessons/05-vlan.md`](lessons/05-vlan.md) | ↑ Merge (Duplicate দূর) |
| `Trunk Link & Inter-VLAN Routing #6.md` | [`lessons/06-trunk-inter-vlan.md`](lessons/06-trunk-inter-vlan.md) | নাম পরিষ্কার + Tags/Nav যোগ (6.1 আগে থেকেই ছিল না) |
| `Layer 2 Switch Technologies #7.md` | [`lessons/07-switching.md`](lessons/07-switching.md) | এর সাথে `#7.1` **Merge** |
| `Integrated Practical Lab #7.1.md` | [`lessons/07-switching.md`](lessons/07-switching.md) | ↑ Merge (Duplicate দূর) |
| `Integrated Practical Lab #8.1.md` | [`lessons/08-final-project.md`](lessons/08-final-project.md) | Final Project = লেসন ০৮ |
| `Cisco Packet Tracer — Final Lesson #8.md` | [`reference/cli-command-cheatsheet.md`](reference/cli-command-cheatsheet.md) | Lesson নয় — Cheat-Sheet/Reference |
| `README.md` (25 বাইট, প্রায় খালি) | [`README.md`](README.md) | সম্পূর্ণ নতুন ইনডেক্স + লিংক |

---

## 🧰 Packet Tracer ফাইল (.pkt)

| পুরনো নাম (root-এ) | নতুন নাম |
| :--- | :--- |
| `Bus_topology.pkt` | [`pkt-files/topologies/bus-topology.pkt`](pkt-files/topologies/bus-topology.pkt) |
| `Star_topology.pkt` | [`pkt-files/topologies/star-topology.pkt`](pkt-files/topologies/star-topology.pkt) |
| `Ring_topology.pkt` | [`pkt-files/topologies/ring-topology.pkt`](pkt-files/topologies/ring-topology.pkt) |
| `Mash_topology.pkt` | [`pkt-files/topologies/mesh-topology.pkt`](pkt-files/topologies/mesh-topology.pkt) ← **বানান সংশোধন** |
| `Tree_topology.pkt` | [`pkt-files/topologies/tree-topology.pkt`](pkt-files/topologies/tree-topology.pkt) |
| `Hybrid_topology.pkt` | [`pkt-files/topologies/hybrid-topology.pkt`](pkt-files/topologies/hybrid-topology.pkt) |
| `Network Topology using Router.pkt` | [`pkt-files/labs/lesson-01-router-cli-basics.pkt`](pkt-files/labs/lesson-01-router-cli-basics.pkt) ✅ |
| `Static Routing using two Router.pkt` | [`pkt-files/labs/lesson-02-static-routing.pkt`](pkt-files/labs/lesson-02-static-routing.pkt) ✅ |
| `IP Subnet Tester.pkt` | [`pkt-files/practice/ip-subnet-tester.pkt`](pkt-files/practice/ip-subnet-tester.pkt) |
| `Office Shared Printer Network.pkt` | [`pkt-files/practice/office-shared-printer-network.pkt`](pkt-files/practice/office-shared-printer-network.pkt) |

---

## 🔗 পুরনো লিংক ভেঙে গেছে?

পুরনো লিংকের ধরন: `Two%20Routers%20%2B%20Static%20Routing%20%232.md`
নতুন লিংক: `lessons/02-static-routing.md`

উপরের টেবিল থেকে নাম মিলিয়ে নাও — Git History-তে পুরনো ফাইলগুলোও সুরক্ষিত আছে।

---

> **নেভিগেশন:** [🏠 হোম](README.md)


---

## 🆕 নতুন যোগ হওয়া ফাইল (এই রিস্ট্রাকচারের পরে)

| ফাইল | কী |
| :--- | :--- |
| [`lessons/09-real-hardware.md`](lessons/09-real-hardware.md) | বাস্তব হার্ডওয়্যার পরিচিতি (আসল ছবিসহ) |
| [`lessons/10-practice-lab.md`](lessons/10-practice-lab.md) | Practice Lab — ৬০% Simple + ৪০% Hard, **সমাধানসহ** |
| [`lessons/11-practice-list.md`](lessons/11-practice-list.md) | Practice List — **সমাধান ছাড়া** Self-Practice |
| `lessons/images/*.jpg` | লেসন ০৯-এর Real Hardware ছবি |
| `lessons/12-problem-solve.md` | শেষ লেসন — Problem Solve (সমস্যা ও সমাধানের ব্যাংক) |
| `pkt-files/labs/lesson-03…08-*.pkt` | লেসন ০৩–০৮-এর ল্যাব ফাইল — কনভেনশন অনুযায়ী নামেই ✅ |
| `lessons/images/*.gif` | লেসন ০৬-এর 802.1Q Tagging ও Trunk ছাড়া VLAN Extending অ্যানিমেশন |

---

## 🎯 pkt ফাইল নামকরণ কনভেনশন (নতুন pkt বানানোর সময় মানো)

**নিয়ম:** `pkt-files/labs/lesson-NN-<লেসনের-নাম>.pkt` — ঠিক লেসন ফাইলের মতোই:

| লেসন ফাইল | মিলিয়ে pkt ফাইলের নাম |
| :--- | :--- |
| `lessons/03-dhcp.md` | `pkt-files/labs/lesson-03-dhcp.pkt` |
| `lessons/04-dns-http-server.md` | `pkt-files/labs/lesson-04-dns-http-server.pkt` |
| `lessons/05-vlan.md` | `pkt-files/labs/lesson-05-vlan.pkt` |
| `lessons/06-trunk-inter-vlan.md` | `pkt-files/labs/lesson-06-trunk-inter-vlan.pkt` |
| `lessons/07-switching.md` | `pkt-files/labs/lesson-07-switching.pkt` |
| `lessons/08-final-project.md` | `pkt-files/labs/lesson-08-final-project.pkt` |
| `lessons/12-problem-solve.md` | `pkt-files/labs/lesson-12-problem-solve.pkt` |

> এভাবে নাম রাখলে লেসন ↔ pkt ফাইল সবসময় জুড়ে যাবে — খুঁজতে সময় লাগবে না।

---

## 🚀 v2.0 ইকোসিস্টেম আপডেট লগ (নতুন সংযোজনসমূহ)

| নতুন ফাইল / ফোল্ডার | কাজ ও বিবরণ |
| :--- | :--- |
| [`ROADMAP.md`](ROADMAP.md) | ৩০ দিনের পূর্ণাঙ্গ স্টুডেন্ট স্টাডি প্ল্যান + ৭ দিনের ক্র্যাশ প্ল্যান + Phase 1–5 রেপো রোডম্যাপ |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | নতুন লেসন, ল্যাব বা সমস্যা যোগ করার কন্ট্রিবিউটর গাইড |
| [`lessons/README.md`](lessons/README.md) | ১২টি প্র্যাকটিক্যাল লেসনের ইনডেক্স ও প্রোগ্রেস চেকলিস্ট |
| [`Extras/README.md`](Extras/README.md) | ৫টি এক্সট্রা প্র্যাকটিক্যাল ল্যাবের সূচি |
| [`Extras/office-shared-printer-lab.md`](Extras/office-shared-printer-lab.md) | `office-shared-printer-network.pkt`-এর পূর্ণাঙ্গ বাংলা ল্যাব গাইড |
| [`Extras/ip-subnet-tester-lab.md`](Extras/ip-subnet-tester-lab.md) | `ip-subnet-tester.pkt`-এর হাতে-কলমে সাবনেটিং পরীক্ষা গাইড |
| [`Extras/network-topologies-lab.md`](Extras/network-topologies-lab.md) | ৬টি টপোলজি (`.pkt`)-এর ভিজ্যুয়াল ও Simulation Mode তুলনা গাইড |
| [`reference/README.md`](reference/README.md) | ২টি বাংলা নেটওয়ার্কিং ই-বুক (`.md` + `.pdf`), SVG গ্যালারি ও Cheat-Sheet ইনডেক্স |
| [`pkt-files/README.md`](pkt-files/README.md) | ১৮টি `.pkt` ফাইলের সম্পূর্ণ ক্যাটালগ |
| [`scripts/`](scripts/README.md) | ৫টি Python CLI টুল (`lab_writer.py`, `ios_config_generator.py`, `subnet_calculator.py`, `quiz_trainer.py`, `repo_doctor.py`) |
| `.github/workflows/repo-check.yml` | পুশ/PR-এ স্বয়ংক্রিয় লিংক ও স্ক্রিপ্ট যাচাইয়ের GitHub Actions CI |

---

> **নেভিগেশন:** [🏠 হোম](README.md) · [🗺️ রোডম্যাপ](ROADMAP.md) · [🛠️ স্ক্রিপ্ট গাইড](scripts/README.md)
