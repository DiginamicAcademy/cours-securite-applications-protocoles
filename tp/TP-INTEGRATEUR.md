# TP intégrateur — Sécuriser de bout en bout une place de marché et son pipeline de données

> **Nature :** TP intégrateur **facultatif et non noté** — un travail pour pousser la compréhension, il ne compte pas au bulletin · **Durée :** 4 h · **Notion :** le cours entier (J7-J9), appliqué de bout en bout à une application et à son pipeline de données
> 🔵 **Intégration** · **Lien :** les trois journées ([chapitres 01 à 18](../Readme.md))
> **Objectif :** sécuriser un service réel de bout en bout et le prouver dans un dossier unique.

---

## Contexte

**Marché des Cévennes** est une place de marché en ligne de produits régionaux : trente producteurs y vendent fromages, confitures et charcuteries, et vingt-cinq mille comptes clients y passent commande. Six salariés tiennent la boutique depuis un bureau unique.

Le service repose sur six briques :

- **la boutique en ligne** — comptes clients, catalogue, panier, commandes et avis produits ; une base de commandes conserve nom, adresse e-mail, adresse de livraison et historique des achats ;
- **l'API des partenaires** — un transporteur pour le suivi des livraisons, un prestataire de paiement, un prestataire d'e-mailing ; les appels vont dans les deux sens, sans limitation de débit ;
- **le pipeline de données** — chaque nuit, un script d'extraction exporte les commandes vers un stockage objet, un job les transforme, et un entrepôt alimente les tableaux de bord de la direction ; un export mensuel part vers le prestataire d'e-mailing ;
- **la chaîne d'intégration continue** — un dépôt Git, un workflow de build et de déploiement, des variables d'environnement et des secrets ;
- **le réseau du bureau** — les postes des six salariés, le serveur d'application, la base de commandes, l'entrepôt ;
- **les sauvegardes** — nocturnes, hébergées chez un prestataire.

La direction veut passer de trente à cent vingt producteurs dans six mois, et confier une partie de la maintenance à une équipe externe. Elle pose une seule question : « **où en est la sécurité du service, et que faut-il faire en priorité ?** »

Votre mission : **sécuriser le service de bout en bout** — du code jusqu'au plan d'incident — et répondre à cette question dans un **dossier de sécurisation** unique.

**Ce qui est fourni** — le module de gestion des commandes à auditer : [`tp/marche-cevennes/`](marche-cevennes/). Son README explique comment le lancer, ce que vous verrez à l'exécution et ce qui n'est pas un bug du support. Les étapes 1 à 3 portent sur ce code ; les deux factures de démonstration y sont livrées, et relancer l'application laisse la base à trois commandes.

---

## Objectifs

À l'issue de ce TP, vous serez capable de :

- **Auditer** le code d'un module et classer les faiblesses trouvées.
- **Corriger** les injections, valider les entrées, échapper les sorties.
- **Traiter** les erreurs et les journaux sans rien exposer.
- **Recenser** les dépendances et les secrets d'un projet, et traiter les avis de sécurité.
- **Sécuriser** une API : autorisation, limitation, données exposées.
- **Classer** les données personnelles et les minimiser.
- **Traduire** les obligations RGPD en contraintes concrètes.
- **Analyser** les risques d'un pipeline de données, étape par étape.
- **Segmenter** un réseau et justifier chaque flux autorisé.
- **Écrire** un workflow d'intégration continue qui bloque les régressions.
- **Rédiger** un plan de réponse à incident.
- **Prioriser** les mesures restantes en une feuille de route motivée.

---

## Étapes

Les durées indiquées sont des **repères** pour tenir les 4 h annoncées — environ 25 minutes par étape, un peu plus pour la 2 et la 6 —, pas des minima. Avancez à votre rythme : le dossier compte plus que la montre.

### 1. Faire l'état des lieux du code — chapitres 01 et 06 (25 min)

