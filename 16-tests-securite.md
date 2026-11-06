[← Chapitre précédent](15-devsecops.md) · [Sommaire](Readme.md) · [Chapitre suivant →](17-reponse-incident.md)

# Tests de sécurité — empêcher la faille corrigée de revenir

> En mars, l'équipe corrige une injection dans le module de recherche de sa
> plateforme de billetterie : la saisie est enfin paramétrée, le test manuel
> passe, tout le monde est content. En septembre, une réécriture du même module
> réintroduit la concaténation d'origine. Personne ne s'en aperçoit : la faille
> était corrigée, elle n'était pas **gardée** corrigée. Un smoke test de sécurité
> — le test rapide qui rejoue l'ancien trou — dit une chose simple : « l'ancien
> trou est bien bouché ». Sans lui, chaque réécriture rejoue la mise en production
> de l'an dernier.

**Durée de lecture :** 55 min · **Prérequis :** les vulnérabilités web des journées
précédentes, les bases des tests automatisés

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Écrire** un test de sécurité qui rejoue un payload connu contre une API.
- **Transformer** une faille corrigée en test de non-régression permanent.
- **Mettre en œuvre** un fuzzing léger pour faire remonter des comportements
  imprévus.
- **Décider** quels tests méritent d'entrer dans la suite permanente, et lesquels
  restent des explorations ponctuelles.

---

## I. Les smoke tests de sécurité

### Le principe : rejouer ce qui marchait avant

Un payload, c'est une donnée d'entrée conçue pour déclencher un comportement
indésirable — `' OR '1'='1` pour une injection SQL (Structured Query Language, le
langage de requête des bases relationnelles), `<script>alert(1)</script>` pour un
XSS (Cross-Site Scripting, l'injection de script dans une page). Le jour où on
corrige la faille, ce payload cesse de fonctionner. Le smoke test de sécurité
consiste à **le rejouer à chaque exécution** et à vérifier qu'il échoue toujours.

### Un premier test, contre le lab

Le lab du cours expose deux versions de la même API : `vulnerable` (port 8080),
où la recherche de produits est injectable, et `secure` (port 8081), où la même
requête est paramétrée. Le test ci-dessous vérifie que le payload historique est
bien rejeté par la version corrigée :

```python
import requests

BASE = "http://localhost:8081"

def test_recherche_rejette_injection():
    # Le payload qui listait tous les produits sur l'API vulnérable
    reponse = requests.get(
        BASE + "/products/search",
        params={"q": "' OR '1'='1"},
    )
    assert reponse.status_code == 400
```

Trois détails font la qualité de ce test :

- il nomme **le payload exact** qui posait problème, pas une vague catégorie ;
- il attend un **code de réponse précis** (ici 400, la requête est refusée), et
  pas seulement « ça ne plante pas » ;
- il est **indépendant** : il ne dépend d'aucune donnée laissée par un autre test.

> 🧪 **Atelier rapide (10 min)**
>
> Écrivez le test pytest ci-dessus dans un fichier `test_securite.py`, puis
> lancez-le avec `pytest test_securite.py -v` contre le service `secure` du lab
> (démarré avec `docker compose up --build -d` dans `lab/`). Modifiez ensuite
> l'adresse de base pour viser `vulnerable` : le test doit **échouer**. Vous venez
> d'écrire un test qui distingue une API corrigée d'une API vulnérable.

---

## II. Le fuzzing léger

### Envoyer l'inattendu

Les tests classiques vérifient ce qu'on a prévu. Le fuzzing (l'envoi d'entrées
aléatoires ou aberrantes pour observer ce qui casse) explore le reste : chaînes
vides, caractères de contrôle, entrées très longues, encodages bizarres. L'objectif
n'est pas de « casser » l'application pour le plaisir, mais de découvrir les
endroits où une valeur inattendue provoque une erreur non gérée — qui révèle
souvent un traitement dangereux juste derrière.

```python
import random
import string

import requests

def test_fuzz_recherche_ne_plante_pas():
    for _ in range(200):
        taille = random.randint(1, 64)
        q = "".join(random.choice(string.printable) for _ in range(taille))
        reponse = requests.get(
            "http://localhost:8081/products/search",
            params={"q": q},
        )
        # Une erreur serveur trahit un traitement non maîtrisé de l'entrée
        assert reponse.status_code != 500
```

Ce test ne prouve pas l'absence de faille : il prouve l'absence de **plantage**,
ce qui est déjà beaucoup, et il le refait à chaque exécution.

