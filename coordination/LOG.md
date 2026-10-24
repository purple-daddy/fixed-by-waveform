# Fixed by Waveform — log (newest at the top)
## 2026-10-23 21:14 — Standby 09 (review fixes)
- Independent review (Sonnet): fixed the host first names that still showed in free text on unverified items (originals kept in gitignored reference/attributions-unverified.json; build.py now refuses them); footer wording; audit hardening: https hosts must be globally routable, hostile URLs can't crash the run, linear-time page-text extraction with a 30 s fetch cap, quote must match word for word, new gripes auto-add only from podscripts.co / pod.wave.co with the company named in the quote and a clean validation, FIXES GO TO THE REVIEW FILE by default (--auto-fixes to change), items.json re-read before writing, atomic write, only the two files this job writes are committed, claude -p loads project settings only.
- Real dry runs through claude -p work (search ok): 0 new items since 2026-10-01 and 0 verified fixes, nothing written.

## 2026-10-23 21:08 — Standby 09 (set up)
- Project created from the artifact: data split into data/items.json + data/meta.json, template with a strict CSP, https-only links, aria labels, a prominent fan-made banner, "raised by" gated on verification, build.py rules (fixed needs a source link). Checked at 375 px: no overflow, 64 items, search works.
- scripts/audit_weekly.py written and tested with a fake answer (unverifiable items go to review).
