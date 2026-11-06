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
> Classer ces colonnes est exactement la Partie 1 de l'exercice [Sécuriser un endpoint qui en dit trop](tp/09-securiser-endpoint-data.md), sur un autre jeu de données.
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
> L'exercice [Sécuriser un endpoint qui en dit trop](tp/09-securiser-endpoint-data.md) fait parcourir ce chemin, sur une réponse tout aussi bavarde.
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

*Formatif, jamais noté. Répondez sans relire le chapitre, puis cochez. Les réponses sont juste après le séparateur : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Sur quoi se base la classification d'une donnée en quatre niveaux de sensibilité ?

- A. Sur la « valeur » commerciale de la donnée
- B. Sur le dommage causé par sa divulgation
- C. Sur la taille du colonne qui la stocke
- D. Sur le chiffre d'affaires du service qui la détient

- [ ] ✓ je savais

**2.** La fiche d'un salarié renvoie son numéro de sécurité sociale et son RIB dans une réponse destinée à un simple affichage de planning. À quel niveau appartiennent ces champs, et quelle est la règle par défaut ?

- A. Interne : restreindre au périmètre de l'entreprise
- B. Confidentielle : accès nominatif, journalisé
- C. Strictement confidentielle : accès exceptionnel, chiffrement, jamais exposée par une API
- D. Publique : ces valeurs circulent déjà entre services

- [ ] ✓ je savais

**3.** La minimisation de la réponse d'un endpoint se décide à trois endroits. Lesquels ?

- A. La requête (nommer les colonnes), le modèle de réponse (schéma de sortie explicite), le code mort (supprimer les anciens endpoints généreux)
- B. Le pare-feu, le chiffrement des flux, la sauvegarde chiffrée
- C. Les en-têtes de réponse, la pagination, la compression
- D. La politique de mots de passe, la double authentification, la durée de session

- [ ] ✓ je savais

**4.** Un export « pseudonymisé » (des codes comme `EMP-0042` au lieu des noms) est croisé avec l'annuaire interne. Que se passe-t-il ?

- A. Rien : la pseudonymisation rend la donnée définitivement non personnelle
- B. Le croisement rétablit l'identité : le pseudonyme reste une donnée personnelle, à traiter avec les mêmes contrôles d'accès
- C. La donnée devient publique, n'étant plus rattachée à un nom
- D. Le croisement ne concerne que les données en base, jamais les exports

- [ ] ✓ je savais

**5.** *Question ouverte (2-3 lignes).* Masquer, pseudonymiser, anonymiser : donnez pour chacune technique un usage qui la désigne, et expliquez pourquoi l'anonymisation est le choix irréversible.

- [ ] ✓ je savais

---

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

---

[← Chapitre précédent](08-auth-et-limitation-api.md) · [Sommaire](Readme.md) · [Chapitre suivant →](10-rgpd-applique.md)
