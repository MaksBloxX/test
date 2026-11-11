#!/usr/bin/env python3
"""Repository link, image, illustrated-coverage and convention auditor.

All Markdown files need a valid local visual; remote status badges do not count.
SVG files must parse as XML and raster files must have the correct signature.

Usage:
  python3 scripts/repo_doctor.py
  python3 scripts/repo_doctor.py --strict
"""

import argparse
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "node_modules", "build", "site"}
IMAGE_EXTS = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}

MD_LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTML_ATTR_RE = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')
HTML_IMAGE_RE = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
ANCHOR_ID_RE = re.compile(r'<a\s+id=["\']([^"\']+)["\']', re.IGNORECASE)


def strip_fenced_code(text: str) -> str:
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def github_slug(heading_text: str) -> str:
    s = heading_text.strip().lower()
    s = re.sub(r"[^\w\s\u0980-\u09ff-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def collect_anchors(md_text: str) -> set[str]:
    anchors = set(ANCHOR_ID_RE.findall(md_text))
    for line in strip_fenced_code(md_text).splitlines():
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            anchors.add(github_slug(m.group(2)))
    return anchors


def validate_image(md: str, raw: str, errors: list[str], svg_cache: dict[str, bool]) -> str | None:
    """Return a valid local image path, or None for a broken/remote image.

    Remote README badges are allowed, but do not count as teaching visuals.
    The signature/XML checks reject HTML error pages renamed with an image extension.
    """
    target = raw.strip().split()[0].split("#", 1)[0].split("?", 1)[0] if raw.strip() else ""
    if target.startswith(("https://", "http://", "//", "data:")):
        return None
    rel = urllib.parse.unquote(target)
    resolved = os.path.normpath(os.path.join(os.path.dirname(md), rel)).replace("\\", "/")
    full = os.path.abspath(os.path.join(REPO_ROOT, resolved))
    if not rel or os.path.commonpath((REPO_ROOT, full)) != REPO_ROOT or not os.path.isfile(full):
        errors.append(f"[Broken Image] {md}: '{raw}' is not a local file")
        return None
    ext = os.path.splitext(resolved)[1].lower()
    if ext not in IMAGE_EXTS or os.path.getsize(full) == 0:
        errors.append(f"[Invalid Image] {md}: '{raw}' is empty or has no supported image extension")
        return None
    if ext == ".svg":
        if resolved not in svg_cache:
            try:
                root = ET.parse(full).getroot()
                svg_cache[resolved] = root.tag == "{http://www.w3.org/2000/svg}svg"
            except (ET.ParseError, OSError):
                svg_cache[resolved] = False
        if not svg_cache[resolved]:
            errors.append(f"[Invalid SVG] {md}: '{raw}' is not parseable SVG")
            return None
    else:
        with open(full, "rb") as image:
            head = image.read(12)
        signatures = {
            ".png": head.startswith(b"\x89PNG\r\n\x1a\n"),
            ".jpg": head.startswith(b"\xff\xd8"),
            ".jpeg": head.startswith(b"\xff\xd8"),
            ".gif": head.startswith((b"GIF87a", b"GIF89a")),
            ".webp": head.startswith(b"RIFF") and head[8:12] == b"WEBP",
        }
        if not signatures[ext]:
            errors.append(f"[Invalid Image Data] {md}: '{raw}' is not a real {ext} image")
            return None
    return resolved


def audit_repository() -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []

    all_files: set[str] = set()
    md_files: list[str] = []
    pkt_files: list[str] = []
    ios_files: list[str] = []
    script_files: list[str] = []

    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), REPO_ROOT).replace("\\", "/")
            all_files.add(rel)
            if fn.endswith(".md"):
                md_files.append(rel)
            elif fn.endswith(".pkt"):
                pkt_files.append(rel)
            elif fn.endswith(".ios"):
                ios_files.append(rel)
            elif rel.startswith("scripts/") and fn.endswith(".py"):
                script_files.append(rel)

    md_files.sort()
    pkt_files.sort()
    ios_files.sort()
    script_files.sort()

    anchors_cache: dict[str, set[str]] = {}
    for md in md_files:
        txt = open(os.path.join(REPO_ROOT, md), encoding="utf-8").read()
        anchors_cache[md] = collect_anchors(txt)

    referenced_files: set[str] = {"README.md"}
    total_lines = 0
    illustrated_md = 0
    image_embeds = 0
    local_images: set[str] = set()
    svg_cache: dict[str, bool] = {}

    for md in md_files:
        full_path = os.path.join(REPO_ROOT, md)
        txt = open(full_path, encoding="utf-8").read()
        lines = txt.splitlines()
        total_lines += len(lines)

        # 1. Check balanced code fences & HTML <details>/<summary> toggles
        fence_count = sum(1 for l in lines if l.strip().startswith("```"))
        if fence_count % 2 != 0:
            errors.append(f"[Unclosed Code Fence] {md} (``` count = {fence_count})")

        clean_txt = strip_fenced_code(txt)
        if clean_txt.count("<details>") != clean_txt.count("</details>"):
            errors.append(f"[Unclosed <details>] {md}")
        if clean_txt.count("<summary>") != clean_txt.count("</summary>"):
            errors.append(f"[Unclosed <summary>] {md}")

        # Every guide needs a valid-looking local image (not just a remote badge).
        # SVGs are parsed as XML; JPG/PNG/GIF/WEBP are checked by signature.
        image_targets = [(m.group(1), m.group(2)) for m in MD_IMAGE_RE.finditer(clean_txt)]
        image_targets += [("HTML image", m.group(1)) for m in HTML_IMAGE_RE.finditer(clean_txt)]
        has_local_visual = False
        for alt, raw in image_targets:
            resolved_image = validate_image(md, raw, errors, svg_cache)
            if resolved_image is None:
                continue
            if not alt.strip():
                warnings.append(f"[Missing Image Alt] {md}: '{raw}' has no alternative text")
            has_local_visual = True
            image_embeds += 1
            local_images.add(resolved_image)
        if has_local_visual:
            illustrated_md += 1
        else:
            errors.append(f"[No Local Visual] {md} needs a valid local diagram or photo")

        # 2. Check navigation presence (except root README.md and CONTRIBUTING.md)
        if md not in ("README.md", "CONTRIBUTING.md") and "নেভিগেশন" not in txt and "README.md" not in txt:
            warnings.append(f"[Missing Navigation] {md} has no link back to README.md")

        # 3. Validate all relative links & images outside code blocks
        raw_targets = [m[1] for m in MD_LINK_RE.findall(clean_txt)] + HTML_ATTR_RE.findall(clean_txt)

        for raw in raw_targets:
            target = raw.strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
                continue
            # Strip optional markdown link title
            if " " in target and not target.startswith("#"):
                target = target.split()[0]

            if target.startswith("#"):
                frag = target[1:]
                if frag and frag not in anchors_cache[md]:
                    errors.append(f"[Broken Anchor] {md}: '#{frag}' not found in same file")
                continue

            parts = target.split("#", 1)
            rel_part = urllib.parse.unquote(parts[0])
            frag = parts[1] if len(parts) > 1 else ""

            resolved = os.path.normpath(os.path.join(os.path.dirname(md), rel_part)).replace("\\", "/")
            full_target = os.path.join(REPO_ROOT, resolved)

            if not os.path.exists(full_target):
                errors.append(f"[Broken Link] {md}: '{raw}' -> '{resolved}' does not exist")
                continue

            if os.path.isdir(full_target):
                # Mark directory files or its README as referenced
                dir_readme = f"{resolved}/README.md"
                if dir_readme in all_files:
                    referenced_files.add(dir_readme)
            else:
                referenced_files.add(resolved)
                if frag and resolved in anchors_cache and frag not in anchors_cache[resolved]:
                    errors.append(f"[Broken Cross-File Anchor] {md}: '{raw}' -> '#{frag}' not in {resolved}")

    # 4. Check .pkt lab naming convention in pkt-files/labs/
    for pkt in pkt_files:
        if pkt.startswith("pkt-files/labs/"):
            base = os.path.basename(pkt)
            if not re.match(r"^lesson-\d{2}-[a-z0-9-]+\.pkt$", base):
                warnings.append(f"[PKT Naming] {pkt} does not match 'lesson-NN-<slug>.pkt'")
        if pkt not in referenced_files:
            warnings.append(f"[Unreferenced .pkt] {pkt} is never linked from any Markdown file")

    # 5. Check unreferenced images or markdown guides
    ignore_unref = {".gitignore", ".github/workflows/repo-check.yml", "CONTRIBUTING.md", "ROADMAP.md"}
    for f in sorted(all_files - referenced_files - ignore_unref):
        if f.startswith(".github/"):
            continue
        warnings.append(f"[Unreferenced File] {f} is not linked from any Markdown page")

    stats = {
        "total_files": len(all_files),
        "md_files": len(md_files),
        "pkt_files": len(pkt_files),
        "ios_files": len(ios_files),
        "scripts": len(script_files),
        "total_md_lines": total_lines,
        "illustrated_md": illustrated_md,
        "image_embeds": image_embeds,
        "local_image_assets": len(local_images),
        "practical_lessons": sum(
            1 for f in md_files if f.startswith("lessons/") and os.path.basename(f) != "README.md"
        ),
        "ccna_lessons": sum(
            1 for f in md_files if f.startswith("ccna-fundamentals/") and os.path.basename(f) != "README.md"
        ),
        "extra_labs": sum(
            1 for f in md_files if f.startswith("Extras/") and os.path.basename(f) != "README.md"
        ),
    }
    return errors, warnings, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Cisco-Packet-Tracer-Lab repository health")
    parser.add_argument("--strict", action="store_true", help="Fail (exit 1) on warnings as well as errors")
    args = parser.parse_args()

    errors, warnings, stats = audit_repository()

    print("🩺 Cisco-Packet-Tracer-Lab — Repository Health Report (v4.0)")
    print("=" * 65)
    print(f"  📚 Practical Lessons  : {stats['practical_lessons']}")
    print(f"  🎓 CCNA Lessons       : {stats['ccna_lessons']}")
    print(f"  📦 Extra Labs         : {stats['extra_labs']}")
    print(f"  📄 Total Markdown     : {stats['md_files']} files ({stats['total_md_lines']:,} lines)")
    print(f"  🖼️  Illustrated guides : {stats['illustrated_md']}/{stats['md_files']} with {stats['image_embeds']} local image embeds")
    print(f"  🎨 Local image assets : {stats['local_image_assets']} unique assets used")
    print(f"  🧰 Packet Tracer Labs : {stats['pkt_files']} .pkt + {stats['ios_files']} .ios fault scripts")
    print(f"  🛠️  Helper Scripts     : {stats['scripts']} Python tools")
    print("=" * 65)

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  • {e}")
    else:
        print("\n✅ 0 broken links, invalid images or code-fence errors!")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  • {w}")
    else:
        print("✅ 0 orphan files, naming or accessibility warnings!")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
