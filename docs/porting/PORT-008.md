## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Repérage de la cour de la fontaine (téléportation de test, pas un parcours joué) : room 59 autour de X54000 Z41000 Y256, Doberman et grille verrouillée visibles (play-tp59-20261029/01.png). Room 69 = toit/point de vue, pas la fontaine. La route jouée jusqu'à cette cour reste à établir ; Opera Backstage (room 11) est atteint en marche réelle. Build-gameplay11 SHA256 4bd9aa4515872d351a602a3be8ec071becbec2a21b5f95a63e22e61a0d9f812b; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Ennemis niveau 1 initialisés après InitialiseItem : DOG hp10, LARSON hp100, MAFIA/MAFIA2 hp40, intelligent=1, status non invisible. Preuve GDB : chien réel hp10 touché par PistolHandler, hp passe à 4. Limite : pas d'IA déplacement/attaque, CreatureCollision stub, ennemis statiques. Build-gameplay11 SHA256 4bd9aa4515872d351a602a3be8ec071becbec2a21b5f95a63e22e61a0d9f812b; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Combat minimal : PistolHandler implémenté (hitscan cône ±60°, HitTarget, munitions, SFX_LARA_FIRE, flash). Preuve GDB : chien forcé à hp=100/intelligent=1, 6 tirs font passer hp à 64. Limite : les ennemis de niveau ne sont pas initialisés (hp=-16384, pas d'IA/contrôle), donc chiens/Larson restent inertes ; BaddyObjects et contrôles ennemis à compléter. Build-gameplay10 SHA256 51efd1a024a13ff39c0e942076d2a754dd5da8a689f01190ad344ce266b33152; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Parcours réel sans téléportation dans Rome : room 0 (départ) → room 2 (cour) → room 11 (zone Opera Backstage, caisse/passerelle) → room 3 → room 44, avec les flèches Up/Left/Right. Preuves play-room1-20261029/ et play-train-20261029/. Les lettres AZERTY q/d produisent des rotations ambiguës en test ; utiliser les flèches. Interactions pickups/serrures/switchs/portes déjà validées séparément. Restent : maillage de porte statique, ennemis/combat stubs, fin de niveau/campagne non atteinte. Build-gameplay9 SHA256 3d8e1ffd660c271425e5717b2e63367a196588549709b86928e5736c11043c62; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

CombatCamera (corps PSX non reconstruit) utilise désormais ChaseCamera en repli : sortir les armes ne noircit plus la vue. Preuve NTSC build-gameplay9 : moyennes 0,1012 (idle) / 0,1012 (armes) / 0,1018 (rengainé), aucun SIGSEGV (gameplay-draw-fix-20261029/). La visée automatique du combat reste absente. Build-gameplay9 SHA256 3d8e1ffd660c271425e5717b2e63367a196588549709b86928e5736c11043c62; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Portes : PortInitialiseDoor() alloue DOOR_DATA, mémorise le FLOOR_INFO d'origine et ouvre la cellule de plancher. Vérifié GDB sur l'item 24 : data non NULL, Opened=1, floor box=135 (passable). Le maillage de porte reste statique. Déplacement réel validé avec les scancodes AZERTY : z=avant fait passer Lara de room 0 X46592 Z31232 à room 2 X46592 Z38830 en 8 s (play-move2-20261029/). Attention : w est le scancode draw en AZERTY, pas forward. Build-gameplay8 SHA256 559827c17f132301cabb942179dd56bfe61b15d6cbd23a926aeaab29b5aa299e; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Première couche gameplay : dispatch des collisions d'objets (PortCollideItems), TestBoundsCollide/TestLaraPosition/MoveLaraPosition/ItemPushLara, PickUpCollision, KeyHoleCollision, PuzzleHoleCollision, SwitchCollision/SwitchControl, DoorControl, DoubleDoorCollision, PushPullKickDoorCollision, et PortSetupGameplayObjects(). Preuves GDB niveau 1 : pickup objet 339 ajouté une seule fois (ammo 0→36, item invisible), serrure avec clé (TestLaraPosition=1 + IN_ACTION), switch (TestLaraPosition=1), smoke Nouvelle partie sans SIGSEGV. Limites : pas d'InitialiseDoor (portes non ouvrables géométriquement), ennemis/combat stubs, objets spéciaux non couverts, campagne non jouée. Build-gameplay7 SHA256 294177084e2e14951db1604f5be410f99b44713f78f8d5319d2503b9e0b88898. tests/porting+emulator 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Chaîne PAL revérifiée sur build-pause (pause réordonnée + correctif SqrtTable) : injections GDB toutes les 600 frames, niveaux 1→14 avec salles/positions conformes, puis cutseq name: 0 et retour titre, aucun SIGSEGV. Preuve build/porting/pal-chain-pause-20261029/. Déclenchements synthétiques, pas une complétion jouée. Build-pause SHA256 870166e1030a5399d88271eec135e66e59bbedff03ad485ca9f1827acaba1ae8. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Chaîne de régression finale sur build-pause (pause réordonnée Resume/Game Settings/Quit + correctif SqrtTable) : injections GDB toutes les 600 frames, niveaux 1→14 avec salles/positions conformes (2/50, 3/20, 4/99, 5/20, 6/123, 7/2, 8/70, 9/5, 10/20, 11/3, 12/129, 13/3, 14/8), puis cutseq name: 0 et retour titre, aucun SIGSEGV. Preuve build/porting/final-chain-pause-20261029/. Déclenchements synthétiques, pas une complétion jouée. Build-pause SHA256 870166e1030a5399d88271eec135e66e59bbedff03ad485ca9f1827acaba1ae8. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Défaut reproductible lié aux stubs : sortir les armes (Y manette) rend la vue 3D entièrement noire, HUD visible ; rengainer (Y) restaure la scène. Cause : CombatCamera (GAME/CAMERA.C:1638) a son corps sous #if 0 || PC_VERSION et tombe sur UNIMPLEMENTED. NTSC : moyennes 0,1018 → 0 → 0,1025, 63 appels CombatCamera. Preuve build/porting/vpad-draw-20261029/. Le combat aux armes est inutilisable, en plus des pickups/interactions déjà bloqués. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Soak PAL de 10 minutes avec manette Xbox 360 virtuelle (boutons et stick gauche aléatoires après New Game) : 32 échantillons VmRSS, 74928 Ko constant sur 571 s, exit 0, aucune erreur fatale, scène de rue rendue à 360 s. Preuve build/porting/pal-gp-soak-20261029/. Matériel physique non testé. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

