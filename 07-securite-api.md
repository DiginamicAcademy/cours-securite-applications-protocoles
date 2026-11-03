# Sécurité des API — la porte d'entrée des applications modernes

> L'API d'une grande rétention de véhicules expose `GET /users/{id}` sans aucun
> contrôle : il suffit d'incrémenter l'identifiant pour lister les clients, un
> par un. Pas de faille exotique dans cette histoire — seulement des droits
> absents. La fromagerie **DIGICHEESE** (la fromagerie du fil rouge) ouvre elle
> aussi son API au monde : 200 clients, 8 000 commandes, et une surface qu'il
> faut auditer **avant** la mise en production.

**Durée de lecture :** 70 min · **Prérequis :** les vulnérabilités web étudiées
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

> [!TIP]
> Pour cartographier une API, commencez par ce qu'elle documente elle-même :
> une page `/docs`, un fichier `/openapi.json`, ou le code du routeur. La
> surface déclarée est déjà la moitié du travail d'audit.

> 🧪 **Atelier rapide (8 min)**
>
> Le lab du cours contient l'API sécurisée de la fromagerie (service `secure`,
> `http://localhost:8081`). Listons ses endpoints et notons lesquels exigent un
> jeton :

```bash
# La page d'accueil liste les endpoints de l'API
curl -s http://localhost:8081/

# Endpoint public : la recherche de produits répond sans authentification
curl -s "http://localhost:8081/products/search?q=Comté"

# Endpoint protégé : la requête est refusée, il manque un jeton
curl -s http://localhost:8081/admin/users
```

Notez pour chaque endpoint : que demande-t-il, que renvoie-t-il, et
**exige-t-il un jeton** ? Cette liste en trois colonnes est le premier livrable
d'un audit d'API.

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

Sur le lab, la version vulnérable de la fromagerie expose `GET /admin/users`
**sans vérifier le rôle** de l'appelant : n'importe quel compte connecté lit la
table des utilisateurs. La version corrigée refuse la requête si le rôle n'est
pas `admin`.

### La limitation de ressources

Un appelant qui peut enchaîner les requêtes sans limite épuise l'API, la base de
données, ou les deux. C'est le risque « consommation de ressources sans
restriction » : le script qui envoie 10 000 requêtes par minute n'a pas besoin
d'être malveillant pour faire tomber le service — un simple bug de boucle
suffit. Le chapitre suivant traite ce point en détail.

### L'injection de masse

Quand le corps d'une requête est recopié **tel quel** dans un objet métier,
l'appelant peut écrire des champs qu'on ne lui a jamais montrés : un formulaire
d'inscription qui accepte `role: admin`, une mise à jour de profil qui accepte
`credit: 500`. On appelle cela l'injection de masse (mass assignment) : la
propriété existe dans le modèle, donc elle est écrite — sans jamais avoir été
prévue dans le formulaire.

> [!WARNING]
> Une API qui renvoie « tout ce qu'il y a dans la table » est déjà en échec,
> même sans injection : chaque champ exposé est un champ à protéger, à auditer
> et à ficher. C'est le sujet du bloc *Données sensibles*.

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

> [!NOTE]
> Une version obsolète qui tourne encore est invisible dans les tableaux de
> bord fonctionnels — mais parfaitement visible depuis l'extérieur. Faites
> l'inventaire des versions **avant** de décider lesquelles restent.

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
