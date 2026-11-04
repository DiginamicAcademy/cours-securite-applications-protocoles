# Échapper les sorties d'un livre d'or

> **Nature :** exercice · **Durée :** 15 min · **Notion :** l'échappement des sorties et la CSP — que le texte reste du texte
> 🟢 **Débutant** · **Durée :** 15 min · **Lien :** chapitre
> [XSS (Cross-Site Scripting) et sorties](../03-xss-et-sorties.md)
> **Objectif :** repérer les contextes d'insertion d'une page, appliquer
> l'échappement adapté à chacun, puis poser une politique de sécurité du contenu.

---

## Contexte

Une association de randonnée tient un livre d'or en ligne : les adhérents y
laissent un mot après chaque sortie. La page est servie par une petite
application Python, écrite à la main, qui assemble le HTML (HyperText Markup
Language) dans une chaîne.

Depuis la dernière sortie, plusieurs adhérents signalent que la page « se
comporte bizarrement » : un message ne s'affiche pas, et la session d'un
modérateur s'est déconnectée toute seule.

```python
@app.get("/livre-d-or")
def livre_d_or(q: str = ""):
    messages = charger_messages()
    html = f"<h2>Messages — recherche : {q}</h2><ul>"
    for m in messages:
        html += f"<li><b>{m['auteur']}</b> : {m['texte']}</li>"
    html += "</ul>"
    return html
```

L'association veut garder cette page simple : pas de framework, pas de
refonte. Elle veut juste que les messages restent des messages.

---

## Consignes

### Partie 1 — Repérer les contextes d'insertion

Listez, dans le gabarit ci-dessus, chaque endroit où une donnée extérieure
s'insère dans la page. Pour chacun, précisez le contexte : texte affiché,
contenu d'une balise, ou autre. Identifiez celui où la donnée peut devenir du
code exécuté.

### Partie 2 — Échapper les sorties

Appliquez l'échappement adapté à chaque insertion. Le texte doit rester du texte
dans tous les cas, y compris quand un message contient des chevrons ou des
guillemets. Vérifiez qu'un message contenant une balise de script s'affiche
comme du texte.

### Partie 3 — Poser une politique de sécurité du contenu

Ajoutez l'en-tête de réponse qui limite la page à ses propres ressources. Notez
la valeur exacte de l'en-tête, et expliquez en une phrase ce qu'elle change si
l'échappement venait à être oublié ailleurs.

### Partie 4 — Vérifier

Testez la page avec trois messages : un message normal, un message contenant une
balise de script, un message contenant un chevron isolé. Notez ce qui s'affiche
dans chaque cas.

---

## ✅ Auto-évaluation

- [ ] J'ai listé chaque insertion de donnée et son contexte.
- [ ] Chaque valeur affichée passe par un échappement adapté à son contexte.
- [ ] Une balise de script déposée dans un message s'affiche comme du texte.
- [ ] L'en-tête de politique de sécurité du contenu est posé côté serveur.
- [ ] Je peux expliquer ce que cette politique change en cas d'oubli d'échappement.
- [ ] J'ai testé les trois messages de la partie 4.

---

## Pour aller plus loin

*Facultatif — ne bloque pas la suite du parcours.*

Le livre d'or affiche aussi, sous chaque message, un lien vers la page
personnelle de l'auteur. Proposez le traitement de cette adresse pour qu'elle ne
puisse pas devenir un lien vers une destination inattendue, et justifiez-le en
une phrase.
