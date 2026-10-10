---
name: ameliorer-prompt
description: >-
  Révise et enrichit un prompt brut de l'utilisateur avant de l'exécuter :
  détecte l'intention, comble les manques (contexte, objectif, contraintes,
  format de sortie, critères de réussite), propose une version améliorée, puis
  l'exécute après validation. À utiliser quand l'utilisateur tape
  /ameliorer-prompt, commence son message par "++", ou demande "améliore mon
  prompt", "enrichis ce prompt", "mejora mi prompt", "improve my prompt".
  NE PAS utiliser quand l'utilisateur demande d'exécuter directement
  ("fais-le", "hazlo", "just do it") ou pour optimiser du code.
---

# Améliorer un prompt avant exécution

L'utilisateur te donne un prompt brut, souvent court, écrit vite, parfois
depuis un téléphone. Ton rôle : le transformer en une demande claire et
complète, la lui montrer, puis l'exécuter une fois validée.

Réponds toujours dans la langue de l'utilisateur (français, espagnol,
anglais…). Le prompt amélioré est rédigé dans cette même langue.

## Étape 1 — Comprendre

Lis le prompt brut et identifie :

1. **L'intention** : créer, corriger, rechercher, résumer, rédiger, analyser,
   comparer, automatiser…
2. **Le contexte disponible** : la conversation en cours, le dossier de
   travail (`CLAUDE.md`, `README`, fichiers du projet), les fichiers joints.
   Regarde-les rapidement avant d'inventer quoi que ce soit.
3. **Les manques**, avec cette grille :

| Élément | Question à se poser |
|---|---|
| Objectif | Quel résultat concret est attendu ? Pour quoi faire ? |
| Contexte | Sur quoi on travaille (projet, fichier, public, outil) ? |
| Périmètre | Qu'est-ce qui est inclus / exclu ? |
| Contraintes | Langue, ton, longueur, technologie, délai, budget ? |
| Format de sortie | Fichier, tableau, liste, code, document, artifact ? |
| Critères de réussite | Comment savoir que c'est réussi ? |
| Ressources | Liens, fichiers, skills ou agents utiles déjà disponibles ? |

## Étape 2 — Enrichir

Rédige le prompt amélioré :

- Garde **l'intention exacte** de l'utilisateur. N'ajoute pas d'objectifs
  qu'il n'a pas demandés ; enrichir ≠ élargir.
- Corrige fautes et ambiguïtés, mais garde son vocabulaire métier.
- Comble les manques par des **hypothèses raisonnables**, marquées
  `[hypothèse]`, plutôt que par des questions — sauf si un manque change
  complètement le résultat.
- Si une skill ou un agent disponible convient (liste des skills de la
  session, `~/.claude/skills`, `~/.claude/agents`, ou un catalogue
  `CATALOGUE.md` dans le dossier de travail), cite-le dans le prompt.
- Structure seulement si c'est utile : un prompt simple reste court.

## Étape 3 — Présenter

Affiche exactement ce format, sans rien exécuter encore :

```
### Prompt original
<le texte de l'utilisateur, tel quel>

### Ce que j'ai ajouté
- <2 à 5 puces : manques comblés, hypothèses faites>

### Prompt amélioré
<le prompt enrichi, prêt à copier>

### Question (facultatif)
<au plus 2 questions, uniquement si une réponse changerait le résultat>
```

Termine par une seule ligne : **« Je l'exécute ? (oui / modifie … / non) »**

## Étape 4 — Exécuter

- **oui** (ou ok, vas-y, sí, dale, go) → exécute le prompt amélioré comme
  une demande normale, avec tous tes outils.
- **modifie …** → applique la correction, réaffiche le prompt amélioré,
  redemande.
- **non** → arrête-toi ; l'utilisateur peut copier le prompt ailleurs.

Si l'utilisateur a écrit `++!` au début (au lieu de `++`), saute la
validation : affiche brièvement le prompt amélioré puis exécute-le
directement.

## Exemple

Prompt brut : `fais moi un resume du repo agency agents`

Prompt amélioré :

> Clone https://github.com/msitarzewski/agency-agents et rédige en français
> un résumé d'une page : à quoi sert le projet, comment il est organisé
> (divisions et nombre d'agents), comment l'installer dans Claude Code, la
> licence et l'activité récente. Format : Markdown avec titres courts et un
> tableau des divisions. [hypothèse] Public : utilisateur non développeur,
> lecture sur téléphone.
