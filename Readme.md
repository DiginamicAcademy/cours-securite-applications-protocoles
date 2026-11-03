<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/Logo-diginamic-color-blk.png">
    <img src="assets/Logo-diginamic-color.svg" alt="Diginamic Formation" width="358">
  </picture>
</p>

# La sécurité des applications et des protocoles réseau par l'attaque

> Cours d'**autoformation** · **RNCP40573** Expert en informatique et systèmes d'information · spécialisation **4B Big Data & IA**
> 3 journée(s) · supports **rédigés par IA**, relus et validés.

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
de vie sécurisé, en suivant un fil rouge concret : la boutique en ligne
DIGICHEESE (la fromagerie du fil rouge) et les données personnelles de ses
clients. Les enjeux y sont autant
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
| 01 | [Principes du secure coding — écrire pour que ça ne casse pas](01-principes-secure-coding.md) | 50 min |
| 02 | [Validation et injections — séparer les données des instructions](02-validation-et-injections.md) | 75 min |
| 03 | [XSS et sorties — que le texte reste du texte](03-xss-et-sorties.md) | 60 min |
| 04 | [Erreurs et logging — ne rien exposer, tout tracer](04-erreurs-et-logging.md) | 55 min |
| 05 | [Dépendances et configuration — ce qui tourne autour du code](05-dependances-et-configuration.md) | 65 min |
| 06 | [Revue de code sécurité — chercher les patterns, pas relire tout](06-revue-de-code-securite.md) | 55 min |
| 07 | [Sécurité des API — la porte d'entrée des applications modernes](07-securite-api.md) | 70 min |
| 08 | [Auth et limitation d'API — qui appelle, et à quelle vitesse](08-auth-et-limitation-api.md) | 60 min |
| 09 | [Données sensibles — classer, minimiser, masquer](09-donnees-sensibles.md) | 65 min |
| 10 | [RGPD appliqué — la donnée personnelle a une date de péremption](10-rgpd-applique.md) | 60 min |
| 11 | [Pipelines de données — sécuriser chaque étape du flux](11-pipelines-data.md) | 55 min |
| 12 | [Partage et tiers — quand la donnée sort du système](12-partage-et-tiers.md) | 45 min |
| 13 | [Protocoles réseau — ce que le réseau chiffre, et ce qu'il laisse ouvert](13-protocoles-reseau.md) | 70 min |
| 14 | [Architecture réseau — segmenter, cloisonner, ne rien croire sur parole](14-architecture-reseau.md) | 60 min |
| 15 | [DevSecOps et traçabilité des dépendances — sécuriser la chaîne, pas seulement le code](15-devsecops.md) | 70 min |
| 16 | [Tests de sécurité — empêcher la faille corrigée de revenir](16-tests-securite.md) | 55 min |
| 17 | [Réponse à incident — le jour où ça casse](17-reponse-incident.md) | 50 min |
| 18 | [Maturité et perspectives — la sécurité est une trajectoire](18-maturite-et-perspectives.md) | 55 min |

**Travaux pratiques** — chaque énoncé se fait juste après le chapitre
correspondant, puis se corrige soi-même :

| | Sujet | Durée |
| --- | --- | --- |
| 🟢 | [Appliquer les principes du secure coding](tp/01-appliquer-les-principes.md) · [corrigé](tp/corrige/01-appliquer-les-principes.md) | 25 min |
| 🟢 | [Corriger une injection dans une recherche](tp/02-corriger-injection.md) · [corrigé](tp/corrige/02-corriger-injection.md) | 25 min |
| 🟢 | [Échapper les sorties d'un livre d'or](tp/03-echapper-les-sorties.md) · [corrigé](tp/corrige/03-echapper-les-sorties.md) | 20 min |
| 🟡 | [Durcir un endpoint de réservation](tp/04-durcir-un-endpoint.md) · [corrigé](tp/corrige/04-durcir-un-endpoint.md) | 50 min |
| 🟡 | [Traiter une CVE sur son propre projet](tp/05-traiter-une-cve.md) · [corrigé](tp/corrige/05-traiter-une-cve.md) | 40 min |
| 🔵 | [Auditer un module de gestion des adhésions](tp/06-auditer-un-module.md) · [corrigé](tp/corrige/06-auditer-un-module.md) | 55 min |
| 🟢 | [Auditer l'API d'un service de mobilité](tp/07-auditer-api.md) · [corrigé](tp/corrige/07-auditer-api.md) | 25 min |
| 🟡 | [Sécuriser un endpoint qui en dit trop](tp/09-securiser-endpoint-data.md) · [corrigé](tp/corrige/09-securiser-endpoint-data.md) | 50 min |
| 🔵 | [Analyser les risques d'un pipeline de données](tp/11-analyser-pipeline.md) · [corrigé](tp/corrige/11-analyser-pipeline.md) | 55 min |
| 🔴 | [Brouillon de registre des traitements](tp/12-defi-registre.md) · [corrigé](tp/corrige/12-defi-registre.md) | libre |
| 🟢 | [Durcir le réseau d'une petite entreprise](tp/13-durcir-reseau.md) · [corrigé](tp/corrige/13-durcir-reseau.md) | 25 min |
| 🟡 | [Intégrer la sécurité dans une intégration continue](tp/15-cicd-securise.md) · [corrigé](tp/corrige/15-cicd-securise.md) | 50 min |
| 🔵 | [Rédiger un mini-plan de réponse à incident](tp/17-plan-incident.md) · [corrigé](tp/corrige/17-plan-incident.md) | 55 min |
| 🔴 | [Construire sa feuille de route de sécurité](tp/18-defi-maturite.md) · [corrigé](tp/corrige/18-defi-maturite.md) | non chronométré |

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
