# Corrigé — Échapper les sorties d'un livre d'or

> Corrigé de [l'exercice « Échapper les sorties d'un livre d'or »](../03-echapper-les-sorties.md).
> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte
> autant que le résultat.

---

## Partie 1 — Repérer les contextes d'insertion

Le gabarit assemble la page à partir de trois données extérieures :

| Insertion | Contexte | Risque |
| --- | --- | --- |
| **La valeur de recherche** | texte d'un titre de section | la donnée devient du code |
| **Le nom de l'auteur** | contenu d'une balise de mise en gras | la donnée devient du code |
| **Le texte du message** | contenu d'un élément de liste | la donnée devient du code |

Les trois insertions sont du **texte affiché**. Aucune n'est traitée : la chaîne
est assemblée telle quelle, donc une balise déposée par un adhérent est relue
par le navigateur comme faisant partie de la page. C'est le mécanisme du XSS
(Cross-Site Scripting) : la confusion entre le texte que la personne voit et le
code que le navigateur exécute.

Le cas le plus visible est le nom de l'auteur : il s'insère dans une balise de
mise en gras, et une balise de script déposée à cet endroit s'exécute dès
l'ouverture de la page.

---

## Partie 2 — Échapper les sorties

Chaque insertion passe par l'échappement HTML (HyperText Markup Language) :

```python
from html import escape


@app.get("/livre-d-or")
def livre_d_or(q: str = ""):
    messages = charger_messages()
    html = f"<h2>Messages — recherche : {escape(q or '')}</h2><ul>"
    for m in messages:
        html += (f"<li><b>{escape(m['auteur'])}</b> : "
                 f"{escape(m['texte'])}</li>")
    html += "</ul>"
    return html
```

Rien n'est supprimé, rien n'est censuré : les chevrons et les guillemets sont
réécrits de façon à rester du texte. Un message contenant une balise de script
s'affiche littéralement, et le navigateur ne l'exécute pas.

L'échappement est appliqué **au moment de l'insertion**, pas au moment de la
saisie : c'est le contexte d'affichage qui décide du traitement, et une valeur
stockée peut être réutilisée plus tard dans un autre contexte.

---

## Partie 3 — Poser une politique de sécurité du contenu

L'en-tête se pose sur la réponse, côté serveur :

```python
return HTMLResponse(html, headers={
    "Content-Security-Policy": "default-src 'self'",
})
```

Cette politique annonce au navigateur que la page ne charge que ses propres
ressources. Si un échappement venait à être oublié ailleurs, un script injecté
depuis une autre origine serait refusé au chargement : la page perdrait la
ressource étrangère, mais ne l'exécuterait pas.

C'est une seconde barrière, pas un substitut : elle encaisse l'oubli, elle ne le
corrige pas.

---

## Partie 4 — Vérifier

| Message déposé | Résultat attendu |
| --- | --- |
| **Un message normal** | affiché tel quel, sans changement |
| **Une balise de script** | affichée comme du texte, non exécutée |
| **Un chevron isolé** | affiché comme du texte, la page reste structurée |

Le troisième cas est celui qu'on oublie : un chevron seul ne casse rien quand il
est échappé, alors qu'il peut faire disparaître le reste de la page quand il ne
l'est pas.

---

## Points à retenir

- Toute insertion de donnée dans une page est un **contexte**, et chaque
  contexte attend son traitement.
- L'échappement réécrit les caractères sensibles : rien n'est perdu, la donnée
  reste du texte.
- Il s'applique **à l'insertion**, pas à la saisie — le stockage ne présume pas
  de l'usage.
- La politique de sécurité du contenu est la seconde barrière : elle limite ce
  que la page charge, même quand l'échappement a été oublié.
