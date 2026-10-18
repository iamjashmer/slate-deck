#!/usr/bin/env bash
# Opens a .slate deck in Slate: the app at $SLATE_APP if set, otherwise the
# installed Slate. When Slate is not installed, says where to get it.
# Usage: open_deck.sh <Deck.slate>
set -euo pipefail

# Where people download Slate.
# PLACEHOLDER: replace with the real download page once the DMG is online.
DOWNLOAD_URL="https://example.com/slate (download link coming soon)"

deck=${1:?usage: open_deck.sh <Deck.slate>}
[[ -d $deck ]] || { echo "No deck folder at $deck" >&2; exit 1; }
[[ $deck == *.slate ]] || { echo "The deck folder must end in .slate" >&2; exit 1; }

if [[ -n ${SLATE_APP:-} ]]; then
  open -a "$SLATE_APP" "$deck"
elif open -b com.aprilanting.slate "$deck" 2>/dev/null; then
  :
elif [[ -d /Applications/Slate.app ]]; then
  open -a /Applications/Slate.app "$deck"
else
  echo "Slate is not installed, so the deck was not opened." >&2
  echo "Get Slate (macOS 15 or later): $DOWNLOAD_URL" >&2
  echo "The deck is ready at: $deck" >&2
  exit 1
fi
echo "Opened $deck in Slate."
