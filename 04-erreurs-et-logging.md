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

### Exercice 1 — Durcir un endpoint de réservation (30 min)

#### Contexte

Un grand groupe mutualise ses salles de réunion via un petit service interne de
réservation. L'équipe qui l'a livré est partie ; il tourne, personne n'y touche.
La direction des systèmes d'information vous demande une passe de durcissement
avant de l'ouvrir à un nouveau site.

Voici les deux routes principales :

```python
import logging
import traceback

journal = logging.getLogger("reservations")


@app.get("/reservations")
def lister_reservations(email: str = ""):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE email = %s", (email,))
        rows = cursor.fetchall()
        conn.close()
        return {"reservations": rows}
    except Exception as exc:
        return {"erreur": str(exc), "trace": traceback.format_exc()}


@app.post("/reservations")
def creer_reservation(email: str = Form(...), salle: str = Form(...),
                      mot_de_passe: str = Form(...)):
    journal.info("creation pour %s (mdp %s)", email, mot_de_passe)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reservations (email, salle) VALUES (%s, %s)",
        (email, salle),
    )
    conn.commit()
    conn.close()
    return {"message": "réservation enregistrée"}
```

Le contrat attendu par la direction est le suivant : une personne ne voit que
ses propres réservations ; une erreur interne renvoie le code **500** avec un
message générique et un numéro de suivi ; un accès refusé renvoie le code
**403** ; aucun mot de passe ne se retrouve dans les journaux.

---

#### Consignes

##### Partie 1 — Repérer ce qui sort du service

Listez tout ce qui quitte le service : ce qui est renvoyé au client, ce qui est
écrit dans les journaux. Pour chacun, dites s'il renseigne la personne qui
utilise le service, ou surtout quelqu'un qui chercherait à comprendre le
système.

##### Partie 2 — Durcir les erreurs

Modifiez la route de lecture pour que l'erreur interne renvoie le message
générique et le numéro de suivi prévus au contrat, et que le détail aille dans
les journaux. Le comportement normal de la route ne doit pas changer.

##### Partie 3 — Nettoyer les journaux

Reprenez l'écriture du journal de création : l'événement doit rester traçable —
qui a réservé quoi, quand — sans jamais contenir le mot de passe. Justifiez en
une phrase ce que vous mettez à la place.

##### Partie 4 — Contrôle d'accès et en-têtes

Ajoutez le contrôle qui empêche une personne de lister les réservations d'une
autre, avec le code **403** prévu au contrat. Ajoutez ensuite les en-têtes de
sécurité de réponse, au niveau du service plutôt que route par route.

---

#### ✅ Auto-évaluation

- [ ] J'ai listé ce qui sort du service, côté client et côté journal.
- [ ] L'erreur interne renvoie le code 500, un message générique et un numéro de
      suivi.
- [ ] Le détail de l'erreur est journalisé côté serveur, jamais renvoyé.
- [ ] Aucun mot de passe n'apparaît dans les journaux.
- [ ] Le contrôle d'accès empêche de lire les réservations d'autrui, avec le
      code 403.
- [ ] Les en-têtes de sécurité sont posés au niveau du service.
- [ ] Le fonctionnement normal des deux routes est inchangé.

---

#### Prolongement de l'exercice

*Facultatif — ne bloque pas la suite du parcours.*

Le service expose aussi une route de santé, utilisée par la supervision.
Proposez ce qu'elle doit renvoyer pour être utile à l'exploitation sans
renseigner quiconque la consulterait depuis l'extérieur.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Repérer ce qui sort du service

| Ce qui sort | Où | Ce que cela renseigne |
| --- | --- | --- |
| **Le message d'erreur** | réponse client | le type d'échec, parfois la structure de la base |
| **La trace complète** | réponse client | les chemins de fichiers, les versions, la ligne fautive |
| **La ligne de journal** | journal serveur | l'événement, et le mot de passe en clair |
| **La liste des réservations** | réponse client | les données d'une autre personne |

Le constat est le même pour les deux premières lignes : ce qui aide le
développeur à corriger est exactement ce qui aide quiconque à cartographier le
service. La trace complète n'a rien à faire dans une réponse client.

La troisième ligne est plus discrète et plus grave : un journal est lu par plus
de monde que la base de données, et il contient une copie des identifiants.

---

#### Partie 2 — Durcir les erreurs

La route renvoie le contrat attendu, et laisse le détail au journal :

```python
@app.get("/reservations")
def lister_reservations(email: str = ""):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations WHERE email = %s", (email,))
        rows = cursor.fetchall()
        conn.close()
        return {"reservations": rows}
    except Exception:
        reference = nouvelle_reference()
        journal.exception("echec de la lecture des reservations")
        return JSONResponse(
            status_code=500,
            content={"erreur": "la demande n'a pas pu être traitée",
                     "reference": reference},
        )
```

