#!/usr/bin/env python3
"""Stage all public repository guides/assets for MkDocs without duplicating sources.

Why stage? The git repository root contains scripts, .git and CI metadata and
MkDocs refuses a site_dir inside its docs_dir. We copy publishable files into
ignored build/docs/, then MkDocs writes ignored build/site/. Normal Markdown
links and README.md-as-index semantics stay intact; raw HTML <a href='x.md'>
links are rewritten in STAGING ONLY to MkDocs pretty URLs, leaving GitHub
source links untouched.

Usage: python3 scripts/portal_docs.py && python3 -m mkdocs build --strict
"""

from __future__ import annotations

import argparse
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
from urllib.parse import urlsplit, urlunsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
STAGE = ROOT / "build" / "docs"
PUBLIC_SUFFIXES = {".md", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp",
                   ".pdf", ".pkt", ".ios", ".py", ".yml", ".yaml", ".json", ".css", ".js", ".txt"}
HTML_HREF = re.compile(r"(?P<start><a\b[^>]*?\bhref=)(?P<q>[\"'])(?P<target>[^\"']+)(?P=q)", re.I)


def staged_markdown(rel: Path) -> bytes:
    """Convert ONLY raw HTML links, which MkDocs leaves unrewritten, to pretty URLs.

    A Markdown link to foo.md is rewritten by MkDocs itself. A raw HTML link
    to foo.md is not; on GitHub it works, but the Pages site only has foo/.
    """
    source = ROOT / rel
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    current = rel.parent.as_posix() if rel.name == "README.md" else rel.with_suffix("").as_posix()
    if current == ".":
        current = ""

    def rewrite(match: re.Match[str]) -> str:
        raw = match.group("target")
        url = urlsplit(raw)
        if url.scheme or url.netloc or not url.path.lower().endswith(".md"):
            return match.group(0)
        target = (source.parent / unquote(url.path)).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            return match.group(0)
        target_rel = target.relative_to(ROOT)
        page = target_rel.parent.as_posix() if target_rel.name == "README.md" else target_rel.with_suffix("").as_posix()
        if page == ".":
            page = ""
        route = posixpath.relpath(page or ".", current or ".") + "/"
        new_url = urlunsplit(("", "", route, url.query, url.fragment))
        return f'{match.group("start")}{match.group("q")}{new_url}{match.group("q")}'

    result = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        result.append(line if in_fence else HTML_HREF.sub(rewrite, line))
    return "".join(result).encode("utf-8")


def expected_bytes(rel: Path) -> bytes:
    return staged_markdown(rel) if rel.suffix.lower() == ".md" else (ROOT / rel).read_bytes()


def public_files() -> list[Path]:
    # Includes new-but-not-yet-committed content in a developer preview.
    output = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    )
    files = []
    for raw in output.split(b"\0"):
        if not raw:
            continue
        rel = Path(raw.decode("utf-8"))
        # Older documentation links CI YAML and regression tests as source files.
        if (rel.parts[0].startswith(".") and rel.parts[0] != ".github") or rel.parts[0] in {"build", "site"}:
            continue
        if rel.suffix.lower() in PUBLIC_SUFFIXES and (ROOT / rel).is_file():
            files.append(rel)
    return sorted(set(files))


def stage() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    for rel in public_files():
        dest = STAGE / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if rel.suffix.lower() == ".md":
            dest.write_bytes(staged_markdown(rel))
        else:
            shutil.copy2(ROOT / rel, dest)
    count = len(list(STAGE.rglob("*.md")))
    if count < 96:
        raise RuntimeError(f"Only {count} Markdown pages staged; expected the bilingual v4 capstone and all earlier guides")
    print(f"Staged {len(public_files())} public files and {count} Markdown pages in build/docs")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check that all publishable source files are staged")
    args = parser.parse_args()
    if args.check:
        files = public_files()
        missing = [str(rel) for rel in files if not (STAGE / rel).is_file()
                   or (STAGE / rel).read_bytes() != expected_bytes(rel)]
        if missing:
            raise SystemExit(f"Portal staging missing/stale files: {missing[:8]}")
        print(f"Staging OK: {len(files)} public files match sources")
    else:
        stage()


if __name__ == "__main__":
    main()
