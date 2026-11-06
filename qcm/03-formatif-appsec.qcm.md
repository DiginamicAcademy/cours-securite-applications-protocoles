---
qcm:
  version: 1
  module: "QCM formatif — Sécuriser les applications et les protocoles (J7-J9)"
  duree: 30                    # minutes, à titre indicatif (24 questions)
  niveau-global: mixte         # facile | moyen | avance
  type: formatif               # non noté, tentatives illimitées
  pedagogie:
    rncp: "RNCP40573"
    certification: "Expert en informatique et systèmes d'information"
    niveau: "Bac+5 (Niveau 7)"
    specialisation: "4B Big Data & IA"
  profil-export: moodle
  bareme: { correct: 1, mauvais: 0 }
  seuil: 0.7                   # indicatif : le formatif n'est pas noté au bulletin
---

<!--
  SOURCE DE VÉRITÉ de ce QCM formatif. Le XML d'import, 03-formatif-appsec.moodle.xml,
  est couplé 1:1 à ce fichier (règle maison : 1 QCM = 1 .qcm.md + 1 .moodle.xml).
  24 questions, choix unique, 1 point, réponses mélangées (shuffleanswers).
  Une section par journée : J7 chapitres 01-06, J8 chapitres 07-12, J9 chapitres 13-18.
  Les questions portent uniquement sur le contenu OBLIGATOIRE des chapitres : aucun
  approfondissement « Pour aller plus loin » n'est interrogé.
  Les lettres A/B/C/D sont celles de cette liste : elles ne figurent ni dans le XML,
  ni dans les feedbacks, parce que Moodle mélange les propositions.
-->

## Journée 7 — Sécuriser l'application dans le code (chapitres 01 à 06)

## Q1 {niveau: facile, tags: [ch01, principes]}

Le moindre privilège se vérifie avec trois questions, à poser pour chaque script, chaque service, chaque requête. Laquelle ne fait **pas** partie de ces trois questions ?

- [ ] A. Quelles données cette tâche doit-elle réellement lire ?
- [ ] B. Quels droits ce composant doit-il détenir ?
- [ ] C. Quel compte exécute ce code ?
- [x] D. Qui a écrit ce code et quand a-t-il été revu ?

> **Réponse : D** — Les trois questions portent sur les données, les droits et le compte ; l'auteur et la date de revue relèvent de la revue de code, pas du moindre privilège.
> **Chapitre à revoir : 01.**

## Q2 {niveau: facile, tags: [ch02, injections]}

Une recherche est écrite `WHERE titre LIKE ?`, la saisie étant transmise comme paramètre. Pourquoi cette forme neutralise-t-elle une saisie du type `' OR '1'='1` ?

- [ ] A. Parce qu'elle supprime les caractères spéciaux de la saisie avant de l'utiliser
- [ ] B. Parce qu'elle chiffre la requête avant de l'envoyer à la base
- [x] C. Parce que la saisie reste une valeur et ne devient jamais un morceau de l'instruction
- [ ] D. Parce qu'elle échappe la saisie en HTML avant de l'insérer

> **Réponse : C** — L'instruction est choisie avant que la saisie ne soit lue : elle ne peut donc pas en modifier la forme. L'échappement HTML, lui, protège une page, pas une base.
> **Chapitre à revoir : 02.**

## Q3 {niveau: moyen, tags: [ch02, validation]}

Un champ libre reçoit une valeur qui ne correspond ni au format ni à la longueur attendus. Que fait une validation d'entrée bien conçue ?

- [ ] A. Elle remplace les caractères dangereux par des caractères sûrs, puis enregistre
- [ ] B. Elle enregistre la valeur telle quelle : l'échappement interviendra à l'affichage
- [ ] C. Elle borne la longueur et laisse passer le reste de la valeur
- [x] D. Elle refuse la valeur, au lieu de la réparer

