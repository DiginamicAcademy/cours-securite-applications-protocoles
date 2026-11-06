[Sommaire](Readme.md) · [Chapitre suivant →](02-validation-et-injections.md)

# Principes du secure coding — écrire pour que ça ne casse pas

> Le développeur de la fromagerie **DIGICHEESE** (la fromagerie du fil rouge) a ouvert le
> fichier de sa boutique en ligne : les failles étudiées lors des journées
> précédentes sont bien là, commentées, visibles. Le travail d'aujourd'hui n'est
> pas de les *voir* — c'est de les *corriger*, sans en introduire de nouvelles.
> Et pour corriger sans casser, il faut d'abord **écrire autrement**.

**Durée de lecture :** 40 min hors approfondissements facultatifs · **Prérequis :** les vulnérabilités web vues lors
des journées précédentes

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Décrire** les principes qui guident un code sûr : écrire simple, donner le
  moins possible, superposer les barrières.
- **Repérer** dans un script les endroits où l'un de ces principes est bafoué.
- **Appliquer** le moindre privilège à un composant : données lues, droits,
  compte d'exécution.
- **Choisir** le comportement d'un programme face à une erreur : refuser plutôt
  qu'accepter.

---

## I. Moindre privilège

Le secure coding n'est pas un framework qu'on ajoute par-dessus un programme :
c'est une **façon d'écrire**. Trois réflexes reviennent sans cesse :

- **Écrire simple** — KISS (Keep It Simple, Stupid) : un code court et lisible se
  relit, se corrige et se vérifie. Un code qui fait trop de choses finit par
  cacher ce qu'il a de dangereux.
- **Donner le moins possible** — le moindre privilège : chaque composant ne
  reçoit que le strict nécessaire, ni plus.
- **Superposer les barrières** — la defense in depth (défense en profondeur) :
  aucune mesure ne suffit seule ; on emploie plusieurs couches, pour qu'une
  erreur n'ouvre pas tout.

### Ce dont un composant a réellement besoin

Le moindre privilège se vérifie avec trois questions, à poser pour chaque script,
chaque service, chaque requête :

| Question | Ce qu'on se demande | L'excès classique |
| --- | --- | --- |
| **Quelles données ?** | quels champs sont réellement utiles à la tâche | lire toute une table « au cas où » |
| **Quels droits ?** | ce que le composant peut lire, écrire ou exécuter | un fichier d'export ouvert à tous les comptes de la machine |
| **Quel compte ?** | sous quelle identité le code s'exécute | un script de service qui tourne avec les droits de l'administrateur |

Un droit en trop n'est pas un détail de confort : c'est une porte qu'on laisse
ouverte le jour où le code est détourné.

---

## II. Defense in depth en code

Valider en entrée, maîtriser la sortie, journaliser sans exposer : la defense in
depth appliquée au code ne fait jamais confiance à **une seule** barrière. Le jour où elle cède, tout est ouvert.

Trois couches se complètent :

| Couche | Ce qu'on fait | Ce que ça arrête |
| --- | --- | --- |
| **En entrée** | vérifier le type, le format et la longueur de ce qui arrive | les valeurs absurdes et les surprises |
| **En sortie** | rendre à chaque système ce qu'il attend — du texte reste du texte | la confusion entre une donnée et une instruction |
| **Dans les journaux** | tracer ce qui s'est passé, sans y mettre les données ni les secrets | l'aveuglement quand vient l'incident |

Aucune couche ne remplace les autres : un journal trop bavard annule le bénéfice
des deux premières, parce qu'il redonne à tout le monde ce qu'on avait protégé.

---

## III. Fail-closed

Face à une erreur, un programme réagit en **fail-open** (il continue
et accepte par défaut) ou en **fail-closed** (il s'arrête, refuse et
signale).

| Ce qui arrive | Fail-open | Fail-closed |
| --- | --- | --- |
| Le programme rencontre une erreur | il continue et renvoie un résultat | il s'arrête et signale l'échec |
| La personne qui récupère le résultat | elle croit que tout va bien | elle sait qu'il faut vérifier |
| Le jour où l'erreur revient | on découvre le problème trop tard | on le voit tout de suite |

Pour la fromagerie, la différence est concrète : un script d'export qui échoue en
silence livre au service comptabilité un fichier vide, parfaitement semblable à
une journée sans commande. Un script fail-closed laisse un signe visible, et la
comptabilité sait qu'elle ne doit pas le reprendre.

---

### Exercice 1 — Appliquer les principes du secure coding (20 min)

#### Contexte

