# Corrigé — Sécuriser un endpoint qui en dit trop

> Corrigé de [l'exercice « Sécuriser un endpoint qui en dit trop
> »](../09-securiser-endpoint-data.md). Comparez d'abord votre travail aux
> **étapes** ci-dessous : la méthode compte autant que le résultat.

---

## Partie 1 — Classifier les champs

**Éléments attendus :**

| Champ | Niveau | Pourquoi |
| --- | --- | --- |
| `id`, `numero_client` | interne | des identifiants opérationnels, sans danger immédiat, mais inutiles à diffuser |
| `nom` | confidentielle | une donnée personnelle, utile à l'écran, à ne pas exposer ailleurs |
| `courriel`, `telephone`, `adresse` | confidentielle | des coordonnées directes : leur fuite ouvre la voie au démarchage et à l'hameçonnage |
| `rib` | strictement confidentielle | un moyen de paiement : sa divulgation permet un prélèvement frauduleux |
| `contrat` | interne | des informations commerciales, gênantes si diffusées, sans gravité immédiate |
| `releves` | confidentielle | la consommation à 30 minutes près décrit les habitudes de vie du logement |
| `historique_factures` | confidentielle | des données financières personnelles |

**Les deux classements les plus élevés, justifiés :** le `rib` est strictement
confidentiel parce que sa divulgation cause un dommage **financier direct** et
immédiat ; les `releves` sont confidentiels parce qu'une série toutes les 30
minutes renseigne sur la présence et les habitudes du foyer — une fuite de ce
type a déjà servi à déterminer quand un logement est vide.

**Ce qu'il faut retenir :** le niveau ne se déduit pas du type technique
(chaîne, nombre) mais du **dommage** causé par la divulgation. Une série de
nombres anodins peut être plus sensible qu'un nom.

---

## Partie 2 — Minimiser la réponse

**Éléments attendus :**

```json
{
  "nom": "Camille Durand",
  "echeances": [
    {"date": "…", "montant": …}
  ]
}
```

Les valeurs des échéances viennent de la facturation ; la forme de la réponse,
elle, ne porte plus rien d'autre que l'écran n'affiche.

| Champ retiré | Où il devrait vivre |
| --- | --- |
| `id`, `numero_client` | nulle part dans une réponse client ; un endpoint interne de gestion, si besoin |
| `courriel`, `telephone`, `adresse` | un endpoint « mes coordonnées », appelé par l'écran qui les affiche |
| `rib` | un endpoint « mes moyens de paiement », avec masquage systématique |
| `contrat` | un endpoint « mon contrat » |
| `releves` | un endpoint « ma consommation », paginé, réservé à l'écran qui les trace |
| `historique_factures` | un endpoint « mes factures » |

**Erreurs fréquentes :** garder `id` et `numero_client` « au cas où » — ils ne
servent à l'écran que s'il les affiche ; ou vider la réponse de ses champs
sensibles mais garder `releves` complet, ce qui laisse la série la plus
bavarde dans la réponse.

**Sur la minimisation :** la question n'est pas « ce champ est-il dangereux ? »
mais « **cet écran en a-t-il besoin ?** ». Un endpoint par usage donne des
réponses minimales **et** des surfaces d'attaque séparées.

---

## Partie 3 — Masquer et pseudonymiser

**Éléments attendus :**

| Donnée | Traitement | Ce qui reste visible | Ce qui reste derrière |
| --- | --- | --- | --- |
| `rib` | masquage | `**** **** **** 0189` (les derniers caractères seulement) | le RIB (relevé d'identité bancaire) complet en base, accessible au seul
module de prélèvement |
| `releves` | pseudonymisation | FOYER (code interne du foyer), comme `FOYER-4021`, à la place du nom et du
numéro client | la table de correspondance `FOYER-4021` → client, dans un espace restreint |

**Points de vigilance :** masquer le RIB côté **réponse** ne suffit pas si le
module qui construit la réponse lit le RIB complet — le masquage se fait au
plus près de la source. Et la table de correspondance de la pseudonymisation
est elle-même une donnée personnelle : si l'application partenaire l'obtient,
la pseudonymisation ne protège plus rien.

**Sur les deux techniques :** masquer protège **l'affichage**, pseudonymiser
protège **l'analyse**. Les deux laissent la donnée exister — c'est le
compromis assumé quand l'usage exige de revenir à la personne.

---

## Partie 4 — Justifier au regard du RGPD

**Éléments attendus :**

| Question | Réponse attendue |
| --- | --- |
| **Finalité** | facturer la consommation réelle et permettre au client de suivre son usage — pas « améliorer nos services » en général |
| **Base légale** | l'exécution du contrat de fourniture d'énergie (la donnée sert à établir la facture) |
| **Sort après résiliation** | effacement ou archivage restreint selon l'obligation légale de conservation des factures ; la série détaillée des relevés, elle, n'a plus de finalité et disparaît |

**Erreurs fréquentes :** invoquer le consentement pour une donnée nécessaire à
la facturation — le consentement serait révocable, et la facturation ne l'est
pas ; ou répondre « on la garde 10 ans » sans distinguer la **facture** (retenue
par une obligation comptable) du **relevé détaillé** (sans objet une fois le
contrat clos).

**Sur la base légale :** elle se choisit **avant** de collecter, et elle
décide de la suite — notamment de ce qui se passe quand la personne part. Une
finalité floue produit toujours la même réponse : « on garde, au cas où ».

---

## Points à retenir

- Classifier, c'est juger le **dommage** de la divulgation — une série de
  mesures peut être plus sensible qu'un nom.
- Minimiser, c'est répondre à « **cet écran en a-t-il besoin ?** » — et donner
  un endpoint dédié à chaque usage qui, lui, en a besoin.
- Masquer protège l'affichage, pseudonymiser protège l'analyse — et la table de
  correspondance reste une donnée personnelle.
- La base légale se choisit avant la collecte : elle décide du **sort** de la
  donnée quand le contrat s'arrête.
