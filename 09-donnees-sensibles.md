[← Chapitre précédent](08-auth-et-limitation-api.md) · [Sommaire](Readme.md) · [Chapitre suivant →](10-rgpd-applique.md)

# Données sensibles — classer, minimiser, masquer

> Un éditeur de logiciel de gestion RH découvre, en revoyant son API de paie,
> que la fiche d'un salarié renvoie son numéro de sécurité sociale, son RIB (relevé d'identité bancaire)
> et son salaire — dans une réponse destinée à un simple affichage de planning. La
> base ne fuit pas : c'est l'**endpoint** qui donne trop. Le meilleur moyen de
> protéger une donnée, c'est souvent de ne pas la renvoyer.

**Durée de lecture :** 40 min hors approfondissements facultatifs · **Prérequis :** les chapitres [Sécurité des API](07-securite-api.md) et [Auth et limitation d'API](08-auth-et-limitation-api.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Classifier** les données d'un schéma de base en quatre niveaux de
  sensibilité.
- **Minimiser** la réponse d'un endpoint aux seuls champs utiles à son usage.
- **Masquer** ou pseudonymiser une donnée qui ne peut pas être supprimée.
- **Arbitrer** entre lisibilité métier et exposition de données.

---

## I. Classification

Avant de protéger quoi que ce soit, il faut savoir **ce que l'on détient**. La
classification attribue à chaque donnée un niveau, du plus exposable au plus
protégé :

| Niveau | Définition | Exemples | Règle par défaut |
| --- | --- | --- | --- |
| **Publique** | diffusable sans dommage | catalogue de produits, horaires d'ouverture | publier librement |
| **Interne** | utile à l'organisation, gênant si diffusé | organigramme, plannings internes | restreindre au périmètre de l'entreprise |
| **Confidentielle** | dommageable en cas de fuite | courriels clients, historiques de commandes | accès nominatif, journalisé |
| **Strictement confidentielle** | fuite = dommage grave ou irréversible | mots de passe, RIB, numéro de sécurité sociale, données de santé | accès exceptionnel, chiffrement, jamais exposée par une API |

Le critère n'est pas la « valeur » de la donnée mais le **dommage** causé par sa
divulgation — et la réglementation vient ensuite renforcer ce classement pour
les données personnelles (le RGPD est traité au chapitre suivant).

---

## II. Minimisation

La minimisation consiste à ne **renvoyer que les champs utiles** à la fonction exacte
de l'endpoint : sur un écran de planning, l'identifiant, le nom, le poste et la semaine
suffisent — pas le numéro de sécurité sociale, pas le hash du mot de passe.

La minimisation se prend à trois endroits :

| Endroit | Geste | Ce que ça retire |
| --- | --- | --- |
| **La requête** | nommer les colonnes au lieu de toutes les prendre | les champs qui n'ont rien à faire ici |
| **Le modèle de réponse** | déclarer un schéma de sortie explicite | les champs ajoutés « au cas où » par la suite |
| **Le code mort** | supprimer les anciens endpoints généreux | les vieilles portes qu'on croyait fermées |

---

## III. Masquage et pseudonymisation

Supprimer un champ n'est pas toujours possible : un écran de paie a besoin du
RIB pour afficher un virement, un support client a besoin d'un numéro de
téléphone pour rappeler. Deux outils permettent alors de **réduire ce qui
circule** sans perdre l'usage :

| Technique | Ce qu'elle fait | Exemple | Limite |
| --- | --- | --- | --- |
| **Masquage** | cache une partie de la valeur | `**** **** **** 4821` pour une carte bancaire | la valeur complète reste en base, accessible aux systèmes autorisés |
| **Pseudonymisation** | remplace l'identité par un identifiant stable, comme EMP (le code interne de l'employé) | `EMP-0042` au lieu du nom, dans un export d'analyse | le croisement avec une table de correspondance rétablit l'identité |
| **Anonymisation** | supprime la possibilité de ré-identification | un jeu de données agrégé par département | définitive — et donc irréversible pour les usages individuels |

Le choix se fait selon l'usage : si la donnée doit **revenir** à une personne
identifiable (support, paie), on masque ou on pseudonymise ; si elle ne sert
qu'à des statistiques, on anonymise. La pseudonymisation est un compromis
pratique — le RGPD la reconnaît comme une mesure de protection, **sans** la
confondre avec l'anonymisation.

> [!WARNING]
> Un pseudonyme n'est pas un anonymat. Un export « pseudonymisé » croisé avec
> l'annuaire interne redonne tout : traitez-le comme une donnée personnelle,
> avec les mêmes contrôles d'accès.

