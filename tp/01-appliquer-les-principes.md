# Exercice — Appliquer les principes du secure coding

> 🟢 **Débutant** · **Durée :** 25 min · **Lien :** chapitre
> [Principes du secure coding](../01-principes-secure-coding.md)
> **Objectif :** auditer un script avec les principes du chapitre — moindre
> privilège, defense in depth, fail-closed — et proposer un comportement durci.

---

## Contexte

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

## Consignes

### Partie 1 — Repérer les écarts aux principes

Listez les endroits du script où un principe du chapitre n'est pas respecté. Pour
chacun, dites **quel principe** est en jeu (moindre privilège, defense in depth,
fail-closed) et **pourquoi**.

### Partie 2 — Appliquer le moindre privilège

Pour ce script d'export, répondez aux trois questions du chapitre : **quelles
données** doit-il réellement lire, **quels droits** doit-il avoir sur le fichier
produit, **quel compte** doit-il tourner ? Justifiez chaque réponse en une
phrase.

### Partie 3 — Renforcer la defense in depth

Indiquez ce qu'il faut **valider en entrée**, ce qu'il faut **maîtriser en
sortie**, et ce qui doit rester une **seconde barrière** si la première cède.

### Partie 4 — Rendre le script fail-closed

Décrivez le comportement attendu du script dans trois situations : le paramètre
`jour` est invalide, la base est injoignable, l'export est incomplet. Dans chaque
cas, que doit faire le script, et que doit savoir la personne qui récupère le
fichier ?

---

## ✅ Auto-évaluation

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

## Pour aller plus loin

*Facultatif.* Le service comptabilité reprend le fichier tôt le lendemain matin.
Si vous deviez ajouter **une seule** mesure pour qu'il détecte qu'un export est
incomplet, laquelle choisiriez-vous, et pourquoi ?