> **Réponse : D** — En entrée on refuse ce qui n'est pas attendu : « réparer » la saisie cache un problème et lui apprend à revenir. L'échappement est un geste distinct, fait au moment de l'affichage.
> **Chapitre à revoir : 02.**

## Q4 {niveau: moyen, tags: [ch03, echappement]}

Un commentaire saisi par un utilisateur est affiché sur une page. Dans quel cas l'échappement HTML est-il insuffisant à lui seul ?

- [ ] A. Quand le commentaire est affiché dans un paragraphe de texte
- [x] B. Quand le commentaire est inséré dans un gestionnaire d'événement JavaScript d'une balise
- [ ] C. Quand le commentaire contient des accents ou des apostrophes
- [ ] D. Quand le commentaire est plus long que la colonne qui le stocke

> **Réponse : B** — Le traitement dépend du contexte d'insertion : dans un contexte JavaScript, c'est celui-là qui commande, et l'échappement HTML n'y suffit pas.
> **Chapitre à revoir : 03.**

## Q5 {niveau: moyen, tags: [ch03, csp]}

Que fait une Content Security Policy (CSP) ?

- [ ] A. Elle échappe les sorties HTML au moment de l'affichage
- [x] B. Elle liste ce qu'une page a le droit de charger et d'exécuter, et se déclare dans un en-tête de réponse HTTP
- [ ] C. Elle remplace l'échappement dès lors qu'elle est en place
- [ ] D. Elle interdit l'exécution de tout script sur le site

> **Réponse : B** — La CSP est une liste posée côté serveur dans un en-tête de réponse : ceinture et bretelles derrière l'échappement, jamais à sa place.
> **Chapitre à revoir : 03.**

## Q6 {niveau: facile, tags: [ch04, journalisation]}

Une opération échoue en production. Quelle information a sa place dans le journal d'application ?

- [ ] A. Le mot de passe saisi, masqué par des astérisques
- [ ] B. La saisie entière de l'utilisateur, pour reproduire l'incident
- [x] C. Le fait que l'opération a échoué, avec l'identifiant technique concerné
- [ ] D. Le contenu complet du fichier traité

> **Réponse : C** — Un journal décrit ce qui s'est passé, pas ce que contenaient les données : le fait et l'identifiant technique, jamais la valeur. À l'utilisateur, un message générique avec un identifiant de suivi.
> **Chapitre à revoir : 04.**

## Q7 {niveau: moyen, tags: [ch05, dependances]}

Une faille est publiée sur une bibliothèque de votre application. Quelle suite de gestes correspond à ce que le cours appelle l'analyse des composants ?

- [ ] A. Retirer la bibliothèque, réécrire la fonctionnalité, tester, livrer
- [ ] B. Attendre la prochaine version majeure et tout mettre à jour d'un coup
- [x] C. Lire l'inventaire des composants, situer l'exposition réelle, corriger, vérifier
- [ ] D. Relever la note de gravité publiée et décider d'après elle seule

> **Réponse : C** — Quatre temps : lire, situer (le code vulnérable est-il réellement appelé ?), corriger, vérifier. La note de gravité décrit la bibliothèque, pas votre situation.
> **Chapitre à revoir : 05.**

## Q8 {niveau: moyen, tags: [ch06, revue-de-code]}

La revue de sécurité d'un diff se conduit en trois passes indépendantes, chacune avec sa question. Lesquelles, et dans quel ordre ?

- [ ] A. Lisibilité, performance, maintenabilité
- [ ] B. Entrées, appels système, sorties
- [x] C. Entrées, sorties, appels système
- [ ] D. Nommage, commentaires, tests

> **Réponse : C** — Qu'arrive-t-il de l'extérieur, qu'est-ce qui sort, que déclenche le code : chaque passe se fait sur tout le fichier avant de passer à la suivante.
> **Chapitre à revoir : 06.**

## Journée 8 — API, données et conformité (chapitres 07 à 12)

## Q9 {niveau: facile, tags: [ch07, api]}

Un client authentifié obtient le dossier d'un autre client en changeant l'identifiant dans l'URL. De quel risque s'agit-il ?