La fromagerie **DIGICHEESE** (la fromagerie du fil rouge) lance un programme de fidélité.
Chaque soir, un script exporte les commandes du jour dans un fichier que le
service comptabilité reprend le lendemain matin.

Marc, le développeur de la fromagerie, vous le montre. Le script tourne depuis la
mise en production avec le **même compte que la boutique en ligne**, et personne
ne s'est plaint :

```python
import os
import sqlite3

BASE = "/data/commandes.db"
SORTIE = "/data/export/fidelite.csv"

def exporter(jour):
    try:
        connexion = sqlite3.connect(BASE)
        curseur = connexion.cursor()
        curseur.execute(
            "SELECT * FROM commandes WHERE jour = ?", (jour,)
        )
        lignes = curseur.fetchall()
        fichier = open(SORTIE, "w")
        for ligne in lignes:
            print("ligne exportée :", ligne)
            fichier.write(";".join(str(champ) for champ in ligne) + "\n")
        fichier.close()
        connexion.close()
        os.system("chmod 666 " + SORTIE)
        return len(lignes)
    except Exception:
        return 0
```

Marc résume la situation : « Il marche, il est court, et la comptabilité
récupère son fichier tous les matins. »

---

#### Consignes

##### Partie 1 — Repérer les écarts aux principes

Listez les endroits du script où un principe du chapitre n'est pas respecté. Pour
chacun, dites **quel principe** est en jeu (moindre privilège, defense in depth,
fail-closed) et **pourquoi**.

##### Partie 2 — Appliquer le moindre privilège

Pour ce script d'export, répondez aux trois questions du chapitre : **quelles
données** doit-il réellement lire, **quels droits** doit-il avoir sur le fichier
produit, **quel compte** doit-il tourner ? Justifiez chaque réponse en une
phrase.

##### Partie 3 — Renforcer la defense in depth

Indiquez ce qu'il faut **valider en entrée**, ce qu'il faut **maîtriser en
sortie**, et ce qui doit rester une **seconde barrière** si la première cède.

##### Partie 4 — Rendre le script fail-closed

Décrivez le comportement attendu du script dans trois situations : le paramètre
`jour` est invalide, la base est injoignable, l'export est incomplet. Dans chaque
cas, que doit faire le script, et que doit savoir la personne qui récupère le
fichier ?

---

#### ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque écart que je cite est rattaché à un **principe** du chapitre, et pas
  seulement décrit.
- [ ] J'ai répondu aux **trois questions** du moindre privilège (données, droits,
  compte), et pas seulement à celle des données.
- [ ] Ma partie sur la defense in depth distingue bien **l'entrée, la sortie et la
  journalisation**.
- [ ] Pour chaque situation en erreur, j'ai dit **ce que fait le script** et **ce
  que sait la personne** qui récupère le fichier.
- [ ] Mes propositions ne se contentent pas d'interdire : elles disent **quoi
  faire à la place**.

---

#### Pour aller plus loin

*Facultatif.* Le service comptabilité reprend le fichier tôt le lendemain matin.
Si vous deviez ajouter **une seule** mesure pour qu'il détecte qu'un export est
incomplet, laquelle choisiriez-vous, et pourquoi ?

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Repérer les écarts aux principes

**Éléments attendus :**

| Écart dans le script | Principe en jeu | Pourquoi c'est un problème |
| --- | --- | --- |
| La requête lit **toutes les colonnes** de la table | Moindre privilège | Le service comptabilité n'a besoin ni des courriels, ni des modes de paiement, ni des adresses. |
| La commande qui termine le script rend le fichier lisible et modifiable par tous | Moindre privilège | N'importe quel compte de la machine peut lire ou réécrire l'export. |
| Le script tourne avec le compte de la boutique en ligne | Moindre privilège | Un export de comptabilité n'a pas besoin des droits de la boutique. |
| Le paramètre `jour` n'est contrôlé nulle part | Defense in depth | Une valeur inattendue donne un export faux ou vide, sans le moindre signal. |
| Chaque ligne exportée est affichée dans les journaux | Defense in depth | Les données clients se retrouvent là où elles n'ont rien à faire. |
| L'erreur est absorbée et le script renvoie `0` | Fail-closed | Une panne est traitée comme « aucune commande » : le programme accepte au lieu de refuser. |

**Ce qu'il faut retenir :** aucun de ces écarts n'est une erreur de syntaxe. Le
script *fonctionne* — c'est précisément ce qui les rend invisibles. Chacun donne
un peu plus que ce qui est nécessaire, ou accepte un peu plus que ce qui est
raisonnable.

