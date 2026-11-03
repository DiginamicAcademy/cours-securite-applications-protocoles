# Corrigé — Construire sa feuille de route de sécurité

> Corrigé de [l'exercice « Construire sa feuille de route de
> sécurité »](../18-defi-maturite.md). Ce défi porte sur **votre** projet : le
> corrigé ne peut donc pas donner « la » réponse. Il donne la **forme d'une bonne
> réponse**, puis un exemple complet sur un projet fictif — le dépôt
> `analyse-ventes` d'une équipe data (scripts Python, notebooks partagés, un
> fichier `requirements.txt`, une API de restitution, des sauvegardes
> hebdomadaires).

---

## Partie 1 — S'auto-évaluer

**Ce qui fait une bonne justification :** un fait observable, que quelqu'un d'autre
peut vérifier en regardant. « On fait attention aux dépendances » n'est pas un
fait. « `requirements.txt` ne fige aucune version, et personne ne sait dire quelles
composants sont embarqués » en est un.

**Exemple rempli :**

| Domaine | Note | Justification (fait observable) |
| --- | --- | --- |
| Code | 2 | les scripts sont relus entre pairs, mais aucun contrôle automatique ne tourne à la livraison |
| Dépendances | 1 | `requirements.txt` ne fige aucune version, et aucun inventaire des composants n'existe |
| Accès | 3 | les comptes sont nominatifs, mais un compte de service partagé subsiste pour l'extraction |
| Réseau | 2 | l'API de restitution est exposée, et la base est joignable depuis tout le réseau interne |
| Réponse à incident | 1 | aucun document écrit, personne n'est nommée pour décider |

**Erreurs fréquentes :** mettre la même note partout (l'évaluation n'a pas été
faite), ou justifier par une intention (« on prévoit de… ») au lieu d'un fait.

---

## Partie 2 — Identifier les écarts les plus coûteux

**Ce qui fait un bon écart :** un chemin d'attaque décrit en une phrase, et un
geste qui le **coupe** — pas une liste de bonnes intentions.

**Exemple, sur les trois écarts retenus :**

| Écart | Le chemin le plus court | Le geste qui le coupe |
| --- | --- | --- |
| Dépendances (note 1) | une faille publiée sur un composant de `requirements.txt` est exploitable sans que personne ne le sache | figer les versions, produire un inventaire des composants (SBOM, Software Bill of Materials) à chaque livraison, et recevoir l'alerte quand une version est affectée |
| Réseau (note 2) | un poste interne compromis donne accès direct à la base de données | n'autoriser que l'API de restitution à joindre la base, et refuser le reste |
| Réponse à incident (note 1) | le jour où ça casse, personne ne sait qui décide quoi, et les gestes de première urgence détruisent les traces | écrire le mini-plan de réponse, nommer les rôles, le tester par une simulation |

**Erreurs fréquentes :** retenir les écarts « les plus simples à corriger » plutôt
que les plus coûteux, ou décrire un remède général (« sensibiliser l'équipe ») qui
ne coupe aucun chemin.

---

## Partie 3 — Construire la feuille de route

**Exemple sur 3 mois :**

| Horizon | Action | Responsable | Échéance |
| --- | --- | --- | --- |
| **Immédiat** | fermer l'accès direct à la base depuis le réseau interne | l'administratrice de la base | la première semaine |
| **Immédiat** | révoquer le compte de service partagé, créer un compte nominatif par usage | le responsable de l'équipe data | la première semaine |
| **Court terme** | figer les versions de `requirements.txt` et produire l'inventaire des composants à chaque livraison | la personne qui maintient la chaîne de livraison | le premier mois |
| **Court terme** | ajouter les contrôles automatisés du chapitre sur la chaîne de livraison | la même personne | le deuxième mois |
| **Structurel** | écrire le mini-plan de réponse à incident et nommer les rôles | le responsable de l'équipe data | le deuxième mois |
| **Structurel** | faire une simulation de crise, puis mettre le plan à jour | toute l'équipe | le troisième mois |

**Ce qui fait une bonne feuille de route :** au moins une action visible dans les
premières semaines (sinon l'élan retombe), un responsable et une échéance pour
chaque ligne, et un mélange des trois horizons.

---

## Partie 4 — Définir les preuves de progression

**Ce qui fait une bonne preuve :** quelque chose qu'on **montre**, pas quelque
chose qu'on décrit.

**Exemple :**

| Horizon | Preuve observable |
| --- | --- |
| **Immédiat** | une tentative de connexion à la base depuis un poste quelconque échoue, et le refus apparaît dans les journaux |
| **Court terme** | l'inventaire des composants de la dernière livraison existe, daté, et une alerte est bien remontée sur une dépendance volontairement laissée ancienne pour le test |
| **Structurel** | le compte rendu de la simulation de crise existe, avec les changements décidés et leur mise en œuvre |

**Erreurs fréquentes :** une preuve qui consiste à dire « c'est fait », ou une
preuve qui demande une enquête pour être constatée. Si la preuve ne se voit pas en
quelques minutes, elle ne servira pas à la revue de trois mois.

---

## Points à retenir

- Une note ne vaut que par **le fait observable** qui la justifie.
- Un écart se décrit comme **un chemin d'attaque et le geste qui le coupe**.
- La feuille de route tient en trois horizons, avec **un responsable et une
  échéance** pour chaque action.
- La progression se prouve par **ce qu'on montre**, pas par ce qu'on affirme.
