# Travaux pratiques — mode d'emploi

Depuis le 06/11/2026, les quatorze exercices, TD et défis du cours ne sont plus
des énoncés de ce dossier : ils sont **intégrés aux chapitres**, à la fin de la
partie qui enseigne la notion, et leur correction se **déplie sous les questions**
(« Voir la correction ») — un corrigé **formatif**, qui reste dans ce dépôt public
et sert à s'auto-corriger. Le TP intégrateur, lui, est **facultatif** ; s'il est
rendu, il est **noté** : son corrigé est réservé à l'évaluation et n'est pas publié.

> ⚖️ **Cadre légal.** Toutes les manipulations de ce cours se pratiquent sur
> **vos propres conteneurs** (lab Docker) et sur des données fictives. Accéder ou
> se maintenir sans droit dans un système d'autrui est un délit (articles 323-1
> et suivants du Code pénal), même « pour tester ». Les tests d'intrusion réels
> se font sous contrat, dans un périmètre défini.

## Ce qui reste dans ce dossier

| Élément | Nature | Durée |
| --- | --- | --- |
| [TP-INTEGRATEUR.md](TP-INTEGRATEUR.md) | **TP intégrateur — l'un des deux éléments notés du cours**, facultatif, noté sur 20 s'il est rendu ; son corrigé n'est pas publié | 4 h |
| [marche-cevennes/](marche-cevennes/) | Le module de commandes à auditer, fourni pour les étapes 1 à 3 du TP intégrateur | — |

## Table des exercices

Les exercices ne se cherchent plus ici : ils sont dans le chapitre indiqué.

| Niveau | Exercice | Où le trouver |
| --- | --- | --- |
| 🟢 | Appliquer les principes du secure coding (20 min) | 01 — Principes du secure coding |
| 🟢 | Corriger une injection dans une recherche (20 min) | 02 — Validation et injections |
| 🟢 | Échapper les sorties d'un livre d'or (15 min) | 03 — XSS et sorties |
| 🟡 | Durcir un endpoint de réservation (30 min) | 04 — Erreurs et logging |
| 🔵 | Traiter une CVE sur son propre projet (25 min) — **facultatif** | 05 — Dépendances et configuration |
| 🔵 | Auditer un module de gestion des adhésions (35 min) — **facultatif** | 06 — Revue de code sécurité |
| 🟢 | Auditer l'API d'un service de mobilité (25 min) | 07 — Sécurité des API |
| 🟡 | Sécuriser un endpoint qui en dit trop (30 min) | 09 — Données sensibles |
| 🔵 | Analyser les risques d'un pipeline de données (35 min) | 11 — Pipelines de données |
| 🔴 | Brouillon de registre des traitements (durée libre) — **facultatif** | 12 — Partage et tiers |
| 🟢 | Durcir le réseau d'une petite entreprise (20 min) | 13 — Protocoles réseau |
| 🟡 | Intégrer la sécurité dans une intégration continue (35 min) | 15 — DevSecOps |
| 🔵 | Rédiger un mini-plan de réponse à incident (40 min) | 17 — Réponse à incident |
| 🔴 | Construire sa feuille de route de sécurité (non chronométré) — **facultatif** | 18 — Maturité et perspectives |
| 🔵 | [Sécuriser de bout en bout une place de marché et son pipeline de données](TP-INTEGRATEUR.md) — **TP intégrateur facultatif, noté sur 20 s'il est rendu** — l'un des deux éléments notés, avec le QCM évaluatif de fin de séquence ; corrigé non publié | les chapitres 01 à 18 (J7-J9) |

Les niveaux suivent la progression 🟢 découverte · 🟡 application · 🔵 intégration ·
🔴 défi facultatif. Un 🔴 ne bloque jamais la progression.

## Comment travailler un exercice

1. **Ouvre le chapitre** indiqué dans la table : l'exercice y porte le titre
   « Exercice 1 — … » (ou « Exercice bonus — … » pour les défis 🔴) et se situe à
   la fin de la partie qui vient de traiter la notion.
2. **Fais-le** par écrit — pour les défis aussi, un livrable court vaut mieux
   qu'une réponse orale.
3. **Déplie « Voir la correction »** sous les questions et compare : la méthode
   compte autant que le résultat.
4. **Note ce qui a manqué**, repasse par la section concernée du chapitre, puis
   avance vers le chapitre suivant.