---

#### Partie 2 — Appliquer le moindre privilège

**Éléments attendus :**

| Question | Réponse attendue |
| --- | --- |
| **Quelles données ?** | Le numéro de commande et le montant, rien d'autre. Le reste (courriel, mode de paiement, adresse) sort du fichier sans que personne ne le demande. |
| **Quels droits ?** | Un fichier que le service comptabilité peut lire, et que personne d'autre ne peut ni lire ni modifier : un dossier dédié, des droits restreints, aucune mise à disposition générale. |
| **Quel compte ?** | Un compte dédié à l'export, sans droits sur le reste de la boutique. Si le script est détourné un jour, il ne pourra rien faire d'autre qu'écrire son fichier. |

**Sur le moindre privilège :** on ne juge pas un script à ce qu'il sait faire,
mais à ce qu'on lui a **laissé** faire. Chaque droit retiré est une conséquence
d'incident en moins.

---

#### Partie 3 — Renforcer la defense in depth

**Éléments attendus :**

- **En entrée** — vérifier que `jour` est bien une date au format attendu, sur une
  longueur bornée, avant toute requête. Ce qui ne correspond pas est refusé, pas
  réparé en silence.
- **En sortie** — n'écrire dans le fichier que les champs nécessaires, et ne
  journaliser ni les lignes, ni les valeurs clients : seulement le fait que l'export
  a eu lieu, son ampleur et les erreurs.
- **Seconde barrière** — la requête est déjà paramétrée : une valeur piégée ne
  peut pas devenir une instruction. Et si le fichier tombe malgré tout entre de
  mauvaises mains, son contenu réduit limite ce qui fuite.

**Erreurs fréquentes :** valider l'entrée puis tout journaliser, ou maîtriser la
sortie puis faire confiance au premier contrôle. La defense in depth ne consiste
pas à empiler les mesures : elle consiste à ce qu'**aucune** mesure ne soit le
seul rempart.

---

#### Partie 4 — Rendre le script fail-closed

**Éléments attendus :**

| Situation | Ce que fait le script | Ce que sait la personne |
| --- | --- | --- |
| Le paramètre `jour` est invalide | il refuse de lancer l'export et le signale | que l'export n'a pas eu lieu, et pourquoi |
| La base est injoignable | il s'arrête, sans produire un fichier qui a l'air complet | qu'il ne faut pas reprendre le fichier |
| L'export est incomplet | il n'écrit pas un fichier qui ressemble à un export réussi | que le fichier est à écarter |

**Sur le fail-closed :** renvoyer `0` après une erreur, c'est répondre à la
question « combien de commandes ? » par une information fausse. Un programme sûr
distingue **une journée sans commande** d'**une journée qu'on n'a pas pu lire**,
et il le dit.

---

#### Points à retenir

- Le moindre privilège se décide sur **trois axes** : les données, les droits, le
  compte.
- La defense in depth se joue **en entrée, en sortie et dans les journaux** —
  aucune couche ne remplace les autres.
- Face à une erreur, un programme sûr **refuse et prévient** : c'est le
  fail-closed.
- Ce qui rend un script dangereux n'est pas qu'il casse : c'est qu'il **continue
  de marcher** en donnant de mauvaises informations.

</details>

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour terminer
la journée.*

- **Les principes de Saltzer et Schroeder** — leur article fondateur sur la
  protection de l'information énonce déjà le moindre privilège, l'économie de
  mécanisme ou la validation complète : ceux de ce chapitre en sont les héritiers
  directs.
- **OWASP** (Open Web Application Security Project) — ses guides de bonnes
  pratiques détaillent ces principes, langage par langage.
- **Les recommandations de sécurité de votre langage** — Python, Java ou PHP (Hypertext Preprocessor)
  publient chacun leurs propres guides : gestion des erreurs, validation des
  entrées, journalisation.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> L'analyse de ce script est conduite de bout en bout dans