PAL (SLES_033.31) : chaîne complète 1→14→titre validée par injections GDB de gfLevelComplete=gfCurrentLevel+1 toutes les 600 frames. Salles/positions conformes au tableau NTSC (1/0, 2/50, 3/20, 4/99, 5/20, 6/123, 7/2, 8/70, 9/5, 10/20, 11/3, 12/129, 13/3, 14/8), puis cutseq name: 0 et retour titre, aucun SIGSEGV. Preuve build/porting/pal-chain-20261029/. Déclenchements synthétiques, pas une complétion jouée. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

PAL (SLES_033.31) : transition 1→2 validée par injection GDB de gfLevelComplete=2 après 600 frames de niveau 1. Cutseq name: 2 (1657 occurrences), scène TRAJAN_MARKETS rendue, aucun SIGSEGV. Preuve build/porting/pal-transition-20261029/. Déclenchement synthétique, pas une complétion jouée. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Cause racine de la campagne non jouable identifiée sous GDB au niveau 1 : InitialiseObjects met tous les handlers d'objets à NULL, ObjectObjects n'initialise que LARA et un fragment de SAS, TrapObjects est vide. Les objets pickup/keyhole/puzzle/switch/porte du niveau 1 ont collision=NULL (Lara control=NULL), et PickUpCollision, KeyHoleCollision, PuzzleHoleCollision, TestLaraPosition, MoveLaraPosition, TestBoundsCollide, ItemPushLara, DoorControl, SwitchCollision, CreatureCollision sont des stubs. Aucun pickup ni interaction n'est donc possible, quelle que soit la route ; ce n'est pas une régression Linux32 mais un manque hérité de la décompilation (travail RE sous gates BLOCKED-004). Preuve build/porting/objcoll-20261029/. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b; tests/porting 497 PASS, tests/emulator 3677 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Chaîne finale sur les sources build-ci avec hook QA TOMB5_CHAIN_TEST (non intégré) : 1→2→…→14 puis Handle cutseq name: 0, sans SIGSEGV. Preuve final-chain-cj-20261029/chain.log. Déclenchements synthétiques, aucune complétion jouée/crédits.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006, PORT-007, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Build-cd final : v4 (item_flags/timer/trigger_flags, v3/v2 compatibles), écriture atomique, audio SDL/SPU, memmove gameflow validé ASan. Vérifié : Rome v4/v2, niveau 2 v3, PCM audio pendant la marche, ASan nouvelle partie + F5 + F6 sans erreur, chaîne 1→14→titre sans SIGSEGV (hook QA). Build-cd SHA256 b5deda7ed9e0b655d4e335116b76a278f058841b3065d590565da574b3e8a162. tests/porting 497 PASS, tests/emulator 3677 PASS. Restent non validés : campagne réelle/crédits, écoute humaine/CD-XA, manette.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006, PORT-007, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

