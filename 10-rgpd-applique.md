[← Chapitre précédent](09-donnees-sensibles.md) · [Sommaire](Readme.md) · [Chapitre suivant →](11-pipelines-data.md)

# RGPD appliqué — la donnée personnelle a une date de péremption

> Une plainte vise une chaîne de magasins de sport : ses adresses courriel sont
> conservées « au cas où », sans limite de durée, des années après le dernier
> achat. La loi n'est pas un frein à l'activité — c'est une **contrainte
> technique** à concevoir dès le départ, comme on conçoit une contrainte de
> performance ou de disponibilité.

**Durée de lecture :** 60 min · **Prérequis :** le chapitre [Données sensibles](09-donnees-sensibles.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Rattacher** chaque traitement de données personnelles à une base légale.
- **Définir** une durée de conservation et son mécanisme d'effacement.
- **Mettre en œuvre** les droits des personnes dans une application (accès,
  rectification, effacement, portabilité).
- **Documenter** un traitement dans un registre.

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

> 🧪 **Atelier rapide (5 min)**
>
> Une chaîne de magasins de sport conserve sa table `ventes` indéfiniment.
> Voici ses colonnes. Pour chacune, décidez : **effacer**, **archiver** ou
> **anonymiser** après 5 ans, et pourquoi ?

```sql
CREATE TABLE ventes (
    id INT PRIMARY KEY,
    client_id INT,            -- décision : ?
    date_achat DATE,          -- décision : ?
    montant DECIMAL(8, 2),    -- décision : ?
    magasin VARCHAR(64),      -- décision : ?
    mode_paiement VARCHAR(16) -- décision : ?
);
```

Notez vos décisions : la question « qui a besoin de quoi, et encore combien de
temps ? » est exactement celle que pose l'exercice de fin de bloc.

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

> [!TIP]
> Traitez chaque droit comme un ticket de bug : un besoin, un responsable, un
> délai, une preuve de clôture. Les droits qui ne sont jamais demandés sont
  ceux qui tombent le plus vite en panne.

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

[← Chapitre précédent](09-donnees-sensibles.md) · [Sommaire](Readme.md) · [Chapitre suivant →](11-pipelines-data.md)
