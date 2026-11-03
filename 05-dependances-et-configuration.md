[← Chapitre précédent](04-erreurs-et-logging.md) · [Sommaire](Readme.md) · [Chapitre suivant →](06-revue-de-code-securite.md)

# Dépendances et configuration — ce qui tourne autour du code

> L'équipe data d'une mutuelle maintient un petit service d'export de rapports.
> Le lundi matin, l'analyse de dépendances signale une vulnérabilité dans une
> bibliothèque de mise en page de documents. Personne n'a écrit cette
> bibliothèque, personne ne l'a choisie : elle est arrivée avec une autre. Et
> pourtant, c'est votre service qui est exposé. Tu ne changes pas le monde — tu
> changes **ta version**.

**Durée de lecture :** 65 min · **Prérequis :** le cycle de vie d'une
vulnérabilité connue, et le chapitre
[XSS (Cross-Site Scripting) et sorties](03-xss-et-sorties.md)

---

## Objectifs

À l'issue de ce chapitre, vous serez capable de :

- **Lire** un avis de sécurité et en tirer ce qui concerne votre projet.
- **Évaluer** l'exposition réelle d'une dépendance signalée, avant de corriger.
- **Appliquer** un correctif de dépendance, tester l'absence de régression, et
  rétro-patcher si la mise à jour complète est impossible.
- **Durcir** la configuration d'un service : en-têtes de sécurité, mode debug,
  emplacement des secrets.

---

## I. SCA et réponse à une CVE

Le SCA (Software Composition Analysis) est l'analyse de ce que votre projet
**embarque** : bibliothèques, moteurs, outils de build. Un scanner SCA compare
la liste de vos dépendances aux bases de vulnérabilités connues et signale ce
qui est affecté.

Quand il sonne, la réaction se déroule en quatre temps :

| Étape | Ce qu'on fait | Ce qu'on cherche |
| --- | --- | --- |
| **Lire** | ouvrir l'avis de sécurité | la faille décrite, les versions concernées |
| **Situer** | regarder si le code vulnérable est appelé | l'exposition réelle, pas la simple présence |
| **Corriger** | monter la version, ou rétro-patcher | le plus petit changement qui ferme la faille |
| **Vérifier** | relancer les tests, rejouer le cas | l'absence de régression |

L'ordre compte. Corriger sans lire conduit à monter une version majeure qui
casse le service ; lire sans situer conduit à traiter en urgence une
dépendance qui n'est jamais exécutée.

### Lire un avis de sécurité

Un avis se lit pour quatre informations : l'identifiant, la gravité, les
versions affectées, et le mécanisme. Exemple, sur le cas réel de PHP (Hypertext Preprocessor) en octobre
2026 — l'advisory 2026-018 du CERT (Computer Emergency Response Team)
européen :

| Information | Ce qu'elle dit |
| --- | --- |
| **Identifiant** | un numéro d'avis, et les CVE (Common Vulnerabilities and Exposures) associées |
| **Gravité** | un score CVSS (Common Vulnerability Scoring System), ici 9.2 sur 10 |
| **Versions** | ce qui est affecté, ce qui est corrigé |
| **Mécanisme** | deux exécutions de code à distance non authentifiées |

Le calendrier de cet avis est instructif : annonce le 20 octobre, correctif le
21, preuve de concept en circulation dans la foulée, troisième faille annoncée
le 23. Le temps de correction se compte en heures ; le temps d'exploitation, en
minutes. C'est pour cela que « lire l'avis » n'est pas une lecture de fin de
journée.

> 🧪 **Atelier rapide (10 min)**
>
> Dans le lab du cours, lancez un audit de dépendances sur le dossier `lab/` —
> `pip-audit` pour Python, ou `trivy fs lab/` pour un regard plus large. Notez
> les dépendances signalées, leur version installée et la version corrigée.
> Comparez avec le contenu de `lab/cve/requirements.txt`, qui fige
> volontairement une version obsolète.

### Situer l'exposition

La présence d'une dépendance vulnérable n'est pas l'exposition. Trois questions
tranchent :

- **La fonctionnalité concernée est-elle appelée ?** Une bibliothèque entière
  peut être installée pour une seule fonction, saine.
- **Les entrées de la faille sont-elles atteignables ?** Une faille déclenchée
  par un champ administratif n'a pas le même poids que celle déclenchée par
  n'importe quelle requête.
- **Quel est l'impact métier ?** Les données concernées, l'exposition du
  service, la possibilité de reprendre la main.

> 💡 **À retenir** — L'avis de sécurité décrit une faille de bibliothèque ;
  l'avis d'exposition décrit **votre** situation. Les deux se rédigent
  séparément, et c'est le second qui décide de l'urgence.

