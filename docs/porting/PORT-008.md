## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum: portage PUSHABLE_OBJECT1..5 depuis game/moveblok.cpp (nouveau GAME/MOVEBLOK.C/.H: InitialiseMovingBlock, MovableBlock, MovableBlockCollision, TestBlockPush/Pull + PortCollidedObjects sous-ensemble local car GetCollidedObjects global est un stub). PortSetupGameplayObjects assigne initialise/control/collision + save_position/save_flags. build-gameplay59 SHA256 52c73c373ee86ed6c5c3a08e60eb14c51cb9350550f38797079551f759b0b4a3; tests 4177 PASS. Runtime push100e/push100f: item100 room112 79360,4864,54784 bounds -512..512/-1024..0; depuis le sud 55300 face nord, accroche state38 anim120 snap 79360,4864,55391; fin ready frame 2067 + IN_FORWARD -> state36 anim123 status1; bloc z 54784->53760 (-1024) puis anim417 et TestTriggers; status revient 0. Approche nord echoue: snap 54177 reassigne room19 alors que le bloc est room112, donc PortCollideItems ne dispatche plus (limite empilement rooms). Limite preexistante: GetSpheres UNIMPLEMENTED dans SPEC_PSXPC_N/SPHERES.C donc TestCollision=0 et ObjectCollision ne repousse pas; le bloc est traversable sans accroche. Golden rose item99 81408,4864,57856 pas encore ramassee. Build59 produit en recompilant MOVEBLOK.C+SETUP.C et ajout objet au link.txt de build58 (build propre toujours bloque par declarations preexistantes). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum: niveau 3 charge via DoLevel name=3 gfCurrentLevel=3. Recon level3-recon-20261113: 125 rooms, 110 items, Lara room1 96768,-384,52736. Objets: item100 PUSHABLE_OBJECT1 room112 79360,4864,54784; item99 PICKUP_ITEM4 room112 81408,4864,57856; item5 TELEPORTER + items6-19 CRUMBLING_FLOOR/EARTHQUAKE room8 X40448..43520 Z51712..53760; item124 six TEETH_SPIKES. Parcours joue level3walk-20261113: glissement initial 96768,-384,52736 room1 -> room20 x92025..85435 y3718->4352 -> room2, arret 77925,4351,52736 cellule xx3/zz2; carrefour room2 ouvre zz0->rooms22/5 et zz3->rooms19/4; bloc pushable au sud Z54784. Blocage moteur: PUSHABLE_OBJECT1..5 sans initialise/control/collision dans PortSetupGameplayObjects, donc premier secret et passage du bloc non jouables; portage PC a faire. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: geometrie corrigee (GetFloor PSX transpose index=zz+xx*x_size). Salle 116: receptacles cellules xx1/zz4 et xx1/zz6, passage ouest xx0/zz5 -> room70, porte item106 CLOSED_DOOR1 a 51712,-256,27136. Traversee reelle validee walkgate-20261113: 52000,-256,27136 face ouest -> room116->70 a x50585 -> room204 a x49097 (y -256->1536 par pit_room=204); blocage a x47205 sur cellule solide xx5/zz2 de room204 (X46080..47104), sauts sans effet (spike/spike2/spike3-20261113). Caverne finale: pont zz2 y=1536 avec TEETH_SPIKES items132-137 X44544..50688; room241 corniche y0/2304/3584 ouvre room233; room233 couloir X33792..43008 Z25600..28672, sol 2304->9728 vers l'ouest, trigger TO_FINISH idx5606 en X37888,Z26624. levelend2-20261113: depuis 42100,2304,27136 glissement scripte state24 anim70 jusqu'a x38887 y6680 -> gfLevelComplete=3, puis DoLevel name=3 gfCurrentLevel=3: The Colosseum charge. Limites: pont a pointes non franchi (mur plein), fin atteinte par teleport sur la derniere pente puis glissement+trigger executes par le moteur; symboles poses par sonde PuzzleDone+_TestTriggers. Preuves geom-20261113, geo2-20261113, walkgate-20261113, spike*-20261113, finish-20261113, levelend2-20261113. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: triggers des receptacles VENUS/MARS ciblent item106 CLOSED_DOOR1 obj300 room116 51712,-256,27136 + effets portal/flamme/X-ray. Correctif moteur build-gameplay58: PortSetupGameplayObjects assigne DoorControl/DoorCollision aux CLOSED_DOOR1..6 non-MIP comme le setup PC. Apres placement des symboles, item106 passe a status=1 flags=15904 data initialise et DoorControl(106) l'anime; avant, control NULL laissait la porte inactive. Traversee reelle de la porte restant a jouer. Build propre encore bloque par declarations preexistantes (anims COLLIDE, GetFloor OBJLIGHT, input TRAPS, TestCollision/GLOBAL_ SWITCH); build58 produit par recompilation SETUP.C + link des objets build57. SHA256 f00f70e094d8ecb250ec872088aad6422a75d7d62e7ee8e4941c1ba1b60b7410; tests 4177 PASS. Preuve closeddoor-20261113/. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: symboles VENUS/MARS valides. item49 PUZZLE_ITEM5 room64 collecte (puzzleitems[4]=1 status=3); item63 PUZZLE_ITEM4 room69 collecte (puzzleitems[3]=1 status=3). Placement item95 PUZZLE_HOLE4 et item96 PUZZLE_HOLE5 -> objets253/254 PUZZLE_DONE4/5 status=1 flags=15904. Aucun flipmap modifie ni porte 284-295 apres placement; porte finale des deux symboles reste a identifier (trigger hors plage ou cutscene/fin). Preuve symbols-20261113/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: retour rue pavee valide (walk0-20261113). Depuis room46 78747,768,37376 marche nord puis est -> room10 78747,256,40027 -> room0 81614,256,42988 -> 83118,0,43975. Boucle golden coin bouclee. Prochaine zone: rue pavee, petite porte mur blanc, allee, bassin. Symboles VENUS/MARS probablement PUZZLE_ITEM5 item49 room64 55808,1792,34304; PUZZLE_ITEM4 item63 room69 45568,1792,43520; PUZZLE_ITEM1 item129 room196 56832,4864,52736. Room70 contient ANIMATING5 et trappe item71 (Mouth of Truth) pres du bassin. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: porte113 franchie! Depuis room134 75000,0,37376 marche est -> 76335,0,37376 room134 (au-dela de la porte) -> 77792,256,37376 room46 -> arret 78747,768,37376. La porte de la golden coin ramene dans la cour (room46). Preuve walk134c-20261113/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, porte 113: room134 X70656..75776 Z34816..41984 minfloor=0; room83 X74752..80896 Z34816..37888 minfloor=-2048; porte 113 a 76288,0,37376 entre les deux. Approche correcte depuis room134 a x~75000,y=0,z=37376 en marchant vers l'est. Les tentatives walk134/walk134b ont ete interrompues par redemarrages serveur avant la sortie. Preuve rooms134b-20261113/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: porte item113 activee par la golden coin (status=1 flags=15904). DoorControl(113) initialise data, anim=601 frame=0. Teleport a 76288,0,37900 reassigne room83 y=-2048; marche sud s'arrete a 76288,-2048,35941. Porte activee mais franchissement encore bloque par l'empilement 5D room134/83. Preuve walk134-20261113/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-12

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-12T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: walkthrough Stella confirme 3 golden roses = PICKUP_ITEM4 items 14/88/139 et golden coin = item122 PUZZLE_ITEM3 obj174 room166 83456,-1024,19968. Collecte validee (coin122-20261112): puzzleitems[2] 0->1, item.status=3. Placement valide (hole42b/hole42c-20261112): item42 PUZZLE_HOLE3 obj244 room63 78336,-1024,15872; PuzzleDone -> obj252 PUZZLE_DONE3 status=2 flags=15904 et active porte item113 obj288 room134 76288,0,37376 status=1 flags=15904. Aucun flipmap modifie. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-08

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-08T23:59:00+01:00. Linux32 provisoire.

