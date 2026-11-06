[← Chapitre précédent](16-tests-securite.md) · [Sommaire](Readme.md) · [Chapitre suivant →](18-maturite-et-perspectives.md)

# Réponse à incident — le jour où ça casse

> Un vendredi matin, la base de commandes d'une plateforme de livraison ne répond
> plus. Les fichiers portent une extension inconnue, et un message demande une
> rançon. Qui décide quoi ? Qui parle aux clients ? Qui a le droit d'éteindre un
> serveur ? Sans plan écrit, chacun improvise à sa place — et l'incident dure bien
> plus longtemps qu'il ne devrait, parce que les bonnes décisions arrivent dans le
> mauvais ordre. La réponse à incident ne consiste pas à être plus brillant le jour
> venu : elle consiste à avoir **écrit à l'avance** ce qu'on fera.

**Durée de lecture :** 55 min hors approfondissements facultatifs · **Prérequis :** les notions de vulnérabilités et
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


---

### Exercice 1 — Rédiger un mini-plan de réponse à incident (40 min)

#### Contexte

**Transports Virelai** est un transporteur régional de marchandises. Un mardi
matin, l'application de planification des tournées est à l'arrêt : la base
`expeditions` est chiffrée par un ransomware, et un message demande une rançon de
20 000 € pour la clé de déchiffrement.

Ce que l'équipe sait à ce stade :

- la sauvegarde la plus récente date de **la veille**, mais le serveur de
  sauvegarde était joignable depuis le réseau où l'attaque a eu lieu ;
- les données personnelles sont concernées : noms et coordonnées des chauffeurs,
  adresses de livraison des clients. Le RGPD (Règlement général sur la protection
  des données) impose une notification à l'autorité de contrôle dans les **72 h**
  après prise de conscience de l'incident ;
- trois équipes attendent des instructions : exploitation, informatique,
  direction.

Le directeur vous demande « le plan, maintenant ». Vous rédigez le document que
l'équipe suivra.

---

#### Consignes

##### Partie 1 — Ordonner les premières actions

Proposez l'ordre des premières actions à lancer, en couvrant les cinq temps du
chapitre. Pour chacune, indiquez **ce qu'elle produit comme résultat
vérifiable** — pas seulement ce qu'elle « fait ». Dites enfin ce qu'il ne faut
**surtout pas** faire avant d'avoir observé et relevé ce qui se passe.

##### Partie 2 — Rédiger le mini-plan

Rédigez la partie « organisation » du plan : les rôles du chapitre (pilote,
technique, communication, décideur), la personne qui les tient dans cette équipe,
le canal de communication interne, et la fréquence des points d'avancement pendant
l'incident.

##### Partie 3 — Décider face à la rançon et à la restauration

Traitez deux décisions, en justifiant chacune : **payer la rançon ou non**, et
**quelle sauvegarde restaurer, comment, et avec quelle vérification** avant la
remise en service. Tenez compte de ce que le contexte dit du serveur de
sauvegarde.

##### Partie 4 — Organiser la notification et la communication

Décidez qui notifie l'autorité de contrôle, avec quelles informations, et qui
informe les chauffeurs et les clients. Rédigez les **quatre premières phrases** du
premier message destiné aux clients.

---

#### ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Mes premières actions sont **ordonnées**, et chacune produit un résultat
  vérifiable (un relevé fait, une décision prise, un message envoyé).
- [ ] J'ai nommé **qui tient chaque rôle**, même si une personne en cumule
  plusieurs.
- [ ] Mes deux décisions de la partie 3 sont **justifiées par les faits du
  contexte**, et pas par une règle générale.
- [ ] Ma notification tient compte du **délai** rappelé dans le contexte, et mon
  message client ne spécule sur rien.
- [ ] Mon plan dit explicitement **ce qu'on ne fait pas** (les gestes qui
  détruisent les traces ou aggravent la situation).

---

#### Pour aller plus loin

*Facultatif.* Que faudrait-il avoir **préparé avant l'incident** pour que ce plan
soit exécutable demain matin, sans discussion ? Listez les préparatifs, du plus
urgent au plus confortable.

<details>
<summary>Voir la correction</summary>

> Comparez d'abord votre travail aux **étapes** ci-dessous : la méthode compte autant que le résultat.

#### Partie 1 — Ordonner les premières actions

**Éléments attendus :**

| Action | Ce qu'elle produit (vérifiable) | Son rang |
| --- | --- | --- |
| Constat et relevé | une chronologie datée de ce qui s'observe, les machines touchées, le message de rançon capturé | d'abord : rien ne se décide sans savoir ce qui se passe |
| Contention | la base `expeditions` isolée, les accès du compte suspect désactivés, le réseau coupé entre les zones | ensuite : empêcher l'extension sans détruire les traces |
| Analyse de la porte d'entrée | une hypothèse écrite sur le chemin d'attaque, et la preuve qu'elle est fermée | avant toute restauration |
| Restauration | une sauvegarde restaurée **sur un système vérifié**, avec un contrôle que le chiffrement ne revient pas | après l'éradication |
| Communication | les notifications lancées, le point interne fait | en parallèle dès la contention, dans le respect du délai |

