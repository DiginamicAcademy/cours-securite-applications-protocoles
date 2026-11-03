[← Chapitre précédent](16-tests-securite.md) · [Sommaire](Readme.md) · [Chapitre suivant →](18-maturite-et-perspectives.md)

# Réponse à incident — le jour où ça casse

> Un vendredi matin, la base de commandes d'une plateforme de livraison ne répond
> plus. Les fichiers portent une extension inconnue, et un message demande une
> rançon. Qui décide quoi ? Qui parle aux clients ? Qui a le droit d'éteindre un
> serveur ? Sans plan écrit, chacun improvise à sa place — et l'incident dure bien
> plus longtemps qu'il ne devrait, parce que les bonnes décisions arrivent dans le
> mauvais ordre. La réponse à incident ne consiste pas à être plus brillant le jour
> venu : elle consiste à avoir **écrit à l'avance** ce qu'on fera.

**Durée de lecture :** 50 min · **Prérequis :** les notions de vulnérabilités et
d'incident des journées précédentes

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Découper** une réponse à incident en cinq temps ordonnés, du signal au retour
  d'expérience.
- **Rédiger** les premières actions d'une réponse, dans l'ordre où elles sont
  utiles.
- **Appliquer** les obligations de notification quand des données personnelles
  sont concernées.
- **Conduire** un retour d'expérience qui produit des changements, pas des
  reproches.

---

## I. Les cinq temps

### L'ordre compte plus que la vitesse

Un incident se traite dans un ordre précis. Sauter une étape — restaurer avant
d'avoir éradiqué, nettoyer avant d'avoir observé — fait perdre du temps et
détruit des indices dont on aura besoin.

```text
   1. Détecter     repérer le signal, confirmer qu'il s'agit bien d'un incident
        │
   2. Contenir     limiter l'extension, sans détruire les traces
        │
   3. Éradiquer    supprimer la cause, pas seulement les symptômes
        │
   4. Restaurer    remettre en service, vérifié, en tenant compte de ce qu'on a appris
        │
   5. Capitaliser  écrire ce qui s'est passé, changer ce qui a failli
```

| Temps | La question à se poser | Le piège classique |
| --- | --- | --- |
| **Détecter** | qu'est-ce qui me fait dire qu'un incident a lieu ? | confondre une panne et une intrusion, et traiter la mauvaise chose |
| **Contenir** | comment empêcher que ça s'étende, sans tout casser ? | éteindre la machine compromise, et perdre les traces avec |
| **Éradiquer** | quelle est la porte d'entrée, et est-elle fermée ? | restaurer une sauvegarde contaminée, ou corriger le symptôme seul |
| **Restaurer** | comment remettre en service en vérifiant que c'est propre ? | repartir trop vite, avec la même faille qu'avant |
| **Capitaliser** | qu'est-ce qui a permis ou retardé la réponse ? | ne rien écrire, et rejouer la même improvisation au prochain incident |

> ⚠️ **Point d'attention** — contenir n'est pas détruire. Couper un accès, isoler
> un segment, désactiver un compte : oui. Formater un disque, effacer des
> journaux, réinstaller sans rien relever : non. Les traces de l'incident servent
> à comprendre ce qui s'est passé, à savoir quoi restaurer, et parfois à
> constituer un dossier.

### Qui décide quoi

Le plan écrit nomme les rôles avant l'incident, pas pendant :

| Rôle | Sa décision |
| --- | --- |
| **Pilote de l'incident** | coordonne, tranche les priorités, tient le fil du temps |
| **Équipe technique** | observe, contient, restaure |
| **Communication** | informe l'interne, les clients, les autorités selon les règles |
| **Décideur** | engage les moyens, arbitre entre continuer à servir et tout arrêter |

Dans une petite équipe, une personne cumule plusieurs rôles — mais les rôles
restent nommés, pour que personne ne se demande qui tranche.

---

## II. Communication

### Les obligations légales

