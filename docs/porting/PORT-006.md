## Progression vérifiée du 2026-10-29

PORT-006 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Format v4 : les valeurs item_flags[0..3], timer et trigger_flags correspondant aux bits 0x80..0x1000 sont écrites et relues; PortSave_LevelFormat=3 conserve la lecture des anciens fichiers v3 (sans ces champs). Rome 586 octets, niveau 2 594, round-trip v4 propre; E.SAV v3 et RESTORE3.SAV v2 acceptés. Build-cc SHA256 63b12a331747deffe06a235e08cd78d08250f02174fca8992f5be50d5faba823. tests/porting 497 PASS, tests/emulator 3677 PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006, PORT-007, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

État final combiné build-bx : artefact de rendu corrigé par replacement du bloc scratch; reprise v3 (bloc 8192, atomique) validée Rome 586 octets et niveau 2 594 octets avec scènes identiques; backend audio SDL/SPU (VAG, pitch/pan/volume, boucles SF_LOOP, SoundFXVolume) avec PCM non nul pendant la marche; chaîne 1→14 puis titre sans SIGSEGV (hook QA). Build-bx SHA256 57322612388cf44b2172979e5ee68e5289d12c28e7c9de965a925a36ff0827c9. tests/porting 497 PASS, tests/emulator 3677 PASS. Restent non validés : écoute humaine/CD-XA, campagne réelle/crédits, manette physique.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Reprise v3 de l'état du niveau intégrée : PortSave écrit un bloc fixe de 8192 octets via SaveLevelData (flips, meshes statiques, caméras, items). SaveLevelData écrit désormais un mot nul pour les items inactifs, sinon la sauvegarde Rome faisait 286 octets et RestoreLevelData en lisait 586 (désynchronisation). Après correction, F5 à Rome sérialise 586 octets et le rechargement lit exactement 586 octets (caméras 259, items 586), scène propre. Les fichiers v2 de 466 octets restent lisibles mais sans état de niveau. TOMB5_AUTOLOAD=1 conservé comme hook QA. Build-bb SHA256 469d42764959dc9c9aec4984343af29976a7c0a9cd70bf263d3fe2f6de961389. Preuves : restorefull-debug2-20261029, final-bb-v3-20261029, restorefull-v2-20261029. tests/porting 497 PASS, tests/emulator 3677 PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Artefact de reprise attribué et corrigé : la grande surface brune n'était pas liée à F6/AUTOLOAD/RestoreLevelData, elle apparaissait dès New Game à Rome. Bissection build-c (propre) vs build-s (artefact) puis cff51ec2 : les tableaux SkinVertNums/ScratchVertNums agrandis à 8192 octets cassaient l'hypothèse de contiguïté du chargeur, qui écrivait les 480 octets scratch à SkinVertNums+480 et laissait ScratchVertNums à zéro. GAME/SETUP.C recopie désormais le bloc scratch vers ScratchVertNums après la lecture contiguë (DEL_CDFS_Read avance par secteurs). Vérifié : New Game Rome propre, F6 RESTORE3 propre, niveau 6 chargé/rendu sans SIGSEGV, tests/porting 497 PASS, tests/emulator 3677 PASS. Build-au SHA256 dee0479c6000441af05b4d9724bb7b57605859eca2df0b74c0dbe920c32a467e. Preuves : master-fix-smoke-20261029, fix-objectdata-final-load-20261029, fix-objectdata-level6c-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-006 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Sauvegarde rapide de port : F5 écrit TOMB5.SAV (magic T5P2, savegame_info, position/rotation/salle/animation de Lara, checksum FNV-1a) ; F6 au titre recharge et reprend. Preuve réelle : partie Rome, marche, F5 room 2 X46592 Y0 Z35826, fermeture normale exit 0, relance, F6, application de la même position et scène identique ; exits 0. Limites : RestoreLevelData non implémenté, les objets/portes/pickups du niveau repartent de l'état initial, seuls Lara et son inventaire/santé sont restaurés ; pas de carte mémoire PSX, pas de chargement en jeu, pas de slots multiples, écriture non atomique. Preuves privées : build/porting/port006-20261028 et port006b-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

# PORT-006 — Sauvegarder et reprendre après relancement

[Tracker](README.md) · [Tableau HTML](index.html#PORT-006)

Status: Blocked

Priorité : P1

Motif : Recette intégrée bloquée tant que PORT-005 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-005

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Retrouver une partie sauvegardée après fermeture complète de l’application.

## Faits existants — base eac6d930

LoadGame/SaveGame existent côté PSXPC_N ; RestoreLevelData est implémenté dans GAME/SAVEGAME.C pour la sauvegarde rapide v4 (bloc de niveau de 8192 octets, item_flags/timer/trigger_flags inclus). Les fichiers v3/v2 restent lisibles. La présence des menus ne vaut pas restauration du monde. Le stockage carte mémoire passe par EMULATOR/LIBMCRD.C.

## Portée

Un emplacement de sauvegarde local, cycle complet save/exit/relaunch/load, état de Lara et d’un objet représentatif.

## Exclusions

Compatibilité universelle avec sauvegardes originales, migration de versions, synchronisation cloud et tous slots exclus.

## Tâches — implémentation non commencée

- [ ] Définir un état avant/après et isoler le stockage de test des sauvegardes utilisateur.
- [ ] Caractériser sérialisation, restauration et taille des buffers avant correction.
- [ ] Faire le cycle avec processus neuf puis tester annulation et fichier invalide sur copies.

## Critères d’acceptation futurs

- [ ] Après relancement, niveau, position, santé, inventaire et état d’un objet correspondent aux valeurs sauvegardées.
- [ ] Un déplacement après sauvegarde n’est pas confondu avec l’état restauré.
- [ ] Annulation/fichier invalide n’écrasent pas la sauvegarde valide et produisent une réponse compréhensible.

## Validation et capture attendues

Captures privées avant/après, comparaison structurée des états et hashes des fichiers privés ; aucune sauvegarde originale en Git.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Format, checksum, validité des chemins et logique de restauration ; aucune corruption réelle prétendue sans reproduction.

## Estimation indicative

5–20 jours-personne exploratoires ; compatibilité externe à estimer séparément. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `SPEC_PSXPC_N/LOADSAVE.C:119` — LoadGame.
- `GAME/SAVEGAME.C:52` — sgRestoreGame et RestoreLevelData.
- `EMULATOR/LIBMCRD.C:78` — Stockage carte mémoire.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