**Ce qu'on ne fait surtout pas avant d'avoir observé et relevé :**

- éteindre ou réinstaller les machines touchées — les traces disparaissent avec ;
- déchiffrer ou restaurer « pour voir » sur le système contaminé ;
- répondre au message de rançon ou payer avant décision collective ;
- effacer les journaux, même « pour nettoyer ».

**Erreurs fréquentes :** traiter d'abord la remise en service (la pression
opérationnelle est réelle, mais restaurer avant d'avoir fermé la porte d'entrée
reproduit l'incident), ou communiquer avant d'avoir relevé les faits.

---

#### Partie 2 — Rédiger le mini-plan

**Éléments attendus :**

| Rôle | Qui le tient ici | Sa décision |
| --- | --- | --- |
| Pilote de l'incident | le responsable informatique | coordonne, tranche les priorités, tient la chronologie |
| Équipe technique | l'administrateur système, aidé du prestataire habituel | observe, contient, restaure |
| Communication | la responsable exploitation | informe les chauffeurs, les clients, les autorités |
| Décideur | le directeur | arbitre entre continuer à servir et tout arrêter, engage les moyens |

- **Canal interne** : un canal unique et écrit (une messagerie de crise ou un fil
  dédié), pour que la chronologie se construisse toute seule.
- **Fréquence des points** : un point toutes les heures au début, puis un point à
  chaque changement de phase. L'important est la **régularité annoncée** : chacun
  sait quand la prochaine information arrive.

**Ce qu'il faut retenir :** dans une petite équipe, une personne cumule souvent
plusieurs rôles. Ce qui compte est que chaque rôle ait un titulaire connu de
tous — sinon, la première décision contestée fait perdre un temps précieux.

---

#### Partie 3 — Décider face à la rançon et à la restauration

**Éléments attendus :**

**Sur la rançon (20 000 €) :** la décision se prend en équipe, avec le décideur,
et la position par défaut est de **ne pas payer**. Les raisons, tirées du
contexte : rien ne garantit la clé, rien ne garantit que les données ne seront
pas revendues ou publiées, et payer finance la même activité contre d'autres
entreprises. La décision et ses motifs sont écrits dans la chronologie.

**Sur la restauration :** la sauvegarde de la veille est la seule candidate, mais
le contexte précise que le serveur de sauvegarde était **joignable depuis le
réseau attaqué**. La restauration se fait donc ainsi :

1. restaurer sur un système **neuf ou réinstallé**, jamais sur la machine
   chiffrée ;
2. vérifier, avant remise en service, que la sauvegarde elle-même ne contient pas
   le chiffrement (ouvrir les fichiers, contrôler les dates de modification) ;
3. remettre en service en surveillant, et prévoir le retour en arrière si le
   chiffrement réapparaît.

**Erreurs fréquentes :** restaurer sur la machine d'origine, ou restaurer sans
vérifier la sauvegarde — dans les deux cas, l'incident recommence.

---

#### Partie 4 — Organiser la notification et la communication

**Éléments attendus :**

- **Qui notifie** : la responsable communication prépare la notification, le
  décideur la valide. L'autorité de contrôle est la CNIL (Commission nationale de
  l'informatique et des libertés).
- **Quand** : dans les **72 h** après prise de conscience, délai rappelé dans le
  contexte. Si l'analyse n'est pas terminée, la notification part quand même, avec
  ce qui est établi et la suite annoncée.
- **Avec quelles informations** : la nature de l'incident, les catégories de
  données et de personnes concernées, les mesures prises, les contacts, et ce qui
  est encore en cours d'analyse.
- **Qui informe les personnes** : la même responsable communication, aux
  chauffeurs par le canal interne, aux clients par le canal habituel.

**Premier message aux clients — quatre phrases attendues** (les faits établis, les
données concernées, les mesures prises, la suite) :

> Nous avons détecté un incident informatique affectant notre application de
> planification des tournées. Les adresses de livraison que vous nous avez
> confiées, ainsi que les coordonnées de nos chauffeurs, font partie des données
> concernées. Nous avons isolé les systèmes touchés et une enquête est en cours
> avec l'autorité de contrôle. Nous reviendrons vers vous dès que notre analyse
> sera terminée, et vous pouvez nous joindre à l'adresse
> contact@transports-virelai.example.

**Ce qu'il ne faut pas écrire** : la cause avant qu'elle soit établie, l'ampleur
avant qu'elle soit mesurée, une promesse de délai de résolution, ou toute
formulation qui minimise.

---

#### Points à retenir

- Les premières actions suivent les **cinq temps** du chapitre, et chacune produit
  un résultat vérifiable avant la suivante.
- **Rien ne se détruit avant d'avoir relevé** : éteindre, réinstaller ou effacer
  fait disparaître ce dont l'équipe a besoin.
- La rançon se décide en équipe, et la position par défaut est de **ne pas
  payer** ; la décision et ses motifs sont écrits.
- Une sauvegarde restaurée se **vérifie** avant la remise en service, surtout
  quand le serveur de sauvegarde était accessible depuis le réseau attaqué.
