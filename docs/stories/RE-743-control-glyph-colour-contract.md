# RE-743 — Couleur locale des glyphes de contrôle PSXPC_N

## Statut et progression

**Unité bornée reconstruite et vérifiée, revue indépendante favorable, intégration validée. Le contrat complet des glyphes reste ouvert.**

- [x] Continuité RE-742 et HEAD `617a46d6` vérifiés ; début le 8 septembre 2026 à 21 h 13 Paris, limite de cette unité à 23 h 15.
- [x] Nouvelle inspection Ghidra en lecture seule, mémoire authentifiée, sortie complète et code retour conservés.
- [x] Contrat local de couleur prouvé indépendamment des accents et des substitutions sentinelles.
- [x] Tests publics sur la vraie unité et tables synthétiques écrits puis observés RED avant toute correction.
- [x] Correction limitée à la sélection de couleur des glyphes de contrôle dans `SPEC_PSXPC_N/TEXT_S.C`.
- [x] GREEN ciblé, régression émulateur, différentiel privé authentique, ASan/UBSan de la vraie unité.
- [x] Revue indépendante favorable ; parent : 1 150 tests émulateur réussis, recompilation/rejeu différentiel normal et ASan/UBSan (3 056 cas chacun) sans écart. Intégration validée.
- [ ] Contrat complet des octets élevés, accents, sentinelles et domaine d’entrée.

## Preuve et contrat retenu

Cible inchangée : boot US PSX attribué dans RE-742. Le chargement bas vérifié par l’en-tête et l’empreinte du payload concorde avec la mémoire du projet Ghidra. Aucun projet concurrent ni verrou n’était présent avant accès. La nouvelle inspection des fonctions de texte conserve les instructions et la décompilation **uniquement dans le dossier ignoré** `build/reverse/autonomy-20260908/re743-colour/`.

La lecture des instructions, y compris les delay slots et retours ajustés du helper, établit :

| Entrée de rendu | Banque de couleur utilisée | État courant après rendu |
|---|---|---|
| Glyphe ordinaire | Courante | Inchangé |
| Contrôle 20 à 23 | Zéro | Inchangé |
| Contrôle 24 à 27 | Courante | Inchangé |
| Contrôle 28 à 31 | Zéro | Inchangé |

Le test cible porte sur une comparaison **non signée de la différence**, pas une comparaison signée après stockage dans `char`. La source traitait donc à tort les contrôles 20 à 23 comme héritant de la couleur courante sur le mode signé. Le correctif exprime directement la plage 24 à 27, garde l’octet original pour le choix du glyphe et réutilise le pointeur sélectionné. Il ne modifie ni la couleur persistante, ni les métriques, ni les API, ni les autres backends.

Les sélecteurs 1 à 8, les espaces, tabulations, sauts de ligne et glyphes suivants vérifient la persistance de la couleur. Les deux raccordements entre table de mesure authentique et stockage de rendu existant sont vérifiés par égalité exacte dans le harness privé ; aucune donnée de rendu authentique n’y est réécrite. La publication ne remplace aucune table et n’introduit **aucune politique de rejet**.

## TDD public : vraie unité, aucun asset

`tests/emulator/test_text_colour.py` compile `TEXT_S.C` et son vrai `DrawChar` avec les en-têtes ordinaires, en mode `signed char`. Les métriques et teintes sont entièrement inventées, distinctes par glyphe et par niveau de nuance ; le harness ne recopie aucune fonction de production.

- **RED : 344 échecs comportementaux, 681 réussites**, avant le correctif. Les différences attendues concernent les couleurs des contrôles 20 à 23 et leur combinaison avec les sélecteurs.
- Matrice publique : 12 contrôles × 10 couleurs initiales × 8 combinaisons de drapeaux ; 64 séquences de sélecteurs et transitions de lignes ; un contrôle de sortie anticipée par clignotement.
- Vérifications : identité UV synthétique, position, largeur, RGB des quatre sommets, maintien de la couleur des glyphes suivants et restauration de l’échelle.
- **GREEN : 1 061 tests texte réussis**, dont les nouveaux cas et les régressions mesure/layout.
- **Régression : 1 150 tests émulateur réussis**, sans diagnostic.

