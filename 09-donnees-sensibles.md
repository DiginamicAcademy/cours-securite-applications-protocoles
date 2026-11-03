[← Chapitre précédent](08-auth-et-limitation-api.md) · [Sommaire](Readme.md) · [Chapitre suivant →](10-rgpd-applique.md)

# Données sensibles — classer, minimiser, masquer

> Un éditeur de logiciel de gestion RH découvre, en revoyant son API de paie,
> que la fiche d'un salarié renvoie son numéro de sécurité sociale, son RIB (relevé d'identité bancaire)
> et son salaire — dans une réponse destinée à un simple affichage de planning. La
> base ne fuit pas : c'est l'**endpoint** qui donne trop. Le meilleur moyen de
> protéger une donnée, c'est souvent de ne pas la renvoyer.

**Durée de lecture :** 65 min · **Prérequis :** les chapitres [Sécurité des
API](07-securite-api.md) et [Auth et limitation d'API](08-auth-et-limitation-api.md)

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

> 🧪 **Atelier rapide (8 min)**
>
> Voici le schéma simplifié de la base d'un SaaS de gestion RH. Classez chaque
> colonne dans les quatre niveaux ci-dessus :

```sql
CREATE TABLE employes (
    id INT PRIMARY KEY,
    nom VARCHAR(64),              -- niveau : ?
    email VARCHAR(254),           -- niveau : ?
    poste VARCHAR(64),            -- niveau : ?
    salaire DECIMAL(8, 2),        -- niveau : ?
    numero_secu CHAR(15),         -- niveau : ?
    mot_de_passe_hash CHAR(60)    -- niveau : ?
);

CREATE TABLE formations (
    id INT PRIMARY KEY,
    employe_id INT,
    intitule VARCHAR(128),        -- niveau : ?
    date_session DATE             -- niveau : ?
);
```

Notez votre classement : deux colonnes reviendront dans l'exercice du bloc. La
question utile pour chacune est : « si cette valeur apparaissait dans un journal
d'application lu par toute l'équipe, que se passerait-il ? »

---

## II. Minimisation

La minimisation consiste à ne **renvoyer que les champs utiles** à la fonction
exacte de l'endpoint. Le contraste se lit dans deux réponses du même endpoint GET (lecture d'une
ressource), `/planning/{id}` :

```json
// Avant : la requête SQL faisait un SELECT * et tout partait dans la réponse
{
  "id": 42,
  "nom": "Durand",
  "email": "c.durand@example.fr",
  "salaire": 3200.00,
  "numero_secu": "2850376123456 78",
  "mot_de_passe_hash": "$2b$12$...",
  "semaine": "2026-04-13"
}
```

```json
// Après : la réponse porte ce dont l'écran de planning a besoin, rien d'autre
{
  "id": 42,
  "nom": "Durand",
  "poste": "technicienne support",
  "semaine": "2026-04-13"
}
```

La minimisation se prend à trois endroits :

| Endroit | Geste | Ce que ça retire |
| --- | --- | --- |
| **La requête** | nommer les colonnes au lieu de toutes les prendre | les champs qui n'ont rien à faire ici |
| **Le modèle de réponse** | déclarer un schéma de sortie explicite | les champs ajoutés « au cas où » par la suite |
| **Le code mort** | supprimer les anciens endpoints généreux | les vieilles portes qu'on croyait fermées |

```sql
SELECT * FROM employes;            -- prend tout, y compris le superflu
SELECT nom, poste FROM employes;   -- prend l'utile
```

> [!TIP]
> Un champ retiré de la réponse n'a pas besoin d'être retiré de la base : c'est
> l'**exposition** qui compte. Mais un champ que personne n'utilise plus mérite
> d'être retiré des deux côtés — il coûte de l'espace et de la surface
> d'attaque.

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

[← Chapitre précédent](08-auth-et-limitation-api.md) · [Sommaire](Readme.md) · [Chapitre suivant →](10-rgpd-applique.md)
