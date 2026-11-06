[← Chapitre précédent](10-rgpd-applique.md) · [Sommaire](Readme.md) · [Chapitre suivant →](12-partage-et-tiers.md)

# Pipelines de données — sécuriser chaque étape du flux

> Un job d'orchestration alimente chaque nuit l'entrepôt de données d'un
> opérateur de vélos en libre-service. Le script d'extraction tourne avec un
> compte de service qui peut lire **toutes** les bases de l'entreprise. Un
> fichier CSV (Comma-Separated Values) malformé fait planter le job… et les données manquantes partent
> en production sans la moindre alerte. Sécuriser un pipeline, c'est sécuriser
> **chaque étape** : extraction, transformation, chargement — et le compte qui
> les exécute.

**Durée de lecture :** 45 min hors approfondissements facultatifs · **Prérequis :** les notions de base de l'ETL
(Extract, Transform, Load) et du SQL

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Sécuriser** les flux d'un pipeline de données : chiffrement, comptes de
  service, secrets.
- **Écrire** un test de données qui détecte une anomalie avant le chargement.
- **Cloisonner** les accès entre les étapes d'un pipeline et ses stockages.
- **Détecter** un pipeline qui échoue en silence.

---

## I. Sécurité des flux

Un pipeline est une chaîne de systèmes qui se parlent : une base source, un
script d'extraction, un stockage intermédiaire, un moteur de transformation, un
entrepôt. Chaque maillon est une **frontière** — et chaque frontière se protège
comme une API : on authentifie l'appelant, on chiffre le transport, on limite
ce qu'il peut faire.

| Geste | Ce qu'il protège | Mise en œuvre typique |
| --- | --- | --- |
| **Chiffrer les flux** | la donnée en transit entre deux briques | TLS (Transport Layer Security) partout, y compris « à l'intérieur » du réseau |
| **Compte de service dédié** | le périmètre d'un job | un compte par pipeline, avec les seuls droits nécessaires |
| **Gérer les secrets** | les identifiants de connexion | un coffre de secrets, jamais un mot de passe dans le script ni dans le dépôt |
| **Journaliser les exécutions** | la capacité d'enquêter après coup | qui a lu quoi, quand, combien de lignes |

Le compte de service est le point le plus négligé. Un script d'extraction qui
tourne avec un compte administrateur « pour ne pas être bloqué » offre à quiconque
le détourne la totalité du système d'information. Le moindre privilège s'applique
aux pipelines comme au code : un compte par job, un droit par ressource.

> [!DANGER]
> Un mot de passe écrit dans un script d'ETL ne reste pas dans le script : il
> finit dans l'historique Git, dans une sauvegarde, dans un journal d'erreur.
> Les secrets vivent dans un coffre, et le script ne manipule qu'une référence.

---

## II. Qualité et intégrité

Un pipeline qui « marche » n'est pas un pipeline qui a **raison**. Un fichier
malformé, une colonne décalée, des valeurs négatives là où c'est impossible :
la charge passe, l'entrepôt se remplit de données fausses, et les tableaux de
bord mentent avec aplomb. Les tests de données appliquent au flux la même
discipline que les tests unitaires au code.

Le cas le plus simple est un test maison, quelques lignes avant le chargement :

```python
def verifier_trajets(df):
    """Refuse le chargement si les données sortent du cadre attendu."""
    assert df["duree_minutes"].gt(0).all(), "durée de trajet négative ou nulle"
    assert df["station_depart"].notna().all(), "station de départ manquante"
    assert df["date_trajet"].max() <= date.today(), "trajet daté dans le futur"
    return df
```

Trois familles de tests reviennent :

| Famille | Question | Exemple |
| --- | --- | --- |
| **Fraîcheur** | les données sont-elles à jour ? | le dernier chargement date de moins de 24 h |
| **Complétude** | rien ne manque-t-il ? | le nombre de lignes du jour est dans la plage attendue |
| **Validité** | les valeurs sont-elles plausibles ? | durées positives, identifiants non nuls, formats respectés |

Peu importe l'outil : le test doit **bloquer le chargement** au lieu d'alerter dans un
coin — un pipeline fail-closed.

---

## III. Accès et cloisonnement

