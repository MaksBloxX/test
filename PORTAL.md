# 🌐 v4.0 Web Portal · Build, Preview and Publish

> **নেভিগেশন:** [🏠 বাংলা হোম](README.md) · [🏆 v4 বাংলা capstone](capstone/README.md) · [English capstone](en/capstone/README.md) · [🎞️ GIF Search Catalog](GIF-CATALOG.md) · [🗺️ Roadmap](ROADMAP.md)

![বাঙলা ও English কোর্স, Extra Lab, `.pkt` ফাইল এবং স্ক্রিপ্টের ভিজ্যুয়াল মানচিত্র।](assets/diagrams/repo-overview.svg)

[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) পোর্টালে আগের **৯২টি Markdown page** (মূল ৪৯ + English ৩৯ + ৪টি resource/index) এবং v4.0-এ **আরও ৪টি** ([বাংলা capstone](capstone/README.md), [English capstone](en/capstone/README.md), [খালি PT evidence log](capstone/VERIFICATION.md), [নিজের `.pkt` বানানোর নির্দেশ](pkt-files/capstone/README.md))—মোট **৯৬টি page**। নতুন `🏆 v4.0 Capstone` nav-এ চারটি পাতা পাওয়া যাবে। Light/Dark toggle, পুরো সাইটে client-side search, code block `Copy`, sidebar ও mobile layout আছে। বাংলা শব্দ (exact/Unicode term) এবং English term index-এ থাকে; English-এ stemming আছে, বাংলায় একই morphological stemming নিশ্চিত নয়। **GitHub Pages live/push যাচাই করা হয়নি; local build ও gated workflow প্রস্তুত।**

> **বাস্তবতা ও সীমা:** ২৬টি GIF (প্রতিটি ৩০ সেকেন্ডের) মূল SVG থেকে আঁকা conceptual walkthrough, আসল Packet Tracer recording নয়। আগের ১৮টি `.pkt` অপরিবর্তিত; **Phase 3/5-এর নতুন native `.pkt` নেই**। v4 capstone-এর config/diagram/worksheet PT-তে এখানে চালানো হয়নি; `Expected` ফল actual evidence নয়। DAI enforcement নিশ্চিত নয়। ৩৫টি English pages **curated adaptations**, আক্ষরিক অনুবাদ নয়; নতুন English capstone একটি আলাদা build guide।

## 💻 লোকাল ওয়েবসাইট চালাও

রেপোর root directory-তে Python **3.11+** দিয়ে:

```bash
python3 -m pip install -r requirements-docs.txt
python3 scripts/english_track_generator.py --check
python3 scripts/gif_walkthrough_generator.py --check
python3 scripts/capstone_config_generator.py --check
python3 scripts/portal_docs.py
python3 -m mkdocs build --strict -f mkdocs.yml
python3 -m mkdocs serve -f mkdocs.yml -a 0.0.0.0:8000
```

লোকাল browser-এ `http://localhost:8000/` খুলবে (এই sandbox-এর live preview-এর host ভিন্ন হতে পারে)। [`scripts/portal_docs.py`](scripts/portal_docs.py) source files stage করে: সাইট তৈরি হয় `build/site/`-এ; public guide ও assets কপি হয় `build/docs/`-এ। দুটো generated directory `.gitignore`-এ বাদ—**সম্পাদনা সবসময় মূল `.md`, `en/*.yml`, `capstone/plan.json`, `assets/diagrams/*.svg`-র generator বা `portal/assets/css/portal.css`-এ করবে**, `build/`-এ নয়। GitHub README-র HTML টেবিলের `.md` লিংক শুধু staged কপিতে website-এর সুন্দর `/` URL-এ রূপান্তরিত হয়; source Markdown-এর GitHub লিংক অক্ষত থাকে। Site snapshot বা release archive-এ generated build ঢোকানোর প্রয়োজন নেই।