- [ ] A. Une injection dans la base
- [x] B. Du BOLA (Broken Object Level Authorization)
- [ ] C. Un manquement à la validation de schéma
- [ ] D. Une dépendance vulnérable

> **Réponse : B** — C'est le risque n°1 des API : l'API vérifie que vous êtes connecté, pas que l'objet demandé est le vôtre.
> **Chapitre à revoir : 07.**

## Q10 {niveau: moyen, tags: [ch07, versioning]}

Une équipe garde `/v1` ouverte « au cas où », trois ans après l'arrivée de `/v2`. Quel est le problème, du point de vue de la sécurité ?

- [ ] A. Cela rend la validation de schéma des requêtes impossible
- [x] B. Chaque version maintenue est une surface d'attaque maintenue
- [ ] C. Cela empêche de versionner dans le chemin
- [ ] D. Cela alourdit uniquement les journaux d'accès

> **Réponse : B** — Garder `/v1`, c'est garder les erreurs de `/v1` : on annonce une fin de vie (date de dépréciation, en-tête `Sunset`), on mesure l'usage, puis on coupe l'ancienne version.
> **Chapitre à revoir : 07.**

## Q11 {niveau: facile, tags: [ch08, scopes]}

Un appel arrive avec un jeton valide dont le scope ne couvre pas l'action demandée. Quel code de refus est le bon ?

- [ ] A. 401, car l'appelant n'est pas autorisé
- [x] B. 403, car l'appelant est identifié mais n'a pas ce droit
- [ ] C. 429, car l'appel insiste au-delà du périmètre
- [ ] D. 404, car la ressource doit rester invisible

> **Réponse : B** — 401 dit « je ne sais pas qui vous êtes », 403 dit « je sais qui vous êtes, et vous n'avez pas ce droit ». Un jeton valide au périmètre trop étroit, c'est un 403.
> **Chapitre à revoir : 08.**

## Q12 {niveau: moyen, tags: [ch08, limitation]}

Un appelant dépasse le quota que l'API lui fixe. Que doit-il recevoir pour cesser de marteler ?

- [ ] A. Un 403 sans information complémentaire
- [ ] B. Une réponse vide, pour ne rien divulguer
- [x] C. Un 429 (Too Many Requests) accompagné de l'en-tête `Retry-After`
- [ ] D. Un 500, pour que le client retente plus tard

> **Réponse : C** — Le rate limiting se décide sur trois points : qui compte, quel rythme, que renvoyer — un 429 avec `Retry-After`, pour que l'appelant sache quand réessayer.
> **Chapitre à revoir : 08.**

## Q13 {niveau: facile, tags: [ch09, classification]}

La classification attribue à chaque donnée un niveau de sensibilité, du plus exposable au plus protégé. Sur quel critère se décide ce niveau ?

- [ ] A. Sur la valeur commerciale de la donnée
- [x] B. Sur le dommage causé par sa divulgation
- [ ] C. Sur le volume de données stockées
- [ ] D. Sur l'ancienneté de la donnée

