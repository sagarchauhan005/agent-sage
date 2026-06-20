#!/usr/bin/env bash
# Sage SDLC global installer — skills for Cursor, Claude Code, and Codex.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SAGE_HOME="${SAGE_HOME:-$HOME/.sage}"
SOURCE_SKILLS="$REPO_ROOT/.cursor/skills"
GENERATOR="$REPO_ROOT/scripts/generate-global-skills.py"
VERSION="$(tr -d '[:space:]' < "$REPO_ROOT/install/VERSION")"

CURSOR_SKILLS="$HOME/.cursor/skills"
CURSOR_RULES="$HOME/.cursor/rules"
CLAUDE_SKILLS="$HOME/.claude/skills"
CODEX_SKILLS="$HOME/.codex/skills"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
  cat <<EOF
Sage SDLC installer

Usage:
  $(basename "$0")                 Interactive tool selection
  $(basename "$0") --all           Install for Cursor, Claude, and Codex
  $(basename "$0") --cursor        Install Cursor skills + rule only
  $(basename "$0") --claude        Install Claude Code skills only
  $(basename "$0") --codex         Install Codex skills only
  $(basename "$0") --project [DIR] [--no-agents-md]  Bootstrap project (/sage-init equivalent)
  $(basename "$0") --uninstall     Remove global Sage install
  $(basename "$0") --status        Show install state

Environment:
  SAGE_HOME   Global Sage core directory (default: ~/.sage)

After install, /sage-* commands work in any project. Run artifacts go in ./runs/<run-id>/.
EOF
}

log() { printf "${GREEN}→${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}!${NC} %s\n" "$*"; }
err() { printf "${RED}✗${NC} %s\n" "$*" >&2; }

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "Required command not found: $1"
    exit 1
  fi
}

install_core() {
  log "Installing Sage core to $SAGE_HOME"
  mkdir -p "$SAGE_HOME"/{agents,workflows,runs,skills}

  cp "$REPO_ROOT/Agents.md" "$SAGE_HOME/Agents.md"
  cp -R "$REPO_ROOT/agents/." "$SAGE_HOME/agents/"
  cp -R "$REPO_ROOT/workflows/." "$SAGE_HOME/workflows/"
  cp "$REPO_ROOT/runs/_plan-template.md" "$SAGE_HOME/runs/_plan-template.md"
  if [[ -f "$REPO_ROOT/runs/_plan-steps-template.md" ]]; then
    cp "$REPO_ROOT/runs/_plan-steps-template.md" "$SAGE_HOME/runs/_plan-steps-template.md"
  fi
  cp "$REPO_ROOT/runs/_manifest-template.json" "$SAGE_HOME/runs/_manifest-template.json"
  if [[ -f "$REPO_ROOT/runs/_manifest-template.schema.json" ]]; then
    cp "$REPO_ROOT/runs/_manifest-template.schema.json" "$SAGE_HOME/runs/_manifest-template.schema.json"
  fi
  cp "$REPO_ROOT/install/claude/CLAUDE.md" "$SAGE_HOME/CLAUDE.md"
  cp "$REPO_ROOT/install/VERSION" "$SAGE_HOME/VERSION"

  python3 "$GENERATOR" "$SOURCE_SKILLS" "$SAGE_HOME/skills"
}

link_skill_dir() {
  local target_root="$1"
  local skill_name="$2"
  local link_path="$target_root/$skill_name"
  local source_path="$SAGE_HOME/skills/$skill_name"

  if [[ ! -d "$source_path" ]]; then
    warn "Skipping missing skill: $skill_name"
    return 0
  fi

  mkdir -p "$target_root"
  if [[ -L "$link_path" || -e "$link_path" ]]; then
    rm -rf "$link_path"
  fi
  ln -s "$source_path" "$link_path"
}

