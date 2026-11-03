# Exercice — Rédiger un mini-plan de réponse à incident

> 🔵 **Intégration** · **Durée :** 55 min · **Lien :** chapitre
> [Réponse à incident](../17-reponse-incident.md)
> **Objectif :** produire un mini-plan de réponse à incident exécutable pour une
> PME, des premières actions jusqu'à la communication.

---

## Contexte

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

## Consignes

### Partie 1 — Ordonner les premières actions

Proposez l'ordre des premières actions à lancer, en couvrant les cinq temps du
chapitre. Pour chacune, indiquez **ce qu'elle produit comme résultat
vérifiable** — pas seulement ce qu'elle « fait ». Dites enfin ce qu'il ne faut
**surtout pas** faire avant d'avoir observé et relevé ce qui se passe.

### Partie 2 — Rédiger le mini-plan

Rédigez la partie « organisation » du plan : les rôles du chapitre (pilote,
technique, communication, décideur), la personne qui les tient dans cette équipe,
le canal de communication interne, et la fréquence des points d'avancement pendant
l'incident.

### Partie 3 — Décider face à la rançon et à la restauration

Traitez deux décisions, en justifiant chacune : **payer la rançon ou non**, et
**quelle sauvegarde restaurer, comment, et avec quelle vérification** avant la
remise en service. Tenez compte de ce que le contexte dit du serveur de
sauvegarde.

### Partie 4 — Organiser la notification et la communication

Décidez qui notifie l'autorité de contrôle, avec quelles informations, et qui
informe les chauffeurs et les clients. Rédigez les **quatre premières phrases** du
premier message destiné aux clients.

---

## ✅ Auto-évaluation

Avant de passer au corrigé, vérifiez que :

- [ ] Mes premières actions sont **ordonnées**, et chacune produit un résultat
  vérifiable (un relevé fait, une décision prise, un message envoyé).
- [ ] J'ai nommé **qui tient chaque rôle**, même si une personne en cumule
  plusieurs.
- [ ] Mes deux décisions de la partie 3 sont **justifiées par les faits du
  contexte**, et pas par une règle générale.
- [ ] Ma notification tient compte du **délai** rappelé dans le contexte, et mon
  message client ne spéculé sur rien.
- [ ] Mon plan dit explicitement **ce qu'on ne fait pas** (les gestes qui
  détruisent les traces ou aggravent la situation).

---

## Pour aller plus loin

*Facultatif.* Que faudrait-il avoir **préparé avant l'incident** pour que ce plan
soit exécutable demain matin, sans discussion ? Listez les préparatifs, du plus
urgent au plus confortable.
