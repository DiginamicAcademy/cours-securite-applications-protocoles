[← Chapitre précédent](03-xss-et-sorties.md) · [Sommaire](Readme.md) · [Chapitre suivant →](05-dependances-et-configuration.md)

# Erreurs et logging — ne rien exposer, tout tracer

> En pleine ouverture des ventes, la billetterie d'un festival local affiche une
> page d'erreur. Pas un message poli : la trace complète de l'échec, avec le
> chemin des fichiers, la version du moteur de base et la requête qui a échoué.
> Une stack trace en production, c'est le plan du système d'incendie affiché sur
> la porte du coffre-fort.

**Durée de lecture :** 45 min hors approfondissements facultatifs · **Prérequis :** le chapitre
[Principes du secure coding](01-principes-secure-coding.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Distinguer** ce qui se renvoie à la personne qui utilise le service et ce qui
  reste dans les journaux, en fonction de l'environnement.
- **Rédiger** un message d'erreur qui aide l'utilisateur sans renseigner
  l'attaquant.
- **Choisir** ce qui mérite d'être journalisé, à quel niveau de détail, et
  pendant combien de temps.
- **Repérer** les secrets qui fuient dans les journaux, et les en sortir.

---

## I. Ne pas exposer

Une erreur est une information : le programme qui échoue sait des choses —
les chemins, les versions, la requête. Les renvoyer à qui a déclenché
l'erreur, c'est lui donner le plan du système.

La règle se résume ainsi : **le détail aide le développeur, le général rassure
l'utilisateur**.

| Environnement | Ce qu'on renvoie | Pourquoi |
| --- | --- | --- |
| **Développement** | le détail complet, la trace, la ligne fautive | c'est l'outil de travail |
| **Production** | un message générique, un identifiant de suivi | le détail sert d'abord à qui cherche à en abuser |

```python
# en production : le message est stable, le détail part dans les journaux
except Exception:
    journal.exception("échec de la génération du rapport")
    return {"erreur": "la demande n'a pas pu être traitée",
            "reference": identifiant_de_suivi}
```

L'identifiant de suivi est le joint entre les deux mondes : la personne signale
un numéro, l'équipe retrouve la trace complète dans les journaux.

> ⚠️ **Attention** — Un message d'erreur trop précis reste une fuite, même sans
> trace technique. « Le compte n'existe pas » et « mot de passe incorrect » ne
> disent pas la même chose à quelqu'un qui énumère des comptes : le premier
> confirme ce qui existe, le second ne dit rien.

C'est le fail-closed du chapitre sur les principes, appliqué à l'affichage.

---

## II. Logger correctement

Journaliser, c'est se préparer au jour où il faudra reconstituer ce qui s'est
passé. Un journal utile répond à quatre questions : **qui**, **quand**, **quoi**,
**avec quel résultat**. Tout le reste est du bruit qui finit par masquer
l'essentiel.

| Ce qu'on journalise | Exemple | Niveau |
| --- | --- | --- |
| **Les accès** | la route appelée, l'heure, le résultat | information |
| **Les refus** | une authentification qui échoue, un droit manquant | avertissement |
| **Les erreurs** | ce qui a échoué, avec la trace côté serveur | erreur |
| **Les actions sensibles** | un changement de rôle, une suppression, un export | information, conservé plus longtemps |

Trois décisions se prennent en même temps que le contenu du journal :

- **Où** — un emplacement que le code applicatif ne sert pas lui-même, pour
  qu'une lecture ne devienne pas une écriture.
- **Combien de temps** — une durée de conservation décidée à l'avance, pas
  « jusqu'à ce que le disque soit plein ».
- **Qui peut lire** — les journaux contiennent ce qui s'est passé dans le
  système : leur accès se limite à ceux qui en ont besoin.

---

## III. Pas de secrets dans les logs

Le piège est classique : pour comprendre un problème de connexion, on journalise
la requête complète — et la requête contient le mot de passe. Le journal, conçu
pour être lu par plus de monde que la base, se retrouve avec une copie des
identifiants.

| Ce qui ne va jamais dans un journal | Ce qu'on met à la place |
| --- | --- |
| **mot de passe, jeton, clé** | le fait que l'authentification a échoué |
| **donnée personnelle complète** | un identifiant technique, une empreinte |
| **contenu d'un fichier sensible** | sa taille, son type, son empreinte |

```python
# à éviter : la saisie entière part dans le journal
journal.info("connexion de %s avec %s", utilisateur, mot_de_passe)

# à faire : l'événement, sans ce qui ne doit pas sortir
journal.info("tentative de connexion", extra={"utilisateur": utilisateur,
                                              "resultat": "refuse"})
```

> 💡 **À retenir** — Un journal n'est pas une copie de la base. Il décrit ce qui
> s'est passé, pas ce que contenaient les données. Quand un doute subsiste, on
> journalise le fait et l'identifiant technique, jamais la valeur.

Ce principe vaut aussi pour les traces d'erreur : une exception transporte
parfois le contenu de la requête qui l'a provoquée. Avant de la journaliser
entièrement, on vérifie ce qu'elle charrie.

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **La journalisation structurée** — au lieu d'une phrase libre, chaque
  événement est un ensemble de champs nommés, au format JSON (JavaScript Object
  Notation). Les journaux deviennent interrogeables, et une alerte se définit
  sur un champ plutôt que sur une phrase à deviner.
- **Le SIEM** (Security Information and Event Management) — une plateforme qui
  agrège les journaux de plusieurs systèmes et y cherche des motifs. Elle ne
  vaut que ce que valent les journaux qu'on lui envoie : un événement non tracé
  ne sera jamais corrélé.
- **Le droit à l'oubli, appliqué aux journaux** — anonymiser, tronquer ou
  supprimer les données personnelles au fil du temps est un travail de
  conception, pas une opération de nettoyage lancée quand quelqu'un le demande.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> Le RGPD a son chapitre dans ce cours : [RGPD appliqué](10-rgpd-applique.md). Ici,
> seule la décision compte — la durée de conservation se fixe à l'avance.
>
> La durée de conservation n'est pas un détail d'exploitation : elle engage la
> conformité. Le RGPD (Règlement général sur la protection des données) impose de
> ne garder les données que le temps nécessaire — et un journal qui accumule des
> données personnelles pendant des années est un traitement comme un autre.

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien
> d'obligatoire n'en dépend
>
> La partie 1 de l'exercice [Durcir un endpoint de réservation](tp/04-durcir-un-endpoint.md)
> est cette manipulation même, conduite sur un service complet.
>
> 🧪 **Atelier rapide (5 min)**
>
> Dans le lab du cours, lancez `lab/vulnerable/app.py`, puis provoquez une
> erreur de base de données en appelant la route de recherche avec une valeur
> qui casse la requête. Regardez ce que reçoit le client, puis ce qui apparaît
> dans la sortie du serveur. Notez ce qui, dans la réponse, renseigne la
> personne — et ce qui renseigne surtout quelqu'un qui chercherait à cartographier
> le service.

---

## Points clés

- Une erreur renvoie **le général** à la personne, et garde **le détail** pour
  l'équipe — avec un identifiant de suivi pour relier les deux.
- Un journal utile répond à **qui, quand, quoi, avec quel résultat** — et se
  donne une durée de conservation et un cercle de lecteurs.
- **Aucun secret** dans les journaux : ni mot de passe, ni jeton, ni donnée
  personnelle en clair.
- Journaliser, c'est se préparer à reconstituer un incident — c'est donc une
  décision de conception, pas une variable de débogage qu'on oublie.

---

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis cochez. Les réponses sont juste après le séparateur : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** En pleine ouverture des ventes, la billetterie plante en production. Que doit recevoir la personne qui utilisait le service ?

- A. La trace complète de l'échec, pour qu'elle puisse la transmettre au support
- B. La version du moteur de base de données et la requête fautive
- C. Un message générique et un identifiant de suivi ; le détail part dans les journaux
- D. Rien : une page blanche, pour ne rien divulguer du tout

- [ ] ✓ je savais

**2.** À la connexion, l'application renvoie « Le compte n'existe pas » quand l'identifiant est inconnu. Pourquoi est-ce une fuite ?

- A. Parce que le message est trop poli et n'inquiète personne
- B. Parce qu'il confirme à quelqu'un qui énumère des comptes ce qui existe
- C. Parce qu'il révèle la version du moteur de base de données
- D. Parce qu'il devrait mentionner le nombre de tentatives restantes

- [ ] ✓ je savais

**3.** Un journal utile répond à quatre questions. Lesquelles ?

- A. Qui, quand, quoi, avec quel résultat
- B. Pourquoi, combien, comment, où
- C. Qui, pourquoi, quel budget, quel délai
- D. Quelle version, quel correctif, quel test, quel déploiement

- [ ] ✓ je savais

**4.** Pour comprendre un problème de connexion, faut-il journaliser la requête de connexion complète ?

- A. Oui : sans la requête entière, on ne peut rien reconstituer
- B. Oui, mais seulement si le journal est chiffré
- C. Non : on journalise le fait que l'authentification a échoué, jamais le mot de passe ni le jeton
- D. Non : une tentative de connexion ne mérite jamais d'être journalisée

- [ ] ✓ je savais

**5.** *Question ouverte (2-3 lignes).* « Un journal n'est pas une copie de la base. » Expliquez la formule, et pourquoi une copie des identifiants dans un journal est pire que dans la base elle-même.

- [ ] ✓ je savais

---

### Réponses

**1. C.** Le détail aide le développeur, le général rassure l'utilisateur : en production, un message générique avec un identifiant de suivi ; la trace complète reste côté serveur.
**Pourquoi :** l'identifiant de suivi est le joint entre les deux mondes — la personne signale un numéro, l'équipe retrouve la trace dans les journaux.

**2. B.** « Le compte n'existe pas » et « mot de passe incorrect » ne disent pas la même chose à quelqu'un qui énumère des comptes : le premier confirme ce qui existe, le second ne dit rien.
**Pourquoi :** un message d'erreur trop précis reste une fuite même sans trace technique — c'est le fail-closed appliqué à l'affichage.

**3. A.** Qui, quand, quoi, avec quel résultat. Tout le reste est du bruit qui finit par masquer l'essentiel.
**Pourquoi :** le journal se conçoit pour reconstituer un incident ; s'y ajoutent trois décisions prises en même temps : où il est stocké, combien de temps on le garde, qui peut le lire.

**4. C.** Le journal décrit ce qui s'est passé, pas ce que contenaient les données : on note la tentative et son résultat, avec l'identifiant technique — jamais la valeur du secret.
**Pourquoi :** une exception ou une requête transporte parfois le contenu qui l'a provoquée ; avant de journaliser entièrement, on vérifie ce qu'elle charrie.

**5.** Attendu : le journal trace les événements (tentative, refus, accès, résultat), il ne duplique pas le contenu des données — à la place d'un mot de passe ou d'une donnée personnelle complète, un fait et un identifiant technique.
**Pourquoi :** le journal est conçu pour être lu par plus de monde que la base ; y recopier les identifiants, c'est en multiplier la copie et les lecteurs.

---

[← Chapitre précédent](03-xss-et-sorties.md) · [Sommaire](Readme.md) · [Chapitre suivant →](05-dependances-et-configuration.md)
