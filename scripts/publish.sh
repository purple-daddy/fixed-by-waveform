#!/bin/bash
# Rebuild, commit the data + site, push to the (PRIVATE) repo. The site is NOT public: GitHub Pages stays off until Jay says yes.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build.py
git add data docs
git commit -m "${1:-update data}" -- data docs
git push origin main
