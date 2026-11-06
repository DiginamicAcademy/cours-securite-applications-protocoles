[← Chapitre précédent](11-pipelines-data.md) · [Sommaire](Readme.md) · [Chapitre suivant →](13-protocoles-reseau.md)

# Partage et tiers — quand la donnée sort du système

> Une mutuelle sous-traite l'impression et l'envoi de ses courriers à un
> prestataire. Elle lui transmet chaque mois la liste de ses adhérents :
> noms, adresses postales, numéros de contrat. Que devient cette donnée chez
> le tiers ? Qui la lit, combien de temps la garde-t-il, la supprime-t-il
> vraiment ? Le partage de données sort du système d'information : les
> contrats et l'anonymisation deviennent des sujets de **sécurité**.

**Durée de lecture :** 40 min hors approfondissements facultatifs · **Prérequis :** les chapitres [Données sensibles](09-donnees-sensibles.md) et [RGPD appliqué](10-rgpd-applique.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Encadrer** un transfert de données vers un tiers : contrat, traçabilité,
  minimisation.
- **Choisir** entre anonymisation et pseudonymisation selon l'usage visé.
- **Évaluer** la robustesse d'une anonymisation face à un croisement de
  données.
- **Relier** éco-conception et réduction du risque de fuite.

---

## I. Transferts

Dès qu'une donnée quitte le système — vers un prestataire, un partenaire, une
filiale — le contrôle direct disparaît. Ce qui reste, c'est ce qui a été
**écrit avant** : le contrat, le périmètre, la trace.

| Geste | Ce qu'il fixe | Ce qu'il évite |
| --- | --- | --- |
| **Contractualiser** | ce que le tiers a le droit de faire des données, et l'obligation de les effacer | un usage secondaire « pratique » jamais discuté |
| **Limiter le périmètre** | les seules données nécessaires au service | l'envoi de la table complète « pour être tranquille » |
| **Tracer les envois** | quoi, quand, à qui, combien de lignes | l'impossibilité de répondre « qu'a fui exactement ? » le jour d'un incident |
| **Encadrer la fin** | la suppression effective au terme du contrat | la copie qui survit cinq ans chez le prestataire |

En langage du RGPD, le prestataire est un **sous-traitant** : il traite les
données pour le compte du responsable de traitement, sur ses instructions
documentées. La même discipline s'applique entre deux responsables de
traitement distincts — chacun reste responsable de ce qu'il détient.

> [!WARNING]
> « Le prestataire est sérieux » n'est pas une mesure de sécurité. Ce qui
> protège, c'est le contrat, le périmètre minimal et la preuve de suppression —
> vérifiés, pas supposés.

---

## II. Anonymisation

Quand le tiers n'a pas besoin de **qui**, on peut retirer l'identité. Deux
familles de techniques, deux promesses très différentes :

| Technique | Promesse | Exemple | Réversible ? |
| --- | --- | --- | --- |
| **Pseudonymisation** | l'identité est remplacée par un identifiant stable, comme ADH (le code interne de l'adhérent) | `ADH-00482` au lieu du nom dans l'export | oui, avec la table de correspondance |
| **Anonymisation** | la ré-identification n'est plus raisonnablement possible | statistiques agrégées par département | non — définitivement |

L'anonymisation tient ou tombe selon une question simple : **peut-on recroiser
ce jeu avec une autre source pour re-trouver une personne ?** Le cas classique
est le croisement de quasi-identifiants — des champs qui ne sont pas des
identifiants pris isolément, mais qui le deviennent ensemble.

**L'anonymat se mesure à la ré-identification possible, pas aux colonnes supprimées.**

> [!DANGER]
> Un jeu pseudonymisé transmis à un tiers reste une donnée personnelle : si le
> tiers détient — ou peut obtenir — la table de correspondance, l'identité
> revient. Traitez-le avec les mêmes contrôles qu'une donnée nominative.

---

## III. Éco-conception

