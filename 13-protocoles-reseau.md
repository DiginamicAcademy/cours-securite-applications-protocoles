# Protocoles réseau — ce que le réseau chiffre, et ce qu'il laisse ouvert

> Le courrier électronique naît en 1982 avec SMTP (Simple Mail Transfer Protocol, le
> protocole d'envoi du courrier), dans un monde de confiance : les machines se
> connaissent, personne ne ment, et le réseau est un campus universitaire. Quarante
> ans plus tard, les mêmes protocoles transportent nos mots de passe. DNS (Domain
> Name System, l'annuaire qui traduit les noms de domaine en adresses) résout les
> noms, SSH (Secure Shell, l'accès distant chiffré) administre les serveurs, HTTPS
> (la version chiffrée du protocole du web) protège les pages — et chacun garde les
> hypothèses de son époque.

**Durée de lecture :** 70 min · **Prérequis :** les vulnérabilités web des journées
précédentes, la notion de chiffrement

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Décrire** ce que chaque protocole courant chiffre réellement — et ce qui circule
  en clair malgré lui.
- **Repérer** les failles de conception héritées des protocoles anciens : interception,
  dégradation forcée, usurpation de nom.
- **Décider** des mesures de durcissement adaptées à un service : HTTPS imposé,
  résolution de noms authentifiée, accès par clé.
- **Vérifier** sur un service réel les en-têtes qui attestent d'une connexion chiffrée.

---

## I. HTTPS, DNS, SMTP, SSH — ce que chacun chiffre (ou pas)

Quatre protocoles, quatre époques. Ce que chacun protège dépend de ce que son
concepteur voulait protéger — et les menaces de 1982 n'étaient pas celles
d'aujourd'hui.

| Protocole | Né en | Ce qu'il chiffre | Ce qui reste ouvert |
| --- | --- | --- | --- |
| **DNS** | 1983 | rien, dans sa version d'origine | la requête et la réponse : n'importe qui peut dire « ce nom pointe ici » |
| **SMTP** | 1982 | rien au départ, le chiffrement est venu après | le contenu du courrier et les identifiants, si le transport n'est pas chiffré |
| **HTTP** | 1991 | rien | tout : pages, formulaires, jetons de session, cookies |
| **SSH** | 1995 | tout, dès l'origine | la confiance accordée à la première connexion (voir plus bas) |

HTTPS n'est pas un protocole à part : c'est HTTP (HyperText Transfer Protocol, le
protocole du web) transporté dans TLS (Transport Layer Security, la couche de
chiffrement qui sécurise les échanges). La même logique vaut ailleurs : la version
chiffrée de SMTP repose sur TLS, et SSH embarque son propre chiffrement.

Ce que TLS garantit, concrètement :

- la **confidentialité** — personne sur le chemin ne lit ce qui circule ;
- l'**intégrité** — personne ne modifie un octet sans que ça se voie ;
- l'**authentification du serveur** — le certificat prouve à qui vous parlez.

Ce que TLS **ne** garantit **pas** : que le site est honnête, que vos données sont
bien stockées côté serveur, ou que le nom de domaine que vous avez tapé est celui
que vous vouliez. Un site de phishing parfaitement chiffré reste un site de
phishing.

> ⚠️ **Point d'attention** —
> Le cadenas du navigateur ne dit pas « ce site est sûr ». Il dit « cet échange est
> chiffré et le serveur prouve être le propriétaire du nom de domaine ». La nuance
> change tout quand on évalue un risque.

> 🧪 **Atelier rapide (8 min)**
>
> Comparez les en-têtes d'un service local en clair et d'un service réel chiffré :
>
```bash
curl -I http://localhost:8080
curl -I https://tutor.diginamic.fr/docs
```

> (La seconde commande interroge un service de production : une seule requête de
> lecture, jamais plus.) Notez les en-têtes présents d'un côté et absents de
> l'autre, en particulier `Strict-Transport-Security` et `Server`. Que dit
> l'absence d'en-tête de sécurité sur la configuration du service ?

---

## II. Failles courantes

Les protocoles anciens ont été conçus pour un réseau amical. Les attaques
d'aujourd'hui exploitent précisément ce qu'ils n'ont pas prévu.

### Usurpation de résolution de noms

Le DNS d'origine répond sans preuve. Quiconque peut répondre plus vite que le
serveur légitime — ou corrompre un cache — redirige les victimes vers une machine
contrôlée par l'attaquant, tout en affichant le bon nom de domaine. C'est le
**DNS spoofing** (usurpation de réponse DNS). La victime tape le bon nom, obtient
la mauvaise machine, et si elle accepte n'importe quel certificat, elle ne voit
rien.

### Interception et dégradation forcée

Deux attaques du même genre, très employées contre les protocoles qui chiffrent
« si possible » :

| Attaque | Ce que fait l'attaquant | Protocole visé |
| --- | --- | --- |
| **Interception** | le MITM (man in the middle, l'attaque par personne interposée) se place entre le client et le serveur et relaie les échanges | tous |
| **Dégradation forcée** (downgrade) | fait croire au client que le serveur ne sait pas chiffrer, pour récupérer la version en clair | SMTP, les anciennes versions de TLS |
| **Interception de la montée en chiffrement** | laisse passer la commande de chiffrement, l'annule, continue en clair | STARTTLS (la commande qui négocie le chiffrement en cours de connexion) |

Le cas de STARTTLS est emblématique : le client annonce « je peux chiffrer », le
serveur répond « moi aussi », puis les deux basculent. Entre les deux messages,
l'attaquant peut effacer la proposition — les deux extrémités croient que l'autre
ne chiffre pas et poursuivent en clair. Le chiffrement était disponible, il n'a
simplement jamais été utilisé.

> 🚨 **Piège à éviter** —
> « Notre messagerie est chiffrée, on utilise STARTTLS » ne suffit pas. Si le
> repli en clair est accepté, un attaquant sur le chemin obtient exactement ce
> qu'il veut. Un chiffrement optionnel est un chiffrement contournable.

### Les versions et les algorithmes morts

Un protocole vivant garde ses anciennes versions pour compatibilité — et chacune
porte ses faiblesses. SSL (Secure Sockets Layer, l'ancêtre de TLS) est cassé
depuis des années ; TLS 1.0 et 1.1 sont déconseillés. Les maintenir « pour les
vieux clients », c'est offrir à l'attaquant la porte d'entrée qu'il cherche : il
demande la version faible, le serveur accepte.

---

## III. Durcissement

Chaque faille ci-dessus a une réponse directe, applicable sans réécrire le
protocole.

### Imposer le chiffrement au lieu de le proposer

HSTS (HTTP Strict Transport Security, l'en-tête qui interdit le repli en clair)
dit au navigateur : « pour ce domaine, le HTTPS est obligatoire, et ce pendant un
an ». Même si l'utilisateur tape `http://`, même si un lien propose le clair, le
navigateur refuse et chiffre. La première visite reste à protéger par ailleurs —
d'où l'inscription du domaine dans les listes de préchargement des navigateurs.

```bash
# Ce que le serveur doit renvoyer, en tête de chaque réponse
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Authentifier les réponses DNS

DNSSEC (DNS Security Extensions, les extensions de sécurité du DNS) fait signer
les réponses de résolution par le détenteur de la zone. Le client vérifie la
signature et refuse une réponse falsifiée. Ce n'est pas du chiffrement — la
requête reste lisible — mais l'usurpation devient détectable. La montée en
chiffrement du DNS lui-même arrive ensuite, avec DoH (DNS over HTTPS, la
résolution de noms transportée dans HTTPS) et DoT (DNS over TLS).

### Administrer par clé, pas par mot de passe

Sur SSH, deux façons de s'authentifier :

| Mécanisme | Résistance | Ce qui reste à faire |
| --- | --- | --- |
| Mot de passe | faible — devinable, réutilisable, interceptable | le désactiver purement |
| Clé publique | forte — la clé privée ne quitte jamais le poste | protéger la clé, limiter les comptes autorisés |

Le durcissement standard d'un serveur SSH tient en quelques lignes de
configuration : clés uniquement, comptes nommés, journalisation des connexions.

```text
PasswordAuthentication no
PermitRootLogin no
AllowUsers admin-data
```

> 💡 **Astuce** —
> Avant de désactiver l'authentification par mot de passe, vérifiez qu'une clé est
> bien installée et testée sur un second canal. Se verrouiller dehors de son propre
> serveur est le seul incident que ce durcissement provoque lui-même.

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour terminer
la journée.*

- **TLS 1.3** — la version actuelle du protocole raccourcit la négociation à un
  aller-retour, supprime les algorithmes anciens et chiffre davantage d'en-têtes.
  Une migration vers TLS 1.3 est souvent l'occasion de nettoyer toute la
  configuration de chiffrement.
- **DoH et DoT** — chiffrer la résolution de noms protège la navigation de
  l'observation, mais concentre la confiance sur quelques résolveurs : un choix
  d'architecture, pas une simple case à cocher.
- **La surveillance des certificats** — les journaux publics de certificats
  permettent de détecter un certificat émis pour votre domaine sans votre accord.
  Un abonnement à ces alertes coûte quelques minutes et en sauve des jours.

---

## Points clés

- Chaque protocole chiffre **ce que son époque menaçait** : DNS et SMTP d'origine
  ne chiffraient rien, HTTPS et SSH chiffrent presque tout.
- TLS garantit la confidentialité, l'intégrité et l'identité du serveur — **pas**
  l'honnêteté du site ni la sécurité du stockage.
- Un chiffrement **optionnel** est contournable : dégradation forcée, interception
  de la montée en chiffrement, repli en clair.
- Le durcissement tient en trois gestes : **imposer** le chiffrement (HSTS),
  **authentifier** les réponses (DNSSEC), **administrer par clé** (SSH).
