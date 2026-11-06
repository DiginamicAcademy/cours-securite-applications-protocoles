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
> Le modèle à copier reste dans la section II : cet atelier le fait écrire à la main. L'exercice [Analyser les risques d'un pipeline de données](tp/11-analyser-pipeline.md), lui, demande de **recommander** les tests — sa Partie 3 et son corrigé disent lesquels.
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

[← Chapitre précédent](10-rgpd-applique.md) · [Sommaire](Readme.md) · [Chapitre suivant →](12-partage-et-tiers.md)
