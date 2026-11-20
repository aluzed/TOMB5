# RMIG-021 — Campagne 64 bits : parcours du Colosseum

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Colosseum terminé, transition → niveau 4 re-validée, niveaux 4 et 5 rendus, costume 6 dessiné en entier. Pour les cinématiques : la donnée existe (`CUTSEQ.JIZ` = entrée 1 de `GAMEWAD.OBJ`, extraite avec succès, signature `(C) DEL!`) et le chemin de chargement `Load_and_Init_Cutseq` est prêt avec instrumentation (`TOMB5_CUTDBG`), mais (a) `cutseq_num` reste à 0 au démarrage (aucun trigger TO_CUTSCENE armé) et (b) les intros de niveau sont des FMV `FMV*.STR` que le port ne sait pas décoder. Le lecteur FMV est le vrai chantier restant.

## Objectif

Parcourir The Colosseum (niveau 3) en 64 bits et valider la stabilite/rendu des salles du parcours.

## Faits établis

TOMB5_START_LEVEL=3 charge le niveau 3 (The Colosseum, 125 salles). Le decor est rendu, Lara est visible/deplacable (pos 90642,4608,52736 room 20), le processus reste stable. Le rendu du sable est encore deforme par endroits et la camera peut regarder un mur sombre apres deplacement.

## Périmètre

SPEC_PSXPC_N/ROOMLET* / DRAW*, GAME/EFFECTS/control du niveau 3.

Hors périmètre : Vulkan, ImGui, RT.

## Tâches

- [ ] Rejouer le parcours 12 -> 26 -> 27 -> 108 -> 15 -> 18 -> 100 -> 90 -> 102 -> 110 -> 83 -> 111 -> 85 -> 70 en 64 bits.
- [ ] Corriger les derniers polygones deformes/rendu sable observes dans le Colosseum.
- [ ] Verifier les sauvegardes F5/F6 aux etapes cles du parcours.

## Critères d’acceptation

- Le parcours du Colosseum est realisable sans SIGSEGV en 64 bits.
- Les salles cles et les objets du parcours sont rendus correctement.
- Une sauvegarde en milieu de niveau est rechargee correctement.

## Validation

Execution 64 bits avec captures et journal, comparaison avec le parcours 32 bits documente.

## Inconnues

Le rendu deforme du sable peut venir de la sous-division (SubDiv/div3tab/div4tab) ou de la projection des grands polygones.

## Estimation

1 a 2 jours-personne.

## Dépendances

- RMIG-020

## Preuves