---

### Exercice 1 — Sécuriser un endpoint qui en dit trop (30 min)

#### Contexte

Un fournisseur d'énergie met à jour son portail client. L'écran « Échéancier de
paiement » affiche trois informations : le nom du client, ses prochaines
échéances et les montants dus. L'endpoint qui alimente cet écran a été écrit
pendant la refonte, « en reprenant la fiche client complète, comme ça on aura
tout ce qu'il faut ».

Voici ce que renvoie actuellement l'endpoint `/compte/{id}` :

```json
{
  "id": 4021,
  "numero_client": "CL-4021",
  "nom": "Camille Durand",
  "courriel": "c.durand@example.fr",
  "telephone": "0612345678",
  "adresse": "12 rue des Lilas, 34000 Montpellier",
  "rib": "FR7630006000011234567890189",
  "contrat": {
    "offre": "Tarif Vert",
    "puissance_souscrite": 9
  },
  "releves": [
    {"horodatage": "2026-04-13T00:00", "kwh": 1.2},
    {"horodatage": "2026-04-13T00:30", "kwh": 0.9}
  ],
  "historique_factures": [
    {"date": "2026-03-05", "montant": 84.10, "statut": "payée"},
    {"date": "2026-02-05", "montant": 91.30, "statut": "payée"}
  ]
}
```

Le fournisseur relève la consommation **toutes les 30 minutes** : la série
`releves` est donc longue, et elle décrit la vie quotidienne du logement
(quand la personne se lève, quand elle est absente). L'endpoint est appelé par
le portail web, mais aussi par une application partenaire d'aide à la gestion
de l'énergie.

---

#### Consignes

##### Partie 1 — Classifier les champs

Classez chaque champ de la réponse dans les quatre niveaux du chapitre.
Justifiez en une phrase les deux classements les plus élevés.

##### Partie 2 — Minimiser la réponse

Réécrivez la réponse de `GET /compte/{id}` pour qu'elle porte **exactement** ce
dont l'écran d'échéancier a besoin. Listez ensuite les champs retirés et, pour
chacun, l'usage qui justifierait — le cas échéant — un endpoint dédié.

##### Partie 3 — Masquer et pseudonymiser

L'application partenaire a besoin d'afficher « le RIB du prélèvement »
sans le montrer en entier, et d'analyser la consommation par profil sans que l'identité des clients
apparaisse. Décrivez le masquage du RIB et la pseudonymisation des
relevés : que devient chaque donnée, et que garde-t-on derrière ?

##### Partie 4 — Justifier au regard du RGPD

Pour la série `releves`, répondez aux trois questions : quelle est la
**finalité** de sa collecte, quelle **base légale** la justifie, et que
devient-elle quand le contrat est résilié ? Une réponse par question, une à
deux phrases chacune.

---

#### ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque champ de la réponse originale est **classé**, sans exception.
- [ ] Ma réponse minimisée ne contient **que** ce dont l'écran a besoin — j'ai
  vérifié champ par champ.
- [ ] Pour chaque champ retiré, j'ai dit **où il devrait vivre** (endpoint
  dédié, jamais nulle part).
- [ ] Mon masquage du RIB laisse **impossible** la lecture du numéro complet
  depuis la réponse.
- [ ] Ma partie RGPD nomme une **finalité**, une **base légale** et un **sort**
  de la donnée — pas seulement « c'est sensible ».

---

#### Pour aller plus loin

*Facultatif.* Le fournisseur veut proposer un service de « comparaison avec les
foyers similaires » à partir des relevés. Sans écrire de code, décrivez comment
produire ce service **sans** que les données individuelles de consommation
quittent le système.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Classifier les champs

**Éléments attendus :**

| Champ | Niveau | Pourquoi |
| --- | --- | --- |
| `id`, `numero_client` | interne | des identifiants opérationnels, sans danger immédiat, mais inutiles à diffuser |
| `nom` | confidentielle | une donnée personnelle, utile à l'écran, à ne pas exposer ailleurs |
| `courriel`, `telephone`, `adresse` | confidentielle | des coordonnées directes : leur fuite ouvre la voie au démarchage et à l'hameçonnage |
| `rib` | strictement confidentielle | un moyen de paiement : sa divulgation permet un prélèvement frauduleux |
| `contrat` | interne | des informations commerciales, gênantes si diffusées, sans gravité immédiate |
| `releves` | confidentielle | la consommation à 30 minutes près décrit les habitudes de vie du logement |
| `historique_factures` | confidentielle | des données financières personnelles |

