"""Offline v3.5 tests: guide parity, original GIF timing and Pages-ready search.

These are checks of sources, media and built HTML, not simulations of Cisco IOS,
Packet Tracer file opening, telephony registration, failover or DAI enforcement.
Install requirements-docs.txt before running this module.
"""

from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urljoin, urlparse

from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from gif_walkthrough_generator import LABS, entry_path, first_svg  # noqa: E402


class PhaseFourRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = sum((yaml.safe_load((ROOT / "en" / (family + ".yml")).read_text(encoding="utf-8"))
                           for family in ("lessons", "ccna-fundamentals", "Extras")), [])

    def test_every_bengali_guide_has_a_substantial_english_peer_and_backlink(self) -> None:
        self.assertEqual(35, len(self.entries))
        self.assertEqual(35, len({row["source"] for row in self.entries}))
        for row in self.entries:
            with self.subTest(source=row["source"]):
                src = ROOT / row["source"]
                english = ROOT / "en" / row["source"]
                self.assertTrue(src.is_file() and english.is_file())
                native_text, en_text = src.read_text(encoding="utf-8"), english.read_text(encoding="utf-8")
                self.assertIn(f"../en/{row['source']}", native_text)
                self.assertIn(f"../../{row['source']}", en_text)
                self.assertGreaterEqual(len(en_text.split()), 380, english)
                self.assertNotRegex(en_text, r"[\u0980-\u09ff]", "English page unexpectedly contains Bangla prose")
                self.assertIn("## Verify; do not guess", en_text)
                self.assertIn("## If it fails", en_text)
                self.assertIn("<details><summary>Reveal the explanation</summary>", en_text)
                self.assertIn(first_svg(row["source"]).name, en_text)
                if row["source"].startswith(("lessons/", "Extras/")):
                    self.assertIn(entry_path(row["source"]).name, en_text)
                    self.assertIn(entry_path(row["source"]).name, native_text)
                else:
                    self.assertNotIn("30-second GIF", en_text)

    def test_english_roas_keeps_trunk_demo_separate_from_254_gateway_lab(self) -> None:
        english = (ROOT / "en/lessons/06-trunk-inter-vlan.md").read_text(encoding="utf-8")
        self.assertIn("Part 3 is a SEPARATE router-on-a-stick build", english)
        self.assertIn("ip address 192.168.10.254 255.255.255.0", english)
        self.assertIn("ip address 192.168.20.254 255.255.255.0", english)
        self.assertNotIn("gateway 192.168.10.1", english)
        self.assertNotIn("gateway 192.168.20.1", english)
        self.assertIn("PC0-to-PC2 (same VLAN 10)", english)
        self.assertIn("PC0-to-PC1 (VLAN 10 to VLAN 20)", english)
        self.assertNotIn("PC0-to-PC2 across VLANs", english)

    def test_shell_examples_have_correct_fences_and_hardware_has_reference_photos(self) -> None:
        for sample in ("en/Extras/ip-subnet-tester-lab.md", "en/ccna-fundamentals/06-subnetting-vlsm.md"):
            self.assertIn("```bash\npython3 scripts/subnet_calculator.py", (ROOT / sample).read_text())
        problem = (ROOT / "en/lessons/12-problem-solve.md").read_text()
        self.assertIn("Router R1 (run each relevant command separately)", problem)
        self.assertIn("Switch SW1 (run each relevant command separately)", problem)
        hardware = (ROOT / "en/lessons/09-real-hardware.md").read_text()
        for filename in ("rack-patch-panel-cabling.jpg", "router-cisco-1941-back-panel.jpg",
                         "switch-cisco-2960-front.jpg", "sfp-fiber-lc-module.jpg"):
            self.assertIn("../../lessons/images/" + filename, hardware)

    def test_all_26_gifs_are_30s_generated_infographics_with_current_svg_source(self) -> None:
        records = json.loads((ROOT / "assets/gifs/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(26, len(records))
        self.assertEqual(26, len(LABS))
        self.assertEqual(26, len(list((ROOT / "assets/gifs").glob("*.gif"))))
        for record in records:
            with self.subTest(gif=record["gif"]):
                gif = ROOT / record["gif"]
                svg = ROOT / record["source_svg"]
                self.assertEqual(hashlib.sha256(svg.read_bytes()).hexdigest(), record["source_sha256"])
                if "followup_svg" in record:
                    extra = ROOT / record["followup_svg"]
                    self.assertEqual("lessons/06-trunk-inter-vlan.md", record["source"])
                    self.assertEqual(hashlib.sha256(extra.read_bytes()).hexdigest(), record["followup_sha256"])
                self.assertEqual(hashlib.sha256(gif.read_bytes()).hexdigest(), record["gif_sha256"])
                self.assertIn(record["importance"], ("P1", "P2"))
                self.assertGreater(len(record["gif_search_name"]), 18)
                with Image.open(gif) as animated:
                    self.assertEqual((960, 776), animated.size)
                    self.assertEqual(12, animated.n_frames)
                    self.assertEqual(0, animated.info["loop"])
                    total = 0
                    for frame in range(animated.n_frames):
                        animated.seek(frame)
                        total += animated.info.get("duration", 0)
                    self.assertEqual(30000, total)
        self.assertEqual(30000, records[0]["duration_ms"])

    def test_gif_catalog_lists_every_topic_search_name_and_study_priority(self) -> None:
        catalog = (ROOT / "GIF-CATALOG.md").read_text(encoding="utf-8")
        self.assertIn("Packet Tracer-এর screen recording", catalog)
        self.assertIn("traffic/feature test নয়", catalog)
        for row in json.loads((ROOT / "assets/gifs/manifest.json").read_text(encoding="utf-8")):
            with self.subTest(name=row["gif"]):
                self.assertIn(f"[{row['topic']}]({row['source']})", catalog)
                self.assertIn(f"[▶ ৩০ সেকেন্ড]({row['gif']})", catalog)
                self.assertIn(f"`{row['gif_search_name']} gif`", catalog)
                self.assertIn(f"**{row['importance']}**", catalog)
        self.assertIn("GIF-CATALOG.md", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_mkdocs_material_nav_has_each_english_guide_and_github_pages_is_gated(self) -> None:
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        self.assertEqual("material", config["theme"]["name"])
        self.assertEqual(2, len(config["theme"]["palette"]))
        self.assertIn("content.code.copy", config["theme"]["features"])
        self.assertTrue(any(isinstance(p, dict) and "search" in p for p in config["plugins"]))
        self.assertIn("github.io/Cisco-Packet-Tracer-Lab/", config["site_url"])
        nav_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for row in self.entries:
            self.assertIn("en/" + row["source"], nav_text)
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request:", workflow)
        self.assertIn("actions/upload-pages-artifact@v3", workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)
        self.assertIn("github.event_name != 'pull_request'", workflow)
        self.assertIn("mkdocs build --strict", workflow)

    def test_portal_staging_strict_build_and_bilingual_search_index(self) -> None:
        def invoke(*args: str) -> None:
            result = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
            if result.returncode:
                self.fail(f"{args} failed:\n{result.stdout[-4000:]}\n{result.stderr[-4000:]}")
        invoke("scripts/portal_docs.py")
        invoke("scripts/portal_docs.py", "--check")
        self.assertIn('href="lessons/01-router-cli-basics.md"', (ROOT / "README.md").read_text())
        self.assertIn('href="lessons/01-router-cli-basics/"', (ROOT / "build/docs/README.md").read_text())
        invoke("-m", "mkdocs", "build", "--strict", "-f", "mkdocs.yml")
        site = ROOT / "build/site"
        self.assertTrue((site / "en/lessons/17-hsrp-gateway-redundancy/index.html").is_file())
        self.assertTrue((site / "assets/gifs/17-hsrp-gateway-redundancy.gif").is_file())
        self.assertTrue((site / "assets/diagrams/index.html").is_file())
        self.assertTrue((site / "pkt-files/topologies/index.html").is_file())
        # v4: all four capstone pages and their linked, role-separated source files are staged.
        for relative in ("capstone/index.html", "en/capstone/index.html",
                         "capstone/VERIFICATION/index.html", "pkt-files/capstone/index.html",
                         "capstone/configs/HQ1.txt", "capstone/configs/CME.txt",
                         "capstone/plan.json", "assets/diagrams/capstone-v4-sites.svg",
                         "assets/diagrams/capstone-v4-paths.svg"):
            self.assertTrue((site / relative).is_file(), relative)
        self.assertEqual(96, len(list((ROOT / "build/docs").rglob("*.md"))))
        index = json.loads((site / "search/search_index.json").read_text(encoding="utf-8"))
        combined = " ".join(row.get("text", "") for row in index["docs"])
        self.assertIn("নেটওয়ার্ক", combined)
        self.assertIn("virtual gateway", combined.lower())
        self.assertTrue(any(row["location"].startswith("en/lessons/17-") for row in index["docs"]))
        self.assertTrue(any(row["location"].startswith("lessons/17-") for row in index["docs"]))
        self.assertTrue(any(row["location"].startswith("en/capstone/") for row in index["docs"]))
        self.assertTrue(any(row["location"].startswith("capstone/") for row in index["docs"]))
        self.assertIn("four private WAN circuits", combined)

        class LocalTargets(HTMLParser):
            def __init__(self) -> None:
                super().__init__()
                self.links: list[str] = []
                self.ids: set[str] = set()

            def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
                fields = dict(attrs)
                if fields.get("id"):
                    self.ids.add(fields["id"])
                if tag == "a" and fields.get("name"):
                    self.ids.add(fields["name"])
                if tag in {"a", "img", "script", "link", "source"}:
                    self.links.extend(value for name, value in fields.items()
                                      if name in {"href", "src"} and value)

        pages = {}
        for page in site.rglob("*.html"):
            parser = LocalTargets()
            parser.feed(page.read_text(encoding="utf-8"))
            pages[page] = parser
        missing = []
        base = "https://example.org/Cisco-Packet-Tracer-Lab/"
        for page, parser in pages.items():
            page_dir = page.parent.relative_to(site).as_posix().strip(".")
            page_url = base + (page_dir + "/" if page_dir else "")
            for raw in parser.links:
                if raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "//")):
                    continue
                url = urlparse(urljoin(page_url, raw))
                if url.netloc != "example.org":
                    continue  # external link, badge or canonical URL
                prefix = "/Cisco-Packet-Tracer-Lab/"
                if not url.path.startswith(prefix):
                    missing.append((page, raw))
                    continue
                target = site / unquote(url.path[len(prefix):])
                if target.is_dir():
                    target /= "index.html"
                if not target.is_file():
                    missing.append((page, raw))
                elif url.fragment and target.suffix == ".html" and unquote(url.fragment) not in pages[target].ids:
                    missing.append((page, raw, "missing fragment"))
        self.assertEqual([], missing, f"Broken built-site links/assets/fragments: {missing[:8]}")

    def test_no_phase_three_pkt_has_been_invented_and_limits_are_disclosed(self) -> None:
        self.assertEqual(18, len(list((ROOT / "pkt-files").rglob("*.pkt"))))
        all_pkt = " ".join(p.name for p in (ROOT / "pkt-files").rglob("*.pkt"))
        for new in ("16-", "17-", "18-", "voip-", "dhcp-snooping-"):
            self.assertNotIn(new, all_pkt)
        for path in ("README.md", "PORTAL.md", "en/README.md", "GIF-CATALOG.md"):
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertRegex(text, re.compile(r"Packet Tracer.*(recording|রেকর্ডিং|screen|স্ক্রিন)", re.I | re.S))
        en_dai = (ROOT / "en/Extras/dhcp-snooping-dai-lab.md").read_text(encoding="utf-8")
        self.assertIn("unverified", en_dai)


if __name__ == "__main__":
    unittest.main()