Analyse géométrie données Trajan's Markets (NTSC, LBA 18404, 252 rooms, offsetRoomInfo/roomInfoLength) : puits 207->201->199->200 intégralement pit (non atterrissable), aucun CLIMB/MONKEY floor_data dans la zone. Hub 209 (portails 10/11/201/206/210/213) ; 207->10 plat, 10->209 +256u sky/pit ; montées +1024u sans CLIMB à valider (209->11,213->45,214->12,210->48,211->49,212->5). Route plausible 207->10->209 puis branche nord (213/214 vers 45/12/202) ou est (210-212 vers 48/49/5, 212<->50 départ). Non validé en jeu. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-08

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-08T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: blocage navigation dans l'empilement 5D 207/201/214/213. Room46 minfloor=1024 sky_room=214; room214 minfloor=-1024 pit_room=46; 214->213 horizontal z~38912 x=76800..80896; 213->209 horizontal z~39936 x=76800..80896; rooms12/45 minfloor=-2048 au-dessus. Sauts aveugles dans les trous insuffisants pour trouver la route prevue. Besoin d'un walkthrough/ordre des salles ou d'une vue du maillage/escalier pour continuer sans deviner. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-08

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-08T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: essai saut sud depuis 78747,0,44500 (jump201c-20261108) ne monte pas dans room201; traverse la limite et retombe room10 (78747,0,43259) puis 9/46/17/15/52. Bord z0 non grimpable. Room201 accessible seulement en vol, sans atterrissage maitrise. Il faut etude geometrique du trou (maillage/echelle) ou autre route. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: teleport room201 a 77500,-1024,43500 reassigne la room a 10 (empilement 5D), puis marche nord retombe en room207 et s'arrete a 77500,0,48031. Teleport direct 201 non fiable. Route alternative: room209 reliee a room10 (deja traversee a 78336,256,40788), permettant d'eviter le trou 207->201 et d'enchainer 209->206/210/213. Preuve walk209b-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: room207->201 par trou vertical. Essais saut: Lara entre bien dans room201 en vol (room=201, y~-954/-884) mais retombe en 207. Room201: murs en x3, trous x1-2/z1-4, cellules solides x0 et bordure z0. Prochain essai: saut lance est x~77000->79000 ou passage par bordure z0. Preuves jump201-20261107/, jump201b-20261107/, floors207-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: room207->201 n'est pas une marche mais un trou vertical. Cellules 7-10 et 13-16 de room207 ont sky_room=201; memes cellules de room201 ont pit_room=207. Room207 minfloor=0, room201 minfloor=-1024. Joueur a 78747,46528 cellule15 juste sous le trou; il faut saut/grab ou echelle pour monter. Preuve floors207-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: depuis room219, marche est a z=46528 passe a cote de la porte138 (z=46592) et entre dans room207 (77487,0,46528), arret a 78747,0,46528. Portail room207->201 horizontal x=76800..78848 z=44032..48128; room201 minfloor=-1024 (un secteur au-dessus de room207 minfloor=0), marche a franchir, joueur arrete juste avant. Preuves walkdoor138-20261107/ et rooms201-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: collecte validee de item139 PICKUP_ITEM4 en room219. PickUpCollision -> status=3; DEL_picked_up_object branche PICKUP_ITEM4 (lara.pickupitems |= 8, son secret CDA_XA1_SECRET). C'est un secret. Porte item138 DOOR_TYPE3 (76288,0,46592) reste status=0 anim=601 state=0 goal=0, non ouverte. Preuve pickup139-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: grande traversee marche depuis room161 (78336,256,22016): 161->52 (78336,256,23304) ->15 (78336,1280,27675) ->17 (78336,1024,33503) ->46 (78336,1024,36417) ->9 (78336,256,39331) ->10 (78336,256,40788) ->207 (78336,0,45159) ->219 (76395,0,46181 puis 71781,0,46528). Room219 contient item138 DOOR_TYPE3 76288,0,46592 et item139 PICKUP_ITEM4 71168,0,47616; joueur arrete a 71781,0,46528. Preuves walk161n-20261107/ et walk219-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, portail 52->161: le joueur s'arrete a z=22629 devant le portail z~22527 x=76800..79872. Up+Jump: saut sur place state=28 sans franchir. Up+Duck: rampement state=80 anim=263, recule a z=22729 puis bloque. Passage necessite alignement/geste plus precis ou teleport de validation. Room161 contient item118 ANIMATING1 78336,256,22016. Preuves walk52route-20261107/, walk161-20261107/, walk161c-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: retour marche vers le marche bas. Depuis room15 (78000,1280,28500), marche sud -> room52 a 78000,1280,27447 puis descente a 78000,256,22629 (room52). Portail room52->161 a z~22527 x=76800..79872 normale +z; le joueur s'arrete a z=22629 juste avant, petit saut/rebord necessaire. Room161 contient item118 ANIMATING1 78336,256,22016. Preuve walk52route-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-07

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-07T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, structure verticale room224/24/222/232/154: room224 X69632 Z30720 6x8 minfloor=-2048 portes 23x3/222x2/154/232 pit=23 sky=232; room24 X69632 Z30720 6x7 minfloor=3072 porte 23 sky=23 (cul-de-sac bas); room222 X69632 Z26624 6x8 minfloor=-2048 portes 224/224/16/51/168/16/221 pit=16; room232 X69632 Z30720 6x8 minfloor=-4096 portes 205/224/168 pit=224; room154 X70656 Z34816 5x6 minfloor=-2048 portes 203/83/224/205/84. Room23 (floor1024) sous room224 (floor-2048); suite demande montee par trou/escalier ou passage 222/232. Preuve room224-20261107/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: route 223->221 validee depuis la corniche ouest (teleport de test 80500,-2048,30000 puis marche reelle): room223 -> 221 (79325,-1729,30000) -> chute room15 (78342,1280,30000) -> room16 (75679,1280,30000) -> room23 (72198,1024,32797 puis 71640,1024,34161). Le joueur atteint la zone des engrenages (room23) par la marche. Portails 16->23 x=71680..72704/73728..75776 z~31744; 23->224 plans horizontaux x=71680..72704/73728..75776 z=31744..35840; 23->24 x=70656..75776 z=32768..34816 normale -y. Suite probable par 224 ou 24. Preuve walk23b-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, portails decodes (format AdjoiningRoom+Normal+4 vertices): room223->221 paroi ouest x~79871 z=28672..31744 y=-2048..0; room221->163 paroi nord x~77824..78848 z~27647; room21->225 ouverture horizontale y~-2048 x=80896..86016 z=31744..36864; room163->164 x~77776..78848 z~23551. Route 223->221 non franchie, demande saut vers corniche ouest ou contournement de la fosse. Preuve doorsfull-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, room223: X78848 Z26624 6x7 minfloor=-2048, portes 18/33/225/225/18/221, pit_room=18 sur cellules x2-5 z1-4. La marche nord depuis l'entree room33 tombe dans room18; deplacement ouest bloque vers x=80997. Route vers room225 probablement par saut au-dessus de la fosse ou porte dans la paroi ouest, non franchie. Preuve room223-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, room225: X79872 Z30720 6x7 minfloor=-2048 maxceiling=-4352, portes 21/223/223/3, pit_room=21 sur de nombreuses cellules (room225 juste au-dessus de room21 par un trou). Tentative de montee depuis room21 centre avec Up+Action: input=0x100041 mais Lara reste immobile (state=2 anim=103, position inchangee); escalade non trouvee. Preuve room225-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, donnees rooms 21/22/23: room21 X78848 Z30720 6x8 portes 18/18/225/22 et sky_room=225 sur plusieurs cellules (ouverture de plafond vers room225); room22 X79872 Z30720 6x7 porte 21; room23 X69632 Z30720 6x8 portes 224/224/224/16/16/24 et sky_room=224. Suite probable room21->225 par l'ouverture/escaliers puis 225->3/223/21. Escalade reelle vers room225 restant a jouer. Preuve rooms212223-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: exploration reelle de la room21 apres le parcours 33->223->18->21. Positions 81408,1024,34727 -> 83215,1024,32869 -> 85915,1024,33093, toujours room21; le passage vers room22/23 (objets et engrenages) n'est pas franchi. Portes room21 -> 18/225/22. Preuve walk21c-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: parcours reellement marche apres le flyby, sans teleportation pendant la marche, room 33 -> 223 -> 18 -> 21 en maintenant Up. Positions: 81408,-2048,25600 (room33) -> 81408,-2048,28439 (room223) -> 81408,8,29878 puis 81408,1280,30149 (room18) -> 81408,1024,32001 (room21) -> 81408,1024,34727 (room21, pres de item11 TRAPDOOR1 et des engrenages). Le joueur atteint la zone des engrenages par la porte ouverte. Autre route du graphe: 33->223->221->163->164->166. Preuve walk33-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: le flyby SPOTCAMS 1 se termine naturellement (spot=0, dis=0) au 6e echantillon, donc bDisableLaraControl est bien remis a 0 et le controle revient sans patch (preuve flyend2-20261106/). La navigation dans la room52 fonctionne alors (input=0x1, deplacement, montee/descente). Graphe de portes: 33->223->221->163->164->166; room52 est la salle basse, room163 (Uzi ammo) au-dessus (sky_room=163), portes 163->52/221/164. Parcours joue 223/221/163 restant a faire. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, navigation: apres le flyby bDisableLaraControl reste a 1 tant que la spotcam n'est pas finie; en laissant finir (ou en forcant la variable pour la sonde), Lara marche (input=0x1) dans la room52. Graphe de portes: 33->223->221->163->164->166. Room52 est la salle basse, room163 (Uzi ammo) au-dessus (sky_room=163); portes 163->52/221/164. Parcours joue 223/221/163 restant a faire. Preuves doors52-20261106/, doors33-20261106/, roomgraph-20261106/, navwalk-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: apres la correction multi-flip, vue de controle depuis la room52 (X79360 Y1792 Z24064) montrant l'escalier/passage degage derriere la porte circulaire (room52-20261106/screenshot.png). La navigation reellement jouee au-dela de cette salle reste a effectuer. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: correction du traitement multi-TO_FLIPMAP dans _TestTriggers. Le flyby contient FLIPMAP 3 et 4; le code ne conservait qu'un seul flip (le dernier). PortRecordFlip collecte les valeurs et _TestTriggers applique chaque FlipMap en fin de trigger. Runtime: FlipMap(3) et FlipMap(4) appeles, flip_stats[3]=1 et flip_stats[4]=1; rooms 52/176 (porte circulaire, X75776 Z21504 Y1280..-2048) et 147/163 (Uzi ammo item119, Y-2048..-4096) permutees. Collecte item119 validee (num_uzi_ammo 30->60, status=3). Preuve multiflip-20261106/. Build-gameplay57 SHA256 5b104499da49733526656e8fdbc4b4fb1fdadb4ee8a06752e57b1c020976373d; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets: le flyby applique FlipMap(4) (flip_stats[4]=1), permutant les rooms 52/176 (X75776 Z21504, Y1280..-2048): c'est la porte circulaire effective. flipmap[3] est aussi a 0x3E00 mais flip_stats[3]=0: le trigger contient deux entrees TO_FLIPMAP et _TestTriggers ne conserve qu'un seul flip (le dernier), donc les rooms 147/163 (Uzi ammo item119) ne sont pas permutees. Collecte directe de item119 validee (num_uzi_ammo 30->60, status=3), mais acces via flip3 a corriger. Preuves flip4-20261106/, flipstats-20261106/, uziammo-20261106/. Build-gameplay56 SHA256 85783c9a13bc36606f388f557e9521fd66a384690df5ca22f1b3949602905d12; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-06

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-06T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets, suite du puzzle: apres l'activation des engrenages, le flyby SPOTCAMS 1 se poursuit et declenche TO_FLIPMAP 3; flipmap[3] passe de 0 a 15872 (0x3E00). Rooms concernees: 147 et 163, meme emprise X75776 Z21504 (7x5 secteurs, Y-2048..-4096); room 163 contient item 119 UZI_AMMO_ITEM X78336 Y-2048 Z27136. La porte circulaire ouvre donc l'acces aux munitions Uzi. flipmap[8] et gfLevelComplete restent a 0. Preuves flyby-state-20261105/ et flip3-rooms-20261106/. Build-gameplay56 SHA256 85783c9a13bc36606f388f557e9521fd66a384690df5ca22f1b3949602905d12; tests 4174 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-05

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-05T23:59:00+01:00. Linux32 provisoire.