Dans un pipeline, plusieurs acteurs touchent les données : le job d'extraction,
l'analyste qui explore, l'application qui restitue, le prestataire qui reçoit
un export. Sans cloisonnement, le moindre d'entre eux voit tout.

| Zone | Qui y accède | Règle |
| --- | --- | --- |
| **Stockage intermédiaire** (MinIO, S3 — Simple Storage Service) | les jobs du pipeline | écriture à l'étape qui produit, lecture à l'étape qui consomme, rien d'autre |
| **Entrepôt de données** | les analystes, les applications de restitution | vues restreintes par domaine, pas d'accès direct aux tables brutes |
| **Exports vers l'extérieur** | un destinataire nommé | périmètre minimal, traçabilité de l'envoi, expiration du fichier |

Le cloisonnement se décrit en une phrase par acteur : « **qui** peut faire
**quoi**, sur **quelle** ressource, **combien de temps** ». Si la réponse est
« tout le monde, sur tout, tout le temps », le pipeline n'a pas de cloison — il
a un couloir.

---

### Exercice 1 — Analyser les risques d'un pipeline de données (35 min)

#### Contexte

Une chaîne de librairies compte **42 magasins**. Chaque caisse enregistre les
ventes de la journée ; chaque nuit, un pipeline alimente l'entrepôt de données
qui sert aux tableaux de bord de la direction. Depuis le début de l'année, un
export **quotidien** part vers un prestataire d'e-mailing, qui anime la
newsletter de la fidélité.

Voici le flux, tel qu'il est documenté :

1. **Extraction** — un job d'orchestration (type Airflow) se connecte aux bases
   des 42 magasins et exporte les ventes du jour en fichiers CSV, avec un
   compte de service unique créé « au début du projet », administrateur sur
   toutes les bases.
2. **Dépôt intermédiaire** — les fichiers sont poussés dans un stockage objet
   (type MinIO), dans un compartiment unique où le prestataire d'e-mailing
   dépose aussi ses fichiers de réponses.
3. **Transformation** — un script Python nettoie, déduplique et agrège les
   ventes, puis charge l'entrepôt.
4. **Restitution** — les tableaux de bord lisent l'entrepôt ; l'export
   quotidien vers le prestataire part depuis le même script de transformation.

La semaine dernière, un fichier CSV malformé (un séparateur différent) a fait
planter le job de transformation. **Deux jours de ventes** sont manquants dans
l'entrepôt — personne ne s'en est aperçu avant qu'un responsable de magasin
signale un tableau de bord faux.

---

#### Consignes

##### Partie 1 — Décrire le flux

Reprenez les quatre étapes et, pour chacune, notez : les **données** qui y
circulent, les **acteurs** (comptes, systèmes, personnes) qui y accèdent, et
la **frontière** franchie. Un tableau à
quatre lignes suffit.

##### Partie 2 — Analyser les risques

Pour chaque étape, identifiez **un risque de fuite** et **un risque
d'intégrité**. Appuyez-vous sur les faits du contexte (le compte administrateur,
le compartiment partagé, l'incident du fichier malformé) — pas sur des cas
génériques.

##### Partie 3 — Recommander

Proposez des mesures pour : les **comptes de service**, les **flux** entre les
briques, les **tests de données**, le **cloisonnement** du stockage et de
l'entrepôt, et la **traçabilité** de l'envoi au prestataire. Une mesure par
sujet, formulée comme une action concrète.

##### Partie 4 — Prioriser

Classez vos mesures en **trois actions** à mener en premier, de la plus urgente
à la moins urgente. Chaque action est justifiée par le dommage qu'elle évite.

---

#### ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque étape du flux nomme ses **données**, ses **acteurs** et sa
  **frontière**.
- [ ] Pour chaque étape, j'ai donné **un risque de fuite et un risque
  d'intégrité** — pas un seul des deux.
- [ ] Mes risques s'appuient sur les **faits du contexte**, pas sur des
  généralités.
- [ ] Mes mesures couvrent les **cinq sujets** demandés (comptes, flux, tests,
  cloisonnement, traçabilité).
- [ ] Mes trois actions prioritaires sont **justifiées par un dommage** évité.

---

#### Prolongement de l'exercice

