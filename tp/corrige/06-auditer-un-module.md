# Corrigé — Auditer un module de gestion des adhésions

> Corrigé de [l'exercice « Auditer un module de gestion des adhésions »](../06-auditer-un-module.md).
> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte
> autant que le résultat.

---

## Partie 1 — Appliquer les trois passes

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

## Partie 2 — Retracer l'anatomie d'un problème

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

## Partie 3 — Rédiger le rapport de dette

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

## Points à retenir

- Les trois passes — entrées, sorties, appels système — couvrent un module
  complet sans qu'il faille le comprendre en détail.
- Suivre la donnée de l'arrivée jusqu'à l'impact donne l'anatomie du problème,
  et donc le bon endroit pour corriger.
- Le rapport classe selon **l'exposition**, pas selon la facilité du correctif.
- Un rapport exploitable dit où, pourquoi c'est grave, quoi faire — et se lit
  sans son auteur.