Quand un incident expose des **données personnelles**, la loi encadre la
notification. Le RGPD (Règlement général sur la protection des données) impose
d'en notifier l'autorité de contrôle — en France, la CNIL (Commission nationale de
l'informatique et des libertés) — dans les **72 h** après en avoir pris
conscience, sauf si l'incident est peu susceptible d'engendrer un risque pour les
personnes. Les personnes concernées sont informées quand le risque est élevé.

Ces délais se préparent : savoir **qui** notifie, **avec quelles informations**, et
**comment on contacte les personnes** ne s'improvise pas le jour de l'incident.

### Informer sans aggraver

| À faire | À éviter |
| --- | --- |
| dire ce qui est **établi**, et depuis quand | spéculer sur l'ampleur ou l'origine avant l'analyse |
| nommer un interlocuteur unique | laisser chacun répondre de son côté |
| donner les mesures de protection pour les personnes | minimiser pour rassurer |
| annoncer la prochaine communication, avec sa date | promettre une résolution qu'on ne maîtrise pas |

> 🧪 **Atelier rapide (10 min)**
>
> La plateforme de livraison **Livraison Cadence** vient de découvrir qu'un tiers
> a exfiltré sa table de commandes : noms, adresses de livraison, historique des
> commandes. Rédigez **les quatre premières actions** à lancer, dans l'ordre, en
> une phrase chacune. Pour chacune, dites qui la conduit et ce qu'elle produit
> comme résultat vérifiable.

### La communication interne

L'incident se vit aussi en interne : les équipes ont besoin de savoir ce qu'elles
peuvent dire, à qui, et quand. Un message court, factuel, régulier, évite deux
écueils : la rumeur qui remplace l'information, et le silence qui fait croire que
personne ne fait rien.

---

## III. Retour d'expérience

### Le post-mortem sans coupable

Une fois l'incident clos, l'équipe écrit ce qui s'est passé. La règle d'or : **on
cherche ce qui a permis l'incident, pas qui l'a laissé faire**. Un retour
d'expérience qui finit en recherche de responsables ne produit plus jamais de
récit honnête : la prochaine fois, personne ne dira « j'avais vu le signal et je
n'ai rien fait ».

Le document tient en quelques parties :

1. la **chronologie** : ce qui s'est passé, heure par heure, avec les sources ;
2. les **causes** : la porte d'entrée, ce qui a permis l'extension, ce qui a
   retardé la détection ;
3. ce qui a **aidé** : les mesures, les outils, les personnes qui ont accéléré la
   réponse ;
4. les **changements** : ce qui doit bouger, avec un responsable et une échéance
   pour chacun.

> 💡 **Astuce** — une action de post-mortem sans responsable ni échéance est un
> vœu. Trois actions datées valent mieux qu'une liste de quinze intentions.

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour terminer
la journée.*

- **Les exercices de crise** — simuler un incident, avec les vrais rôles et les
  vrais canaux de communication, révèle les blocages qu'aucun document ne montre.
  Une simulation par an suffit à garder le plan vivant.
- **Les cellules CERT** — un CERT (Computer Emergency Response Team, l'équipe
  spécialisée dans la réponse à incident) mutualise la veille, l'expertise et la
  réponse entre plusieurs organisations. Les guides publics de l'ANSSI (Agence
  nationale de la sécurité des systèmes d'information) décrivent ces
  organisations et fournissent des modèles de documents.
- **La préparation technique** — centraliser les journaux, conserver des sauvegardes
  vérifiées, documenter les dépendances : tout ce qui a été préparé avant l'incident
  se paie le jour venu.

---

## Points clés

- La réponse à incident suit **cinq temps** : détecter, contenir, éradiquer,
  restaurer, capitaliser. L'ordre compte plus que la vitesse.
- **Contenir n'est pas détruire** : les traces servent à comprendre, restaurer et
  parfois prouver.
- Les rôles sont **nommés à l'avance** : pilote, technique, communication,
  décideur.
- Une fuite de données personnelles déclenche une **notification dans les 72 h** à
  l'autorité de contrôle : cette obligation se prépare, elle ne s'improvise pas.
- Le retour d'expérience cherche **ce qui a permis l'incident**, pas qui l'a
  laissé faire ; chaque changement a un responsable et une échéance.

---

[← Chapitre précédent](16-tests-securite.md) · [Sommaire](Readme.md) · [Chapitre suivant →](18-maturite-et-perspectives.md)
