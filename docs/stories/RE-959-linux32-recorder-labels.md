# RE-959 — labels bornés du recorder Linux32

## Intention et progression
- [x] Choisir un scope ordinaire indépendant : validation des noms de journaux Python.
- [x] Reproduire le défaut avec fichiers temporaires et vrais enfants Python uniquement.
- [x] Corriger avant acquisition de ressource, puis vérifier les mêmes cas et la régression.
- [x] Écrire story, dashboard et tests de liens publics.
- [x] Cleanup : zéro suppression, aucune redondance démontrée ; FAILs et uniques conservés.

## Inputs, cause et étapes
Entrée : `record(out, label, argv, cwd)` dans [linux32.py](../../scripts/porting/linux32.py), source courante après RE958. Les appelants CLI utilisent déjà des labels constants valides ; aucun défaut de parcours CLI utilisateur n’est revendiqué. L’API concaténait sans validation le label avec les extensions JSON/log : un label relatif ou absolu pouvait donc sélectionner une autre destination. Tous les exemples restent sous un répertoire temporaire propre au test, sans fichier tiers ni données de jeu.

Le label doit maintenant correspondre à `[A-Za-z0-9][A-Za-z0-9_.-]{0,127}` : 1 à 128 caractères ASCII, début alphanumérique, puis lettres/chiffres/point/tiret/underscore. Les chemins, espaces, contrôles, Unicode, noms vides ou points seuls sont refusés par ValueError avant toute création de journal ou enfant. Ce contrat volontairement étroit ne change aucun label des appelants existants. Ce n’est pas une protection contre un tiers concurrent modifiant le répertoire de sortie.

## Preuves et acceptation finie
Racine privée ignorée : `build/reverse/autonomy-20261016-night/unit03/`. `red-labels.stdout` : **12 FAIL**, 4 PASS avant correction ; `green-labels.stdout` : mêmes **16 PASS**, exit0 après correction. Cas valides : label usuel, tiret, ponctuation autorisée et frontière128. Cas invalides : vide/points, chemin relatif/absolu, séparateurs, espace, contrôle, Unicode, préfixe tiret, frontière129. Chaque refus exige absence d’enfant et inventaire temporaire inchangé.

`regression.stdout` : **477 PASS**, exit0, tests/porting avant ajout des deux tests documentaires. Cette suite contient des fixtures actual-TU ordinaires préexistantes ; ce n’est ni build complet du jeu ni lancement graphique. RED documentaire distinct : deux fichiers absents, pas une preuve comportementale. Les commandes et exits exacts sont au ledger prospectif, hors bootstrap déclaré.

Recette publique : `PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -B -m pytest -q -p no:cacheprovider tests/porting/test_linux32_labels.py tests/porting/test_re959_publication.py`. Acceptation publication/revue reste une gate exacte distincte ; les nombres auteur ne sont pas un rejeu indépendant.

## Limites et prochaine frontière indépendante
integration=false ; production_patch=false pour le jeu. Outil seulement modifié ; pas boot, menu ou gameplay nouveau. BLOCKED-008/009/RE944 et dépendants restent exclus et non résolus ; aucune relance allocateur/MIPS/Unicorn. Réservation JSON/log non atomique, erreurs d’écriture finale, liens symboliques/tiers concurrents et limites d’interruption RE957 restent hors garantie. Prochaine unité éventuelle : caractériser la gestion d’échec d’écriture finale sans inventer un correctif préalable ; autorisation et budget à revérifier avant tout travail.

[Dashboard](../reverse/tomb5-progress-dashboard-re959-v1.html) · [Recette Linux32](../porting/linux32.md)
