# Glossaire et ressources

> **Nature :** annexe de référence · **Usage :** tout au cours

Cette page rassemble les acronymes et les termes techniques du cours, avec leurs définitions, et les ressources de référence — à garder sous la main pendant les trois journées.

---

## Acronymes

| Sigle | Signification | En clair |
| --- | --- | --- |
| **ACL** | Access Control List | la liste de qui a le droit de faire quoi sur une ressource |
| **ANSSI** | Agence nationale de la sécurité des systèmes d'information | l'autorité française de cybersécurité : guides, recommandations, avis |
| **API** | Application Programming Interface | un contrat qui dit comment un programme en appelle un autre |
| **BOLA** | Broken Object Level Authorization | la faille où un appelant lit l'objet d'un autre en changeant un identifiant |
| **CERT** | Computer Emergency Response Team | l'équipe qui publie les avis de sécurité : CERT-FR en France |
| **CI** | intégration continue (Continuous Integration) | la chaîne qui vérifie chaque changement automatiquement |
| **CNIL** | Commission nationale de l'informatique et des libertés | l'autorité française de contrôle des données personnelles |
| **CSP** | Content Security Policy | l'en-tête qui dit au navigateur ce qu'il a le droit de charger |
| **CSV** | Comma-Separated Values | un fichier de tableau où les valeurs sont séparées par des virgules |
| **CTF** | Capture The Flag | un exercice de sécurité sous forme de jeu |
| **CVE** | Common Vulnerabilities and Exposures | l'identifiant normalisé d'une faille connue, comme CVE-2021-44228 |
| **CVSS** | Common Vulnerability Scoring System | la note de gravité d'une faille, de 0 à 10 |
| **DAST** | Dynamic Application Security Testing | les tests d'intrusion automatisés, sur l'application en fonctionnement |
| **DMZ** | demilitarized zone | la zone tampon entre Internet et le réseau interne |
| **DNS** | Domain Name System | l'annuaire qui traduit un nom de domaine en adresse |
| **DNSSEC** | DNS Security Extensions | les extensions qui signent les réponses DNS |
| **DOM** | Document Object Model | l'arbre de la page web, manipulé par le navigateur |
| **DPIA** | Data Protection Impact Assessment | l'analyse d'impact des traitements à risque, prévue par le RGPD |
| **DPO** | délégué à la protection des données | la personne qui suit les obligations RGPD au quotidien |
| **ETL** | Extract, Transform, Load | extraction, transformation, chargement : les trois étapes d'un pipeline de données |
| **GHSA** | GitHub Security Advisory | l'identifiant des avis de sécurité publiés sur GitHub |
| **HDFS** | Hadoop Distributed File System | le système de fichiers distribué de Hadoop |
| **HSTS** | HTTP Strict Transport Security | l'en-tête qui force le navigateur à passer en HTTPS |
| **HTML** | HyperText Markup Language | le langage de balisage des pages web |
| **HTTP** | HyperText Transfer Protocol | le protocole qui transporte les pages et les réponses web |
| **HTTPS** | HTTP Secure | HTTP chiffré par TLS |
| **IA** | intelligence artificielle | |
| **IP** | Internet Protocol | le protocole d'adressage du réseau |
| **ISO** | Organisation internationale de normalisation | l'organisme qui publie les normes, dont ISO 27001 pour la sécurité |
| **JSON** | JavaScript Object Notation | un format de données structurées, très utilisé par les API |
| **JWT** | JSON Web Token | le format de jeton le plus répandu dans les API |
| **KISS** | Keep It Simple, Stupid | le principe : ce qui est simple se trompe moins |
| **LLM** | large language model | un modèle de langage de grande taille |
| **MITM** | Man In The Middle | l'attaque où un tiers s'interpose dans une communication |
| **NVD** | National Vulnerability Database | la base américaine des failles connues |
| **ORM** | Object-Relational Mapping | la bibliothèque qui construit les requêtes SQL à partir d'objets |
| **OWASP** | Open Worldwide Application Security Project | la communauté de référence de la sécurité applicative |
| **PHP** | Hypertext Preprocessor | un langage de développement web |
| **PME** | petite et moyenne entreprise | |
| **REST** | Representational State Transfer | l'architecture d'API la plus répandue sur le web |
| **RGPD** | Règlement général sur la protection des données | le texte européen qui encadre les données personnelles |
| **RIB** | relevé d'identité bancaire | les coordonnées bancaires d'un compte |
| **RNCP** | Répertoire national des certifications professionnelles | le registre des certifications : RNCP40573 est la certification visée ici |
| **S3** | Simple Storage Service | le stockage objet d'Amazon, devenu un standard de fait |
| **SASE** | Secure Access Service Edge | l'architecture qui fusionne réseau et sécurité à la périphérie |
| **SAST** | Static Application Security Testing | l'analyse de sécurité du code source, sans l'exécuter |
| **SBOM** | Software Bill of Materials | la liste de ce qui compose le logiciel : composants et versions |
| **SCA** | Software Composition Analysis | l'analyse des composants d'un projet et de leurs failles connues |
| **SIEM** | Security Information and Event Management | la plateforme qui centralise et corrèle les journaux de sécurité |
| **SLSA** | Supply-chain Levels for Software Artifacts | les niveaux de maturité de la chaîne d'approvisionnement logicielle |
| **SMTP** | Simple Mail Transfer Protocol | le protocole d'envoi du courrier électronique |
| **SPDX** | Software Package Data Exchange | un format standard de SBOM |
| **SQL** | Structured Query Language | le langage des requêtes sur les bases de données |
| **SSH** | Secure Shell | le protocole d'administration à distance, chiffré |
| **SSL** | Secure Sockets Layer | l'ancêtre de TLS — le nom est resté dans les habitudes |
| **STARTTLS** | Start TLS | la commande qui chiffre une connexion déjà ouverte, notamment en SMTP |
| **SSE** | Security Service Edge | la brique de sécurité des services à la périphérie |
| **TD** | travaux dirigés | une série d'exercices, souvent en séquence découverte |
| **TLS** | Transport Layer Security | le protocole qui chiffre les communications réseau |
| **TP** | travaux pratiques | une mise en pratique — ici, le TP intégrateur noté de fin de parcours |
| **UE** | Union européenne | |
| **XML** | Extensible Markup Language | un format de données structurées en balises |
| **XSS** | Cross-Site Scripting | l'injection de script dans une page web |
| **YARN** | Yet Another Resource Negotiator | l'ordonnanceur de ressources de Hadoop |
| **ZAP** | Zed Attack Proxy | l'outil de test d'intrusion web de l'OWASP |

