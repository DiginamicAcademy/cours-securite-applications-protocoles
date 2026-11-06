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
> La même manipulation, menée de bout en bout sur un livre d'or, est l'exercice
> [Échapper les sorties d'un livre d'or](tp/03-echapper-les-sorties.md).
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

[← Chapitre précédent](02-validation-et-injections.md) · [Sommaire](Readme.md) · [Chapitre suivant →](04-erreurs-et-logging.md)