- La notification dans les **72 h** et le message aux clients se préparent : faits
  établis, données concernées, mesures prises, suite annoncée.

</details>

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

> 🔁 **Pour aller plus loin (facultatif)** — à lire si le créneau le permet, rien d'obligatoire n'en dépend
>
> 💡 **Astuce** — une action de post-mortem sans responsable ni échéance est un
> vœu. Trois actions datées valent mieux qu'une liste de quinze intentions.

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

## 🧠 Vérifiez vos acquis

*Formatif, jamais noté. Répondez sans relire le chapitre, puis dépliez « Vérifier ses réponses » : ce qui compte est de repérer où vous vacillez, pas de faire 5 sur 5.*

**1.** L'équipe veut aller vite : elle restaure la sauvegarde avant d'avoir supprimé la cause de l'intrusion. Quel temps de la réponse a été sauté, et quel risque prend-elle ?

- A. Détecter : elle traite ce qui arrive comme une panne alors qu'il s'agit d'une intrusion en cours
- B. Contenir : en redémarrant au hasard, elle détruit les traces dont l'analyse aurait eu besoin
- C. Éradiquer : elle repart d'une sauvegarde contaminée ou garde la porte d'entrée ouverte, et l'incident recommence
- D. Capitaliser : elle ne rédige aucun retour d'expérience et l'équipe n'apprend rien de l'incident

**2.** Parmi ces actions, laquelle relève d'une containment correcte ?

- A. Formater le disque de la machine compromise pour repartir propre
- B. Effacer les journaux pour que personne ne les lise
- C. Réinstaller la machine sans rien relever, tout de suite
- D. Désactiver le compte détourné et isoler le segment concerné

**3.** Un incident a exposé des données personnelles. Que impose le RGPD ?

- A. Informer les clients dans les trente jours qui suivent l'incident, par un courriel groupé envoyé à toute la base
- B. Notifier l'autorité de contrôle — la CNIL en France — dans les 72 h de la prise de conscience, sauf risque faible ; les personnes concernées quand le risque est élevé
- C. Attendre la fin de l'analyse technique avant toute notification, afin de ne rien annoncer d'erroné à l'autorité
- D. Rien d'automatique : seule une plainte déposée par une personne concernée ferait naître l'obligation de notifier

**4.** L'incident dure ; faut-il continuer à servir les clients ou tout arrêter ? Qui arbitre cette décision ?

- A. Le pilote de l'incident, qui coordonne et tient le fil du temps
- B. L'équipe technique, qui observe et restaure
- C. La communication, qui informe l'interne et les clients
- D. Le décideur, qui engage les moyens

**5.** *Question ouverte (2-3 lignes).* « On cherche ce qui a permis l'incident, pas qui l'a laissé faire. » Pourquoi cette règle d'or du post-mortem, et que doit contenir le document ?

---

<details>

<summary>Vérifier ses réponses</summary>

### Réponses

**1. C.** Les cinq temps sont ordonnés : détecter, contenir, éradiquer, restaurer, capitaliser — l'ordre compte plus que la vitesse. Restaurer avant d'avoir éradiqué, c'est repartir trop vite, avec la même faille qu'avant.
**Pourquoi :** le piège classique d'éradiquer est de restaurer une sauvegarde contaminée ou de corriger le symptôme seul : la porte d'entrée doit être fermée avant la remise en service.

**2. D.** Contenir n'est pas détruire : couper un accès, isoler un segment, désactiver un compte — oui. Formater un disque, effacer des journaux, réinstaller sans rien relever — non.
**Pourquoi :** les traces servent à comprendre ce qui s'est passé, à savoir quoi restaurer, et parfois à constituer un dossier.

**3. B.** Ces délais se préparent : savoir qui notifie, avec quelles informations, et comment on contacte les personnes ne s'improvise pas le jour de l'incident.
**Pourquoi :** côté message, on dit ce qui est établi et depuis quand, on nomme un interlocuteur unique, on annonce la prochaine communication avec sa date — sans spéculer sur l'ampleur ni promettre une résolution qu'on ne maîtrise pas.

**4. D.** Le décideur engage les moyens et arbitre entre continuer à servir et tout arrêter. Le pilote coordonne et tranche les priorités, l'équipe technique observe, contient, restaure, la communication informe.
**Pourquoi :** les rôles sont nommés dans le plan, avant l'incident, pas pendant ; dans une petite équipe une personne cumule plusieurs rôles, mais les rôles restent nommés pour que personne ne se demande qui tranche.

**5.** Attendu : un retour d'expérience qui finit en recherche de responsables ne produit plus jamais de récit honnête — la prochaine fois, personne ne dira « j'avais vu le signal et je n'ai rien fait ». Le document tient en quatre parties : la chronologie heure par heure avec les sources, les causes (porte d'entrée, extension, détection tardive), ce qui a aidé, et les changements à apporter.
**Pourquoi :** chaque changement doit avoir un responsable et une échéance, sinon le post-mortem reste une liste d'intentions.

</details>

---

[← Chapitre précédent](16-tests-securite.md) · [Sommaire](Readme.md) · [Chapitre suivant →](18-maturite-et-perspectives.md)
