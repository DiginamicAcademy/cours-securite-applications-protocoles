[← Chapitre précédent](05-dependances-et-configuration.md) · [Sommaire](Readme.md) · [Chapitre suivant →](07-securite-api.md)

# Revue de code sécurité — chercher les patterns, pas relire tout

> Une association sportive fait relire le module de gestion de ses adhésions,
> écrit par un bénévole. Le relecteur n'a pas une journée : il a une heure. Il
> ne cherche pas les bugs — il cherche les **patterns**. Une passe sur les
> entrées, une passe sur les sorties, une passe sur les appels système. À la fin
> de l'heure, il sait où le module est fragile, et pourquoi.

**Durée de lecture :** 45 min hors approfondissements facultatifs · **Prérequis :** les chapitres
[Validation et injections](02-validation-et-injections.md) et
[XSS (Cross-Site Scripting) et sorties](03-xss-et-sorties.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Appliquer** une revue de code en trois passes — entrées, sorties, appels
  système — plutôt qu'une relecture linéaire.
- **Lire un diff** pour y repérer ce qui introduit une surface d'attaque.
- **Rédiger** un rapport de revue qui priorise, documente et propose.
- **Décider** ce qui relève de l'automatisation et ce qui exige un regard humain.

---

## I. La méthode en trois passes

Relire un fichier du début à la fin, c'est lire ce que le code **raconte**. La
revue de sécurité lit ce que le code **accepte**, **affiche** et **exécute**.
D'où trois passes indépendantes, chacune avec sa question :

| Passe | La question | Ce qu'on regarde |
| --- | --- | --- |
| **Entrées** | qu'est-ce qui arrive de l'extérieur ? | paramètres, fichiers, en-têtes, données de base |
| **Sorties** | qu'est-ce qui sort vers l'extérieur ? | pages, réponses, journaux, exports |
| **Appels système** | qu'est-ce que le code déclenche ? | requêtes, commandes, fichiers, appels réseau |

Chaque passe se fait sur **tout** le fichier, puis on passe à la suivante. C'est
plus rapide qu'une relecture attentive ligne à ligne, et surtout plus fiable :
le cerveau ne saute pas d'une préoccupation à l'autre.

Reste ce que chaque passe vérifie. **Entrées** : ce qui arrive
est-il **contrôlé** — type, format, longueur ? **Sorties** :
dans quel **contexte** la valeur s'insère-t-elle, et son traitement est-il
là ? **Appels système** : une donnée extérieure peut-elle en **modifier la
forme** ?

> 🧪 **Atelier rapide (10 min)**
>
> Prenez `lab/vulnerable/app.py` et appliquez les trois passes, sans chercher à
> comprendre le code en détail. Première passe : listez les paramètres reçus par
> chaque route. Deuxième passe : listez tout ce qui est renvoyé ou affiché.
> Troisième passe : listez les appels à la base de données. Comparez ensuite vos
> trois listes aux commentaires du fichier : les failles signalées tombent-elles
> dans une de vos passes ?

L'exercice montre quelque chose d'utile : les trois passes suffisent à
retrouver l'essentiel, sans expertise particulière du langage. C'est ce qui
rend la méthode transmissible à toute une équipe.

---

## II. Lire un diff

En pratique, la revue de sécurité ne porte pas sur un module entier : elle porte
sur **ce qui change**. Un diff montre les lignes ajoutées et retirées — et c'est
là que se joue l'essentiel.

Quatre signaux attirent l'attention dans un diff :

| Signal | Ce qu'il faut se demander |
| --- | --- |
| **Une chaîne assemblée** | une donnée extérieure entre-t-elle dans une requête, une commande, une adresse ? |
| **Une sortie sans traitement** | la valeur est-elle échappée pour le contexte où elle s'affiche ? |
| **Un contrôle retiré** | la vérification supprimée était-elle redondante, ou est-ce la seule ? |
| **Un chemin ou une commande** | une saisie peut-elle choisir le fichier, le programme, l'argument ? |

Le quatrième signal mérite un exemple. Une commande lancée par le code est un
appel système comme une requête :

```python
# dangereux : la saisie choisit l'argument de la commande
os.system("chmod 666 " + nom_du_fichier)

# sûr : la commande est fixe, la donnée est un paramètre
os.chmod(nom_du_fichier, 0o666)
```

> ⚠️ **Attention** — Un diff propre n'est pas un diff sûr. Le code ajouté peut
> être irréprochable et supprimer, en passant, la seule vérification qui
> protégeait la route. La revue regarde donc aussi **ce qui disparaît**.

---

## III. Le rapport

Une revue qui ne produit rien de transmissible est une opinion. Le rapport se
réduit à l'essentiel : **où**, **pourquoi c'est grave**, **quoi faire**.

| Élément | Ce qu'il contient |
| --- | --- |
| **Localisation** | le fichier et la ligne concernés |
| **Le problème** | le pattern reconnu, en une phrase |
| **La gravité** | ce qui devient possible si personne ne corrige |
| **La proposition** | le correctif, ou la piste à explorer |

La priorisation suit l'exposition, pas l'élégance du correctif. Un problème sur
une route ouverte à tous pèse plus lourd que le même problème sur une route
réservée à l'administration interne — même si le correctif est identique.

> 💡 **À retenir** — Le rapport de revue s'adresse à la personne qui va corriger.
> Il donne le contexte pour décider, pas seulement la liste de ce qui ne va pas.
> Un rapport qui dit « à corriger » sans dire « pourquoi maintenant » finit dans
> la pile des choses qu'on fera plus tard.

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **L'analyse statique automatisée** — le SAST (Static Application Security
  Testing) applique des motifs de recherche sur le code, sans l'exécuter. Il
  trouve vite ce qui est fréquent, et signale beaucoup de faux positifs : c'est
  un filtre, pas un verdict.
