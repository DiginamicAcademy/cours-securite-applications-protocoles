# Corrigé — Appliquer les principes du secure coding

> Corrigé de [l'exercice « Appliquer les principes du secure coding »](../01-appliquer-les-principes.md).
> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte
> autant que le résultat.

---

## Partie 1 — Repérer les écarts aux principes

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

## Partie 2 — Appliquer le moindre privilège

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

## Partie 3 — Renforcer la defense in depth

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

## Partie 4 — Rendre le script fail-closed

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

## Points à retenir

- Le moindre privilège se décide sur **trois axes** : les données, les droits, le
  compte.
- La defense in depth se joue **en entrée, en sortie et dans les journaux** —
  aucune couche ne remplace les autres.
- Face à une erreur, un programme sûr **refuse et prévient** : c'est le
  fail-closed.
- Ce qui rend un script dangereux n'est pas qu'il casse : c'est qu'il **continue
  de marcher** en donnant de mauvaises informations.
