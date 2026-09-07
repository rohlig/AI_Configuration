#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/sync-config.sh [--check|--install|--list] [--yes] [--codex-home PATH]

Commands:
  --check       Compare managed sources with the target (default).
  --install     Prompt before creating or replacing each target file.
  --list        Show the managed source-to-target mappings.

Options:
  --yes         Apply all install changes without per-file prompts.
  --codex-home  Override the target Codex home (also respects CODEX_HOME).
EOF
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-${HOME}/.codex}"
command="check"
assume_yes="false"

while (($#)); do
  case "$1" in
    --check|--install|--list) command="${1#--}" ;;
    --yes) assume_yes="true" ;;
    --codex-home)
      shift
      [[ $# -gt 0 ]] || { echo "--codex-home requires a path" >&2; exit 2; }
      codex_home="$1"
      ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if [[ "$codex_home" != /* ]]; then
  echo "Codex home must be an absolute path: $codex_home" >&2
  exit 2
fi

source_agents="$repo_root/config/global/AGENTS.md"
target_agents="$codex_home/AGENTS.md"
source_config="$repo_root/config/global/config.toml"
target_config="$codex_home/config.toml"

managed_sources=("$source_agents:$target_agents" "$source_config:$target_config")
while IFS= read -r source_agent; do
  agent_name="$(basename "$source_agent")"
  managed_sources+=("$source_agent:$codex_home/agents/ai-configuration/$agent_name")
done < <(find "$repo_root/config/global/agents" -maxdepth 1 -type f -name '*.toml' -print | sort)

if [[ "$command" == "list" ]]; then
  printf '%s\n' "Managed files:"
  for mapping in "${managed_sources[@]}"; do
    printf '  %s -> %s\n' "${mapping%%:*}" "${mapping#*:}"
  done
  exit 0
fi

status=0
files_current() {
  local source_file="$1"
  local target_file="$2"
  [[ -e "$target_file" ]] || return 1
  if [[ "$source_file" == "$source_agents" ]]; then
    python3 "$repo_root/scripts/merge-agents.py" --check "$source_file" "$target_file"
  elif [[ "$source_file" == "$source_config" ]]; then
    python3 "$repo_root/scripts/merge-config.py" --check "$source_file" "$target_file"
  else
    cmp -s "$source_file" "$target_file"
  fi
}

for mapping in "${managed_sources[@]}"; do
  source_file="${mapping%%:*}"
  target_file="${mapping#*:}"
  if [[ ! -e "$target_file" ]]; then
    printf '[missing] %s\n' "$target_file"
    status=1
  elif files_current "$source_file" "$target_file"; then
    printf '[current] %s\n' "$target_file"
  else
    printf '[different] %s\n' "$target_file"
    status=1
  fi
done

[[ "$command" == "check" ]] && exit "$status"

backup_dir="$codex_home/backups/ai-configuration/$(date +%Y%m%d-%H%M%S)"
for mapping in "${managed_sources[@]}"; do
  source_file="${mapping%%:*}"
  target_file="${mapping#*:}"
  if files_current "$source_file" "$target_file"; then
    continue
  fi

  if [[ "$assume_yes" != "true" ]]; then
    printf 'Install %s -> %s? [y/N] ' "$source_file" "$target_file"
    read -r answer
    [[ "$answer" =~ ^[Yy]([Ee][Ss])?$ ]] || { echo "Skipped."; continue; }
  fi

  mkdir -p "$(dirname "$target_file")"
  if [[ -e "$target_file" ]]; then
    mkdir -p "$backup_dir"
    cp -p "$target_file" "$backup_dir/$(basename "$target_file")"
    printf 'Backed up existing file to %s\n' "$backup_dir/$(basename "$target_file")"
  fi
  if [[ "$source_file" == "$source_agents" ]]; then
    python3 "$repo_root/scripts/merge-agents.py" "$source_file" "$target_file"
    printf 'Merged portable instructions into %s\n' "$target_file"
  elif [[ "$source_file" == "$source_config" ]]; then
    python3 "$repo_root/scripts/merge-config.py" "$source_file" "$target_file"
    printf 'Merged portable settings into %s\n' "$target_file"
  else
    cp "$source_file" "$target_file"
    printf 'Installed %s\n' "$target_file"
  fi
done