---

## Termes techniques clés

- **Anonymisation** — rendre une donnée impossible à rattacher à une personne, même avec des informations complémentaires. Au-delà, elle ne relève plus du RGPD.
- **Arbitrage** — le choix documenté : ce qu'on fait, ce qu'on écarte, et pourquoi.
- **Chiffrement en transit / au repos** — protéger les données quand elles circulent, puis quand elles sont stockées.
- **Cloisonnement** — découper un système en zones pour qu'une compromission reste locale.
- **Compte de service** — le compte utilisé par un script ou un job, jamais par une personne : droits minimaux, pas de session interactive.
- **Correctif (patch)** — la modification qui supprime une faille connue.
- **Course patch / exploit** — la course entre le défenseur qui applique le correctif et l'attaquant qui écrit l'exploit.
- **Criticité** — ce que vaut un système à protéger, combinant valeur des données, exposition et impact métier.
- **Défense en profondeur** — superposer des protections indépendantes : une couche qui cède n'entraîne pas tout.
- **Donnée personnelle** — toute information qui identifie une personne : nom, adresse, historique d'achat, adresse IP.
- **Durée de conservation** — le temps au-delà duquel une donnée doit être purgée, fixé par table ou par traitement.
- **Échappement de sortie** — transformer les caractères dangereux avant de les afficher, pour que le texte reste du texte.
- **En-têtes de sécurité** — les instructions envoyées au navigateur : CSP, HSTS, X-Content-Type-Options.
- **Fail-closed / fail-open** — en cas d'erreur, bloquer (fail-closed) ou laisser passer (fail-open). La sécurité choisit fail-closed.
- **Faille (vulnérabilité)** — une faiblesse qu'un attaquant peut exploiter.
- **Injection** — faire passer des données pour des instructions : requête SQL, commande système, script.
- **Journalisation** — tracer ce qui se passe, sans y mettre de secret ni de donnée personnelle.
- **Masquage** — ne montrer que la partie nécessaire d'une donnée : les quatre derniers chiffres d'une carte, le début d'un e-mail.
- **Méthodes HTTP** — GET (lire), POST (créer), PUT (remplacer), DELETE (supprimer) : ce que chaque appel demande au serveur.
- **Minimisation** — ne collecter et ne renvoyer que la donnée strictement nécessaire à la finalité.
- **Moindre privilège** — n'accorder que les droits nécessaires, seulement le temps nécessaire.
- **Pseudonymisation** — remplacer un identifiant par un autre, tout en gardant la possibilité de le rattacher (clé conservée ailleurs).
- **Registre des traitements** — la liste des traitements de données personnelles d'une organisation : finalité, données, durée, destinataires.
- **Requête paramétrée** — envoyer la donnée à part de la requête, pour qu'elle ne puisse jamais devenir une instruction.
- **Revue de code** — la lecture ciblée du code pour y chercher des patterns de faiblesse, pas une relecture intégrale.
- **Secret** — une donnée d'accès (clé, jeton, mot de passe) qui vit dans un coffre, jamais dans le code ni dans un journal.
- **Segmentation réseau** — séparer les zones du réseau et ne laisser passer que les flux nécessaires.
- **Stockage objet** — un dépôt de fichiers adressés par clé (S3, MinIO), utilisé par les pipelines de données.
- **Surface d'attaque** — tout ce qui est joignable, visible, ou qui permet d'aller plus loin.
- **Tests de non-régression** — les tests qui empêchent une faille corrigée de revenir à la prochaine modification.
- **Validation d'entrée** — contrôler ce qui entre : type, longueur, format, valeur autorisée.
- **Violation de données** — une fuite ou une perte de données personnelles : elle se déclare à l'autorité de contrôle dans les 72 heures.

