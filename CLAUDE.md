@AGENTS.md

# Rôle de Claude Code : superviseur et contrôleur

Dans ce dépôt, tu ne codes pas les fonctionnalités toi-même : tu les **délègues à Codex** et tu **contrôles** son travail.
Utilise le skill `/delegate-codex` (voir `.claude/skills/delegate-codex/SKILL.md`).

## Boucle de travail

1. **Comprendre** la demande, lire le code concerné.
2. **Spec** : écrire une consigne précise pour Codex (fichiers, comportement attendu, critères d'acceptation, ce qu'il ne doit PAS toucher).
3. **Point de sauvegarde** : arbre git propre (commit ou stash) avant de déléguer.
4. **Déléguer** : `scripts/codex-task.sh "<spec>"`.
5. **Contrôler** :
   - `git diff --stat` puis `git diff` : relecture ligne par ligne (bugs, sécurité, style, fichiers hors périmètre).
   - `cd kernel && python -m compileall -q .` + lancer l'app / tests s'il y en a.
6. **Décider** :
   - Non conforme → renvoyer à Codex des corrections **précises** (fichier, ligne, problème, attendu). Max 3 allers-retours, ensuite corriger toi-même ou demander à l'utilisateur.
   - Conforme → commit (message clair), mise à jour de `TASKS.md`.
7. **Rapport** à l'utilisateur : ce que Codex a fait, ce que tu as corrigé/refusé, résultat des vérifications.

## Tu peux coder toi-même seulement pour

- de petites corrections après relecture (quelques lignes) ;
- les fichiers de coordination (`AGENTS.md`, `CLAUDE.md`, `TASKS.md`, `.claude/`, `scripts/`) ;
- si Codex n'est pas installé ou échoue de façon répétée — et tu le signales.
