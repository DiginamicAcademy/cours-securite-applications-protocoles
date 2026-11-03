# Corrigé — Durcir un endpoint de réservation

> Corrigé de [l'exercice « Durcir un endpoint de réservation »](../04-durcir-un-endpoint.md).
> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte
> autant que le résultat.

---

## Partie 1 — Repérer ce qui sort du service

| Ce qui sort | Où | Ce que cela renseigne |
| --- | --- | --- |
| **Le message d'erreur** | réponse client | le type d'échec, parfois la structure de la base |
| **La trace complète** | réponse client | les chemins de fichiers, les versions, la ligne fautive |
| **La ligne de journal** | journal serveur | l'événement, et le mot de passe en clair |
| **La liste des réservations** | réponse client | les données d'une autre personne |

Le constat est le même pour les deux premières lignes : ce qui aide le
développeur à corriger est exactement ce qui aide quiconque à cartographier le
service. La trace complète n'a rien à faire dans une réponse client.

La troisième ligne est plus discrète et plus grave : un journal est lu par plus
de monde que la base de données, et il contient une copie des identifiants.

---

## Partie 2 — Durcir les erreurs

La route renvoie le contrat attendu, et laisse le détail au journal :

```python
@app.get("/reservations")
def lister_reservations(email: str = ""):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE email = %s", (email,))
        rows = cursor.fetchall()
        conn.close()
        return {"reservations": rows}
    except Exception:
        reference = nouvelle_reference()
        journal.exception("echec de la lecture des reservations")
        return JSONResponse(
            status_code=500,
            content={"erreur": "la demande n'a pas pu être traitée",
                     "reference": reference},
        )
```

Le numéro de suivi est le joint entre les deux mondes : la personne signale un
numéro, l'équipe retrouve la trace complète dans les journaux. Le message
générique ne dit rien de la structure du système, et reste suffisant pour que la
personne sache que sa demande a été prise en compte.

---

## Partie 3 — Nettoyer les journaux

L'événement reste traçable, sans le secret :

```python
journal.info("creation de reservation",
             extra={"email": email, "salle": salle})
```

Ce qui est conservé — qui a réservé quoi — suffit à reconstituer l'historique.
Ce qui disparaît — le mot de passe — n'a rien à faire là : il ne sert à rien
pour comprendre un incident de réservation, et il se retrouverait dans chaque
copie du journal.

Si le paiement doit être tracé, on journalise le **fait** et un identifiant
technique de la transaction, jamais la donnée d'authentification.

---

## Partie 4 — Contrôle d'accès et en-têtes

Le contrôle d'accès empêche de lire les réservations d'autrui :

```python
@app.get("/reservations")
def lister_reservations(email: str = "", utilisateur=Depends(get_current_user)):
    if utilisateur["email"] != email:
        raise HTTPException(status_code=403,
                            detail="accès réservé à vos propres réservations")
    ...
```

Puis les en-têtes se posent une fois, pour tout le service :

```python
@app.middleware("http")
async def en_tetes_securite(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

Posés au niveau du service, ils couvrent aussi les routes ajoutées plus tard —
c'est l'avantage de ne pas les répéter route par route.

---

## Points à retenir

- Ce qui aide le développeur — la trace, le détail — part dans les journaux ; la
  réponse client garde un message générique et un numéro de suivi.
- Un journal décrit **ce qui s'est passé**, pas ce que contenaient les données :
  aucun secret n'y figure.
- Le contrôle d'accès se pose sur la donnée demandée, pas seulement sur la route.
- Les en-têtes de sécurité se posent **une fois**, au niveau du service.
