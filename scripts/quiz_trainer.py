#!/usr/bin/env python3
"""
quiz_trainer.py — Interactive CCNA MCQ & Cisco CLI Flashcard Trainer
Automatically loads all 68 real quizzes (MCQs + VLSM Q&As) from `ccna-fundamentals/*.md`!

Usage examples:
  python3 scripts/quiz_trainer.py --list
  python3 scripts/quiz_trainer.py --demo
  python3 scripts/quiz_trainer.py --count 5
  python3 scripts/quiz_trainer.py --lesson 5 --count 5
  python3 scripts/quiz_trainer.py --mode cli --count 5
"""

import argparse
import os
import random
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CCNA_DIR = os.path.join(REPO_ROOT, "ccna-fundamentals")

CLI_FLASHCARDS = [
    ("রাউটারের সব ইন্টারফেসের IP ও Status এক টেবিলে দেখার শর্টকাট কমান্ড কী?", "show ip interface brief (বা sh ip int br)"),
    ("Running কনফিগারেশন স্থায়ীভাবে NVRAM-এ সেভ করার কমান্ড কী?", "copy running-config startup-config (বা wr)"),
    ("সুইচে কোন VLAN-এ কোন পোর্ট আছে তা দেখার কমান্ড কী?", "show vlan brief"),
    ("দুই সুইচের মধ্যে 802.1Q Trunk চালু আছে কি না দেখার কমান্ড কী?", "show interfaces trunk"),
    ("Router-এ DHCP থেকে কোন পিসি কোন IP পেয়েছে তার লিজ টেবিল দেখার কমান্ড কী?", "show ip dhcp binding"),
    ("Port Security লঙ্ঘনের ফলে err-disabled হওয়া পোর্ট পুনরায় সচল করার ২টি কমান্ড কী?", "shutdown তারপর no shutdown"),
    ("LACP EtherChannel ঠিকমতো বান্ডেল ('SU') হয়েছে কি না দেখার কমান্ড কী?", "show etherchannel summary"),
    ("ভিন্ন সাবনেটে থাকা DHCP সার্ভারে ব্রডকাস্ট পাঠানোর রাউটার ইন্টারফেস কমান্ড কী?", "ip helper-address <DHCP_SERVER_IP>"),
]


def load_ccna_quizzes(lesson_filter: int | None = None, mcq_only: bool = False) -> list[dict]:
    quizzes = []
    if not os.path.isdir(CCNA_DIR):
        return quizzes

    opt_pattern = re.compile(r"^-\s*\*\*([A-D])\.\*\*\s*(.+)$", re.MULTILINE)
    ans_mcq_re = re.compile(r"\*\*✅\s*উত্তর:\s*([A-D])\b[^*]*\*\*")
    details_re = re.compile(r"<details>\s*<summary>.*?</summary>(.*?)</details>", re.DOTALL)

    for fn in sorted(os.listdir(CCNA_DIR)):
        if not fn.endswith(".md") or fn == "README.md":
            continue
        m_num = re.match(r"^(\d+)-", fn)
        lnum = int(m_num.group(1)) if m_num else 0
        if lesson_filter is not None and lnum != lesson_filter:
            continue

        txt = open(os.path.join(CCNA_DIR, fn), encoding="utf-8").read()
        chunks = re.split(r"(?=\*\*প্রশ্ন\s*[^\n*]+\.\*\*)", txt)

        for chunk in chunks[1:]:
            first_line, _, rest = chunk.partition("\n")
            m_head = re.match(r"\*\*প্রশ্ন\s*([^\.*]+)\.\*\*\s*(.+)", first_line.strip())
            if not m_head:
                continue
            q_no = m_head.group(1).strip()
            q_text = m_head.group(2).strip()

            before_details = rest.split("<details>", 1)[0]
            options = {k: v.strip() for k, v in opt_pattern.findall(before_details)}

            m_det = details_re.search(rest)
            if not m_det:
                continue
            det_body = m_det.group(1).strip()

            m_ans = ans_mcq_re.search(det_body)
            if options and m_ans:
                ans_letter = m_ans.group(1).upper()
                exp_part = det_body[m_ans.end():].strip()
                exp_part = re.sub(r"^\*\*🧠\s*কেন:\*\*\s*", "", exp_part).strip()
                exp_short = " ".join(
                    l.strip() for l in exp_part.splitlines() if l.strip() and not l.strip().startswith("```")
                )
                quizzes.append({
                    "type": "mcq",
                    "lesson": lnum,
                    "file": fn,
                    "num": q_no,
                    "question": q_text,
                    "options": options,
                    "answer": ans_letter,
                    "explanation": exp_short[:320] + ("…" if len(exp_short) > 320 else ""),
                })
            elif not mcq_only:
                exp_short = " ".join(l.strip() for l in det_body.splitlines() if l.strip())
                quizzes.append({
                    "type": "open",
                    "lesson": lnum,
                    "file": fn,
                    "num": q_no,
                    "question": q_text,
                    "options": {},
                    "answer": "",
                    "explanation": exp_short[:320] + ("…" if len(exp_short) > 320 else ""),
                })
    return quizzes


