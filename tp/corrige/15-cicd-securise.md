# Corrigé — Intégrer la sécurité dans une intégration continue

> Corrigé de [l'exercice « Intégrer la sécurité dans une intégration
> continue »](../15-cicd-securise.md). Comparez d'abord votre travail aux
> **étapes** ci-dessous : la méthode compte autant que le résultat.

---

## Partie 1 — Rattacher chaque risque à son contrôle

**Éléments attendus :**

| Risque | Contrôle | Moment | Sortie exploitable |
| --- | --- | --- | --- |
| Un mot de passe commité | recherche de secrets (`gitleaks`) | à chaque modification, et sur l'historique du dépôt | le fichier et la ligne, pour savoir quelle clé révoquer |
| Une bibliothèque affectée | SCA (analyse des composants) avec `pip-audit` | à chaque modification, sur `requirements.txt` | le composant, sa version, la référence de la faille publiée |
| Une concaténation dans une requête | SAST (analyse statique du code) avec `bandit` | à chaque modification, sur les scripts | le fichier, la ligne, la règle enfreinte |

**Ce qu'il faut retenir :** chaque contrôle répond à une question différente, et
aucun ne détecte ce qui relève des deux autres. Un outil unique ne couvre jamais
les trois risques.

---

## Partie 2 — Écrire le workflow

**Éléments attendus :** un fichier `.github/workflows/securite.yml` de cette
forme :

```yaml
name: securite
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  controles:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Composants (SCA)
        run: |
          pip install pip-audit
          pip-audit -r requirements.txt

      - name: Code (SAST)
        run: |
          pip install bandit
          bandit -r scripts/

      - name: Secrets
        uses: gitleaks/gitleaks-action@v2
```

**Points de méthode :**

- Le déclenchement couvre **les deux portes d'entrée** du code : la modification
  directe de `main` et les demandes de fusion. Un workflow qui ne surveille qu'une
  des deux laisse l'autre ouverte.
- Un seul job suffit : les étapes s'exécutent dans l'ordre, et la première qui
  échoue arrête la suite. Séparer les contrôles en plusieurs jobs n'est utile que
  pour les exécuter en parallèle.
- Chaque étape installe son outil avant de lancer : un workflow qui suppose un
  outil déjà présent fonctionne sur le poste de la personne qui l'écrit, et pas
  ailleurs.

**Erreurs fréquentes :** oublier le déclenchement sur les demandes de fusion,
cibler le mauvais dossier (`lab/` au lieu de `scripts/`), ou écrire une étape qui
échoue silencieusement quand l'outil remonte une alerte.

---

## Partie 3 — Décider les gates

**Éléments attendus :**

| Contrôle | Décision | Justification par le coût des deux erreurs |
| --- | --- | --- |
| Recherche de secrets | **bloquer** | laisser passer coûte une clé compromise ; bloquer coûte quelques minutes de correction à la personne qui a commité |
| SCA, faille critique | **bloquer** | laisser passer expose une faille déjà publiée, donc déjà cherchée ; bloquer coûte une mise à jour de dépendance |
| SCA, faille moyenne ou faible | **avertir**, avec une tâche de suivi | bloquer paralyse les livraisons pour des risques modérés ; laisser sans suivi fait oublier le problème |
| SAST, règle dangereuse | **avertir** d'abord, bloquer quand le stock est propre | le code existant contient souvent des écarts anciens : bloquer tout de suite empêche de livrer quoi que ce soit |

**Ce que devient une alerte non bloquante :** elle devient une tâche de suivi dans
le gestionnaire de tickets de l'équipe, avec une personne nommée et une échéance.
Une alerte qui revient à chaque exécution sans jamais être traitée n'est pas une
alerte : c'est du bruit, et la gate doit alors durcir.

**Sur la montée en pression :** on commence en avertissement, on nettoie le stock
existant, puis on bloque. Ce qui est bloqué le reste — régresser revient à
réapprendre à ignorer les alertes.

---

## Partie 4 — Assurer la traçabilité

**Éléments attendus :**

- **Contenu** — chaque composant de `requirements.txt` avec sa version et son
  origine, ainsi que les dépendances qu'il entraîne lui-même.
- **Moment** — à chaque livraison, sur l'artefact réellement livré, et pas
  seulement sur le dépôt.
- **Conservation** — avec l'artefact, daté et versionné, dans le stockage de
  livraison de l'équipe. Un inventaire rangé à part et jamais mis à jour ne
  reflète rien.
- **Usage** — le jour où une faille est publiée, croiser la liste des versions
  affectées avec l'inventaire donne en minutes la liste des scripts à corriger,
  au lieu d'une recherche de plusieurs jours.

**Erreurs fréquentes :** générer l'inventaire une seule fois « pour l'audit », ou
le produire sur le dépôt au lieu de l'artefact livré — les deux donnent une
réponse fausse le jour où on en a besoin.

---

## Points à retenir

- Un risque, un contrôle, un moment d'exécution : les trois familles se
  complètent, aucune ne couvre les autres.
- Les **gates** se décident selon le coût des deux erreurs : laisser passer, ou
  bloquer une livraison saine.
- Une alerte non bloquante doit avoir **un responsable et une échéance**, sinon
  elle devient du bruit.
- Le **SBOM** transforme la question « sommes-nous concernés ? » en une liste de
  travail immédiatement exploitable.