*Facultatif.* Le prestataire d'e-mailing propose de déposer ses fichiers de
réponses dans le même compartiment que les exports, « pour simplifier ».
Sans écrire de code, décrivez ce que ce partage change pour la sécurité du
pipeline, et l'alternative que vous proposeriez.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Décrire le flux

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

#### Partie 2 — Analyser les risques

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

#### Partie 3 — Recommander

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

#### Partie 4 — Prioriser

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

#### Points à retenir

- La carte d'un pipeline est une liste de **frontières** : données, acteurs,
  franchissements — c'est là que se posent les contrôles.
- Chaque étape porte **deux** risques : la fuite **et** l'intégrité. L'incident
  réel du contexte était un incident d'intégrité.
- Les mesures se formulent en **actions** : un compte par job, TLS partout,
  tests qui bloquent, compartiments séparés, envois tracés.
- On priorise par dommage : ce qui **corrompt** d'abord, ce qui **élargit
  l'accès** ensuite.

</details>

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **La sécurité des clusters Spark et Hadoop** — sur un cluster, la question
  devient : qui soumet un job, avec quelles identités, sur quelles données ?
  Kerberos, les ACL (Access Control List) de HDFS (Hadoop Distributed File
  System), l'isolation des espaces YARN (Yet Another Resource Negotiator) : les
  mêmes principes
  (identité, moindre privilège, cloisonnement), à l'échelle d'une grappe.
- **La dérive de schéma (schema drift)** — quand la source change de format sans
  prévenir (une colonne en plus, un séparateur différent). Les outils modernes
  comparent le schéma détecté au schéma attendu et refusent l'écart.
- **L'observabilité des pipelines** — métriques de volume, temps d'exécution,
  taux d'échec par étape. Un pipeline dont personne ne regarde les métriques
  échoue exactement comme celui de l'accroche : en silence.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Des outils pour déclarer les tests**
>
> Great Expectations et ses pairs formalisent ces tests ; le garde-fou, lui, ne dépend d'aucun outil.
>
> Des outils comme Great Expectations formalisent ces tests sous forme de
> « expectations » déclaratives, versionnables et rejouables à chaque exécution.
> L'important n'est pas l'outil : c'est que le test **bloque le chargement** au
> lieu d'alerter dans un coin — un pipeline fail-closed.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Le test arrête le job, il n'avertit pas après**
>
> Reprend, en l'insistant, ce que la phrase ci-dessus vient de poser.
>
> Un test de données qui échoue doit arrêter le job **avant** l'entrepôt. Une
> alerte envoyée après chargement ne protège que la prochaine fois — entre-temps,
> les données fausses sont déjà dans les rapports.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> Le modèle à copier reste dans la section II : cet atelier le fait écrire à la main. L'exercice 1 de ce chapitre, plus haut, lui, demande de **recommander** les tests — sa Partie 3 et son corrigé disent lesquels.
>
> 🧪 **Atelier rapide (10 min)**
>
> Écrivez un test de non-régression pour la table `locations` d'un service de
> vélos en libre-service. Le schéma est le suivant — le test doit vérifier que
> `duree_minutes` reste strictement positive et que `identifiant_velo` n'est
> jamais nul :
>
> ```sql
> CREATE TABLE locations (
>     id INT PRIMARY KEY,
>     identifiant_velo VARCHAR(12),
>     station_depart VARCHAR(64),
>     station_arrivee VARCHAR(64),
>     duree_minutes INT,
>     date_trajet DATE
> );
> ```
>
> En Python avec pandas, ou en SQL avec une simple requête de filtrage, écrivez le
> test, puis **faites-le échouer volontairement** en insérant une ligne invalide :
> un test qui n'a jamais échoué n'a jamais rien prouvé.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Un export qui part est une sortie du système**
>
> Le chapitre [Partage et tiers](12-partage-et-tiers.md), dans la même journée, traite ce cas pour lui-même.
>
> Un export vers un tiers est une **sortie du système d'information** : le
> fichier échappe au contrôle dès qu'il part. Le chapitre
> [Partage et tiers](12-partage-et-tiers.md) traite ce cas pour lui-même.

---

## Points clés

- Chaque maillon d'un pipeline est une frontière : **TLS** pour le transport,
  **compte de service dédié** pour l'identité, **coffre de secrets** pour les
  identifiants.
