# Corrigé — Rédiger un mini-plan de réponse à incident

> Corrigé de [l'exercice « Rédiger un mini-plan de réponse à
> incident »](../17-plan-incident.md). Comparez d'abord votre travail aux
> **étapes** ci-dessous : la méthode compte autant que le résultat.

---

## Partie 1 — Ordonner les premières actions

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

## Partie 2 — Rédiger le mini-plan

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

## Partie 3 — Décider face à la rançon et à la restauration

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

## Partie 4 — Organiser la notification et la communication

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

## Points à retenir

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
