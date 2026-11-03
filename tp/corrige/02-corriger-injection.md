# Corrigé — Corriger une injection dans une recherche

> Corrigé de [l'exercice « Corriger une injection dans une recherche »](../02-corriger-injection.md).
> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte
> autant que le résultat.

---

## Partie 1 — Distinguer les instructions des données

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

## Partie 2 — Réécrire la requête

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

## Partie 3 — Contrôler la saisie

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

## Partie 4 — Vérifier le comportement

| Saisie | Comportement attendu |
| --- | --- |
| **La valeur piégée** | elle est traitée comme une recherche littérale : aucun résultat, ou un résultat contenant réellement ces caractères |
| **La chaîne très longue** | refusée avec le code 400, avant toute requête |
| **Une valeur normale** | résultat inchangé par rapport à la version initiale |

Le premier cas est le plus instructif : la valeur ne casse plus rien parce
qu'elle n'est plus une instruction. Elle ne « passe pas » — elle ne veut plus
rien dire pour le moteur.

---

## Points à retenir

- La séparation des données et des instructions se fait avec le pilote de base
  de données, pas avec des remplacements de caractères.
- Le contrôle d'entrée porte sur la longueur et le format, et **refuse** plutôt
  que de réparer.
- Le `fullmatch` vérifie toute la valeur ; un `match` simple ne vérifie que le
  début.
- Vérifier les trois cas — piégé, trop long, normal — montre que la correction
  ne change rien au fonctionnement attendu.
