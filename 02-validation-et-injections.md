[← Chapitre précédent](01-principes-secure-coding.md) · [Sommaire](Readme.md) · [Chapitre suivant →](03-xss-et-sorties.md)

# Validation et injections — séparer les données des instructions

> Sur la plateforme de suivi de colis d'une PME (petite et moyenne entreprise)
> de logistique, le champ de
> recherche interroge directement la base. Une saisie anodine renvoie la liste
> complète des expéditions en cours. La correction tient en une ligne : passer
> d'une chaîne assemblée à une requête paramétrée. Mais pour savoir qu'il
> fallait la changer, il faut d'abord avoir compris ce qui, dans la requête,
> faisait office de **donnée** et ce qui faisait office d'**instruction**.

**Durée de lecture :** 50 min hors approfondissements facultatifs · **Prérequis :** les injections étudiées lors des
journées précédentes, et le chapitre
[Principes du secure coding](01-principes-secure-coding.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Séparer** les données des instructions dans une requête, en remplaçant une
  concaténation par une requête paramétrée.
- **Contrôler** une saisie avant usage : type, format attendu, longueur maximale.
- **Arbitrer** entre requête paramétrée, ORM et validation d'entrée, selon ce que
  le code doit réellement faire — l'exposé de l'ORM est en approfondissement.
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

`re.match(r"[\w\s\-']*", q)` accepterait `bonjour` suivi de n'importe quoi :
il ne regarde que le commencement.

> ⚠️ **Attention** — Valider n'est pas **nettoyer**. Supprimer les caractères
> interdits et laisser
> passer le reste fabrique des valeurs que personne n'a jamais testées. Une
> valeur hors format est refusée, avec un message qui dit pourquoi — c'est le
> fail-closed du chapitre précédent, appliqué à la saisie.

La longueur maximale se décide une fois, dans le code, et se retrouve
partout où la valeur circule : elle borne la surface de ce qui peut
atteindre la base, les journaux et l'écran.

---

## III. ORM

Un ORM (Object-Relational Mapping) construit les requêtes à partir d'objets
et apporte, dans le cas courant, la même séparation qu'une requête
paramétrée. Les trois situations où une saisie lui échappe, et l'exemple du
nom de colonne, sont développés en « Aller plus loin ».

> 💡 **À retenir**
> La règle de décision est simple : dès qu'une saisie influence **la forme** de
> la requête — un nom de table, un nom de colonne, un opérateur — elle ne peut
> pas voyager en valeur. On la remplace par un choix dans une liste fermée,
> décidée par le code.

C'est le même réflexe que pour les en-têtes de réponse ou les chemins de
fichiers : ce qui structure reste du code, ce qui remplit reste de la donnée.

---

### Exercice 1 — Corriger une injection dans une recherche (20 min)

#### Contexte

Le complexe sportif municipal de votre commune met à disposition un portail de
réservation de créneaux. La recherche de séances est arrivée dans une version
expresse, écrite pour la démonstration du conseil d'administration. Elle
fonctionne — et, en jouant avec le champ de recherche, un agent de la piscine a
obtenu la liste complète des séances, y compris celles qui ne sont pas ouvertes
au public.

Voici la route concernée :

```python
@app.get("/seances/search")
def search_seances(q: str = ""):
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM seances WHERE titre LIKE '%{q}%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return {"query": q, "results": rows}
```

Le service doit rester simple : une recherche par titre, une réponse au format
JSON (JavaScript Object Notation). La règle fixée par la commune est la
suivante : une saisie invalide est **refusée**, jamais réparée en silence, et le
refus est explicite.

---

#### Consignes

##### Partie 1 — Distinguer les instructions des données

Reprenez la chaîne de la requête et délimitez, à la main, ce qui appartient au
langage de requête et ce qui appartient à la saisie. Expliquez, en deux phrases,
pourquoi une valeur de recherche peut modifier le **sens** de la requête plutôt
que de seulement remplir un emplacement.

##### Partie 2 — Réécrire la requête

Réécrivez la route avec une requête paramétrée. La recherche doit rester
identique pour une saisie normale : même résultat sur un titre existant, aucun
changement de comportement visible.

##### Partie 3 — Contrôler la saisie

Ajoutez le contrôle d'entrée en amont de la requête :

- la valeur est une chaîne, et sa longueur maximale est de **64** caractères ;
- elle ne contient que des lettres, des chiffres, des espaces, des apostrophes ou
  des tirets ;
- toute valeur hors de ces critères est refusée avec le code **400**, et un
  message qui dit ce qui n'allait pas.

##### Partie 4 — Vérifier le comportement

Rejouez la recherche avec la valeur `' OR '1'='1`, puis avec une chaîne de
plusieurs centaines de caractères, puis avec une valeur normale. Notez, pour
chacune, ce que renvoie le service.

---

#### ✅ Auto-évaluation

- [ ] Je sais nommer, dans une requête, ce qui relève de l'instruction et ce qui
      relève de la donnée.
- [ ] Ma route utilise une requête paramétrée, sans concaténation de la saisie.
- [ ] La longueur maximale de 64 caractères est contrôlée avant la requête.
- [ ] Le format de la saisie est vérifié sur toute la valeur, pas seulement sur
      son début.
- [ ] Une saisie invalide renvoie le code 400 avec un message explicite.
- [ ] J'ai vérifié les trois cas de la partie 4 et noté les résultats.

---

#### Prolongement de l'exercice

*Facultatif — ne bloque pas la suite du parcours.*

Le champ de recherche accepte aussi un paramètre de tri, qui choisit la colonne
de classement. Proposez une façon de l'implémenter sans qu'une saisie puisse
choisir le nom de la colonne, et justifiez votre choix en une phrase.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Distinguer les instructions des données

La chaîne de la requête contient trois zones de nature différente :

| Zone | Exemple | Nature |
| --- | --- | --- |
| **Le vocabulaire de la requête** | les mots de sélection et de filtrage | instruction, écrite par le développeur |
| **La structure de la condition** | le motif de recherche, avec ses signes | instruction |
| **La valeur recherchée** | ce que la personne a tapé | donnée |

Le problème vient de la troisième zone : collée dans la chaîne, elle est relue
par le moteur comme faisant partie de la première. Une valeur qui contient un
signe de fin de condition termine la condition prématurément, et ce qui suit est
exécuté comme instruction. La saisie ne remplit plus un emplacement : elle
modifie le sens de la requête.

---

#### Partie 2 — Réécrire la requête

La réécriture remplace la concaténation par un emplacement, et passe la valeur
à part :

```python
@app.get("/seances/search")
def search_seances(q: str = ""):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM seances WHERE titre LIKE %s",
        (f"%{q}%",),
    )
    rows = cursor.fetchall()
    conn.close()
    return {"query": q, "results": rows}
```

Le résultat est identique pour une saisie normale : le moteur reçoit la même
structure, et la valeur ne peut plus en faire partie. Le signe générique du
motif reste dans la valeur, où il a sa place — c'est un caractère de recherche,
pas un morceau de requête.

---

#### Partie 3 — Contrôler la saisie

Le contrôle se pose en amont, avant la requête :

```python
import re

MOTIF = re.compile(r"[\w\s\-']*")


def valider_recherche(q):
    if len(q) > 64:
        return None
    if not MOTIF.fullmatch(q or ""):
        return None
    return q
```

Puis la route refuse explicitement :

```python
@app.get("/seances/search")
def search_seances(q: str = ""):
    if valider_recherche(q) is None:
        raise HTTPException(status_code=400,
                            detail="recherche invalide : longueur ou "
                                   "caractères non acceptés")
    ...
```

Deux points méritent l'attention. Le `fullmatch` porte sur toute la valeur : un
`match` simple accepterait un début valide suivi de n'importe quoi. Et le refus
est explicite — la valeur n'est pas nettoyée puis acceptée, elle est refusée,
avec un message qui dit ce qui n'allait pas.

---

#### Partie 4 — Vérifier le comportement

| Saisie | Comportement attendu |
| --- | --- |
| **La valeur piégée** | elle est traitée comme une recherche littérale : aucun résultat, ou un résultat contenant réellement ces caractères |
| **La chaîne très longue** | refusée avec le code 400, avant toute requête |
| **Une valeur normale** | résultat inchangé par rapport à la version initiale |

Le premier cas est le plus instructif : la valeur ne casse plus rien parce
qu'elle n'est plus une instruction. Elle ne « passe pas » — elle ne veut plus
rien dire pour le moteur.

---

#### Points à retenir

- La séparation des données et des instructions se fait avec le pilote de base
  de données, pas avec des remplacements de caractères.
- Le contrôle d'entrée porte sur la longueur et le format, et **refuse** plutôt
  que de réparer.
- Le `fullmatch` vérifie toute la valeur ; un `match` simple ne vérifie que le
  début.
- Vérifier les trois cas — piégé, trop long, normal — montre que la correction
  ne change rien au fonctionnement attendu.

</details>

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

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> Le réflexe à appliquer reste celui de l'encadré « À retenir », ci-dessous.
>
> Un ORM (Object-Relational Mapping) construit les requêtes à partir d'objets : le
> développeur décrit ce qu'il veut lire ou écrire, la bibliothèque assemble la
> requête et y place les valeurs. Dans le cas courant, il apporte donc la même
> séparation qu'une requête paramétrée — sans qu'on ait à y penser.
>
> ```python
> # avec un ORM : la valeur est un filtre, pas un morceau de requête
> produits = session.query(Produit).filter(Produit.nom.ilike(f"%{q}%")).all()
> ```
>
> L'ORM aide donc beaucoup, mais il ne **remplace** pas la réflexion. Trois
> situations le contournent :
>
> | Situation | Pourquoi ça échappe |
> | --- | --- |
> | **Requête écrite à la main** | la chaîne redevient une instruction, l'ORM ne la voit pas |
> | **Tri ou filtre dynamique** | un nom de colonne vient de la saisie, et un nom de colonne n'est pas une valeur |
> | **Motif de recherche** | le caractère générique reste dans la valeur : il faut le borner soi-même |
>
> ```python
> # dangereux : le nom de colonne vient de la saisie
> session.execute(text(f"SELECT * FROM produits ORDER BY {tri}"))
>
> # sûr : la valeur choisie dans une liste fermée
> COLONNES = {"nom": Produit.nom, "prix": Produit.prix}
> if tri not in COLONNES:
>     raise ValueError("tri inconnu")
> ```

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> La même correction est conduite de bout en bout dans
> l'exercice 1 de ce chapitre, plus haut.
>
> 🧪 **Atelier rapide (10 min)**
>
> Dans le lab du cours, ouvrez `lab-securite/vulnerable/app.py` et repérez la route de
> recherche de produits : la requête y est assemblée par une f-string.
> Remplacez-la par une requête paramétrée, redémarrez le service, puis relancez
> la même recherche avec la valeur `' OR '1'='1`. La liste complète ne revient
> plus : seule la recherche littérale reste, et la comparaison avec
> `lab-securite/secure/app.py` montre le même résultat.

---

## Points clés

- Une requête paramétrée **sépare les données des instructions** : la saisie
  remplit un emplacement, elle ne peut pas changer le sens de la requête.
- Échapper les guillemets à la main ne remplace jamais cette séparation.
- La validation d'entrée porte sur **trois choses** : le type, le format et la
  longueur maximale — et elle refuse, elle ne répare pas.
- Un ORM sécurise le cas courant ; dès qu'une saisie influence la **forme** de la
  requête, on revient à une liste fermée de valeurs autorisées.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Pourquoi une requête paramétrée empêche-t-elle une saisie de devenir une instruction ?

- A. Parce qu'elle échappe les guillemets et les apostrophes de la saisie, qui ne peut plus fermer la chaîne où elle s'insère
- B. Parce que le pilote envoie la structure de la requête et les valeurs séparément, et le moteur ne les confond jamais
- C. Parce qu'elle contrôle la longueur et le format de la valeur avant l'exécution, et écarte tout ce qui sort du modèle attendu
- D. Parce qu'elle chiffre la saisie avant de la transmettre au moteur, qui ne voit jamais le texte brut de la requête

**2.** Un développeur double toutes les apostrophes de la saisie « à la main » au lieu d'utiliser une requête paramétrée. Quel est le problème ?

- A. Aucun : échapper les caractères dangereux fait exactement ce que fait une requête paramétrée, en moins de code
- B. C'est plus lent : la requête change de texte à chaque valeur, là où une requête paramétrée se prépare une fois
- C. Il répare le symptôme : le jour où un cas n'a pas été prévu, la requête redevient injectable
- D. Cela empêche le moteur de réutiliser son plan d'exécution, ce qui coûte plus cher que l'injection elle-même

**3.** Pour vérifier qu'un mot de recherche ne contient que des caractères autorisés, pourquoi utiliser `re.fullmatch` plutôt que `re.match` ?

- A. Parce que `re.match` est plus lent que `re.fullmatch` sur une longue saisie et ralentit toute la requête
- B. Parce que `re.match` ne regarde que le commencement : la valeur pourrait se poursuivre par n'importe quoi
- C. Parce que `re.fullmatch` échappe de lui-même les caractères dangereux, ce qui rendrait tout échappement inutile
- D. Parce que `re.match` refuse les valeurs vides, ce qui bloque au passage les champs facultatifs laissés à blanc

**4.** Une saisie doit choisir la colonne selon laquelle trier une liste. Que dit la règle du chapitre ?

- A. On la passe en paramètre de la requête, comme toute valeur venue de l'extérieur : le moteur ne la confondra pas avec du code
- B. On échappe les caractères spéciaux du nom de colonne, comme on le ferait pour n'importe quelle chaîne envoyée au moteur
- C. On la laisse voyager telle quelle : un nom de colonne ne contient que des lettres, il ne peut rien casser dans la requête
- D. Elle influence la forme de la requête : on la remplace par un choix dans une liste fermée décidée par le code

**5.** *Question ouverte (2-3 lignes).* « Valider n'est pas nettoyer. » Expliquez la différence, et pourquoi réparer une valeur hors format en silence est plus dangereux que la refuser.

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. B.** Le moteur reçoit la structure d'un côté, les valeurs de l'autre : une valeur ne peut donc pas devenir une instruction, même si elle en a exactement l'apparence.
**Pourquoi :** c'est le moteur qui fait la distinction données/instructions ; échapper ou filtrer laisse cette distinction à la charge du code, donc à l'erreur.

**2. C.** Échapper à la main répare le symptôme : le traitement ne couvre que les cas prévus, et un cas non prévu rend la requête injectable.
**Pourquoi :** la séparation se fait avec le pilote, pas avec des remplacements de caractères — c'est l'encadré « Piège » du chapitre.

**3. B.** `re.match` ne vérifie que le début de la valeur : `bonjour` suivi de n'importe quoi passerait. `re.fullmatch` exige que le motif couvre toute la valeur.
**Pourquoi :** le contrôle de format ne vaut que s'il porte sur la totalité de ce qui sera utilisé.

**4. D.** Un nom de colonne n'est pas une valeur : dès qu'une saisie influence la forme de la requête — table, colonne, opérateur — elle ne peut pas voyager en valeur, on la remplace par un choix dans une liste fermée.
**Pourquoi :** ce qui structure reste du code, ce qui remplit reste de la donnée — le même réflexe que pour les en-têtes de réponse ou les chemins de fichiers.

**5.** Attendu : valider, c'est vérifier le type, le format et la longueur, et refuser ce qui est hors format avec un message qui dit pourquoi ; nettoyer, c'est supprimer les caractères interdits et laisser passer le reste. Une valeur « réparée » devient une valeur que personne n'a jamais testée.
**Pourquoi :** le refus est le fail-closed appliqué à la saisie — l'usage d'une valeur silencieusement modifiée est un fail-open dont personne ne sait qu'il a eu lieu.

</details>

---

[← Chapitre précédent](01-principes-secure-coding.md) · [Sommaire](Readme.md) · [Chapitre suivant →](03-xss-et-sorties.md)
