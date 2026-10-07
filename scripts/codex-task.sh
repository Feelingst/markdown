#!/usr/bin/env bash
# Délègue une tâche à Codex CLI (non interactif) dans la racine du dépôt,
# puis affiche son résumé final et le diff produit.
#
# Usage : scripts/codex-task.sh "<spec de la tâche>"
#         scripts/codex-task.sh -f spec.md
set -euo pipefail

ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$ROOT"

if ! command -v codex >/dev/null 2>&1; then
  echo "Erreur : codex introuvable. Installer avec : npm install -g @openai/codex && codex login" >&2
  exit 127
fi

if [[ "${1:-}" == "-f" ]]; then
  SPEC="$(cat "$2")"
else
  SPEC="${1:?Usage: $0 \"<spec>\" | -f spec.md}"
fi

LOG_DIR="$ROOT/.codex-runs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
LAST_MSG="$LOG_DIR/$STAMP-summary.md"

PROMPT="$SPEC

---
Rappels : respecte AGENTS.md. Ne fais pas de commit. Ne modifie que les fichiers nécessaires.
Termine par un résumé : fichiers modifiés, ce qui a été fait, points incertains."

# --full-auto : Codex peut éditer les fichiers du dépôt sans demander (sandbox workspace-write).
codex exec --full-auto --output-last-message "$LAST_MSG" "$PROMPT" | tee "$LOG_DIR/$STAMP-log.txt"

echo
echo "===== Résumé de Codex ====="
cat "$LAST_MSG" 2>/dev/null || echo "(pas de résumé)"
echo
echo "===== Fichiers modifiés ====="
git status --short
git diff --stat
