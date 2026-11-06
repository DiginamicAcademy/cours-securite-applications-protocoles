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

### Exercice bonus — Brouillon de registre des traitements (durée libre, facultatif)

#### Contexte

Le club de randonnée des Trois Vallées compte **200 adhérents**. Son
secrétariat tient à jour une petite application de gestion qui collecte :

- le nom, le courriel et le téléphone de chaque adhérent ;
- la date de naissance, exigée par le contrat d'assurance de la fédération ;
- le certificat médical, demandé **chaque année** à la rentrée ;
- l'historique des sorties auxquelles l'adhérent a participé.

Ces données servent à quatre choses : gérer les adhésions et les cotisations,
envoyer la **newsletter mensuelle**, transmettre à la fédération les
informations nécessaires à l'assurance, et produire des statistiques d'activité
pour l'assemblée générale.

La fédération propose cette année un hébergement mutualisé de l'application.
Le président du club vous demande, avant de répondre, un **brouillon de registre
des traitements** : « juste pour y voir clair sur ce qu'on garde, pourquoi, et
combien de temps. »

---

#### Le défi

Produisez ce brouillon de registre : **une ligne par traitement**, avec les
colonnes suivantes :

| Colonne | Ce qu'elle doit contenir |
| --- | --- |
| Traitement | le nom du traitement (ce qu'il fait, en quelques mots) |
| Finalité | pourquoi ce traitement existe |
| Base légale | la base du RGPD qui le justifie |
| Données | les données qu'il utilise |
| Destinataires | qui les reçoit, à l'intérieur comme à l'extérieur |
| Durée de conservation | combien de temps, et ce qui arrive ensuite |
| Mesures de sécurité | ce qui protège concrètement ces données |

Le registre reste un **brouillon** : il doit être complet et honnête, pas
parfait. Là où vous ne savez pas, écrivez la question à poser au club plutôt
que de deviner.

---

#### Indices

- Commencez par **lister les traitements** avant de remplir les colonnes : les
  quatre usages décrits dans le contexte ne donnent pas forcément quatre
  traitements — et un traitement peut en cacher un autre.
- Chaque traitement porte **une** finalité. Si vous écrivez « et » dans la
  colonne finalité, vous avez probablement deux traitements à séparer.
- La durée de conservation se justifie par la finalité ou par une obligation
  légale — jamais par « on ne sait pas ».
- Le partage avec la fédération est un **transfert** : il se décrit comme les
  autres (quoi, à qui, combien de temps, quelle preuve).

---

#### ✅ Auto-évaluation

Avant de confronter votre travail à la grille de vérification, vérifiez que :

- [ ] Mon registre contient **une ligne par traitement**, et chaque traitement
  tient en une finalité unique.
- [ ] Chaque ligne porte une **base légale** nommée (consentement, contrat,
  obligation légale, intérêt légitime).
- [ ] Chaque ligne nomme ses **destinataires**, y compris la fédération.
- [ ] Chaque ligne donne une **durée** et ce qui arrive à la donnée ensuite —
  aucune durée n'est « illimitée ».
- [ ] Les questions que je ne peux pas trancher sont **écrites** comme des
  questions, pas comblées par des suppositions.

---

#### Prolongement de l'exercice

*Facultatif.* La fédération propose aussi de mutualiser les certificats médicaux
dans son hébergement. Dites, en quelques lignes, ce que ce transfert change par
rapport aux autres données du registre — et ce que vous demanderiez avant de
l'accepter.

<details>
<summary>Voir la correction</summary>

> Un défi se vérifie par **critères**, pas par une correction pas-à-pas : confrontez chaque colonne de votre registre aux repères ci-dessous.

#### Repérage des traitements

Un brouillon solide distingue au moins les traitements suivants — la découpe
peut varier, à condition que chaque traitement porte **une seule finalité** :

| Traitement | Ce qui le rend distinct |
| --- | --- |
| Gestion des adhésions et des cotisations | il exécute le contrat d'adhésion |
| Envoi de la newsletter mensuelle | il repose sur le consentement, révocable |
| Transmission à la fédération (assurance) | il sort du système : c'est un transfert |
| Statistiques d'activité | il n'a pas besoin de l'identité des adhérents |

**Point de vigilance :** le certificat médical mérite une attention
particulière — c'est une **donnée de santé**, au niveau de sensibilité le plus
élevé. S'il apparaît dans un traitement, ce traitement doit le dire
explicitement, avec des mesures à la hauteur.

---

#### Vérification colonne par colonne

| Colonne | Ce qui est attendu | Ce qui trahit une réponse faible |
| --- | --- | --- |
| **Traitement** | un nom qui décrit une action (« gestion des adhésions ») | un nom vague (« base de données ») |
| **Finalité** | une phrase, sans « et » | plusieurs usages mélangés dans une même ligne |
| **Base légale** | l'une des quatre bases, cohérente avec l'usage | « le consentement » pour une donnée indispensable à l'adhésion |
| **Données** | les données réellement utilisées, pas « toutes celles du formulaire » | une liste qui inclut des données que le traitement n'utilise pas |
| **Destinataires** | le club, la fédération le cas échéant, et personne d'autre sans raison | « l'équipe » ou « nos partenaires » sans précision |
| **Durée** | une durée explicite, justifiée, avec le sort de la donnée ensuite | « illimitée », « tant que possible », ou aucune durée |
| **Mesures** | des gestes concrets (droits d'accès, chiffrement, restriction) | « conforme au RGPD » ou « sécurisé » |

---

#### Erreurs fréquentes

- **Un traitement par donnée** — le registre devient illisible et personne ne
  le tient à jour. On regroupe par finalité, pas par champ.
- **La durée oubliée** — la colonne la plus souvent vide, et la première
  question posée en contrôle. Une donnée sans durée de conservation est une
  donnée qu'on garde pour toujours.
- **Le transfert non décrit** — la fédération reçoit des données : le registre
  doit dire quoi, pourquoi, et ce qui advient de la copie chez elle.
- **Les questions comblées** — un registre honnête contient des trous assumés
  (« durée à confirmer auprès du trésorier »). Un registre rempli de
  suppositions est plus dangereux qu'un registre incomplet.

---

#### Points à retenir

- Un registre se construit **traitement par traitement**, une finalité par
  ligne — c'est ce qui le rend tenable dans la durée.
- La colonne **durée** est la plus révélatrice : elle oblige à décider ce que
  devient chaque donnée.
- Un transfert vers un tiers (la fédération) se décrit comme les autres
  traitements : quoi, à qui, combien de temps, quelle preuve.
- Un brouillon honnête, avec ses questions écrites, vaut mieux qu'un registre
  complet mais faux.

</details>

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
> Le récit ci-dessous montre ce que ces deux questions visent ; le défi à faire, lui, est l'exercice bonus de ce chapitre, plus haut.
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

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Une mutuelle confie l'envoi de ses courriers à un prestataire. Qu'est-ce qui protège réellement les données transmises ?

- A. La réputation du prestataire : « le prestataire est sérieux »
- B. Le contrat, le périmètre minimal et la preuve de suppression — vérifiés, pas supposés
- C. Le chiffrement du fichier au moment de l'envoi, et rien d'autre
- D. Rien ne protège : dès qu'une donnée sort, elle est perdue de vue

**2.** Dans le langage du RGPD, comment nomme-t-on un prestataire qui traite des données pour le compte du responsable de traitement, sur ses instructions documentées ?

- A. Le responsable de traitement conjoint
- B. Le destinataire occasionnel
- C. Le sous-traitant
- D. Le co-responsable solidaire

**3.** Un jeu « anonymisé » d'adhérents ne contient plus de nom ni de courriel, mais garde code postal, date de naissance et sexe. À quoi mesure-t-on l'anonymat réel du jeu ?

- A. Au nombre de colonnes supprimées du fichier avant de le confier au destinataire
- B. À la présence ou non du mot « anonymisé » dans le nom du fichier et dans celui de la table d'origine
- C. À la ré-identification possible : un croisement avec une autre source peut-il retrouver une personne (quasi-identifiants)
- D. À la taille du fichier exporté : un petit fichier ne contient pas assez de matière pour retrouver quelqu'un

**4.** Comment l'éco-conception et la sécurité des données convergent-elles ?

- A. Elles n'ont aucun rapport : l'une est une question d'énergie, l'autre une obligation réglementaire sans recouvrement
- B. Moins de données détenues, c'est moins de risque : ne collecter que l'utile, purger, agréger avant de partager, alléger les exports
- C. L'éco-conception pousse à tout conserver longtemps pour éviter de recalculer, ce qui contredit la minimisation
- D. Elles s'opposent : la sécurité veut des duplications pour la disponibilité, l'éco-conception des suppressions

**5.** *Question ouverte (2-3 lignes).* Pseudonymiser et anonymiser sont « deux promesses très différentes ». Lesquelles, et dans quel cas un jeu pseudonymisé transmis à un tiers reste-t-il une donnée personnelle ?

---

<details>

<summary>Vérifier ses réponses</summary>

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

</details>

---

[← Chapitre précédent](11-pipelines-data.md) · [Sommaire](Readme.md) · [Chapitre suivant →](13-protocoles-reseau.md)