L'éco-conception réduit l'impact environnemental d'un service numérique :
moins de stockage, moins de transferts, moins de calcul. Elle rejoint la
sécurité des données par un bout très concret : **moins de données, moins de
risque**.

| Geste d'éco-conception | Effet environnemental | Effet sécurité |
| --- | --- | --- |
| **Ne collecter que l'utile** | moins de stockage | moins de données à protéger |
| **Purger ce qui ne sert plus** | moins de volumétrie | moins de données à ficher en cas d'incident |
| **Agréger avant de partager** | moins de transferts | moins de données détaillées hors du système |
| **Alléger les exports** | moins de bande passante | une copie légère fuit moins qu'une copie complète |

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **Les transferts hors Union européenne** — quand un prestataire stocke les
  données en dehors de l'UE, le transfert doit être encadré : clauses
  contractuelles types de la Commission européenne, décisions d'adéquation, ou
  mesures supplémentaires. La question se pose dès qu'un outil SaaS a des
  serveurs — ou des équipes de support — hors UE.
- **Les techniques d'anonymisation avancées** — k-anonymat (chaque combinaison
  de quasi-identifiants couvre au moins k personnes), l-diversité, le bruit
  statistique (différentiel). Elles rendent l'anonymisation mesurable — au prix
  d'une perte de précision à assumer explicitement.
- **La DPIA (Data Protection Impact Assessment)** — l'évaluation d'impact,
  obligatoire pour les traitements à risque
  élevé (données sensibles à grande échelle, surveillance), elle force à
  décrire les risques **avant** de déployer.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> Le récit ci-dessous montre ce que ces deux questions visent ; le défi à faire, lui, est l'exercice [Brouillon de registre des traitements](tp/12-defi-registre.md).
>
> 🧪 **Atelier rapide (5 min)**
>
> Un jeu de données « anonymisé » d'adhérents contient : code postal, date de
> naissance, sexe. Sans nom, sans courriel. Répondez aux deux questions :
>
> 1. Dans une commune de 400 habitants, combien de personnes partagent le
> même code postal et la même date de naissance ?
> 2. Que devient ce chiffre si on ajoute le sexe, puis la rue ?

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Une ré-identification célèbre**
>
> Rappel de littérature — instructif, jamais requis.
>
> L'exercice est célèbre dans la littérature : aux États-Unis, des chercheurs ont
> ré-identifié une gouverneure dans un jeu de données de santé publique
> « anonymisé » à partir de son code postal, sa date de naissance et son sexe —
> trois informations que chacun donne sans hésiter. La leçon tient en une phrase :
> **l'anonymat se mesure à la ré-identification possible, pas aux colonnes
> supprimées**.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Une donnée non détenue ne fuit pas**
>
> Reprend en une phrase ce que la table ci-dessus détaille, et renvoie au registre du chapitre [RGPD appliqué](10-rgpd-applique.md).
>
> La convergence est rarement enseignée et pourtant évidente : la donnée qu'on ne
> détient pas ne peut ni fuir, ni être réclamée, ni coûter de l'énergie à stocker.
> Le registre des traitements (chapitre [RGPD appliqué](10-rgpd-applique.md)) sert
> ici de tableau de bord : ce qui n'a plus de finalité n'a plus de raison d'être.

---

## Points clés

- Un transfert vers un tiers se **contractualise**, se **limite** et se **trace**
  — et se termine par une preuve de suppression.
- Pseudonymiser masque l'identité de façon réversible ; anonymiser rend la
  ré-identification non raisonnablement possible — deux promesses différentes.
- L'anonymat se mesure à la **ré-identification possible** (croisement de
  quasi-identifiants), pas aux colonnes supprimées.
- Éco-conception et sécurité convergent : **moins de données détenues = moins
  de risque**, et moins de coût.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis cochez. Les réponses sont juste après le séparateur : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Une mutuelle confie l'envoi de ses courriers à un prestataire. Qu'est-ce qui protège réellement les données transmises ?

