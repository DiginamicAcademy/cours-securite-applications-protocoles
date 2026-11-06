[← Chapitre précédent](12-partage-et-tiers.md) · [Sommaire](Readme.md) · [Chapitre suivant →](14-architecture-reseau.md)

# Protocoles réseau — ce que le réseau chiffre, et ce qu'il laisse ouvert

> Le courrier électronique naît en 1982 avec SMTP (Simple Mail Transfer Protocol, le
> protocole d'envoi du courrier), dans un monde de confiance : les machines se
> connaissent, personne ne ment, et le réseau est un campus universitaire. Quarante
> ans plus tard, les mêmes protocoles transportent nos mots de passe. DNS (Domain
> Name System, l'annuaire qui traduit les noms de domaine en adresses) résout les
> noms, SSH (Secure Shell, l'accès distant chiffré) administre les serveurs, HTTPS
> (la version chiffrée du protocole du web) protège les pages — et chacun garde les
> hypothèses de son époque.

**Durée de lecture :** 60 min hors approfondissements facultatifs · **Prérequis :** les vulnérabilités web des journées
précédentes, la notion de chiffrement

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Décrire** ce que chaque protocole courant chiffre réellement — et ce qui circule
  en clair malgré lui.
- **Repérer** les failles de conception héritées des protocoles anciens : interception,
  dégradation forcée, usurpation de nom.
- **Décider** des mesures de durcissement adaptées à un service : HTTPS imposé,
  résolution de noms authentifiée, accès par clé.
- **Vérifier** sur un service réel les en-têtes qui attestent d'une connexion chiffrée.

---

## I. HTTPS, DNS, SMTP, SSH — ce que chacun chiffre (ou pas)

Quatre protocoles, quatre époques. Ce que chacun protège dépend de ce que son
concepteur voulait protéger — et les menaces de 1982 n'étaient pas celles
d'aujourd'hui.

| Protocole | Né en | Ce qu'il chiffre | Ce qui reste ouvert |
| --- | --- | --- | --- |
| **DNS** | 1983 | rien, dans sa version d'origine | la requête et la réponse : n'importe qui peut dire « ce nom pointe ici » |
| **SMTP** | 1982 | rien au départ, le chiffrement est venu après | le contenu du courrier et les identifiants, si le transport n'est pas chiffré |
| **HTTP** | 1991 | rien | tout : pages, formulaires, jetons de session, cookies |
| **SSH** | 1995 | tout, dès l'origine | la confiance accordée à la première connexion (voir plus bas) |

HTTPS n'est pas un protocole à part : c'est HTTP (HyperText Transfer Protocol, le
protocole du web) transporté dans TLS (Transport Layer Security, la couche de
chiffrement qui sécurise les échanges). La même logique vaut ailleurs : la version
chiffrée de SMTP repose sur TLS, et SSH embarque son propre chiffrement.

Ce que TLS garantit, concrètement :

- la **confidentialité** — personne sur le chemin ne lit ce qui circule ;
- l'**intégrité** — personne ne modifie un octet sans que ça se voie ;
- l'**authentification du serveur** — le certificat prouve à qui vous parlez.

Ce que TLS **ne** garantit **pas** : que le site est honnête, que vos données sont
bien stockées côté serveur, ou que le nom de domaine que vous avez tapé est celui
que vous vouliez. Un site de phishing parfaitement chiffré reste un site de
phishing.

> ⚠️ **Point d'attention** —
> Le cadenas du navigateur ne dit pas « ce site est sûr ». Il dit « cet échange est
> chiffré et le serveur prouve être le propriétaire du nom de domaine ». La nuance
> change tout quand on évalue un risque.

> 🧪 **Atelier rapide (8 min)**
>
> Comparez les en-têtes d'un service local en clair et d'un service réel chiffré :
>
```bash
curl -I http://localhost:8080
curl -I https://tutor.diginamic.fr/docs
```

> (La seconde commande interroge un service de production : une seule requête de
> lecture, jamais plus.) Notez les en-têtes présents d'un côté et absents de
> l'autre, en particulier `Strict-Transport-Security` et `Server`. Que dit
> l'absence d'en-tête de sécurité sur la configuration du service ?

---

## II. Failles courantes

Les protocoles anciens ont été conçus pour un réseau amical. Les attaques
d'aujourd'hui exploitent précisément ce qu'ils n'ont pas prévu.

### Usurpation de résolution de noms

Le DNS d'origine répond sans preuve. Quiconque peut répondre plus vite que le
serveur légitime — ou corrompre un cache — redirige les victimes vers une machine
contrôlée par l'attaquant, tout en affichant le bon nom de domaine. C'est le
**DNS spoofing** (usurpation de réponse DNS). La victime tape le bon nom, obtient
la mauvaise machine, et si elle accepte n'importe quel certificat, elle ne voit
rien.

### Interception et dégradation forcée

Deux attaques du même genre, très employées contre les protocoles qui chiffrent
« si possible » :

| Attaque | Ce que fait l'attaquant | Protocole visé |
| --- | --- | --- |
| **Interception** | le MITM (man in the middle, l'attaque par personne interposée) se place entre le client et le serveur et relaie les échanges | tous |
| **Dégradation forcée** (downgrade) | fait croire au client que le serveur ne sait pas chiffrer, pour récupérer la version en clair | SMTP, les anciennes versions de TLS |
| **Interception de la montée en chiffrement** | laisse passer la commande de chiffrement, l'annule, continue en clair | STARTTLS (la commande qui négocie le chiffrement en cours de connexion) |

> 🚨 **Piège à éviter** —
> « Notre messagerie est chiffrée, on utilise STARTTLS » ne suffit pas. Si le
> repli en clair est accepté, un attaquant sur le chemin obtient exactement ce
> qu'il veut. Un chiffrement optionnel est un chiffrement contournable.

---

## III. Durcissement

Chaque faille ci-dessus a une réponse directe, applicable sans réécrire le
protocole.

### Imposer le chiffrement au lieu de le proposer

HSTS (HTTP Strict Transport Security, l'en-tête qui interdit le repli en clair)
dit au navigateur : « pour ce domaine, le HTTPS est obligatoire, et ce pendant un
an ». Même si l'utilisateur tape `http://`, même si un lien propose le clair, le
navigateur refuse et chiffre.

```bash
# Ce que le serveur doit renvoyer, en tête de chaque réponse
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Authentifier les réponses DNS

DNSSEC (DNS Security Extensions, les extensions de sécurité du DNS) fait signer
les réponses de résolution par le détenteur de la zone. Le client vérifie la
signature et refuse une réponse falsifiée. Ce n'est pas du chiffrement — la
requête reste lisible — mais l'usurpation devient détectable.

### Administrer par clé, pas par mot de passe

Sur SSH, deux façons de s'authentifier :

| Mécanisme | Résistance | Ce qui reste à faire |
| --- | --- | --- |
| Mot de passe | faible — devinable, réutilisable, interceptable | le désactiver purement |
| Clé publique | forte — la clé privée ne quitte jamais le poste | protéger la clé, limiter les comptes autorisés |

Le durcissement standard d'un serveur SSH tient en quelques lignes de
configuration : clés uniquement, comptes nommés, journalisation des connexions.

```text
PasswordAuthentication no
PermitRootLogin no
AllowUsers admin-data
```

---

### Exercice 1 — Durcir le réseau d'une petite entreprise (20 min)

#### Contexte

Les **Éditions Belcastel** publient une vingtaine de titres par an et vendent leurs
livres en ligne. L'infrastructure a grandi au fil des besoins, sans plan de réseau.
Voici ce qui tourne aujourd'hui :

| Machine | Rôle | Ce qui est ouvert |
| --- | --- | --- |
| `web-boutique` | boutique en ligne | ports 80 et 443 depuis Internet |
| `admin-boutique` | back-office de la boutique | port 80, depuis Internet **et** depuis le réseau interne |
| `messagerie` | serveur de courrier interne | port 25, en clair, depuis Internet |
| `bdd-commandes` | base des commandes | port 3306 ouvert à tout le réseau interne |
| `sauvegarde` | copie des sauvegardes | partage de fichiers ouvert à tous les postes |
| poste du prestataire | maintenance à distance | port 22 depuis Internet, authentification par mot de passe |

Tout est sur **un seul réseau plat** : chaque machine peut joindre toutes les
autres. L'administrateur résume : « Ça marche depuis des années. »

---

#### Consignes

##### Partie 1 — Repérer les flux en clair et les expositions

Listez, dans le tableau ci-dessus, les lignes qui posent problème. Pour chacune,
dites s'il s'agit d'un **flux en clair**, d'une **exposition inutile** ou d'un
**accès trop large**, et pourquoi.

##### Partie 2 — Regrouper les machines en zones

 Regroupez les six machines
en **trois zones** : une zone publique, une zone interne, une zone de données.
Justifiez chaque placement en une phrase.

##### Partie 3 — Décrire les flux autorisés

Pour chaque zone, indiquez **qui a le droit de joindre qui**, et sur quel port.
Un flux non cité doit être refusé. Complétez ce tableau :

| De | Vers | Port | Autorisé ? |
| --- | --- | --- | --- |
| Internet | `web-boutique` | 443 | oui |
| Internet | `web-boutique` | 80 | à décider |
| `web-boutique` | `bdd-commandes` | 3306 | à décider |
| poste du prestataire | `admin-boutique` | 22 | à décider |
| postes du bureau | `sauvegarde` | partage | à décider |

##### Partie 4 — Durcir les accès restants

Parmi les accès que vous maintenez, choisissez **deux durcissements** du chapitre
(chiffrement imposé, authentification par clé, restriction de comptes) et décrivez
la mesure exacte à appliquer, machine par machine.

---

#### ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque ligne que je signale est rattachée à une **catégorie** (flux en clair,
  exposition inutile, accès trop large), et pas seulement décrite.
- [ ] Mes **trois zones** sont nommées, et chaque machine y est placée avec une
  justification.
- [ ] Mon tableau de flux dit **oui ou non** pour chaque ligne, et tout ce qui n'est
  pas cité est refusé par défaut.
- [ ] Mes deux durcissements sont **applicables tels quels** : je dis quoi changer,
  sur quelle machine.
- [ ] Je n'ai pas proposé de mesure qui empêche la maintenance ou la sauvegarde de
  fonctionner.

---

#### Pour aller plus loin

*Facultatif.* Si vous ne pouviez ajouter qu'**une seule** règle de pare-feu à ce
réseau, laquelle choisiriez-vous pour réduire le plus le risque, et pourquoi ?

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Repérer les flux en clair et les expositions

**Éléments attendus :**

| Ligne | Catégorie | Pourquoi c'est un problème |
| --- | --- | --- |
| `messagerie`, port 25 en clair | Flux en clair | Le courrier et les identifiants de connexion transitent lisibles par quiconque est sur le chemin. |
| `admin-boutique`, port 80 | Flux en clair | Le back-office est administré sans chiffrement : mots de passe et jetons de session circulent en clair. |
| `admin-boutique`, depuis Internet | Exposition inutile | Un back-office n'a rien à faire accessible depuis l'extérieur : c'est une surface d'attaque offerte. |
| poste du prestataire, port 22 depuis Internet | Exposition inutile + accès trop large | Un accès d'administration ouvert sur Internet avec un mot de passe est la combinaison la plus recherchée. |
| `bdd-commandes`, port 3306 pour tout le réseau | Accès trop large | N'importe quel poste compromis peut joindre la base des commandes directement. |
| `sauvegarde`, partage ouvert à tous | Accès trop large | La copie de sécurité vaut ce que vaut son accès : ouverte à tous, elle est compromise dès le premier poste infecté. |

**Ce qu'il faut retenir :** aucun de ces problèmes n'est une panne. Tout
fonctionne, et c'est exactement ce qui les rend invisibles — chaque ligne donne
un peu plus d'accès que ce que le besoin justifie.

---

#### Partie 2 — Regrouper les machines en zones

**Éléments attendus :**

| Zone | Machines | Justification |
| --- | --- | --- |
| **Zone publique** — la zone tampon, ou DMZ (demilitarized zone) | `web-boutique` | Seule machine destinée à être jointe depuis Internet : elle reçoit les coups, elle ne doit rien contenir de sensible. |
| **Zone interne** | `messagerie`, `admin-boutique`, les postes du bureau | Usage interne : ces machines n'ont pas à être visibles depuis l'extérieur. |
| **Zone de données** | `bdd-commandes`, `sauvegarde` | Ce qu'il y a de plus précieux : isolé, joignable seulement par les machines qui en ont besoin. |

**Sur la segmentation :** le but n'est pas de multiplier les machines, mais de
faire en sorte qu'un poste compromis ne mène pas automatiquement aux données. Le
prestataire, lui, n'appartient à aucune zone : son accès doit être traité comme un
flux venant de l'extérieur.

---

#### Partie 3 — Décrire les flux autorisés

**Éléments attendus :**

| De | Vers | Port | Autorisé ? | Raison |
| --- | --- | --- | --- | --- |
| Internet | `web-boutique` | 443 | oui | c'est le service public, chiffré. |
| Internet | `web-boutique` | 80 | uniquement pour rediriger vers le 443 | le clair ne sert qu'à renvoyer vers le chiffré, jamais à servir du contenu. |
| `web-boutique` | `bdd-commandes` | 3306 | oui | la boutique doit lire et écrire les commandes ; c'est le seul chemin vers la base. |
| poste du prestataire | `admin-boutique` | 22 | oui, mais depuis un point d'entrée unique et avec une clé | la maintenance doit rester possible, sans exposition directe. |
| postes du bureau | `sauvegarde` | partage | non | les postes n'ont rien à faire sur la copie de sécurité : seul le serveur qui produit les sauvegardes y écrit. |

**Erreurs fréquentes :** autoriser « tout le réseau interne » vers la zone de
données par facilité, ou oublier de refuser explicitement ce qui n'est pas cité.
Une règle de pare-feu qui n'autorise rien par défaut est la seule qui tient dans
le temps.

---

#### Partie 4 — Durcir les accès restants

**Éléments attendus** (deux mesures parmi celles du chapitre) :

- **Authentification par clé sur le poste du prestataire** — désactiver
  l'authentification par mot de passe sur le port 22, installer une clé publique
  par intervenant, et journaliser les connexions. Un mot de passe deviné ne donne
  alors plus rien.
- **Chiffrement imposé sur la boutique** — faire répondre `web-boutique` avec
  l'en-tête qui interdit le repli en clair, et faire du port 80 une simple
  redirection vers le port 443. L'administration passe alors obligatoirement par
  le chiffré.
- **Compte dédié pour la maintenance** — le prestataire ne reçoit pas un compte
  administrateur général, mais un compte limité à `admin-boutique`, avec les
  seuls droits nécessaires à sa mission.

**Sur le choix des mesures :** un durcissement qui empêche la maintenance de
fonctionner sera désactivé à la première urgence. Les mesures ci-dessus gardent
chaque usage légitime — elles retirent seulement ce que personne n'utilisait.

---

#### Points à retenir

- Un réseau plat transforme chaque poste compromis en accès à tout : la
  **segmentation** casse cette chaîne.
- Les flux en clair (courrier, administration) livrent identifiants et contenus à
  quiconque est sur le chemin : le chiffrement se **décide**, il n'arrive pas
  seul.
- Une exposition inutile (back-office depuis Internet, accès d'administration
  ouvert) est un risque que personne n'a demandé : la fermer ne casse rien.
- Par défaut, **tout ce qui n'est pas explicitement autorisé est refusé**.

</details>

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour terminer
la journée.*

- **TLS 1.3** — la version actuelle du protocole raccourcit la négociation à un
  aller-retour, supprime les algorithmes anciens et chiffre davantage d'en-têtes.
  Une migration vers TLS 1.3 est souvent l'occasion de nettoyer toute la
  configuration de chiffrement.
- **DoH et DoT** — chiffrer la résolution de noms protège la navigation de
  l'observation, mais concentre la confiance sur quelques résolveurs : un choix
  d'architecture, pas une simple case à cocher.
- **La surveillance des certificats** — les journaux publics de certificats
  permettent de détecter un certificat émis pour votre domaine sans votre accord.
  Un abonnement à ces alertes coûte quelques minutes et en sauve des jours.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Le détail de l'attaque STARTTLS**
>
> Le cas de STARTTLS est emblématique : le client annonce « je peux chiffrer », le
> serveur répond « moi aussi », puis les deux basculent. Entre les deux messages,
> l'attaquant peut effacer la proposition — les deux extrémités croient que l'autre
> ne chiffre pas et poursuivent en clair. Le chiffrement était disponible, il n'a
> simplement jamais été utilisé.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
>
> **Les versions et les algorithmes morts**
>
>
> Un protocole vivant garde ses anciennes versions pour compatibilité — et chacune
> porte ses faiblesses. SSL (Secure Sockets Layer, l'ancêtre de TLS) est cassé
> depuis des années ; TLS 1.0 et 1.1 sont déconseillés. Les maintenir « pour les
> vieux clients », c'est offrir à l'attaquant la porte d'entrée qu'il cherche : il
> demande la version faible, le serveur accepte.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Chiffrer la résolution de noms (DoH, DoT)**
>
> La montée en
> chiffrement du DNS lui-même arrive ensuite, avec DoH (DNS over HTTPS, la
> résolution de noms transportée dans HTTPS) et DoT (DNS over TLS).

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **La première visite et le préchargement HSTS**
>
> La première visite reste à protéger par ailleurs —
> d'où l'inscription du domaine dans les listes de préchargement des navigateurs.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> 💡 **Astuce** —
> Avant de désactiver l'authentification par mot de passe, vérifiez qu'une clé est
> bien installée et testée sur un second canal. Se verrouiller dehors de son propre
> serveur est le seul incident que ce durcissement provoque lui-même.

---

## Points clés

- Chaque protocole chiffre **ce que son époque menaçait** : DNS et SMTP d'origine
  ne chiffraient rien, HTTPS et SSH chiffrent presque tout.
- TLS garantit la confidentialité, l'intégrité et l'identité du serveur — **pas**
  l'honnêteté du site ni la sécurité du stockage.
- Un chiffrement **optionnel** est contournable : dégradation forcée, interception
  de la montée en chiffrement, repli en clair.
- Le durcissement tient en trois gestes : **imposer** le chiffrement (HSTS),
  **authentifier** les réponses (DNSSEC), **administrer par clé** (SSH).

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Un site de phishing arbore le cadenas du navigateur. Que peut-on en conclure ?

- A. Que le site est sûr et honnête : le cadenas est délivré après un examen du contenu des pages et de l'éditeur
- B. L'échange est chiffré et le serveur prouve posséder le nom de domaine — rien de plus : un site de phishing chiffré reste un site de phishing
- C. Que les données saisies seront conservées côté serveur, à l'abri sur le réseau local, et jamais revendues à des tiers
- D. Que le nom de domaine affiché est forcément celui que la personne cherchait à joindre, sans confusion avec un imitateur

**2.** « Notre messagerie est chiffrée, on utilise STARTTLS. » Pourquoi cette affirmation ne suffit-elle pas ?

- A. Parce que STARTTLS est un protocole au point cassé depuis l'origine, et qu'il faut le bannir des serveurs modernes
- B. Parce que STARTTLS ne s'emploie qu'avec DNS, et jamais avec la messagerie ni le transfert de fichiers
- C. Parce qu'un repli en clair accepté laisse un attaquant sur le chemin annuler la montée en chiffrement : un chiffrement optionnel est contournable
- D. Parce que le chiffrement d'une session de messagerie ne protège de toute façon jamais les identifiants de connexion

**3.** Une victime tape le bon nom de domaine mais aboutit sur une machine contrôlée par l'attaquant. Quelle attaque est en cause, et quelle mesure la rend détectable ?

- A. Une attaque par dégradation forcée du protocole ; HSTS, qui interdit ensuite tout repli en clair
- B. Une usurpation de résolution de noms (DNS spoofing) ; DNSSEC, qui fait signer les réponses — sans chiffrer la requête
- C. Une interception de type MITM sur le réseau ; un mot de passe fort côté SSH suffit à l'écarter
- D. Une attaque par dégradation forcée du chiffrement ; DNSSEC, qui signe les réponses du résolveur

**4.** Que garantit l'en-tête HSTS (Strict-Transport-Security) envoyé par un serveur ?

- A. Que toutes les réponses du serveur sont compressées avant d'être envoyées en HTTPS au navigateur
- B. Que le certificat du domaine sera renouvelé automatiquement chaque année, sans intervention de l'administrateur
- C. Que le navigateur doit refuser le repli en clair pour ce domaine : même si l'utilisateur tape `http://`, le navigateur refuse et chiffre
- D. Que les mots de passe ne transitent jamais en clair par le formulaire de connexion du site

**5.** *Question ouverte (2-3 lignes).* Pour administrer un serveur SSH, pourquoi durcir avec l'authentification par clé plutôt que par mot de passe, et quels gestes de durcissement le chapitre applique-t-il ?

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. B.** Le cadenas dit « cet échange est chiffré et le serveur prouve être le propriétaire du nom de domaine ». TLS garantit confidentialité, intégrité et authentification du serveur — pas l'honnêteté du site, ni la qualité du stockage, ni que le nom tapé est celui voulu.
**Pourquoi :** la nuance change tout quand on évalue un risque : le chiffrement protège le transport, pas la personne qui saisit ses identifiants sur une page mensongère.

**2. C.** STARTTLS négocie le chiffrement en cours de connexion ; un attaquant peut laisser passer la commande, l'annuler, et faire continuer les deux extrémités en clair.
**Pourquoi :** « si le repli en clair est accepté, un attaquant sur le chemin obtient exactement ce qu'il veut » — c'est la famille des dégradations forcées : un chiffrement optionnel est un chiffrement contournable.

**3. B.** Le DNS d'origine répond sans preuve : quiconque répond plus vite que le serveur légitime — ou corrompt un cache — redirige vers sa machine tout en affichant le bon nom.
**Pourquoi :** DNSSEC fait signer les réponses par le détenteur de la zone : le client vérifie et refuse une réponse falsifiée. Ce n'est pas du chiffrement — la requête reste lisible — mais l'usurpation devient détectable.

**4. C.** HSTS dit au navigateur : « pour ce domaine, le HTTPS est obligatoire, et ce pendant un an » — même si l'utilisateur tape `http://`, même si un lien propose le clair.
**Pourquoi :** c'est le principe du durcissement : imposer le chiffrement au lieu de le proposer ; la réponse à chaque faille des protocoles anciens est de ne plus laisser le choix à l'attaquant.

**5.** Attendu : le mot de passe est devinable, réutilisable, interceptable — on le désactive purement ; avec la clé publique, la clé privée ne quitte jamais le poste. Durcissement : clés uniquement (`PasswordAuthentication no`), pas de root direct (`PermitRootLogin no`), comptes nommés (`AllowUsers …`), journalisation des connexions.
**Pourquoi :** il reste alors à protéger la clé et à limiter les comptes autorisés — la surface se réduit à ce qui prouve son identité, plus à ce qui se devine.

</details>

---

[← Chapitre précédent](12-partage-et-tiers.md) · [Sommaire](Readme.md) · [Chapitre suivant →](14-architecture-reseau.md)
