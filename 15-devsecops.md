[← Chapitre précédent](14-architecture-reseau.md) · [Sommaire](Readme.md) · [Chapitre suivant →](16-tests-securite.md)

# DevSecOps et traçabilité des dépendances — sécuriser la chaîne, pas seulement le code

> En décembre 2020, SolarWinds publie une mise à jour de sa plateforme de
> supervision Orion : un logiciel légitime, une mise à jour **signée**, distribuée
> à environ 18 000 organisations, dont des agences publiques et de grandes
> entreprises. Le code malveillant n'était pas dans l'application livrée aux
> clients — il avait été introduit **en amont**, dans la chaîne qui construit la
> mise à jour. Sécuriser le code sans sécuriser la chaîne qui le livre, c'est
> vérifier la serrure de sa porte tout en laissant la porte de service ouverte.

**Durée de lecture :** 55 min hors approfondissements facultatifs · **Prérequis :** les bases du développement et de
l'intégration continue, les vulnérabilités des journées précédentes

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Distinguer** les trois familles de contrôles automatisés : analyse du code,
  analyse des composants, recherche de secrets.
- **Écrire** un pipeline d'intégration continue qui exécute ces contrôles à chaque
  modification.
- **Décider**, contrôle par contrôle, ce qui bloque une livraison et ce qui se
  contente d'avertir.
- **Produire** un inventaire des composants d'une application pour répondre
  rapidement à la publication d'une faille.

---

## I. Les contrôles automatisés dans l'intégration continue

### Pourquoi si tôt

L'intégration continue (CI, l'exécution automatique des vérifications à chaque
modification du code) offre un meilleur endroit : **à chaque commit**, pendant que
le contexte est encore frais dans la tête de la personne qui écrit.

### Les trois familles de contrôles