Trajan's Markets : item 18 identifie comme RAISING_COG (389), pas HIGH_OBJECT1. GetSwitchTrigger corrige (trigger_index lu apres GetHeight, iteration sur chaque mot) renvoie 3 cibles [36,27,28]; _TestTriggers verrouille correctement TRIGTRIGGER_TYPE tant que IFLAG_TRIGGERED 0x20 est absent; ControlTriggerTriggerer implemente. InitialiseRaisingCog/ControlRaisingCog portes, initialisation croisee rejouee apres InitialiseItem (PortInitialiseRaisingCogs) et retrait de l'objet actif seulement a la fin de l'etape 3 (sinon le cog s'arretait a f0=1). ControlAnimatingSlots/InitialiseAnimatingSlots implementes pour trigger_flags 0/2/333/555 et assignes uniquement a Trajan's Markets pour ANIMATING3_MIP/ANIMATING4 et TRAPDOOR1..3 (l'assignation globale ANIMATING plantait le plan du titre via ANIMATING4). Sequence reelle jouee: poulie 36 -> SPOTCAMS 9, cog f0 0->1->2->3, y 3072->2304, item 27 deverrouillee (f1 1->0), item 28 actif; poulie 27 -> items 11/15/16/17 status=1 active=1 flags=15904, ANIMATING4 frame 62, SPOTCAMS 1; aucun SIGSEGV. flipmap[3], flipmap[8] et gfLevelComplete restent a 0. Preuves cog-init3-20261105/, cog-state4-20261105/ et sequence-real2-20261105/. Build-gameplay56 SHA256 85783c9a13bc36606f388f557e9521fd66a384690df5ca22f1b3949602905d12; tests 4174 PASS. Streets of Rome termine, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-05

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-05T23:59:00+01:00. Linux32 provisoire.