- Un pipeline fiable se teste : **fraîcheur, complétude, validité** — et le
  test **bloque** le chargement au lieu d'alerter après.
- Le cloisonnement se résume par « qui peut faire quoi, sur quelle ressource,
  combien de temps » — y compris pour les exports vers l'extérieur.
- Un pipeline qui échoue en silence est plus dangereux qu'un pipeline en panne :
  il produit des données fausses **qui ont l'air vraies**.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Le script d'extraction d'un pipeline tourne avec un compte administrateur « pour ne pas être bloqué ». Quel est le risque principal ?

- A. Aucun : un compte administrateur évite les incidents de production
- B. Le job tourne plus lentement à cause des droits
- C. Quiconque détourne le script dispose de la totalité du système d'information
- D. La base source refuse les connexions administrateur la nuit

**2.** Quelles sont les trois familles de tests de données du chapitre ?

- A. Unitaires, intégration, bout en bout
- B. Fraîcheur, complétude, validité
- C. Charge, latence, disponibilité
- D. Volume, coût, volumétrie

**3.** Un test de données détecte des durées négatives, mais seulement en envoyant une alerte après le chargement. Que vaut cette protection ?

- A. Elle est suffisante : l'équipe est prévenue le jour même et peut corriger avant la prochaine réunion
- B. Elle ne protège que la fois suivante : entre-temps les données fausses sont dans les rapports — le test doit bloquer avant l'entrepôt
- C. Elle est équivalente au blocage, avec en moins les faux positifs qui arrêtent un job pour rien
- D. Elle est supérieure : bloquer un job de nuit coûte plus cher à l'équipe que laisser passer et prévenir

**4.** Dans le cloisonnement d'un pipeline, quelle règle s'applique au stockage intermédiaire (MinIO, S3) ?

- A. Lecture en écriture pour tous les services, afin de simplifier les échanges
- B. Écriture à l'étape qui produit, lecture à l'étape qui consomme, rien d'autre
- C. Accès libre en lecture pour les analystes, l'entrepôt étant déjà protégé
- D. Suppression immédiate après lecture, sans exception

**5.** *Question ouverte (2-3 lignes).* « Un pipeline qui échoue en silence est plus dangereux qu'un pipeline en panne. » Expliquez, en vous appuyant sur l'accroche du chapitre (le fichier CSV malformé).

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. C.** Le compte de service est le point le plus négligé : un compte administrateur offre à quiconque détourne le script la totalité du système d'information.
**Pourquoi :** le moindre privilège s'applique aux pipelines comme au code — un compte par job, un droit par ressource.

**2. B.** Fraîcheur (le dernier chargement date de moins de 24 h), complétude (le nombre de lignes du jour est dans la plage attendue), validité (durées positives, identifiants non nuls, formats respectés).
**Pourquoi :** un pipeline qui « marche » n'est pas un pipeline qui a raison ; les tests appliquent au flux la discipline des tests unitaires au code.

**3. B.** Une alerte envoyée après chargement ne protège que la prochaine fois : entre-temps, les données fausses sont déjà dans les rapports.
**Pourquoi :** le test doit bloquer le chargement au lieu d'alerter dans un coin — c'est le pipeline fail-closed, peu importe l'outil.

**4. B.** Écriture à l'étape qui produit, lecture à l'étape qui consomme, rien d'autre ; l'entrepôt, lui, s'ouvre par vues restreintes par domaine, pas par accès direct aux tables brutes.
**Pourquoi :** le cloisonnement se décrit en une phrase par acteur — « qui peut faire quoi, sur quelle ressource, combien de temps » ; sinon le pipeline n'a pas de cloison, il a un couloir.

**5.** Attendu : un pipeline en panne se voit et stoppe la chaîne ; un pipeline qui échoue en silence livre des données manquantes ou fausses qui ont l'air vraies — dans l'accroche, un CSV malformé fait planter le job et les données manquantes partent en production sans alerte, donc les tableaux de bord mentent.
**Pourquoi :** le danger n'est pas l'absence de données mais la fausse donnée crue : personne ne soupçonne les rapports, et l'erreur se décide avec eux.

</details>

---

[← Chapitre précédent](10-rgpd-applique.md) · [Sommaire](Readme.md) · [Chapitre suivant →](12-partage-et-tiers.md)
