## Progression vérifiée du 2026-10-29

PORT-006, PORT-007 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Correctifs de revue : pitch SPU_Play sans division /64 (4096/32256 cohérents), registre de volume courant +6 renseigné à key-on/key-off pour que SpuGetKeyStatus ne libère plus les voix immédiatement, lecture du bloc niveau bornée à 8192 et numéros de salle validés avant ItemNewRoom/UpdateLaraRoom, SGpoint/SGcount restaurés après SaveLevelDataToBuffer. ASan nouvelle partie + F5 + rechargement v4 et niveau 2 propres. PCM audio actif 94–99 s pendant la marche. Build-cg SHA256 824ea2ea0e5f3e75e24c01680c1b897061e6c1ef98ae9471a80995be7f21fd2d; tests/porting 497 PASS, tests/emulator 3677 PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006, PORT-007, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Build-cd final : v4 (item_flags/timer/trigger_flags, v3/v2 compatibles), écriture atomique, audio SDL/SPU, memmove gameflow validé ASan. Vérifié : Rome v4/v2, niveau 2 v3, PCM audio pendant la marche, ASan nouvelle partie + F5 + F6 sans erreur, chaîne 1→14→titre sans SIGSEGV (hook QA). Build-cd SHA256 b5deda7ed9e0b655d4e335116b76a278f058841b3065d590565da574b3e8a162. tests/porting 497 PASS, tests/emulator 3677 PASS. Restent non validés : campagne réelle/crédits, écoute humaine/CD-XA, manette.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-003 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

ASan 32 bits a trouvé un memcpy-param-overlap dans LoadGameflow: le déplacement du bloc gfStringOffset chevauchait la source. Les cinq copies sont passées en memmove. Partie neuve à Rome sans erreur ASan. Build-cd SHA256 b5deda7ed9e0b655d4e335116b76a278f058841b3065d590565da574b3e8a162; tests/porting 497 PASS, tests/emulator 3677 PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

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

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Chaîne finale revalidée après les correctifs : build de test avec hook QA TOMB5_CHAIN_TEST (même logique de transition, non intégré) enchaîne 1→2→…→14 puis Handle cutseq name: 0, sans SIGSEGV; preuve build/porting/final-chain-bs2-20261029/chain.log. Déclenchements toujours synthétiques, aucune fin de niveau jouée, crédits/FMV non caractérisés.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-007 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Audio final combiné : boucles SF_LOOP et volume FX (SoundFXVolume) appliqués au mixage. Build-bu SHA256 a2722e6c2da9f0241f101674bb6ae4fe336c982e6f77983e795383e4d952c01f. Preuve SDL disk sur build-bu : 18,4 Mo PCM, RMS 1266, actif pendant la marche; dummy sans crash. Limites inchangées : pas d'écoute humaine, pas de CD/XA, ADSR/reverb approximés, pas de test pause/retour titre audio.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-007 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T06:00:00+01:00. Linux32 provisoire.

Backend audio hôte et mixage SPU de base : RAM SPU 512 Ko conservée, getters registres/key-on, VAG/ADPCM 24 voix, pitch/pan/volume, SDL2 44100 stéréo. Correction du pont SpuSetVoiceAttr (volume 14 bits vers 7 bits, ADSR +4/+5) et de PlaySample (vrai index/pitch/pan sans casser la frontière 7 args). Preuves : SDL_AUDIODRIVER=disk pendant une marche à Rome -> 21,1 Mo PCM, RMS 977, actif uniquement pendant la marche; dummy sans crash; tests/porting 497 PASS, tests/emulator 3677 PASS. Build-bn SHA256 809e8cae8f26536052a0590486f5f3672349b8dfc4c4a0a675a7e0d4662ae9a9. Limites : pas d'écoute humaine, pas de CD/XA, ADSR/reverb/loop approximés, pas de test volume nul/pause.

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

## Progression vérifiée du 2026-10-28