État final combiné build-bx : artefact de rendu corrigé par replacement du bloc scratch; reprise v3 (bloc 8192, atomique) validée Rome 586 octets et niveau 2 594 octets avec scènes identiques; backend audio SDL/SPU (VAG, pitch/pan/volume, boucles SF_LOOP, SoundFXVolume) avec PCM non nul pendant la marche; chaîne 1→14 puis titre sans SIGSEGV (hook QA). Build-bx SHA256 57322612388cf44b2172979e5ee68e5289d12c28e7c9de965a925a36ff0827c9. tests/porting 497 PASS, tests/emulator 3677 PASS. Restent non validés : écoute humaine/CD-XA, campagne réelle/crédits, manette physique.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Chaîne finale revalidée après les correctifs : build de test avec hook QA TOMB5_CHAIN_TEST (même logique de transition, non intégré) enchaîne 1→2→…→14 puis Handle cutseq name: 0, sans SIGSEGV; preuve build/porting/final-chain-bs2-20261029/chain.log. Déclenchements toujours synthétiques, aucune fin de niveau jouée, crédits/FMV non caractérisés.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Artefact de reprise attribué et corrigé : la grande surface brune n'était pas liée à F6/AUTOLOAD/RestoreLevelData, elle apparaissait dès New Game à Rome. Bissection build-c (propre) vs build-s (artefact) puis cff51ec2 : les tableaux SkinVertNums/ScratchVertNums agrandis à 8192 octets cassaient l'hypothèse de contiguïté du chargeur, qui écrivait les 480 octets scratch à SkinVertNums+480 et laissait ScratchVertNums à zéro. GAME/SETUP.C recopie désormais le bloc scratch vers ScratchVertNums après la lecture contiguë (DEL_CDFS_Read avance par secteurs). Vérifié : New Game Rome propre, F6 RESTORE3 propre, niveau 6 chargé/rendu sans SIGSEGV, tests/porting 497 PASS, tests/emulator 3677 PASS. Build-au SHA256 dee0479c6000441af05b4d9724bb7b57605859eca2df0b74c0dbe920c32a467e. Preuves : master-fix-smoke-20261029, fix-objectdata-final-load-20261029, fix-objectdata-level6c-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T23:00:00+01:00. Linux32 provisoire.

Boucle mécanique complète validée : deux runs indépendants sur build-x atteignent les niveaux 1→2→…→14 puis déclenchent la fin et reviennent au titre (Handle cutseq name: 0), sans SIGSEGV. Le crash GetDoor(0xfe4cb8d4) du niveau 14 n'est plus reproduit après le garde des numéros de salle (< number_rooms). La garde GAMEWAD reste validée séparément par le saut direct 1→15. Déclenchements synthétiques : aucune fin de niveau jouée, aucun FMV/crédit de fin ni sauvegarde de progression campagne validés. Build-x SHA256 78b5ac0233b7e7fd9325a2c34e00a173b854ce93e17afa859a4bcf11b2468edd. Preuves privées : port008-fullchain15-20261028, port008-fullchain-title-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T19:00:00+01:00. Linux32 provisoire.

Garde défensive ajoutée aux boucles de suivi de porte LARASWIM/CONTROL : data/next_room de GetDoor doit être < number_rooms avant r=&room[data] ou retour de salle. Vise le floor invalide 0xfe4cb8d4 observé au niveau 14. Build-x SHA256 78b5ac0233b7e7fd9325a2c34e00a173b854ce93e17afa859a4bcf11b2468edd. Limite : la chaîne 1→14 n'a pas pu être rejouée après correctif dans cette fenêtre (entrées Cross de démarrage titre non acceptées sur les derniers runs) ; suites porting/emulator PASS, mais pas de preuve de chaîne après garde. À revalider.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T19:00:00+01:00. Linux32 provisoire.

Chaîne complète 1→14 vérifiée à nouveau (14 captures) puis déclenchement 15 : SIGSEGV dans GetDoor(floor=0xfe4cb8d4) à GETSTUFF.C:32, AVANT DoLevel(15). Trace DoLevel : Name=1 puis Name=14, jamais Name=15 ; la garde GAMEWAD n'est donc pas atteinte dans ce chemin. Le saut direct 1→15 atteint bien la garde et retourne au titre. Blocage suivant : pointeur de floor invalide pendant le niveau 14 (pas la lecture du niveau 15). Fin de campagne réelle non caractérisée. Build-v SHA256 fdeecaf52d5e0d7422d8fa3390236c782e61032690d61e19083c2e366eba783c. Preuves privées : port008-fullchain6-20261028, port008-dolevel14-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T19:00:00+01:00. Linux32 provisoire.

