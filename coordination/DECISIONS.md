# Fixed by Waveform — decisions
- D-001: Same static-site setup as two-weeks (data JSON, build.py with CSP hash, add.py, publish.sh).
- D-002: "Raised by" is shown only where `raised_by_verified` is true; the audit never sets it. Reason: transcript speaker labels are unreliable.
- D-003: The weekly audit may add new gripes only with a verified quote on the episode page (status "unknown", speaker unknown) and apply a fix only with a verified quote on the fix source; all else goes to the gitignored review file.
- D-004: Repo PRIVATE, Pages OFF until Jay says yes. `<meta name=robots noindex>` is in the page for when it does go up.
