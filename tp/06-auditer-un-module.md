# Auditer un module de gestion des adhésions

> **Nature :** élément intégrable dans le TP intégrateur ([TP-INTEGRATEUR.md](TP-INTEGRATEUR.md)) — utilisable aussi en exercice autonome · **Durée :** 35 min · **Notion :** la revue de code sécurité en trois passes et le rapport de dette
> 🔵 **Avancé** · **Durée :** 35 min · **Lien :** chapitre
> [Revue de code sécurité](../06-revue-de-code-securite.md)
> **Objectif :** appliquer la revue en trois passes sur un module complet, puis
> en tirer un rapport de dette priorisé, exploitable par l'équipe.
>
> Cet exercice est **facultatif** : il prolonge le chapitre et s'intègre au
> [TP intégrateur](TP-INTEGRATEUR.md). Il ne bloque la progression nulle part.

---

## Contexte

L'association sportive dont vous êtes membre gère ses adhésions depuis un module
Python écrit au fil des saisons par plusieurs bénévoles. Il fonctionne, il est
utilisé chaque semaine — et personne ne l'a jamais relu sous l'angle sécurité.
Avant la prochaine campagne d'adhésions, le bureau vous demande cette revue.

Voici le module en l'état :

```python
import logging
import os
import traceback

from fastapi import FastAPI

app = FastAPI()
journal = logging.getLogger("adhesions")


def chercher_adhesions(nom):
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM adhesions WHERE nom LIKE '%{nom}%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


def page_resultats(nom, adhesions):
    html = f"<h2>Adhésions — recherche : {nom}</h2><ul>"
    for a in adhesions:
        html += f"<li>{a['nom']} — {a['email']}</li>"
    html += "</ul>"
    return html


def exporter_fichier(nom_du_fichier):
    os.system("chmod 666 " + nom_du_fichier)
    return nom_du_fichier


def enregistrer_paiement(email, mot_de_passe):
    journal.info("paiement de %s (compte %s)", email, mot_de_passe)
    return {"statut": "enregistre"}


@app.get("/adhesions")
def route_adhesions(nom: str = ""):
    try:
        return page_resultats(nom, chercher_adhesions(nom))
    except Exception as exc:
        return {"erreur": str(exc), "trace": traceback.format_exc()}
```

Le bureau attend un document qu'il puisse utiliser : pas un avis général sur la
qualité du code, mais une liste de points classés, avec pour chacun ce qu'il
permet de faire et ce qu'il faudrait changer.

---

## Consignes

### Partie 1 — Appliquer les trois passes

Faites les trois passes du chapitre sur l'ensemble du module, dans l'ordre :
entrées, sorties, appels système. Pour chaque passe, produisez une liste — sans
encore chercher à comprendre le fonctionnement général du module.

### Partie 2 — Retracer l'anatomie d'un problème

Choisissez l'un des problèmes relevés et retracez son anatomie : par où la
donnée arrive, où elle est transformée, ce qu'elle permet de faire si personne
ne corrige. Trois ou quatre phrases suffisent.

### Partie 3 — Rédiger le rapport de dette

Rédigez le rapport destiné au bureau : pour chaque point, la localisation, le
problème en une phrase, la gravité, et la proposition de correction. Classez les
points selon l'exposition — ce qui est atteignable par n'importe quel adhérent
passe avant ce qui exige un accès particulier.

---

## ✅ Auto-évaluation

- [ ] Mes trois listes (entrées, sorties, appels système) sont faites séparément.
- [ ] Chaque problème du module apparaît dans au moins une de mes listes.
- [ ] L'anatomie choisie suit la donnée de l'arrivée jusqu'à l'impact.
- [ ] Mon rapport donne, pour chaque point, la localisation et la proposition.
- [ ] Les points sont classés selon l'exposition, pas selon la facilité du
      correctif.
- [ ] Le rapport se lit sans moi pour être compris.

---

## Pour aller plus loin

*Facultatif — ne bloque pas la suite du parcours.*

🔴 **Défi** — Rédigez la checklist de revue de code de l'équipe : une page, les
questions à se poser à chaque passe, les signaux qui déclenchent une revue
approfondie. Puis appliquez-la à un ancien module de l'association, et notez ce
que la checklist a fait trouver que la relecture libre n'avait pas vu.