> 🚨 **Piège à éviter** — le fuzzing s'exerce **uniquement** sur votre lab local ou
> sur un environnement de test dont vous êtes responsable. Lancer un fuzzing sur
> un service de production, même « pour vérifier », est une charge réelle pour ce
> service et une atteinte à ce qui ne vous appartient pas.

### Borner l'exploration

Un fuzzing sans bornes est lent, bruyant, et finit abandonné. Trois limites le
rendent utile au quotidien : un **nombre d'itérations** fixé, une **durée** maximale,
et une **graine aléatoire** enregistrée pour rejouer exactement la même séquence
le jour où un test échoue. Un test qu'on ne peut pas rejouer ne sert à rien.

---

## III. Les tests de non-régression

### Les payloads deviennent des tests

La règle tient en une phrase : **chaque faille corrigée devient un test**. C'est
le même réflexe que pour un bug fonctionnel — sauf que l'enjeu est plus grave,
parce qu'une régression de sécurité ne se voit pas dans les résultats de
l'application. Elle se voit dans les journaux d'un attaquant.

| Faille corrigée | Test à ajouter | Ce qu'il protège |
| --- | --- | --- |
| Injection dans la recherche | rejouer le payload d'injection, attendre un refus | la requête paramétrée |
| Script injecté dans un commentaire | rejouer le balisage de script, attendre un affichage échappé | l'échappement en sortie |
| Endpoint d'administration sans contrôle | appeler sans jeton, attendre un refus | le contrôle de rôle |
| Réponse qui exposait un champ sensible | vérifier l'absence du champ dans la réponse | la minimisation des données |

### Où les faire tourner

Ces tests prennent place dans le pipeline décrit au chapitre précédent :
[DevSecOps et traçabilité des dépendances](15-devsecops.md).


---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour terminer
la journée.*