- A. La réputation du prestataire : « le prestataire est sérieux »
- B. Le contrat, le périmètre minimal et la preuve de suppression — vérifiés, pas supposés
- C. Le chiffrement du fichier au moment de l'envoi, et rien d'autre
- D. Rien ne protège : dès qu'une donnée sort, elle est perdue de vue

- [ ] ✓ je savais

**2.** Dans le langage du RGPD, comment nomme-t-on un prestataire qui traite des données pour le compte du responsable de traitement, sur ses instructions documentées ?

- A. Le responsable de traitement conjoint
- B. Le destinataire occasionnel
- C. Le sous-traitant
- D. Le co-responsable solidaire

- [ ] ✓ je savais

**3.** Un jeu « anonymisé » d'adhérents ne contient plus de nom ni de courriel, mais garde code postal, date de naissance et sexe. À quoi mesure-t-on l'anonymat réel du jeu ?

- A. Au nombre de colonnes supprimées
- B. À l'absence du mot « anonymisé » dans le nom du fichier
- C. À la ré-identification possible : un croisement avec une autre source peut-il retrouver une personne (quasi-identifiants)
- D. À la taille du fichier : un petit fichier est forcément anonyme

- [ ] ✓ je savais

**4.** Comment l'éco-conception et la sécurité des données convergent-elles ?

- A. Elles n'ont aucun rapport : l'une est écologique, l'autre réglementaire
- B. Moins de données détenues, c'est moins de risque : ne collecter que l'utile, purger, agréger avant de partager, alléger les exports
- C. L'éco-conception impose de tout conserver longtemps pour éviter les recalculs
- D. La sécurité impose de tout dupliquer, l'éco-conception de tout supprimer

- [ ] ✓ je savais

**5.** *Question ouverte (2-3 lignes).* Pseudonymiser et anonymiser sont « deux promesses très différentes ». Lesquelles, et dans quel cas un jeu pseudonymisé transmis à un tiers reste-t-il une donnée personnelle ?

- [ ] ✓ je savais

---

### Réponses

**1. B.** Ce qui protège, c'est ce qui a été écrit avant : contractualiser (droits d'usage et obligation d'effacement), limiter le périmètre, tracer les envois, encadrer la fin — la suppression effective au terme du contrat.
**Pourquoi :** « le prestataire est sérieux » n'est pas une mesure de sécurité ; sans trace des envois, impossible de répondre « qu'a fui exactement ? » le jour d'un incident.

**2. C.** Le prestataire est un sous-traitant : il traite les données pour le compte du responsable de traitement, sur ses instructions documentées.
**Pourquoi :** la même discipline s'applique entre deux responsables de traitement distincts — chacun reste responsable de ce qu'il détient.

**3. C.** L'anonymat se mesure à la ré-identification possible, pas aux colonnes supprimées : code postal, date de naissance et sexe sont des quasi-identifiants — sans effet pris isolément, ils deviennent des identifiants ensemble.
**Pourquoi :** la question utile est : peut-on recroiser ce jeu avec une autre source pour retrouver une personne ?

**4. B.** Les deux démarches se rejoignent sur un point concret : moins de données, moins de risque — et moins de coût.
**Pourquoi :** ne collecter que l'utile réduit ce qu'il y a à protéger ; purger réduit ce qu'il y a à ficher en cas d'incident ; agréger avant de partager limite les données détaillées hors du système.

**5.** Attendu : la pseudonymisation remplace l'identité par un identifiant stable (ex. `ADH-00482`) et reste réversible avec la table de correspondance ; l'anonymisation rend la ré-identification non raisonnablement possible, définitivement. Le jeu pseudonymisé transmis à un tiers reste une donnée personnelle si le tiers détient — ou peut obtenir — la table de correspondance.
**Pourquoi :** dans ce cas il faut le traiter avec les mêmes contrôles d'accès qu'une donnée nominative.

---

[← Chapitre précédent](11-pipelines-data.md) · [Sommaire](Readme.md) · [Chapitre suivant →](13-protocoles-reseau.md)