Seconde poulie niveau 2 : traction validée (STATE_LARA_PULLEY 104, anim 339->340, trigger_flags 1->0) mais pas de DoorControl/flyby. Trigger de tuile : SWITCH item 36 (flags 0x3E00) ciblant uniquement item 18 HIGH_OBJECT1 room 24 X74240 Y3072 Z32256. HIGH_OBJECT1 n'a pas de contrôle dans le port, donc inactif et la porte circulaire ne s'ouvre pas. Preuves pulley36-direct5-20261105/ et trig36-20261105/. Build-gameplay48b SHA256 6ed6233a84cb950ba66712b4129e4bfdeb5fc6410ae4480de8cf38c2160dfd59; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-05

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-05T23:59:00+01:00. Linux32 provisoire.

Poulie niveau 2 : la traction déclenche bien le flyby SPOTCAMS 1 (level2-pulley-gear-20261105/). Les cibles du trigger restent inactives (item 11 TRAPDOOR1, item 15/16 ANIMATING6_MIP, item 17 ANIMATING7 : status=0, active=0) faute de routines de contrôle assignées dans le port. Mécanisme d'engrenage partiel : flyby OK, activation des engrenages incomplète. Build-gameplay48b SHA256 6ed6233a84cb950ba66712b4129e4bfdeb5fc6410ae4480de8cf38c2160dfd59; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-05

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-05T23:59:00+01:00. Linux32 provisoire.

