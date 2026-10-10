# Pack catalogue d'agents et de skills — pour le dépôt local

Ce pack ajoute à la racine du dépôt (celui qui contient détecteur de
portefeuille, faux jeu de données et POC Kelia) :

```
.claude/
  skills/   20 skills chargées automatiquement par Claude Code
  agents/   18 agents chargés automatiquement par Claude Code
outils/
  catalogue/   catalogue complet (350 agents, 294 skills) + CATALOGUE.md
```

Aucun fichier des trois projets n'est modifié.

## Sélection active (`.claude/`)

**Skills** : ameliorer-prompt, find-skills, python-patterns, python-testing,
tdd-workflow, security-review, security-scan, coding-standards, git-workflow,
verification-loop, search-first, codebase-onboarding, documentation-lookup,
deep-research, postgres-patterns, database-migrations, api-design,
error-handling, repo-scan, data-scraper-agent.

**Agents** : python-reviewer, code-reviewer, security-reviewer, planner,
architect, tdd-guide, refactor-cleaner, doc-updater, database-reviewer,
build-error-resolver, code-explorer, silent-failure-hunter, data-engineer,
ai-engineer, backend-architect, secrets-credential-engineer, appsec-engineer,
test-automation-engineer.

Pour en activer d'autres : copier depuis `outils/catalogue/` vers
`.claude/skills/` (un dossier) ou `.claude/agents/` (un fichier `.md`).

## Installation

1. Dézipper `pack-depot.zip` n'importe où (par exemple dans Téléchargements).
2. Lancer le script avec le chemin du dépôt :

   **Windows (PowerShell)**
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\installer.ps1 -Depot "C:\chemin\vers\le\depot"
   ```

   **macOS / Linux**
   ```bash
   bash installer.sh /chemin/vers/le/depot
   ```

Le script crée la branche `ajout-catalogue-agents`, copie les fichiers et
fait un commit. Il ne fait **aucun push** et s'arrête si le dépôt a des
modifications non commitées.

3. Vérifier, puis fusionner dans la branche principale :
   ```
   git log --stat -1
   git checkout main      # ou master
   git merge ajout-catalogue-agents
   ```

## Répliquer le dépôt en ligne (facultatif)

Créer un dépôt **privé** vide sur GitHub (sans README), puis :
```
git remote add origin https://github.com/Feelingst/<nom-du-depot>.git
git push -u origin main
git push -u origin ajout-catalogue-agents
```
Vérifier avant le premier push qu'aucun secret (clés API, mots de passe,
fichiers `.env`) ni donnée réelle n'est dans le dépôt.

Sources : github.com/affaan-m/ECC, github.com/msitarzewski/agency-agents,
github.com/vercel-labs/skills (licence MIT).