install_tool_skills() {
  local tool="$1"
  local target=""

  case "$tool" in
    cursor) target="$CURSOR_SKILLS" ;;
    claude) target="$CLAUDE_SKILLS" ;;
    codex)  target="$CODEX_SKILLS" ;;
    *) err "Unknown tool: $tool"; return 1 ;;
  esac

  log "Linking Sage skills for $tool → $target"
  for skill_dir in "$SAGE_HOME/skills"/*/; do
    link_skill_dir "$target" "$(basename "$skill_dir")"
  done
}

install_cursor_rule() {
  mkdir -p "$CURSOR_RULES"
  local dest="$CURSOR_RULES/sage-system.mdc"
  cp "$REPO_ROOT/install/cursor/sage-system.mdc" "$dest"
  log "Installed Cursor rule → $dest"
}

write_install_manifest() {
  local tools_csv="$1"
  local agents_md_sha=""
  if [[ -f "$SAGE_HOME/Agents.md" ]]; then
    agents_md_sha="$(shasum -a 256 "$SAGE_HOME/Agents.md" | awk '{print $1}')"
  fi
  python3 - "$SAGE_HOME" "$VERSION" "$REPO_ROOT" "$tools_csv" "$agents_md_sha" <<'PY'
import json, sys
from datetime import datetime, timezone

sage_home, version, source, tools_csv, agents_md_sha = sys.argv[1:6]
tools = [t.strip() for t in tools_csv.split(",") if t.strip()]
manifest = {
    "version": version,
    "installed_at": datetime.now(timezone.utc).isoformat(),
    "sage_home": sage_home,
    "source_repo": source,
    "tools": tools,
}
if agents_md_sha:
    manifest["agents_md_sha256"] = agents_md_sha
path = f"{sage_home}/install.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")
print(path)
PY
}

read_global_agents_sha() {
  python3 - "$SAGE_HOME/install.json" 2>/dev/null <<'PY' || true
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
if p.is_file():
    data = json.loads(p.read_text(encoding="utf-8"))
    print(data.get("agents_md_sha256", ""))
PY
}

bootstrap_project() {
  local project_dir="${1:-.}"
  local copy_agents="${2:-yes}"
  project_dir="$(cd "$project_dir" && pwd)"
  mkdir -p "$project_dir/runs"
  if [[ ! -f "$project_dir/runs/.gitkeep" ]]; then
    touch "$project_dir/runs/.gitkeep"
  fi
  log "Bootstrapped $project_dir/runs/ (Sage run artifacts directory)"

  local sage_version=""
  if [[ -f "$SAGE_HOME/VERSION" ]]; then
    sage_version="$(tr -d '[:space:]' < "$SAGE_HOME/VERSION")"
  fi

  local local_agents="false"
  local agents_action="skipped"
  local global_sha=""
  global_sha="$(read_global_agents_sha)"

  if [[ "$copy_agents" == "yes" && -f "$SAGE_HOME/Agents.md" ]]; then
    local project_sha=""
    if [[ -f "$project_dir/Agents.md" ]]; then
      project_sha="$(shasum -a 256 "$project_dir/Agents.md" | awk '{print $1}')"
    fi
    if [[ ! -f "$project_dir/Agents.md" ]]; then
      cp "$SAGE_HOME/Agents.md" "$project_dir/Agents.md"
      log "Copied Agents.md → $project_dir/Agents.md"
      local_agents="true"
      agents_action="copied"
    elif [[ -n "$global_sha" && "$project_sha" != "$global_sha" ]]; then
      cp "$SAGE_HOME/Agents.md" "$project_dir/Agents.md"
      log "Refreshed stale Agents.md from \$HOME/.sage/Agents.md"
      local_agents="true"
      agents_action="refreshed"
    elif [[ -f "$project_dir/Agents.md" ]]; then
      local_agents="true"
      agents_action="unchanged"
      log "Agents.md already matches global Sage contract"
    fi
  elif [[ -f "$project_dir/Agents.md" ]]; then
    local_agents="true"
    agents_action="unchanged"
    log "Using existing $project_dir/Agents.md (copy skipped)"
  else
    warn "No ./Agents.md — agents will use \$HOME/.sage/Agents.md until you add one"
  fi

  python3 - "$project_dir" "$SAGE_HOME" "$sage_version" "$local_agents" "$global_sha" <<'PY'
import json, sys
from datetime import datetime, timezone

project_dir, sage_home, sage_version, local_agents, agents_md_sha = sys.argv[1:6]
data = {
    "initialized_at": datetime.now(timezone.utc).isoformat(),
    "sage_home": sage_home,
    "sage_version": sage_version,
    "local_agents_md": local_agents == "true",
    "next_command": "sage-orchestrator",
}
if agents_md_sha:
    data["agents_md_sha256"] = agents_md_sha
path = f"{project_dir}/.sage-project.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(path)
PY
  if [[ "$agents_action" == "refreshed" ]]; then
    warn "If you customized Agents.md, restore from git or add overrides below a project-specific section."
  fi

  if [[ "$copy_agents" == "yes" && -f "$SAGE_HOME/CLAUDE.md" && ! -f "$project_dir/CLAUDE.md" ]]; then
    cp "$SAGE_HOME/CLAUDE.md" "$project_dir/CLAUDE.md"
    log "Copied CLAUDE.md → $project_dir/CLAUDE.md"
  fi
}

install_tools() {
  local tools=("$@")
  need_cmd python3
  install_core

  local csv=""
  for tool in "${tools[@]}"; do
    install_tool_skills "$tool"
    csv="${csv}${tool},"
    if [[ "$tool" == "cursor" ]]; then
      install_cursor_rule
    fi
  done
  csv="${csv%,}"

  local manifest_path
  manifest_path="$(write_install_manifest "$csv")"
  log "Wrote install manifest → $manifest_path"
}

interactive_select() {
  echo ""
  echo "Sage SDLC installer (v$VERSION)"
  echo "================================"
  echo "Select AI tools to configure (global /sage-* skills):"
  echo "  1) Cursor   ($CURSOR_SKILLS)"
  echo "  2) Claude   ($CLAUDE_SKILLS)"
  echo "  3) Codex    ($CODEX_SKILLS)"
  echo "  a) All"
  echo "  q) Quit"
  echo ""
  read -r -p "Choice [1/2/3/a/q]: " choice

  local tools=()
  case "$choice" in
    1) tools=(cursor) ;;
    2) tools=(claude) ;;
    3) tools=(codex) ;;
    a|A) tools=(cursor claude codex) ;;
    q|Q) echo "Aborted."; exit 0 ;;
    *) err "Invalid choice: $choice"; exit 1 ;;
  esac

  install_tools "${tools[@]}"

  echo ""
  read -r -p "Bootstrap ./runs/ in current directory ($(pwd))? [y/N]: " bootstrap
  if [[ "$bootstrap" =~ ^[yY]$ ]]; then
    bootstrap_project "."
  fi

  echo ""
  log "Done. Open any project and use /sage-plan, /sage-orchestrator, etc."
  log "Re-run this script after updating agent-sage to refresh ~/.sage."
}

show_status() {
  echo "Sage install status"
  echo "==================="
  if [[ -f "$SAGE_HOME/install.json" ]]; then
    cat "$SAGE_HOME/install.json"
    echo ""
  else
    warn "No install manifest at $SAGE_HOME/install.json"
  fi

  if [[ -d "$SAGE_HOME/skills" ]]; then
    echo "Skills in $SAGE_HOME/skills:"
    ls -1 "$SAGE_HOME/skills" 2>/dev/null || true
    echo ""
  fi

  for pair in "cursor:$CURSOR_SKILLS" "claude:$CLAUDE_SKILLS" "codex:$CODEX_SKILLS"; do
    local name="${pair%%:*}"
    local dir="${pair##*:}"
    echo "$name links:"
    ls -1 "$dir"/sage-* "$dir"/about-sage 2>/dev/null || echo "  (none)"
    echo ""
  done
}

uninstall_sage() {
  if [[ -f "$SAGE_HOME/install.json" ]]; then
    log "Removing tool skill links"
    for skill_dir in "$SAGE_HOME/skills"/*/; do
      [[ -d "$skill_dir" ]] || continue
      local name
      name="$(basename "$skill_dir")"
      for root in "$CURSOR_SKILLS" "$CLAUDE_SKILLS" "$CODEX_SKILLS"; do
        if [[ -L "$root/$name" ]]; then
          rm -f "$root/$name"
          log "Removed link $root/$name"
        fi
      done
    done
  fi

  if [[ -f "$CURSOR_RULES/sage-system.mdc" ]]; then
    rm -f "$CURSOR_RULES/sage-system.mdc"
    log "Removed Cursor rule"
  fi

  if [[ -d "$SAGE_HOME" ]]; then
    read -r -p "Delete $SAGE_HOME entirely? [y/N]: " confirm
    if [[ "$confirm" =~ ^[yY]$ ]]; then
      rm -rf "$SAGE_HOME"
      log "Removed $SAGE_HOME"
    else
      warn "Left $SAGE_HOME on disk"
    fi
  fi
}

main() {
  if [[ $# -eq 0 ]]; then
    interactive_select
    return 0
  fi

  case "$1" in
    -h|--help)
      usage
      ;;
    --all)
      install_tools cursor claude codex
      log "Done. Use /sage-* in any project."
      ;;
    --cursor)
      install_tools cursor
      ;;
    --claude)
      install_tools claude
      ;;
    --codex)
      install_tools codex
      ;;
    --project)
      shift
      local project_dir="."
      local copy_agents="yes"
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --no-agents-md) copy_agents="no"; shift ;;
          --copy-agents-md) copy_agents="yes"; shift ;;
          -*) err "Unknown project flag: $1"; exit 1 ;;
          *) project_dir="$1"; shift ;;
        esac
      done
      if [[ ! -f "$SAGE_HOME/install.json" ]]; then
        err "Global Sage not installed. Run: sage install --all  (or npx agent-sage install --all)"
        exit 1
      fi
      bootstrap_project "$project_dir" "$copy_agents"
      log "Project ready. Use /sage-orchestrator or /sage-plan next."
      ;;
    --status)
      show_status
      ;;
    --uninstall)
      uninstall_sage
      ;;
    *)
      err "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
}

main "$@"
