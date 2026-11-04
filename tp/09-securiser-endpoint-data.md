# Exercice — Sécuriser un endpoint qui en dit trop

> **Nature :** exercice · **Durée :** 30 min · **Notion :** les données sensibles — classification, minimisation, masquage
> 🟡 **À vous de jouer** · **Durée :** 30 min · **Lien :** chapitre [Données
> sensibles](../09-donnees-sensibles.md)
> **Objectif :** appliquer la minimisation et le masquage sur un endpoint
> réellement trop bavard, et justifier les choix au regard du RGPD.

---

## Contexte

Un fournisseur d'énergie met à jour son portail client. L'écran « Échéancier de
paiement » affiche trois informations : le nom du client, ses prochaines
échéances et les montants dus. L'endpoint qui alimente cet écran a été écrit
pendant la refonte, « en reprenant la fiche client complète, comme ça on aura
tout ce qu'il faut ».

Voici ce que renvoie actuellement l'endpoint GET (lecture d'une ressource),
`/compte/{id}` :

```json
{
  "id": 4021,
  "numero_client": "CL-4021",
  "nom": "Camille Durand",
  "courriel": "c.durand@example.fr",
  "telephone": "0612345678",
  "adresse": "12 rue des Lilas, 34000 Montpellier",
  "rib": "FR7630006000011234567890189",
  "contrat": {
    "offre": "Tarif Vert",
    "puissance_souscrite": 9
  },
  "releves": [
    {"horodatage": "2026-04-13T00:00", "kwh": 1.2},
    {"horodatage": "2026-04-13T00:30", "kwh": 0.9}
  ],
  "historique_factures": [
    {"date": "2026-03-05", "montant": 84.10, "statut": "payée"},
    {"date": "2026-02-05", "montant": 91.30, "statut": "payée"}
  ]
}
```

Le fournisseur relève la consommation **toutes les 30 minutes** : la série
`releves` est donc longue, et elle décrit la vie quotidienne du logement
(quand la personne se lève, quand elle est absente). L'endpoint est appelé par
le portail web, mais aussi par une application partenaire d'aide à la gestion
de l'énergie.

---

## Consignes

### Partie 1 — Classifier les champs

Classez chaque champ de la réponse dans les quatre niveaux du chapitre
(publique, interne, confidentielle, strictement confidentielle). Justifiez en
une phrase les deux classements les plus élevés.

### Partie 2 — Minimiser la réponse

Réécrivez la réponse de `GET /compte/{id}` pour qu'elle porte **exactement** ce
dont l'écran d'échéancier a besoin. Listez ensuite les champs retirés et, pour
chacun, l'usage qui justifierait — le cas échéant — un endpoint dédié.

### Partie 3 — Masquer et pseudonymiser

L'application partenaire a besoin d'afficher « le RIB (relevé d'identité
bancaire) du prélèvement » sans le montrer en entier, et d'analyser la consommation par profil sans que l'identité des clients
apparaisse. Décrivez le masquage du RIB et la pseudonymisation des
relevés : que devient chaque donnée, et que garde-t-on derrière ?

### Partie 4 — Justifier au regard du RGPD

Pour la série `releves`, répondez aux trois questions : quelle est la
**finalité** de sa collecte, quelle **base légale** la justifie, et que
devient-elle quand le contrat est résilié ? Une réponse par question, une à
deux phrases chacune.

---

## ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque champ de la réponse originale est **classé**, sans exception.
- [ ] Ma réponse minimisée ne contient **que** ce dont l'écran a besoin — j'ai
  vérifié champ par champ.
- [ ] Pour chaque champ retiré, j'ai dit **où il devrait vivre** (endpoint
  dédié, jamais nulle part).
- [ ] Mon masquage du RIB laisse **impossible** la lecture du numéro complet
  depuis la réponse.
- [ ] Ma partie RGPD nomme une **finalité**, une **base légale** et un **sort**
  de la donnée — pas seulement « c'est sensible ».

---

## Pour aller plus loin

*Facultatif.* Le fournisseur veut proposer un service de « comparaison avec les
foyers similaires » à partir des relevés. Sans écrire de code, décrivez comment
produire ce service **sans** que les données individuelles de consommation
quittent le système.
