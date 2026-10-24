#!/usr/bin/env python3
"""Add or update one gripe by hand, then rebuild.

  python3 scripts/add.py new --title "..." --company X --product Y --category app --description "..." \
      --episode "Episode title" --date 2026-10-20 --url https://... [--status unknown]
  python3 scripts/add.py fix --id <id> --status fixed|partially_fixed --source https://... [--fixed-in "v1.2"] [--fixed-date 2026-10-21]
  python3 scripts/add.py raised --id <id> --by "Name"      # ONLY after checking the episode AUDIO; marks the speaker as verified
Then: bash scripts/publish.sh "message"   (pushes to the private repo)
"""
import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "data" / "items.json"


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", s.lower()))).strip("-")[:60]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["new", "fix", "raised"])
    for k in ("title", "company", "product", "category", "description", "episode", "date", "url", "status", "id", "source", "fixed-in",
              "fixed-date", "by"):
        ap.add_argument("--" + k)
    a = ap.parse_args()
    items = json.loads(P.read_text())
    old = P.read_text()
    if a.cmd == "new":
        need = ("title", "company", "description", "episode", "date", "url")
        if not all(getattr(a, k) for k in need):
            sys.exit("new needs " + ", ".join("--" + k for k in need))
        base = slug(f"{a.company}-{a.title}")
        nid, n = base, 2
        while any(i["id"] == nid for i in items):
            nid = f"{base}-{n}"
            n += 1
        items.append({"id": nid, "title": a.title, "company": a.company, "product": a.product or "", "category": a.category or "other",
                      "description": a.description, "raised_by": "unknown", "raised_by_detail": None, "raised_by_verified": False,
                      "episode": a.episode, "episode_date": a.date, "episode_url": a.url, "status": a.status or "unknown",
                      "fixed_in": None, "fixed_date": None, "fix_source": None, "credited_to_waveform": None, "checkable": True,
                      "how_to_check": "", "notes": ""})
    else:
        row = next((i for i in items if i["id"] == a.id), None)
        if not row:
            sys.exit("no item with that id")
        if a.cmd == "fix":
            if not (a.status and a.source):
                sys.exit("fix needs --status and --source")
            row.update({"status": a.status, "fix_source": a.source, "fixed_in": a.fixed_in, "fixed_date": a.fixed_date})
        else:
            if not a.by:
                sys.exit("raised needs --by")
            row.update({"raised_by": a.by, "raised_by_verified": True})
    P.write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n")
    if subprocess.call([sys.executable, str(ROOT / "scripts" / "build.py")]) != 0:
        P.write_text(old)
        sys.exit("rejected; data left as it was")


main()