### Corriger et vérifier

Le correctif le plus sûr est la mise à jour vers la version corrigée. Quand elle
n'est pas possible — dépendance majeure, compatibilité cassée — on
**rétro-patche** : on applique le correctif de sécurité sur la version en place,
sans prendre le reste des changements. C'est plus lourd à maintenir, donc
temporaire, et daté.

La vérification a deux volets : les tests existants passent toujours, et le cas
décrit dans l'avis ne passe plus. L'un sans l'autre ne prouve rien.

---

## II. En-têtes de sécurité

Le code écrit n'est pas le seul à décider de la sécurité d'une page : les
**en-têtes de réponse** disent au navigateur ce qu'il a le droit de faire. Ils
se posent une fois, au niveau du service, et couvrent toutes les routes.

```python
@app.middleware("http")
async def en_tetes_securite(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=63072000"
    return response
```

| En-tête | Ce qu'il empêche |
| --- | --- |
| **Content-Security-Policy** | le chargement de ressources étrangères non voulues |
| **Strict-Transport-Security** | le retour en clair de la connexion |
| **X-Content-Type-Options** | l'interprétation d'un fichier selon un type qu'il n'a pas |
| **X-Frame-Options** | l'intégration de la page dans une page étrangère |

Le premier a été vu au chapitre précédent ; les trois autres suivent la même
logique : annoncer au navigateur une règle, plutôt que de compter sur le bon
comportement de chaque page.

> ⚠️ **Attention** — Un en-tête posé côté serveur se contourne si la page peut
> être servie ailleurs. La politique se vérifie depuis le client, sur la
> réponse réelle — pas depuis le fichier de configuration.

---

## III. Configuration durcie

La configuration est du code : elle s'écrit, se relit, se versionne. Trois
réflexes couvrent l'essentiel.

**Le mode debug reste en développement.** Un serveur en mode debug renvoie des
traces, des variables, parfois une console exécutable. C'est l'outil de travail
du développeur devenu, en production, une porte d'entrée.

**Les secrets vivent hors du code.** Un mot de passe écrit dans le dépôt est
copié dans chaque clone, chaque sauvegarde, chaque historique. Il se lit depuis
l'environnement d'exécution ou depuis un gestionnaire de secrets — et le code
ne contient que le nom de la variable.

```python
# le code nomme, l'environnement fournit
DB_PASSWORD = os.environ["DB_PASSWORD"]
```

**Les valeurs par défaut sont des valeurs.** Un secret de secours écrit dans le
code pour « faire tourner en local » finit par tourner en production. Une
configuration qui refuse de démarrer quand elle est incomplète est plus sûre
qu'une configuration qui devine.

| Ce qu'on durcit | Le geste |
| --- | --- |
| **Mode debug** | désactivé en production, vérifié au démarrage |
| **Secrets** | lus depuis l'environnement, jamais dans le dépôt |
| **Valeurs par défaut** | aucune valeur de secours en production |
| **Services inutiles** | routes de débogage supprimées, pas seulement masquées |

---

## IV. Aller plus loin

*Ces approfondissements sont facultatifs : ils ne sont jamais exigés pour
terminer la journée.*

- **Le SBOM** (Software Bill of Materials) — la liste de ce que contient un
  logiciel, dans un format standard. Quand une vulnérabilité est annoncée, le
  SBOM répond en quelques secondes à la question « sommes-nous concernés ? » —
  au lieu d'une recherche manuelle dans les fichiers de dépendances.
- **La veille automatisée** — les plateformes d'hébergement ouvrent des demandes
  de mise à jour dès qu'un avis concerne le projet. C'est utile, à condition de
  lire l'avis avant de fusionner : une mise à jour automatique qui casse le
  service n'est pas une sécurité.
- **Les politiques de version** — figer les versions interdites, imposer une
  plage de versions corrigées, refuser les dépendances abandonnées : autant de
  règles qui se vérifient à chaque build, plutôt qu'à chaque incident.

---

## Points clés

- La réponse à une vulnérabilité suit quatre temps : **lire, situer, corriger,
  vérifier** — dans cet ordre.
- La présence d'une dépendance n'est pas l'exposition : c'est **l'appel réel**
  du code concerné qui décide de l'urgence.
- Les en-têtes de sécurité se posent **côté serveur**, une fois, et se
  vérifient depuis le client.
- Une configuration durcie : **debug off**, secrets hors du code, aucune valeur
  de secours en production.

---

[← Chapitre précédent](04-erreurs-et-logging.md) · [Sommaire](Readme.md) · [Chapitre suivant →](06-revue-de-code-securite.md)
