# Le dossier `assets`

Ce dossier rassemble ce que le cours montre sans l'écrire : logos, captures
d'écran, schémas exportés, illustrations. Le Readme et les chapitres y puisent ;
GitHub et le support PDF les affichent.

## Ce qu'il contient

| Fichier | Fond | Usage |
|---|---|---|
| `Logo-diginamic-color.svg` | clair | en-tête du Readme et du support PDF |
| `Logo-diginamic-color-blk.png` | sombre | en-tête du Readme quand GitHub est en thème sombre |
| `course-patch-exploit.svg` | clair | chapitre 05 — la course entre le correctif et l'exploit |

Les deux logos sont des copies du dépôt
[PublicAssets](https://github.com/DiginamicInternal/PublicAssets). Le texte de
la version `-blk`, gris très clair, disparaît sur fond blanc : c'est pourquoi le
Readme les déclare toutes les deux dans une balise `<picture>`. GitHub choisit
selon le thème du lecteur ; pour le PDF, imprimé sur fond blanc, le workflow ne
garde que la version couleur.

> Merci de ne pas modifier les logos 😉

Les schémas en SVG de ce dossier, eux, sont des copies exactes de ceux du cours
frère [Les vulnérabilités et les techniques d'attaque](https://github.com/DiginamicAcademy/cours-securite-vulnerabilites-attaques) :
même mécanique illustrée, même charte, même tracé. Ce sont bien des copies — si
l'original est corrigé là-bas, il faut rejouer le correctif ici.

## Y ranger ses images

Une image se désigne par son chemin relatif à la racine du dépôt :

```markdown
![Architecture de la réplication](assets/replication.png)
```

Tous les fichiers du cours vivent à la racine : le même chemin vaut dans le
Readme et dans un chapitre. Des sous-dossiers sont possibles
(`assets/chapitre-02/…`) pour ranger un cours chargé.

Quelques règles évitent les mauvaises surprises :

- **pas d'espace ni d'accent** dans les noms : un espace oblige à l'encoder
  (`%20`) dans le lien ;
- **la casse compte** : le workflow tourne sous Linux, où `Schema.png` et
  `schema.png` sont deux fichiers différents. Windows et macOS tolèrent l'écart,
  la construction du PDF non ;
- le **SVG** (Scalable Vector Graphics) pour les schémas, le **PNG** (Portable Network Graphics) pour les captures d'écran.

## Ce qu'en fait le workflow

- **Support de cours** : chaque image locale citée est recopiée à côté du
  document avant le rendu. Une image introuvable fait échouer la construction,
  et le journal donne le chemin en cause. Une image citée dans un bloc de code
  ou entre accents graves est un exemple : elle n'est pas recherchée.

Ce fichier-ci n'apparaît pas dans le support : seuls les `.md` de la racine y
sont repris.