Poulie niveau 2 : PulleyCollision (port TOMB4) fonctionnel. item 27 room 33 : Lara STATE_LARA_PULLEY (104), anim 339 GRAB -> 340 PULL, trigger_flags 1 -> 0. Preuve level2-pulley4-20261105/. Trigger de tuile : type spécial 20 + SWITCH item 27 (flags 0x3E00) ciblant item 11 TRAPDOOR1, item 15/16 ANIMATING6_MIP, item 17 ANIMATING7 et TO_FLYBY 1. Preuve trig27-20261105/. Mécanisme d'engrenage activé ; validation visuelle du flyby à faire. Build-gameplay48b SHA256 6ed6233a84cb950ba66712b4129e4bfdeb5fc6410ae4480de8cf38c2160dfd59; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-05

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-05T23:59:00+01:00. Linux32 provisoire.

Niveau 2 : PulleyCollision implémenté (port TOMB4) et assigné à PULLEY. Test item 27 room 33 X81408 Y-2048 Z25088 : Lara entre STATE_LARA_PULLEY (104), anim 339 GRAB, TestLaraPosition=1, trigger_flags=1. Preuve level2-pulley2-20261105/. La transition vers l'anim 340 (PULL) ne se fait pas, donc le trigger d'engrenage (frame +44) n'est pas atteint. Poulie partielle. Build-gameplay48b SHA256 6ed6233a84cb950ba66712b4129e4bfdeb5fc6410ae4480de8cf38c2160dfd59; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-04

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-04T23:59:00+01:00. Linux32 provisoire.

