#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# This is a heuristic gate, not a secrets scanner. It catches common accidental
# leaks before publication while allowing intentional documentation such as
# "$HOME/.codex" and the words "API key".
patterns=(
  '/Users/[A-Za-z0-9._-]+'
  '/home/[A-Za-z0-9._-]+'
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
  'sk-[A-Za-z0-9_-]{20,}'
  'gh[pousr]_[A-Za-z0-9]{20,}'
  'xox[baprs]-[A-Za-z0-9-]{20,}'
  'AIza[A-Za-z0-9_-]{20,}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
)

found=0
for pattern in "${patterns[@]}"; do
  if rg -n -I -e "$pattern" . -g '!.git/**' -g '!*.sqlite*' -g '!*.jsonl'; then
    found=1
  fi
done

if ((found)); then
  echo "Public audit failed: review the matches above before publishing." >&2
  exit 1
fi

echo "Public audit passed: no common personal-path, email, token, or private-key patterns found."
