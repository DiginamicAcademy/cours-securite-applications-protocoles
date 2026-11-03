[Sommaire](Readme.md) · [Chapitre suivant →](02-validation-et-injections.md)

# Principes du secure coding — écrire pour que ça ne casse pas

> Le développeur de la fromagerie **DIGICHEESE** (la fromagerie du fil rouge) a ouvert le
> fichier de sa boutique en ligne : les failles étudiées lors des journées
> précédentes sont bien là, commentées, visibles. Le travail d'aujourd'hui n'est
> pas de les *voir* — c'est de les *corriger*, sans en introduire de nouvelles.
> Et pour corriger sans casser, il faut d'abord **écrire autrement**.

**Durée de lecture :** 50 min · **Prérequis :** les vulnérabilités web vues lors
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

On commence par le deuxième, le plus immédiat à appliquer dans un fichier de
code.

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

> 🧪 **Atelier rapide (5 min)**
>
> La fromagerie fait tourner chaque soir un script d'export des commandes, repris
> le lendemain par le service comptabilité. Il s'exécute avec le même compte que
> la boutique en ligne. Voici le script :

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

Repérez les trois endroits où le **moindre privilège** est violé. Notez-les sans
chercher à corriger : la correction vient dans [l'exercice qui
suit](tp/01-appliquer-les-principes.md).

---

## II. Defense in depth en code

Valider en entrée, maîtriser la sortie, journaliser sans exposer : la defense in
depth appliquée au code ne fait jamais confiance à **une seule** barrière. Le jour
où elle cède — un champ qu'on n'avait pas prévu, un appel qui échoue, une personne
qui se trompe — tout est ouvert.

Trois couches se complètent :

| Couche | Ce qu'on fait | Ce que ça arrête |
| --- | --- | --- |
| **En entrée** | vérifier le type, le format et la longueur de ce qui arrive | les valeurs absurdes et les surprises |
| **En sortie** | rendre à chaque système ce qu'il attend — du texte reste du texte | la confusion entre une donnée et une instruction |
| **Dans les journaux** | tracer ce qui s'est passé, sans y mettre les données ni les secrets | l'aveuglement quand vient l'incident |

Aucune de ces couches ne remplace les autres. Une validation d'entrée qui échoue
ne dispense pas de maîtriser ce qui sort ; un journal trop bavard annule le
bénéfice des deux autres, parce qu'il redonne à tout le monde ce qu'on avait
protégé.

---

## III. Fail-closed

Face à une erreur, un programme a deux façons de réagir :

- **fail-open** — il continue comme si de rien n'était, et accepte par défaut ;
- **fail-closed** — il s'arrête, refuse, et signale ce qui ne va pas.

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

[Sommaire](Readme.md) · [Chapitre suivant →](02-validation-et-injections.md)
