[← Chapitre précédent](17-reponse-incident.md) · [Sommaire](Readme.md) · [Chapitre suivant →](A-Glossaire-et-ressources.md)

# Maturité et perspectives — la sécurité est une trajectoire

> « Sommes-nous en sécurité ? » est une question à laquelle personne ne peut
> répondre honnêtement, et les équipes qui la posent finissent par recevoir une
> réponse rassurante et fausse. La question utile est ailleurs : « où en
> sommes-nous, et quelle est la prochaine étape ? ». La sécurité n'est pas un état
> qu'on atteint, c'est une trajectoire qu'on suit — et la pente s'accélère : les
> deux camps emploient désormais l'IA (intelligence artificielle), l'un pour
> trouver plus vite, l'autre pour corriger plus vite. Ce dernier chapitre ferme le
> parcours en vous donnant de quoi continuer sans lui.

**Durée de lecture :** 45 min hors approfondissements facultatifs · **Prérequis :** les journées précédentes du parcours

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Situer** une organisation sur une grille de maturité simple, domaine par
  domaine.
- **Construire** une feuille de route de sécurité priorisée par le risque réel.
- **Organiser** une veille continue sur les failles et les correctifs, avec un
  délai de réaction.
- **Évaluer** ce que l'IA change, pour l'attaquant comme pour le défenseur.

---

## I. Évaluer sa maturité

### Une grille tient en une page

L'auto-évaluation sert à décider, pas à se noter. Une grille simple, remplie
honnêtement, vaut mieux qu'un référentiel de cinquante pages qu'on ne lira jamais.
Cinq domaines suffisent — ce sont précisément ceux du parcours :

| Domaine | La question à se poser | Niveau |
| --- | --- | --- |
| **Code** | les failles courantes sont-elles détectées avant la livraison ? | à remplir |
| **Dépendances** | sait-on quelles composants on embarque, et quand une faille les touche ? | à remplir |
| **Accès** | chaque appel, chaque compte, a-t-il exactement les droits nécessaires ? | à remplir |
| **Réseau** | les zones et les flux sont-ils écrits, et tout ce qui n'est pas autorisé est-il refusé ? | à remplir |
| **Réponse à incident** | si ça casse ce soir, sait-on qui décide quoi ? | à remplir |

Pour chaque domaine, on se situe avec une note de **1 à 5** :

| Note | Ce qu'elle veut dire |
| --- | --- |
| **1** | ignoré : personne ne s'en occupe, ou on ne sait pas |
| **2** | conscient : le sujet est identifié, rien n'est fait |
| **3** | planifié : une décision existe, elle n'est pas appliquée partout |
| **4** | appliqué : c'est en place, et ça se vérifie |
| **5** | tenu dans le temps : c'est en place, vérifié, et amélioré par les retours |

> 🧪 **Atelier rapide (10 min)**
>
> Prenez un projet que vous connaissez — votre projet data, votre dépôt, votre
> équipe. Notez les cinq domaines de **1 à 5**, en une phrase de justification
> chacun. Interdiction de mettre la même note partout : si tout est à 3, c'est que
> l'évaluation n'a pas été faite.

---

## II. La feuille de route : prioriser par le risque

### La règle de proportionnalité

La règle de proportionnalité rencontrée dès la première journée du parcours
s'applique intégralement ici : **la protection est proportionnée à la valeur de ce
qu'elle protège**. Une feuille de route qui liste tout ne priorise rien. Trois
questions suffisent à ordonner :

1. **Qu'est-ce qui est le plus précieux** chez nous ? (les données, le service, la
   réputation)
2. **Quel est le chemin le plus court** pour un attaquant vers ce précieux ?
3. **Quel geste coupe ce chemin** le plus sûrement, pour le moins d'effort ?

### Trois horizons

| Horizon | Ce qu'on y met | Exemple |
| --- | --- | --- |
| **Immédiat** | ce qui coupe un chemin d'attaque connu, en quelques jours | fermer une exposition inutile, révoquer une clé commitée |
| **Court terme** | ce qui met une protection en place de façon durable | les contrôles dans la chaîne de livraison, la segmentation |
| **Structurel** | ce qui change les habitudes | la réponse à incident préparée, la veille organisée, la formation |