Appliquez la [revue de code en trois passes](../06-revue-de-code-securite.md) au module de gestion des commandes de la boutique : les entrées, les sorties, les appels système. Classez chaque faiblesse avec les [principes du secure coding](../01-principes-secure-coding.md) — moindre privilège, défense en profondeur, fail-closed — et dites pour chacune ce qu'elle permet à un attaquant.

Deux précautions pour ne pas conclure trop vite. Sur la route de recherche, **le caractère `%` seul affiche déjà toutes les lignes** : c'est le joker de `LIKE`, pas une injection. Écrire « j'ai obtenu plus de lignes que prévu » ne prouve donc rien — pour prouver quelque chose, il faut faire apparaître dans la réponse **une ligne que la base ne contient pas**. Et sur la route d'annulation, l'appel au prestataire échoue toujours (domaine réservé) : regardez ce qui a **déjà** été écrit en base au moment où ça casse.

### 2. Sécuriser le code — chapitres 02, 03 et 04 (35 min)

Corrigez ce que l'état des lieux a fait remonter : requêtes paramétrées et [validation des entrées](../02-validation-et-injections.md), [échappement des sorties](../03-xss-et-sorties.md) et en-têtes de sécurité, [erreurs et journaux](../04-erreurs-et-logging.md) qui n'exposent rien. Chaque correction figure au dossier en extrait **avant / après**, avec une phrase qui dit ce qu'elle change.

### 3. Traiter les dépendances et la configuration — chapitre 05 (20 min)

Recensez les [dépendances et la configuration](../05-dependances-et-configuration.md) **du module fourni** : bibliothèques et leurs versions, secrets et mots de passe, configuration par environnement. Pour chaque avis de sécurité trouvé, dites si le service est exposé et quelle version retenir ; nommez les secrets à sortir du code et où les mettre.

Le module est la seule partie du service dont le code vous est donné. Pour les cinq autres briques, travaillez à partir du contexte : vous recensez ce qui **devrait** être déclaré, et vous signalez ce que vous ne pouvez pas vérifier sans le code. C'est une réponse, pas un oubli.

### 4. Sécuriser l'API des partenaires — chapitres 07 et 08 (20 min)

Reprenez la [surface d'attaque de l'API](../07-securite-api.md) : pour chaque endpoint, qui peut l'appeler, ce qu'il renvoie, ce qu'il coûte. Traitez les cas d'[autorisation et de limitation](../08-auth-et-limitation-api.md) — un partenaire ne doit lire que ses commandes, et aucun partenaire ne doit pouvoir épuiser le service.

Les endpoints des partenaires (transporteur, paiement, e-mailing) ne sont pas livrés : traitez-les comme à l'étape 3, en déclarant ce qui est vérifiable dans le module et ce qui ne l'est pas.

### 5. Protéger les données personnelles — chapitres 09 et 10 (20 min)

Classez les [données manipulées](../09-donnees-sensibles.md) par sensibilité, appliquez la minimisation et le masquage, puis traduisez les [obligations RGPD](../10-rgpd-applique.md) du service en contraintes concrètes : finalité, durée de conservation, information des clients. Complétez le registre des traitements pour les trois traitements principaux du service.

### 6. Sécuriser le pipeline de données — chapitres 11 et 12 (25 min)

Parcourez le [pipeline de données](../11-pipelines-data.md) étape par étape — extraction, stockage intermédiaire, transformation, entrepôt, export — et écrivez pour chacune les risques de fuite et d'altération, puis les mesures qui les traitent. Encadrez le [partage avec les tiers](../12-partage-et-tiers.md) : ce qui part vers le prestataire d'e-mailing, sous quelle forme, et avec quel contrat.

### 7. Durcir le réseau — chapitres 13 et 14 (20 min)

Listez les [protocoles utilisés](../13-protocoles-reseau.md) et dites, pour chacun, ce qui circule en clair. Puis découpez le service en [zones de confiance](../14-architecture-reseau.md) et ne gardez que les flux nécessaires : chaque flux retenu est justifié, chaque flux refusé aussi.

