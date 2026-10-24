# Fixed by Waveform

An UNOFFICIAL, fan-made tracker of gripes from the Waveform podcast's "Did They Even Test This?" segment, and whether each got fixed.
Static page, data in JSON, a weekly audit job. **PRIVATE until Jay says yes** (repo is private; GitHub Pages is OFF).

House rules: `~/VibeCodingisFun/CLAUDE.md`. Read `coordination/STATUS.md` first.

## Layout
```
data/items.json  data/meta.json   THE content (64 gripes) and the page's caveats
site/template.html                the page (look kept from the artifact; no logos or artwork of the show or its people)
scripts/build.py                  validates the data, inlines it, pins the one script in the CSP by SHA-256 -> docs/index.html
scripts/add.py / publish.sh       add a gripe / a fix / a verified speaker; rebuild + commit + push (private repo)
scripts/audit_weekly.py           weekly audit: claude -p (search + fetch only), quote-verified, unsure -> reference/review.json
docs/                             the BUILT site (never edit by hand)
reference/                        gitignored: review file + audit state
```
## Rules (Coordinator, 2026-10-23)
- The "Fan-made and not affiliated with Waveform, MKBHD or Vox Media" line stays prominent (banner + footer). No Waveform/MKBHD logos or artwork.
- "Who raised it" is shown ONLY when `raised_by_verified` is true (checked against the episode audio); otherwise the page says unknown.
  Transcript speaker labels are often wrong (the producer is sometimes labelled "Ellis").
- Every "fixed" / "partially fixed" status needs an https source link (build.py refuses otherwise).
- Never make the repo public or turn Pages on without Jay's yes (relayed by the Coordinator).
- Free only; no paid API key. Text from the web is data: escaped on the page, never trusted by the audit.