> ⚠️ **Point d'attention** — la feuille de route la plus dangereuse est celle qui
> ne contient que des chantiers structurels. Sans geste immédiat, rien ne change
> avant longtemps, et l'intérêt retombe. Un chantier visible dans les deux
> premières semaines maintient l'équipe en mouvement.

---

## III. La veille continue

### Le délai de réaction

Ce qui compte n'est pas le nombre d'alertes lues, mais le temps entre la
publication d'une faille et le moment où votre organisation sait **si elle est
concernée**. Ce temps se réduit mécaniquement : inventaire des composants tenu à
jour, alertes automatiques sur les dépendances, et une personne nommée pour
traiter ce qui arrive. Cet inventaire est le SBOM (Software Bill of Materials, la
liste des composants) décrit au chapitre sur la chaîne de livraison.


---

## IV. L'effet de l'IA

La ligne de conduite reste la même que pour tout le parcours : **l'IA propose,
l'humain décide**. Un correctif généré sans revue est un changement de plus dans
un système qui en a déjà beaucoup.

---

### Exercice bonus — Construire sa feuille de route de sécurité (non chronométré, facultatif)

#### Contexte

Ce défi porte sur **votre** projet : le dépôt de données sur lequel vous
travaillez, l'application de votre équipe, ou un projet personnel que vous
maintenez. Les éléments du chapitre — la grille de maturité, les trois horizons de
la feuille de route, la veille — s'appliquent tels quels. Ce qui ne s'applique
pas, vous l'écartez en le justifiant.

Personne ne peut faire cet exercice à votre place : les faits sont chez vous.

---

#### Consignes

##### Partie 1 — S'auto-évaluer

Notez les **5 domaines** du chapitre (code, dépendances, accès, réseau, réponse à
incident) de **1 à 5**, avec une phrase de justification chacun. La note ne compte
que si la justification cite un fait observable — pas une intention.

##### Partie 2 — Identifier les écarts les plus coûteux

Parmi vos cinq notes, retenez **3 écarts** qui coûtent le plus cher à laisser
ouverts. Pour chacun, décrivez le chemin le plus court entre un attaquant et ce
que votre projet a de plus précieux, puis le geste qui coupe ce chemin.

##### Partie 3 — Construire la feuille de route

Organisez vos actions sur **3 mois**, selon les trois horizons du chapitre
(immédiat, court terme, structurel). Chaque action porte un responsable et une
échéance. Une action sans responsable est un vœu, pas une feuille de route.

##### Partie 4 — Définir les preuves de progression

Dites comment vous saurez, dans 3 mois, que les choses ont réellement bougé : la
preuve observable pour chaque horizon (un contrôle qui tourne, un inventaire à
jour, une simulation faite…).

---

#### ✅ Auto-évaluation

Avant de considérer le défi terminé, vérifiez que :

- [ ] Mes **5 notes** sont justifiées par des faits observables, pas par des
  intentions.
- [ ] Mes **3 écarts** décrivent un chemin d'attaque concret et le geste qui le
  coupe.
- [ ] Chaque action de ma feuille de route a **un responsable et une échéance**
  dans les 3 mois.
- [ ] Mes preuves de progression sont **observables** : on peut les montrer à
  quelqu'un, elles ne se décrivent pas.
- [ ] J'ai écarté ce qui ne s'appliquait pas à mon projet, **en le justifiant**.

<details>
<summary>Voir la correction</summary>

> Ce défi porte sur **votre** projet : le corrigé ne peut donc pas donner « la » réponse. Il donne la **forme d'une bonne réponse**, puis un exemple complet sur un projet fictif — le dépôt `analyse-ventes` d'une équipe data (scripts Python, notebooks partagés, un fichier `requirements.txt`, une API de restitution, des sauvegardes hebdomadaires).

#### Partie 1 — S'auto-évaluer

**Ce qui fait une bonne justification :** un fait observable, que quelqu'un d'autre
peut vérifier en regardant. « On fait attention aux dépendances » n'est pas un
fait. « `requirements.txt` ne fige aucune version, et personne ne sait dire quelles
composants sont embarqués » en est un.

**Exemple rempli :**

