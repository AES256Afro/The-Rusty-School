#!/bin/sh
# Regenerates the social share card at docs/assets/og-image.png.
#
# The card is designed as a normal web page (tools/og-card.html) using the
# school's own colors, then photographed by headless Chrome at exactly the
# 1200x630 that social platforms expect. Editing the card means editing HTML,
# which beats fighting an image editor.
#
# Usage:  sh tools/build-og-image.sh
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --screenshot="$ROOT/docs/assets/og-image.png" \
  --window-size=1200,630 \
  "file://$ROOT/tools/og-card.html"
echo "wrote docs/assets/og-image.png"
