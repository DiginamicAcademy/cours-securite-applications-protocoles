[← Chapitre précédent](02-validation-et-injections.md) · [Sommaire](Readme.md) · [Chapitre suivant →](04-erreurs-et-logging.md)

# XSS et sorties — que le texte reste du texte

> Sur le site d'un magazine en ligne, les lecteurs laissent des commentaires
> sous les articles. L'un d'eux dépose un message qui ne s'affiche pas : il
> s'exécute. Le lendemain, plusieurs rédacteurs constatent que leur session se
> vide toute seule. Le problème est toujours le même : la confusion entre ce que
> la personne **voit** et ce que le navigateur **exécute**.

**Durée de lecture :** 45 min hors approfondissements facultatifs · **Prérequis :** les failles de type injection
étudiées lors des journées précédentes, et le chapitre
[Validation et injections](02-validation-et-injections.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Échapper** une donnée affichée dans une page, selon le contexte où elle
  s'insère.
- **Distinguer** les contextes d'insertion — texte, attribut, script, adresse —
  et le traitement qui correspond à chacun.
- **Poser** une politique de sécurité du contenu pour limiter ce qu'une page
  peut charger et exécuter — en principe : la mécanique des directives est en
  approfondissement.
- **Choisir** un moteur de gabarit qui échappe par défaut, et repérer les endroits
  où ce défaut est désactivé.

---

## I. Échappement

Le XSS (Cross-Site Scripting) naît d'une confusion vieille comme le web : une
page mélange du **texte** et du **code**, et une donnée qui devait rester du
texte se retrouve du code. L'échappement est la ponctuation qui les sépare — il
réécrit les caractères qui ont un sens particulier pour qu'ils redeviennent de
la lettre.

En Python, la fonction de base est `html.escape` :

```python
from html import escape

saisie = "<script>alert(1)</script>"
print(escape(saisie))
# la balise s'affiche comme du texte : les chevrons sont encodés
```

Le navigateur affiche la balise au lieu de l'exécuter. C'est tout le mécanisme :
rien n'est supprimé, rien n'est censuré — la donnée est **rendue inoffensive**
pour le contexte où elle s'insère.

| Contexte d'insertion | Ce qui s'y insère | Traitement |
| --- | --- | --- |
| **Texte** entre deux balises | un commentaire, un nom | échappement HTML classique |
| **Attribut** de balise | une valeur d'option | échappement HTML, et guillemets de l'attribut toujours posés |
| **Bloc de script** | une valeur lue par du code | jamais d'échappement HTML : sérialisation dédiée |
| **Adresse** (lien) | une destination | validation du schéma, refus de ce qui n'est pas une adresse attendue |

> ⚠️ **Attention** — L'échappement dépend du contexte. Une valeur correctement
> échappée pour du texte le devient beaucoup moins dans un bloc de script ou dans
> une adresse : c'est le traitement du contexte qui compte, pas une fonction
> appliquée partout à l'aveugle.

---

## II. CSP

L'échappement protège ce que **votre page** affiche. Il ne dit rien de ce que la
page **charge** : une bibliothèque tierce, une image distante, un script hébergé
ailleurs. La CSP (Content Security Policy) est la liste de ce que la page a le
droit de charger et d'exécuter — annoncée au navigateur par un en-tête de
réponse.

> 💡 **À retenir** — La CSP est la ceinture et les bretelles : elle ne remplace
> pas l'échappement, elle encaisse le jour où il a été oublié. Une politique
> stricte transforme une injection réussie en page qui refuse de charger le
> code étranger.

Elle se pose **en réponse HTTP**, côté serveur — pas dans une balise de la page,
qu'une injection pourrait retirer. Et elle se teste : un navigateur qui refuse
une ressource le signale dans sa console, ce qui permet de resserrer la
politique progressivement plutôt que de casser la page d'un coup.

---

## III. Templates sûrs

La plupart des pages ne sont pas écrites à la main : elles sont produites par un
moteur de gabarit. Ce moteur a donc un rôle décisif — s'il échappe les valeurs
par défaut, l'oubli devient rare ; s'il ne le fait pas, chaque affichage est une
porte ouverte.

Jinja2, le moteur de gabarit de Flask, échappe par défaut dans les gabarits
fichiers :

```html
<!-- la valeur est échappée automatiquement -->
<h3>Recherche : {{ q }}</h3>
```

Deux habitudes annulent cette protection :

| Habitude | Pourquoi ça échappe |
| --- | --- |
| **Marquer une valeur comme sûre** | le moteur ne l'échappe plus, alors qu'elle vient de l'extérieur |
| **Assembler le gabarit depuis une chaîne** | le texte n'est plus un gabarit, mais du code interprété |

> ⚠️ **Attention** — Un moteur de gabarit sûr ne protège que ce qu'il voit. Une
> chaîne assemblée à la main, puis injectée dans la page, lui échappe
> complètement : la sécurité du gabarit s'arrête là où le code reprend la main.

---

### Exercice 1 — Échapper les sorties d'un livre d'or (15 min)

#### Contexte

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

#### Consignes

##### Partie 1 — Repérer les contextes d'insertion

Listez, dans le gabarit ci-dessus, chaque endroit où une donnée extérieure
s'insère dans la page. Pour chacun, précisez le contexte : texte affiché,
contenu d'une balise, ou autre. Identifiez celui où la donnée peut devenir du
code exécuté.

##### Partie 2 — Échapper les sorties

Appliquez l'échappement adapté à chaque insertion. Le texte doit rester du texte
dans tous les cas, y compris quand un message contient des chevrons ou des
guillemets. Vérifiez qu'un message contenant une balise de script s'affiche
comme du texte.

##### Partie 3 — Poser une politique de sécurité du contenu

Ajoutez l'en-tête de réponse qui limite la page à ses propres ressources. Notez
la valeur exacte de l'en-tête, et expliquez en une phrase ce qu'elle change si
l'échappement venait à être oublié ailleurs.

##### Partie 4 — Vérifier

Testez la page avec trois messages : un message normal, un message contenant une
balise de script, un message contenant un chevron isolé. Notez ce qui s'affiche
dans chaque cas.

---

#### ✅ Auto-évaluation

- [ ] J'ai listé chaque insertion de donnée et son contexte.
- [ ] Chaque valeur affichée passe par un échappement adapté à son contexte.
- [ ] Une balise de script déposée dans un message s'affiche comme du texte.
- [ ] L'en-tête de politique de sécurité du contenu est posé côté serveur.
- [ ] Je peux expliquer ce que cette politique change en cas d'oubli d'échappement.
- [ ] J'ai testé les trois messages de la partie 4.

---

#### Pour aller plus loin

*Facultatif — ne bloque pas la suite du parcours.*

Le livre d'or affiche aussi, sous chaque message, un lien vers la page
personnelle de l'auteur. Proposez le traitement de cette adresse pour qu'elle ne
puisse pas devenir un lien vers une destination inattendue, et justifiez-le en
une phrase.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Repérer les contextes d'insertion

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

#### Partie 2 — Échapper les sorties

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

#### Partie 3 — Poser une politique de sécurité du contenu

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

#### Partie 4 — Vérifier

| Message déposé | Résultat attendu |
| --- | --- |
| **Un message normal** | affiché tel quel, sans changement |
| **Une balise de script** | affichée comme du texte, non exécutée |
| **Un chevron isolé** | affiché comme du texte, la page reste structurée |

Le troisième cas est celui qu'on oublie : un chevron seul ne casse rien quand il
est échappé, alors qu'il peut faire disparaître le reste de la page quand il ne
l'est pas.

---

#### Points à retenir

- Toute insertion de donnée dans une page est un **contexte**, et chaque
  contexte attend son traitement.
- L'échappement réécrit les caractères sensibles : rien n'est perdu, la donnée
  reste du texte.
- Il s'applique **à l'insertion**, pas à la saisie — le stockage ne présume pas
  de l'usage.
- La politique de sécurité du contenu est la seconde barrière : elle limite ce
  que la page charge, même quand l'échappement a été oublié.

</details>

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **Le XSS côté client** — quand la donnée dangereuse est lue puis réécrite par
  du code JavaScript dans la page, l'échappement serveur ne voit rien. Le
  problème se traite là où la valeur est insérée dans le DOM (Document Object
  Model), c'est-à-dire dans le code de la page elle-même.
- **Trusted Types** — une protection du navigateur qui oblige le code de la page
  à construire le HTML par des fonctions dédiées, et refuse les insertions de
  chaînes brutes. Elle transforme une famille entière d'erreurs en échec
  immédiat, au lieu d'une faille silencieuse.
- **La politique en deux temps** — on commence par une CSP en mode signalement :
  le navigateur rapporte les violations sans bloquer. Une fois la politique
  ajustée, on passe en application. C'est la façon réaliste de durcir une page
  existante.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> Ce cas de bibliothèque a déjà été ouvert à la journée sur les vulnérabilités ;
> il illustre les deux habitudes du tableau ci-dessus.
>
> C'est exactement le mécanisme de la faille de gabarit étudiée lors du travail
> sur les vulnérabilités des bibliothèques : un filtre qui assemble des attributs
> de balise à partir d'un dictionnaire laissait passer des clés non validées, et
> une clé piégée ajoutait un attribut exécutable. La correction avait deux volets —
> mettre la bibliothèque à jour, **et** valider les clés côté applicatif. La
> mise à jour ferme la faille connue ; la validation empêche la suivante.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> Le geste à retenir tient sans ce détail : une politique `default-src 'self'`
> se pose, puis se resserre ressource par ressource.
>
> ```http
> Content-Security-Policy: default-src 'self'; script-src 'self'
> ```
>
> Cet en-tête signifie : par défaut, la page ne charge que ce qui vient de son
> propre domaine, et les scripts suivent la même règle. Un script injecté depuis
> une autre origine est refusé par le navigateur, même si l'échappement a été
> contourné.
>
> | Directive | Ce qu'elle borne | Effet en cas d'injection |
> | --- | --- | --- |
> | `default-src` | tout ce qui n'est pas couvert ailleurs | le chargement par défaut se limite à l'origine |
> | `script-src` | les scripts exécutables | un script distant ne tourne pas |
> | `style-src` | les feuilles de style | le détournement de mise en forme est limité |
> | `img-src` | les images | les pistages par pixel externe sont bloqués |

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> La même manipulation, menée de bout en bout sur un livre d'or, est l'exercice 1 de ce chapitre, plus haut.
>
> 🧪 **Atelier rapide (8 min)**
>
> Ouvrez un interpréteur Python et comparez deux façons d'afficher une saisie :
> la chaîne brute, puis la même chaîne passée par `html.escape`. Faites de même
> avec une valeur contenant une apostrophe et un chevron. Puis ouvrez
> `lab/vulnerable/app.py`, repérez la route qui réaffiche la recherche dans une
> page, et identifiez la ligne où la donnée redevient du code. La même route,
> dans `lab/secure/app.py`, montre le traitement appliqué.
>
> Ce qui frappe en faisant l'exercice, c'est que la correction tient en un appel
> de fonction. Comme pour la requête paramétrée, tout le travail est dans le
> diagnostic : voir qu'une donnée arrive dans un contexte de code.

---

## Points clés

- Le XSS vient de la **confusion** entre le texte affiché et le code exécuté ;
  l'échappement rend la donnée inoffensive pour son contexte.
- Le traitement dépend du **contexte d'insertion** : texte, attribut, script ou
  adresse n'attendent pas le même travail.
- La CSP borne ce que la page **charge et exécute** : c'est la seconde barrière,
  posée en en-tête de réponse.
- Un moteur de gabarit qui échappe par défaut supprime une famille d'oubliés —
  à condition de ne pas le contourner avec des chaînes assemblées à la main.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** D'où naît une faille XSS (Cross-Site Scripting) ?

- A. D'une base de données mal indexée, qui renvoie bien plus de lignes que prévu pour la page demandée
- B. De la confusion entre le texte que la personne voit et le code que le navigateur exécute
- C. D'un mot de passe trop court, deviné par un tiers qui prend la session de la personne à sa place
- D. D'une page qui charge des images trop lourdes, dont les adresses exposées livrent l'arborescence du serveur

**2.** Que fait exactement `html.escape` sur une saisie contenant `<script>alert(1)</script>` ?

- A. Il supprime purement et simplement la balise de la valeur avant de l'afficher : il ne reste rien à exécuter
- B. Il refuse toute saisie contenant un chevron et renvoie un message d'erreur, pour n'afficher aucun doute
- C. Il réécrit les caractères qui ont un sens particulier : la balise s'affiche comme du texte au lieu d'être exécutée
- D. Il chiffre la valeur avant de l'afficher, si bien que le navigateur ne voit plus une balise mais un texte illisible

**3.** Pourquoi la CSP (Content Security Policy) se pose-t-elle en en-tête de réponse HTTP, côté serveur, plutôt que dans une balise de la page ?

- A. Parce que les en-têtes sont plus rapides à analyser que les balises
- B. Parce qu'une balise dans la page pourrait être retirée par une injection
- C. Parce que les navigateurs ignorent les balises de politique de contenu
- D. Parce que l'en-tête chiffre aussi les échanges avec le navigateur

**4.** Le moteur de gabarit échappe les valeurs par défaut. Quelles habitudes annulent cette protection ?

- A. Nommer les variables en minuscules et éviter les accents
- B. Utiliser des gabarits en fichier plutôt qu'en chaîne, et limiter leur taille
- C. Marquer une valeur comme sûre, et assembler le gabarit depuis une chaîne
- D. Journaliser les valeurs affichées et limiter la longueur des champs

**5.** *Question ouverte (2-3 lignes).* « Une valeur correctement échappée pour du texte le devient beaucoup moins dans un bloc de script ou dans une adresse. » Expliquez pourquoi le contexte d'insertion décide du traitement, avec un exemple du chapitre.

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. B.** Le XSS naît quand une donnée qui devait rester du texte se retrouve du code : la page mélange texte et code, et le navigateur exécute.
**Pourquoi :** c'est la confusion entre ce que la personne voit et ce que le navigateur exécute — rien de plus, rien de moins.

**2. C.** Rien n'est supprimé, rien n'est censuré : les chevrons sont encodés, la balise s'affiche comme du texte. La donnée est rendue inoffensive pour son contexte.
**Pourquoi :** supprimer ou refuser serait traiter le symptôme ; l'échappement est la ponctuation qui sépare le texte du code.

**3. B.** Une politique posée dans la page est une donnée comme une autre : une injection peut la retirer. L'en-tête de réponse, lui, est posé par le serveur.
**Pourquoi :** la CSP est la seconde barrière — « la ceinture et les bretelles » : elle encaisse le jour où l'échappement a été oublié, à condition d'être hors d'atteinte de l'injection.

**4. C.** Marquer une valeur comme sûre empêche le moteur de l'échapper alors qu'elle vient de l'extérieur ; assembler le gabarit depuis une chaîne transforme le texte en code interprété.
**Pourquoi :** un moteur de gabarit sûr ne protège que ce qu'il voit — la sécurité s'arrête là où le code reprend la main.

**5.** Attendu : chaque contexte a son langage — entre deux balises un échappement HTML suffit ; dans un attribut il faut aussi les guillemets toujours posés ; dans un bloc de script l'échappement HTML ne sert à rien, il faut une sérialisation dédiée ; pour une adresse c'est le schéma qu'on valide.
**Pourquoi :** c'est le traitement du contexte qui compte, pas une fonction appliquée partout à l'aveugle : la même valeur ne signifie pas la même chose selon l'endroit où elle s'insère.

</details>

---

[← Chapitre précédent](02-validation-et-injections.md) · [Sommaire](Readme.md) · [Chapitre suivant →](04-erreurs-et-logging.md)
