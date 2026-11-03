# Corriger une injection dans une recherche

> 🟢 **Débutant** · **Durée :** 25 min · **Lien :** chapitre
> [Validation et injections](../02-validation-et-injections.md)
> **Objectif :** repérer ce qui, dans une requête, relève de l'instruction et ce
> qui relève de la donnée, puis réécrire la route en requête paramétrée avec un
> contrôle de saisie.

---

## Contexte

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

## Consignes

### Partie 1 — Distinguer les instructions des données

Reprenez la chaîne de la requête et délimitez, à la main, ce qui appartient au
langage de requête et ce qui appartient à la saisie. Expliquez, en deux phrases,
pourquoi une valeur de recherche peut modifier le **sens** de la requête plutôt
que de seulement remplir un emplacement.

### Partie 2 — Réécrire la requête

Réécrivez la route avec une requête paramétrée. La recherche doit rester
identique pour une saisie normale : même résultat sur un titre existant, aucun
changement de comportement visible.

### Partie 3 — Contrôler la saisie

Ajoutez le contrôle d'entrée en amont de la requête :

- la valeur est une chaîne, et sa longueur maximale est de **64** caractères ;
- elle ne contient que des lettres, des chiffres, des espaces, des apostrophes ou
  des tirets ;
- toute valeur hors de ces critères est refusée avec le code **400**, et un
  message qui dit ce qui n'allait pas.

### Partie 4 — Vérifier le comportement

Rejouez la recherche avec la valeur `' OR '1'='1`, puis avec une chaîne de
plusieurs centaines de caractères, puis avec une valeur normale. Notez, pour
chacune, ce que renvoie le service.

---

## ✅ Auto-évaluation

- [ ] Je sais nommer, dans une requête, ce qui relève de l'instruction et ce qui
      relève de la donnée.
- [ ] Ma route utilise une requête paramétrée, sans concaténation de la saisie.
- [ ] La longueur maximale de 64 caractères est contrôlée avant la requête.
- [ ] Le format de la saisie est vérifié sur toute la valeur, pas seulement sur
      son début.
- [ ] Une saisie invalide renvoie le code 400 avec un message explicite.
- [ ] J'ai vérifié les trois cas de la partie 4 et noté les résultats.

---

## Pour aller plus loin

*Facultatif — ne bloque pas la suite du parcours.*

Le champ de recherche accepte aussi un paramètre de tri, qui choisit la colonne
de classement. Proposez une façon de l'implémenter sans qu'une saisie puisse
choisir le nom de la colonne, et justifiez votre choix en une phrase.
