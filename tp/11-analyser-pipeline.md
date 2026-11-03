# Exercice — Analyser les risques d'un pipeline de données

> 🔵 **Intégration** · **Durée :** 55 min · **Lien :** chapitre [Pipelines de
> données](../11-pipelines-data.md)
> **Objectif :** analyser les risques de fuite et d'intégrité d'un pipeline ETL (Extract, Transform, Load)
> étape par étape, et prioriser des recommandations.

---

## Contexte

Une chaîne de librairies compte **42 magasins**. Chaque caisse enregistre les
ventes de la journée ; chaque nuit, un pipeline alimente l'entrepôt de données
qui sert aux tableaux de bord de la direction. Depuis le début de l'année, un
export **quotidien** part vers un prestataire d'e-mailing, qui anime la
newsletter de la fidélité.

Voici le flux, tel qu'il est documenté :

1. **Extraction** — un job d'orchestration (type Airflow) se connecte aux bases
   des 42 magasins et exporte les ventes du jour en fichiers CSV (Comma-Separated Values), avec un
   compte de service unique créé « au début du projet », administrateur sur
   toutes les bases.
2. **Dépôt intermédiaire** — les fichiers sont poussés dans un stockage objet
   (type MinIO), dans un compartiment unique où le prestataire d'e-mailing
   dépose aussi ses fichiers de réponses.
3. **Transformation** — un script Python nettoie, déduplique et agrège les
   ventes, puis charge l'entrepôt.
4. **Restitution** — les tableaux de bord lisent l'entrepôt ; l'export
   quotidien vers le prestataire part depuis le même script de transformation.

La semaine dernière, un fichier CSV malformé (un séparateur différent) a fait
planter le job de transformation. **Deux jours de ventes** sont manquants dans
l'entrepôt — personne ne s'en est aperçu avant qu'un responsable de magasin
signale un tableau de bord faux.

---

## Consignes

### Partie 1 — Décrire le flux

Reprenez les quatre étapes et, pour chacune, notez : les **données** qui y
circulent, les **acteurs** (comptes, systèmes, personnes) qui y accèdent, et
la **frontière** franchie (ce qui passe d'un système à un autre). Un tableau à
quatre lignes suffit.

### Partie 2 — Analyser les risques

Pour chaque étape, identifiez **un risque de fuite** et **un risque
d'intégrité**. Appuyez-vous sur les faits du contexte (le compte administrateur,
le compartiment partagé, l'incident du fichier malformé) — pas sur des cas
génériques.

### Partie 3 — Recommander

Proposez des mesures pour : les **comptes de service**, les **flux** entre les
briques, les **tests de données**, le **cloisonnement** du stockage et de
l'entrepôt, et la **traçabilité** de l'envoi au prestataire. Une mesure par
sujet, formulée comme une action concrète.

### Partie 4 — Prioriser

Classez vos mesures en **trois actions** à mener en premier, de la plus urgente
à la moins urgente. Chaque action est justifiée par le dommage qu'elle évite.

---

## ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque étape du flux nomme ses **données**, ses **acteurs** et sa
  **frontière**.
- [ ] Pour chaque étape, j'ai donné **un risque de fuite et un risque
  d'intégrité** — pas un seul des deux.
- [ ] Mes risques s'appuient sur les **faits du contexte**, pas sur des
  généralités.
- [ ] Mes mesures couvrent les **cinq sujets** demandés (comptes, flux, tests,
  cloisonnement, traçabilité).
- [ ] Mes trois actions prioritaires sont **justifiées par un dommage** évité.

---

## Pour aller plus loin

*Facultatif.* Le prestataire d'e-mailing propose de déposer ses fichiers de
réponses dans le même compartiment que les exports, « pour simplifier ».
Sans écrire de code, décrivez ce que ce partage change pour la sécurité du
pipeline, et l'alternative que vous proposeriez.