- **Les linters spécialisés** — des outils comme `bandit` pour Python ou
  `semgrep` pour plusieurs langages encodent des patterns de sécurité. Ils se
  branchent dans la CI (intégration continue) et vérifient chaque changement.
- **La revue par les pairs, gardée humaine** — l'automatisation traite les
  patterns connus. La question « cette donnée peut-elle modifier la forme de ce
  que le code fait ? » reste un raisonnement, et c'est précisément celui que la
  méthode en trois passes rend rapide.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> Affinage de posture : le rapport reste obligatoire dans sa forme minimale
> (où, pourquoi c'est grave, quoi faire).
>
> Deux formulations à éviter : le reproche sur le code existant, et la solution
> unique présentée comme la seule possible. La revue ouvre un arbitrage — elle ne
> le ferme pas.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> La version détaillée des trois passes, avec ses exemples de terrain.
>
> **Passe 1 — les entrées**
>
>
> On liste tout ce qui vient de l'extérieur, puis on demande pour chacun : est-ce
> qu'il est **contrôlé** ? Un identifiant qui devrait être un entier, une date qui
> devrait suivre un format, une chaîne qui devrait être bornée en longueur.
>
> **Passe 2 — les sorties**
>
>
> On liste tout ce qui sort, puis on demande dans quel **contexte** cela s'insère :
> du texte affiché, une adresse cliquable, un fichier téléchargeable, une ligne de
> journal. Chaque contexte attend son traitement — et l'absence de traitement se
> voit d'un coup d'œil quand on regarde toutes les sorties à la suite.
>
> **Passe 3 — les appels système**
>
>
> On liste ce que le code déclenche : les requêtes vers la base, les commandes
> lancées, les fichiers ouverts, les appels vers d'autres services. Pour chacun, la
> question est la même : une donnée extérieure peut-elle en **modifier la forme** ?

---

## Points clés

- La revue de sécurité lit ce que le code **accepte, affiche et déclenche** —
  trois passes, trois questions, dans cet ordre.
- Un diff se lit aussi pour ce qu'il **retire** : un contrôle supprimé est un
  changement de surface d'attaque.
- Le rapport dit **où, pourquoi c'est grave, quoi faire** — et priorise selon
  l'exposition.
- L'automatisation filtre les patterns connus ; la question de la forme reste
  humaine.

---

[← Chapitre précédent](05-dependances-et-configuration.md) · [Sommaire](Readme.md) · [Chapitre suivant →](07-securite-api.md)