- 2026-11-17 : TOMB5_START_LEVEL=3 : [DRAW] lvl=3 nrooms=125 room=20, [LARA] pos=(90642,4608,52736) mesh_bits=FFFFFFFF, 3897 sommets, processus stable apres deplacement Up. Capture du Colosseum (arene de sable, murs) correcte mais sable partiellement deforme.
- 2026-11-18 : TOMB5_START_LEVEL=3 + TOMB5_START_POS=43364,768,52325,12,-16384 place Lara en room 12 et le gameplay repond (deplacement Up change pos/room, camera room 26). Une chute volontaire depuis la corniche declenche un GAME OVER attendu (pas un crash). Comparaison 32 bits au meme point : le sable et les grands polygones sont egalement deformes, donc ce defaut visuel est pre-existant et non specifique au 64 bits.
- 2026-11-18 : Salles validees en 64 bits via TOMB5_START_LEVEL=3 + TOMB5_START_POS : room15 (48640,1024,58880) rendue avec bannieres/colonnes ; room90 (48640,512,70144) rendue avec arene/arches/ciel, Lara visible ; room102 (49664,512,62976) rendue avec porte/serrure. Aucun SIGSEGV, processus stable. Coordonnees de room : R15 x=45056 z=53248, R90 x=46080 z=65536, R102 x=48128 z=60416 ; items : gladiateur probable obj59 room15, Roman God obj61 item79 room90 (48154,512,69120), keyhole2 obj259 room102, pickup final obj220 room70 (55808,7936,70144).
- 2026-11-18 : Tentative de reprise en room 12 (40448,1023,51712) avec TOMB5_SKIP_CUTSCENE : Lara est placee en room 12 mais est immediate repoussee en room 14 (y=6144, anim 25) par le demarrage/cinematique du niveau. Les reprises directes en rooms 15/90/102 restent valides. Le parcours depuis la corniche doit donc se faire en jeu (ou via une sauvegarde 64 bits native) ; la compatibilite des sauvegardes 32 bits reste un point ouvert.
- 2026-11-18 : Outils de debug ajoutes : TOMB5_SKIP_CUTSCENE (force GLOBAL_playing_cutseq/cutseq_num/cutseq_trig a 0) et TOMB5_START_POS_HOLD=n (force la position START_POS pendant n frames). Avec hold=600, la position room12 est maintenue mais le niveau reste en fade (ScreenFade=239, fading=1) sans progression observable : la cinematique/le start trigger garde la main. Les reprises directes en rooms 15/90/102 restent la voie valide pour tester le rendu.
- 2026-11-18 : Clignotement de Lara corrige en 64 bits. Les primitives de Lara etaient generees et parsees chaque frame (laraPrims 286..418) mais la bbox ecran alternait corps complet / sous-ensemble. La desactivation de l interpolation (TOMB5_NO_LARA_INTERP=1) stabilisait le modele. Cause : dans DEL_CalcLaraMatrices_Interpolated_ASM, l adaptation LP64 affectait s0=lara_matrices avant mTranslateXYZ_CL(s0[6..8]) (translation lue dans les rotations), et l arithmetique du squelette utilisait des index short* sur le tableau hote bones (long, 8 octets). Correction : pointeur m0 separe pour les matrices, pointeur long* b1 avec index en mots. Validation : bbox pleine chaque frame, lara_matrices stable autour de (-8,155,1295), captures stables ; build 32 bits inchange.
- 2026-11-18 : Fin des disparitions du processus : le pool PORT_LowAlloc (16 Mio, MAP_32BIT) etait sature par des allocations par appel. Reproduit sous gdb : exit code 1 apres PORT_LowAlloc: pool exhausted (16777056 + 1024 > 16777216). Sites : ROOMLET1/2/3/4/B (scratchPad 1K + scratchPad2 2K par appel) et ANIMITEM CalcAllAnimatingItems_ASM (1K par frame). Le code de cache statique LP64 existait mais etait dans un #else inatteignable. Correction : allocation unique via pointeur statique local. Validation : reproduction gdb de plusieurs minutes (marche, rotations, animations) sans epuisement ; build 32 bits inchange.
- 2026-11-18 : Fin de The Colosseum atteinte en 64 bits via F9 (teleport runtime depuis /tmp/tomb5_teleport). Salles 15/90/102 rendues et stables (captures), pickup final obj220 ocb66 salle 70 (55808,7936,70144) pris -> transition effective vers le niveau 4 : lvl=4 room=70 nrooms=169. Blocage suivant : intro du niveau 4 sur ecran noir (ndraw=1, camera 12288,2048,49152, action c sans effet), lecteur de cinematique non porte.
- 2026-11-18 : Niveau 4 : LaraDrawType=6 (module LARA6 non porte) -> Lara invisible (aucun case dans le switch). Repli temporaire type 6 -> DrawLaraL1 + masquage des meshes optionnels pendant le draw (0x80000000) pour supprimer un polygone noir etire du a une skin non geree. Avec TOMB5_START_LEVEL=4 TOMB5_SKIP_CUTSCENE=1, salle 99 chargee, Lara visible et controlable (35328,-4096,29596 -> 33893,-4096,30019). Outils F10 (/tmp/tomb5_laradraw) et F11 (/tmp/tomb5_meshbits). Reste : porter LARA6 et le lecteur de cinematique (intro niveau 4 en ecran noir sans SKIP_CUTSCENE).
- 2026-11-19 : Niveau 5 chargé et rendu en 64 bits/Vulkan (TOMB5_START_LEVEL=5, 300 frames) : lvl=5 room=23, 195 salles, LaraDrawType=6 (repli L1 documenté), scène industrielle rendue correctement, aucun incident. La campagne dépasse donc le Colosseum ; restent le module LARA6 (modèle gris) et le lecteur de cinématique pour les intros.
- 2026-11-19 : Niveau 4 sans TOMB5_SKIP_CUTSCENE : la scène se rend correctement (plus d’écran noir), mais l’intro ne joue pas. Diagnostic : handle_cutseq_triggering s’exécute chaque frame (arme cutseq_trig + fondu), Load_and_Init_Cutseq n’atteint jamais init_resident_cutseq, et le repli PCopen("\\CUTSEQ.JIZ") échoue. L’image disque TOMB5.BIN ne contient aucune chaîne CUTSEQ/.JIZ : la source de données des cinématiques est absente du dépôt. Blocage de données, pas de code.
- 2026-11-19 : Re-validation de la transition de niveau avec le build Vulkan-only actuel (après les correctifs LP64 MULFP/pointeurs) : départ niveau 3 (Colosseum, 125 salles), téléport F9 sur le pickup final de la salle 70 (55808,7936,70144), pickup déclenché → le jeu charge le niveau suivant (lvl=4, 169 salles, Lara en salle 99), rendu correct, aucun incident. Capture : docs/porting/render/colosseum-vers-niveau4.png.
- 2026-11-19 : Costume 6 : le masquage de meshes du repli L1 (mesh_bits=0x80000000) est retiré — le polygone noir qui le justifiait venait des bugs de pointeurs LP64 corrigés en RMIG-023. Modèle complet vérifié niveaux 4 et 5 (capture docs/porting/render/lara-costume6-complet.png) ; capture de référence niveau 3 inchangée (sha256 63041e5c…). Le module LARA6 dédié reste absent mais le rendu n’est plus amputé.
- 2026-11-19 : Niveau 5 : le build 32 bits rend noir parce qu’il émet 3× plus de quads que le 64 bits ([PH] 3C=1008 vs 335, nv=7251 vs 3102) ; les primitives Lara sont identiques, le défaut est dans le chemin roomlet 32 bits (RoomDrawType=2, ROOMLET2.C). Le build 64 bits rend la scène correctement — ce n’est pas une régression du portage.
- 2026-11-20 : Niveau 5, build 32 bits : la transmission du pointeur cdb par les registres GTE LG2/LG3 est correcte (a1 == cdb, a3/s0 dans les buffers bas) — piste écartée. Le surplus de quads (3C=1008 vs 335) reste à instruire côté construction de la liste de salles (number_draw_rooms / draw_rooms[]) ou boucle roomlet. Instrumentation : TOMB5_RL2DBG=1 → [RL2]. Sans impact sur le build 64 bits.
- 2026-11-20 : CUTSEQ.JIZ extrait de GAMEWAD.OBJ (entrée 1 : offset 2048, taille 3299328 ; signature « (C) DEL! » + table offsets/tailles, conforme à ce qu’attend Load_and_Init_Cutseq). Placé dans le répertoire de données, le chargement n’est toutefois jamais déclenché : [CUT] name=4 num=0 trig=0 à chaque frame (aucun trigger TO_CUTSCENE armé) et [CUTL]/[CUTP] ne s’affichent pas. Par ailleurs le disque contient FMV0..FMV7.STR : les intros de niveau sont des FMV, non décodées par le port.

## Références

- `docs/porting/colosseum-walkthrough.md:7` (parcours salle par salle)
- `SPEC_PSXPC_N/DRAWOBJ.C:680` (SubDiv/div tables)