PORT-007 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Constat de blocage : aucun backend de sortie audio hôte (ni SDL_Audio, ni ALSA/Pulse/OpenAL) et aucun mixage SPU/CD dans PSXPC_N ; l'audibilité demandée par PORT-007 ne peut pas être validée sur cet hôte. Correctifs d'arrêt propre intégrés : SPU_StopAll libère toutes les voix et reconstruit les canaux, S_SoundStopSample/S_SoundStopAllSamples/S_SetReverbType implémentés, test SpuSetKey(SPU_OFF, SPU_ALLCH) ajouté, smoke titre exit 0 sans ligne Unimplemented. Aucune écoute, aucun réglage de volume, aucune musique XA validés. Ticket non Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-006 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Sauvegarde rapide de port : F5 écrit TOMB5.SAV (magic T5P2, savegame_info, position/rotation/salle/animation de Lara, checksum FNV-1a) ; F6 au titre recharge et reprend. Preuve réelle : partie Rome, marche, F5 room 2 X46592 Y0 Z35826, fermeture normale exit 0, relance, F6, application de la même position et scène identique ; exits 0. Limites : RestoreLevelData non implémenté, les objets/portes/pickups du niveau repartent de l'état initial, seuls Lara et son inventaire/santé sont restaurés ; pas de carte mémoire PSX, pas de chargement en jeu, pas de slots multiples, écriture non atomique. Preuves privées : build/porting/port006-20261028 et port006b-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-005 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Route bornée sur build-l avec positions relevées par point d'arrêt GDB sur UpdateLaraRoom : salle 0 (X46592 Z31232) → salle 2 (Z34964..38853, Y 0→256) → salle 62 (Z38913, Y -1792) → salle 61 (Z40645, Y -274), sans téléportation X/Z. Mur : 12 s de marche bloquées contre une paroi, saut avec W accroche le rebord, pas de traversée. Poussée latérale de 3 s sans déplacement. Pause/Resume reprend au même endroit. Limites : route unique, pas de pente raide/eau, échantillonnage GDB, pas d'équivalence GetHeight cible ; RE-770/771 restent ouvertes. Preuves privées : build/porting/port005b-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Keymap clavier/manette livré (INPUT.CFG, double bind, éditeur F1, 17 tests, 496 PASS) et build-j vérifié. PORT-004 : HUD debug Camera X/Y/Z retiré ; LookCamera remplacé par une implémentation de port fonctionnelle (joint de tête, angles tête/torse, rig de poursuite, retour au suivi) ; réinitialisation du clavier sur perte de focus ; déconnexion manette traitée par instance SDL. Parcours réel sur build-l (SHA256 3b6863…4747) : avance/relâchement, rotations, saut, action, regard gauche/droite avec retour, pause/Resume, scène stable sans entrée, fermeture normale exit 0 ; 15 captures inspectées. Aucun contrôleur physique, pas d'équivalence cible de LookCamera, caméra combat et collisions étendues non validées. Preuves privées : build/porting/port004-final-l-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-27

PORT-001, PORT-002, PORT-003 — **In progress**. Autorisation bornée jusqu’au 2026-10-27T23:59:00+01:00. Linux32 provisoire.

Clone neuf de b5411b6b sans preuves privées. Environnement remis en état sans sudo (pytest, en-têtes C++ 32 bits, GLU et GLEW via un sysroot local). tests/porting 496 PASS, tests/emulator 3676 PASS. Deux builds ELF32 i386 neufs avec GLEW recompilé séparément. Images PAL SLES_033.31 et NTSC SLUS_013.11 converties en TOMB5.CUE/BIN ; l'image NTSC n'est pas la révision exacte du baseline (MD5 3530… au lieu de 4EF5…). Trois lancements PORT-002 : menu à ~35 s, Down/Up changent la sélection, Special Features puis retour, New Game atteint la cinématique. PORT-003 : la scène de Rome est atteinte vers 140 s, Lara et la géométrie sont rendues, déplacement observé, fermeture WM_DELETE_WINDOW et exit 0. Aucune revue indépendante ; le HUD Camera X/Y/Z était encore présent. Preuves privées : build/porting/port002-20261027c, launch-newgame2..4.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-20

