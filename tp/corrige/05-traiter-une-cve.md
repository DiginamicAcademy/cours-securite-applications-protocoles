# Corrigé — Traiter une CVE sur son propre projet

> Corrigé de [l'exercice « Traiter une CVE sur son propre projet »](../05-traiter-une-cve.md).
> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte
> autant que le résultat.

---

## Partie 1 — Lire l'avis

| Champ | Ce qu'il permet de décider |
| --- | --- |
| **Identifiant** | retrouver l'avis dans les bases, le citer dans vos propres documents |
| **Composant** | savoir quelle partie du projet est concernée |
| **Versions affectées** | dire si votre figeage est concerné, sans rien installer |
| **Mécanisme** | comprendre ce qui permet l'exploitation, et donc si vous l'exposez |
| **Impact** | estimer ce qui devient possible si personne ne corrige |

L'identifiant CVE (Common Vulnerabilities and Exposures) sert de référence
commune entre les bases ; l'avis GHSA (GitHub Security Advisory) est la
publication de l'éditeur, avec le détail du correctif.

Ce que l'avis **ne** dit pas, et que le projet doit établir lui-même :

- si la fonctionnalité concernée est réellement utilisée par votre code ;
- si les entrées qui déclenchent la faille sont atteignables depuis
  l'extérieur ;
- quel est l'impact métier, compte tenu des données traitées.

C'est la différence entre l'avis de sécurité et l'avis d'exposition : le premier
décrit une bibliothèque, le second décrit votre situation.

---

## Partie 2 — Situer l'exposition

Le code du service utilise le filtre concerné pour assembler les attributs d'une
liste de résultats, et une des clés du dictionnaire vient de la requête. Le
mécanisme de l'avis est donc atteignable : la clé n'est pas validée, et le filtre
l'insère telle quelle dans la balise.

Conclusion en deux phrases : le service est exposé, et l'exposition est
directement déclenchable depuis la page de recherche. La simple présence de la
dépendance ne l'aurait pas établi — c'est l'usage du filtre, avec une clé venue
de l'extérieur, qui tranche.

---

## Partie 3 — Corriger

Deux volets, indissociables :

```text
Jinja2==3.1.3
```

Le composant est monté vers la version corrigée. Et la validation des clés est
ajoutée côté applicatif :

```python
CLES_AUTORISEES = {"data-nom", "class"}


def valider_attributs(attributs):
    for cle in attributs:
        if cle not in CLES_AUTORISEES:
            raise ValueError("cle d'attribut non autorisee")
    return attributs
```

Le premier volet ferme la faille connue ; le second empêche qu'un mécanisme
voisin ne se reproduise sur une version ultérieure. S'en tenir à la mise à jour
aurait laissé la porte ouverte à la faille suivante du même type.

La vérification porte sur les deux points : les tests existants passent
toujours, et le cas décrit dans l'avis — une clé contenant des espaces — ne
produit plus d'attribut parasite dans la page.

---

## Partie 4 — Rédiger l'avis d'exposition

Un avis interne tient en quelques lignes :

> **Objet** — vulnérabilité sur une dépendance du service d'export.
>
> **Situation** — le composant de mise en page est affecté par l'avis
> CVE-2024-22195, dans la version figée par le projet.
>
> **Exposition** — la fonctionnalité concernée est utilisée, avec une clé
> fournie par la requête : le service est exposé.
>
> **Correction** — montée du composant vers la version corrigée, et validation
> des clés côté applicatif.
>
> **Vérification** — les tests passent, le cas de l'avis ne fonctionne plus.

Cet avis se passe de son auteur : quelqu'un qui reprend le sujet comprend la
situation sans avoir à interroger l'équipe.

---

## Points à retenir

- La réponse suit quatre temps : **lire, situer, corriger, vérifier** —
  corriger avant de lire conduit à des mises à jour qui cassent le service.
- L'avis de sécurité décrit la bibliothèque ; l'avis d'exposition décrit
  **votre** projet, et c'est lui qui décide de l'urgence.
- La mise à jour ferme la faille connue ; la validation des entrées ferme la
  suivante.
- La vérification a deux volets : les tests passent, et le cas de l'avis ne
  passe plus.