GAMEWAD analysé directement : entrées 3..16 = 14 fichiers de niveau, entrées 17+ vides; Gameflow->nLevels=18. Le déclenchement synthétique +1 après le niveau 14 demandait l'entrée 17 inexistante et produisait un en-tête invalide (DEL_CDFS_Read size=-16388 -> fseek/SIGSEGV). DoLevel vérifie désormais l'entrée avant S_LoadLevelFile : hors bornes ou taille nulle -> log, gfStatus=1/gfCurrentLevel=0, retour titre. Recette : 1→15 synthétique retourne au titre sans SIGSEGV (port008-endguard-20261028); 1→2 charge toujours TRAJAN_MARKETS (port008-valid2-20261028). Protège aussi toute donnée de niveau manquante. Fin de campagne réelle (crédits/FMV après RED_ALERT) non caractérisée. Build-v SHA256 fdeecaf52d5e0d7422d8fa3390236c782e61032690d61e19083c2e366eba783c.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Gardes de vertices ajoutés aux variantes LARA1-LARA4 (même borne tsv_buffer que LARA5). Le crash GetDoor du niveau 15 n'est plus atteint en saut direct 1→15; il est remplacé par un SIGSEGV dans la lecture CD : DEL_CDFS_Read size=-16388 -> CdControlB -> fseek, pendant S_LoadLevelFile(Name=15). GetDoor était probablement un symptôme de la corruption de vertices, pas la cause racine. Niveau 15 toujours bloqué sur un problème d'offset/lecture CD. Chaîne 1→14 précédemment vérifiée. Build-u SHA256 0866d3242a02d68e253c089c6933900585498ab607517dd83b2951df395b8fce. Preuve privée : port008-level15guard-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Chaîne contrôlée 1→14 stable (14 captures), puis SIGSEGV au passage niveau 15 (RED_ALERT) : GetDoor(floor=0xfe4cb8d4) à GETSTUFF.C:32, pointeur de floor hors tas. Ce n'est pas le crash niveau 6 corrigé; blocage suivant non instruit. Déclenchements synthétiques, aucune complétion jouée/FMV/crédit/campagne complète. Preuve privée : port008-fullchain4-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Crash niveau 6 corrigé. AddressSanitizer 32 bits a localisé deux dépassements : ClearOTagR écrivait hors de GadwOrderingTables (seconde ordering table décalée de nOTSize au lieu de nOTSize*POLYGON_BUFFER_MULT, et nOTSize=sizeof/8 au lieu de sizeof/(8*MULT) en mode 32 bits), et sub_C1CL5 (LARA5.C) écrivait sans borne dans tsv_buffer car la liste de vertices n'avait pas de sentinelle, jusqu'à écraser psxtextinfo (0xc100ff). Corrections : layout OT 32 bits, tsv_buffer 1024 TSV, SkinVertNums/ScratchVertNums 8192, borne explicite dans sub_C1CL5. Après correctif, niveau 6 chargé/rendu, saut direct 1→6 sans crash, chaîne contrôlée 1→2→…→14 sans SIGSEGV (salles/positions relevées, 14 captures). Le garde-fou peut tronquer un mesh malformé : protection mémoire, pas correction du parseur. Déclenchements synthétiques, aucune complétion jouée/FMV/crédit/campagne complète. Build-t SHA256 1272d6c7ab932b85fcd3005de9dafb40f9e0714954fa80fc91182ae1d477e2fc. Preuves privées : port008-fullchain2/3-20261028, port008-level6guard2-20261028, port008-asan4-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Chaîne complète tentée : 1→2→3→4→5 OK, puis SIGSEGV au niveau 6. Backtrace : sub_658L5 (LARA5.C:834, t4=((int*)t5)[2]) appelé par sub_2CL5/DrawLaraL5. État : psxtextinfo=0xc100ff (hors malloc_buffer 0x567...), a22=0xc100ff. Le saut direct 1→6 (gfLevelComplete=6) reproduit le crash, donc ce n'est pas l'état des transitions précédentes mais l'initialisation des textures du niveau 6. Aucun patch spéculatif. Blocage suivant à instruire : textureInfoLength/relocalisation ou format mesh/texture TR5 du niveau 6. Preuves privées : port008-fullchain-20261028, port008-level6diag2-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Chaîne multi-niveaux après correctif de transition : gfLevelComplete=gfCurrentLevel+1 injecté tous les 600 frames de jeu réel -> 1→2→3→4→5 sans retour au titre. Salles/positions observées : niveau 1 room 0 Z31232 ; 2 room 50 Z42496 ; 3 room 20 Z52736 ; 4 room 99 Z29664 ; 5 room 20/23 Z42496/53760. Scènes distinctes (Rome, marchés, Russie, base, sous-marin), milliers de frames stables (7500 cumulées). Déclenchements synthétiques : aucune fin de niveau jouée, aucun puzzle/porte/clé, aucun FMV/crédit/campagne complète. Preuve privée : build/porting/port008-chain-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Défaut de transition corrigé dans GAME/GAMEFLOW.C : après gfStatus==3, gfCurrentLevel était affecté à gfLevelComplete puis écrasé inconditionnellement par 0, donc toute fin de niveau renvoyait au titre. gfCurrentLevel=0 est maintenant dans le else (démo/build 2 niveaux/fin de campagne). Recette : injection GDB de gfLevelComplete=2 après 600 frames de jeu réel dans Rome -> niveau 2 chargé (room 50, Z42496, cutseq name 2), milliers de frames stables, scène TRAJAN_MARKETS rendue ; avant correctif la même injection renvoyait au titre/DEMO MODE. Régression New Game : Rome se charge toujours (cutseq name 1, exit 0). Le déclenchement est synthétique : aucune fin de niveau jouée, aucun FMV/crédit/campagne complète validé. Build-s SHA256 a34430c76aeeb8a61213fbfc30745079f75c1ca91c93ff0592a302d654200f31. Preuves privées : port008-transition2-20261028, port008-newgame-regress-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Non validé : la route Rome complète (clés, portes, puzzles, fin de niveau) n'a pas été jouée et aucun gfLevelComplete de fin de niveau n'a été déclenché par du gameplay. Seul point observé : le raccourci QA existant (maintenir look/L1 puis New Game) charge une scène industrielle distincte (niveau 4) ; une tentative walk/R1 a rendu Rome, donc le raccourci n'est pas fiable. Chargement/rendu d'un autre niveau seulement, pas de boucle de niveau, pas de transition campagne, pas de sauvegarde inter-niveaux. Preuve privée : build/porting/port008-level4-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

