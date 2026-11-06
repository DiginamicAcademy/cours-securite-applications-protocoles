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

### Exercice 1 — Auditer un module de gestion des adhésions (35 min, facultatif)

#### Contexte

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

#### Consignes

##### Partie 1 — Appliquer les trois passes

Faites les trois passes du chapitre sur l'ensemble du module, dans l'ordre :
entrées, sorties, appels système. Pour chaque passe, produisez une liste — sans
encore chercher à comprendre le fonctionnement général du module.

##### Partie 2 — Retracer l'anatomie d'un problème

Choisissez l'un des problèmes relevés et retracez son anatomie : par où la
donnée arrive, où elle est transformée, ce qu'elle permet de faire si personne
ne corrige. Trois ou quatre phrases suffisent.

##### Partie 3 — Rédiger le rapport de dette

Rédigez le rapport destiné au bureau : pour chaque point, la localisation, le
problème en une phrase, la gravité, et la proposition de correction. Classez les
points selon l'exposition — ce qui est atteignable par n'importe quel adhérent
passe avant ce qui exige un accès particulier.

---

#### ✅ Auto-évaluation

- [ ] Mes trois listes (entrées, sorties, appels système) sont faites séparément.
- [ ] Chaque problème du module apparaît dans au moins une de mes listes.
- [ ] L'anatomie choisie suit la donnée de l'arrivée jusqu'à l'impact.
- [ ] Mon rapport donne, pour chaque point, la localisation et la proposition.
- [ ] Les points sont classés selon l'exposition, pas selon la facilité du
      correctif.
- [ ] Le rapport se lit sans moi pour être compris.

---

#### Prolongement de l'exercice

*Facultatif — ne bloque pas la suite du parcours.*

🔴 **Défi** — Rédigez la checklist de revue de code de l'équipe : une page, les
questions à se poser à chaque passe, les signaux qui déclenchent une revue
approfondie. Puis appliquez-la à un ancien module de l'association, et notez ce
que la checklist a fait trouver que la relecture libre n'avait pas vu.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Appliquer les trois passes

**Passe 1 — les entrées.** Ce qui arrive de l'extérieur : le nom de recherche,
le nom de fichier à exporter, l'adresse électronique et le mot de passe de
paiement. Pour chacun, la question est de savoir s'il est contrôlé avant usage —
et ici, aucun ne l'est.

**Passe 2 — les sorties.** Ce qui sort du module : la page de résultats, la
réponse d'erreur, la ligne de journal, le fichier exporté. La page insère des
données sans traitement ; la réponse d'erreur renvoie la trace ; le journal
contient un mot de passe.

**Passe 3 — les appels système.** Ce que le module déclenche : la requête vers
la base, la commande de changement de droits sur un fichier. Dans les deux cas,
une donnée extérieure influence la **forme** de ce qui est exécuté.

| Passe | Point relevé | Localisation |
| --- | --- | --- |
| **Entrées** | la saisie entre dans une requête | fonction de recherche |
| **Entrées** | aucune vérification d'identité sur la route | route des adhésions |
| **Sorties** | les données s'insèrent dans la page sans échappement | fonction de mise en page |
| **Sorties** | la trace d'erreur part dans la réponse | route des adhésions |
| **Sorties** | le mot de passe est écrit au journal | fonction de paiement |
| **Appels système** | la saisie choisit l'argument d'une commande | fonction d'export |

Les trois passes couvrent l'ensemble du module sans qu'il ait fallu le
comprendre en détail — c'est ce qui rend la méthode applicable en une heure.

---

#### Partie 2 — Retracer l'anatomie d'un problème

Prenons la saisie qui entre dans la requête. Le nom de recherche arrive depuis
le champ de la page, sans contrôle de format ni de longueur. Il est collé dans
la chaîne de la requête, où il rejoint le vocabulaire de la requête elle-même.
Le moteur de base ne fait pas la différence entre ce qui vient du développeur et
ce qui vient du champ : une valeur qui contient un signe de fin de condition
termine la condition, et la suite est exécutée comme instruction.

Si personne ne corrige, n'importe quel adhérent peut lire la table des
adhésions au-delà de ce que la recherche devait montrer — et, selon les droits du
compte de base, aller au-delà de la lecture.

---

#### Partie 3 — Rédiger le rapport de dette

| Localisation | Problème | Gravité | Proposition |
| --- | --- | --- | --- |
| **Fonction de recherche** | la saisie entre dans la requête | haute — atteignable par n'importe quel adhérent | requête paramétrée, contrôle de format et de longueur |
| **Fonction de mise en page** | les données s'insèrent sans échappement | haute — atteignable par n'importe quel adhérent | échappement de chaque insertion, politique de sécurité du contenu |
| **Route des adhésions** | la trace d'erreur part dans la réponse | haute — renseigne sur le système | message générique et numéro de suivi, détail au journal |
| **Route des adhésions** | aucun contrôle d'identité | haute — lecture des données d'autrui | vérification de l'identité demandée, refus explicite |
| **Fonction d'export** | la saisie choisit l'argument d'une commande | moyenne — dépend de qui appelle l'export | appel direct de la fonction système, sans chaîne de commande |
| **Fonction de paiement** | le mot de passe est écrit au journal | moyenne — fuite vers un support plus largement lu | journaliser le fait et l'identifiant technique, jamais le secret |

