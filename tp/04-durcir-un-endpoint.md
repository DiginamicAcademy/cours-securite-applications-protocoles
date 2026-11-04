# Durcir un endpoint de réservation

> **Nature :** TD (quatre mini-durcissements en séquence) · **Durée :** 30 min · **Notion :** durcir un endpoint — erreurs, journaux, contrôle d'accès, en-têtes de sécurité
> 🟡 **Intermédiaire** · **Durée :** 30 min · **Lien :** chapitre
> [Erreurs et logging](../04-erreurs-et-logging.md)
> **Objectif :** durcir une route de service — erreurs non exposées, journaux
> sans secret, contrôle d'accès explicite, en-têtes de sécurité — sans changer
> son fonctionnement normal.

---

## Contexte

Un grand groupe mutualise ses salles de réunion via un petit service interne de
réservation. L'équipe qui l'a livré est partie ; il tourne, personne n'y touche.
La direction des systèmes d'information vous demande une passe de durcissement
avant de l'ouvrir à un nouveau site.

Voici les deux routes principales :

```python
import logging
import traceback

journal = logging.getLogger("reservations")


@app.get("/reservations")
def lister_reservations(email: str = ""):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE email = %s", (email,))
        rows = cursor.fetchall()
        conn.close()
        return {"reservations": rows}
    except Exception as exc:
        return {"erreur": str(exc), "trace": traceback.format_exc()}


@app.post("/reservations")
def creer_reservation(email: str = Form(...), salle: str = Form(...),
                      mot_de_passe: str = Form(...)):
    journal.info("creation pour %s (mdp %s)", email, mot_de_passe)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reservations (email, salle) VALUES (%s, %s)",
        (email, salle),
    )
    conn.commit()
    conn.close()
    return {"message": "réservation enregistrée"}
```

Le contrat attendu par la direction est le suivant : une personne ne voit que
ses propres réservations ; une erreur interne renvoie le code **500** avec un
message générique et un numéro de suivi ; un accès refusé renvoie le code
**403** ; aucun mot de passe ne se retrouve dans les journaux.

---

## Consignes

### Partie 1 — Repérer ce qui sort du service

Listez tout ce qui quitte le service : ce qui est renvoyé au client, ce qui est
écrit dans les journaux. Pour chacun, dites s'il renseigne la personne qui
utilise le service, ou surtout quelqu'un qui chercherait à comprendre le
système.

### Partie 2 — Durcir les erreurs

Modifiez la route de lecture pour que l'erreur interne renvoie le message
générique et le numéro de suivi prévus au contrat, et que le détail aille dans
les journaux. Le comportement normal de la route ne doit pas changer.

### Partie 3 — Nettoyer les journaux

Reprenez l'écriture du journal de création : l'événement doit rester traçable —
qui a réservé quoi, quand — sans jamais contenir le mot de passe. Justifiez en
une phrase ce que vous mettez à la place.

### Partie 4 — Contrôle d'accès et en-têtes

Ajoutez le contrôle qui empêche une personne de lister les réservations d'une
autre, avec le code **403** prévu au contrat. Ajoutez ensuite les en-têtes de
sécurité de réponse, au niveau du service plutôt que route par route.

---

## ✅ Auto-évaluation

- [ ] J'ai listé ce qui sort du service, côté client et côté journal.
- [ ] L'erreur interne renvoie le code 500, un message générique et un numéro de
      suivi.
- [ ] Le détail de l'erreur est journalisé côté serveur, jamais renvoyé.
- [ ] Aucun mot de passe n'apparaît dans les journaux.
- [ ] Le contrôle d'accès empêche de lire les réservations d'autrui, avec le
      code 403.
- [ ] Les en-têtes de sécurité sont posés au niveau du service.
- [ ] Le fonctionnement normal des deux routes est inchangé.

---

## Pour aller plus loin

*Facultatif — ne bloque pas la suite du parcours.*

Le service expose aussi une route de santé, utilisée par la supervision.
Proposez ce qu'elle doit renvoyer pour être utile à l'exploitation sans
renseigner quiconque la consulterait depuis l'extérieur.