---

## Ressources utiles

### Référentiels et vulnérabilités

- **OWASP Top 10** — les dix familles de failles web les plus courantes : https://owasp.org/www-project-top-ten/
- **OWASP Cheat Sheet Series** — les fiches pratiques, une par sujet : https://cheatsheetseries.owasp.org/
- **OWASP ASVS** — le référentiel de vérification d'une application : https://owasp.org/www-project-application-security-verification-standard/
- **OWASP API Security** — les risques propres aux API : https://owasp.org/www-project-api-security/
- **OWASP Web Security Testing Guide** — la méthode de test d'intrusion web : https://owasp.org/www-project-web-security-testing-guide/
- **CWE** — la nomenclature des types de faiblesses : https://cwe.mitre.org/
- **CVE** — les identifiants de failles connues : https://www.cve.org/
- **NVD** — la base de données des failles et de leur gravité : https://nvd.nist.gov/
- **GitHub Advisory Database** — les avis de sécurité par composant : https://github.com/advisories

### Autorités et cadre légal

- **ANSSI** — guides et recommandations : https://cyber.gouv.fr/
- **CERT-FR** — avis et alertes en France : https://www.cert.ssi.gouv.fr/
- **CNIL** — obligations et pratiques des données personnelles : https://www.cnil.fr/
- **RGPD** — le texte officiel : https://eur-lex.europa.eu/eli/reg/2016/679/oj

### Outils

- **OWASP ZAP** — le test d'intrusion web : https://www.zaproxy.org/
- **pip-audit** — l'audit des dépendances Python : https://github.com/pypa/pip-audit
- **bandit** — l'analyse statique de sécurité du code Python : https://bandit.readthedocs.io/
- **gitleaks** — la recherche de secrets dans un dépôt : https://github.com/gitleaks/gitleaks
- **SSL Labs** — le test de configuration TLS d'un site : https://www.ssllabs.com/ssltest/
- **Mozilla SSL Configuration Generator** — les configurations TLS à jour : https://ssl-config.mozilla.org/

### Chaîne d'approvisionnement logicielle

- **CycloneDX** — un format de SBOM : https://cyclonedx.org/
- **SPDX** — l'autre format standard de SBOM : https://spdx.dev/
- **SLSA** — les niveaux de maturité de la chaîne : https://slsa.dev/

### À garder sous la main

- **MDN** — la référence de l'en-tête Content-Security-Policy : https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
- **Have I Been Pwned** — savoir si une adresse a fui : https://haveibeenpwned.com/

*URLs vérifiées le 4 novembre 2026.*