- **Le DAST** (Dynamic Application Security Testing, les tests d'intrusion
  automatisés) — des outils comme ZAP (Zed Attack Proxy, l'outil de test
  d'intrusion) publié par l'OWASP (Open Web Application Security Project, le
  projet de référence de la sécurité applicative) explorent
  l'application en cours d'exécution et signalent les comportements suspects. Plus
  lent qu'un smoke test, utile en vérification périodique.
- **Les suites de tests de sécurité partagées** — publier ses payloads de
  non-régression comme une bibliothèque permet à plusieurs équipes de les rejouer.
  Ce qui protège une application protège souvent les autres.
- **Le fuzzing structuré** — fournir au fuzzing le format attendu (un schéma de
  requête, un modèle de données) multiplie les cas pertinents et réduit le bruit.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **Ce qui fait la force du smoke test**
>
> Le test est minuscule, et c'est sa force : il tourne en quelques secondes, il ne
> demande aucune infrastructure, et il dit vrai.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> 💡 **Astuce** — un test de sécurité qui échoue est une bonne nouvelle : il vient
> de vous apprendre que la protection a disparu, avant vos utilisateurs. Traitez
> un test rouge comme un incident naissant, pas comme du bruit de build.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> **SAST et smoke test : deux regards complémentaires**
>
> La différence avec
> les contrôles de ce chapitre : le SAST (Static Application Security Testing,
> l'analyse statique du code) **devine** les risques à partir du code, tandis qu'un
> smoke test **constate** le comportement réel de l'API. Les deux se complètent —
> l'un regarde le code, l'autre regarde ce qui tourne.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> ⚠️ **Point d'attention** — un test de sécurité qui passe parce qu'il interroge
> le mauvais service ne protège rien. Vérifiez toujours que votre test vise la
> bonne adresse : un test vert contre `vulnerable` est un test qui vous ment.

---

## Points clés

- Un smoke test de sécurité **rejoue le payload qui marchait avant** et vérifie
  qu'il échoue toujours : la faille corrigée reste corrigée.
- Un bon test nomme le payload exact, attend un **code de réponse précis**, et
  reste indépendant des autres tests.
- Le fuzzing léger cherche les **plantages** provoqués par l'inattendu — borné en
  itérations, en durée, et rejouable grâce à une graine enregistrée.
- **Chaque faille corrigée devient un test** ; ces tests rejoignent le pipeline du
  chapitre précédent, à côté des contrôles statiques.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis cochez. Les réponses sont juste après le séparateur : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** Qu'est-ce qu'un smoke test de sécurité ?

- A. Un test rapide qui vérifie que la page d'accueil s'affiche bien
- B. Un test qui rejoue le payload qui marchait avant la correction, et vérifie qu'il échoue toujours
- C. Une analyse statique du code qui devine les risques avant l'exécution
- D. Un test de charge qui mesure le temps de réponse de l'API

- [ ] ✓ je savais

**2.** Quels trois détails font la qualité du test de sécurité du chapitre ?

- A. Il est court, il passe vite, il est bien documenté
- B. Il nomme le payload exact, attend un code de réponse précis, et reste indépendant des autres tests
- C. Il utilise un payload générique, accepte tout code 4xx, et s'appuie sur les données du test précédent
- D. Il teste plusieurs failles à la fois, boucle sur tous les endpoints, et journalise ses résultats

- [ ] ✓ je savais

**3.** Le test de fuzzing du chapitre s'arrête sur `assert reponse.status_code != 500`. Que prouve-t-il quand il passe ?

- A. L'absence de faille dans l'API
- B. L'absence de plantage : une erreur serveur trahit un traitement non maîtrisé de l'entrée — c'est déjà beaucoup, et il le refait à chaque exécution
- C. Que toutes les entrées ont été testées
- D. Que l'API rejette bien les entrées invalides par un code 400

- [ ] ✓ je savais

**4.** Un collègue propose de lancer le fuzzing « pour vérifier » sur le service de production du partenaire. Que dit le chapitre ?

- A. C'est acceptable si le fuzzing est borné en durée
- B. C'est acceptable la nuit, quand le service est peu chargé
- C. C'est exclu : le fuzzing s'exerce uniquement sur son lab local ou un environnement de test dont on est responsable — sur un service de production, c'est une charge réelle et une atteinte à ce qui ne vous appartient pas
- D. C'est exclu uniquement si le service est public ; un service de partenaire privé est un terrain de test

- [ ] ✓ je savais

**5.** *Question ouverte (2-3 lignes).* « Chaque faille corrigée devient un test. » Pourquoi ce réflexe est-il plus important en sécurité qu'en fonctionnel, et donnez un exemple de test de non-régression pris dans le chapitre.

- [ ] ✓ je savais

---

### Réponses

**1. B.** Le payload (`' OR '1'='1` pour une injection SQL, `<script>alert(1)</script>` pour un XSS) cesse de fonctionner le jour où la faille est corrigée ; le smoke test le rejoue à chaque exécution pour vérifier qu'il échoue toujours.
**Pourquoi :** dans l'accroche, une réécriture de septembre réintroduit l'injection corrigée en mars : la faille était corrigée, elle n'était pas gardée corrigée.

**2. B.** Le payload exact — pas une vague catégorie ; un code de réponse précis (ici 400, la requête est refusée) — pas seulement « ça ne plante pas » ; et l'indépendance — aucune donnée laissée par un autre test.
**Pourquoi :** pointé sur le service `vulnerable` du lab, le test doit échouer — c'est ce qui le distingue d'un simple test de bon fonctionnement.

**3. B.** Ce test ne prouve pas l'absence de faille : il prouve l'absence de plantage.
**Pourquoi :** le fuzzing explore ce qui n'a pas été prévu (chaînes vides, entrées très longues, encodages bizarres) pour découvrir les endroits où une valeur inattendue provoque une erreur non gérée, souvent le signe d'un traitement dangereux juste derrière.

**4. C.** Lancer un fuzzing sur un service de production, même « pour vérifier », est une charge réelle pour ce service et une atteinte à ce qui ne vous appartient pas.
**Pourquoi :** le fuzzing léger se pratique sur son lab ou un environnement de test dont on est responsable ; et là, on le borne — nombre d'itérations, durée maximale, graine enregistrée pour rejouer la séquence : un test qu'on ne peut pas rejouer ne sert à rien.

**5.** Attendu : une régression de sécurité ne se voit pas dans les résultats de l'application — elle se voit dans les journaux d'un attaquant ; l'enjeu est donc plus grave que pour un bug fonctionnel. Exemple (un parmi) : injection corrigée dans la recherche → rejouer le payload, attendre un refus ; script injecté → attendre un affichage échappé ; endpoint d'administration → appeler sans jeton, attendre un refus ; champ sensible retiré → vérifier son absence dans la réponse.
**Pourquoi :** ces tests rejoignent le pipeline d'intégration continue et gardent la correction effective à chaque livraison.

---

[← Chapitre précédent](15-devsecops.md) · [Sommaire](Readme.md) · [Chapitre suivant →](17-reponse-incident.md)
