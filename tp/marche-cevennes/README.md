# Marché des Cévennes — module à auditer

Module de gestion des commandes fourni pour le [TP intégrateur](../TP-INTEGRATEUR.md)
(étapes 1 à 3). Il est **volontairement fragile** : les trouver fait partie de l'exercice.

## Contenu

| Fichier | Rôle |
| --- | --- |
| `commandes.py` | L'application : cinq routes, une base SQLite créée au lancement. |
| `requirements.txt` | Les dépendances et leurs versions — l'étape 3 du TP part d'ici. |
| `factures/F-0001.pdf`, `factures/F-0002.pdf` | Deux factures de démonstration, utilisées par la route de téléchargement. |

## Lancer

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python commandes.py        # l'application écoute sur http://127.0.0.1:8000
```

Relancer `python commandes.py` est sans risque : la base ne se remplit qu'au premier
lancement et reste à trois commandes. Vous pouvez donc comparer l'avant et l'après d'une
correction sans que les chiffres bougent entre deux essais.

Si `pip install -r requirements.txt` échoue sur un Python récent, installez `Flask` et
`requests` sans épingler, en gardant `Jinja2==3.1.2`. Le module n'emploie que des API
stables de Flask (`Flask`, `jsonify`, `request`, `send_file`, `errorhandler`), présentes
dans toutes les versions récentes ; les versions figées du fichier datent de 2018-2021.

## Ce que vous verrez et qui n'est pas un bug du support

- **L'appel au prestataire de paiement échoue toujours.** Le module appelle
  `paiement-marche.invalid`, un domaine réservé qui ne peut pas être résolu — rien ne
  sort de votre machine. La route d'annulation part donc en erreur **après** avoir écrit
  en base. Regardez ce qui a déjà été modifié au moment où ça casse : c'est un constat.
- **Les erreurs renvoient la trace complète dans le corps de la réponse.** Ouvrez une
  route qui échoue et lisez ce que le client reçoit.
- **Le module n'a pas d'authentification.** Une simple en-tête HTTP suffit à choisir de
  quel client on parle.

## Observer proprement

Une recherche sur la route de liste accepte un texte libre et l'insère dans la requête.
Avant de conclure à une injection, sachez ceci : **le caractère `%` seul affiche déjà
toutes les lignes**, sans la moindre injection — c'est le joker de `LIKE`. « J'ai eu plus
de lignes que prévu » ne prouve donc rien.

Pour prouver quelque chose, il faut faire apparaître dans la réponse **une ligne que la
base ne contient pas**. C'est ce que cherche la première passe du chapitre 06 : une
méthode, pas une liste de payloads.

## À vous

Lancez l'application, essayez ses routes, lisez le code. Puis appliquez les trois passes
du chapitre 06 — entrées, sorties, appels système — avant toute correction.