| উৎস | কী পরিবর্তন করবে | তারপর কী চালাবে |
| :--- | :--- | :--- |
| [`en/lessons.yml`](en/lessons.yml), [`en/ccna-fundamentals.yml`](en/ccna-fundamentals.yml), [`en/Extras.yml`](en/Extras.yml) | English guide-এর নিজস্ব অনুচ্ছেদ, steps, check বা answer | [`english_track_generator.py`](scripts/english_track_generator.py) → `--check` |
| [`scripts/diagram_generator.py`](scripts/diagram_generator.py) | আগের ৫৬টি SVG topology/IP label | SVG regenerate → [`gif_walkthrough_generator.py`](scripts/gif_walkthrough_generator.py) → `--check` |
| [`capstone/plan.json`](capstone/plan.json), [`capstone_config_generator.py`](scripts/capstone_config_generator.py) | v4 চার WAN, role-wise config/IP ও দুটি নতুন SVG | plan সংশোধন → `capstone_config_generator.py --write` → `--check` → **নিজের PT-তে পুনরায় পরীক্ষা** |
| [`GIF-CATALOG.md`](GIF-CATALOG.md) | GIF search topic নাম/importance; নিজের legal replacement-এর উৎস ও attribution | নতুন GIF/manifest মিলিয়ে `repo_doctor.py --strict` |
| [`mkdocs.yml`](mkdocs.yml), [`portal.css`](portal/assets/css/portal.css), [`language.js`](portal/assets/js/language.js) | Nav, Material style, theme/search ও English page-এর `lang`/search label | `portal_docs.py` → `mkdocs build --strict` |
| [`requirements-docs.txt`](requirements-docs.txt) | Site ও GIF generator-এর ঐচ্ছিক dependency | ইন্সটল → সম্পূর্ণ পরীক্ষা |

**Search:** MkDocs Material-এর একক search index-এ বাংলা/English উভয় corpus। `theme.language: bn` থাকায় control labels বাংলায়, English section-এ সমস্ত বিষয়বস্তু English এবং প্রতি পাতায় original-এর language-switch link আছে। বাংলা যুক্তাক্ষর/বানান ভিন্ন হলে প্রথমে একটি মূল শব্দ বা English command name লিখে খোঁজো। Built site-এ `search/search_index.json`-এ দুই ভাষার guide আছে কি না পরীক্ষা করো।

**Copy button:** Material-এর `content.code.copy` feature; ক্লিপবোর্ডে নেওয়ার আগে block-এর `IOS`, `PC`, `shell` ও `R1/R2/SW1` role অবশ্যই দেখবে। GitHub Markdown-এ এই website-only button নেই; command content থাকে।

## 🚀 GitHub Pages-এ প্রকাশ

এই রেপোতে `.github/workflows/pages.yml`-এ PR-তে `mkdocs build --strict` পরীক্ষা এবং **main branch-এ push হলে** GitHub Actions Pages artifact upload/deploy কনফিগার আছে। প্রকাশের জন্য repo maintainer-কে:

1. GitHub-এর **Settings → Pages → Build and deployment → Source: GitHub Actions** নির্বাচন করতে হবে।
2. এই v4.0 source `main` branch-এ push করতে হবে; কেবল লোকাল commit/ZIP থাকলে website live হয় না।
3. Pages workflow সফল হয়েছে কি না এবং প্রকাশিত URL আসলেই খোলে কি না পরীক্ষা করতে হবে। `mkdocs.yml`-এ সম্ভাব্য `site_url` দেওয়া আছে; live URL যাচাইয়ের আগে এটিকে live-দাবি মনে কোরো না।
4. অন্য repo name/owner ব্যবহার করলে `mkdocs.yml`-এ `repo_url` ও `site_url` বদলাতে হবে।

**গোপনীয়তা/সুরক্ষা:** Repo-তে কোনো নতুন API token রাখা নেই। Pages action GitHub-এর স্বল্পমেয়াদি `GITHUB_TOKEN` permissions ব্যবহার করবে; workflow থেকে বাহ্যিক translator বা image-search download হয় না। বাহিরের GIF upload করলে ব্যবহারের অনুমতি ও credit যোগ করুন।

**Check before a PR:**

```bash
python3 scripts/diagram_generator.py --check
python3 scripts/gif_walkthrough_generator.py --check
python3 scripts/english_track_generator.py --check
python3 scripts/capstone_config_generator.py --check
python3 scripts/repo_doctor.py --strict
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/portal_docs.py && python3 -m mkdocs build --strict -f mkdocs.yml
```

> **পরের ধাপ:** [v4 বাংলা build-along](capstone/README.md) · [English build-along](en/capstone/README.md) · [GIF topics](GIF-CATALOG.md) · [মূল README](README.md)