Niveau 2 : porte au crowbar testée. item 0 DOOR_TYPE1 room 0 X81408 Z43520 trigger_flags=2 ; avec crowbar et GLOBAL_inventoryitemchosen=CROWBAR_ITEM, DoorControl(0) est activé (status=1, flags=15904, goal=1). Preuve level2-crowbardoor0e-20261104/. Crash ensuite dans DEL_CalcLaraMatrices_Interpolated_ASM (lara.right_arm.frame_base, animation 403) : état d'animation des bras incomplet, ouverture non validée de bout en bout. Build-gameplay44 SHA256 67ca8a288b0ee76ef93741e22c5ca477d6fd687eedd1bb6582a765be6a18d8cb; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-04

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-04T23:59:00+01:00. Linux32 provisoire.

Niveau 2 Trajan's Markets : trois pickups validés après transition depuis Streets of Rome. LASERSIGHT_ITEM item 19 room 25 X89600 Y-512 Z47616 -> obj 351 (level2-laser2-20261104/). CROWBAR_ITEM item 2 room 1 X89600 Y-512 Z36352 -> obj 240 (level2-crowbar-20261104/). SHOTGUN_ITEM item 115 room 135 X70144 Y0 Z48640 -> obj 338 (level2-shotgun-20261104/). Tous avec L2 LEVEL2 start room=50 et TestLaraPosition=1. Build-gameplay44 SHA256 67ca8a288b0ee76ef93741e22c5ca477d6fd687eedd1bb6582a765be6a18d8cb; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-04

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-04T23:59:00+01:00. Linux32 provisoire.

Niveau 2 : transition depuis le niveau 1 confirmée (room 50) et pickup LASERSIGHT_ITEM validé. item 19 room 25 X89600 Y-512 Z47616 -> AddDisplayPickup(obj=351). Preuve level2-laser2-20261104/ (L2L LEVEL2 start room=50, L2L LASER test=1, L2L PICK obj=351). Build-gameplay44 SHA256 67ca8a288b0ee76ef93741e22c5ca477d6fd687eedd1bb6582a765be6a18d8cb; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets en cours. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-04

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-04T23:59:00+01:00. Linux32 provisoire.

