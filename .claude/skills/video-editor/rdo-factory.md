# RDO Factory — référence pour les vidéos clients

Source : artifact « Pipeline RDO Factory »
(https://claude.ai/artifact/BJ5zySJGZeyJfm5zw19QmB). Si ce document et
l'artifact divergent, l'artifact fait foi : relis-le et mets cette fiche à
jour.

RDO = reprise de données (migration de portefeuille vers une nouvelle
plateforme). La RDO Factory est une chaîne de **7 modules** qui va de la
cartographie des données source jusqu'au code de migration. La sortie de
chaque module devient l'entrée du suivant, jusqu'au script Python
exécutable. Les repères **E2 à E5** renvoient aux étapes de la fiche de
cadrage RDO Factory.

## Les 7 modules

| # | Module | Étape | Ce qu'il fait | Sortie |
|---|--------|-------|---------------|--------|
| 1 | Détecteur de portefeuilles (source) | E2 · Détection | Analyse les fichiers du client et déduit la structure réelle des données : entités, colonnes, types, volumes, anomalies. | Profil technique du portefeuille |
| 2 | Faux jeu de données | E2b · Jumeau fictif | Génère, à partir du profil détecté, un jeu de données fictif représentatif, assez réaliste pour étudier le ou les produits du portefeuille en détail, **sans données client réelles**. | Jeu de données fictif |
| 3 | Vérificateur de portefeuille | — | Contrôle que le jeu fictif contient les bonnes données : cohérence des règles métier, valeurs attendues par type de produit, aucune incohérence introduite par la génération. | Jeu de données fictif validé |
| 4 | Analyseur du schéma de données cible | E3 · Analyse cible | Lit la plateforme de destination (DDL, dictionnaires, échantillons) et en déduit la structure cible attendue. | Schéma cible |
| 5 | Outil de création de mapping | E4 · Correspondance | Fait correspondre chaque champ source validé à son équivalent cible : correspondances directes, transformations, valeurs par défaut, cas particuliers. | Mapping champ à champ |
| 6 | Traducteur en Structured English | E5 · Règles | Reformule le mapping en règles lisibles et vérifiables par un humain : RULE, FOR EACH, WHEN, PASS-THROUGH, LOOKUP OR CREATE, FLAG, JOIN… | Règles en Structured English |
| 7 | Générateur de code Python | — | Traduit chaque règle Structured English en script Python (pandas) exécutable sur les données réelles du client. | Script Python de migration |

**Point de fusion** : le module 5 reçoit **deux** entrées, le jeu de
données validé (module 3) et le schéma cible (module 4). C'est leur
rencontre qui produit le mapping. À montrer visuellement dans les vidéos
(deux flux qui convergent).

## Messages clés pour le client

Ne reformuler qu'à partir des faits ci-dessus :

- **Confidentialité** : l'étude détaillée du portefeuille se fait sur un
  jumeau fictif ; aucune donnée client réelle n'est utilisée avant
  l'exécution finale du script.
- **Fiabilité** : un module dédié (3) vérifie le jeu fictif avant toute
  correspondance avec la cible.
- **Transparence** : les règles de migration sont écrites en Structured
  English, lisibles et vérifiables par un humain avant d'être transformées
  en code.
- **Traçabilité** : chaque étape produit un livrable qui alimente la
  suivante, du profil du portefeuille jusqu'au script Python.

Tout chiffre (délais, volumes, taux d'erreur, gains) ou nom de client doit
être fourni et validé par l'utilisateur : ne jamais l'inventer.

## Formats de vidéo suggérés

- **Vue d'ensemble (60–90 s)** : les 7 modules en un schéma animé
  vertical, une carte par module, flèches entre les cartes, fusion au
  module 5. Skill HyperFrames : `faceless-explainer`.
- **Zoom sur un module (30–45 s)** : entrée → ce que fait le module →
  sortie → bénéfice client. Une vidéo par module.
- **Focus confidentialité (30 s)** : modules 1 → 2 → 3, le jumeau fictif.
- **Focus règles lisibles (30–45 s)** : modules 5 → 6 → 7, exemple de
  règle Structured English puis du code Python correspondant (exemple
  fictif, à valider par l'utilisateur).

## Repères visuels de l'artifact

Le schéma d'origine utilise un fond bleu nuit (`#0b1420`), un accent ambre
(`#f0a24a`), du texte clair (`#e8edf2`) et les polices IBM Plex Sans /
IBM Plex Mono. À utiliser pour les vidéos RDO Factory si l'utilisateur le
valide dans `brand.md`.
