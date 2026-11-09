#!/usr/bin/env python3
"""Build/check the 35 English curriculum companions from curated English YAML.

All prose in en/*.yml is written in English and reviewed against the source
lesson's topology, addressing and simulator limits. The adaptations teach the
same core lab workflows; they are NOT machine-translated, paragraph-for-paragraph
copies of the substantially longer Bengali source chapters. Link back to the
original for extended case sets and full quiz banks.

Requires PyYAML (requirements-docs.txt). Use --check in CI.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Install requirements-docs.txt (PyYAML) to generate/check the English track") from exc

from gif_walkthrough_generator import LABS, entry_path, first_svg

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ("en/lessons.yml", "en/ccna-fundamentals.yml", "en/Extras.yml")
GIF_SOURCES = {item[0] for item in LABS}


def relative(target: Path, dest: Path) -> str:
    return Path(os.path.relpath(target, dest.parent)).as_posix()


def data() -> list[dict]:
    entries = []
    for filename in SOURCES:
        group = yaml.safe_load((ROOT / filename).read_text(encoding="utf-8"))
        assert isinstance(group, list), filename
        entries.extend(group)
    if len(entries) != 35 or len({x["source"] for x in entries}) != 35:
        raise ValueError("Expected 18 practical + 9 CCNA + 8 Extra distinct source guides")
    for item in entries:
        source = ROOT / item["source"]
        if not source.is_file() or source.name == "README.md":
            raise ValueError(f"English source guide missing: {source}")
        for key in ("title", "goal", "plan", "question", "answer"):
            min_chars = 20 if key in ("goal", "plan") else 12
            if not isinstance(item.get(key), str) or len(item[key]) < min_chars:
                raise ValueError(f"English guide {source}: missing {key}")
        for key in ("ideas", "steps", "verify", "fix"):
            if not isinstance(item.get(key), list) or len(item[key]) < 2:
                raise ValueError(f"English guide {source}: missing {key}")
        if item.get("sample_language", "text") not in {"text", "bash", "cisco"}:
            raise ValueError(f"English guide {source}: invalid sample_language")
        for photo in item.get("visuals", []):
            path = (ROOT / photo["path"]).resolve()
            if (not path.is_relative_to(ROOT) or not path.is_file()
                    or path.suffix.lower() not in {".jpg", ".jpeg", ".png"}
                    or path.name not in source.read_text(encoding="utf-8")
                    or not photo.get("alt") or not photo.get("caption")):
                raise ValueError(f"English guide {source}: invalid hardware reference {photo}")
    return entries


def render(item: dict) -> tuple[Path, str]:
    src = ROOT / item["source"]
    out = ROOT / "en" / item["source"]
    family = src.parent.name
    series = "Practical Lesson" if family == "lessons" else "CCNA Chapter" if family == "ccna-fundamentals" else "Extra Lab"
    number = re.match(r"(\d\d)-", src.stem)
    if family == "Extras":
        number = next((f"{i+1:02}" for i, row in enumerate(LABS[18:]) if row[0] == item["source"]), None)
    else:
        number = number.group(1) if number else None
    if not number:
        raise ValueError(f"Cannot number English guide: {src}")

    img_path = relative(first_svg(item["source"]), out)
    original = relative(src, out)
    index = relative(ROOT / "en" / "README.md", out)
    series_index = relative(ROOT / "en" / family / "README.md", out)
    caption = "Illustrated topology or concept map from the corresponding Bengali guide; a diagram, not a Packet Tracer capture."
    title = f"{series} {number}: {item['title']}"
    lines = [f"# {title}", "",
             f"> **Navigation:** [English home]({index}) · [{series} index]({series_index}) · [Full Bengali guide]({original})",
             "",
             f"**Learning goal.** {item['goal']}", "",
             f"![{item['title']}: original accessible topology or concept diagram.]({img_path})", "",
             f"> **About this visual:** {caption}", ""]

    if item["source"] in GIF_SOURCES:
        gif = relative(entry_path(item["source"]), out)
        catalog = relative(ROOT / "GIF-CATALOG.md", out)
        lines += [f"![30-second illustrated walkthrough of {item['title']}; six steps, not a Packet Tracer screen recording.]({gif})", "",
                  f"> **30-second GIF:** six illustrated stages of the topology and checks. This is **not a Packet Tracer recording or proof of successful device behavior**. See the [GIF search names and study priorities]({catalog}) if you want to source your own alternative.", ""]
        source_text = src.read_text(encoding="utf-8")
        images = re.findall(r"!\[[^\]]*\]\(([^)]+\.svg)\)", source_text)
        if len(images) > 1:
            second = relative((src.parent / images[1]).resolve(), out)
            lines += [f"![Second concept or packet-path diagram for {item['title']}.]({second})", "",
                      "> This second diagram separates the concept/flow from the physical topology. Compare its labels with the numbered build steps below.", ""]

    lines += ["## Understand the design", "", item["plan"], "",
              "### Key ideas", ""]
    lines += [f"- {idea}" for idea in item["ideas"]]
    if item.get("visuals"):
        lines += ["", "## Real-device photo references", "",
                  "These pre-existing reference images illustrate physical components; they are not proof of a particular lab setup or a definitive hardware model/port map."]
        for photo in item["visuals"]:
            photo_path = relative(ROOT / photo["path"], out)
            lines += ["", f"![{photo['alt']}]({photo_path})", "", f"*{photo['caption']}*"]
    lines += ["", "## Build or work through it", ""]
    lines += [f"{i}. {step}" for i, step in enumerate(item["steps"], 1)]
    if sample := item.get("sample"):
        # Use a shell fence only for host-shell examples, never for mixed IOS/host lists.
        kind = item.get("sample_language")
        if kind is None:
            if "python3 scripts/" in sample and not re.search(r"(?m)^show (?:ip|vlan|interfaces|standby|etherchannel)", sample):
                kind = "bash"
            elif ("#" in sample or "Full mesh" in sample or "R1 ONLY" in sample
                  or sample.startswith(("Application:", "192."))):
                kind = "text"
            else:
                kind = "cisco"
        lines += ["", "### Copyable study example", "",
                  "Read the comment or role label first: IOS commands, PC commands and shell commands run in **different places**. This example is not a verified Packet Tracer run.", "",
                  f"```{kind}", sample.rstrip(), "```"]
    lines += ["", "## Verify; do not guess", ""]
    lines += [f"- [ ] {test}" for test in item["verify"]]
    lines += ["", "## If it fails", ""]
    lines += [f"- {problem}" for problem in item["fix"]]
    lines += ["", "## Check your understanding", "", f"**Question.** {item['question']}", "",
              "<details><summary>Reveal the explanation</summary>", "",
              f"**Answer.** {item['answer']}", "", "</details>", "",
              "---", "",
              f"**Continue:** [English track]({series_index}) · [Full Bengali lesson, complete tables and additional exercises]({original})", ""]
    return out, "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when an English page does not match its curated data")
    args = parser.parse_args()
    for item in data():
        path, expected = render(item)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                raise SystemExit(f"English page missing or stale: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
    print("Checked" if args.check else "Generated", "35 English chapter/lab companions: 18 practical, 9 CCNA, 8 Extra.")


if __name__ == "__main__":
    main()