| Domaine | Note | Justification (fait observable) |
| --- | --- | --- |
| Code | 2 | les scripts sont relus entre pairs, mais aucun contrôle automatique ne tourne à la livraison |
| Dépendances | 1 | `requirements.txt` ne fige aucune version, et aucun inventaire des composants n'existe |
| Accès | 3 | les comptes sont nominatifs, mais un compte de service partagé subsiste pour l'extraction |
| Réseau | 2 | l'API de restitution est exposée, et la base est joignable depuis tout le réseau interne |
| Réponse à incident | 1 | aucun document écrit, personne n'est nommée pour décider |

**Erreurs fréquentes :** mettre la même note partout (l'évaluation n'a pas été
faite), ou justifier par une intention (« on prévoit de… ») au lieu d'un fait.

---

#### Partie 2 — Identifier les écarts les plus coûteux

**Ce qui fait un bon écart :** un chemin d'attaque décrit en une phrase, et un
geste qui le **coupe** — pas une liste de bonnes intentions.

**Exemple, sur les trois écarts retenus :**

| Écart | Le chemin le plus court | Le geste qui le coupe |
| --- | --- | --- |
| Dépendances (note 1) | une faille publiée sur un composant de `requirements.txt` est exploitable sans que personne ne le sache | figer les versions, produire le SBOM (Software Bill of Materials, l'inventaire
  des composants) à chaque livraison, et recevoir l'alerte quand une version est
  affectée |
| Réseau (note 2) | un poste interne compromis donne accès direct à la base de données | n'autoriser que l'API de restitution à joindre la base, et refuser le reste |
| Réponse à incident (note 1) | le jour où ça casse, personne ne sait qui décide quoi, et les gestes de première urgence détruisent les traces | écrire le mini-plan de réponse, nommer les rôles, le tester par une simulation |

