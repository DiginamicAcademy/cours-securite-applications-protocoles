# Validation et injections — séparer les données des instructions

> Sur la plateforme de suivi de colis d'une PME (petite et moyenne entreprise)
> de logistique, le champ de
> recherche interroge directement la base. Une saisie anodine renvoie la liste
> complète des expéditions en cours. La correction tient en une ligne : passer
> d'une chaîne assemblée à une requête paramétrée. Mais pour savoir qu'il
> fallait la changer, il faut d'abord avoir compris ce qui, dans la requête,
> faisait office de **donnée** et ce qui faisait office d'**instruction**.

**Durée de lecture :** 75 min · **Prérequis :** les injections étudiées lors des
journées précédentes, et le chapitre
[Principes du secure coding](01-principes-secure-coding.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Séparer** les données des instructions dans une requête, en remplaçant une
  concaténation par une requête paramétrée.
- **Contrôler** une saisie avant usage : type, format attendu, longueur maximale.
- **Arbitrer** entre requête paramétrée, ORM et validation d'entrée, selon ce que
  le code doit réellement faire.
- **Refuser** proprement une valeur hors format, au lieu de la réparer en
  silence.

---

## I. Requêtes paramétrées

Le principe tient en une phrase : **les données ne doivent jamais devenir des
instructions**. Un moteur de base de données reçoit une chaîne et l'exécute ; il
ne devine pas que la moitié venait du développeur et l'autre moitié d'un champ
de formulaire. Quand les deux sont collées ensemble, tout est instruction.

La requête paramétrée demande au moteur de faire cette distinction lui-même. On
écrit la requête avec des **emplacements**, puis on envoie les valeurs à part :

```python
# avant : la saisie est collée dans la requête
query = f"SELECT * FROM products WHERE name LIKE '%{q}%'"
cursor.execute(query)

# après : la saisie voyage à part, le moteur sait que c'est une donnée
cursor.execute(
    "SELECT * FROM products WHERE name LIKE %s",
    (f"%{q}%",),
)
```

Le `%s` n'est pas une valeur : c'est un **emplacement**. Le pilote de base de
données envoie la structure de la requête, puis les valeurs, et le moteur
assemble les deux sans jamais les confondre. Une valeur ne peut donc pas
devenir une instruction, même si elle en a exactement l'apparence.

| | Avant | Après |
| --- | --- | --- |
| **Ce que voit le moteur** | une seule chaîne à exécuter | une structure, puis des valeurs |
| **Ce que peut la saisie** | modifier le sens de la requête | remplir un emplacement, rien de plus |
| **Ce qu'on écrit** | une f-string, un `+`, un format | un marqueur et un tuple de valeurs |

> ⚠️ **Piège** — Échapper les guillemets à la main, doubler les apostrophes ou
> entourer les
> valeurs de quotes — revient à réparer le symptôme. Le jour où un cas n'a pas
> été prévu, la requête redevient injectable. La séparation se fait avec le
> pilote, pas avec des remplacements de caractères.

> 🧪 **Atelier rapide (10 min)**
>
> Dans le lab du cours, ouvrez `lab/vulnerable/app.py` et repérez la route de
> recherche de produits : la requête y est assemblée par une f-string.
> Remplacez-la par une requête paramétrée, redémarrez le service, puis relancez
> la même recherche avec la valeur `' OR '1'='1`. La liste complète ne revient
> plus : seule la recherche littérale reste, et la comparaison avec
> `lab/secure/app.py` montre le même résultat.

Ce geste est la correction la plus fréquente du secure coding. Il est court
précisément parce que tout le travail a été fait en amont : reconnaître qu'une
valeur utilisateur arrivait dans une instruction.

---

## II. Validation en entrée

La requête paramétrée protège la base. Elle ne dit rien de la **valeur** elle-même : une date au format inattendu, un identifiant de 4 000 caractères ou un
mot de recherche vide restent des surprises pour le reste du programme. La
validation d'entrée les traite avant qu'ils n'arrivent nulle part.

Trois contrôles suffisent dans la grande majorité des cas :

| Contrôle | Ce qu'on vérifie | Exemple de refus |
| --- | --- | --- |
| **Type** | la valeur est bien un entier, une date, une chaîne | `abc` pour un identifiant numérique |
| **Format** | la valeur suit le motif attendu | une adresse électronique sans arobase |
| **Longueur** | la valeur tient dans ce que le reste du code prévoit | un champ de recherche de plusieurs milliers de caractères |

Le format se vérifie avec une expression régulière, et surtout avec
`re.fullmatch` plutôt qu'avec `re.match` : le motif doit couvrir **toute** la
valeur, pas seulement son début.

```python
import re

def valider_recherche(q):
    if len(q) > 64:
        return None            # trop long : refusé
    if not re.fullmatch(r"[\w\s\-']*", q or ""):
        return None            # caractère hors motif : refusé
    return q
```

Le `fullmatch` est le détail qui change tout : `re.match(r"[\w\s\-']*", q)`
accepterait `bonjour` suivi de n'importe quoi, puisqu'il ne regarde que le
commencement.

> ⚠️ **Attention** — Valider n'est pas **nettoyer**. Supprimer les caractères
> interdits et laisser
> passer le reste fabrique des valeurs que personne n'a jamais testées. Une
> valeur hors format est refusée, avec un message qui dit pourquoi — c'est le
> fail-closed du chapitre précédent, appliqué à la saisie.

La longueur maximale mérite un mot : elle n'est pas un détail de confort. Un
champ de recherche borné limite la surface de ce qui peut arriver jusqu'à la
base, jusqu'aux journaux et jusqu'à l'écran. Elle se décide une fois, dans le
code, et se retrouve partout où la valeur circule.

---

## III. ORM

Un ORM (Object-Relational Mapping) construit les requêtes à partir d'objets : le
développeur décrit ce qu'il veut lire ou écrire, la bibliothèque assemble la
requête et y place les valeurs. Dans le cas courant, il apporte donc la même
séparation qu'une requête paramétrée — sans qu'on ait à y penser.

```python
# avec un ORM : la valeur est un filtre, pas un morceau de requête
produits = session.query(Produit).filter(Produit.nom.ilike(f"%{q}%")).all()
```

L'ORM aide donc beaucoup, mais il ne **remplace** pas la réflexion. Trois
situations le contournent :

| Situation | Pourquoi ça échappe |
| --- | --- |
| **Requête écrite à la main** | la chaîne redevient une instruction, l'ORM ne la voit pas |
| **Tri ou filtre dynamique** | un nom de colonne vient de la saisie, et un nom de colonne n'est pas une valeur |
| **Motif de recherche** | le caractère générique reste dans la valeur : il faut le borner soi-même |

```python
# dangereux : le nom de colonne vient de la saisie
session.execute(text(f"SELECT * FROM produits ORDER BY {tri}"))

# sûr : la valeur choisie dans une liste fermée
COLONNES = {"nom": Produit.nom, "prix": Produit.prix}
if tri not in COLONNES:
    raise ValueError("tri inconnu")
```

> 💡 **À retenir**
> La règle de décision est simple : dès qu'une saisie influence **la forme** de
> la requête — un nom de table, un nom de colonne, un opérateur — elle ne peut
> pas voyager en valeur. On la remplace par un choix dans une liste fermée,
> décidée par le code.

C'est le même réflexe que pour les en-têtes de réponse ou les chemins de
fichiers : ce qui structure reste du code, ce qui remplit reste de la donnée.

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **Les requêtes préparées en profondeur** — sur MySQL, une requête préparée
  passe par deux temps : le moteur analyse et optimise la structure, puis il
  l'exécute avec les valeurs fournies. Le plan d'exécution est calculé une fois
  et réutilisé : la séparation de sécurité vient donc avec un gain de
  performance quand la même requête tourne souvent.
- **Ce que les paramètres ne couvrent pas** — les noms de tables et de colonnes
  ne sont pas des valeurs : aucun pilote ne les accepte en paramètre. Ils se
  valident contre une liste fermée, décidée par le code.
- **La validation côté client** — une contrainte de formulaire dans une page web
  améliore le confort, pas la sécurité : elle se contourne en une requête. Tout
  ce qui compte se vérifie côté serveur.

---

## Points clés

- Une requête paramétrée **sépare les données des instructions** : la saisie
  remplit un emplacement, elle ne peut pas changer le sens de la requête.
- Échapper les guillemets à la main ne remplace jamais cette séparation.
- La validation d'entrée porte sur **trois choses** : le type, le format et la
  longueur maximale — et elle refuse, elle ne répare pas.
- Un ORM sécurise le cas courant ; dès qu'une saisie influence la **forme** de la
  requête, on revient à une liste fermée de valeurs autorisées.
