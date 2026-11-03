# Exercice — Auditer l'API d'un service de mobilité

> 🟢 **Débutant** · **Durée :** 25 min · **Lien :** chapitre [Sécurité des
> API](../07-securite-api.md)
> **Objectif :** cartographier la surface d'attaque d'une API et repérer ses
> manques d'autorisation et de limitation avant sa mise en production.

---

## Contexte

La métropole de Montclair déploie un service de vélos en libre-service :
380 stations et 12 000 abonnés. L'application mobile s'appuie sur une API
interne que la ville s'apprête à **ouvrir à des partenaires** (une application
de mobilité, le journal local). Avant cette ouverture, vous êtes missionné pour
auditer l'API.

La documentation interne décrit cinq endpoints — GET (consulter une
ressource) et POST (agir) étant les deux verbes en jeu :

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

## Consignes

### Partie 1 — Cartographier la surface d'attaque

Pour chaque endpoint, notez : les **paramètres** qu'il accepte, les **données**
qu'il échange, et ce qu'un appelant malveillant pourrait y chercher. Classez
ensuite les cinq endpoints du plus exposé au moins exposé, en justifiant votre
premier choix en une phrase.

### Partie 2 — Auditer l'autorisation

Le jeton prouve **qui** appelle. Pour chacun des trois endpoints protégés,
dites ce que l'API doit vérifier **en plus** du jeton pour que l'appelant
n'accède qu'à ce qui lui appartient. Illustrez le risque par un scénario
concret : qui appelle quel endpoint, sur quoi, et ce qu'il obtient à tort.

### Partie 3 — Auditer la limitation

Parmi les cinq endpoints, lesquels doivent être soumis à une limitation de
débit, et à quel rythme ? Pour chacun retenu, précisez **qui compte** (quelle
clé de comptage) et **ce que l'API renvoie** quand le rythme est dépassé.

### Partie 4 — Hiérarchiser les recommandations

Rédigez **trois recommandations** maximum, de la plus urgente à la moins
urgente. Chacune tient en une phrase, suivie de la raison pour laquelle elle
vient à cette place.

---

## ✅ Auto-évaluation

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

## Pour aller plus loin

*Facultatif.* La ville veut aussi ouvrir `GET /comptes/{id}/trajets` (les
trajets détaillés d'un abonné) à un partenaire de recherche sur la mobilité.
Sans écrire une ligne de code, décrivez les trois conditions à remplir pour que
cet endpoint soit ouvert sans exposer les abonnés.