PORT-004, PORT-005 — **In progress**. Autorisation bornée jusqu’au 2026-09-20T12:00:00+02:00. Linux32 provisoire.

Deux corrections intégrées : restauration complète R22 (RED66/84 puis84PASS) et mgLOS, deux omissions géométriques (RED28/111 puis111PASS, backend PSX_VERSION && PSXPC_TEST i386). Suite publique après source :446 passed. Build GLEW+jeu neuf ; un parcours réel avec 13 captures inspectées, scène/déplacement/pause/retour titre et exits application/GDB0. LookCamera reste stub en production, regard noir persistant. Reconstruction privée non intégrée : corps avec vrais joint/vue/collision/LOS,79/79 accords fonctionnels mais12/79 écarts GTE bruts conservés ; géométrie/RNG doublés, matrices synthétiques, niveaux11/12 exclus. Module11/12 attribué et239cas privés, ABI moteur à fermer. Aucun Done ni preuve campagne. Prochaine preuve : frontière GTE et module natif avant intégration caméra. Détails : docs/porting/camera-foundations.md ; preuves build/reverse/autonomy-20260920-1200/.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-19

PORT-003, PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Nouveau parcours natif complet avec 13 captures inspectées, retour titre et exits application/GDB 0. Préconditions LookCamera et matrices du joint observées sans injection ; vue noire du regard persistante. Trois exports Ghidra authentifiés (13 fonctions), 384 cas de préfixes cible avec RAM construite, arrêts avant transfert COP2 ou première arithmétique GTE ; rejeu parent identique. Aucun calcul GTE complet ni équivalence actual-TU démontré ; aucun nouveau patch jeu ni rebuild. Candidat de restauration de matrice identifié statiquement, correction bloquée avant RED réel. Aucun Done. Preuves privées : build/reverse/autonomy-20260919-1000/unit03-look-0923/. Détails : docs/porting/runtime-look.md.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-19

PORT-003, PORT-004, PORT-005 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Trois parcours neufs : saut/réception et première transition room 0 → room 2 observés par entrées réelles. Défaut regard reproduit ; réarmement lara.look manquant attribué par Ghidra et corrigé sous PSX_VERSION && PSXPC_TEST (validation i386). RED réel 60 failed / 56 passed, GREEN 116 passed sur TU intégral avec services doublés explicitement ; 251 tests publics PASS. GLEW et jeu reconstruits dans un dossier neuf ; parcours après patch : tête contrôlée sans rotation du corps, mais vue noire du regard toujours présente (LookCamera stub). Relâchement, pause, retour titre et exits applicatifs/GDB 0 pour les trois runs ; 15/13/13 captures inspectées. Aucun Done ; recette complète commandes/caméra/collisions, interactions, sauvegarde et audio non validés. Preuves privées : build/reverse/autonomy-20260919-1000/unit02-controls-0824/. Détails complémentaires : docs/porting/runtime-controls.md.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-19

PORT-002, PORT-003 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Lancement frais : New Game termine LoadLevel vers 71 s, scène avec Lara et locomotion minimale vérifiées par entrées réelles et captures inspectées ; pause, Quit/Yes, retour titre puis fermeture normale (application et GDB exit 0). Aucun patch loader : observation précédente trop courte. Sept tests des archives du 18 septembre réussis, sans nouveaux runtimes pour ces archives. Source jeu inchangée depuis 73faba47 ; binaire existant authentifié, pas de rebuild dans cette unité. PORT-001 reste en cours, PORT-004 et suivants bloqués pour recette intégrée ; campagne, collisions étendues, sauvegarde et audio non validés. Preuves privées : build/reverse/autonomy-20260919-1000/unit01-0757/.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression runtime du 2026-09-18

PORT-002 — **In progress** ; PORT-001 reste en cours. Autorisation jusqu’au 2026-09-18T10:30:00+02:00. Linux32 provisoire.

