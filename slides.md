---
marp: true
theme: default
RNCPBloc: [RNCP40573BC03]
style: |
  section {background-color: #121114}
  h1,h2,h3 {color: #8393f0}
  p,ul,li,td,th {color: #ccc}
  section table {font-size: 0.85em}
  section table td {background-color: #121114}
  section table th {background-color: #272133; font-weight: bolder}
  pre {background-color: #17151a; color: #ccc}
  blockquote {border: 2px green solid; border-left-width: 15px; padding: 0.5em 15px;font-style: italic }
paginate: true
header: "La sécurité des applications et des protocoles réseau par l'attaque"
footer: "![height:20px](https://raw.githubusercontent.com/DiginamicInternal/PublicAssets/refs/heads/main/Logo-diginamic-color-blk.png)"
---

# La sécurité des applications et des protocoles réseau par l'attaque

## Écrire, exécuter et opérer en sécurité — journées 7 à 9

**RNCP40573** (Répertoire national des certifications professionnelles) — Expert en informatique et systèmes d'information
Brique transversale de sécurité adossée au bloc **BC03** du RNCP40573 · 3 journées · autoformation

<!-- Diapositive d'ouverture. Ce cours clôt le parcours sécurité : les
     vulnérabilités ont été étudiées lors des journées précédentes, on apprend
     ici à les corriger et à tenir la sécurité dans la durée. -->

---

## 🎯 Objectifs pédagogiques

À l'issue de ce cours, vous serez capables de :

1. **Écrire** du code applicatif qui résiste aux failles courantes : validation des entrées, requêtes paramétrées, moindre privilège
2. **Analyser** un code pour y repérer les failles restantes, et **prioriser** la dette de sécurité d'un module
3. **Sécuriser** une API (Application Programming Interface) et minimiser les données qu'elle expose
4. **Appliquer** les principes du RGPD (Règlement général sur la protection des données) à un projet data
5. **Intégrer** les contrôles de sécurité dans une chaîne d'intégration continue, et les **tester** automatiquement
6. **Concevoir** une stratégie de réponse à incident simple, et **évaluer** la maturité sécurité d'un projet

---

## Le parcours

| Journée | Thème | Ce qu'on y fait | Durée |
| --- | --- | --- | --- |
| **J7** | Sécurité du code applicatif | Corriger les failles dans le code, sans en introduire de nouvelles | 7 h |
| **J8** | Sécurité des API et des données | Sécuriser les échanges, protéger les données, appliquer le RGPD | 7 h |
| **J9** | Réseaux, protocoles et cycle de vie | Opérer en sécurité : réseau, intégration continue, tests, incident | 7 h |

> Chaque journée suit le même rythme : un concept, pratiqué tout de suite, puis auto-corrigé.

---

## Le fil rouge

Tout le cours s'ancre dans la même histoire : **DIGICHEESE** (la fromagerie du fil rouge) et sa boutique en ligne.

- une **application** web et ses scripts (commandes, exports du soir)
- une **API** qui expose les clients et les commandes
- des **données** : 200 clients, 8 000 commandes, des avis, des produits
- un **lab Docker** : la même application en deux versions — `vulnerable` et `secure`

> Chaque faille étudiée se corrige dans ce lab, au même endroit qu'elle a été vue.

---

## Comment se passe une journée

| Étape | Activité |
| --- | --- |
| 1. **Découverte** | Lire un chapitre du cours |
| 2. **Mise en pratique** | Faire immédiatement le TP (travaux pratiques) associé |
| 3. **Auto-correction** | Se confronter au corrigé, puis passer au bloc suivant |
| 4. **Checkpoint** | En fin de journée, répondre au QCM (questionnaire à choix multiples) et cocher les critères |

> Les sections « Aller plus loin » sont facultatives : elles ne sont jamais exigées pour terminer la journée.

---

## J7 — Sécurité du code applicatif

### Corriger le code, sans en introduire de nouvelles

---

## J7 — le programme

| Bloc | Notion | Durée |
| --- | --- | --- |
| 1 | Principes du secure coding | 50 min |
| 2 | Validation et injections | 75 min |
| 3 | XSS (Cross-Site Scripting) et sorties | 60 min |
| 4 | Erreurs et journalisation | 55 min |
| 5 | Dépendances et configuration | 65 min |
| 6 | Revue de code sécurité | 55 min |

> Les vulnérabilités ont été *étudiées* lors des journées précédentes : ici, on les **corrige** dans le code.

---

## J7 — écrire pour que ça ne casse pas

Le secure coding n'est pas un framework qu'on ajoute par-dessus un programme : c'est une **façon d'écrire**.

- **Écrire simple** — KISS (Keep It Simple, Stupid) : un code court et lisible se relit, se corrige et se vérifie
- **Donner le moins possible** — le moindre privilège : chaque composant ne reçoit que le strict nécessaire
- **Superposer les barrières** — la defense in depth (défense en profondeur) : aucune mesure ne suffit seule

Le moindre privilège se décide avec trois questions : **quelles données ? quels droits ? quel compte ?**

---

## J7 — face à l'erreur : fail-closed

| Ce qui arrive | Fail-open | Fail-closed |
| --- | --- | --- |
| Le programme rencontre une erreur | il continue et renvoie un résultat | il s'arrête et signale l'échec |
| La personne qui récupère le résultat | elle croit que tout va bien | elle sait qu'il faut vérifier |

Valider en entrée, maîtriser la sortie, journaliser sans exposer — et **refuser plutôt qu'accepter** quand l'erreur arrive.

> Une stack trace en production, c'est le plan du système d'incendie affiché sur la porte du coffre-fort.

---

## J8 — Sécurité des API et des données

### Les données sont l'actif, l'API est la porte

---

## J8 — le programme

| Bloc | Notion | Durée |
| --- | --- | --- |
| 1 | Sécurité des API | 70 min |
| 2 | Authentification et limitation | 60 min |
| 3 | Données sensibles : classification, masquage, minimisation | 65 min |
| 4 | RGPD appliqué | 60 min |
| 5 | Pipelines de données | 55 min |
| 6 | Partage et tiers | 45 min |

---

## J8 — qui a accès à quoi, et pour combien de temps

Le RGPD et la sécurité des données ne sont pas deux sujets : ce sont les deux faces du même problème.

- **Minimiser** : ne renvoyer que les champs utiles — une empreinte de mot de passe n'a rien à faire dans une réponse
- **Classer** : publique, interne, confidentielle — et traiter chaque donnée à sa mesure
- **Limiter** : authentifier l'appelant, borner son débit, valider son schéma
- **Conserver** : toute donnée a une date de péremption — archiver, purger, et notifier une fuite de données personnelles en 72 h

> Le meilleur moyen de protéger une donnée, c'est souvent de ne pas la stocker.

---

## J9 — Réseaux, protocoles et cycle de vie sécurisé

### Sécuriser ce qui entoure le code — et savoir réagir

---

## J9 — le programme

| Bloc | Notion | Durée |
| --- | --- | --- |
| 1 | Protocoles réseau : failles et durcissement | 70 min |
| 2 | Architecture réseau : segmentation et zero trust | 60 min |
| 3 | DevSecOps (développement, sécurité, opérations) et traçabilité des dépendances | 70 min |
| 4 | Tests de sécurité | 55 min |
| 5 | Réponse à incident | 50 min |
| 6 | Maturité, veille et perspectives | 55 min |

---

## J9 — ce qui entoure le code

En 2020, SolarWinds : une mise à jour légitime, signée, distribuée à 18 000 clients — et compromise en amont.

- **Le réseau** — HTTP (Hypertext Transfer Protocol), HTTPS (Hypertext Transfer Protocol Secure), DNS (Domain Name System), SMTP (Simple Mail Transfer Protocol) et SSH (Secure Shell) ont été conçus avec les hypothèses de leur époque : ils ne chiffrent pas les mêmes choses
- **La chaîne de livraison** — SAST (Static Application Security Testing), SCA (Software Composition Analysis) et recherche de secrets : les contrôles dans l'intégration continue, pas en fin de course
- **L'inventaire** — le SBOM (Software Bill of Materials) : sans inventaire des composants, pas de réponse rapide quand une CVE (Common Vulnerabilities and Exposures) sort

---

## J9 — quand ça casse : les 5 temps

1. **Détecter** — voir qu'il se passe quelque chose
2. **Contenir** — limiter les dégâts, maintenant
3. **Éradiquer** — supprimer la cause
4. **Restaurer** — remettre en service, proprement
5. **Capitaliser** — le retour d'expérience, sans coupable

> Sans plan écrit, les équipes improvisent — et l'incident dure trois fois plus longtemps. Une fuite de données personnelles se notifie dans les 72 h.

---

## 🐳 Le lab Docker

| | |
| --- | --- |
| **Deux versions** | `vulnerable` et `secure` : chaque faille est corrigée au même endroit qu'elle a été vue |
| **La base** | la base `fromagerie` : users, products, comments, orders |
| **Démarrage** | `cd lab && docker compose up --build -d` |

Comparer les deux fichiers `lab/vulnerable/app.py` et `lab/secure/app.py`, c'est tout le cours en un diff.

---

## 📝 Évaluation

| Élément | Quand | Durée |
| --- | --- | --- |
| QCM formatif (auto-évaluation) | en fin de chaque journée | 15 min |
| Checkpoint de fin de journée | en fin de chaque journée | 15 min |
| QCM évaluatif sur les journées 7 à 9 | en fin de parcours | 30 min |
| Bilan de parcours | en fin de parcours | 30 min |

> Le checkpoint se coche soi-même : on n'avance pas tant que les points clés de la journée ne sont pas clairs.

---

## 📚 Aller plus loin

*Ces approfondissements sont facultatifs.*

- **OWASP** (Open Web Application Security Project) — les guides de bonnes pratiques et les Cheat Sheet Series, langage par langage
- **Les principes de Saltzer et Schroeder** — leur article fondateur sur la protection de l'information
- **La veille** — CERT (Computer Emergency Response Team), GHSA (GitHub Security Advisories), NVD (National Vulnerability Database) et les listes de sécurité des éditeurs
- **OWASP ZAP** (Zed Attack Proxy) — pour aller plus loin sur les tests de sécurité automatisés
- **Le SBOM** — l'inventaire des composants, pour répondre vite quand une dépendance est touchée

---

## Des questions ?

### Le dépôt reste la référence

Pour toute question [adressez-vous au service pédagogie](mailto:pedagogie@diginamic.fr)