**Les deux classements les plus élevés, justifiés :** le `rib` est strictement
confidentiel parce que sa divulgation cause un dommage **financier direct** et
immédiat ; les `releves` sont confidentiels parce qu'une série toutes les 30
minutes renseigne sur la présence et les habitudes du foyer — une fuite de ce
type a déjà servi à déterminer quand un logement est vide.

**Ce qu'il faut retenir :** le niveau ne se déduit pas du type technique
(chaîne, nombre) mais du **dommage** causé par la divulgation. Une série de
nombres anodins peut être plus sensible qu'un nom.

---

#### Partie 2 — Minimiser la réponse

**Éléments attendus :**

```json
{
  "nom": "Camille Durand",
  "echeances": [
    {"date": "…", "montant": …}
  ]
}
```

Les valeurs des échéances viennent de la facturation ; la forme de la réponse,
elle, ne porte plus rien d'autre que l'écran n'affiche.

| Champ retiré | Où il devrait vivre |
| --- | --- |
| `id`, `numero_client` | nulle part dans une réponse client ; un endpoint interne de gestion, si besoin |
| `courriel`, `telephone`, `adresse` | un endpoint « mes coordonnées », appelé par l'écran qui les affiche |
| `rib` | un endpoint « mes moyens de paiement », avec masquage systématique |
| `contrat` | un endpoint « mon contrat » |
| `releves` | un endpoint « ma consommation », paginé, réservé à l'écran qui les trace |
| `historique_factures` | un endpoint « mes factures » |

**Erreurs fréquentes :** garder `id` et `numero_client` « au cas où » — ils ne
servent à l'écran que s'il les affiche ; ou vider la réponse de ses champs
sensibles mais garder `releves` complet, ce qui laisse la série la plus
bavarde dans la réponse.

**Sur la minimisation :** la question n'est pas « ce champ est-il dangereux ? »
mais « **cet écran en a-t-il besoin ?** ». Un endpoint par usage donne des
réponses minimales **et** des surfaces d'attaque séparées.

---

#### Partie 3 — Masquer et pseudonymiser

**Éléments attendus :**