def print_summary() -> None:
    all_q = load_ccna_quizzes()
    by_file: dict[str, int] = {}
    for q in all_q:
        by_file[q["file"]] = by_file.get(q["file"], 0) + 1
    print("📚 CCNA Fundamentals কুইজ ব্যাংক সারাংশ:\n")
    for fn, cnt in sorted(by_file.items()):
        print(f"  • {fn:35s} : {cnt:2d} টি প্রশ্ন")
    print(f"\n  মোট অনুশীলন প্রশ্ন     : {len(all_q)} টি")
    print(f"  CLI শর্টকাট ফ্ল্যাশকার্ড : {len(CLI_FLASHCARDS)} টি")


def run_demo(lesson_filter: int | None, seed: int = 42) -> None:
    quizzes = load_ccna_quizzes(lesson_filter, mcq_only=True)
    rng = random.Random(seed)
    sample = rng.sample(quizzes, min(3, len(quizzes)))
    print(f"🎓 CCNA Quiz Trainer — নমুনা প্রশ্ন প্রিভিউ (মোট {len(quizzes)}টি MCQ থেকে ৩টি):\n")
    for idx, q in enumerate(sample, 1):
        print(f"[{idx}] ({q['file']} · প্রশ্ন {q['num']}) {q['question']}")
        for k in ("A", "B", "C", "D"):
            if k in q["options"]:
                print(f"    {k}. {q['options'][k]}")
        print(f"    ✅ সঠিক উত্তর: {q['answer']} ({q['options'].get(q['answer'], '')})")
        print(f"    🧠 কেন: {q['explanation']}\n")


def run_interactive_mcq(quizzes: list[dict], count: int) -> None:
    selected = random.sample(quizzes, min(count, len(quizzes)))
    score = 0
    mcq_total = 0
    print(f"\n🚀 শুরু হচ্ছে {len(selected)}টি প্রশ্নের কুইজ! (বের হতে 'q' লেখো)\n")
    for idx, q in enumerate(selected, 1):
        print("-" * 64)
        print(f"প্রশ্ন {idx}/{len(selected)} [লেসন ০{q['lesson']}]: {q['question']}\n")
        if q["type"] == "mcq":
            mcq_total += 1
            for k in ("A", "B", "C", "D"):
                if k in q["options"]:
                    print(f"  {k}) {q['options'][k]}")
            try:
                ans = input("\n👉 তোমার উত্তর (A/B/C/D): ").strip().upper()
            except EOFError:
                print("\n⚠️ ইনপুট স্ট্রিম বন্ধ — কুইজ সমাপ্ত।")
                break
            if ans == "Q":
                break
            if ans == q["answer"]:
                score += 1
                print("🎉 সঠিক উত্তর! ✅")
            else:
                print(f"❌ ভুল হয়েছে! সঠিক উত্তর: {q['answer']} ({q['options'].get(q['answer'], '')})")
            if q["explanation"]:
                print(f"🧠 কেন: {q['explanation']}")
        else:
            try:
                ans = input("👉 উত্তর ভেবে Enter চাপো (অথবা 'q' বের হতে): ").strip().upper()
            except EOFError:
                break
            if ans == "Q":
                break
            print(f"✅ সমাধান: {q['explanation']}")
        print()

    if mcq_total:
        print("=" * 64)
        print(f"🏆 তোমার চূড়ান্ত MCQ স্কোর: {score} / {mcq_total}")
        print("=" * 64)


def run_interactive_cli(count: int) -> None:
    cards = random.sample(CLI_FLASHCARDS, min(count, len(CLI_FLASHCARDS)))
    print(f"\n⚡ Cisco CLI ফ্ল্যাশকার্ড অনুশীলন ({len(cards)}টি কার্ড) — উত্তর ভেবে Enter চাপো!\n")
    for idx, (prompt, answer) in enumerate(cards, 1):
        print(f"[{idx}/{len(cards)}] ❓ {prompt}")
        try:
            input("   (উত্তর দেখতে Enter চাপো...) ")
        except EOFError:
            print(f"   ✅ উত্তর: {answer}\n")
            continue
        print(f"   ✅ উত্তর: {answer}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="CCNA MCQ & CLI Flashcard Trainer")
    parser.add_argument("--list", action="store_true", help="Show total quiz counts per lesson")
    parser.add_argument("--demo", action="store_true", help="Non-interactive preview of 3 random questions")
    parser.add_argument("--mode", choices=["mcq", "cli"], default="mcq", help="Quiz mode: mcq or cli flashcards")
    parser.add_argument("--lesson", type=int, default=None, help="Filter questions by CCNA lesson number (1-9)")
    parser.add_argument("--count", type=int, default=5, help="Number of questions to ask (default: 5)")
    args = parser.parse_args()

    if args.list:
        print_summary()
        return 0
    if args.demo:
        run_demo(args.lesson)
        return 0
    if args.mode == "cli":
        run_interactive_cli(args.count)
        return 0

    quizzes = load_ccna_quizzes(args.lesson)
    if not quizzes:
        print("❌ কোনো কুইজ পাওয়া যায়নি!", file=sys.stderr)
        return 1
    run_interactive_mcq(quizzes, args.count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
