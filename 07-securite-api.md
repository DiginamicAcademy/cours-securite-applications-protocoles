[← Chapitre précédent](06-revue-de-code-securite.md) · [Sommaire](Readme.md) · [Chapitre suivant →](08-auth-et-limitation-api.md)

# Sécurité des API — la porte d'entrée des applications modernes

> L'API d'une grande rétention de véhicules expose `GET /users/{id}` sans aucun
> contrôle : il suffit d'incrémenter l'identifiant pour lister les clients, un
> par un. Pas de faille exotique dans cette histoire — seulement des droits
> absents. La fromagerie **DIGICHEESE** (l'entreprise d'étude du parcours) ouvre elle
> aussi son API au monde : 200 clients, 8 000 commandes, et une surface qu'il
> faut auditer **avant** la mise en production.

**Durée de lecture :** 45 min hors approfondissements facultatifs · **Prérequis :** les vulnérabilités web étudiées
lors des journées précédentes

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Décrire** la surface d'attaque d'une API : endpoints, paramètres, données
  échangées.
- **Identifier** les risques de l'OWASP API Security Top 10 sur un endpoint
  concret.
- **Repérer** une autorisation manquante au niveau objet dans un parcours d'API.
- **Décider** une politique de versioning et de dépréciation pour une API qui
  évolue.

---

## I. La surface d'attaque

Une API (Application Programming Interface) est un **contrat** : elle promet à
qui l'appelle que, si la requête est bien formée, la réponse le sera aussi. Une
API web décrit ce contrat en HTTP (HyperText Transfer Protocol) — le même
protocole que les pages web — et échange le plus souvent du JSON (JavaScript
Object Notation). L'architecture la plus répandue s'appelle REST (Representational
State Transfer) : des **ressources** (une commande, un client, un produit) qu'on
lit ou qu'on modifie par des verbes HTTP : GET (lire), POST (créer), PUT
(remplacer), DELETE (supprimer).

La surface d'attaque, c'est **tout ce que l'API accepte du monde extérieur** :

| Entrée | Exemple sur l'API de la fromagerie | Ce qu'un attaquant y cherche |
| --- | --- | --- |
| **Le chemin** | `/products/search` | un endpoint oublié, une ressource qui n'aurait pas dû être publique |
| **Les paramètres** | `?q=Comté` | une valeur qui déborde du cadre prévu |
| **Le corps de la requête** | `username`, `password` à la connexion | un champ de trop, accepté sans être vérifié |
| **Les en-têtes** | `Authorization: Bearer …` | un jeton (token) volé, contourné ou deviné |
| **Les données renvoyées** | la liste des produits | un champ sensible qui sort sans qu'on le lui demande |

Ce qui rend les API différentes des pages web : une page est faite pour un œil
humain, une API est faite pour être **scriptée**. Un attaquant ne navigue pas, il
programme — et il peut tester des milliers de valeurs pendant que vous lisez
cette phrase.

---

## II. OWASP API Top 10

L'OWASP (Open Web Application Security Project) publie, à côté de son Top 10 des
vulnérabilités web, un **API Security Top 10** : le classement des risques
propres aux API. Trois d'entre eux reviennent sans cesse dans les audits.

### L'autorisation au niveau objet — BOLA

BOLA (Broken Object Level Authorization) est le risque n°1 des API : l'appelant
est authentifié, mais il accède à **l'objet d'un autre**. Le cas de la rétention
de véhicules en est l'image exacte — `GET /users/4251` répond, donc
`GET /users/4252` répondra aussi. L'API vérifie que vous êtes connecté, pas que
le client 4252 est le vôtre.

### La limitation de ressources

Le second risque est la **consommation de ressources sans restriction** : un appelant au
débit non limité épuise l'API et la base de données derrière. Le chapitre suivant y est
consacré.

### L'injection de masse

