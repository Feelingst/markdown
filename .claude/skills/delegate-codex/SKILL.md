---
name: delegate-codex
description: Déléguer une tâche de code à Codex (OpenAI) puis la contrôler — Claude écrit la spec, Codex implémente, Claude relit le diff, vérifie, demande des corrections et committe. À utiliser pour toute fonctionnalité ou correction de code dans ce dépôt.
---

# Déléguer à Codex et contrôler

Argument : la demande de l'utilisateur (`$ARGUMENTS`).

## 1. Préparer
- `command -v codex` : s'il manque, dire à l'utilisateur `npm install -g @openai/codex && codex login` et s'arrêter.
- `git status --short` : si l'arbre n'est pas propre, demander s'il faut committer ou stasher avant.
- Lire les fichiers concernés pour écrire une spec juste.

## 2. Écrire la spec
Écrire la spec dans `.codex-runs/spec.md` avec ces sections :
- **Objectif** (1–2 phrases)
- **Fichiers à modifier / créer**
- **Comportement attendu** (cas normaux + cas limites)
- **Critères d'acceptation** (vérifiables)
- **Hors périmètre** (ce qu'il ne faut pas toucher)

## 3. Déléguer
```bash
scripts/codex-task.sh -f .codex-runs/spec.md
```
(timeout long : jusqu'à 10 min)

## 4. Contrôler
- `git diff` complet ; vérifier : respect de la spec, fichiers hors périmètre, bugs, sécurité (chemins de fichiers, uploads, injection), style d'AGENTS.md.
- `cd kernel && python -m compileall -q .` ; démarrer l'app et tester la route touchée si pertinent (`curl`).
- Noter chaque problème : fichier:ligne, problème, correction attendue.

## 5. Itérer (max 3 tours)
S'il y a des problèmes, écrire `.codex-runs/fix.md` avec la liste précise et relancer `scripts/codex-task.sh -f .codex-runs/fix.md`, puis recontrôler.
Après 3 tours sans succès : corriger toi-même si c'est petit, sinon expliquer le blocage à l'utilisateur.
Si une modification est mauvaise et irrécupérable : `git restore` des fichiers concernés (pas de `git reset --hard` sans accord).

## 6. Valider
- Commit avec un message clair (mentionner « implémenté par Codex, relu par Claude »).
- Ajouter l'entrée dans `TASKS.md` (format en tête du fichier).
- Rapport à l'utilisateur : résumé, corrections demandées, vérifications passées, ce qui reste.
