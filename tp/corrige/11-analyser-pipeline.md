# Corrigé — Analyser les risques d'un pipeline de données

> Corrigé de [l'exercice « Analyser les risques d'un pipeline de données
> »](../11-analyser-pipeline.md). Comparez d'abord votre travail aux
> **étapes** ci-dessous : la méthode compte autant que le résultat.

---

## Partie 1 — Décrire le flux

**Éléments attendus :**

| Étape | Données | Acteurs | Frontière franchie |
| --- | --- | --- | --- |
| Extraction | les ventes du jour des 42 magasins | le job d'orchestration, le compte de service unique | les bases des magasins → le job |
| Dépôt intermédiaire | fichiers CSV (Comma-Separated Values) de ventes, fichiers de réponses du prestataire | le job, le prestataire d'e-mailing | le réseau de l'entreprise → le stockage objet partagé |
| Transformation | les mêmes fichiers, nettoyés et agrégés | le script de transformation | le stockage objet → l'entrepôt |
| Restitution | agrégats de ventes, export quotidien | les tableaux de bord, le prestataire | l'entrepôt → l'extérieur du système |

**Ce qu'il faut retenir :** la carte du flux n'est pas un schéma technique —
c'est la liste de **ce qui franchit quoi**. Chaque ligne de ce tableau est une
frontière à protéger, et deux d'entre elles sortent du système d'information
(le compartiment partagé, l'export quotidien).

---

## Partie 2 — Analyser les risques

**Éléments attendus :**

| Étape | Risque de fuite | Risque d'intégrité |
| --- | --- | --- |
| Extraction | le compte de service administrateur peut lire **toutes** les bases : quiconque le détourne lit bien au-delà des ventes | un export partiel (une base injoignable) produit un fichier incomplet, sans signal |
| Dépôt intermédiaire | le compartiment unique mélange les fichiers de ventes et ceux du prestataire : un accès trop large expose les deux | un fichier écrasé ou déposé deux fois corrompt la chaîne en aval |
| Transformation | le script manipule des données clients pour la fidélité : ses journaux peuvent les recopier | l'incident du fichier malformé le montre : un séparateur différent fait planter le job, et **deux jours de ventes** manquent sans alerte |
| Restitution | l'export quotidien envoie des données clients **hors** du système, vers un tiers | un export incomplet ou dupliqué alimente le prestataire en données fausses |

**Erreurs fréquentes :** ne lister que des risques de fuite (le sujet le plus
visible) et oublier l'intégrité — alors que l'incident réel du contexte est un
incident d'**intégrité** ; ou décrire des risques génériques (« un pirate
pourrait… ») sans les rattacher aux faits : le compte administrateur, le
compartiment partagé, le job qui plante en silence.

---

## Partie 3 — Recommander

**Éléments attendus :**

| Sujet | Mesure attendue |
| --- | --- |
| **Comptes de service** | remplacer le compte administrateur unique par un compte par job, avec les seuls droits nécessaires (lecture des tables de ventes, écriture dans le stockage) |
| **Flux** | activer TLS (Transport Layer Security) entre chaque brique, y compris vers le stockage objet, et sortir les identifiants du script vers un coffre de secrets |
| **Tests de données** | poser avant chargement des tests de fraîcheur, de complétude et de validité — dont un qui vérifie la forme attendue des fichiers — et **bloquer** le chargement en cas d'échec |
| **Cloisonnement** | séparer les compartiments de stockage (celui des exports, celui des réponses du prestataire) et donner à l'entrepôt des vues restreintes plutôt qu'un accès aux tables brutes |
| **Traçabilité** | journaliser chaque envoi au prestataire : quoi, quand, combien de lignes, à qui — et encadrer la suppression du fichier chez le tiers |

**Sur la forme :** une mesure se formule comme une action (« remplacer »,
« activer », « bloquer »), pas comme un principe (« il faudrait être prudent »).
Si la mesure ne dit pas **qui fait quoi**, elle ne sera pas faite.

---

## Partie 4 — Prioriser

**Éléments attendus** (un ordre différent est acceptable s'il est justifié) :

1. **Bloquer le chargement sur échec de test** — c'est le dommage déjà arrivé :
   deux jours de ventes manquants, découverts par hasard. Un pipeline qui
   produit des données fausses corrompt tout ce qui en dépend.
2. **Réduire le compte de service aux droits strictement nécessaires** — le
   compte administrateur est la pire exposition du flux : il transforme une
   faille isolée en accès à toutes les bases.
3. **Cloisonner le compartiment partagé et tracer les envois** — la frontière
   la plus sensible est celle qui sort du système : elle se sépare et se
   journalise avant de s'étendre.

**Sur la hiérarchie :** on range d'abord ce qui **corrompt les données**
(l'intégrité, qui trompe silencieusement), ensuite ce qui **élargit l'accès**
(la fuite), enfin ce qui **facilite l'enquête** (la traçabilité). L'ordre
inverse est fréquent — et il laisse l'incident se répéter pendant qu'on
sécurise ailleurs.

---

## Points à retenir

- La carte d'un pipeline est une liste de **frontières** : données, acteurs,
  franchissements — c'est là que se posent les contrôles.
- Chaque étape porte **deux** risques : la fuite **et** l'intégrité. L'incident
  réel du contexte était un incident d'intégrité.
- Les mesures se formulent en **actions** : un compte par job, TLS partout,
  tests qui bloquent, compartiments séparés, envois tracés.
- On priorise par dommage : ce qui **corrompt** d'abord, ce qui **élargit
  l'accès** ensuite.