Quand le corps d'une requête est recopié **tel quel** dans un objet métier,
l'appelant peut écrire des champs qu'on ne lui a jamais montrés : un formulaire
d'inscription qui accepte `role: admin`, une mise à jour de profil qui accepte
`credit: 500`. On appelle cela l'injection de masse (mass assignment) : la
propriété existe dans le modèle, donc elle est écrite — sans jamais avoir été
prévue dans le formulaire.

---

## III. Versioning et dépréciation

Une API vivante change : un champ apparaît, un format évolue, un endpoint se
révèle mal conçu. Le réflexe consiste à **ajouter** une version (`/v1/…`,
`/v2/…`) et à laisser l'ancienne tourner « pour ne pas casser les clients ».
L'API Security Top 10 range ce risque dans la mauvaise gestion de l'inventaire :
une vieille version garde **vieilles les failles** qu'elle contenait.

| Geste | Ce qu'il apporte |
| --- | --- |
| **Versionner dans le chemin** (`/v1/`, `/v2/`) | deux contrats coexistent, lisibles et séparés |
| **Annoncer une fin de vie** (en-tête `Sunset`, date de dépréciation) | les consommateurs savent quand migrer |
| **Mesurer l'usage de chaque version** | on sait qui utilise encore l'ancienne |
| **Couper l'ancienne version** | la surface d'attaque diminue d'autant |

La dépréciation n'est pas une question de confort : chaque version maintenue est
une surface d'attaque maintenue. Garder `/v1` trois ans « au cas où », c'est
garder trois ans les erreurs de `/v1`.

---

### Exercice 1 — Auditer l'API d'un service de mobilité (25 min)

#### Contexte

La métropole de Montclair déploie un service de vélos en libre-service :
380 stations et 12 000 abonnés. L'application mobile s'appuie sur une API
interne que la ville s'apprête à **ouvrir à des partenaires** (une application
de mobilité, le journal local). Avant cette ouverture, vous êtes missionné pour
auditer l'API.

La documentation interne décrit cinq endpoints (les deux verbes sont vus au
chapitre) :

| Endpoint | Ce qu'il renvoie ou fait | Jeton requis |
| --- | --- | --- |
| `GET /stations` | la liste des stations et des places disponibles | non |
| `GET /comptes/{id}` | la fiche abonné : nom, courriel, téléphone, historique de trajets, moyen de paiement | oui |
| `GET /factures/{id}` | la facture détaillée d'un abonné | oui |
| `POST /locations` | démarre une location pour l'appelant | oui |
| `POST /connexion` | vérifie les identifiants et renvoie un jeton | non |

Le développeur qui vous reçoit résume la situation : « Tous les endpoints
sensibles demandent un jeton, donc ils sont protégés. »

---

#### Consignes

##### Partie 1 — Cartographier la surface d'attaque

Pour chaque endpoint, notez les **paramètres** qu'il accepte, les **données**
qu'il échange et ce qu'un attaquant pourrait y chercher. Classez les cinq du
plus exposé au moins exposé ; une phrase pour justifier le premier.

##### Partie 2 — Auditer l'autorisation

Le jeton prouve **qui** appelle. Pour chacun des trois endpoints protégés,
dites ce que l'API doit vérifier **en plus** du jeton pour que l'appelant
n'accède qu'à ce qui lui appartient. Illustrez le risque par un scénario
concret : qui appelle quel endpoint, sur quoi, et ce qu'il obtient à tort.

##### Partie 3 — Auditer la limitation

Parmi les cinq endpoints, lesquels doivent être soumis à une limitation de
débit, et à quel rythme ? Pour chacun retenu, précisez **qui compte** (quelle
clé de comptage) et **ce que l'API renvoie** quand le rythme est dépassé.

##### Partie 4 — Hiérarchiser les recommandations

Rédigez **trois recommandations** maximum, de la plus urgente à la moins
urgente. Chacune tient en une phrase, suivie de la raison pour laquelle elle
vient à cette place.

---

#### ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] J'ai listé, pour chaque endpoint, ses **paramètres** et ses **données
  échangées** — pas seulement son rôle.