| Donnée | Traitement | Ce qui reste visible | Ce qui reste derrière |
| --- | --- | --- | --- |
| `rib` | masquage | `**** **** **** 0189` (les derniers caractères seulement) | le RIB (relevé d'identité bancaire) complet en base, accessible au seul
module de prélèvement |
| `releves` | pseudonymisation | FOYER (code interne du foyer), comme `FOYER-4021`, à la place du nom et du
numéro client | la table de correspondance `FOYER-4021` → client, dans un espace restreint |

**Points de vigilance :** masquer le RIB côté **réponse** ne suffit pas si le
module qui construit la réponse lit le RIB complet — le masquage se fait au
plus près de la source. Et la table de correspondance de la pseudonymisation
est elle-même une donnée personnelle : si l'application partenaire l'obtient,
la pseudonymisation ne protège plus rien.

**Sur les deux techniques :** masquer protège **l'affichage**, pseudonymiser
protège **l'analyse**. Les deux laissent la donnée exister — c'est le
compromis assumé quand l'usage exige de revenir à la personne.

---

#### Partie 4 — Justifier au regard du RGPD

**Éléments attendus :**

| Question | Réponse attendue |
| --- | --- |
| **Finalité** | facturer la consommation réelle et permettre au client de suivre son usage — pas « améliorer nos services » en général |
| **Base légale** | l'exécution du contrat de fourniture d'énergie (la donnée sert à établir la facture) |
| **Sort après résiliation** | effacement ou archivage restreint selon l'obligation légale de conservation des factures ; la série détaillée des relevés, elle, n'a plus de finalité et disparaît |

**Erreurs fréquentes :** invoquer le consentement pour une donnée nécessaire à
la facturation — le consentement serait révocable, et la facturation ne l'est
pas ; ou répondre « on la garde 10 ans » sans distinguer la **facture** (retenue
par une obligation comptable) du **relevé détaillé** (sans objet une fois le
contrat clos).

**Sur la base légale :** elle se choisit **avant** de collecter, et elle
décide de la suite — notamment de ce qui se passe quand la personne part. Une
finalité floue produit toujours la même réponse : « on garde, au cas où ».

---

#### Points à retenir

- Classifier, c'est juger le **dommage** de la divulgation — une série de
  mesures peut être plus sensible qu'un nom.
- Minimiser, c'est répondre à « **cet écran en a-t-il besoin ?** » — et donner
  un endpoint dédié à chaque usage qui, lui, en a besoin.
- Masquer protège l'affichage, pseudonymiser protège l'analyse — et la table de
  correspondance reste une donnée personnelle.
- La base légale se choisit avant la collecte : elle décide du **sort** de la
  donnée quand le contrat s'arrête.

</details>

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **Le chiffrement applicatif des colonnes sensibles** — chiffrer une colonne au
  niveau du code applicatif (la base ne voit que du chiffré) protège contre une
  fuite de sauvegarde ou un accès direct à la base. Les primitives et leurs
  usages sont détaillés dans la journée consacrée à la cryptographie.
- **Les vues SQL et les procédures stockées** — exposer une vue qui ne contient
  que les colonnes utiles, plutôt que la table brute : la minimisation devient
  alors une propriété de la base, pas seulement de l'application.
- **La traçabilité des accès** — journaliser qui a lu une donnée sensible, quand
  et pourquoi. Une donnée confidentielle sans journal d'accès est une donnée
  qu'on ne saura pas avoir été lue.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> Classer ces colonnes est exactement la Partie 1 de l'exercice 1 de ce chapitre, plus haut, sur un autre jeu de données.
>
> 🧪 **Atelier rapide (8 min)**
>
> Voici le schéma simplifié de la base d'un SaaS de gestion RH. Classez chaque
> colonne dans les quatre niveaux ci-dessus :
>
> ```sql
> CREATE TABLE employes (
>     id INT PRIMARY KEY,
>     nom VARCHAR(64),              -- niveau : ?
>     email VARCHAR(254),           -- niveau : ?
>     poste VARCHAR(64),            -- niveau : ?
>     salaire DECIMAL(8, 2),        -- niveau : ?
>     numero_secu CHAR(15),         -- niveau : ?
>     mot_de_passe_hash CHAR(60)    -- niveau : ?
> );
>
> CREATE TABLE formations (
>     id INT PRIMARY KEY,
>     employe_id INT,
>     intitule VARCHAR(128),        -- niveau : ?
>     date_session DATE             -- niveau : ?
> );
> ```
>
> Notez votre classement : deux colonnes reviendront dans l'exercice du bloc. La
> question utile pour chacune est : « si cette valeur apparaissait dans un journal
> d'application lu par toute l'équipe, que se passerait-il ? »

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Le même endpoint, avant et après minimisation**
>
> L'exercice 1 de ce chapitre, plus haut, fait parcourir ce chemin, sur une réponse tout aussi bavarde.
>
> La minimisation consiste à ne **renvoyer que les champs utiles** à la fonction
> exacte de l'endpoint. Le contraste se lit dans deux réponses du même endpoint GET (lecture d'une
> ressource), `/planning/{id}` :
>
> ```json
> // Avant : la requête SQL faisait un SELECT * et tout partait dans la réponse
> {
>   "id": 42,
>   "nom": "Durand",
>   "email": "c.durand@example.fr",
>   "salaire": 3200.00,
>   "numero_secu": "2850376123456 78",
>   "mot_de_passe_hash": "$2b$12$...",
>   "semaine": "2026-04-13"
> }
> ```
>
> ```json
> // Après : la réponse porte ce dont l'écran de planning a besoin, rien d'autre
> {
>   "id": 42,
>   "nom": "Durand",
>   "poste": "technicienne support",
>   "semaine": "2026-04-13"
> }
> ```

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Deux SELECT, deux intentions**
>
> Le tableau ci-dessus énonce le geste ; ces deux lignes ne font que le montrer.
>
> ```sql
> SELECT * FROM employes;            -- prend tout, y compris le superflu
> SELECT nom, poste FROM employes;   -- prend l'utile
> ```

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Retirer de la réponse, pas forcément de la base**
>
> Nuance utile en revue de code, jamais exigée pour faire l'exercice.
>
> Un champ retiré de la réponse n'a pas besoin d'être retiré de la base : c'est
> l'**exposition** qui compte. Mais un champ que personne n'utilise plus mérite
> d'être retiré des deux côtés — il coûte de l'espace et de la surface
> d'attaque.

---

## Points clés

- Classifier avant de protéger : **publique, interne, confidentielle, strictement
  confidentielle** — le critère est le dommage causé par la divulgation.
- La minimisation se joue à trois endroits : la **requête**, le **modèle de
  réponse**, le **code mort**. Un champ qui ne sert à rien ne doit pas sortir.
- Masquer, pseudonymiser, anonymiser répondent à trois usages différents — et
  un pseudonyme **reste** une donnée personnelle.
