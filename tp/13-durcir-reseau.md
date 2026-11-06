# Exercice — Durcir le réseau d'une petite entreprise

> **Nature :** TD (quatre gestes en séquence découverte) · **Durée :** 20 min · **Notion :** le durcissement réseau — repérer les flux, zoner, cloisonner
> 🟢 **Échauffement** · **Durée :** 20 min · **Lien :** chapitre
> [Protocoles réseau](../13-protocoles-reseau.md)
> **Objectif :** repérer, sur une description de réseau, les flux en clair et les
> expositions inutiles, puis proposer un durcissement réaliste.

---

## Contexte

Les **Éditions Belcastel** publient une vingtaine de titres par an et vendent leurs
livres en ligne. L'infrastructure a grandi au fil des besoins, sans plan de réseau.
Voici ce qui tourne aujourd'hui :

| Machine | Rôle | Ce qui est ouvert |
| --- | --- | --- |
| `web-boutique` | boutique en ligne | ports 80 et 443 depuis Internet |
| `admin-boutique` | back-office de la boutique | port 80, depuis Internet **et** depuis le réseau interne |
| `messagerie` | serveur de courrier interne | port 25, en clair, depuis Internet |
| `bdd-commandes` | base des commandes | port 3306 ouvert à tout le réseau interne |
| `sauvegarde` | copie des sauvegardes | partage de fichiers ouvert à tous les postes |
| poste du prestataire | maintenance à distance | port 22 depuis Internet, authentification par mot de passe |

Tout est sur **un seul réseau plat** : chaque machine peut joindre toutes les
autres. L'administrateur résume : « Ça marche depuis des années. »

---

## Consignes

### Partie 1 — Repérer les flux en clair et les expositions

Listez, dans le tableau ci-dessus, les lignes qui posent problème. Pour chacune,
dites s'il s'agit d'un **flux en clair**, d'une **exposition inutile** ou d'un
**accès trop large**, et pourquoi.

### Partie 2 — Regrouper les machines en zones

 Regroupez les six machines
en **trois zones** : une zone publique, une zone interne, une zone de données.
Justifiez chaque placement en une phrase.

### Partie 3 — Décrire les flux autorisés

Pour chaque zone, indiquez **qui a le droit de joindre qui**, et sur quel port.
Un flux non cité doit être refusé. Complétez ce tableau :

| De | Vers | Port | Autorisé ? |
| --- | --- | --- | --- |
| Internet | `web-boutique` | 443 | oui |
| Internet | `web-boutique` | 80 | à décider |
| `web-boutique` | `bdd-commandes` | 3306 | à décider |
| poste du prestataire | `admin-boutique` | 22 | à décider |
| postes du bureau | `sauvegarde` | partage | à décider |

### Partie 4 — Durcir les accès restants

Parmi les accès que vous maintenez, choisissez **deux durcissements** du chapitre
(chiffrement imposé, authentification par clé, restriction de comptes) et décrivez
la mesure exacte à appliquer, machine par machine.

---

## ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Chaque ligne que je signale est rattachée à une **catégorie** (flux en clair,
  exposition inutile, accès trop large), et pas seulement décrite.
- [ ] Mes **trois zones** sont nommées, et chaque machine y est placée avec une
  justification.
- [ ] Mon tableau de flux dit **oui ou non** pour chaque ligne, et tout ce qui n'est
  pas cité est refusé par défaut.
- [ ] Mes deux durcissements sont **applicables tels quels** : je dis quoi changer,
  sur quelle machine.
- [ ] Je n'ai pas proposé de mesure qui empêche la maintenance ou la sauvegarde de
  fonctionner.

---

## Pour aller plus loin

*Facultatif.* Si vous ne pouviez ajouter qu'**une seule** règle de pare-feu à ce
réseau, laquelle choisiriez-vous pour réduire le plus le risque, et pourquoi ?
