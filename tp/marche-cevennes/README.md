# Marché des Cévennes — module à auditer

Module de gestion des commandes fourni pour le [TP intégrateur](../TP-INTEGRATEUR.md)
(étapes 1 à 3). Il est **volontairement fragile** : les trouver fait partie de l'exercice.

## Lancer

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python commandes.py        # l'application écoute sur http://127.0.0.1:8000
```

## À vous

Lancez l'application, essayez ses routes, lisez le code. Puis appliquez les trois
passes du chapitre 06 — entrées, sorties, appels système — avant toute correction.