Premier crash de navigation corrigé : SIGILL au retour manquant de S_SoundPlaySample, avec argument pitch rétabli selon preuve cible. RED 30 échecs/60 PASS puis GREEN 90 PASS sur vraie TU i386 et double PlaySample explicite. Trois lancements neufs du binaire corrigé : titre atteint vers 26 secondes, menu capturé à 29 secondes, entrées réelles Down/Up/c/z observées selon parcours ; ouverture Special Features et retour, Nouvelle partie atteint DoLevel(1). Fermetures WM_DELETE_WINDOW : application exit 0. Capture de chargement illustrée, gameplay non validé ; audio complet non reconstruit. Preuves privées : build/reverse/autonomy-20260918-1030-recovery/. Revue indépendante précommit PASS à 09:47 Paris : 126 tests publics réussis, preuves archivées auditées sans régénération ; pas de validation audio matérielle ni gameplay.

Détails : [preuve runtime](runtime-menu.md).

Les blocs antérieurs ci-dessous sont historiques, y compris leur ancienne échéance et leurs réserves visuelles. Aucun Done attribué.

## Progression active du 2026-09-18

PORT-001 — **In progress**. Autorisation technique bornée jusqu’au 2026-09-18T08:30:00+02:00 ; elle ne valide pas définitivement la cible.

Recette build/launch industrialisée : scripts/porting/linux32.py, deux builds ELF32 neufs avec GLEW recompilé séparément, sans chemin runtime-1058. Lancement frais avec données privées ; fermeture WM_DELETE_WINDOW, application exit 0 avant limite. Captures privées non vides (pixels décodés), pas de validation visuelle complète ; menu et gameplay non validés. Rejeu indépendant : troisième build ELF32 réussi ; correction préflight 125/126 caractères après revue. Acceptation visuelle complète non établie. Preuves : build/reverse/autonomy-20260918-0830/.

Recette : [Linux32](linux32.md).

Les statuts, compteurs et restrictions du lot initial ci-dessous restent un historique du 13 septembre, pas une nouvelle demande de GO. Aucun ticket accepté Done.

# TOMB5 — Backlog fonctionnel, lot initial

Date : 2026-09-13 (Europe/Paris). Base inspectée : `eac6d930`.

Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

Backlog fonctionnel initial, distinct des tickets historiques RE. Rédaction terminée ne signifie pas fonctionnalité terminée. Aucune implémentation, nouvelle RE binaire, compilation ou exécution du jeu dans ce lot. État hérité de RE-772 : build64 crash LoadLevel ; build32 splash 30 secondes, timeout 124 ; menu interactif et gameplay non validés. Les tests de ce backlog valident les documents, pas le jeu.

Rédaction : 8/8 tickets. Implémentation validée dans ce lot : 0/8.

## Convention et progression

P0 = prérequis du premier socle jouable ; P1 = boucle utilisateur intégrée suivante. Todo = prêt à planifier, non commencé ; Blocked = recette intégrée dépendante de tickets non validés. Ces dépendances sont des portes de validation : une préparation parallèle peut être proposée, mais ne change pas leur statut et ne crée pas de cycle. Aucun ticket Done. Chaque modification d’implémentation nécessite une nouvelle autorisation ; le rédacteur ne marque pas les tâches fonctionnelles [x].

- [x] Cadrage initial étiqueté comme proposition.
- [x] Premier lot rédigé avec références et dépendances.
- [ ] Cadrage cible définitivement accepté par l’utilisateur.
- [ ] Implémentation et recettes des PORT validées.
- [ ] Domaines restants inventoriés ; backlog non exhaustif.

## Tickets

