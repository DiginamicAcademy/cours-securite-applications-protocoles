[← Chapitre précédent](09-donnees-sensibles.md) · [Sommaire](Readme.md) · [Chapitre suivant →](11-pipelines-data.md)

# RGPD appliqué — la donnée personnelle a une date de péremption

> Une plainte vise une chaîne de magasins de sport : ses adresses courriel sont
> conservées « au cas où », sans limite de durée, des années après le dernier
> achat. La loi n'est pas un frein à l'activité — c'est une **contrainte
> technique** à concevoir dès le départ, comme on conçoit une contrainte de
> performance ou de disponibilité.

**Durée de lecture :** 40 min hors approfondissements facultatifs · **Prérequis :** le chapitre [Données sensibles](09-donnees-sensibles.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Rattacher** chaque traitement de données personnelles à une base légale.
- **Définir** une durée de conservation et son mécanisme d'effacement.
- **Mettre en œuvre** les droits des personnes dans une application (accès,
  rectification, effacement, portabilité).
- **Documenter** un traitement dans un registre — l'exposé du registre est en approfondissement.

---

## I. Les bases légales

Le RGPD (Règlement général sur la protection des données) encadre le
traitement des données personnelles — toute information se rapportant à une
personne identifiable : un nom, un courriel, une adresse, un identifiant client,
une adresse IP. Chaque traitement doit reposer sur **une base légale**, choisie
et documentée avant de collecter quoi que ce soit :

| Base légale | Quand l'utiliser | Exemple dans le commerce de détail |
| --- | --- | --- |
| **Consentement** | la personne dit oui, librement et explicitement | l'inscription à une newsletter promotionnelle |
| **Exécution du contrat** | la donnée sert à exécuter ce qui est convenu | l'adresse de livraison d'une commande en ligne |
| **Obligation légale** | une loi l'impose | la conservation des factures pour la comptabilité |
| **Intérêt légitime** | un intérêt réel, équilibré avec les droits de la personne | la détection de fraude sur les cartes de fidélité |

Le consentement a trois exigences qui le distinguent d'une case pré-cochée : il
est **spécifique** (une case par usage), **éclairé** (on dit ce qu'on en fait),
et **révocable** (un lien de désinscription qui fonctionne vraiment).

> [!WARNING]
> « La personne n'a pas dit non » n'est pas une base légale. Un consentement
> pré-coché, ou glissé dans les conditions générales, ne vaut pas
> consentement — et retourne le traitement vers une autre base à justifier.

---

## II. Durée et effacement

Une donnée personnelle a une **date de péremption**. La durée de conservation
se décide par finalité : le temps de traiter la commande, pas « tant que la
base existe ». Passé ce délai, deux gestes sont possibles selon l'usage :

| Sort de la donnée | Quand | Effet |
| --- | --- | --- |
| **Effacement** | plus aucune obligation ne la retient | la ligne disparaît |
| **Archivage intermédiaire** | une obligation légale la retient (facturation, garantie) | isolée, hors des applications actives, avec un accès restreint |
| **Anonymisation** | on veut garder des statistiques sans garder la personne | la donnée sort du champ du RGPD, définitivement |

---

## III. Droits des personnes

Le RGPD donne à chaque personne un **pouvoir d'action** sur ses données. Chaque
droit se traduit par une fonctionnalité concrète — pas par une adresse
courriel à laquelle « on répondra peut-être » :

| Droit | Ce que la personne demande | Traduction technique |
| --- | --- | --- |
| **Accès** | voir les données la concernant | un export au format JSON ou CSV (Comma-Separated Values), de son profil et de son historique |
| **Rectification** | corriger une donnée fausse | un endpoint de mise à jour, ouvert sur les champs concernés |
| **Effacement** | disparaître | supprimer les données, sauf obligation légale contraire (les factures restent) |
| **Portabilité** | récupérer ses données pour aller ailleurs | un export structuré, lisible par machine |
| **Opposition** | s'arrêter | un mécanisme de désinscription qui agit vraiment |

Deux écueils reviennent dans les audits :

- **Le droit qui existe sur le papier** — un formulaire de contact qui promet
  une réponse sous 30 jours, sans outil derrière. Le délai légal est court :
  un mois, prolongeable une fois, pas plus.
- **L'effacement partiel** — la ligne disparaît de la table `clients`, mais
  reste dans les sauvegardes, les journaux, le tableur du service marketing.
  L'effacement doit couvrir **tous les endroits** où la donnée vit, ou documenter
  pourquoi certains la retiennent temporairement.

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **Le registre des traitements** — le document qui liste, pour chaque
  traitement : finalité, base légale, catégories de données, destinataires,
  durée, mesures de sécurité. Obligatoire au-delà d'une certaine taille
  d'organisation, il est surtout le **seul endroit** où l'on voit l'ensemble de
  ce qu'on détient — l'exercice 🔴 de ce bloc en construit un brouillon.
- **La notification de violation** — en cas de fuite de données personnelles, la
  CNIL (Commission nationale de l'informatique et des libertés) doit être
  prévenue dans les **72 heures** après en avoir pris connaissance, et les
  personnes concernées lorsque le risque est élevé. Un scénario de crise qui se
  répète à l'avance coûte quelques heures ; improvisé, il coûte des semaines.
- **Le DPO (délégué à la protection des données)** — la personne qui pilote la
  conformité, point de contact de la CNIL. Dans une petite structure, la
  responsabilité reste collective — désigner quelqu'un suffit à structurer le
  travail.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> Même question, autre jeu de données : la Partie 4 de l'exercice [Sécuriser un endpoint qui en dit trop](tp/09-securiser-endpoint-data.md) demande finalité, base légale et sort de la donnée.
>
> 🧪 **Atelier rapide (5 min)**
>
> Une chaîne de magasins de sport conserve sa table `ventes` indéfiniment.
> Voici ses colonnes. Pour chacune, décidez : **effacer**, **archiver** ou
> **anonymiser** après 5 ans, et pourquoi ?
>
> ```sql
> CREATE TABLE ventes (
>     id INT PRIMARY KEY,
>     client_id INT,            -- décision : ?
>     date_achat DATE,          -- décision : ?
>     montant DECIMAL(8, 2),    -- décision : ?
>     magasin VARCHAR(64),      -- décision : ?
>     mode_paiement VARCHAR(16) -- décision : ?
> );
> ```
>
> Notez vos décisions : la question « qui a besoin de quoi, et encore combien de
> temps ? » est exactement celle que pose l'exercice de fin de bloc.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Chaque droit est un ticket à fermer**
>
> Réflexe d'organisation pour celui qui exploite l'application ; la table ci-dessus suffit pour la journée.
>
> Traitez chaque droit comme un ticket de bug : un besoin, un responsable, un
> délai, une preuve de clôture. Les droits qui ne sont jamais demandés sont
>   ceux qui tombent le plus vite en panne.

---

## Points clés

- Chaque traitement repose sur **une base légale** choisie et documentée :
  consentement, contrat, obligation légale, intérêt légitime.
- Une donnée a une **date de péremption** : au-delà, on efface, on archive hors
  des applications actives, ou on anonymise.
- Les droits des personnes (accès, rectification, effacement, portabilité,
  opposition) sont des **fonctionnalités** à concevoir, avec un délai et une
  preuve de clôture.
- En cas de fuite de données personnelles : notification à la CNIL dans les
  **72 heures**. Le scénario se répète avant, pas pendant.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis cochez. Les réponses sont juste après le séparateur : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Une boutique en ligne conserve l'adresse de livraison de ses commandes. Sur quelle base légale repose ce traitement ?

- A. Le consentement : la personne a passé commande
- B. L'exécution du contrat : la donnée sert à exécuter ce qui est convenu
- C. L'obligation légale : la loi impose de connaître l'acheteur
- D. L'intérêt légitime : c'est utile pour la logistique

- [ ] ✓ je savais

**2.** L'inscription à la newsletter est activée par une case pré-cochée dans les conditions générales. Le traitement repose-t-il sur le consentement ?

- A. Oui : la personne n'a pas dit non, elle pouvait décocher
- B. Oui : les conditions générales suffisent à informer la personne
- C. Non : un consentement pré-coché ou glissé dans les conditions ne vaut pas consentement — il faut une case spécifique par usage, un usage expliqué et une révocation qui fonctionne
- D. Non, mais l'intérêt légitime couvre automatiquement les newsletters

- [ ] ✓ je savais

**3.** Cinq ans après la fin d'une relation client, les factures doivent encore être conservées pour la comptabilité. Quel sort leur appliquer ?

- A. Effacement : la durée de conservation principale est dépassée
- B. Archivage intermédiaire : isolées, hors des applications actives, avec un accès restreint
- C. Anonymisation : elles ne concernent plus personne
- D. Rien : les laisser dans les applications actives, elles y ont toujours été

- [ ] ✓ je savais

**4.** Un client exerce son droit à l'effacement : la ligne disparaît de la table `clients`. L'audit relève que la donnée vit encore dans les sauvegardes, les journaux et le tableur du service marketing. Qu'en dit le chapitre ?

- A. C'est conforme : la base de production est la référence
- B. C'est conforme si la personne a été informée par courriel
- C. C'est un effacement partiel : l'effacement doit couvrir tous les endroits où la donnée vit, ou documenter pourquoi certains la retiennent temporairement
- D. C'est un problème de sauvegarde, sans lien avec le droit des personnes

- [ ] ✓ je savais

**5.** *Question ouverte (2-3 lignes).* « Chaque droit se traduit par une fonctionnalité concrète — pas par une adresse courriel à laquelle on répondra peut-être. » Donnez deux exemples de traduction technique pris dans le chapitre, et précisez le délai qui s'attache à ces demandes.

- [ ] ✓ je savais

---

### Réponses

**1. B.** L'adresse de livraison d'une commande en ligne est l'exemple même de l'exécution du contrat : la donnée sert à exécuter ce qui est convenu.
**Pourquoi :** chaque traitement doit reposer sur une base légale choisie et documentée avant de collecter — ici ni consentement ni intérêt légitime ne sont nécessaires.

**2. C.** « La personne n'a pas dit non » n'est pas une base légale : le consentement exige d'être spécifique (une case par usage), éclairé (on dit ce qu'on en fait) et révocable (un lien de désinscription qui fonctionne vraiment).
**Pourquoi :** un consentement nul retourne le traitement vers une autre base à justifier — il n'y en a pas : il faut la choisir et l'écrire.

**3. B.** Une obligation légale (facturation, garantie) retient la donnée : elle part en archivage intermédiaire — isolée, hors des applications actives, avec un accès restreint.
**Pourquoi :** passé le délai de la finalité, trois gestes seulement : effacer, archiver, ou anonymiser ; ici l'obligation légale interdit l'effacement et l'anonymisation n'a pas de sens pour des factures nominatives.

**4. C.** C'est l'écueil de l'effacement partiel, récurrent dans les audits : la donnée survit dans les sauvegardes, les journaux, le tableur du marketing.
**Pourquoi :** l'effacement doit couvrir tous les endroits où la donnée vit, ou documenter pourquoi certains la retiennent temporairement — sinon le droit est un formulaire, pas une fonctionnalité.

**5.** Attendu (deux parmi) : accès → export JSON ou CSV du profil et de l'historique ; rectification → endpoint de mise à jour sur les champs concernés ; opposition → mécanisme de désinscription qui agit vraiment ; portabilité → export structuré lisible par machine ; effacement → suppression, sauf obligation légale (les factures restent). Délai : un mois, prolongeable une fois, pas plus.
**Pourquoi :** le droit qui existe sur le papier, sans outil derrière, est l'un des deux écueils les plus relevés en audit.

---

[← Chapitre précédent](09-donnees-sensibles.md) · [Sommaire](Readme.md) · [Chapitre suivant →](11-pipelines-data.md)