Le numéro de suivi est le joint entre les deux mondes : la personne signale un
numéro, l'équipe retrouve la trace complète dans les journaux. Le message
générique ne dit rien de la structure du système, et reste suffisant pour que la
personne sache que sa demande a été prise en compte.

---

#### Partie 3 — Nettoyer les journaux

L'événement reste traçable, sans le secret :

```python
journal.info("creation de reservation",
             extra={"email": email, "salle": salle})
```

Ce qui est conservé — qui a réservé quoi — suffit à reconstituer l'historique.
Ce qui disparaît — le mot de passe — n'a rien à faire là : il ne sert à rien
pour comprendre un incident de réservation, et il se retrouverait dans chaque
copie du journal.

Si le paiement doit être tracé, on journalise le **fait** et un identifiant
technique de la transaction, jamais la donnée d'authentification.

---

#### Partie 4 — Contrôle d'accès et en-têtes

Le contrôle d'accès empêche de lire les réservations d'autrui :

```python
@app.get("/reservations")
def lister_reservations(email: str = "", utilisateur=Depends(get_current_user)):
    if utilisateur["email"] != email:
        raise HTTPException(status_code=403,
                            detail="accès réservé à vos propres réservations")
    ...
```

Puis les en-têtes se posent une fois, pour tout le service :

```python
@app.middleware("http")
async def en_tetes_securite(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

Posés au niveau du service, ils couvrent aussi les routes ajoutées plus tard —
c'est l'avantage de ne pas les répéter route par route.

---

#### Points à retenir

- Ce qui aide le développeur — la trace, le détail — part dans les journaux ; la
  réponse client garde un message générique et un numéro de suivi.
- Un journal décrit **ce qui s'est passé**, pas ce que contenaient les données :
  aucun secret n'y figure.
- Le contrôle d'accès se pose sur la donnée demandée, pas seulement sur la route.
- Les en-têtes de sécurité se posent **une fois**, au niveau du service.

</details>

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
> La partie 1 de l'exercice 1 de ce chapitre, plus haut,
> est cette manipulation même, conduite sur un service complet.
>
> 🧪 **Atelier rapide (5 min)**
>
> Dans le lab du cours, lancez `lab-securite/vulnerable/app.py`, puis provoquez une
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

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** En pleine ouverture des ventes, la billetterie plante en production. Que doit recevoir la personne qui utilisait le service ?

- A. La trace complète de l'échec, pour qu'elle puisse la transmettre au support
- B. La version du moteur de base de données et la requête fautive
- C. Un message générique et un identifiant de suivi ; le détail part dans les journaux
- D. Rien : une page blanche, pour ne rien divulguer du tout

**2.** À la connexion, l'application renvoie « Le compte n'existe pas » quand l'identifiant est inconnu. Pourquoi est-ce une fuite ?

- A. Parce que le message est trop poli et n'inquiète personne
- B. Parce qu'il confirme à quelqu'un qui énumère des comptes ce qui existe
- C. Parce qu'il révèle la version du moteur de base de données
- D. Parce qu'il devrait mentionner le nombre de tentatives restantes

**3.** Un journal utile répond à quatre questions. Lesquelles ?

- A. Qui, quand, quoi, avec quel résultat
- B. Pourquoi, combien, comment, où
- C. Qui, pourquoi, quel budget, quel délai
- D. Quelle version, quel correctif, quel test, quel déploiement

**4.** Pour comprendre un problème de connexion, faut-il journaliser la requête de connexion complète ?

- A. Oui : sans la requête entière dans le journal, on ne peut rien reconstituer quand l'enquête arrive des semaines plus tard
- B. Oui, à condition que le journal soit chiffré et réservé à l'équipe sécurité, ce qui rendrait la valeur inutilisable ailleurs
- C. Non : on journalise le fait que l'authentification a échoué, jamais le mot de passe ni le jeton
- D. Non : une tentative de connexion n'est pas un incident, elle n'a donc pas sa place dans un journal d'application

**5.** *Question ouverte (2-3 lignes).* « Un journal n'est pas une copie de la base. » Expliquez la formule, et pourquoi une copie des identifiants dans un journal est pire que dans la base elle-même.

---

<details>

<summary>Vérifier ses réponses</summary>

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

</details>

---

[← Chapitre précédent](03-xss-et-sorties.md) · [Sommaire](Readme.md) · [Chapitre suivant →](05-dependances-et-configuration.md)
