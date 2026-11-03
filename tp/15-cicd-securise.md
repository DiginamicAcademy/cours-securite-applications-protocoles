# Exercice — Intégrer la sécurité dans une intégration continue

> 🟡 **À vous de jouer** · **Durée :** 50 min · **Lien :** chapitre
> [DevSecOps et traçabilité des dépendances](../15-devsecops.md)
> **Objectif :** écrire un workflow d'intégration continue qui exécute les trois
> familles de contrôles du chapitre, et décider, contrôle par contrôle, ce qui
> bloque une livraison.

---

## Contexte

**Nova Distribution** livre des produits alimentaires dans toute la région. Son
équipe data maintient le dépôt `flux-ventes` : des scripts Python d'extraction et
de transformation, un fichier `requirements.txt`, et une suite de tests. L'équipe
livre plusieurs fois par semaine, et chaque livraison manuelle de vérification
retarde la suivante.

Après un audit interne, la direction demande « la sécurité dans l'intégration
continue, sans paralyser l'équipe ». Vous êtes missionné pour poser les bases.

Le contexte technique à respecter :

| Élément | Valeur |
| --- | --- |
| Langage | Python 3.11 |
| Dépendances | un fichier `requirements.txt` |
| Actions du workflow | `actions/checkout` en v4, `actions/setup-python` en v5, `gitleaks/gitleaks-action` en v2 |
| Contrôles visés | SAST (analyse statique du code) avec `bandit`, SCA (analyse des composants) avec `pip-audit`, recherche de secrets avec `gitleaks` |
| Branche de livraison | `main` |

---

## Consignes

### Partie 1 — Rattacher chaque risque à son contrôle

L'audit a retenu trois incidents redoutés :

1. un mot de passe de base de données commité par mégarde dans un script ;
2. une bibliothèque de `requirements.txt` affectée par une faille publiée ;
3. une concaténation d'une saisie utilisateur dans une requête SQL (Structured
   Query Language, le langage de requête des bases relationnelles).

Pour chacun, indiquez **quel contrôle** le détecte, **à quel moment** il s'exécute
(avant le commit, à chaque modification, à la livraison) et **ce qu'il produit**
comme sortie exploitable.

### Partie 2 — Écrire le workflow

Rédigez le fichier `.github/workflows/securite.yml` : il se déclenche sur les
modifications de `main` et sur les demandes de fusion, puis exécute les trois
contrôles. Les commandes exactes sont libres — le chapitre en donne deux — mais
le workflow doit être complet, lisible et exécutable tel quel.

### Partie 3 — Décider les gates

Pour chaque contrôle, décidez s'il **bloque** la livraison ou **avertit**
seulement. Justifiez chaque décision par le coût des deux erreurs possibles :
laisser passer un problème, ou bloquer une livraison saine. Précisez enfin ce que
devient une alerte qui n'est pas bloquante : qui la traite, et quand.

### Partie 4 — Assurer la traçabilité

Le chapitre présente le SBOM (Software Bill of Materials, l'inventaire des
composants livrés). Pour ce dépôt, répondez aux quatre questions : **ce qu'il
contient**, **quand** il est produit, **où** il est conservé, et **à quoi** il
sert le jour où une faille est publiée sur une dépendance de `requirements.txt`.

---

## ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque risque de la partie 1 est rattaché à **un seul** contrôle, avec le
  moment où il s'exécute et sa sortie.
- [ ] Mon workflow contient les **trois** contrôles, se déclenche comme demandé,
  et se lit sans ambiguïté.
- [ ] Chaque gate de la partie 3 est **décidée** (bloquer ou avertir) et justifiée
  par le coût des deux erreurs.
- [ ] J'ai dit ce que devient une alerte non bloquante : **qui** la traite et
  **quand**.
- [ ] Ma partie 4 répond aux quatre questions, et pas seulement à celle du
  contenu.

---

## Pour aller plus loin

*Facultatif.* Le dépôt existe depuis trois ans, et son historique contient
peut-être des secrets commités bien avant l'arrivée de ces contrôles. Comment les
détecter, et que faire de ce que vous trouvez ?