Niveau 2 (Trajan's Markets) chargé et départ vérifié : room 50, X91648 Y0 Z42496, salle X87040 Z38912 (6x6). Preuves level2-start-20261104/level2-start.png et level2-items-20261104/. Objets proches : item 6 REVOLVER_AMMO_ITEM room 2, item 19 LASERSIGHT_ITEM room 25 ; aucun REVOLVER_ITEM dans la salle de départ. Build-gameplay44 SHA256 67ca8a288b0ee76ef93741e22c5ca477d6fd687eedd1bb6582a765be6a18d8cb; tests 4174 PASS. Streets of Rome terminé, Trajan's Markets commencé. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-04

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-04T23:59:00+01:00. Linux32 provisoire.

Transition niveau 1 -> niveau 2 validée : après gfLevelComplete=2 (cutscene 16, Saturn Symbol/FlipMap 8), le gameflow charge Trajan's Markets. Preuve play-level2c-20261104/attempt1.log (L2 LEVEL2) et capture attempt1.png (couloir de pierre, revolver au sol). Streets of Rome est bouclé jusqu'au niveau suivant. Build-gameplay44 SHA256 67ca8a288b0ee76ef93741e22c5ca477d6fd687eedd1bb6582a765be6a18d8cb; tests 4174 PASS. Aucun Done global (campagne TR5 non terminée).

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-04

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-04T23:59:00+01:00. Linux32 provisoire.

Fin du niveau 1 validée par cutscene réelle, sans synthèse : Saturn Symbol (item 94) -> FlipMap(8) -> tuile de sortie de room 171 (X59904 Z69120, room 171 échangée avec 234) -> TO_CUTSCENE 16 (CUT_ANDREA2) -> Load_and_Init_Cutseq(16) -> cutscene jouée -> gfLevelComplete=2. Preuve play-exit16-20261104/ : E16 LOAD num=16, E16 COMPLETE value=2, captures exit-*.png. Correctifs cutscene : input & IN_LOOK au lieu de lara.look, défaut cutseq_num=value. Build-gameplay44 SHA256 67ca8a288b0ee76ef93741e22c5ca477d6fd687eedd1bb6582a765be6a18d8cb; tests 4174 PASS. Streets of Rome terminé. Aucun Done global (campagne TR5 non terminée).

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-04

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-04T23:59:00+01:00. Linux32 provisoire.

Cutscenes PSX débloquées : NeatAndTidyTriggerCutscene utilisait lara.look, forcé TRUE chaque frame par le hack PSXPC, et n'avait pas de défaut cutseq_num=value. Correctifs (input & IN_LOOK, défaut cutseq_num) : TO_CUTSCENE 17 de room 116 (=CUT_ANDREA1) se charge via Load_and_Init_Cutseq(17) et se joue réellement (capture cinématique play-ending-20261104/ending-00.png). 17 n'est pas une cutscene de fin : les cuts qui posent gfLevelComplete (CUT_RICH_CUT_2=26, CUT_JOBY_CUT_3=22, etc.) n'ont aucun TO_CUTSCENE/TO_FINISH dans les 242 salles. Fin de niveau encore non déclenchée par les données explorées. Build-gameplay44 SHA256 67ca8a288b0ee76ef93741e22c5ca477d6fd687eedd1bb6582a765be6a18d8cb; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-03

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-03T23:59:00+01:00. Linux32 provisoire.

Les pickups appellent TestTriggersAtXYZ sur leur tuile. Saturn Symbol (item 94, room 171) : pickup -> AddDisplayPickup(221) + trigger PICKUP avec TO_FLIPMAP 8 -> FlipMap(8), flip_stats[8]=1. Preuve probe-saturn-finish-20261103/. Recherche de fin : balayage des 242 salles avant/après FlipMap(8), aucun TO_FINISH/TO_CUTSCENE ; TO_FLIPEFFECT des rooms 223/225/228 sans finish_level_effect (index 4). Fin de niveau encore non identifiée. Build-gameplay42 SHA256 1b479bb37abc35e481d25dcd91a9330180812a48a7d1599e09a4936310f0e299; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-03

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-03T23:59:00+01:00. Linux32 provisoire.

Saturn Symbol ramassé sans injection : item 94 PICKUP_ITEM2 room 171 X59904 Z71168 -> AddDisplayPickup(obj=221), TestLaraPosition(PickUpBounds)=1 depuis X59954 Z71168. Preuve probe-saturn2-20261103/. La porte 93 (accès) et le trigger de fin de niveau restent à valider ; le pickup seul ne termine pas le niveau. Second pedestal corbeau/colombe item 85 sans trigger à sa tuile. Build-gameplay41 SHA256 962eeb889a44bcff58563ba990d9e9399eb6d08592aa88b6ddbd30ec405a5cbd; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-03

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-03T23:59:00+01:00. Linux32 provisoire.

Switch corbeau/colombe validé : CROWDOVE_SWITCH assigné à CrowDoveSwitchCollision/CrowDoveSwitchControl ; collision + animation + activation, le contrôle shattere le corbeau (mesh_bits=5) et passe l'objet en ITEM_DEACTIVATED pour libérer SwitchTrigger. Item 84 room 165 X58880 Z81408 -> DoorControl(99) DOOR_TYPE6 room 175. Le second pedestal item 85 n'a pas de trigger à sa tuile. Build-gameplay41 SHA256 962eeb889a44bcff58563ba990d9e9399eb6d08592aa88b6ddbd30ec405a5cbd; tests 4174 PASS. Preuve probe-dove84d-20261103/. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-03

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-03T23:59:00+01:00. Linux32 provisoire.

Cloche du temple validée en tir réel : PistolHandler sélectionne aussi les SWITCH_TYPE7/8 dans le cône, PortHitSwitch78 évalue le déclencheur sous la cloche (y-256), GetSwitchTrigger active la porte cible et joue SFX_BELL. Cloche item 75 room 145 Y-9088 -> DoorControl(79) DOOR_TYPE6 room 153. Correctifs : distances de ciblage en 64 bits (débordement 32 bits sur coordonnées lointaines) et boucle ControlActiveItems corrigée (items[item_num] + next_active) qui bouclait à l'infini avec deux objets actifs chaînés. Build-gameplay37 SHA256 ad9db3541c1b008a0378e2a9d1d83f968d09fafe7ad7da1f03f65b8e60a828b4; tests 4174 PASS. Preuves probe-shootbell-final-20261103/. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-02

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-02T23:59:00+01:00. Linux32 provisoire.

Chaîne des deux clés de jardin validée sans injection : pickup PUZZLE_ITEM1 item 36 room 85, usage trou 63 room 124 (PUZZLE_DONE1, inventaire 1→0), pickup item 92 room 170, usage trou 64, ouverture DoorControl(53) et (54). Correctifs : PuzzleHoleCollision appelle TestTriggersAtXYZ avec KeyTriggerActive ; KeyHoleCollision et PuzzleHoleCollision consomment via remove_inventory_item au lieu de DEL_picked_up_object (qui ajoutait). Build-gameplay30 SHA256 ff83f3aafd70c8af9a21fd08ddf31c0e6f2054b8d9f3aed78ffec008de2f0f7d; tests 4174 PASS. Preuve probe-garden2keys2-20261102/. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-02

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-02T23:59:00+01:00. Linux32 provisoire.

Déclencheurs de switch opérationnels : SwitchTrigger implémenté depuis TOMB4, AnimateItem exécute ACMD_KILL et suit jump_anim_num/jump_frame_num, ControlRaisingBlock implémenté et assigné. Validation : item 72 room 139 ouvre DoorControl(71). Chaîne clé d'or validée sans injection : pickup réel KEY_ITEM1 item 107 room 192 (AddDisplayPickup obj=196), retour idle de Lara, insertion au trou de clé item 25 room 59, DoorControl(24) ouvre la grille de la fontaine. Correction lara_as_pickup (gun_status à frame_end-1). Build-gameplay26 SHA256 35fc8facc4a032d5fad2a5e88a5da3dd75d4e4f7d6b418bbb0875a7cf5297e78; tests 4174 PASS. Preuves probe-switch-effect4-20261102/ et probe-goldkey4-20261102/. Le mécanisme item 72 n'est plus qualifié de Mouth of Truth sans preuve. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-02

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-02T23:00:00+01:00. Linux32 provisoire.

Mécanisme Mouth of Truth validé (téléportation de test) : SWITCH_TYPE7 item72 room139 X48640 Z65024, Action → animation de switch, PV restent 1000, grille ouverte et passage à room170 Z67487. room170 est un réduit avec dalle circulaire, sans sortie identifiée. Preuve play-sw72b-20261102/. Reste la route jouée jusqu'au panneau, la clé, le temple et le Saturn Symbol. Build-gameplay22 SHA256 37feac205848424df8c855a31cbb40ed74dc38079060a6f5c0dc54b273879ccc; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Gravité continue des objets : en gravity_status, fallspeed += 6, chute de pos.y, atterrissage sur GetHeight, arrêt de la gravité et mise à jour de salle. Démarrage vérifié. Build-gameplay22 SHA256 37feac205848424df8c855a31cbb40ed74dc38079060a6f5c0dc54b273879ccc; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

AnimateItem traite aussi la commande 2 (gravity_status/fallspeed/speed) et 3 (remise de l'arme de Lara à l'état neutre). Démarrage vérifié. Toutes les commandes connues 1/2/3/5/6 sont maintenant prises en charge ; physique de chute continue non ajoutée. Build-gameplay21 SHA256 c9904bcb4eb304d2c28950736a76e7e8367b6667cb62461722fe69d5deb317bb; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

AnimateItem traite la commande de translation (type 1) via TranslateItem puis mise à jour GetFloor/ItemNewRoom ; types 2/3 sautés. Sons/effets déjà traités. Démarrage vérifié. Build-gameplay20 SHA256 4fa51ce6ab94ffe3451b6f0e4e7ffc08f80067a14a9f913b6d12da90cf3e5232; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

AnimateItem exécute les commandes d'animation 5 (son à une frame) et 6 (effet à une frame) ; type1 translation avance le pointeur sans déplacer l'objet, types2/3 sautés. Démarrage vérifié. Build-gameplay19 SHA256 d093d90605e3906f23eb0a377ea7cebf42780670809e7054f2f4caa7b1d94411; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

AnimateItem utilise désormais GetChange/changes/ranges pour changer d'animation selon goal_anim_state, puis boucle sur frame_end. Les commandes d'animation (sons/effets/translations) ne sont pas encore exécutées. Démarrage vérifié. Build-gameplay18 SHA256 d7e0303ce0b80e5bc37b6aaa0bd0cc1fbcbbe92d36e93d74daca2fd16ece306b; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

AnimateItem de base implémenté : avance frame_number, boucle sur frame_end, suit jump_anim_num si goal_anim_state diffère. Tables de changements/commandes non traitées, donc transitions d'animation partielles. Build-gameplay17 SHA256 2fd240d91a51696933784f2bcc1b4c1e38b1c425f715e8c9311293def87865dd; tests 4174 PASS; démarrage vérifié. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Poursuite et attaque des créatures : LaraBaddieCollision déplace les ennemis intelligents jusqu'à 4096 unités (16 u/frame, GetFloor/GetHeight/ItemNewRoom) et inflige 5 PV/45 frames à moins de 512 unités. Preuve : chien à ~1000 unités rejoint Lara, PV 1000→700 (play-ai3-20261029/). Aucun blocage au démarrage ; l'approche par control/AddActiveItem avait bloqué le splash et a été abandonnée. Créatures sans animation (AnimateItem stub) ni pathfinding. Build-gameplay16 SHA256 7729307bd024561d30a385f9264c543dd8eb81df32457a2a2e5d17dfd41ea638; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Collisions créatures : CreatureCollision pousse Lara hors des bounds, LaraBaddieCollision inflige 5 PV/45 frames à moins de 512 unités avec SFX_LARA_INJURY_RND. Preuve GDB : Lara 1000→825 PV en ~3 s près du chien (tp_dog.out). Ennemis toujours statiques, sans déplacement/attaque. Build-gameplay13 SHA256 12e7474f28f935e15f39fc079b3f228de2716cc041b5b68c35c115f4a6e8aaaf; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Serrure de la fontaine validée : room 59 item25, KEY_ITEM1 injectée, TestLaraPosition=1, Action déclenche l'animation d'insertion et la zone de grille change (play-keygate-20261029/01-before.png et 02-after.png) ; Doberman visible. La clé doit normalement être trouvée plus tard. Route réelle déjà établie : room0→2→59→16/221. Restent : Mouth of Truth/grille, temple, fin de niveau, IA ennemie. Build-gameplay12 SHA256 25386271b61c5e9614844a4a904d84da8b58b791b7acd1a09732b42cd7ef2ca7; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-31T12:00:00+01:00. Linux32 provisoire.

Route réelle sans téléportation : room 0 → room 2 → room 59 (cour de la fontaine, fontaine visible, X55074 Z38072) → room 16 (ruelle sud, grille, X54373 Z44029), avec Right/Up. Autre branche réelle : room 0 → 2 → 11 (Opera Backstage) → 3 → 44. Preuves play-east-fountain-20261029/ et play-courtyard-20261029/. Restent : porte/grille verrouillée, mécanismes, fin de niveau ; IA ennemie absente. Build-gameplay12 SHA256 25386271b61c5e9614844a4a904d84da8b58b791b7acd1a09732b42cd7ef2ca7; tests 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

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
