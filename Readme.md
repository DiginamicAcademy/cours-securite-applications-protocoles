<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/Logo-diginamic-color-blk.png">
    <img src="assets/Logo-diginamic-color.svg" alt="Diginamic Formation" width="358">
  </picture>
</p>

# La sécurité des applications et des protocoles réseau par l'attaque

> Cours d'**autoformation** · **RNCP40573** Expert en informatique et systèmes d'information · **brique transversale de sécurité** adossée au bloc **BC03** (conception et développement applicatif)
> 3 journées · supports **rédigés par IA**, relus et validés.

---

## Pourquoi ce cours

Une application ne se contente pas de traiter des données : elle les expose, les
échange et les transforme — chaque point d'entrée, chaque protocole et chaque
dépendance devient alors une porte ouverte sur ces données. Les incidents les plus
coûteux viennent rarement d'attaques sophistiquées : ils viennent d'un code écrit
sans y penser, d'une requête concaténée, d'un message d'erreur trop bavard, d'une
API (Application Programming Interface) sans limitation de débit. Ce cours traite
la sécurité des applications et des protocoles réseau **par l'attaque** : chaque
mécanisme défensif est introduit par la menace qu'il contrarie, puis appliqué au
code, à la configuration et aux flux de données. Vous y travaillez le secure
coding, la sécurité des API et des données, puis les protocoles réseau et le cycle
de vie sécurisé, sur un sujet concret : la place de marché
**Marché des Cévennes** et les données personnelles de ses clients — c'est elle
qui sert de cadre au TP. Un seul élément est noté au bulletin : le QCM
évaluatif de fin de séquence (J9, 20 questions, seuil de réussite 0,7, tentative
unique). Le TP intégrateur, facultatif, est un travail pour pousser la
compréhension, il ne compte pas dans la note. Les chapitres et les exercices
s'appuient, eux, sur le lab Docker de la fromagerie **DIGICHEESE**, partagé
entre les cours du parcours ([DiginamicAcademy/lab-securite](https://github.com/DiginamicAcademy/lab-securite)).
Les enjeux y sont autant
techniques que réglementaires : exposer de telles données engage la responsabilité
de l'organisme au titre du RGPD (Règlement général sur la protection des données).

## À l'issue de ce cours

- **Appliquer** les principes du secure coding — écrire simple, donner le moins
  possible, superposer les barrières — à un code existant.
- **Corriger** les injections dans un code applicatif : requêtes SQL (Structured
  Query Language) paramétrées, validation des entrées, échappement des sorties.
- **Neutraliser** les attaques par injection de script XSS (Cross-Site Scripting)
  par un échappement en sortie maîtrisé et une politique de sécurité du contenu
  CSP (Content Security Policy).
- **Implémenter** une gestion des erreurs et une journalisation qui n'exposent
  aucune information sensible.
- **Auditer** une API au regard de l'OWASP (Open Web Application Security Project)
  API Security Top 10, puis la durcir : authentification, limitation de débit,
  validation de schéma.
- **Protéger** les données sensibles : classification, minimisation, masquage,
  pseudonymisation, chiffrement.
- **Appliquer** les exigences du RGPD à un flux de données : finalité, durée de
  conservation, droits des personnes, notification de violation.
- **Analyser** les failles des protocoles courants — HTTP/S (HyperText Transfer
  Protocol Secure), DNS (Domain Name System), SMTP (Simple Mail Transfer Protocol)
  et SSH (Secure Shell) — et durcir l'architecture qui les porte : segmentation,
  DMZ (zone démilitarisée), approche zero trust (confiance zéro).
- **Intégrer** des contrôles de sécurité automatisés au cycle de développement :
  analyse statique de code, inventaire des dépendances, tests de sécurité.
- **Concevoir** un plan de réponse à incident et **évaluer** la maturité sécurité
  d'un projet data.

## Sommaire

| # | Chapitre | Durée de lecture |
| --- | --- | --- |
| 01 | [Principes du secure coding — écrire pour que ça ne casse pas](01-principes-secure-coding.md) | 40 min |
| 02 | [Validation et injections — séparer les données des instructions](02-validation-et-injections.md) | 50 min |
| 03 | [XSS et sorties — que le texte reste du texte](03-xss-et-sorties.md) | 45 min |
| 04 | [Erreurs et logging — ne rien exposer, tout tracer](04-erreurs-et-logging.md) | 45 min |
| 05 | [Dépendances et configuration — ce qui tourne autour du code](05-dependances-et-configuration.md) | 50 min |
| 06 | [Revue de code sécurité — chercher les patterns, pas relire tout](06-revue-de-code-securite.md) | 45 min |
| 07 | [Sécurité des API — la porte d'entrée des applications modernes](07-securite-api.md) | 45 min |
| 08 | [Auth et limitation d'API — qui appelle, et à quelle vitesse](08-auth-et-limitation-api.md) | 45 min |
| 09 | [Données sensibles — classer, minimiser, masquer](09-donnees-sensibles.md) | 40 min |
| 10 | [RGPD appliqué — la donnée personnelle a une date de péremption](10-rgpd-applique.md) | 40 min |
| 11 | [Pipelines de données — sécuriser chaque étape du flux](11-pipelines-data.md) | 45 min |
| 12 | [Partage et tiers — quand la donnée sort du système](12-partage-et-tiers.md) | 40 min |
| 13 | [Protocoles réseau — ce que le réseau chiffre, et ce qu'il laisse ouvert](13-protocoles-reseau.md) | 60 min |
| 14 | [Architecture réseau — segmenter, cloisonner, ne rien croire sur parole](14-architecture-reseau.md) | 70 min |
| 15 | [DevSecOps et traçabilité des dépendances — sécuriser la chaîne, pas seulement le code](15-devsecops.md) | 55 min |
| 16 | [Tests de sécurité — empêcher la faille corrigée de revenir](16-tests-securite.md) | 55 min |
| 17 | [Réponse à incident — le jour où ça casse](17-reponse-incident.md) | 55 min |
| 18 | [Maturité et perspectives — la sécurité est une trajectoire](18-maturite-et-perspectives.md) | 45 min |
| A | [Glossaire et ressources](A-Glossaire-et-ressources.md) | — |

*Les durées ci-dessus couvrent le contenu obligatoire. Chaque chapitre
propose des approfondissements « Pour aller plus loin » : ils restent
facultatifs et ne sont pas comptés dans ces durées.*

**Travaux pratiques** — les exercices sont intégrés aux chapitres, à la fin
de la partie qui enseigne la notion ; leur correction se déplie sous les questions :

| | Sujet | Durée |
| --- | --- | --- |
| 🟢 | Appliquer les principes du secure coding — dans le chapitre 01 | 25 min |
| 🟢 | Corriger une injection dans une recherche — dans le chapitre 02 | 25 min |
| 🟢 | Échapper les sorties d'un livre d'or — dans le chapitre 03 | 20 min |
| 🟡 | Durcir un endpoint de réservation — dans le chapitre 04 | 50 min |
| 🔵 | Traiter une CVE sur son propre projet — **facultatif**, dans le chapitre 05 | 40 min |
| 🔵 | Auditer un module de gestion des adhésions — **facultatif**, dans le chapitre 06 | 55 min |
| 🟢 | Auditer l'API d'un service de mobilité — dans le chapitre 07 | 25 min |
| 🟡 | Sécuriser un endpoint qui en dit trop — dans le chapitre 09 | 50 min |
| 🔵 | Analyser les risques d'un pipeline de données — dans le chapitre 11 | 55 min |
| 🔴 | Brouillon de registre des traitements — dans le chapitre 12 | libre |
| 🟢 | Durcir le réseau d'une petite entreprise — dans le chapitre 13 | 25 min |
| 🟡 | Intégrer la sécurité dans une intégration continue — dans le chapitre 15 | 50 min |
| 🔵 | Rédiger un mini-plan de réponse à incident — dans le chapitre 17 | 55 min |
| 🔴 | Construire sa feuille de route de sécurité — dans le chapitre 18 | non chronométré |
| 🔵 | [Sécuriser de bout en bout une place de marché et son pipeline de données](tp/TP-INTEGRATEUR.md) — **TP intégrateur, l'un des deux éléments notés du cours** — facultatif, noté sur 20 s'il est rendu | 4 h |

Les quatorze exercices intégrés aux chapitres sont formatifs : leur correction,
dépliable dans le chapitre, reste publique et sert à l'auto-évaluation. Le TP intégrateur, lui, est **noté**, comme le QCM évaluatif de fin de séquence — il reprend l'ensemble du
cours (J7 à J9) et se rend en un dossier unique ; son corrigé est réservé à
l'évaluation et n'est pas publié.

---

## ✅ Checkpoints de fin de journée

À cocher avant de passer à la journée suivante. En cas de doute : ne pas
avancer, revenir au concept concerné, refaire l'exercice.

### Jour 7 — chapitres 01 à 06

- [ ] J'ai lu les chapitres 01 à 06 et les points clés sont clairs.
- [ ] J'ai fait au moins les exercices 🟢 et 🟡 (partie principale), et déplié leur correction dans le chapitre concerné. Les extensions « Pour aller plus loin » sont facultatives.
- [ ] J'ai répondu au QCM formatif, lorsqu'il est disponible, et identifié mes notions à revoir.
- [ ] Je sais expliquer, avec mes mots, les 2-3 idées principales de la journée.
- [ ] Je peux appliquer ces idées à un cas simple (un extrait de code, une config, un flux).

### Jour 8 — chapitres 07 à 12

- [ ] J'ai lu les chapitres 07 à 12 et les points clés sont clairs.
- [ ] J'ai fait au moins les exercices 🟢 et 🟡 (partie principale), et déplié leur correction dans le chapitre concerné. Les extensions « Pour aller plus loin » sont facultatives.
- [ ] J'ai répondu au QCM formatif, lorsqu'il est disponible, et identifié mes notions à revoir.
- [ ] Je sais expliquer, avec mes mots, les 2-3 idées principales de la journée.
- [ ] Je peux appliquer ces idées à un cas simple (un extrait de code, une config, un flux).

### Jour 9 — chapitres 13 à 18

- [ ] J'ai lu les chapitres 13 à 18 et les points clés sont clairs.
- [ ] J'ai fait au moins les exercices 🟢 et 🟡 (partie principale), et déplié leur correction dans le chapitre concerné. Les extensions « Pour aller plus loin » sont facultatives.
- [ ] J'ai répondu au QCM formatif, lorsqu'il est disponible, et identifié mes notions à revoir.
- [ ] Je sais expliquer, avec mes mots, les 2-3 idées principales de la journée.
- [ ] Je peux appliquer ces idées à un cas simple (un extrait de code, une config, un flux).

---

## Aller plus loin

- **OWASP (Open Web Application Security Project) Top 10** — les dix risques les
  plus critiques pour les applications web : <https://owasp.org/www-project-top-ten/>
- **OWASP Cheat Sheet Series** — des fiches pratiques de correction, une par
  sujet (injection SQL, XSS, en-têtes HTTP, journalisation…) :
  <https://cheatsheetseries.owasp.org/>
- **OWASP API Security Top 10** — les risques propres aux API et leurs parades :
  <https://owasp.org/www-project-api-security/>
- **ANSSI (Agence nationale de la sécurité des systèmes d'information) — Guide
  d'hygiène informatique** — les mesures de durcissement d'un service en
  production : <https://messervices.cyber.gouv.fr/guides/guide-dhygiene-informatique>
- **CNIL (Commission nationale de l'informatique et des libertés) — Le RGPD** —
  principes, droits des personnes et sécurité des données personnelles :
  <https://www.cnil.fr/fr/reglement-europeen-protection-donnees>
