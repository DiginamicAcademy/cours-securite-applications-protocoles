# Corrigé — Auditer l'API d'un service de mobilité

> Corrigé de [l'exercice « Auditer l'API d'un service de mobilité
> »](../07-auditer-api.md). Comparez d'abord votre travail aux **étapes**
> ci-dessous : la méthode compte autant que le résultat.

---

## Partie 1 — Cartographier la surface d'attaque

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

## Partie 2 — Auditer l'autorisation

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

## Partie 3 — Auditer la limitation

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

## Partie 4 — Hiérarchiser les recommandations

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

## Points à retenir

- Cartographier, c'est lister pour chaque endpoint ses **paramètres** et ses
  **données échangées** — la surface d'attaque se lit là.
- Un `id` dans le chemin pose toujours la question : « **cet objet est-il à
  vous ?** » — c'est le cœur du BOLA.
- Le jeton prouve l'identité, pas l'appartenance ; la limitation protège la
  **disponibilité** autant que les données.
- On priorise par dommage : ce qui **fuit** d'abord, ce qui **tombe** ensuite.
