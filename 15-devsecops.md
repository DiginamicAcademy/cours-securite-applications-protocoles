# DevSecOps et traçabilité des dépendances — sécuriser la chaîne, pas seulement le code

> En décembre 2020, SolarWinds publie une mise à jour de sa plateforme de
> supervision Orion : un logiciel légitime, une mise à jour **signée**, distribuée
> à environ 18 000 organisations, dont des agences publiques et de grandes
> entreprises. Le code malveillant n'était pas dans l'application livrée aux
> clients — il avait été introduit **en amont**, dans la chaîne qui construit la
> mise à jour. Sécuriser le code sans sécuriser la chaîne qui le livre, c'est
> vérifier la serrure de sa porte tout en laissant la porte de service ouverte.

**Durée de lecture :** 70 min · **Prérequis :** les bases du développement et de
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

La sécurité arrivait autrefois en fin de projet : une revue, un audit, quelques
semaines avant la mise en production. Trop tard pour être économique — corriger
une conception coûte alors dix fois plus cher qu'au moment où on l'écrivait — et
trop tard pour être fiable, parce que la pression de la livraison fait sauter ce
qui reste à faire.

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

> 💡 **Astuce** —
> Un contrôle qui tourne en local avant le commit coûte quelques secondes et
> évite un aller-retour complet de pipeline. Les mêmes outils s'exécutent dans
> les deux endroits : en local pour aller vite, en CI pour ne rien oublier.

> 🧪 **Atelier rapide (10 min)**
>
> Écrivez un workflow GitHub Actions minimal qui exécute `pip-audit` (composants)
> et `bandit` (code) sur le dossier `lab/` du cours. Deux étapes suffisent :
>
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

> 🚨 **Piège à éviter** —
> Un dépôt public n'est pas la seule exposition. Un dépôt privé partagé avec un
> prestataire, un fork, une sauvegarde, un export : la clé commitée doit être
> considérée comme publique dès qu'elle a quitté votre machine.

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

### Monter la pression progressivement

Une équipe qui active tout en mode bloquant du jour au lendemain passe sa semaine
à éteindre des incendies. La méthode douce :

1. activer chaque contrôle en **avertissement** pendant deux semaines ;
2. mesurer le bruit : fausses alertes, alertes répétitives, alertes déjà connues ;
3. corriger le stock existant, puis **bloquer** sur ce qui est désormais propre ;
4. ne jamais régresser : ce qui est bloqué le reste.

C'est la même logique que la progression douce du parcours : on monte en pression
quand le niveau de pratique suit.

---

## III. Le SBOM : savoir ce qu'on embarque

### Le problème de Log4Shell

Le 9 décembre 2021, une faille critique est publiée dans Log4j, une bibliothèque
de journalisation très répandue dans l'écosystème Java. Elle porte la référence
CVE-2021-44228 — une CVE (Common Vulnerabilities and Exposures) est l'identifiant
public d'une faille publiée — et sera surnommée Log4Shell. En quelques heures,
des scans automatisés exploitaient la faille sur Internet. La question de chaque organisation fut la même : **sommes-nous
concernés, et où ?**

Pour beaucoup, la réponse a pris des jours — parce que la bibliothèque était
présente en transitive (importée par une autre bibliothèque, sans jamais avoir été
choisie explicitement), dans des applications dont personne n'avait l'inventaire.
Sans inventaire, pas de réponse rapide : on ne peut pas patcher ce qu'on ne sait
pas posséder.

### Ce qu'est un SBOM

Un SBOM (Software Bill of Materials, la liste des composants d'un logiciel) est à
une application ce qu'une liste d'ingrédients est à un produit alimentaire : chaque
composant, sa version, son origine, ses dépendances. Deux formats dominent :
CycloneDX et SPDX (Software Package Data Exchange, l'autre format d'inventaire),
tous deux en XML (Extensible Markup Language, un format de données structurées)
ou JSON.

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

> 🧭
> **Progression :** les contrôles disent « ce commit est-il dangereux ? », les
> gates décident « livre-t-on malgré tout ? », le SBOM répond « qu'avons-nous
> livré, exactement ? ». Les trois se complètent : le premier regarde l'instant,
> le troisième garde la mémoire.

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

---

## Points clés

- La sécurité s'intègre **à chaque commit** dans la CI, pas en fin de projet :
  trois familles de contrôles — SAST, SCA, recherche de secrets.
- Une **gate** arbitre entre bloquer et avertir selon le coût des deux erreurs ;
  les contrôles de sécurité restent séparés des contrôles de style.
- Un secret commité est **compromis** : on révoque d'abord, on corrige ensuite.
- Le **SBOM** est l'inventaire des composants livrés : sans lui, la publication
  d'une faille se traduit par des jours de recherche au lieu de minutes.