## Différentiel privé et instrumentation réelle

Le runner reprend RE-742 avec une nouvelle garde explicite pour le HEAD courant et la limite autorisée de cette unité. Les fichiers et gardes du prédécesseur restent inchangés. Le suffixe authentique du loader est rejoué ; ses sorties concordent avec l’archive antérieure. Les 250 vues terminées sont consommées sans réparation. La dernière vue non terminée reste exclue du corpus, et n’est pas réparée par la production.

| Vérification | Cas | Résultat |
|---|---:|---|
| Modèle borné / instructions cibles, héritage et extension couleur | 3 872 | Aucun écart ; 7 744 exécutions cibles |
| Événements et primitives modèle / cible | 34 384 chacun | Aucun écart dans les champs comparés |
| Vraie unité corrigée / cible, corpus authentique | 2 000 | Mesures et primitives identiques |
| Vraie unité corrigée / cible, contrôles et transitions synthétiques | 1 056 | Mesures et primitives identiques |
| Même vraie unité + harness sous ASan/UBSan | 3 056 | Comparaisons exactes, aucun diagnostic |

Chaque mode hôte compare **30 160 primitives** : nombre, XY, UV et RGB des quatre sommets, plus largeur et bornes verticales de la mesure. Ce sont des assertions d’égalité, pas des tests attendant une divergence. Les 88 écarts RGB authentiques de RE-742 sont ainsi éliminés sur son corpus signé.

Les **816 cas accentués** supplémentaires restent comparés entre le modèle de recherche et le MIPS, mais sont **exclus de l’exécution de la vraie unité**. Cette distinction empêche de présenter les 3 872 cas comme une validation complète de la production.

## Reproduction et preuves locales

Depuis la racine du dépôt :

```sh
python3 -m pytest tests/emulator/test_text_colour.py tests/emulator/test_text_layout.py tests/emulator/test_text_measurement.py -q
python3 -m pytest tests/emulator -q
```

Depuis `build/reverse/autonomy-20260908/re743-colour/`, dans cet ordre :

```sh
PYTHONDONTWRITEBYTECODE=1 ../venv/bin/python differential.py
PYTHONDONTWRITEBYTECODE=1 ../venv/bin/python verify_tu.py
```

Preuves : `ghidra-text.txt`, `headless.log`, `public-red.log`, `public-green.log`, `emulator.log`, `differential.log`, `summary.json`, `rows.json`, `verification.log`, `tu-summary.json`, `normal-build.log`, `sanitized-build.log`, `normal-tu.log`, `sanitized-tu.log`. Les commandes C++ complètes et codes retour sont archivés. Le runner privé requiert le payload authentifié, les données RE741, Unicorn et le HEAD courant ; il refuse après le 8 septembre 2026 à 23 h 15 Paris. Une relance ultérieure exige une adaptation explicitement autorisée, pas un contournement silencieux.

## Limites et handoff

La preuve porte sur les chemins CPU de texte et des buffers synthétiques : ni GPU réel, ni démarrage ou boucle de jeu complète. Le loader utilise les doubles de services fichier déjà déclarés dans RE-742. CPU et RAM sont restaurés par cas, les lectures des chaînes sont bornées ; les teintes, pile, contexte appelant et buffers sont construits.

Le contrat complet reste bloqué par les accents non reconstruits, les substitutions sélectionnant la sentinelle et l’absence de contrat général pour les entrées hors plage. Aucun changement global du signe de `char`, aucun retrait d’assertion accentuée, aucune généralisation des rejets expérimentaux. `GetStringDimensions` n’est pas nouvellement prouvé. Les fonctions complètes ne sont pas reclassées comme reconstruites.

**Prochain objectif :** établir une représentation sûre et fidèle des glyphes accentués/sentinelles et le domaine réellement consommé avant d’unifier la sélection. Cette difficulté ne bloque plus la correction locale de couleur démontrée ici. Dashboard actif mis à jour, inventaires historiques inchangés ; publication limitée aux fichiers relus ; aucun asset ni dump livré.
