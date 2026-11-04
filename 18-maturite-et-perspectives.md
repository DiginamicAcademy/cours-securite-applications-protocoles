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

**Durée de lecture :** 55 min · **Prérequis :** les journées précédentes du parcours

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

### Ce que la note ne dit pas

Une note est un signal, pas un verdict. Deux précautions : une note haute obtenue
« parce qu'on a un outil » ne vaut rien si personne ne regarde ce qu'il produit,
et une note basse n'est pas une faute — c'est une **décision à prendre**. Le but
de la grille est de faire apparaître les écarts qui coûtent cher, pas de classer
les équipes.

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

### Ce qu'il faut suivre

La veille n'est pas une lecture du dimanche : c'est un processus, avec des
sources, un rythme et un **délai de réaction**.

| Source | Ce qu'elle apporte |
| --- | --- |
| **GHSA** (GitHub Security Advisory, l'alerte de sécurité publiée sur GitHub) | les alertes sur les composants que vous utilisez réellement |
| **NVD** (National Vulnerability Database, la base publique de vulnérabilités) | la référence des failles publiées, leur gravité, leurs correctifs |
| **Les listes des éditeurs** | les annonces de versions corrigées, pour vos outils et vos langages |
| **Les CERT** (Computer Emergency Response Team, les équipes de réponse à incident) | les alertes et recommandations par secteur et par pays |

### Le délai de réaction

Ce qui compte n'est pas le nombre d'alertes lues, mais le temps entre la
publication d'une faille et le moment où votre organisation sait **si elle est
concernée**. Ce temps se réduit mécaniquement : inventaire des composants tenu à
jour, alertes automatiques sur les dépendances, et une personne nommée pour
traiter ce qui arrive. Cet inventaire est le SBOM (Software Bill of Materials, la
liste des composants) décrit au chapitre sur la chaîne de livraison.

> 💡 **Astuce** — automatisez la collecte, jamais la décision. Une alerte
> automatique qui crée une tâche assignée est utile ; un correctif appliqué sans
> regarder ce qu'il change ne l'est pas toujours.

---

## IV. L'effet de l'IA

### Ce que ça change pour l'attaquant

L'IA accélère ce qui était lent : la reconnaissance d'une cible, la rédaction de
messages de phishing crédibles et personnalisés, la génération de PoC (proof of
concept, la preuve de concept qu'une faille est exploitable) à partir d'une
description publique. Un LLM (large language model, un modèle de langage de grande
taille) ne découvre pas de faille inédite par magie : il **réduit le délai** entre
la publication d'une faille et sa tentative d'exploitation à grande échelle.

### Ce que ça change pour le défenseur

Exactement le même levier, de l'autre côté :

| Usage défensif | Ce qu'il apporte |
| --- |---|
| **Aide à la revue de code** | repérer les schémas dangereux dans de gros volumes de code |
| **Priorisation des alertes** | trier ce qui arrive des contrôles automatisés, expliquer pourquoi |
| **Rédaction de correctifs et de tests** | produire le premier jet, que l'humain vérifie |
| **Compréhension d'un incident** | résumer des journaux, reconstituer une chronologie |

La ligne de conduite reste la même que pour tout le parcours : **l'IA propose,
l'humain décide**. Un correctif généré sans revue est un changement de plus dans
un système qui en a déjà beaucoup.

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

[← Chapitre précédent](17-reponse-incident.md) · [Sommaire](Readme.md) · [Chapitre suivant →](A-Glossaire-et-ressources.md)