| ID | Priorité | Status | Objectif | Dépendances |
|---|---|---|---|---|
| [PORT-001](PORT-001.md) | P0 | Todo | Build Linux32 reproductible | Aucune |
| [PORT-002](PORT-002.md) | P0 | Blocked | Du splash au menu interactif | PORT-001 |
| [PORT-003](PORT-003.md) | P0 | Blocked | Nouvelle partie et première scène jouable | PORT-002 |
| [PORT-004](PORT-004.md) | P0 | Blocked | Commandes et caméra de base utilisables | PORT-003 |
| [PORT-005](PORT-005.md) | P0 | Blocked | Déplacement solide et passages entre salles | PORT-004 |
| [PORT-006](PORT-006.md) | P1 | Blocked | Sauvegarder et reprendre après relancement | PORT-005 |
| [PORT-007](PORT-007.md) | P1 | Blocked | Audio essentiel et arrêt propre des sons | PORT-004 |
| [PORT-008](PORT-008.md) | P1 | Blocked | Boucle du premier niveau et passage au suivant | PORT-005, PORT-006, PORT-007 |

## Couverture du backlog, pas complétion du port

| Domaine | Couverture | Tickets | Reste / limite |
|---|---|---|---|
| Build/ABI32 | Covered | PORT-001 | Recette bornée, pas tous environnements |
| Titre/menu | Covered | PORT-002 | Menu de base |
| Chargement/rendu initial | Partial | PORT-003 | Premier niveau seulement |
| Entrées/caméra | Partial | PORT-004 | Socle ; caméra combat et remapping restants |
| Collision/salles | Partial | PORT-005 | Route bornée ; eau et cas étendus restants |
| Sauvegarde | Partial | PORT-006 | Cycle local ; compatibilité externe restante |
| Audio | Partial | PORT-007 | Socle ; voix et fidélité restantes |
| Progression/campagne | Partial | PORT-008 | Premier passage seulement, reste campagne à inventorier |
| Combat/IA/armes | To inventory | — | Pas de ticket détaillé dans ce lot |
| Inventaire/puzzles/objets | Partial | PORT-008 | Un pickup/interaction ; catalogue restant |
| Eau/nage/cordes/mouvements spéciaux | To inventory | — | Dépendances du parcours à découvrir |
| Cinématiques/FMV/textes/langues | To inventory | — | Ne pas masquer une dépendance indispensable au titre/parcours |
| Rendu complet/effets/performance | To inventory | — | Pas de budget performance ni fidélité exhaustive |
| Distribution/config/accessibilité | To inventory | — | Installation utilisateur finale et options à définir |
| Linux64 natif/autres plateformes | Separate | — | Cadrage distinct à valider |
| Équivalence binaire complète | Separate | — | Pas le critère du premier port jouable |

Covered = périmètre borné décrit ; Partial = une tranche décrite ; To inventory = pas encore détaillé ; Separate = chantier distinct. Aucun de ces libellés ne valide le fonctionnement du jeu.

## Estimation et suite

Estimations par ticket : jugement exploratoire, pas une mesure ; jours-personne de travail futur sur la portée bornée, pas des engagements et non sommables en durée de port. Confiance Low sauf recette build Medium. Première version du backlog : le socle initial de 8 tickets est rédigé. Reste indicatif 0,5–1 journée pour élargir le cadrage ; 2–4 jours de travail supplémentaires pour un backlog multi-domaines structuré et revu, selon accès aux preuves et arbitrages. Aucun runtime nouveau mesuré pendant ce lot. Portage complet : durée non estimable de façon crédible avant menu/niveau et inventaire de la campagne.

Prochaine décision : confirmer la cible proposée et autoriser séparément PORT-001/002 ; poursuivre le backlog combat/IA, puzzles, eau, cinématiques et campagne après arbitrage. Le rapport distinct de 20:30 peut réestimer à partir de ce lot ; aucune nouvelle cartographie après 20:30 dans la fenêtre autorisée.

## Maintenance et vérification documentaire

`backlog.json` est la source éditoriale. Régénérer avec `python3 scripts/porting/render_backlog.py`. Contrôler sans écriture avec `python3 scripts/porting/render_backlog.py --check`.

`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/porting/test_backlog.py`

Les garde-fous de ce lot initial refusent Done/autorisation d’implémentation ; faire évoluer explicitement contrat et tests lors d’un futur lot autorisé. Le HTML partagé est un snapshot documentaire, sans image ni asset. Le dashboard reconstruction historique n’est pas régénéré.
