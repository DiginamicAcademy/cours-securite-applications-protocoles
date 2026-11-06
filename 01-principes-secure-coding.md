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
> l'exercice [Appliquer les principes du secure coding](tp/01-appliquer-les-principes.md) qui suit ce chapitre.
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
> chercher à corriger : la correction vient dans [l'exercice qui suit](tp/01-appliquer-les-principes.md).

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

*Formatif, jamais noté. Répondez sans relire le chapitre, puis cochez. Les réponses sont juste après le séparateur : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** « Chaque composant ne reçoit que le strict nécessaire, ni plus. » Quel principe énonce cette règle ?

- A. KISS (Keep It Simple, Stupid) : écrire simple
- B. Le moindre privilège : donner le moins possible
- C. La defense in depth : superposer les barrières
- D. Le fail-closed : refuser plutôt qu'accepter

- [ ] ✓ je savais

**2.** Un script de service tourne avec le compte de l'administrateur de la machine. Laquelle des trois questions du moindre privilège est bafouée ?

- A. Quelles données ?
- B. Quels droits ?
- C. Quel compte ?
- D. Aucune : un droit en trop est un détail de confort

- [ ] ✓ je savais

**3.** Dans la defense in depth appliquée au code, pourquoi un journal trop bavard annule-t-il le bénéfice des deux autres couches ?

- A. Parce qu'il ralentit le programme au moment de l'incident
- B. Parce qu'il redonne à tout le monde ce que les deux premières couches protégeaient
- C. Parce qu'il remplace la validation d'entrée
- D. Parce qu'il fait passer une donnée pour une instruction

- [ ] ✓ je savais

**4.** Le script d'export de la fromagerie échoue en silence et livre à la comptabilité un fichier vide, parfaitement semblable à une journée sans commande. Comment nomme-t-on ce comportement ?

- A. Fail-closed : le programme s'arrête et signale
- B. Fail-open : le programme continue et accepte par défaut
- C. Defense in depth : une barrière a cédé
- D. KISS : le programme faisait trop de choses

- [ ] ✓ je savais

**5.** *Question ouverte (2-3 lignes).* Un programme fail-open livre à la comptabilité un fichier vide qui a l'air normal ; un programme fail-closed bloque la journée. Pourquoi le second reste-t-il le comportement sûr ?

- [ ] ✓ je savais

---

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

---

[Sommaire](Readme.md) · [Chapitre suivant →](02-validation-et-injections.md)