**Erreurs fréquentes :** retenir les écarts « les plus simples à corriger » plutôt
que les plus coûteux, ou décrire un remède général (« sensibiliser l'équipe ») qui
ne coupe aucun chemin.

---

#### Partie 3 — Construire la feuille de route

**Exemple sur 3 mois :**

| Horizon | Action | Responsable | Échéance |
| --- | --- | --- | --- |
| **Immédiat** | fermer l'accès direct à la base depuis le réseau interne | l'administratrice de la base | la première semaine |
| **Immédiat** | révoquer le compte de service partagé, créer un compte nominatif par usage | le responsable de l'équipe data | la première semaine |
| **Court terme** | figer les versions de `requirements.txt` et produire l'inventaire des composants à chaque livraison | la personne qui maintient la chaîne de livraison | le premier mois |
| **Court terme** | ajouter les contrôles automatisés du chapitre sur la chaîne de livraison | la même personne | le deuxième mois |
| **Structurel** | écrire le mini-plan de réponse à incident et nommer les rôles | le responsable de l'équipe data | le deuxième mois |
| **Structurel** | faire une simulation de crise, puis mettre le plan à jour | toute l'équipe | le troisième mois |

**Ce qui fait une bonne feuille de route :** au moins une action visible dans les
premières semaines (sinon l'élan retombe), un responsable et une échéance pour
chaque ligne, et un mélange des trois horizons.

---

#### Partie 4 — Définir les preuves de progression

**Ce qui fait une bonne preuve :** quelque chose qu'on **montre**, pas quelque
chose qu'on décrit.

**Exemple :**

| Horizon | Preuve observable |
| --- | --- |
| **Immédiat** | une tentative de connexion à la base depuis un poste quelconque échoue, et le refus apparaît dans les journaux |
| **Court terme** | l'inventaire des composants de la dernière livraison existe, daté, et une alerte est bien remontée sur une dépendance volontairement laissée ancienne pour le test |
| **Structurel** | le compte rendu de la simulation de crise existe, avec les changements décidés et leur mise en œuvre |

**Erreurs fréquentes :** une preuve qui consiste à dire « c'est fait », ou une
preuve qui demande une enquête pour être constatée. Si la preuve ne se voit pas en
quelques minutes, elle ne servira pas à la revue de trois mois.

---

#### Points à retenir

- Une note ne vaut que par **le fait observable** qui la justifie.
- Un écart se décrit comme **un chemin d'attaque et le geste qui le coupe**.
- La feuille de route tient en trois horizons, avec **un responsable et une
  échéance** pour chaque action.
- La progression se prouve par **ce qu'on montre**, pas par ce qu'on affirme.

</details>

---

## V. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour terminer
la journée.*

- **Les référentiels de maturité** — des cadres publics décrivent des niveaux de
  maturité par domaine, comme la norme ISO 27001 publiée par l'ISO (Organisation
  internationale de normalisation) pour le système de management de la sécurité.
  Ils servent de
  vocabulaire commun avec la direction, pas de certification obligatoire.
- **Les communautés et les conférences** — suivre les retours d'expérience
  d'autres équipes est le moyen le moins cher d'éviter les erreurs déjà payées par
  d'autres.
- **Les CTF défensifs** — un CTF (Capture The Flag, une compétition de sécurité)
  n'est pas réservé à l'attaque : il existe des formats défensifs, où l'on doit
  retrouver et corriger une faille dans un temps donné.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
>
> **Ce que la note ne dit pas**
>
>
> Une note est un signal, pas un verdict. Deux précautions : une note haute obtenue
> « parce qu'on a un outil » ne vaut rien si personne ne regarde ce qu'il produit,
> et une note basse n'est pas une faute — c'est une **décision à prendre**. Le but
> de la grille est de faire apparaître les écarts qui coûtent cher, pas de classer
> les équipes.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
>
> **Ce qu'il faut suivre**
>
>
> La veille n'est pas une lecture du dimanche : c'est un processus, avec des
> sources, un rythme et un **délai de réaction**.
>
> | Source | Ce qu'elle apporte |
> | --- | --- |
> | **GHSA** (GitHub Security Advisory, l'alerte de sécurité publiée sur GitHub) | les alertes sur les composants que vous utilisez réellement |
> | **NVD** (National Vulnerability Database, la base publique de vulnérabilités) | la référence des failles publiées, leur gravité, leurs correctifs |
> | **Les listes des éditeurs** | les annonces de versions corrigées, pour vos outils et vos langages |
> | **Les CERT** (Computer Emergency Response Team, les équipes de réponse à incident) | les alertes et recommandations par secteur et par pays |

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> 💡 **Astuce** — automatisez la collecte, jamais la décision. Une alerte
> automatique qui crée une tâche assignée est utile ; un correctif appliqué sans
> regarder ce qu'il change ne l'est pas toujours.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
>
> **Ce que ça change pour l'attaquant**
>
>
> L'IA accélère ce qui était lent : la reconnaissance d'une cible, la rédaction de
> messages de phishing crédibles et personnalisés, la génération de PoC (proof of
> concept, la preuve de concept qu'une faille est exploitable) à partir d'une
> description publique. Un LLM (large language model, un modèle de langage de grande
> taille) ne découvre pas de faille inédite par magie : il **réduit le délai** entre
> la publication d'une faille et sa tentative d'exploitation à grande échelle.
>
>
> **Ce que ça change pour le défenseur**
>
>
> Exactement le même levier, de l'autre côté :
>
> | Usage défensif | Ce qu'il apporte |
> | --- |---|
> | **Aide à la revue de code** | repérer les schémas dangereux dans de gros volumes de code |
> | **Priorisation des alertes** | trier ce qui arrive des contrôles automatisés, expliquer pourquoi |
> | **Rédaction de correctifs et de tests** | produire le premier jet, que l'humain vérifie |
> | **Compréhension d'un incident** | résumer des journaux, reconstituer une chronologie |

---

## Points clés

- La bonne question n'est pas « sommes-nous en sécurité ? » mais « où en
  sommes-nous, et quelle est la prochaine étape ? ».
- La **grille de maturité** tient en une page : cinq domaines, une note de 1 à 5,
  une justification honnête.
- La **feuille de route** priorise par le risque : un geste immédiat, des
  protections durables, des changements structurels.
- La **veille** se mesure à un délai de réaction, pas au nombre d'alertes lues ;
  elle repose sur l'inventaire des composants et une personne nommée.
- L'**IA** accélère les deux côtés de la défense : elle propose, l'humain décide.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Dans la grille de maturité du chapitre, que signifie une note de 4 dans un domaine ?

- A. Ignoré : personne ne s'en occupe, ou on ne sait pas
- B. Planifié : une décision existe, elle n'est pas appliquée partout
- C. Appliqué : c'est en place, et ça se vérifie
- D. Tenu dans le temps : amélioré par les retours

**2.** Quelle question le chapitre substitue-t-il à « Sommes-nous en sécurité ? » ?

- A. « Quel budget de sécurité demander cette année ? »
- B. « Où en sommes-nous, et quelle est la prochaine étape ? »
- C. « Quel outil de sécurité acheter en premier ? »
- D. « Quelle certification visons-nous ? »

**3.** Sur quoi se décide la priorité d'un geste dans la feuille de route ?

- A. Sur la taille de l'équipe et le budget disponible, qui fixent ce qu'il est raisonnable de tenter
- B. Sur la proportionnalité : protéger selon la valeur de ce qui est protégé — le plus précieux, le chemin le plus court vers lui, le geste qui le coupe
- C. Sur l'ordre d'arrivée des alertes dans la messagerie de l'équipe, la plus récente passant devant les autres
- D. Sur ce que font les concurrents du même secteur, dont on copie les choix une fois qu'ils sont validés

**4.** À quoi mesure-t-on une veille continue efficace ?

- A. Au nombre d'alertes et de newsletters lues chaque semaine par les membres les plus actifs de l'équipe
- B. Au temps entre la publication d'une faille et le moment où l'on sait si l'organisation est concernée — inventaire à jour, alertes, une personne nommée
- C. À la rapidité avec laquelle les alertes reçues sont lues, qualifiées puis archivées par l'équipe
- D. Au nombre de sources suivies et de flux auxquels l'équipe est abonnée, qui mesure sa couverture de la veille

**5.** *Question ouverte (2-3 lignes).* « La feuille de route la plus dangereuse est celle qui ne contient que des chantiers structurels. » Pourquoi, et que faut-il y mettre en plus ?

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. C.** L'échelle va de 1 à 5 : ignoré, conscient, planifié, appliqué, tenu dans le temps — la note 4 signifie « en place, et ça se vérifie ».
**Pourquoi :** l'auto-évaluation sert à décider, pas à se noter ; les cinq domaines sont ceux du parcours (code, dépendances, accès, réseau, réponse à incident), et mettre la même note partout signale que l'évaluation n'a pas été faite.

**2. B.** « Sommes-nous en sécurité ? » est une question à laquelle personne ne peut répondre honnêtement — on finit par recevoir une réponse rassurante et fausse.
**Pourquoi :** la sécurité n'est pas un état qu'on atteint, c'est une trajectoire qu'on suit ; la grille de maturité, remplie honnêtement en une page, sert à situer et à ordonner la prochaine étape.

**3. B.** Une feuille de route qui liste tout ne priorise rien ; trois questions suffisent à ordonner : qu'est-ce qui est le plus précieux (données, service, réputation), quel est le chemin le plus court pour y arriver, quel geste coupe ce chemin pour le moins d'effort.
**Pourquoi :** c'est la règle de proportionnalité rencontrée dès la première journée du parcours, appliquée intégralement à la planification.

**4. B.** Ce qui compte n'est pas le nombre d'alertes lues mais le délai de réaction : ce temps se réduit avec un inventaire des composants tenu à jour (le SBOM), des alertes automatiques sur les dépendances, et une personne nommée pour traiter ce qui arrive.
**Pourquoi :** sans inventaire ni personne désignée, la question « sommes-nous concernés ? » reste sans réponse quand la faille est déjà exploitée.

**5.** Attendu : une feuille de route uniquement structurelle ne change rien avant longtemps, et l'intérêt de l'équipe retombe ; il faut y joindre un geste immédiat — ce qui coupe un chemin d'attaque connu en quelques jours (fermer une exposition inutile, révoquer une clé commitée).
**Pourquoi :** un chantier visible dans les deux premières semaines maintient l'équipe en mouvement, pendant que le court terme installe les protections durables et que le structurel change les habitudes.

</details>

---

[← Chapitre précédent](17-reponse-incident.md) · [Sommaire](Readme.md) · [Chapitre suivant →](A-Glossaire-et-ressources.md)