- [ ] J'ai distingué ce que **prouve le jeton** de ce que l'API doit **vérifier
  en plus** (l'appartenance de l'objet).
- [ ] Mon scénario de risque nomme **qui** appelle, **quel endpoint**, et **ce
  qu'il obtient à tort**.
- [ ] Pour chaque endpoint limité, j'ai donné un **rythme**, une **clé de
  comptage** et un **comportement de refus**.
- [ ] Mes trois recommandations sont **hiérarchisées** et chacune est
  **justifiée**.

---

#### Prolongement de l'exercice

*Facultatif.* La ville veut aussi ouvrir `GET /comptes/{id}/trajets` (les
trajets détaillés d'un abonné) à un partenaire de recherche sur la mobilité.
Sans écrire une ligne de code, décrivez les trois conditions à remplir pour que
cet endpoint soit ouvert sans exposer les abonnés.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Cartographier la surface d'attaque

**Éléments attendus :**

Les verbes en jeu : GET (consulter une ressource) et POST (agir).

| Endpoint | Paramètres | Données échangées | Ce qu'on y cherche |
| --- | --- | --- | --- |
| `GET /stations` | aucun (ou un filtre de zone) | positions et disponibilités | un épuisement par appels répétés, une donnée de géolocalisation plus précise que prévu |
| `GET /comptes/{id}` | `id` dans le chemin | identité, contacts, trajets, moyen de paiement | l'identifiant d'**un autre abonné** |
| `GET /factures/{id}` | `id` dans le chemin | facture détaillée | la facture d'un autre abonné |
| `POST /locations` | corps : identifiant de station, identifiant de vélo | confirmation de location | une location déclenchée pour quelqu'un d'autre |
| `POST /connexion` | corps : identifiants | jeton | les identifiants, par essais répétés |

**Classement attendu :** les endpoints qui portent un `id` dans le chemin
(`/comptes/{id}`, `/factures/{id}`) sont les plus exposés, parce que la donnée
demandée **n'appartient pas nécessairement à l'appelant**. `POST /connexion`
vient ensuite : il ne renvoie pas de données, mais il est la porte d'entrée de
tout le reste.

**Ce qu'il faut retenir :** la surface d'attaque ne se lit pas dans la liste
des endpoints, mais dans **ce que chaque endpoint accepte** — et un `id` dans
le chemin est toujours une question à poser : « cet objet est-il à vous ? »

---

#### Partie 2 — Auditer l'autorisation

**Éléments attendus :**

| Endpoint | Ce que prouve le jeton | Ce qu'il faut vérifier en plus |
| --- | --- | --- |
| `GET /comptes/{id}` | l'identité de l'appelant | que le compte `{id}` **est** celui de l'appelant (ou que l'appelant a un rôle d'administration) |
| `GET /factures/{id}` | l'identité de l'appelant | que la facture `{id}` appartient au compte de l'appelant |
| `POST /locations` | l'identité de l'appelant | que la location est bien créée **au nom de** l'appelant, et pas pour un autre compte |

**Scénario attendu — BOLA (Broken Object Level Authorization) :** un abonné se connecte et reçoit un jeton valide.
Il appelle `GET /factures/{id}` en remplaçant `{id}` par l'identifiant de la
facture d'un autre abonné — et l'API la renvoie, parce qu'elle vérifie que le
jeton est valide mais pas que la facture appartient à son porteur. Le même scénario vaut sur `GET /comptes/{id}` : il
suffit d'incrémenter l'identifiant pour parcourir les 12 000 abonnés de la
métropole.

**Sur l'autorisation :** le jeton répond à « qui ? », jamais à « quoi ? ». Un
endpoint protégé par authentification **sans** contrôle d'appartenance est
exactement le cas de la rétention de véhicules du chapitre : ouvert à tous les
connectés.

---

#### Partie 3 — Auditer la limitation

**Éléments attendus :**

| Endpoint | Clé de comptage | Rythme raisonnable | Comportement au dépassement |
| --- | --- | --- | --- |
| `POST /connexion` | identifiant tenté **et** adresse IP | quelques tentatives par minute | refus `429` avec un délai d'attente annoncé (`Retry-After`) |
| `GET /stations` | clé du partenaire appelant | large, mais borné | refus `429` |
| `GET /comptes/{id}`, `GET /factures/{id}` | compte de l'appelant | modéré | refus `429` |
| `POST /locations` | compte de l'appelant | serré (une location à la fois) | refus `429` |

**Erreurs fréquentes :** limiter par adresse IP seule — une entreprise ou un
campus partage une adresse, et tout le monde est puni pour les agissements
d'un seul ; ou ne limiter que `/connexion` alors qu'un partenaire qui boucle
sur `/stations` épuise la base tout aussi bien.

**Sur la limitation :** la question n'est pas « faut-il limiter ? » mais « qui
paie quand ça casse ? ». Ici, ce sont les 12 000 abonnés qui attendent devant
une station — donc chaque endpoint public mérite un garde-fou.

---

#### Partie 4 — Hiérarchiser les recommandations

**Éléments attendus** (un ordre différent est acceptable s'il est justifié) :

1. **Ajouter le contrôle d'appartenance sur `/comptes/{id}` et `/factures/{id}`
   avant toute ouverture** — c'est la faille la plus grave : elle expose
   directement les données des abonnés, sans aucune manipulation exotique.
2. **Limiter `/connexion` et les endpoints publics** — une fois les données
   protégées, il reste à protéger la disponibilité : les essais de mots de passe
   et les appels en boucle s'arrêtent là.
3. **Réduire les données renvoyées par `/comptes/{id}`** — le moyen de paiement
   et l'historique complet n'ont rien à faire dans une fiche consultée par une
   application partenaire (c'est le sujet du bloc *Données sensibles*).

**Sur la hiérarchie :** on range d'abord ce qui **fuit**, ensuite ce qui
**tombe**, enfin ce qui **encombre**. Une recommandation urgente qui demande
plus de travail n'est pas pour autant différée.

---

#### Points à retenir

- Cartographier, c'est lister pour chaque endpoint ses **paramètres** et ses
  **données échangées** — la surface d'attaque se lit là.
- Un `id` dans le chemin pose toujours la question : « **cet objet est-il à
  vous ?** » — c'est le cœur du BOLA.
- Le jeton prouve l'identité, pas l'appartenance ; la limitation protège la
  **disponibilité** autant que les données.
- On priorise par dommage : ce qui **fuit** d'abord, ce qui **tombe** ensuite.

</details>

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **OpenAPI comme source de validation** — le standard OpenAPI décrit une API en
  un document (endpoints, paramètres, types, formats). FastAPI en génère un
  automatiquement : `curl -s http://localhost:8081/openapi.json` renvoie le
  contrat complet de l'API du lab. Ce document peut devenir la **source de
  validation** des requêtes : ce qui n'y figure pas est refusé.
- **Lire une surface d'API réelle** — la documentation publique d'un service
  (par exemple `https://tutor.diginamic.fr/docs`) se lit avec une ou deux
  requêtes de lecture, pour voir comment un contrat d'API réel se présente. Une
  API en production n'est **jamais** un terrain de test : ni scan, ni fuzzing,
  ni charge.
- **Les schémas de réponse** — décrire ce que renvoie chaque endpoint (champs,
  types, cardinalité) permet de détecter automatiquement une fuite de champ
  lors d'une revue de code.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Cartographier une API par ce qu'elle documente**
>
> Le geste est repris dans l'atelier ci-dessous et, en grand, dans l'exercice 1 de ce chapitre, plus haut.
>
> Pour cartographier une API, commencez par ce qu'elle documente elle-même :
> une page `/docs`, un fichier `/openapi.json`, ou le code du routeur. La
> surface déclarée est déjà la moitié du travail d'audit.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> Atelier d'appropriation : le même travail est conduit de bout en bout dans l'exercice 1 de ce chapitre, plus haut ; il ne suppose pas celui-ci fait.
>
> 🧪 **Atelier rapide (8 min)**
>
> Le lab du cours contient l'API sécurisée de la fromagerie (service `secure`,
> `http://localhost:8081`). Listons ses endpoints et notons lesquels exigent un
> jeton :
>
> ```bash
> # La page d'accueil liste les endpoints de l'API
> curl -s http://localhost:8081/
>
> # Endpoint public : la recherche de produits répond sans authentification
> curl -s "http://localhost:8081/products/search?q=Comté"
>
> # Endpoint protégé : la requête est refusée, il manque un jeton
> curl -s http://localhost:8081/admin/users
> ```
>
> Notez pour chaque endpoint : que demande-t-il, que renvoie-t-il, et
> **exige-t-il un jeton** ? Cette liste en trois colonnes est le premier livrable
> d'un audit d'API.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Le même trou sur le lab du cours**
>
> L'accroche et la définition du BOLA ci-dessus suffisent pour aborder l'exercice.
>
> Sur le lab, la version vulnérable de la fromagerie expose `GET /admin/users`
> **sans vérifier le rôle** de l'appelant : n'importe quel compte connecté lit la
> table des utilisateurs. La version corrigée refuse la requête si le rôle n'est
> pas `admin`.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Consommation de ressources sans restriction**
>
> L'exemple développé est ci-dessous ; le chapitre [Auth et limitation d'API](08-auth-et-limitation-api.md) traite le sujet en profondeur.
>
> Un appelant qui peut enchaîner les requêtes sans limite épuise l'API, la base de
> données, ou les deux. C'est le risque « consommation de ressources sans
> restriction » : le script qui envoie 10 000 requêtes par minute n'a pas besoin
> d'être malveillant pour faire tomber le service — un simple bug de boucle
> suffit. Le chapitre suivant traite ce point en détail.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Renvoyer toute la table est déjà un échec**
>
> Avertissement qui renvoie au bloc suivant de la journée : le chapitre [Données sensibles](09-donnees-sensibles.md) en fait son objet.
>
> Une API qui renvoie « tout ce qu'il y a dans la table » est déjà en échec,
> même sans injection : chaque champ exposé est un champ à protéger, à auditer
> et à ficher. C'est le sujet du bloc *Données sensibles*.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Les versions obsolètes sont invisibles côté métier**
>
> Bon réflexe d'audit, mais rien dans la journée ne dépend de ce développement.
>
> Une version obsolète qui tourne encore est invisible dans les tableaux de
> bord fonctionnels — mais parfaitement visible depuis l'extérieur. Faites
> l'inventaire des versions **avant** de décider lesquelles restent.

---

## Points clés

- La surface d'attaque d'une API, c'est **tout ce qu'elle accepte** : chemins,
  paramètres, corps, en-têtes — et tout ce qu'elle renvoie.
- L'API Security Top 10 d'OWASP en bref : **BOLA** (accès à l'objet d'un autre),
  **limitation de ressources** (débit sans frein), **injection de masse** (champs
  écrits sans être prévus).
- Une API vérifie deux choses distinctes : **qui appelle** (authentification) et
  **ce qu'il a le droit de toucher** (autorisation). Confondre les deux donne
  BOLA.
- Chaque version maintenue est une surface maintenue : **versionner, annoncer,
  mesurer, couper**.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Sur l'API d'une rétention de véhicules, `GET /users/4251` répond à un client connecté — puis `GET /users/4252` aussi. Quel risque de l'OWASP API Security Top 10 est illustré ?

- A. Le BOLA (Broken Object Level Authorization) : l'appelant est authentifié mais accède à l'objet d'un autre
- B. L'injection de masse : le corps de la requête écrit des champs non prévus
- C. La consommation de ressources sans restriction : le débit n'est pas limité
- D. La mauvaise gestion de l'inventaire : une vieille version de l'API tourne encore

**2.** Un formulaire d'inscription ne montre pas de champ `role`, mais l'API accepte `{"role": "admin"}` dans le corps de la requête et l'écrit dans l'objet métier. Comment nomme-t-on ce risque ?

- A. Le BOLA, puisque la requête touche le rôle d'un autre utilisateur que celui qui l'a envoyée
- B. L'injection de masse (mass assignment) : le corps est recopié tel quel, la propriété existe donc elle est écrite
- C. La confusion entre authentification et autorisation : la réponse ne renvoie jamais de 403
- D. Le versioning mal géré : le formulaire de la fiche n'a pas suivi les versions successives de l'API

**3.** L'équipe garde `/v1` en production « pour ne pas casser les clients », en plus de `/v2`. Quel est le problème ?

- A. Aucun : deux versions coexistent sans risque tant que le code est propre et que les tests passent au vert
- B. Un ralentissement : `/v1` et `/v2` partagent la même base et se disputent les mêmes index
- C. Une vieille version garde vieilles les failles qu'elle contenait : chaque version maintenue est une surface d'attaque maintenue
- D. Rien du côté sécurité : seuls les clients sont perdus, sans document OpenAPI pour choisir leur version

**4.** Qu'est-ce qui rend une API différente d'une page web face à un attaquant ?

- A. Une API échange du JSON, un format que seul un client légitime sait lire et exploiter
- B. Une API est faite pour être scriptée : l'attaquant ne navigue pas, il programme, et peut tester des milliers de valeurs
- C. Une API est toujours derrière un pare-feu, contrairement aux pages web exposées au public
- D. Une API n'affiche rien à l'écran, donc rien de ce qu'elle renvoie ne peut être lu par quelqu'un

**5.** *Question ouverte (2-3 lignes).* Qu'est-ce que la surface d'attaque d'une API ? Donnez la définition du chapitre et au moins trois exemples d'entrées à auditer sur l'API de la fromagerie.

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. A.** C'est le risque n°1 des API : l'API vérifie que vous êtes connecté, pas que le client 4252 est le vôtre.
**Pourquoi :** une API vérifie deux choses distinctes — qui appelle (authentification) et ce qu'il a le droit de toucher (autorisation) ; les confondre donne le BOLA.

**2. B.** Quand le corps est recopié tel quel dans un objet métier, l'appelant peut écrire des champs qu'on ne lui a jamais montrés : `role: admin`, `credit: 500`.
**Pourquoi :** la propriété existe dans le modèle, donc elle est écrite — sans jamais avoir été prévue dans le formulaire.

**3. C.** Le réflexe « ajouter une version et garder l'ancienne » range le risque dans la mauvaise gestion de l'inventaire : garder `/v1` trois ans « au cas où », c'est garder trois ans les erreurs de `/v1`.
**Pourquoi :** la démarche est versionner dans le chemin, annoncer une fin de vie, mesurer l'usage de chaque version, puis couper l'ancienne.

**4. B.** Une page est faite pour un œil humain, une API pour être scriptée : un attaquant programme et peut tester des milliers de valeurs pendant qu'on lit cette phrase.
**Pourquoi :** c'est ce qui rend l'audit préalable indispensable — le débit de test d'un script n'a rien à voir avec la navigation d'une personne.

**5.** Attendu : tout ce que l'API accepte du monde extérieur, plus ce qu'elle renvoie — par exemple le chemin (`/products/search`, un endpoint oublié), les paramètres (`?q=Comté`, une valeur qui déborde), le corps de la requête (un champ de trop accepté sans vérification), les en-têtes (un jeton volé ou deviné), et les données renvoyées (un champ sensible qui sort sans qu'on le demande).
**Pourquoi :** chaque entrée est un point où une valeur peut déborder du cadre prévu, et chaque champ renvoyé est un champ à protéger.

</details>

---

[← Chapitre précédent](06-revue-de-code-securite.md) · [Sommaire](Readme.md) · [Chapitre suivant →](08-auth-et-limitation-api.md)
