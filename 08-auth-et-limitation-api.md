# Auth et limitation d'API — qui appelle, et à quelle vitesse

> L'API de billetterie d'une salle de spectacle est publique : n'importe qui peut
> consulter les places disponibles. Un script y envoie 10 000 requêtes par
> minute. L'API, elle, tient — mais la base de données est à genoux, et les
> vrais spectateurs reçoivent des pages qui ne chargent plus. Authentifier
> l'appelant n'est pas le tout : il faut aussi **limiter son débit** et
> **valider ses données**.

**Durée de lecture :** 60 min · **Prérequis :** le chapitre [Sécurité des
API](07-securite-api.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Distinguer** ce qu'un jeton autorise (scopes et rôles) de ce qu'il prouve
  (identité).
- **Appliquer** un rate limiting adapté à chaque endpoint d'une API.
- **Écrire** une validation de schéma qui refuse les valeurs hors cadre.
- **Choisir** un niveau de quota par consommateur d'API.

---

## I. Scopes et rôles

Authentifier, c'est répondre à la question « **qui** appelle ? ». Autoriser,
c'est répondre à « **qu'a-t-il le droit de faire** ? ». Le chapitre précédent
montrait que confondre les deux produit du BOLA (Broken Object Level Authorization) ; ici, on construit la réponse.

Deux outils se complètent :

| Outil | Ce qu'il décrit | Exemple |
| --- | --- | --- |
| **Le rôle** | le profil de l'appelant dans le système | `spectateur`, `guichet`, `administrateur` |
| **Le scope** | le périmètre exact accordé à **cet** appel | `places:lire`, `places:reserver`, `remboursements:creer` |

Le rôle est large et stable ; le scope est fin et révocable. Un jeton de
billetterie délivré à une application partenaire peut porter le rôle
`guichet` avec le seul scope `places:lire` : l'application voit les places,
sans jamais pouvoir en réserver ni en rembourser.

Deux verbes HTTP suffisent pour l'exemple : GET (consulter une ressource) et
POST (en créer une). La règle d'or se vérifie endpoint par endpoint :

| Endpoint | Scope exigé | Refus attendu sans ce scope |
| --- | --- | --- |
| `GET /places` | `places:lire` | `401` si pas de jeton, `403` si jeton sans ce scope |
| `POST /reservations` | `places:reserver` | `403` |
| `POST /remboursements` | `remboursements:creer` | `403` |

Notez la différence entre les deux refus : `401 Unauthorized` dit « je ne sais
pas qui vous êtes » (ou votre jeton ne vaut plus rien) ; `403 Forbidden` dit
« je sais qui vous êtes, et vous n'avez pas ce droit ». Un code `403` renvoyé
à la place d'un `401` — ou l'inverse — est le premier indice d'une autorisation
mal branchée.

> [!TIP]
> Écrivez la matrice « endpoint × scope » **avant** d'écrire le code des
> contrôleurs. Une autorisation décidée au cas par cas, endpoint après
> endpoint, finit toujours par en oublier un.

> 🧪 **Atelier rapide (5 min)**
>
> Voici deux réponses de la même API, pour le même endpoint administratif.
> Identifiez, pour chacune, **quel contrôle** a produit le refus :

```text
Requête A — sans en-tête Authorization
HTTP/1.1 401 Unauthorized
{"detail": "token manquant"}

Requête B — avec un jeton valide de scope "places:lire"
HTTP/1.1 403 Forbidden
{"detail": "accès réservé aux remboursements"}
```

La requête A échoue à l'**authentification** (personne n'est identifié) ; la
requête B échoue à l'**autorisation** (l'appelant est identifié, mais son scope
ne couvre pas l'action). Vérifiez que vous pouvez expliquer cette différence à
quelqu'un sans regarder le tableau ci-dessus.

---

## II. Rate limiting

Le rate limiting (limitation de débit) fixe **combien de requêtes** un appelant
peut faire **dans un intervalle**. Il protège trois choses à la fois : la
disponibilité du service, la base de données derrière, et le portefeuille (chaque
appel coûte des ressources).

Le cas le plus simple est un compteur par appelant :

```python
# Compteur minimal de tentatives — clair, mais limité (voir plus bas).
TENTATIVES: dict[str, int] = {}
MAX_TENTATIVES = 5

def verifier_quota(cle: str) -> bool:
    if TENTATIVES.get(cle, 0) >= MAX_TENTATIVES:
        return False          # la requête sera refusée en 429
    TENTATIVES[cle] = TENTATIVES.get(cle, 0) + 1
    return True
```

Trois décisions se prennent dès qu'on pose un rate limiting :

