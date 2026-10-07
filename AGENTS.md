# AGENTS.md — règles communes (Codex + Claude Code)

Ce fichier est lu par **Codex** (automatiquement) et par **Claude Code** (via `CLAUDE.md`).
Toute règle qui doit s'appliquer aux deux agents va ici.

## Projet

- `kernel/` : application Flask qui convertit des documents (PDF, DOCX, PPTX, XLSX, HTML, CSV, JSON, YAML, XML, RTF, TXT, MD) en Markdown.
  - `kernel/app.py` : routes Flask.
  - `kernel/converters/` : un convertisseur par famille de formats ; `registry.py` associe extension → fonction.
  - `kernel/templates/`, `kernel/static/` : interface web (PWA optimisée iPhone).
- L'interface utilisateur et le README sont en espagnol : garder cette langue pour les textes visibles.

## Lancer / vérifier

```bash
cd kernel
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m compileall -q .        # vérification syntaxique minimale
python app.py                    # http://127.0.0.1:5000
```

## Règles de code

- Python 3.10+, `from __future__ import annotations`, type hints sur les fonctions publiques.
- Suivre le style existant (petites fonctions, pas de dépendance nouvelle sans raison).
- Nouveau format → ajouter le handler dans `converters/` **et** l'enregistrer dans `registry.py` (HANDLERS + LABELS) **et** dans `ACCEPT_MIME` de `app.py`.
- Ne jamais committer `uploads/`, `outputs/`, `.venv/`.
- Pas de secrets dans le code.

## Coordination entre agents

- **Claude Code = superviseur** : écrit les specs, délègue, relit, valide, committe.
- **Codex = exécutant** : implémente la tâche reçue, rien de plus.
- Codex **ne fait pas de commit** et ne modifie pas `AGENTS.md`, `CLAUDE.md`, `.claude/` ni `scripts/`.
- Codex ne touche qu'aux fichiers nécessaires à la tâche ; s'il pense qu'il faut aller plus loin, il l'écrit dans son résumé final au lieu de le faire.
- À la fin de chaque tâche, Codex termine par un résumé : fichiers modifiés, ce qui a été fait, ce qui reste incertain.
- Le journal partagé est `TASKS.md` (Claude le tient à jour).