# PORT-008 — Boucle du premier niveau et passage au suivant

[Tracker](README.md) · [Tableau HTML](index.html#PORT-008)

Status: Blocked

Priorité : P1

Motif : Recette intégrée bloquée tant que PORT-005, PORT-006, PORT-007 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-005, PORT-006, PORT-007

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Jouer un parcours représentatif puis atteindre le niveau suivant, avec mort/reprise et retour au titre utilisables.

## Faits existants — base eac6d930

GAMEFLOW.C traite la fin de niveau ; dans la branche gfStatus==3, une affectation vers le niveau suivant est suivie d’une remise à zéro. C’est une observation source, pas une preuve de la cause d’un échec runtime ni un correctif validé.

## Portée

Un parcours réel avec interaction/pickup, obstacle et sortie normale ; mort/reprise, état persistant et entrée au niveau suivant.

## Exclusions

Campagne entière, tous combats/boss/secrets/cinématiques et niveau de fidélité finale exclus ; décomposer un mécanisme indispensable découvert au lieu de le masquer.

## Tâches — implémentation non commencée

- [ ] Choisir le parcours et les mécanismes réellement requis à partir du niveau chargé.
- [ ] Vérifier triggers et transitions avec témoins fin normale/retour volontaire/mort.
- [ ] Intégrer les dépendances indispensables et rejouer la route avec sauvegarde/reprise.

## Critères d’acceptation futurs

- [ ] Une interaction et un pickup changent leur état attendu sur une route jouée par les entrées normales.
- [ ] La sortie normale charge le bon niveau suivant et son point de départ, sans retour inattendu au titre.
- [ ] Mort/reprise, reprise sauvegardée et retour volontaire au titre restent utilisables ; la route est répétée deux fois.

## Validation et capture attendues

Vidéo privée du parcours avec journal transitions et identités des niveaux ; tests des régressions touchées et scénario de reprise.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Mécanismes du niveau non inventoriés, combat/IA/eau/cinématiques potentiellement bloquants ; ce ticket devra être découpé si nécessaire, sans déclarer le port complet.

## Estimation indicative

10–30 jours-personne exploratoires après dépendances ; forte possibilité de nouveaux tickets. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `GAME/CONTROL.C:3011` — TO_FINISH.
- `GAME/GAMEFLOW.C:231` — Traitement gfStatus.
- `GAME/GAMEFLOW.C:1389` — Sortie DoLevel.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
