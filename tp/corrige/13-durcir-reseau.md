# Corrigé — Durcir le réseau d'une petite entreprise

> Corrigé de [l'exercice « Durcir le réseau d'une petite entreprise »](../13-durcir-reseau.md).
> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte
> autant que le résultat.

---

## Partie 1 — Repérer les flux en clair et les expositions

**Éléments attendus :**

| Ligne | Catégorie | Pourquoi c'est un problème |
| --- | --- | --- |
| `messagerie`, port 25 en clair | Flux en clair | Le courrier et les identifiants de connexion transitent lisibles par quiconque est sur le chemin. |
| `admin-boutique`, port 80 | Flux en clair | Le back-office est administré sans chiffrement : mots de passe et jetons de session circulent en clair. |
| `admin-boutique`, depuis Internet | Exposition inutile | Un back-office n'a rien à faire accessible depuis l'extérieur : c'est une surface d'attaque offerte. |
| poste du prestataire, port 22 depuis Internet | Exposition inutile + accès trop large | Un accès d'administration ouvert sur Internet avec un mot de passe est la combinaison la plus recherchée. |
| `bdd-commandes`, port 3306 pour tout le réseau | Accès trop large | N'importe quel poste compromis peut joindre la base des commandes directement. |
| `sauvegarde`, partage ouvert à tous | Accès trop large | La copie de sécurité vaut ce que vaut son accès : ouverte à tous, elle est compromise dès le premier poste infecté. |

**Ce qu'il faut retenir :** aucun de ces problèmes n'est une panne. Tout
fonctionne, et c'est exactement ce qui les rend invisibles — chaque ligne donne
un peu plus d'accès que ce que le besoin justifie.

---

## Partie 2 — Regrouper les machines en zones

**Éléments attendus :**

| Zone | Machines | Justification |
| --- | --- | --- |
| **Zone publique** (la zone tampon, ou DMZ — demilitarized zone) | `web-boutique` | Seule machine destinée à être jointe depuis Internet : elle reçoit les coups, elle ne doit rien contenir de sensible. |
| **Zone interne** | `messagerie`, `admin-boutique`, les postes du bureau | Usage interne : ces machines n'ont pas à être visibles depuis l'extérieur. |
| **Zone de données** | `bdd-commandes`, `sauvegarde` | Ce qu'il y a de plus précieux : isolé, joignable seulement par les machines qui en ont besoin. |

**Sur la segmentation :** le but n'est pas de multiplier les machines, mais de
faire en sorte qu'un poste compromis ne mène pas automatiquement aux données. Le
prestataire, lui, n'appartient à aucune zone : son accès doit être traité comme un
flux venant de l'extérieur.

---

## Partie 3 — Décrire les flux autorisés

**Éléments attendus :**

| De | Vers | Port | Autorisé ? | Raison |
| --- | --- | --- | --- | --- |
| Internet | `web-boutique` | 443 | oui | c'est le service public, chiffré. |
| Internet | `web-boutique` | 80 | uniquement pour rediriger vers le 443 | le clair ne sert qu'à renvoyer vers le chiffré, jamais à servir du contenu. |
| `web-boutique` | `bdd-commandes` | 3306 | oui | la boutique doit lire et écrire les commandes ; c'est le seul chemin vers la base. |
| poste du prestataire | `admin-boutique` | 22 | oui, mais depuis un point d'entrée unique et avec une clé | la maintenance doit rester possible, sans exposition directe. |
| postes du bureau | `sauvegarde` | partage | non | les postes n'ont rien à faire sur la copie de sécurité : seul le serveur qui produit les sauvegardes y écrit. |

**Erreurs fréquentes :** autoriser « tout le réseau interne » vers la zone de
données par facilité, ou oublier de refuser explicitement ce qui n'est pas cité.
Une règle de pare-feu qui n'autorise rien par défaut est la seule qui tient dans
le temps.

---

## Partie 4 — Durcir les accès restants

**Éléments attendus** (deux mesures parmi celles du chapitre) :

- **Authentification par clé sur le poste du prestataire** — désactiver
  l'authentification par mot de passe sur le port 22, installer une clé publique
  par intervenant, et journaliser les connexions. Un mot de passe deviné ne donne
  alors plus rien.
- **Chiffrement imposé sur la boutique** — faire répondre `web-boutique` avec
  l'en-tête qui interdit le repli en clair, et faire du port 80 une simple
  redirection vers le port 443. L'administration passe alors obligatoirement par
  le chiffré.
- **Compte dédié pour la maintenance** — le prestataire ne reçoit pas un compte
  administrateur général, mais un compte limité à `admin-boutique`, avec les
  seuls droits nécessaires à sa mission.

**Sur le choix des mesures :** un durcissement qui empêche la maintenance de
fonctionner sera désactivé à la première urgence. Les mesures ci-dessus gardent
chaque usage légitime — elles retirent seulement ce que personne n'utilisait.

---

## Points à retenir

- Un réseau plat transforme chaque poste compromis en accès à tout : la
  **segmentation** casse cette chaîne.
- Les flux en clair (courrier, administration) livrent identifiants et contenus à
  quiconque est sur le chemin : le chiffrement se **décide**, il n'arrive pas
  seul.
- Une exposition inutile (back-office depuis Internet, accès d'administration
  ouvert) est un risque que personne n'a demandé : la fermer ne casse rien.
- Par défaut, **tout ce qui n'est pas explicitement autorisé est refusé**.
