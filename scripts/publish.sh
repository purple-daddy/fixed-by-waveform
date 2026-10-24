#!/bin/bash
# Rebuild, commit the data + site, push. GitHub Pages republishes https://purple-daddy.github.io/fixed-by-waveform/ in about a minute.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build.py
git add data docs
git commit -m "${1:-update data}" -- data docs
git push origin main