### 8. Verrouiller la chaîne DevSecOps — chapitres 15 et 16 (25 min)

Écrivez le [workflow d'intégration continue](../15-devsecops.md) du service : analyse statique, analyse des composants, recherche de secrets, SBOM (Software Bill of Materials, la liste de ce qui compose le logiciel). Ajoutez les [tests de sécurité](../16-tests-securite.md) qui empêchent une faille corrigée de revenir, et dites quelle porte de sécurité bloque quoi.

Un piège à éviter ici, parce qu'il fait passer un workflow au vert sans rien contrôler : un analyseur lancé **sans cible** audite l'environnement d'exécution, pas votre dépôt. Vérifiez toujours ce que votre porte de sécurité regarde avant de vous fier à sa couleur.

### 9. Préparer la réponse à incident — chapitre 17 (20 min)

Rédigez le [plan de réponse à incident](../17-reponse-incident.md) du service : qui décide, qui communique, dans quel ordre. Puis appliquez-le au scénario suivant — *un export mensuel de clients est retrouvé en accès public sur l'espace de stockage du prestataire d'e-mailing* — et racontez les premières heures heure par heure.

### 10. Arbitrer et conclure — chapitre 18 (15 min)

Rassemblez le tout dans le dossier (voir plus bas), et terminez par une [feuille de route](../18-maturite-et-perspectives.md) : ce qui est fait, ce qui reste, dans quel ordre, et pour quel gain. Un arbitrage motivé vaut mieux qu'une mesure de plus : dites ce que vous **ne faites pas**, et pourquoi.

---

## Livrable

**Le dossier de sécurisation du service** — un document unique de huit à dix pages, avec ces sections :

1. **Le service** — périmètre, actifs, données manipulées, acteurs.
2. **Le code** — état des lieux, corrections appliquées (extraits avant / après), dépendances, configuration et secrets.
3. **L'API et les données personnelles** — autorisation, limitation, minimisation, contraintes RGPD.
4. **Le pipeline et les tiers** — risques par étape, cloisonnement, encadrement du partage.
5. **Le réseau** — zones, flux retenus et refusés, protocoles.
6. **La chaîne DevSecOps** — workflow, portes de sécurité, SBOM, tests.
7. **La réponse à incident et la feuille de route** — plan, scénario traité, priorités.

Les étapes 1 à 9 sont la matière du dossier, pas des livrables à part. Ce TP est **facultatif et non noté** : il se rend pour pousser la compréhension, pas pour la note.

---

## ✅ Auto-évaluation

Avant de considérer le dossier terminé, vérifiez que :

- [ ] Le service est décrit en **briques, données et acteurs** — on sait ce qui est protégé.
- [ ] La revue de code donne une **faiblesse classée** pour chaque problème trouvé, avec ce qu'elle permet à un attaquant.
- [ ] Chaque correction figure en extrait **avant / après**, avec une phrase qui dit ce qu'elle change.
- [ ] Les dépendances sont **recensées avec leurs versions**, les secrets sont **sortis du code**, et chaque avis de sécurité est arbitré.
- [ ] Chaque endpoint de l'API dit **qui peut l'appeler, ce qu'il renvoie, ce qu'il coûte**.
- [ ] Les données personnelles sont **classées**, minimisées, et les durées de conservation sont posées.
- [ ] Le pipeline est traité **étape par étape** — fuite et altération — et le partage avec le prestataire est encadré.
- [ ] Chaque flux réseau retenu est **justifié**, et chaque flux refusé aussi.
- [ ] Le workflow d'intégration continue nomme **quelle porte de sécurité bloque quoi**, et deux tests de non-régression sont écrits.
- [ ] Le plan de réponse à incident nomme **qui décide, qui communique, dans quel ordre**, et le scénario est traité heure par heure.
- [ ] La feuille de route dit ce qui est fait, ce qui reste, **dans quel ordre, et pourquoi** — y compris ce qui ne sera pas fait.
