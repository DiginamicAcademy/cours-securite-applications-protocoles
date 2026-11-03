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

1. [Principes du secure coding — écrire pour que ça ne casse pas](01-principes-secure-coding.md)

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
