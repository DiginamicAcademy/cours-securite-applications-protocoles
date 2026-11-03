# Traiter une CVE sur son propre projet

> 🟡 **Intermédiaire** · **Durée :** 40 min · **Lien :** chapitre
> [Dépendances et configuration](../05-dependances-et-configuration.md)
> **Objectif :** traiter une vulnérabilité signalée sur une dépendance de votre
> projet — lire l'avis, situer l'exposition, corriger, vérifier — et rédiger un
> avis d'exposition interne.

---

## Contexte

Votre équipe maintient un petit service d'export de rapports, utilisé par le
service marketing pour produire des fichiers de suivi. Le lundi matin, l'analyse
automatique des dépendances signale une vulnérabilité, décrite dans un avis
GHSA (GitHub Security Advisory) et référencée par un identifiant CVE (Common
Vulnerabilities and Exposures). Le fichier de figeage du
projet contient ceci :

```text
Flask==3.0.0
Jinja2==3.1.2
MarkupSafe==2.1.5
```

L'avis de sécurité, publié par l'éditeur, dit ceci :

| Champ | Contenu |
| --- | --- |
| **Identifiant** | CVE-2024-22195 — avis GHSA-h5c8-rqwp-cp95 |
| **Composant** | Jinja2, le moteur de gabarit |
| **Versions affectées** | antérieures à 3.1.3 |
| **Mécanisme** | le filtre `xmlattr` accepte des clés d'attribut contenant des espaces |
| **Impact** | injection de balise dans la page produite |

Le service utilise ce filtre pour assembler les attributs d'une liste de
résultats, à partir d'un dictionnaire dont une clé est fournie par la requête.

---

## Consignes

### Partie 1 — Lire l'avis

Reprenez les cinq champs de l'avis et dites, pour chacun, ce qu'il permet de
décider. Identifiez ce que l'avis **ne** dit pas et que vous devez établir
vous-même.

### Partie 2 — Situer l'exposition

Cherchez dans le code du service si le filtre concerné est utilisé, et si les
clés du dictionnaire qu'il reçoit peuvent venir de l'extérieur. Concluez, en
deux phrases, sur l'exposition réelle du service — la présence de la
dépendance ne suffit pas à la trancher.

### Partie 3 — Corriger

Appliquez le correctif : montez le composant vers la version corrigée, et
validez les clés côté applicatif pour que le mécanisme ne puisse pas se
reproduire sur une version ultérieure. Reconstruisez le service, puis vérifiez
que le cas décrit dans l'avis ne fonctionne plus.

### Partie 4 — Rédiger l'avis d'exposition

Rédigez un court avis interne, à destination de l'équipe et de la direction des
systèmes d'information : la situation, l'exposition établie, la correction
appliquée, la vérification effectuée. Une dizaine de lignes suffit.

---

## ✅ Auto-évaluation

- [ ] Je sais dire ce que chaque champ de l'avis apporte à la décision.
- [ ] J'ai identifié ce que l'avis ne dit pas et que le projet doit établir.
- [ ] J'ai vérifié si le filtre concerné est réellement utilisé par le service.
- [ ] Le composant est monté vers la version corrigée.
- [ ] Les clés sont validées côté applicatif, indépendamment de la version.
- [ ] J'ai vérifié que le cas de l'avis ne fonctionne plus après correction.
- [ ] Mon avis d'exposition tient en une dizaine de lignes et se passe de moi
      pour être compris.

---

## Pour aller plus loin

*Facultatif — ne bloque pas la suite du parcours.*

La mise à jour complète n'était pas possible immédiatement : le service dépend
d'une bibliothèque qui exige une version antérieure. Décrivez la marche à suivre
pour rétro-patcher le composant concerné, ce que cela engage pour la
maintenance, et la date à laquelle ce choix devra être revu.