- La question de départ, à poser pour chaque endpoint : « **pourquoi** ce champ
  est-il dans cette réponse ? »

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Sur quoi se base la classification d'une donnée en quatre niveaux de sensibilité ?

- A. Sur la « valeur » commerciale de la donnée
- B. Sur le dommage causé par sa divulgation
- C. Sur la taille du colonne qui la stocke
- D. Sur le chiffre d'affaires du service qui la détient

**2.** La fiche d'un salarié renvoie son numéro de sécurité sociale et son RIB dans une réponse destinée à un simple affichage de planning. À quel niveau appartiennent ces champs, et quelle est la règle par défaut ?

- A. Interne : accès restreint au périmètre de l'entreprise, sans précaution supplémentaire
- B. Confidentielle : accès nominatif et journalisé, comme on le fait pour les fiches de paie
- C. Strictement confidentielle : accès exceptionnel, chiffrement, jamais exposée par une API
- D. Publique : ces valeurs circulent déjà entre les services, elles ne méritent donc aucun verrou

**3.** La minimisation de la réponse d'un endpoint se décide à trois endroits. Lesquels ?

- A. La requête (nommer les colonnes), le modèle de réponse (schéma de sortie explicite), le code mort (supprimer les anciens endpoints généreux)
- B. Le pare-feu applicatif, le chiffrement des flux entre services, la sauvegarde chiffrée côté exploitation
- C. Les en-têtes de réponse HTTP, la pagination des collections, la compression des corps envoyés au client
- D. La politique de mots de passe, la double authentification des comptes, la durée de vie des sessions ouvertes

**4.** Un export « pseudonymisé » (des codes comme `EMP-0042` au lieu des noms) est croisé avec l'annuaire interne. Que se passe-t-il ?

- A. Rien : une fois pseudonymisée, la donnée ne se rattache plus à une personne et devient libre d'usage
- B. Le croisement rétablit l'identité : le pseudonyme reste une donnée personnelle, à traiter avec les mêmes contrôles d'accès
- C. La donnée devient publique, puisqu'elle n'est plus rattachée à un nom directement lisible
- D. Le croisement ne concerne que les données restées en base, jamais les exports partis chez un destinataire

**5.** *Question ouverte (2-3 lignes).* Masquer, pseudonymiser, anonymiser : donnez pour chacune technique un usage qui la désigne, et expliquez pourquoi l'anonymisation est le choix irréversible.

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. B.** Le critère n'est pas la « valeur » de la donnée mais le dommage causé par sa divulgation — la réglementation vient ensuite renforcer ce classement pour les données personnelles.
**Pourquoi :** classer avant de protéger répond à « ce que l'on détient » ; la question utile est : si cette valeur apparaissait dans un journal lu par toute l'équipe, que se passerait-il ?

**2. C.** Mot de passe, RIB, numéro de sécurité sociale, données de santé : fuite = dommage grave ou irréversible, donc accès exceptionnel, chiffrement, jamais exposée par une API.
**Pourquoi :** ici la base ne fuit pas — c'est l'endpoint qui donne trop ; le meilleur moyen de protéger une donnée est souvent de ne pas la renvoyer.

**3. A.** Nommer les colonnes dans la requête, déclarer un schéma de sortie explicite, supprimer les anciens endpoints généreux.
**Pourquoi :** chaque geste retire une catégorie de champs surnuméraires — ceux qui n'ont rien à faire là, ceux ajoutés « au cas où », et les vieilles portes qu'on croyait fermées.

**4. B.** Un pseudonyme n'est pas un anonymat : le croisement avec une table de correspondance (l'annuaire) rétablit tout.
**Pourquoi :** la pseudonymisation est un compromis pratique — reconnue comme mesure de protection, mais sans être confondue avec l'anonymisation ; l'export pseudonymisé se traite comme une donnée personnelle.

**5.** Attendu : le masquage cache une partie de la valeur quand l'usage exige la forme (un écran de paie affiche `**** **** **** 4821`) ; la pseudonymisation remplace l'identité par un identifiant stable quand la donnée doit revenir à une personne identifiable (support, paie) ; l'anonymisation convient quand la donnée ne sert qu'à des statistiques.
**Pourquoi :** l'anonymisation supprime la possibilité de ré-identification — elle est définitive, donc irréversible pour les usages individuels.

</details>

---

[← Chapitre précédent](08-auth-et-limitation-api.md) · [Sommaire](Readme.md) · [Chapitre suivant →](10-rgpd-applique.md)
