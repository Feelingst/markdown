#!/usr/bin/env bash
set -euo pipefail
DEPOT="${1:?Usage : bash installer.sh /chemin/vers/le/depot}"
PACK="$(cd "$(dirname "$0")" && pwd)"
BRANCHE="ajout-catalogue-agents"

[ -d "$DEPOT/.git" ] || { echo "Pas de dépôt git dans : $DEPOT"; exit 1; }
cd "$DEPOT"
[ -z "$(git status --porcelain)" ] || { echo "Le dépôt a des modifications non commitées. Commite-les ou mets-les de côté (git stash), puis relance."; exit 1; }
git show-ref --quiet "refs/heads/$BRANCHE" && { echo "La branche $BRANCHE existe déjà."; exit 1; }

git checkout -b "$BRANCHE"
mkdir -p .claude/skills .claude/agents outils
cp -R "$PACK/.claude/skills/." .claude/skills/
cp -R "$PACK/.claude/agents/." .claude/agents/
cp -R "$PACK/outils/catalogue" outils/
cp "$PACK/LISEZMOI.md" outils/catalogue/LISEZMOI-pack.md

git add .claude outils
git commit -m "Ajoute le catalogue d'agents et de skills (.claude/ et outils/catalogue)"
echo
echo "Terminé sur la branche $BRANCHE. Aucun push effectué."
git log --stat -1 | head -8