Le classement suit l'exposition : les quatre premiers points sont atteignables
par un simple adhérent, les deux derniers supposent un accès ou un usage
particulier. Le correctif le plus rapide n'est pas forcément le plus urgent.

---

#### Points à retenir

- Les trois passes — entrées, sorties, appels système — couvrent un module
  complet sans qu'il faille le comprendre en détail.
- Suivre la donnée de l'arrivée jusqu'à l'impact donne l'anatomie du problème,
  et donc le bon endroit pour corriger.
- Le rapport classe selon **l'exposition**, pas selon la facilité du correctif.
- Un rapport exploitable dit où, pourquoi c'est grave, quoi faire — et se lit
  sans son auteur.

</details>

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

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Pourquoi la revue de sécurité se fait-elle en trois passes (entrées, sorties, appels système) plutôt qu'en relisant le fichier ligne à ligne ?

- A. Parce que relire ligne à ligne est proscrit en revue officielle : on y passerait des journées que l'équipe n'a pas à perdre
- B. Parce que chaque passe porte une seule question sur tout le fichier : c'est plus rapide et plus fiable, le cerveau ne saute pas d'une préoccupation à l'autre
- C. Parce que les trois passes, à chercher des patterns, finissent par couvrir les bugs de fonctionnement en plus des failles
- D. Parce qu'une seule passe suffit dès que le fichier est court : les trois visent les modules qui dépassent la centaine de lignes

**2.** Dans un diff, le code ajouté est irréprochable. Que doit quand même regarder le relecteur ?

- A. Rien : seules comptent les lignes ajoutées, puisqu'elles portent le nouveau comportement du module
- B. Seulement la taille du changement, pour estimer le temps de correction et répartir la dette entre développeurs
- C. Ce que le diff retire : un contrôle supprimé peut être la seule vérification qui protégeait la route
- D. Uniquement le nom de la personne qui a écrit le changement, pour lui demander des explications de vive voix

**3.** Le même défaut existe sur deux routes : l'une est ouverte à tous, l'autre réservée à l'administration interne. Comment le rapport de revue priorise-t-il ?

- A. À gravité égale sur la fiche, les deux corrections ont la même priorité : c'est le score qui tranche
- B. La route interne d'abord, puisque le correctif y est plus simple et libère la revue plus vite
- C. Selon l'élégance du correctif disponible, pour ne pas laisser deux demi-mesures dans le code
- D. La route ouverte à tous d'abord : la priorisation suit l'exposition, pas l'élégance du correctif

**4.** Dans un diff, cette ligne attire l'attention : `os.system("chmod 666 " + nom_du_fichier)`. Quel est le problème ?

- A. Le mode 666 est trop restrictif pour un fichier que la comptabilité doit relire le lendemain matin
- B. `os.system` est simplement plus lent que `os.chmod`, et la lenteur n'est pas un risque de sécurité
- C. La saisie choisit l'argument de la commande : une donnée extérieure peut modifier la forme de l'appel système
- D. Rien : la commande elle-même est fixée dans le code, l'appel système ne peut donc pas être détourné

**5.** *Question ouverte (2-3 lignes).* « Une revue qui ne produit rien de transmissible est une opinion. » Que doit contenir le rapport de revue, et pourquoi la mention « pourquoi c'est grave » est-elle indispensable ?

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. B.** La revue de sécurité lit ce que le code accepte, affiche et exécute : trois passes indépendantes, chacune avec sa question, chacune sur tout le fichier.
**Pourquoi :** c'est plus rapide qu'une relecture attentive ligne à ligne et surtout plus fiable — et la méthode se transmet à toute une équipe sans expertise du langage.

**2. C.** Un diff propre n'est pas un diff sûr : le code ajouté peut être irréprochable et supprimer, en passant, la seule vérification qui protégeait la route.
**Pourquoi :** un contrôle retiré est un changement de surface d'attaque — « la revue regarde aussi ce qui disparaît ».

**3. D.** Un problème sur une route ouverte à tous pèse plus lourd que le même problème sur une route réservée à l'administration interne, même si le correctif est identique.
**Pourquoi :** la priorisation suit l'exposition ; le rapport s'adresse à la personne qui va corriger et doit dire « pourquoi maintenant », sinon il finit dans la pile des choses qu'on fera plus tard.

**4. C.** C'est le quatrième signal du diff : une saisie peut choisir le fichier, le programme, l'argument. La forme de la commande devient pilotable depuis l'extérieur.
**Pourquoi :** la version sûre garde la commande fixe et passe la donnée comme paramètre (`os.chmod(nom_du_fichier, 0o666)`) — un appel système se traite comme une requête.

**5.** Attendu : le rapport donne la localisation (fichier, ligne), le problème (le pattern reconnu), la gravité (ce qui devient possible si personne ne corrige) et la proposition (correctif ou piste).
**Pourquoi :** « pourquoi c'est grave » fournit le contexte de décision et la priorisation ; un rapport qui dit « à corriger » sans le dire reste dans les cartons.

</details>

---

[← Chapitre précédent](05-dependances-et-configuration.md) · [Sommaire](Readme.md) · [Chapitre suivant →](07-securite-api.md)