> **Réponse : B** — Le critère est le dommage, pas la valeur : mots de passe, RIB (relevé d'identité bancaire) et numéro de sécurité sociale sont strictement confidentiels et ne sortent jamais par une API.
> **Chapitre à revoir : 09.**

## Q14 {niveau: moyen, tags: [ch10, rgpd]}

Une case pré-cochée dans les conditions générales vaut-elle consentement, et quelle base légale justifie la conservation de l'adresse de livraison d'une commande ?

- [ ] A. Oui, il vaut consentement ; c'est donc la même base pour l'adresse de livraison
- [ ] B. Non ; elle relève de l'obligation légale
- [x] C. Non ; l'adresse de livraison relève de l'exécution du contrat
- [ ] D. Oui ; l'adresse de livraison relève de l'intérêt légitime

> **Réponse : C** — Un consentement pré-coché ou glissé dans les conditions générales ne vaut pas consentement. L'adresse qui sert à livrer ce qui est convenu repose sur l'exécution du contrat.
> **Chapitre à revoir : 10.**

## Q15 {niveau: moyen, tags: [ch11, pipelines]}

Un test de données détecte des durées négatives dans le lot produit par l'étape de transformation, avant le chargement dans l'entrepôt. Que doit faire ce test ?

- [ ] A. Envoyer une alerte après le chargement, pour ne pas bloquer l'exécution de nuit
- [ ] B. Corriger les valeurs inattendues pour que le lot passe
- [ ] C. Consigner l'anomalie dans un tableau de bord à consulter le lendemain
- [x] D. Bloquer le chargement

> **Réponse : D** — Un pipeline fail-closed : le test bloque avant l'entrepôt. Alerter après le chargement laisse les données fausses entrer dans les rapports.
> **Chapitre à revoir : 11.**

## Q16 {niveau: avance, tags: [ch12, anonymisation]}

Un export « anonymisé » d'adhérents ne contient plus de nom ni de courriel, mais garde le code postal, la date de naissance et le sexe. Comment juger cette anonymisation ?

- [ ] A. Elle est acquise dès lors qu'aucune colonne nominative ne subsiste
- [x] B. Elle se mesure à la ré-identification possible par croisement avec une autre source
- [ ] C. Elle dépend du nombre de lignes que compte l'export
- [ ] D. Elle suffit dès lors que le fichier est transmis chiffré

> **Réponse : B** — L'anonymat se mesure à la ré-identification possible, pas aux colonnes supprimées : des quasi-identifiants recroisés peuvent suffire à retrouver une personne.
> **Chapitre à revoir : 12.**

## Journée 9 — Réseau, chaîne de livraison et service (chapitres 13 à 18)

## Q17 {niveau: facile, tags: [ch13, tls]}

Que garantit une connexion TLS (Transport Layer Security) ?

- [ ] A. Que le site visité est honnête et conserve bien vos données
- [ ] B. Que le nom de domaine que vous avez tapé est bien celui que vous vouliez
- [x] C. La confidentialité de l'échange, son intégrité, et l'authentification du serveur
- [ ] D. Que le site ne peut pas être un site de hameçonnage

> **Réponse : C** — TLS garantit confidentialité, intégrité et identité du serveur — pas l'honnêteté du site : un site de hameçonnage parfaitement chiffré reste un site de hameçonnage.
> **Chapitre à revoir : 13.**

## Q18 {niveau: moyen, tags: [ch13, durcissement]}

Une messagerie propose le chiffrement en cours de connexion, mais accepte le repli en clair si la négociation échoue. Quelle attaque exploite précisément ce point, et quel principe de durcissement y répond ?

- [ ] A. L'usurpation de réponse DNS ; il faut signer les réponses de résolution
- [x] B. La dégradation forcée ; il faut imposer le chiffrement et refuser le repli en clair
- [ ] C. L'interception par personne interposée ; il faut administrer l'accès distant par clé publique
- [ ] D. L'épuisement du service ; il faut limiter le débit des appelants

> **Réponse : B** — La dégradation forcée fait croire que l'autre extrémité ne sait pas chiffrer : un chiffrement optionnel est un chiffrement contournable, il faut l'imposer. DNSSEC et l'authentification par clé répondent aux deux autres failles du chapitre.
> **Chapitre à revoir : 13.**

## Q19 {niveau: moyen, tags: [ch14, zero-trust]}

Quelle phrase reprend le principe Zero Trust (confiance zéro) appliqué à une application ?

- [ ] A. Le réseau interne est sûr, le réseau extérieur est hostile
- [ ] B. Il faut authentifier chaque machine une seule fois, à sa connexion au réseau
- [x] C. La position sur le réseau ne prouve rien : chaque appel prouve son identité et ses droits
- [ ] D. Il faut placer les bases de données dans la zone tampon visible de l'extérieur

> **Réponse : C** — Zero Trust applique au réseau le moindre privilège : chaque appel est authentifié et autorisé, y compris entre services internes, et le trafic est chiffré partout.
> **Chapitre à revoir : 14.**

## Q20 {niveau: facile, tags: [ch15, devsecops]}

Dans la chaîne d'intégration continue, quel contrôle répond à la question « ce que vous importez est-il sain ? »

- [ ] A. Le SAST (Static Application Security Testing), qui lit le code source sans l'exécuter
- [x] B. Le SCA (Software Composition Analysis), qui regarde les dépendances et leurs versions
- [ ] C. La recherche de secrets, qui balaie le code et l'historique des commits
- [ ] D. Le SBOM (Software Bill of Materials), qui inventorie les composants livrés

> **Réponse : B** — Le SCA porte sur les composants importés. SAST lit votre propre code, la recherche de secrets cherche les clés laissées, le SBOM tient l'inventaire : aucun ne remplace les autres.
> **Chapitre à revoir : 15.**

## Q21 {niveau: moyen, tags: [ch15, secrets]}

Une clé d'API vient d'être découverte dans un commit déjà poussé sur un dépôt privé. Quelle est la bonne réaction ?

- [ ] A. Supprimer la ligne et pousser un nouveau commit
- [ ] B. Passer le dépôt en plus restreint et attendre
- [x] C. Révoquer la clé, puis corriger le code
- [ ] D. Réécrire l'historique de Git, et n'en parler à personne

> **Réponse : C** — Un secret commité est compromis : l'historique garde tout, et un dépôt privé n'est pas un dépôt sûr. On révoque d'abord, on corrige ensuite.
> **Chapitre à revoir : 15.**

## Q22 {niveau: moyen, tags: [ch16, tests]}

Au printemps, une injection est corrigée dans la recherche d'une API. À l'automne, une réécriture réintroduit la concaténation d'origine, sans que personne s'en aperçoive. Quel geste aurait empêché cette régression ?

- [ ] A. Une revue de code supplémentaire à la livraison d'automne
- [ ] B. Un audit de sécurité annuel
- [ ] C. Le passage de l'API derrière une passerelle d'API
- [x] D. Un test qui rejoue le payload d'origine et attend un code de refus précis

> **Réponse : D** — Chaque faille corrigée devient un test : le smoke test rejoue le payload qui marchait avant et vérifie qu'il échoue toujours, en attendant un code de réponse précis.
> **Chapitre à revoir : 16.**

## Q23 {niveau: moyen, tags: [ch17, incident]}

Pendant un incident, un serveur est identifié comme compromis. Que fait exactement le temps « contenir » ?

- [ ] A. Il formate le disque du serveur pour repartir d'une base propre
- [x] B. Il limite l'extension de l'incident sans détruire les traces
- [ ] C. Il restaure la dernière sauvegarde vérifiée
- [ ] D. Il écrit la chronologie de l'incident pour l'équipe

> **Réponse : B** — Contenir n'est pas détruire : couper un accès, isoler un segment, désactiver un compte, oui ; formater ou effacer des journaux, non — les traces servent à comprendre, restaurer, parfois prouver.
> **Chapitre à revoir : 17.**

## Q24 {niveau: moyen, tags: [ch18, maturite]}

Dans la grille de maturité du parcours, chaque domaine est noté de 1 à 5. Que signifie une note de 3 ?

- [ ] A. Ignoré : personne ne s'en occupe, ou on ne sait pas
- [ ] B. Conscient : le sujet est identifié, rien n'est fait
- [x] C. Planifié : une décision existe, elle n'est pas appliquée partout
- [ ] D. Tenu dans le temps : c'est en place, vérifié, et amélioré par les retours

> **Réponse : C** — 1 ignoré, 2 conscient, 3 planifié, 4 appliqué, 5 tenu dans le temps. La grille sert à décider de la prochaine étape, pas à se noter.
> **Chapitre à revoir : 18.**