| Famille | Ce qu'elle regarde | Outils courants | Ce qu'elle attrape |
| --- | --- | --- | --- |
| **SAST** (Static Application Security Testing, l'analyse statique du code) | le code source, sans l'exécuter | `bandit`, `semgrep` | concaténation dans une requête, désérialisation dangereuse, mots de passe en dur |
| **SCA** (Software Composition Analysis, l'analyse des composants) | les dépendances et leurs versions | `pip-audit`, `trivy` | une bibliothèque affectée par une faille publiée |
| **Recherche de secrets** | le code et l'historique des commits | `trufflehog`, `gitleaks` | une clé d'API, un jeton, un mot de passe commités |

Chaque famille répond à une question différente. SAST dit « votre code est-il
écrit dangereusement ? ». SCA dit « ce que vous importez est-il sain ? ». La
recherche de secrets dit « avez-vous laissé une clé traîner ? ». Aucune ne
remplace les deux autres.
> 🧪 **Atelier rapide (10 min)**
>
> Écrivez un workflow GitHub Actions minimal qui exécute `pip-audit` (composants)
> et `bandit` (code) sur le dossier `lab/` du cours. Deux étapes suffisent :


```yaml
name: controle-securite
on: [push]
jobs:
  controles:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
      - name: Composants
        run: pip install pip-audit && pip-audit
      - name: Code
        run: pip install bandit && bandit -r lab/
```

> Lancez les deux commandes dans un terminal sur votre projet : lisez la sortie.
> Laquelle des deux est la plus bavarde ? Laquelle trouveriez-vous la plus utile
> à bloquer sur ?

### Les secrets, un cas à part

Un secret découvert dans un commit est déjà compromis : l'historique de Git garde
tout, et quiconque a lu le dépôt a pu le copier. La bonne réaction n'est pas
d'effacer la ligne, c'est de **révoquer** la clé, puis de corriger. Un outil de
recherche de secrets qui alerte à la seconde du commit transforme un incident en
simple corvée de rotation de clé.


---

## II. Les gates : quand bloquer, quand avertir

Un contrôle qui alerte sans rien bloquer finit ignoré. Un contrôle qui bloque sur
tout finit désactivé. Entre les deux, une décision explicite : la **gate** (la
barrière qui décide si la livraison continue).

### Le principe de décision

La question n'est pas « cette alerte est-elle grave en théorie ? » mais « quel
est le coût d'une erreur dans les deux sens ? » :

| Situation | Coût de laisser passer | Coût de bloquer | Décision |
| --- | --- | --- | --- |
| Un secret détecté dans le commit | élevé — la clé est compromise | faible — personne ne commit un secret par hasard | **bloquer** |
| Une faille critique dans une dépendance | élevé — exploitable | moyen — il faut mettre à jour | **bloquer** |
| Une faille moyenne dans une dépendance | modéré | élevé si le correctif casse quelque chose | **avertir**, avec une tâche de suivi |
| Un style de code dangereux (SAST, sévérité faible) | faible à modéré | élevé — paralyse les petites corrections | **avertir** |
| Une règle de style ou de formatage | faible | très élevé | **ne pas mélanger** avec la sécurité |

> ⚠️ **Point d'attention** —
> Une gate qui bloque sur des alertes de style finit par être contournée : on
> désactive le job, on force le merge, on ajoute une exception permanente. Gardez
> les contrôles de sécurité **séparés** des contrôles de style, pour que la
> première reste crédible.

---

## III. Le SBOM : savoir ce qu'on embarque

### Ce qu'est un SBOM

Un SBOM (Software Bill of Materials, la liste des composants d'un logiciel) est à
une application ce qu'une liste d'ingrédients est à un produit alimentaire : chaque
composant, sa version, son origine, ses dépendances.

```bash
# Générer un inventaire avec syft, au format CycloneDX
syft dir:. -o cyclonedx-json > sbom.json
```

Quand une faille est publiée, l'exploitation de l'inventaire tient en une
question : « quelle application embarque la version affectée ? ». Réponse en
minutes au lieu de jours, et surtout **la liste des applications à patcher est
déjà faite**.

### Quand le produire, où le garder

| Moment | Ce qu'on fait |
| --- | --- |
| À chaque build | générer le SBOM de l'artefact livré, pas seulement du dépôt |
| À chaque livraison | le conserver **avec** l'artefact, daté et versionné |
| Quand une faille sort | le croiser avec la liste des versions affectées, obtenir la liste des systèmes touchés |

Un SBOM généré une fois et rangé dans un dossier ne sert à rien : c'est un
instantané, et les composants bougent à chaque livraison.


---

### Exercice 1 — Intégrer la sécurité dans une intégration continue (35 min)

#### Contexte

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

#### Consignes

##### Partie 1 — Rattacher chaque risque à son contrôle

L'audit a retenu trois incidents redoutés :

1. un mot de passe de base de données commité par mégarde dans un script ;
2. une bibliothèque de `requirements.txt` affectée par une faille publiée ;
3. une concaténation d'une saisie utilisateur dans une requête SQL (Structured
   Query Language, le langage de requête des bases relationnelles).

Pour chacun, indiquez **quel contrôle** le détecte, **à quel moment** il s'exécute
(avant le commit, à chaque modification, à la livraison) et **ce qu'il produit**
comme sortie exploitable.

##### Partie 2 — Écrire le workflow

Rédigez le fichier `.github/workflows/securite.yml` : il se déclenche sur les
modifications de `main` et sur les demandes de fusion, puis exécute les trois
contrôles. Les commandes exactes sont libres — le chapitre en donne deux — mais
le workflow doit être complet, lisible et exécutable tel quel.

##### Partie 3 — Décider les gates

Pour chaque contrôle, décidez s'il **bloque** la livraison ou **avertit**
seulement. Justifiez chaque décision par le coût des deux erreurs possibles :
laisser passer un problème, ou bloquer une livraison saine. Précisez enfin ce que
devient une alerte qui n'est pas bloquante : qui la traite, et quand.

##### Partie 4 — Assurer la traçabilité

Le SBOM (Software Bill of Materials, l'inventaire des
composants livrés). Pour ce dépôt, répondez aux quatre questions : **ce qu'il
contient**, **quand** il est produit, **où** il est conservé, et **à quoi** il
sert le jour où une faille est publiée sur une dépendance de `requirements.txt`.

---

#### ✅ Auto-évaluation

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

#### Pour aller plus loin

*Facultatif.* Le dépôt existe depuis trois ans, et son historique contient
peut-être des secrets commités bien avant l'arrivée de ces contrôles. Comment les
détecter, et que faire de ce que vous trouvez ?

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Rattacher chaque risque à son contrôle

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

#### Partie 2 — Écrire le workflow

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

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

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

#### Partie 3 — Décider les gates

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

#### Partie 4 — Assurer la traçabilité

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

#### Points à retenir

- Un risque, un contrôle, un moment d'exécution : les trois familles se
  complètent, aucune ne couvre les autres.
- Les **gates** se décident selon le coût des deux erreurs : laisser passer, ou
  bloquer une livraison saine.
- Une alerte non bloquante doit avoir **un responsable et une échéance**, sinon
  elle devient du bruit.
- Le **SBOM** (Software Bill of Materials, l'inventaire des composants) transforme la question « sommes-nous concernés ? » en une liste de
  travail immédiatement exploitable.

</details>

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour terminer
la journée.*

- **La signature des artefacts** — signer ce que la chaîne produit, et vérifier la
  signature avant déploiement, empêche la remplacement d'un binaire entre le build
  et la mise en production. C'est la leçon directe de l'affaire SolarWinds.
- **SLSA** (Supply-chain Levels for Software Artifacts, les niveaux de maturité de
  la chaîne de livraison) — un cadre public qui décrit, par niveaux, les garanties
  attendues sur l'origine et l'intégrité des artefacts. Un bon cap à long terme
  pour une chaîne de build.
- **La revue humaine des dépendances nouvelles** — ajouter une bibliothèque est un
  choix d'architecture. Une règle simple : toute nouvelle dépendance est examinée
  (activité du projet, mainteneurs, droits demandés) avant d'entrer.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Ce que la sécurité de fin de projet coûtait**
>
> La sécurité arrivait autrefois en fin de projet : une revue, un audit, quelques
> semaines avant la mise en production. Trop tard pour être économique — corriger
> une conception coûte alors dix fois plus cher qu'au moment où on l'écrivait — et
> trop tard pour être fiable, parce que la pression de la livraison fait sauter ce
> qui reste à faire.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> 💡 **Astuce** —
> Un contrôle qui tourne en local avant le commit coûte quelques secondes et
> évite un aller-retour complet de pipeline. Les mêmes outils s'exécutent dans
> les deux endroits : en local pour aller vite, en CI pour ne rien oublier.
>

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> 🚨 **Piège à éviter** —
> Un dépôt public n'est pas la seule exposition. Un dépôt privé partagé avec un
> prestataire, un fork, une sauvegarde, un export : la clé commitée doit être
> considérée comme publique dès qu'elle a quitté votre machine.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
>
> **Monter la pression progressivement**
>
>
> Une équipe qui active tout en mode bloquant du jour au lendemain passe sa semaine
> à éteindre des incendies. La méthode douce :
>
> 1. activer chaque contrôle en **avertissement** pendant deux semaines ;
> 2. mesurer le bruit : fausses alertes, alertes répétitives, alertes déjà connues ;
> 3. corriger le stock existant, puis **bloquer** sur ce qui est désormais propre ;
> 4. ne jamais régresser : ce qui est bloqué le reste.
>
> C'est la même logique que la progression douce du parcours : on monte en pression
> quand le niveau de pratique suit.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
>
> **Le problème de Log4Shell**
>
>
> Le 9 décembre 2021, une faille critique est publiée dans Log4j, une bibliothèque
> de journalisation très répandue dans l'écosystème Java. Elle porte la référence
> CVE-2021-44228 — une CVE (Common Vulnerabilities and Exposures) est l'identifiant
> public d'une faille publiée — et sera surnommée Log4Shell. En quelques heures,
> des scans automatisés exploitaient la faille sur Internet. La question de chaque organisation fut la même : **sommes-nous
> concernés, et où ?**
>
> Pour beaucoup, la réponse a pris des jours — parce que la bibliothèque était
> présente en transitive (importée par une autre bibliothèque, sans jamais avoir été
> choisie explicitement), dans des applications dont personne n'avait l'inventaire.
> Sans inventaire, pas de réponse rapide : on ne peut pas patcher ce qu'on ne sait
> pas posséder.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Les deux formats d'inventaire**
>
> Deux formats dominent :
> CycloneDX et SPDX (Software Package Data Exchange, l'autre format d'inventaire),
> tous deux en XML (Extensible Markup Language, un format de données structurées)
> ou JSON.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> 🧭
> **Progression :** les contrôles disent « ce commit est-il dangereux ? », les
> gates décident « livre-t-on malgré tout ? », le SBOM répond « qu'avons-nous
> livré, exactement ? ». Les trois se complètent : le premier regarde l'instant,
> le troisième garde la mémoire.

---

## Points clés

- La sécurité s'intègre **à chaque commit** dans la CI, pas en fin de projet :
  trois familles de contrôles — SAST, SCA, recherche de secrets.
- Une **gate** arbitre entre bloquer et avertir selon le coût des deux erreurs ;
  les contrôles de sécurité restent séparés des contrôles de style.
- Un secret commité est **compromis** : on révoque d'abord, on corrige ensuite.
- Le **SBOM** est l'inventaire des composants livrés : sans lui, la publication
  d'une faille se traduit par des jours de recherche au lieu de minutes.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** L'intégration continue signale : « une bibliothèque de l'application est affectée par une faille publiée ». Quelle famille de contrôles a produit ce signal ?

- A. Le SAST, qui analyse le code source
- B. Le SCA, qui analyse les dépendances et leurs versions
- C. La recherche de secrets, qui balaie le code et l'historique
- D. La gate, qui arbitre la livraison

**2.** Un développeur a committé une clé d'API dans le dépôt, privé de surcroît. Quelle est la bonne réaction ?

- A. Effacer la ligne au commit suivant : l'historique n'est plus relu par personne une fois la correction poussée
- B. Supprimer le dépôt et le recréer sans l'historique, pour que la ligne disparaisse de toute trace
- C. Révoquer la clé d'abord, puis corriger : un secret découvert dans un commit est déjà compromis
- D. Attendre la prochaine revue de code hebdomadaire pour en parler à l'équipe, qui en décidera à plusieurs

**3.** Une faille de sévérité moyenne est détectée dans une dépendance, et le correctif disponible risque de casser l'application. Que décide la gate, selon le chapitre ?

- A. Bloquer la livraison : toute faille doit être corrigée avant
- B. Avertir, avec une tâche de suivi : le coût de bloquer est élevé si le correctif casse quelque chose
- C. Ne rien signaler : une faille moyenne n'est pas un sujet de sécurité
- D. Mélanger l'alerte avec les contrôles de style pour tout traiter d'un coup

**4.** À quoi sert un SBOM, et quand le produire ?

- A. À lister les composants livrés (nom, version, origine) à chaque build et le garder avec l'artefact : on répond en minutes à « qui embarque la version affectée ? »
- B. À signer chaque artefact produit, afin d'empêcher qu'il soit remplacé entre le build et sa mise en production
- C. À bloquer les commits qui contiennent un secret ; l'outil se configure une fois pour toutes puis tourne seul
- D. À inventorier les dépendances une bonne fois au début du projet, puis à ranger la liste dans un dossier partagé

**5.** *Question ouverte (2-3 lignes).* « Un contrôle qui alerte sans rien bloquer finit ignoré. Un contrôle qui bloque sur tout finit désactivé. » Expliquez ce qu'est une gate, sur quoi se décide son réglage, et pourquoi les contrôles de style doivent rester séparés des contrôles de sécurité.

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. B.** SCA (Software Composition Analysis) regarde les dépendances et leurs versions — « ce que vous importez est-il sain ? ».
**Pourquoi :** le SAST analyse le code source sans l'exécuter, la recherche de secrets balaie code et historique de commits ; chaque famille répond à une question différente et aucune ne remplace les deux autres.

**2. C.** L'historique de Git garde tout, et quiconque a lu le dépôt a pu copier la clé — un dépôt privé partagé, un fork, une sauvegarde suffisent à l'exposer.
**Pourquoi :** la bonne réaction est de révoquer, puis de corriger ; un outil qui alerte à la seconde du commit transforme un incident en simple corvée de rotation de clé.

**3. B.** La question n'est pas « cette alerte est-elle grave en théorie ? » mais « quel est le coût d'une erreur dans les deux sens ? » : ici laisser passer coûte modéré, bloquer coûte élevé.
**Pourquoi :** un secret dans un commit ou une faille critique se bloquent ; une faille moyenne s'avertit avec une tâche de suivi — c'est l'arbitrage explicite de la gate.

**4. A.** Le SBOM (Software Bill of Materials) est la liste des composants d'un logiciel, comme une liste d'ingrédients : à chaque build on le génère pour l'artefact livré, à chaque livraison on le conserve daté et versionné.
**Pourquoi :** quand une faille sort, on le croise avec la liste des versions affectées et la liste des systèmes à patcher est déjà faite — un SBOM généré une fois et rangé ne sert à rien, c'est un instantané et les composants bougent.

**5.** Attendu : la gate est la barrière qui décide si la livraison continue ; le réglage se décide contrôle par contrôle selon le coût des deux erreurs (laisser passer / bloquer) — secret et faille critique : bloquer ; faille moyenne et SAST faible sévérité : avertir.
**Pourquoi :** une gate qui bloque sur du style finit contournée (on désactive le job, on force le merge) ; garder sécurité et style séparés préserve la crédibilité des contrôles de sécurité.

</details>

---

[← Chapitre précédent](14-architecture-reseau.md) · [Sommaire](Readme.md) · [Chapitre suivant →](16-tests-securite.md)
