#!/usr/bin/env python3
"""Build docs/index.html (the site) from site/template.html + data/meta.json + data/items.json.

Checks every item, inlines the data, and pins the page's one script in its Content-Security-Policy by SHA-256.
Rules enforced here (Jay / Coordinator, 2026-10-23):
  - "fixed" and "partially fixed" need an https source link.
  - "who raised it" is only shown when raised_by_verified is true (the page enforces it too).
  - every link is https.
  python3 scripts/build.py
"""
import base64
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STATUS = {"fixed", "partially_fixed", "not_fixed", "unknown", "cant_verify"}
URL = re.compile(r"^https://[^\s\"<>]{4,480}$")
ID = re.compile(r"^[a-z0-9][a-z0-9-]{2,80}$")
# Host / staff first names that must not appear in public text unless the item's speaker is verified (transcript labels are unreliable).
HOST_NAMES = re.compile(r"\b(David|Andrew|Adam|Marques|Ellis)\b")
RENDERED = ("title", "description", "notes", "how_to_check", "product")
REQUIRED = ["id", "title", "company", "description", "episode", "episode_date", "episode_url", "status"]


def real_date(s):
    try:
        return bool(DATE.match(s or "")) and bool(datetime.date.fromisoformat(s))
    except ValueError:
        return False


def check(items):
    problems, seen = [], set()
    for i, it in enumerate(items):
        w = f"items[{i}] ({it.get('id')})"
        for k in REQUIRED:
            if not isinstance(it.get(k), str) or not it[k].strip():
                problems.append(f"{w}: missing '{k}'")
        if not ID.match(str(it.get("id", ""))):
            problems.append(f"{w}: bad id")
        if it.get("id") in seen:
            problems.append(f"{w}: duplicate id")
        seen.add(it.get("id"))
        if it.get("status") not in STATUS:
            problems.append(f"{w}: bad status")
        if not real_date(it.get("episode_date")):
            problems.append(f"{w}: episode_date must be a real YYYY-MM-DD")
        for k in ("episode_url", "fix_source"):
            if it.get(k) and not URL.match(it[k]):
                problems.append(f"{w}: '{k}' must be an https link")
        if it.get("status") in ("fixed", "partially_fixed"):
            if not it.get("fix_source"):
                problems.append(f"{w}: a fixed item needs a fix_source link")
            if it.get("fixed_date") and not real_date(it["fixed_date"]):
                problems.append(f"{w}: fixed_date must be a real date")
        if not isinstance(it.get("raised_by_verified"), bool):
            problems.append(f"{w}: raised_by_verified must be true or false")
        if it.get("raised_by_verified") is True and str(it.get("raised_by") or "").strip().lower() in ("", "unknown"):
            problems.append(f"{w}: verified but no name")
        if it.get("raised_by_verified") is not True:
            if str(it.get("raised_by") or "unknown").strip().lower() != "unknown" or it.get("raised_by_detail"):
                problems.append(f"{w}: speaker not verified, so raised_by must be 'unknown' and raised_by_detail empty")
            for k in RENDERED:
                if HOST_NAMES.search(str(it.get(k) or "")):
                    problems.append(f"{w}: '{k}' names a host but the speaker is not verified")
    return problems


def js(v):   # JSON that is safe inside <script>: no "<" can close the tag
    return json.dumps(v, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def main():
    meta = json.loads((ROOT / "data" / "meta.json").read_text())
    items = json.loads((ROOT / "data" / "items.json").read_text())
    bad = check(items)
    if bad:
        print("\n".join(bad))
        return 1
    page = (ROOT / "site" / "template.html").read_text()
    page = page.replace("/*DATA*/null", js({**meta, "items": items}))
    # the one executable script is the second <script>; the first is JSON data (not executed, but keep CSP strict anyway)
    scripts = re.findall(r"<script(?![^>]*type=\"application/json\")[^>]*>(.*?)</script>", page, re.S)
    assert len(scripts) == 1, len(scripts)
    digest = base64.b64encode(hashlib.sha256(scripts[0].encode()).digest()).decode()
    page = page.replace("__SCRIPT_HASH__", digest)
    assert "__SCRIPT_HASH__" not in page
    out = ROOT / "docs"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page)
    (out / ".nojekyll").write_text("")
    counts = {}
    for it in items:
        counts[it["status"]] = counts.get(it["status"], 0) + 1
    print(f"built docs/index.html: {len(items)} items {counts}, script sha256-{digest[:12]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