| Décision | Options | Ce qu'elle change |
| --- | --- | --- |
| **Qui compte ?** | adresse IP, compte, clé d'application | une IP partagée (entreprise, campus) ne doit pas être punie pour tous ses utilisateurs |
| **Quel rythme ?** | par seconde, par minute, par jour | un login se limite serré ; une lecture de catalogue se limite large |
| **Que renvoyer ?** | `429 Too Many Requests` + en-tête `Retry-After` | l'appelant sait quand réessayer au lieu de marteler |

> [!WARNING]
> Un compteur en mémoire, comme ci-dessus, repart à zéro à chaque redémarrage
> du service et n'est pas partagé entre plusieurs instances. C'est parfait pour
> un premier garde-fou, insuffisant pour une API exposée : le comptage se
> déplace alors vers un stockage partagé (Redis, base de données) ou vers la
> passerelle d'API.

Le débit n'est pas la seule ressource à limiter : la **taille** des requêtes
aussi. Un corps de requête de 50 Mo, un champ de recherche de 10 000
caractères, une réponse paginée sans limite — chacun est un levier d'épuisement.
La section suivante traite ces cas.

---

## III. Validation de schéma

Un appelant envoie ce qu'il veut : un champ de trop, une chaîne à la place d'un
nombre, une valeur négative pour une quantité. La validation de schéma décrit
**à l'avance** la forme acceptable de chaque requête, et refuse le reste.

En Python, Pydantic est le standard de fait avec FastAPI :

```python
from pydantic import BaseModel, Field

class Reservation(BaseModel):
    spectacle_id: int
    places: int = Field(ge=1, le=6)                    # entre 1 et 6 places
    email: str = Field(max_length=254)                 # longueur bornée
    code_postal: str = Field(pattern=r"^\d{5}$")       # format exact
```

Chaque contrainte répond à une question simple :

| Contrainte | Question qu'elle tranche | Ce qu'elle écarte |
| --- | --- | --- |
| **Type** (`int`, `str`) | la valeur est-elle du bon type ? | `"six"` à la place de `6` |
| **Bornes** (`ge`, `le`) | la valeur est-elle plausible ? | `-3` places, `999` places |
| **Longueur** (`max_length`) | la saisie est-elle dimensionnée ? | un champ de commentaire de 10 Mo |
| **Format** (`pattern`) | la valeur suit-elle le schéma attendu ? | un code postal qui n'en est pas un |

Le réflexe est **fail-closed** : ce qui n'est pas explicitement accepté est
refusé, jamais « réparé » en silence. Une API qui transforme `places=-3` en
`places=1` cache un bug du côté de l'appelant — et lui apprend à ne jamais le
corriger.

> [!DANGER]
> Valider le format ne suffit pas : il faut aussi vérifier **l'autorisation**
> sur la donnée touchée. Une réservation parfaitement validée au schéma peut
> porter un `spectacle_id` qui n'appartient pas à l'appelant — c'est du BOLA,
> et la validation de schéma ne le voit pas.

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **Quotas par consommateur** — au-delà du débit instantané, un budget sur la
  journée ou le mois : 100 appels par heure pour l'application partenaire A,
  10 000 pour le partenaire B. Les API publiques (météo, transports, cartographie)
  fonctionnent ainsi, avec un en-tête qui annonce le budget restant.
- **Passerelle d'API (API gateway)** — un composant (Kong, Apigee, ou les
  passerelles cloud) qui applique authentification, rate limiting et validation
  **avant** le code applicatif. Centralisé et homogène — mais il ne dispense pas
  l'application de vérifier l'autorisation sur chaque objet.
- **JWT (JSON Web Token)** — le format de jeton le plus répandu dans les API :
  un en-tête, une charge utile (les scopes, l'identité), une signature. Ses
  scopes sont lus **sans appel à la base** — d'où l'importance de les écrire
  serrés au moment de la délivrance, puisqu'un jeton émis vit jusqu'à son
  expiration.

---

## Points clés

- Authentifier répond à « qui ? », autoriser à « quoi ? » : **rôles** pour le
  profil, **scopes** pour le périmètre exact de chaque appel.
- `401` = je ne sais pas qui vous êtes ; `403` = je sais, et vous n'avez pas ce
  droit. Le bon code renvoyé est déjà une information de sécurité.
- Le rate limiting protège la disponibilité, la base et le budget : on décide
  **qui compte**, **quel rythme**, **que renvoyer** (`429` + `Retry-After`).
- La validation de schéma tranche à l'avance types, bornes, longueurs et
  formats — et refuse par défaut. Elle ne remplace jamais le contrôle
  d'autorisation sur l'objet touché.