> l'exercice 1 de ce chapitre, plus haut.
>
> 🧪 **Atelier rapide (5 min)**
>
> La fromagerie fait tourner chaque soir un script d'export des commandes, repris
> le lendemain par le service comptabilité. Il s'exécute avec le même compte que
> la boutique en ligne. Voici le script :
>
> ```python
> import os
> import sqlite3
>
> BASE = "/data/commandes.db"
> SORTIE = "/data/export/fidelite.csv"
>
> def exporter(jour):
>     try:
>         connexion = sqlite3.connect(BASE)
>         curseur = connexion.cursor()
>         curseur.execute(
>             "SELECT * FROM commandes WHERE jour = ?", (jour,)
>         )
>         lignes = curseur.fetchall()
>         fichier = open(SORTIE, "w")
>         for ligne in lignes:
>             print("ligne exportée :", ligne)
>             fichier.write(";".join(str(champ) for champ in ligne) + "\n")
>         fichier.close()
>         connexion.close()
>         os.system("chmod 666 " + SORTIE)
>         return len(lignes)
>     except Exception:
>         return 0
> ```
>
> Repérez les trois endroits où le **moindre privilège** est violé. Notez-les sans
> chercher à corriger : la correction vient dans l'exercice 1 de ce chapitre, plus haut.

---

## Points clés

- Le secure coding est une **façon d'écrire** : écrire simple, donner le moins
  possible, superposer les barrières.
- Le moindre privilège se décide avec trois questions : **quelles données, quels
  droits, quel compte**.
- La defense in depth se joue **en entrée, en sortie et dans les journaux** —
  aucune couche ne remplace les autres.
- Face à une erreur, un programme sûr **refuse et prévient** : c'est le
  fail-closed.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** « Chaque composant ne reçoit que le strict nécessaire, ni plus. » Quel principe énonce cette règle ?

- A. KISS (Keep It Simple, Stupid) : écrire simple
- B. Le moindre privilège : donner le moins possible
- C. La defense in depth : superposer les barrières
- D. Le fail-closed : refuser plutôt qu'accepter

**2.** Un script de service tourne avec le compte de l'administrateur de la machine. Laquelle des trois questions du moindre privilège est bafouée ?

- A. Quelles données ?
- B. Quels droits ?
- C. Quel compte ?
- D. Aucune : un droit en trop est un détail de confort

**3.** Dans la defense in depth appliquée au code, pourquoi un journal trop bavard annule-t-il le bénéfice des deux autres couches ?

- A. Parce qu'il ralentit le programme précisément au moment de l'incident, quand tout le monde attend
- B. Parce qu'il redonne à tout le monde ce que les deux premières couches protégeaient
- C. Parce qu'il se substitue à la validation d'entrée, qui devient alors inutile à écrire dans le code
- D. Parce qu'il apprend au programme à considérer une donnée venue de l'extérieur comme une instruction

**4.** Le script d'export de la fromagerie échoue en silence et livre à la comptabilité un fichier vide, parfaitement semblable à une journée sans commande. Comment nomme-t-on ce comportement ?

- A. Fail-closed : le programme s'arrête et signale
- B. Fail-open : le programme continue et accepte par défaut
- C. Defense in depth : une barrière a cédé
- D. KISS : le programme faisait trop de choses

**5.** *Question ouverte (2-3 lignes).* Un programme fail-open livre à la comptabilité un fichier vide qui a l'air normal ; un programme fail-closed bloque la journée. Pourquoi le second reste-t-il le comportement sûr ?

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. B.** « Donner le moins possible » est la définition du moindre privilège, le deuxième des trois réflexes du secure coding.
**Pourquoi :** KISS porte sur la simplicité du code, la defense in depth sur la superposition des barrières ; le strict nécessaire, c'est le privilège.

**2. C.** La question « quel compte ? » porte sur l'identité sous laquelle le code s'exécute : un script de service n'a pas besoin des droits de l'administrateur.
**Pourquoi :** un droit en trop n'est pas un détail de confort, c'est une porte qu'on laisse ouverte le jour où le code est détourné.

**3. B.** Les journaux doivent tracer ce qui s'est passé sans y mettre les données ni les secrets : trop bavards, ils redistribuent à tout le monde ce qui avait été protégé.
**Pourquoi :** aucune couche ne remplace les autres, et une couche défaillante peut annuler le bénéfice des deux premières.

**4. B.** Fail-open : le programme rencontre une erreur, continue et renvoie un résultat qui a l'air normal.
**Pourquoi :** la personne qui récupère le fichier croit que tout va bien ; en fail-closed, l'échec laisse un signe visible et la comptabilité sait qu'elle ne doit pas reprendre le fichier.

**5.** Attendu : le fail-open masque le problème — un résultat faux passe pour un résultat normal et on découvre l'erreur trop tard ; le fail-closed s'arrête, refuse et signale, donc on sait immédiatement qu'il faut vérifier.
**Pourquoi :** un échec visible coûte une journée perdue, un succès mensonger coûte des décisions prises sur des données fausses.

</details>

---

[Sommaire](Readme.md) · [Chapitre suivant →](02-validation-et-injections.md)
