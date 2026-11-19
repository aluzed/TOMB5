## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

Cause du noir 32 bits au niveau 5 identifiée : le build 32 bits émet trois fois plus de quads que le 64 bits ([PH] 3C=1008 vs 335, nv=7251 vs 3102) alors que les primitives Lara sont identiques — défaut du chemin roomlet 32 bits pour RoomDrawType=2, pas une régression du portage. Le 64 bits rend la scène correctement. La parité 32/64 reste donc mesurée sur le niveau 3 (où elle est byte-identique), et le script check_parity.sh automatise ce contrôle.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

Ajout de scripts/porting/check_parity.sh : lance les builds 64 bits (Vulkan) et 32 bits (OpenGL) sur la scène de référence, compare les BMP et sort en erreur si l’image diffère. Vérifié : 1800 frames → PARITE OK, captures identiques octet pour octet (sha256 63041e5c…, mean_abs_diff=0.000, 307200/307200) ; à 300 frames, un pixel de bord isolé est toléré et signalé. Documenté dans ETAT-64BITS.md et plan §56.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

Costume 6 (Lara des niveaux 4+) : le masquage de meshes du repli L1 est retiré. Le « polygone noir étiré » qui l’avait motivé provenait des bugs de pointeurs LP64 corrigés en RMIG-023. Le modèle complet est vérifié sur les niveaux 4 et 5 (aucun artefact) et la capture de référence du niveau 3 reste identique (63041e5c…). L’override F11 prime désormais sur ce masque pour les diagnostics. Le module LARA6 dédié reste à porter (fonction d’origine requise), et les cinématiques restent bloquées par l’absence de la source de données CUTSEQ.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

Campagne re-validée avec le build Vulkan-only après les correctifs LP64 : niveau 3 (Colosseum) → téléport F9 sur le pickup final (salle 70) → pickup déclenché → chargement du niveau 4 (169 salles, Lara en salle 99), rendu correct, aucun incident. Capture docs/porting/render/colosseum-vers-niveau4.png. Restent pour la campagne le module LARA6 et la source de données des cinématiques.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

Lecteur de cinématique diagnostiqué : le niveau 4 se rend sans écran noir, mais l’intro ne joue pas. handle_cutseq_triggering s’exécute (arme le fondu), Load_and_Init_Cutseq n’atteint jamais init_resident_cutseq et le repli PCopen(\CUTSEQ.JIZ) échoue ; l’image TOMB5.BIN ne contient aucune chaîne CUTSEQ/.JIZ. C’est un blocage de données (source des cinématiques absente du dépôt), pas un manque de code. Reste pour la campagne : module LARA6 et cette source de données. 4188 tests PASS, builds 32/64 verts.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

Vérifications complémentaires : le niveau 5 se charge et se rend en 64 bits/Vulkan (lvl=5, 195 salles, LaraDrawType=6 avec repli L1) — la campagne dépasse donc le Colosseum. Test 8 bits forcé (TOMB5_FORCE_TEXFMT=8) : 99.79 % de pixels identiques entre 32 et 64 bits (résidu de 0.159 niveau, égalités de sampling nearest). Reste pour la campagne : module LARA6 et lecteur de cinématique.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-022 terminé : la copie framebuffer → VRAM (effet mono/sépia) écrit désormais un mot RGB555 conforme au PSX (R bits 0-4, G 5-9, B 10-14) dans les deux backends. Avant, le chemin OpenGL inversait rouge et bleu et le chemin Vulkan utilisait l’alpha pour le rouge. Les captures de référence 32 et 64 bits restent identiques octet pour octet (sha256 63041e5c…, mean_abs_diff=0.000). Backlog rendu : 19 Done, restent RMIG-005 (portage), RMIG-011 (couverture 8 bits), RMIG-015 (RT bloqué, pas de géométrie monde), RMIG-021 (campagne).

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-023 TERMINÉ : la parité 32/64 bits est atteinte sur la scène de référence. Quatre bugs LP64 corrigés : MULFP non tronquée à 32 bits (caméras flyby en positions absurdes), natte et holsters indexés en octets sur `short** meshes[]` (8 octets par pointeur en LP64), et mesh des joints de peau décalé (28 triangles manquants). Résultat : les builds 32 bits (OpenGL) et 64 bits (Vulkan) produisent le MÊME BMP octet pour octet (sha256 63041e5c…, mean_abs_diff=0.000, 307200/307200 pixels identiques) et l’histogramme de primitives de la frame de référence est identique. Écart historique : 18.730 → 0.000. 4188 tests PASS, builds 32/64 verts.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-023 : deuxième série de correctifs LP64. Après MULFP (caméras flyby), deux décalages de pointeurs sur `short** meshes[]` sont corrigés : la natte (s4 + 4 / s1 += 8 shorts valant 2/4 pointeurs sur PSX mais 1/2 en LP64) et les holsters (s0 += 8 sur int* = 32 octets). L’écart 32/64 sur la scène de référence passe de mean_abs_diff=18.730 (26.12 % de pixels à ±8) à **0.225 (99.63 %)** ; la référence 32 bits reste 51d3a1c7… et la 64 bits devient bcc8a642…. Reste 28 triangles 0x34 et 1 0x3C non émis en 64 bits (section armes/back_gun ou seconde boucle de peau). 4188 tests PASS, builds 32/64 verts.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-023 : cause racine corrigée. `MULFP` (multiplication fixe PSX, GETSTUFF.C) n’était pas tronquée à 32 bits en LP64 ; les bits hauts corrompaient la position de spline des caméras flyby (281474976713275 au lieu de 2619), d’où des caméras absurdes dès la frame 30. Après correctif : caméras identiques, meshes de Lara identiques mesh par mesh, écart 32/64 sur la scène de référence ramené de mean_abs_diff=18.730 (26.12 % de pixels à ±8) à 0.314 (99.41 %). La référence 32 bits reste 51d3a1c7…, la référence 64 bits est régénérée (a1f3d3a6…). Reste 35 triangles de la seconde boucle de DrawLaraL1 (peau/stash) non émis en 64 bits. 4188 tests PASS, builds 32/64 verts.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-023 : cause identifiée — la caméra diverge. Les frames 0..32 sont strictement identiques entre 32 et 64 bits (matrices, MatrixStack, caméra, Lara, table `bones` vérifiée sur 160 entrées) ; à la frame 33 le build 64 bits place la caméra ailleurs pendant deux frames puis revient, mais l’historique de lissage reste décalé, ce qui change la matrice de vue, les matrices de Lara et les triangles écrêtés. L’hypothèse « squelette » est infirmée. Prochaine étape : tracer camera.type / UseForcedFixedCamera / TriggerCamera / cutseq_trig autour de la frame 33. Builds 32/64 verts, 4188 tests PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-023 localisé : l’écart 32/64 n’est ni le rendu ni les textures (VRAM identique hors framebuffer) ni les données d’animation (hash identique) ; les inputs de Lara sont identiques (anim/frame/frac) mais la table `bones` diffère et les matrices de joints divergent (~1,7°), ce qui change le nombre de triangles écrêtés. Prochaine étape : auditer les accès à `bones` (tableau d’long hôtes converti depuis les mots 32 bits). Correctif annexe : TOMB5_SKIP_CUTSCENE traité de façon identique en 32 et 64 bits (le bloc GAMEFLOW était sous #if __LP64__). Harnais ajoutés : TOMB5_LARASTATE, TOMB5_LARAMESH, TOMB5_LARABONES. Builds 32/64 verts.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-008 clôturé : l’interface RendererBackend est la seule dépendance du GPU émulé, le build 64 bits est Vulkan-only (sélection par défaut, refus explicite de TOMB5_RENDERER=gl) et le build 32 bits garde l’adaptateur OpenGL comme référence. Vérification de jouabilité en Vulkan : niveau 3, déplacement clavier, Lara passe de la salle 20 à la salle 2 (pos 90642→77925) sans incident, rendu correct.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-19

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-19T23:59:00+01:00. Linux32 provisoire.

RMIG-016 : overlay F12 enrichi avec le profilage par passe (3 timestamps GPU par frame : début, fin de scène, fin de post, relus après fence) et le coût CPU de la frame, plus un budget réglable avec alerte couleur. Relevé en jeu : GPU scène 0.50 ms, GPU post 0.07 ms, CPU 16.80 ms (budget 16.6). Compteurs de rendu et aperçu VRAM brut ajoutés. L’overlay ne construit aucune frame ImGui tant qu’il n’a pas été ouvert (capture de référence inchangée, sha256 63b778f1…). RMIG-023 (effet 0x34/0x62/DR_TPAGE émis seulement en 32 bits) reste ouvert : analyse faite (VRAM textures identiques, seul le contenu rendu diffère).

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-014 : la scène Vulkan est rendue dans une cible hors-écran couleur + profondeur (D32) puis copiée à l’écran par un triangle plein écran (texelFetch). La profondeur par vertex vient des buckets d’ordering table (0=loin, 1=près). Quatre presets de reflets écran dans l’overlay F12 (aucun/faible/moyen/fort) ; le preset « aucun » redonne l’image de référence à l’octet près (5dbbb251… à 1800 frames). Coût négligeable (60 FPS, ~16,5 ms avec le preset fort). Limite documentée : sans normales ni profondeur view-space dans le flux PSX, le SSR physique et le raytracing matériel (RMIG-015, désormais Blocked pour cette raison) ne sont pas réalisables. Builds 32/64 verts, 4188 tests PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-012 terminé : le build 64 bits n’embarque plus OpenGL (ni GLEW, ni libGL, ni symbole gl*), seul le backend Vulkan reste (PORT_VULKAN_ONLY, échappatoire PORT_ALLOW_GL pour diagnostic). TOMB5_RENDERER=gl affiche un message explicite et continue en Vulkan. Rendu inchangé après retrait (capture 300 frames 63b778f1…). Le build 32 bits conserve OpenGL comme référence. La divergence d’état 32/64 bits (primitives d’effet 0x34/0x62/0xE1, fondu d’écran) est extraite dans un nouveau ticket RMIG-023 avec l’analyse déjà faite.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-013 terminé : overlay ImGui (v1.91.5 vendoré) actif par F12 sur le backend Vulkan 64 bits, avec FPS, niveau/salle, position de Lara, animation, vertices/triangles/draws/ordering tables, interrupteur dithering (push constant), sélecteur de profondeur de texture forcée et bouton de capture BMP. Les entrées du jeu sont bloquées quand l’overlay est ouvert (pad + keymap utilisateur) et reprennent à la fermeture ; le rendu reste identique overlay fermé (capture sha256 63b778f1…). Reste : RMIG-012 (retrait d’OpenGL) et RMIG-014/015 (SSR/RT).

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Vulkan devient le backend par défaut du build 64 bits (TOMB5_RENDERER=gl conserve l’ancien chemin, pas de repli silencieux). Vérifié : écran-titre Vulkan, niveau 3 1800 frames Vulkan identique à la référence GL (sha256 5dbbb251…), niveau 3 GL explicite identique à la capture précédente (d05c8394…), niveau 4 Colosseum 600 frames Vulkan sans erreur de validation. Le build 32 bits reste OpenGL. Reste : retrait d’OpenGL/GLEW du build 64 bits, écart 32/64 (primitives d’effet 0x34/0x62/0xE1, ScreenFading).

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Écart 32/64 analysé : le pipeline de couleur n’est pas en cause (le backend Vulkan égale OpenGL au pixel près). Le dump des vertices montre 977 ordering tables identiques (chargement/intro) puis 300 OTs de jeu divergents : le build 32 bits émet un split de texture et ~99 vertices de plus par frame (6 en blend soustractif), et son journal [DRAW] affiche un fondu actif (fade=239/0 fading=1) absent en 64 bits avec persp 306 vs 256. C’est une divergence d’état/effets LP64, suivie dans RMIG-012 ; piste : histogramme des codes de primitives par OT.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Formats de texture et copie framebuffer→VRAM : harnais TOMB5_FORCE_TEXFMT (4/8/16) ajouté ; la scène de référence n’exerce que 4 et 16 bits (pixel-identique), le 8 bits forcé donne 99,82% de pixels à ±8 (résidu = égalités de sampling nearest sur frontières de texel, epsilon aligné dans les deux backends). Emulator_StoreFrameBuffer porté sur Vulkan (copie de l’image présentée vers un buffer hôte par frame + conversion 16 bits identique au chemin GL), ce qui répare l’effet mono/sépia en Vulkan ; la référence reste bit-identique (sha256 5dbbb251…). Anomalie d’ordre des canaux de cette conversion suivie par un nouveau ticket RMIG-022. Builds 32/64 verts.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Parité visuelle atteinte : le backend Vulkan (TOMB5_RENDERER=vulkan) rend la scène de référence niveau 3 (1800 frames) avec une capture octet pour octet identique à OpenGL 64 bits (sha256 5dbbb251…, 307200 pixels, cmp sans différence). Cause de l’écart « bleu vs orangé » identifiée : la capture OpenGL inversait rouge et bleu (glReadPixels RGBA sauvegardé avec les masques SDL BGRA par défaut) ; masques corrigés côté GL et déduits du format de swapchain + alpha opaque côté Vulkan. Autres correctifs : projection en push constant avec conventions Vulkan (y vers le bas, z dans [0,1]), dither retourné verticalement, ids de texture logiques distincts (PORT_TEXTURE_WHITE/VRAM), read_vram/copy_vram sur la VRAM CPU, barrière de layout à la première utilisation des images de swapchain. Nouvelles références déterministes 32/64 : 51d3a1c7… / 5dbbb251…. Reste : format 8 bits non exercé par la scène, écart 32↔64 bits (plus sombre en 64), retrait d’OpenGL. Builds 32/64 verts, 4188 tests PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Vulkan : readback/capture 640x480 BMP opérationnel (Emulator_RequestScreenshot + copie swapchain). La parité avec la référence GL au même état de jeu n’est pas encore acquise : mean_abs_diff=50.4, gain 0.63, 4.08% à ±8, avec une différence d’ambiance (GL bleuté vs VK orangé) à expliquer (fondu/overlay 2D, timing de cinématique ou CLUT). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Vulkan : blit VRAM activé. L’écran-titre (TOMB RAIDER CHRONICLES + menu) et la scène 3D niveau 3 sont rendus sans OpenGL. RMIG-010 Done, RMIG-011 In progress (4 bits + blit validés, 8/16 à vérifier). Projection 512x240 codée dans psx.vert ; capture/readback VK à implémenter.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-010 terminé : pipeline PSX Vulkan (VRAM RG8, vertex buffer, ordering tables/splits, blends, render pass par OT) rend la scène 3D du niveau 3 room 20 avec Lara et le HUD, sans OpenGL. Sampler REPEAT obligatoire pour éviter les bandes. Capture GL de référence inchangée (675e2c8d…). RMIG-011 en cours : shaders SPIR-V 4/8/16 bits/CLUT/dither validés en 4 bits ; restent blit VRAM et perspective. Limites : projection 512x240 codée en dur, capture VK non implémentée, warping des grands polygones pré-existant. Builds 32/64 verts, 4188 tests PASS.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-009 terminé : backend Vulkan intégré (TOMB5_RENDERER=vulkan), fenêtre SDL_WINDOW_VULKAN, instance/device/swapchain 640x480 4 images, présentation d’une image claire (TOMB5_VK_CLEAR=1 -> bleu). Le jeu tourne sans OpenGL (logs [DRAW]/[LARA] actifs). Le chemin GL par défaut reste identique (capture RMIG-007 sha256 675e2c8d…). Builds 32/64 verts, 4188 tests PASS. RMIG-010 (pipeline PSX Vulkan) débloqué.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-009 démarré : smoke test Vulkan autonome (tools/vulkan_smoke.cpp) validé. Instance Vk, surface SDL2/X11, device + queue graphics/present, swapchain 640x480 4 images, render pass clear, 60 frames présentées, sortie propre. Script scripts/porting/vulkan_smoke.sh. Reste : intégrer dans RENDERER_VK.C et brancher le pipeline PSX (RMIG-010/011).

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-008 démarré : interface RendererBackend (RENDERER.H) + adaptateur OpenGL (RENDERER_GL.C). LIBGPU.C utilise g_renderer pour le chemin de rendu (begin/end, blit, texture, blend, vertex buffer, triangles). Capture déterministe après refactor identique à la référence pré-refactor (sha256 675e2c8d…). Builds 32/64 verts, 4188 tests PASS. Reste : déplacer le code GL hors de EMULATOR.C et brancher Vulkan.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

RMIG-007 : harnais déterministe 32/64 opérationnel (TOMB5_FRAMES/TOMB5_CAPTURE, capture puis sortie). Deux runs du même binaire donnent des BMP identiques : 32 bits sha256 083d24a0…, 64 bits sha256 675e2c8d…. État de jeu identique à la capture (Lara pos=(90642,4608,52736) room=20 rot=-16384 anim=103 frame=1611). Écart image 32/64 mesuré : mean_abs_diff=18.730, gain 0.965, 26.12% de pixels à +/-8 ; le 64 bits est globalement plus sombre, HUD compris. Captures et rapport dans docs/porting/replay/. RMIG-007 Done ; RMIG-008 débloqué. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Niveau 4 : LaraDrawType=6, module LARA6 non porte -> Lara invisible. Repli temporaire type 6 -> L1 avec masquage des meshes optionnels pendant le draw (0x80000000) : corps visible, polygone noir etire supprime. Avec TOMB5_START_LEVEL=4 TOMB5_SKIP_CUTSCENE=1, salle 99 chargee et Lara controlable (deplacement mesure). Outils F10 (override draw type via /tmp/tomb5_laradraw) et F11 (override mesh bits via /tmp/tomb5_meshbits). Restent a porter : module LARA6 et lecteur de cinematique (intro niveau 4 noire sans SKIP_CUTSCENE). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

The Colosseum (niveau 3) : fin de niveau atteinte en 64 bits. Outil F9 de teleport runtime (lit /tmp/tomb5_teleport, format x,y,z,room,rot, reinitialise la camera) ; salles 15/90/102 rendues et stables ; pickup final obj220 salle 70 (55808,7936,70144) pris -> transition effective vers le niveau 4 (lvl=4 room=70, 169 salles). Blocage suivant : introduction du niveau 4 sur ecran noir (cutscene non portee), aucune action c ne la fait avancer. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Colosseum 64 bits : disparitions du processus expliquees et corrigees. Reproduit sous gdb : exit code 1 apres PORT_LowAlloc: pool exhausted (16777056 + 1024 > 16777216). Le pool bas de 16 Mio etait sature par des allocations par appel dans ROOMLET1/2/3/4/B (scratchPad 1K + scratchPad2 2K) et ANIMITEM.CalcAllAnimatingItems_ASM (1K par frame) ; le cache statique LP64 existait mais etait dans un #else inatteignable. Correction : allocation unique par pointeur statique local. Validation : reproduction gdb de plusieurs minutes (marche, rotations, animations) sans epuisement ; build 32 bits inchange. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Colosseum 64 bits : clignotement/etirement de Lara corrige. Diagnostic : primitives generees et parsees chaque frame mais bbox ecran alternee ; TOMB5_NO_LARA_INTERP=1 stabilise le modele. Cause racine dans DEL_CalcLaraMatrices_Interpolated_ASM : (1) s0 ecrase par lara_matrices avant la lecture de la translation de frame ; (2) indexation du squelette en short* sur le tableau hote bones (long 8 octets). Correction : m0 separe pour les matrices + b1 long* avec index en mots. Validation : bbox pleine chaque frame, translation stable (-8,155,1295), captures stables, build 32 bits inchange. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Colosseum : outils de saut de cinematique ajoutes (TOMB5_SKIP_CUTSCENE force GLOBAL_playing_cutseq/cutseq_num/cutseq_trig a 0 chaque frame ; TOMB5_START_POS_HOLD=n force START_POS pendant n frames). Avec hold=600, Lara reste en room12 mais le niveau reste en ScreenFade=239/fading=1 sans progression : le start trigger/cinematique garde la main. Les reprises directes en rooms 15/90/102 restent la voie fiable pour tester le rendu. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Colosseum : tentative de reprise en room 12 via TOMB5_START_POS=40448,1023,51712,12,-16384. Lara est bien placee en room12 mais le demarrage/cinematique du niveau la repousse en room14 (y=6144, anim25), meme avec TOMB5_SKIP_CUTSCENE=1 (GLOBAL_playing_cutseq=0, cutseq_num=0, cutseq_trig=0). Les reprises directes en rooms 15/90/102 restent valides et rendues. Pour rejouer le parcours depuis la corniche il faut jouer en 64 bits ou restaurer une sauvegarde 64 bits native ; la compatibilite des sauvegardes 32 bits reste ouverte. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Colosseum : salles cles validees en 64 bits via TOMB5_START_LEVEL=3 + TOMB5_START_POS. Room15 (48640,1024,58880) rendue avec bannieres/colonnes et gladiateur ; room90 (48640,512,70144) rendue avec arene/arches/ciel et Lara visible ; room102 (49664,512,62976) rendue avec porte/serrure. Aucun SIGSEGV, processus stable. Coordonnees extraites du niveau : R15 x=45056 z=53248, R90 x=46080 z=65536, R102 x=48128 z=60416 ; Roman God obj61 item79 room90 (48154,512,69120), pickup final obj220 room70 (55808,7936,70144). Reste parcours/puzzle complet et rendu deforme pre-existant. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-18

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-18T23:59:00+01:00. Linux32 provisoire.

Colosseum : chargement et reprise a la corniche en 64 bits. TOMB5_START_LEVEL=3 charge le niveau 3 (125 salles), decor rendu, Lara deplacable, processus stable. Nouvel outil TOMB5_START_POS=x,y,z,room,rot place Lara apres chargement ; reprise testee en room 12 (43364,768,52325, rot -16384), deplacement Up -> room 14 puis camera room 26, chute volontaire -> GAME OVER attendu (pas de SIGSEGV). Comparaison 32 bits au meme point : sable/grands polygones egalement deformes, donc defaut pre-existant non specifique au 64 bits. Parcours complet du Colosseum reste a derouler (RMIG-021). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Chemin normal valide et Colosseum charge en 64 bits. Parcours menu -> New Game -> cutscene -> niveau 1 : [LARA] type=1 lvl=1 pos=(46592,0,31232), Lara visible, deplacement Up operationnel, F5 ecrit TOMB5.SAV (level 1 room 0 X 46592 Y 0 Z 34346, level data 586 bytes). RMIG-020 passe Done. TOMB5_START_LEVEL=3 charge The Colosseum : 125 salles, [LARA] pos=(90642,4608,52736) room 20, 3897 sommets, decor rendu, processus stable apres deplacement ; sable partiellement deforme et camera parfois face a un mur sombre, parcours complet suivi par RMIG-021. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Chemin normal (menu -> cutscene -> niveau) stabilise en 64 bits. Crashs corriges : div3tab/div4tab tronques en (int)&table[0] dans SubDiv3/SubDiv4 (DrawAllAnimatingItems), copies basses ajoutees ; dword_2C tronque dans sub_658L4, copie basse ajoutee. Le parcours menu -> New Game -> cutscene -> niveau reste vivant ~60 s sans SIGSEGV ; la capture montre le decor mais Lara n est pas visible dans cette phase (camera/cutscene). Le chemin TOMB5_START_LEVEL affiche Lara, permet le deplacement et F5. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Gameplay niveau 1 atteint en 64 bits via TOMB5_START_LEVEL. Cause de l invisibilite de Lara : le loader 32 bits fait un memmove de m_SkinVertNums+480 vers m_ScratchVertNums apres lecture contigue ; en LP64 les deux blocs sont deja copies separement, donc ce memmove ecrasait ScratchVertNums avec des zeros et les sommets skinnes se repliaient sur un point (SXY ~0x008000e7). Memmove guarde par #if !defined(__LP64__). Resultat : decor rendu, Lara visible, deplacement Up operationnel, F5 ecrit TOMB5.SAV (level 1 room 0 X 46592 Y 0 Z 34346, level data 586 bytes), processus stable. Reste : chemin normal menu/cutscene sans le raccourci. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Lara : logique et generation OK en 64 bits, image encore absente. DrawLaraL1 est appele, db.polyptr avance d environ 15 Ko/frame, lara_item->pos=(46592,0,31232), mesh_bits=FFFFFFFF, lara.mesh_ptrs[0] valide et en-tete de mesh identique au 32 bits ; lara_matrices[0] coherente (m00=4095, translations faibles). Les entrees OT de Lara sont indexees en mots 32 bits ((PSX_ULONG*)db.ot + n) au lieu de db.ot+n*8. Les sommets aberrants -32768 viennent du decor (lara=0), pas de Lara. Les 12 premiers GT3 echantillonnes ont des SXY compacts dans les deux builds (008000e7) : il faut instrumenter par mesh (pointeur meshp, nombre de polygones, min/max SXY) pour identifier le corps. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Niveau 1 rendu et chaine Lara atteinte en 64 bits. Corrections : conversion des drapeaux object_info_file vers les bitfields hotes (loaded/intelligent/save_*/HitEffect/undead/save_mesh), sinon objects[LARA].loaded restait a 0 ; tous les scratchpads locaux places sous 4 Gio via une reference de tableau (semantique de tableau preservee) ; DrawSkyMesh lit l entree OT en PSX_ULONG ; S_CalculateLight utilise &scratchPad[21]. Resultat : DrawLaraL1 est appele sans crash, lara.mesh_ptrs[0]/[7] valides et mesh_bits=FFFFFFFF, 4911 sommets generes, 0 primitive non geree, processus stable 40 s. Reste : Lara n apparait pas encore dans l image et la bbox conserve des sommets aberrants (-32768, 1023), probablement dans la transformation/eclairage de ses meshes. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Le niveau 1 s affiche correctement en 64 bits. Cause principale des polygones deformes : 23 occurrences de sizeof(unsigned long) utilisees comme pas de primitive (POLY_GT3/GT4, boucle de copie MISC) valent 8 octets en LP64 au lieu de 4, donc les primitives se chevauchaient et le parseur lisait des UV/couleurs comme coordonnees ecran ([VBAD] quad code=3c v=(8224,32)). Remplacement global par sizeof(PSX_ULONG). Resultat : bbox (-174,-154)-(628,354) au lieu de ±32000, plus aucun [VBAD], capture du niveau 1 montrant correctement le couloir de Streets of Rome avec textures et eclairage (3717 sommets, 111 splits). Reste a valider l avancee de la cutscene et l affichage/controle de Lara en 64 bits. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

La 3D du niveau 1 s affiche partiellement en 64 bits. Corrections supplementaires : matrix_stack/w2v_matrix/phd_mxptr en mots 32 bits ; roomlets lisant x/y/z et left/right/top/bottom par champs nommes ; SubPolyGTLoopRLx recevant directement le pointeur de table ; s6 passe en intptr_t (sauvegarde du curseur de table sans troncature) ; calc_animating_item_clip_window utilise les champs hotes de room_info pour la porte et x/z/minfloor/maxceiling. Mesure : [OT] verts=3717 splits=111, capture avec surfaces bleues visibles. Anomalie restante : bbox des sommets (-32632,-130)-(30848,15472) au lieu de rester dans 0..512 x 0..240, donc une partie des polygones a des coordonnees ecran invalides et la scene reste surtout noire. Prochain pas : comparer SXY/SZ des premiers polygones avec le 32 bits au meme endroit. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Projection 3D 64 bits corrigee. matrix_stack/w2v_matrix/phd_mxptr etaient des long (8 octets) : les ecritures matrix_stack[9] et lectures phd_mxptr[3] n utilisaient plus le meme pas, toute la projection etait fausse ; ils passent en int en LP64. Les roomlets lisent x/y/z et left/right/top/bottom par nom au lieu des offsets int 5/6/7/14/15 dependants du layout LP64. SubPolyGTLoopRLx recoit directement le pointeur de table (plus de t0[0] sur l adresse d un pointeur global) et les appels ne prennent plus &QuadVertTableRLx/&TriVertTableRLx. DrawMeshRL1 est desormais atteint et produit des appels SubPolyGT4RL1 ; le crash restant est dans SubPolyGT4RL1 sur un pointeur de table tronque (0x5572f1fc au lieu de 0x55555572f1fc sous gdb). Ajout de TOMB5_START_LEVEL=n pour demarrer directement un niveau (diagnostic, ~40 s au lieu de ~90 s). Builds 64 et 32 bits verts, tests a relancer. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Niveau 1 atteint en 64 bits. Envoyer les touches en maintenu (keydown/keyup) permet au menu de repondre : New Game lance DoLevel(Name=1) et les lectures CD du niveau se terminent. Trois crashs LP64 corriges : LaSlot alloue sous 4 Gio pour SoundEffect ; InterpolateMatrix_CL utilise directement lara_matrices/lara_joint_matrices sans cast int ; S_DrawPickup chaine l OT pickup en mots 32 bits. Etat : la cutscene d intro reste bloquee sur 'Handle cutseq triggering name: 1' (ecran noir + icone) alors qu en 32 bits la salle s affiche et passe au nom 3 ; le gameplay niveau 1 n est pas encore atteint (RMIG-020). 4188 tests PASS, builds 64 et 32 bits verts, aucune primitive non geree. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Zero primitive non geree en 64 bits. Les structures DR_ENV/DR_MOVE/DR_AREA/DR_TPAGE et les macros de LIBGPU.H utilisaient encore u_long (8 octets en LP64) : sizeof(DR_ENV) valait 128 au lieu de 64, les paquets DR_* desynchronisaient la chaine et le parseur lisait des instructions MIPS (types 0x10/0x8C/0xFC/0xFF). Remplacement de tous les u_long de EMULATOR/LIBGPU.H et LIBGPU.C par PSX_ULONG (32 bits en LP64) et troncature explicite dans setaddr via uintptr_t. Tailles 32/64 identiques : P_TAG 12, POLY_F3 24, POLY_F4 28, POLY_FT3 36, POLY_FT4 44, POLY_GT3 44, POLY_GT4 56, TILE 20, SPRT 24, DR_ENV 64, DR_MOVE 28. Execution 64 bits de 120 s du mode attractif : 0 'Unhandled primitive type', 0 SIGSEGV, 0 stack smashing. Build 32 bits frais vert et execute 40 s sans erreur. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Premier rendu 64 bits stable. Corrections LP64 : objet/statics lus via object_info_file (LEVEL_OBJECT_DATA_SIZE basee sur 64/28 octets de fichier, plus sizeof LP64=96) ; RelocateModule lit des mots 32 bits ; arene LP64 portee a 4 Mio (MAP_32BIT) ; avance de ptr apres conversion des salles ; bones convertis en tableau de long hotes ; GetFrames_CL recoit des tableaux de pointeurs. La trace TOMB5_TRACE_CD est identique aux 32 premieres lignes du 32 bits. Rendu : PSX_ULONG (32 bits en LP64) pour P_TAG/POLY_* ; buffers GPU, tsv_buffer, scratchpads ANIMITEM/ROOMLET*/LIGHT/DRAWOBJ et temp_rotation_buffer alloues sous 4 Gio via PORT_LowAlloc (mmap MAP_32BIT) ; listes stashees indexees par numero ; matrices globales lara_matrices accedees sans cast int ; meshes/bones parcourus avec les pas hotes. Preuve : sizeof(P_TAG)=12 et sizeof(POLY_F3)=24 en 64 bits (identiques au 32 bits) ; execution 64 bits de 35 s du mode attractif sans SIGSEGV avec capture montrant DEMO MODE ; Unhandled primitive type de 702 a 0-77 (suivi RMIG-019) ; 4188 tests PASS ; build 32 bits fraichement configure (build/porting/build32-check) vert et execute 40 s sans crash. Le hash b9d8e710 n'est pas reproductible depuis un autre repertoire de build (chemins DWARF), la non-regression est couverte par le build frais, l'execution et les tests. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Diagnostic 64 bits: le header de niveau est deja corrompu avant LoadLevel. Instrumentation temporaire (retiree, arbre revenu a HEAD, hash 32 bits b9d8e710 restaure): en 64 bits, S_LoadLevelFile Name=0 puis '[LVL] header ver=-225 numRooms=116 numAiModules=5 numLevelItems=38 anims=576'; objectVersion=-225 (0xFFFFFF1F) n'est pas une version valide, donc le header du niveau est lu au mauvais endroit. La divergence est dans S_LoadLevelFile avant LoadLevel: (1) DEL_CDFS_OpenFile(Name+TITLE) positionne cdCurrentSector a partir de gwLba + (gwHeader.entries[filenum].fileOffset >> 11); (2) DEL_CDFS_Read(mod, gwHeader.entries[NONE].fileSize) lit le SETUP.MOD; (3) LoadLevel lit sizeof(struct Level) = 228 octets, identique dans les deux ABIs. struct GAMEWAD_entry/GAMEWAD_header sont en pragma pack(1) et ne contiennent que des int, donc leur layout ne change pas; les suspects restants sont en amont dans la sequence CD du demarrage (lecture du gameflow, InitNewCDSystem, position du GAMEWAD) qui diverge entre 32 et 64 bits. Prochain test cible: imprimer gwLba, gwHeader.entries[5].fileOffset, gwHeader.entries[NONE].fileSize et cdCurrentSector juste avant la lecture du header dans les deux binaires; si l'entree GAMEWAD differe la lecture du GAMEWAD est en cause, sinon c'est la position CD heritee du gameflow. Etat: 32 bits vert et hash inchange, 64 bits vert mais echec au chargement (702 'Unhandled primitive type' avant le SIGSEGV). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Sonde CD sur le chargement 64 bits (instrumentation temporaire de DEL_CDFS_Read, CdControlB(CdlSetloc) et CdReadSync, retiree ensuite, arbre revenu a HEAD). En 64 bits, chargement du niveau titre (Name=0): Setloc sector=2492 off=5861184 fseek=0 ftell=5861184, CdReadSync fread=1 pos=5863536, DEL_CDFS_Read addr=0x555555755d60 size=1920, puis 'copied 1920 bytes dst=00000000 src=00000000'. Le seek et le fread reussissent mais les donnees du secteur sont nulles: src (buffer de pile) est deja a zero, donc ce n'est ni un probleme de pointeur ni de layout. En 32 bits, sur la meme session, aucun 'copied' n'apparait: aucune lecture non multiple de 2048 octets n'a lieu, donc le bloc if (level->numAiModules != 0) n'est pas execute, autrement dit le niveau titre se charge avec numAiModules == 0 en 32 bits et == 5 en 64 bits. Conclusion: la lecture CD n'est pas cassee, c'est le chemin de chargement du niveau titre qui diverge avant ce point (les deux binaires ne lisent pas la meme chose) et en 64 bits la table demandee tombe sur une zone nulle de l'image. Prochaine investigation: comparer pas a pas la sequence de DEL_CDFS_Read/Setloc des deux binaires pendant S_LoadLevelFile(Name=0) pour trouver la premiere divergence de position. Etat: 32 bits vert avec hash b9d8e710 restaure, 64 bits vert. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

RMIG-017 en cours: ajout au chemin LP64 de LoadLevel (chemin 32 bits intact) de struct anim_struct_file (40 octets, frame_ptr 32 bits, static_assert) converti vers anims[] avec frame_ptr = frames + offset, de struct item_info_file (144 octets, data en adresse 32 bits, static_assert) converti vers items[256] avec les drapeaux actives/status/ai_bits deplies bit par bit depuis le mot 32 bits du fichier (un bitfield n'a pas d'adresse), de la conversion de meshes[] (tableau 32 bits du fichier vers tableau de pointeurs hotes base mesh_base + offset), et de relocationPtr type psx_i32* car en long* chaque champ de la table de modules etait lu sur 8 octets ce qui donnait des tailles et offsets nuls. Builds 32 et 64 bits verts, hash 32 bits INCHANGE b9d8e710. Resultat mesure: le chargement 64 bits depasse meshes/anims/items et s'arrete maintenant dans RelocateModule avec ptr == ptr2 == 0x4019724c (deux allocations de taille 0) alors que level->numAiModules=5 et aiModuleIndices[0]=15 sont corrects et que relocationPtr[0..4] valent tous 0: la lecture des 1920 octets de la table de modules (DEL_CDFS_Read dans tsv_buffer[256]) ne remplit pas le buffer. C'est le prochain point a instruire (positionnement CD vs lecture), pas un probleme de layout. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

RMIG-005 en cours: deux mecanismes supposaient des adresses 32 bits. (1) Arene de jeu sous 4 Gio: MALLOC.C alloue malloc_buffer par mmap(MAP_32BIT) en LP64 (allocation statique inchangee en 32 bits), ce qui garde valides les adresses 32 bits stockees dans les blocs reloges; malloc_buffer devient char* en LP64 avec un acces conditionnel dans MALLOC.H. (2) Format fichier des salles: struct room_info_file (80 octets, pointeurs en psx_u32) avec static_assert, et LoadLevel lit ce format puis convertit champ par champ vers struct room_info sur le chemin LP64, les blocs etant relocalises depuis leur position dans le fichier. (3) Reste a faire et mesure: le binaire 64 bits plante desormais dans LoadLevel a GAME/SETUP.C:1838 sur '((int*)&meshes)[i] += (int)mesh_base + ...', premiere d'une famille de 487 occurrences de '(int*)&' dans GAME/ et SPEC_PSXPC_N/ qui traitent des tableaux de pointeurs comme des tableaux d'int; en LP64 l'element fait 8 octets donc lecture/ecriture fausses et corruption memoire. Ce reste est decoupe dans un nouveau ticket RMIG-017 (relocalisation 64 bits des tableaux de pointeurs issus du fichier: meshes, frame_ptr, models avec un helper base+offset 32 bits), critere de sortie: niveau charge en 64 bits sans SIGSEGV et sans 'Unhandled primitive type', positions d'items identiques a la reference 32 bits. Builds: 32 bits vert et hash INCHANGE b9d8e710, 64 bits vert (compile) mais plante au chargement. Backlog rendu: 5/17 Done, 1 In progress, 11 Blocked. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

RMIG-004 termine: GAME/TYPES.H converti en types a largeur fixe. Les typedefs psx_i32/psx_u32 (int32_t/uint32_t) sont desormais definis dans GAME/TYPES.H (inclus par STYPES.H) et les 148 long + 14 unsigned long du fichier sont convertis (PHD_VECTOR, PHD_3DPOS, FLOOR_INFO, LIGHTINFO, MESH_INFO, OBJECT_VECTOR, SPOTCAM, lara_info, savegame_info...). static_assert sur les structures sans pointeur: PHD_VECTOR 12, PHD_3DPOS 20, FLOOR_INFO 8, LIGHTINFO 32, MESH_INFO 20, OBJECT_VECTOR 16, SPOTCAM 40, donc le format PSX est preserve en 64 bits. Correction induite: UpdateLightning (GAME/CONTROL.C) parcourait les points avec un long* -> type psx_i32*. Resultats: build 32 bits vert avec hash INCHANGE b9d8e710 (aucune regression), build 64 bits vert; le binaire 64 bits rend toujours correctement l'ecran de demarrage mais conserve environ 594 'Unhandled primitive type' en 20 s, ce qui montre que le rendu 2D/sprite passe mais que le flux 3D reste mal interprete. Conclusion: le prochain levier n'est plus le typage des structures de jeu mais la lecture du format fichier, car LoadLevel caste le buffer de salles directement en struct room_info qui contient cinq pointeurs (8 octets en LP64) et decale tous les champs suivants: c'est RMIG-005 (structure de format a pointeurs 32 bits + conversion). Backlog rendu: 5/16 Done, RMIG-005 passe en Todo. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

RMIG-003 termine: SPEC_PSXPC_N/STYPES.H converti en types a largeur fixe. Ajout de typedef int32_t psx_i32 et uint32_t psx_u32 et conversion des champs (seul long restant: les pointeurs de DB_STRUCT, structure hote de buffers hors donnees PSX). static_assert de layout valables toutes ABI pour les structures sans pointeur (DRIP_STRUCT 24, TEXTURE 16, static_info 28, REQUESTER 20, ITEM_LIGHT 48) et seulement hors LP64 pour room_info 80, ITEM_INFO 144, object_info 64, creature_info 228 car elles embarquent des pointeurs hotes: consequence de conception retenue pour RMIG-004/005, il ne faut pas forcer sizeof sur ces structures mais lire le format fichier via une structure dediee a pointeurs 32 bits et convertir au chargement. Resultats mesures: build 32 bits vert (0 erreur) avec binaire de hash INCHANGE b9d8e710 (reference intacte); build 64 bits vert (0 erreur) produisant un ELF64 qui affiche desormais correctement l'ecran de demarrage Tomb Raider Chronicles (capture) et ne declenche plus l'assertion ParsePrimitive, avec 507 'Unhandled primitive type' en 20 s qui relevent de RMIG-004 (TYPES.H). Backlog rendu: 4/16 tickets Done, RMIG-004 passe en Todo. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

RMIG-002 et RMIG-006 termines: cible 64 bits operationnelle et 16 erreurs de compilation -m64 corrigees. Configuration reproductible via scripts/porting/configure64.sh (pas de -m32, SDL2 x86-64 systeme, GLEW 64 bits compile depuis les sources vendored avec -DGLEW_NO_GLU car libglu1-mesa-dev absent); build complet vert et binaire ELF 64-bit LSB pie executable avec ldd entierement x86-64. Corrections de portabilite: collision de macro B de GTEREG.H avec les parametres de DIVFP/MULFP (renommes X/Y dans SPEC_PSXPC_N/GETSTUFF.H), includes manquants ajoutes (SWITCH.C: SPHERE.H+NEWINV2.H; NEWINV2.C: SPOTCAM.H+LARAFIRE.H; OBJLIGHT.C: GETSTUFF.H; COLLIDE.C: DRAW.H). Premiere execution du binaire 64 bits: demarrage (init emulateur, audio, video) puis arret sur l'assertion ParsePrimitive (EMULATOR/LIBGPU.C:1141) avec des 'Unhandled primitive type: 10/08/07/06/05', signature d'un decalage de layout dans le flux de paquets GPU, ce qui confirme l'ordre RMIG-003 -> RMIG-005 (conversion des structures PSX) plutot qu'un ajustement du parseur. Aucune regression 32 bits: arbre recompile vert (0 erreur) et binaire de hash inchange b9d8e710. Backlog rendu: 3/16 tickets Done. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Plan de migration du rendu decoupe en tickets vivants: creation de docs/porting/render-backlog.json (16 tickets RMIG-001..RMIG-016) avec schema complet (objectif, faits, perimetre, taches, criteres d'acceptation, validation, inconnues, estimation, confiance, dependances, references verifiees, avancement, preuves), rendu par scripts/porting/render_tickets.py vers docs/porting/render/index.html (tableau de statut) et une fiche par ticket, plus docs/porting/render-README.md. Regles: statuts Todo/In progress/Blocked/Done, dependances sans cycle, et un ticket ne passe Done qu'avec une entree evidence datee. RMIG-001 (etude 32 vs 64 bits du raytracing Vulkan) est Done avec preuve: sonde Vulkan -m32 = 233 extensions sans aucune extension RT sur la RTX 2080 Ti, -m64 = 248 extensions avec VK_KHR_acceleration_structure, ray_query, ray_tracing_pipeline et VK_NV_ray_tracing; llvmpipe expose le RT dans les deux cas (logiciel). Chaine: RMIG-002 (cible 64 bits sans GLEW) -> RMIG-003 (typedefs STYPES.H) -> RMIG-004 (TYPES.H) -> RMIG-005 (code des champs convertis); RMIG-002 -> RMIG-006 (pointeur<->entier, 4 fichiers en erreur -m64) -> RMIG-007 (harnais de comparaison 32/64); RMIG-002 -> RMIG-008 (abstraction renderer) -> RMIG-009 (Vulkan base) -> RMIG-010 (pipeline PSX) -> RMIG-011 (SPIR-V) -> RMIG-012 (parite + retrait GL), RMIG-013 (ImGui F12), puis RMIG-014 (SSR a presets) -> RMIG-015 (RT avec repli SSR) et RMIG-016 (debug avance). Tests ajoutes: tests/porting/test_render_backlog.py (schema, dependances, preuves des tickets Done, non-derive des fichiers generes, coherence des compteurs). Aucun code de rendu modifie. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Cap valide: migration 64 bits puis backend Vulkan (remplacement d'OpenGL), overlay ImGui toujours compile avec bascule F12, puis reflets SSR a presets et raytracing materiel. Justification mesuree: sonde Vulkan compilee -m32 et -m64 sur la machine cible (RTX 2080 Ti, driver 580.178, Vulkan 1.4.312); en 32 bits le GPU expose 233 extensions SANS aucune extension RT (pas de VK_KHR_acceleration_structure, ray_query ni ray_tracing_pipeline) tandis qu'en 64 bits il en expose 248 avec toutes les extensions RT plus VK_NV_ray_tracing et VK_NV_ray_tracing_invocation_reorder; llvmpipe expose le RT logiciel dans les deux cas (hors temps reel). Inventaire de compilation -m64: sur 200 fichiers GAME/ seulement 4 sont en erreur (COLLIDE.C 7 erreurs dont EMULATOR/GTEREG.H:33 et anims non declare; SWITCH.C 5 dont TestCollision/GLOBAL_inventoryitemchosen/GLOBAL_enterinventory; NEWINV2.C 3 dont LaraGun/bUseSpotCam/bTrackCamInit; OBJLIGHT.C 1 GetFloor), et ~995 occurrences de 'long' dans GAME/*.C et SPEC_PSXPC_N/*.C avec 52+39 long/unsigned long dans STYPES.H et 148+14 dans TYPES.H (risque principal: layouts des structures PSX relogees). Plan ecrit dans docs/porting/vulkan-64bit-plan.md: etapes A types a largeur fixe dans les structures PSX avec static_assert sur les tailles, B code manipulant ces champs plus les 4 fichiers en erreur, C conversions pointeur<->entier vers uintptr_t, D cible CMake 64 bits sans GLEW (SDL2 systeme, loader Vulkan 64 bits), E backend Vulkan reprenant le modele existant (VRAM 1024x512 en une texture RG, VBO dynamique, un draw call par passe d'ordering table, pas de depth, blending PSX, shaders gte_shader_4/8/16 et blit_shader portes en SPIR-V), F ImGui F12, G reflets SSR a presets puis RT materiel derriere detection d'extension avec fallback SSR. Aucune modification de code de rendu effectuee a ce stade. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Precision sur l'invisibilite de Lara dans la zone de la corniche: InDrawRoom n'est JAMAIS ecrit dans le port (declare dans STYPES.H, aucune affectation), donc la valeur 0 observee ne prouve rien. Les conditions reelles de rendu (SPEC_PSXPC_N/DRAWPHAS.C:382) sont objects[LARA].loaded && !(lara_item->flags & 0x40) puis lara_item->mesh_bits != 0 && SCNoDrawLara == 0 puis switch (LaraDrawType). Mesures sur la sauvegarde corniche (room 12, position hors grille): SCNoDrawLara=0, lara_item->flags=0x0, mesh_bits=0xFFFFFFFF, bUseSpotCam=0, current_spline_camera=2, donc toutes les conditions de rendu sont reunies et pourtant Lara n'apparait pas (verifie en zoomant et en poussant la luminosite x3: que du sol). En partie normale (niveau 1, position issue d'une sauvegarde F5) Lara est parfaitement rendue. La difference est donc bien la position de sauvegarde invalide (hors grille de la room 12) qui alimente le pipeline de matrices de Lara. Conclusion operationnelle inchangee: jouer depuis une nouvelle partie et sauvegarder avec F5. Documentation mise a jour dans docs/porting/colosseum-walkthrough.md section 6. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Chaine de demarrage confirmee en conditions reelles (captures a l'appui): titre en attract-mode -> 'c' -> cinematique d'intro (Lara derriere des barreaux) -> flyby du niveau 1 (camera haute, Lara minuscule au fond) -> gameplay avec camera derriere Lara et controles actifs; 'Handle cutseq triggering name: 1' confirme l'execution du niveau 1 et un Up de 2 s deplace Lara dans la ruelle (verifie sur capture). F5 produit alors une sauvegarde valide (level 1 room 2 46592,0,35779), conservee comme reference dans /tmp/opencode/TOMB5.valid_level1.sav. La campagne est donc jouable depuis une nouvelle partie, avec des points de reprise fiables produits par le moteur, ce qui rend caduque la pratique des sauvegardes patchees a la main. Documentation ajoutee dans docs/porting/colosseum-walkthrough.md section 8. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Decouverte majeure pour le test manuel: dans les menus la validation est la touche 'c' (action/confirm) et non 'x'. EMULATOR/INPUTMAP.C mappe { action, confirm, INPUTMAP_IN_ACTION, INPUTMAP_RAW_CROSS } et { jump, jump, INPUTMAP_IN_JUMP, INPUTMAP_RAW_SQUARE }; les menus testent RawEdge & IN_CROSS (0x4000) donc seule l'action valide, 'x' ne produit que le bit Square et ne valide rien. Recette verifiee en conditions reelles: lancer sans TOMB5_AUTOLOAD, appuyer sur 'c' au titre (plusieurs fois a ~4 s d'intervalle car le titre joue une attract-mode pendant laquelle les entrees sont ignorees via title_controls_locked_out); le niveau demarre (Handle cutseq triggering name: 1) et Lara est visible, camera derriere elle, controles clavier fonctionnels (Up avant, Left/Right rotation, x saut, c action). Verification F5: la sauvegarde produite par le moteur est coherente avec la salle ([SAVE] wrote TOMB5.SAV: level 1 room 2 X 46592 Y 0 Z 35779, level data 586 bytes), contrairement aux positions patchees a la main qui peuvent etre hors grille (camera dans une autre salle, Lara culled, cf. section 6). Cela confirme que l'invisibilite observee dans la zone de la corniche est un artefact de sauvegarde patchee: en niveau 1 avec une position valide Lara se dessine parfaitement. Documentation ajoutee dans docs/porting/colosseum-walkthrough.md section 8. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, FixedCamera porte: GAME/CAMERA.C remplace le stub UNIMPLEMENTED() par la version de camera.cpp (camera fixe pilotee par UseForcedFixedCamera ou camera.fixed[camera.number], suivi de cible, MoveCamera(&ideal,1), decrement de camera.timer). C'etait un blocage fonctionnel reel: CalculateCamera appelle FixedCamera() des que camera.type != CHASE_CAMERA, et le stub laissait la camera figee sur sa position precedente (vue statique, Lara hors champ/non dessinee); or la salle 12 porte un trigger CAMERA(0). Includes ajoutes: TOMB4FX.H (FlashFader/DoBloodSplat), DEBRIS.H (ShatterObject), SPOTCAM.H (SniperOverlay). Limite assumee et documentee: le sous-bloc sniper (fixed->flags & 2) n'est pas porte car il depend de TriggerRicochetSpark, DoBloodSplat et ShatterObject, absents du port PSX (TriggerRicochetSpark n'existe que sous PC_VERSION et y est un stub); aucun camera item de ce niveau n'utilise le mode sniper. Validation: corniche 201 frames OK, camtype=0, camera mobile, 4183 tests PASS. Mesure associee: sur la corniche la camera se resout en room 8 (salles empilees) et Lara (room 12) n'est pas dans la liste de rendu - limite de geometrie independante de ce port, documentee section 6 de colosseum-walkthrough.md. Build-gameplay59 SHA256 b9d8e710fcbc4ba3d9bb09310e809ae92384829cfa0ffb02324dd27688d5771e. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, KlaxonTremor porte: GAME/CONTROL.C remplace le stub par la version de joby.cpp (klaxon periodique SFX_KLAXON toutes les 512 frames, tremblement de camera par impulsions camera.bounce declenche aleatoirement apres 450 frames, avec les deux compteurs static timer et bounce du code d'origine). Un stub de moins parmi les fonctions appelees chaque frame. Validation: corniche 201 frames OK, aucun SIGSEGV, 4183 tests PASS; le test tests/porting/test_stub_diagnostics.py a ete mis a jour car KlaxonTremor n'est plus un stub. Note: UpdateFireSparks n'a pas ete porte car le sous-systeme associe est entierement absent du port (fire_spark[20] est declare mais jamais ecrit: il faudrait porter TriggerFireFlame/GetFreeFireSpark/keep_those_fires_burning et le rendu, soit un sous-systeme complet). Build-gameplay59 SHA256 95bdcc4f207cdf7041837630023d863d65b3dd2c92ab6622faa9bdab214cd423. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Bilan du diagnostic 'retour au titre apres chargement': avec des sondes temporaires instrumentees (printf [LEVEL] et CPRET avec fflush, retirees ensuite, arbre revenu a HEAD) le niveau 3 se lance et tourne ([LEVEL] check name=3 entry=5 nEntries=51 size=2711580 puis [LEVEL] post-initial ControlPhase status=0 gameMode=0 level=3 complete=0, et 'Handle cutseq triggering name: 3' en boucle). Les observations precedentes de 'retour au titre' correspondent a des echantillonnages trop precoces pendant le chargement (le chargement du niveau prend plus de 10 s apres [EMU] Initialising) et a la bufferisation de stdout, pas a une sortie du niveau. Egalement verifie: Gameflow->DemoDisc=0 et InputTimeout=18000 (pas de timeout de demo), gfScriptOffset[3]=187 pointe sur GF_KEY_ITEM1=0x92 (debut de preambule de bloc, normal), l'entree GAMEWAD du niveau 3 existe. Note de reproductibilite: apres nettoyage, la recompilation donne MAIN SHA256 b59fa0a336cd9653724838bb3f16eab04050863092061ed76ecbeaf958ba7b0f au lieu de 2b2b6dc2 a source identique, car l'archive EMULATOR/libPSX.a est reassemblee a la main (ar r) et ses metadonnees ne sont pas reproductibles; comportement verifie identique (corniche 201 frames OK, 1493 lignes de log). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, point ouvert documente: un chargement de sauvegarde ressort au titre. Reproduit avec une sauvegarde appliquee en room 12 (40448,1023,51712): le niveau 3 est bien lance puis, en quelques frames, retour au titre. Traces instrumentees: FL DoTitle Name=0 status=0 complete=0 currentLevel=0 gameMode=1; FL DoLevel Name=3 gfCurrentLevel=3 gameMode=4 fromTitle=1; FL DoTitle Name=0 status=1 complete=0 currentLevel=0 gameMode=0. DoLevel(3) est donc appele correctement (gfGameMode=4 = chargement) puis ControlPhase renvoie 1: DoGameflow reinitialise (gfInitialiseGame=1, gfCurrentLevel=0) et rappelle DoTitle. Elimine par mesure: reset_flag jamais ecrit (watch reset_flag ne declenche pas); gfLevelComplete jamais ecrit (watch ne declenche pas); Gameflow->DemoDisc=0 et InputTimeout=18000 donc ce n'est pas le timeout de demo de ControlPhase. Restent les autres return 1 de ControlPhase (menu pause, S_Death(), ou une branche de demo_mode). A trancher avec un point d'arret pose sur les sites return 1 dans la boucle in-level; attention la table de lignes de CONTROL.C est decalee dans gdb (break CONTROL.C:1291 retombe sur la ligne 1642), utiliser les compteurs de fonction plutot que les lignes. Piste prioritaire: lara.death_count > 90 -> S_Death() si la sauvegarde restaure un death_count incoherent. Documentation ajoutee dans docs/porting/colosseum-walkthrough.md section 7. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, invisibilite de Lara dans la zone de la corniche expliquee: observation en capture (on voit le decor et l'ombre de Lara mais pas Lara; la camera avance quand on marche, donc les entrees fonctionnent). Mesures gdb: lara_room=12 mais draw_room=0 et InDrawRoom=0, mesh_bits=0xffffffff, camera.pos.room_number=8, cam_type=0 (CHASE), flip=0. La camera se resout dans la room 8 (GetFloor sur la position camera, au-dessus de Lara dans un empilement de salles) tandis que lara_item->room_number vaut 12: la salle de Lara n'est pas dans la liste de rendu, elle est culled et seule son ombre reste. La cause est la sauvegarde: position hors de la grille de cellules de la room 12 (x=43364 alors que la grille s'arrete a 43008); le moteur le montre au chargement ([SAVE] applied saved position: room 26 X 40448 Y 1024 Z 51712 quand on tente une position dans la room 12 a y=1024). GetFloor a (40448,y,51712): y=1024 -> room 26; y=1023 -> room 12; y=768 -> room 12: la dalle de la corniche est franchie des qu'on est pile a sa hauteur (y >= floor), c'est le pit_room qui prend le relais. Consequence pratique: ne pas patcher une sauvegarde a la main dans cette zone (position hors grille => camera dans une autre salle => Lara invisible); jouer depuis un point valide et faire un F5 en jeu pour obtenir une position coherente avec la salle. Documentation ajoutee dans docs/porting/colosseum-walkthrough.md section 6. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Diagnostics des stubs appeles a chaque frame: plusieurs fonctions non portees sont invoquees par frame (UpdateFireSparks, UpdateGunShells, UpdateRats, UpdateBats, KlaxonTremor, ProcessClosedDoors, WadeSplash cote jeu; PadSetActAlign et PadStartCom cote emulateur) et leur UNIMPLEMENTED() imprimait une ligne par frame, rendant les logs illisibles (9050 lignes / 320 Ko pour 200 frames) et coutant un printf par frame dans la boucle de controle. Ajout de UNIMPLEMENTED_ONCE() dans SPEC_PSXPC_N/SPECIFIC.H et EMULATOR/EMULATOR.H (meme message prefixe '(once)') et utilisation a ces neuf emplacements; le comportement (no-op) est identique, seule la diagnostique change. Mesure sur la sauvegarde corniche 201 frames: chaque message apparait une seule fois (WadeSplash 1, UpdateFireSparks 1, ProcessClosedDoors 1, UpdateGunShells 1, PadSetActAlign 1) et le log passe de 9050 lignes / 320 Ko a 1617 lignes / 54 Ko (-83%). Corniche 201 frames OK. Regression verrouillee par tests/porting/test_stub_diagnostics.py. Build-gameplay59 SHA256 2b2b6dc2ced7f6e9dd4b87d45782583f78a743bf2a079e9fea8496864bf3c85c. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, ControlRollingBall porte: GAME/TRAPS.C remplace le stub par la version de traps.cpp (gravite et fallspeed, rebonds amortis, sondage de sol a +/-128 et +/-512 autour de la bille via GetFloor/GetHeight, correction de vitesse item_flags[0]/[1], camera.bounce selon la distance, reorientation progressive phd_atan_asm, _TestTriggers pour les declencheurs sous la bille). GAME/SETUP.C assigne ROLLINGBALL (control, RollingBallCollision, save_position, save_flags). Includes ajoutes a TRAPS.C: MATHS.H (phd_sqrt_asm/phd_atan_asm) et COLLIDE_S.H (ItemNewRoom, declare sous PC_VERSION seulement dans ITEMS.H). Validation runtime (item 23 force actif, OCB 0): pos initiale 7680,-1280,75264; n=20 pos=7680,5676,91152 f1=3072 fall=53; n=40 pos=7680,6912,92672 f1=21 fall=0; puis inchange (bille arretee). La bille tombe, roule et s'arrete; 200 frames sans SIGSEGV. 4181 tests PASS. Build-gameplay59 SHA256 513472275916c1390736ebddb6953147d729c3b8d275c51adfe6f8e3c3935a47. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, ControlScaledSpike porte: GAME/TRAPS.C remplace le stub par la version de traps.cpp (extension/retraction pilotees par item_flags[0]/[1], TestBoundsCollideTeethSpikes, degats 8 PV glissants, mort si chute ou dents sorties selon trigger_flags & 7, gerbes de sang TriggerBlood, animation de mort dediee ANIMATION_LARA_SPIKED + STATE_LARA_DEATH). GAME/SETUP.C: TEETH_SPIKES recoit InitialiseScaledSpike (deja porte) et ControlScaledSpike avec save_flags; le rendu reste le chemin standard (pas de DrawScaledSpike) car assigner le stub actuel imprimerait un UNIMPLEMENTED par frame sans rien dessiner, alors que le rendu standard affiche au moins le maillage. Validation runtime (sauvegarde corniche, item 104 force actif): handlers non nuls, item identifie obj=117 room=124 ocb=36, 200 frames sans SIGSEGV, lara_hp inchange (Lara a l'autre bout du niveau). Avec l'OCB 36 (bit 32) les dents restent rentrees (f2=1), comportement attendu de cette variante. 4181 tests PASS. Build-gameplay59 SHA256 fc1576c71a62171a8c168654e0c802d0624530e293fd969453b75974c2e4ade1. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

Selection de niveau, chemin de code verifie: dans TitleOptions (SPEC_PSXPC_N/TITSEQ.C) branche MENU_LEVEL_SELECT_MENU, byte_46 est l'entree courante bornee a [0, Gameflow->nLevels-2] et sur IN_CROSS le code fait gfLevelComplete = byte_46 + 1; byte_46 = 0; ret = 3. Dans DoGameflow (GAME/GAMEFLOW.C) branche GF_TITLE_LEVEL, avec gfStatus == 3 il fait gfCurrentLevel = gfLevelComplete ET repositionne le pointeur de script gf = &gfScriptWad[gfScriptOffset[gfCurrentLevel]], donc la mecanique de saut de niveau est complete. Le defaut restant est donc en amont dans l'entree de menu: soit byte_46 n'est pas initialise a l'ouverture de MENU_LEVEL_SELECT_MENU (il est reutilise par le menu de chargement et remis a 0 a plusieurs endroits), soit la navigation IN_DPAD_UP/DOWN n'incremente pas pendant la fenetre de RawEdge. Verification en jeu tentee: la navigation clavier fonctionne dans le menu principal (New Game -> Special Features se deplace), mais sous gdb la cadence tombe a ~0,5 fps et un x sur Special Features declenche le DEMO MODE avant que le sous-menu ne s'affiche; watch gfCurrentLevel n'a enregistre aucune bascule. Le point demande une passe manuelle (menu -> Special Features -> Level Select). Aucun correctif speculatif applique. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, comportement mesure au bord de la corniche (sauvegarde 43364,768,52325, y_rot=-16384): (1) saut sur place (IN_JUMP seul) donne state=28 JUMP_UP avec y 768 -> 14 -> 768, retour exact au point de depart, speed=2 (aucune avance horizontale); (2) saut+avant (IN_FORWARD|IN_JUMP) donne state=14 GRAB_TO_FALL puis retour state=2 au meme endroit: le rebord est agrippable et Lara s'y raccroche; (3) marche seule: arret net a x=43109, bord de la grille de la room 12 (x_size=5, fin a 43008), au-dela aucun sol. Pour descendre vers la salle 26 il faut donc une manoeuvre volontaire (agripper le rebord puis se lacher, ou saut avec elan depuis plus loin); c'est le premier point a faire a la main. Documentation ajoutee dans docs/porting/colosseum-walkthrough.md section 5. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, point de bascule 12 -> 26 mesure: GetFloor le long de la corniche a y=1024, z=53760, en partant de la room 12, donne: x=43520..39936 room=26 (positions hors grille de la room 12, bascule immediate); x=39424 room=26 height=1151 idx=1089; x=38912 room=26 height=1151 idx=1089; x=38400 room=12 height=-32512 (plus de sol). La bascule vers la salle 26 se fait donc a l'extremite ouest de la corniche (x~39424) avec une marche de quelques centaines d'unites et non une chute de 2048: c'est un pas vers l'ouest, ce qui corrige l'hypothese 'chute maitrisee'. Documentation mise a jour dans docs/porting/colosseum-walkthrough.md et docs/porting/linux32.md. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-17

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-17T23:59:00+01:00. Linux32 provisoire.

The Colosseum, document de travail dedie: creation de docs/porting/colosseum-walkthrough.md qui regroupe (1) le chemin de progression calcule depuis les donnees du niveau (12 -> 26 -> 27 -> 108 -> 15 [CLOSED_DOOR1/2, GLADIATOR, KEY_HOLE1] -> 18 -> 100 -> 102 [KEY_HOLE2, CLOSED_DOOR2] -> 110 -> 83 -> 111 -> 85 -> 70 [PICKUP_ITEM1 -> TO_FINISH], avec le ROMAN_GOD en antenne de la salle 100 via 90), (2) les mecaniques a connaitre (temporisation des CRUMBLING_FLOOR, trappes, emetteurs de flammes, seisme, boss), (3) la recette de test Linux32 (sauvegardes de reprise valides en room 12 aux positions 43364,768,52325 ou 43520,768,51712, latence de demarrage 60-200 s et buffering stdout, captures via import -window, pilotage deterministe par break LaraControl + set var input avec les bits IN_*, forcage de pos.y_rot), et (4) le tableau des elements encore stubs avec leur impact reel sur ce parcours (ControlScaledSpike/DrawScaledSpike, ControlRollingBall, SteamLasers, Fishtank, ControlTeleporter, DrawWeaponMissile, rendu de corde, UpdateFireSparks/GunShells/Rats/Bats, FixedCamera, selection de niveau, audio). Constat: le parcours ne depend d'aucun handler manquant, les blocages restants sont de la verification en jeu. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum, carte et graphe de progression: ajout de scripts/porting/render_level_map.py (rendu top-down des cellules par altitude avec salles et items) et de l'option --emit-selftest du decodeur; les deux sont couverts par tests/porting/test_level_floordata.py sur un niveau synthetique. En construisant le graphe des portails (door) et des liens verticaux (pit_room/sky_room), le chemin voulu par le niveau depuis la corniche est 12 -> 26 -> 27 -> 108 -> 15 -> 18 -> 100 -> 102 -> 110 -> 83 -> 111 -> 85 -> 70. Annotations: room 12 = LARA/depart corniche (sol 1024); 26 = puits sous la corniche (3072); 27 = 3072; 108 = 1024 avec 4 triggers (CD 57, objets 29/26); 15 = 1024 avec CLOSED_DOOR1/2, GLADIATOR et KEY_HOLE1; 18 = 1024; 100 = 512 (2 triggers obj 25); 102 = 512 avec KEY_HOLE2, CLOSED_DOOR2, ANIMATING1_MIP; 110 = 2816; 83 = 4352; 111 = 4352; 85 = 5888 (CD 55); 70 = 7936 avec PICKUP_ITEM1 -> TO_FINISH. Le combat du ROMAN_GOD (salle 90) est sur une antenne de la salle 100 (100 -> 90). Conclusion: la corniche mene vers le bas (salle 26) et non vers la salle 8; les salles 8/14/25/92 (dalles qui s'effondrent, pont ANIMATING15_MIP) sont une branche laterale sans issue nouvelle, ce qui clot le blocage du 'bouton du crawlspace': il n'y avait rien a trouver. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum, salle 8 mecanique des dalles et issue ouest: (1) les CRUMBLING_FLOOR de la salle 8 portent chacune un OCB qui est une temporisation (1, 5, 10, 20, 30, 40, 50, 70, 80, 100, 120); stationner sur une dalle la fait ceder. C'est la cause de TOUTES les chutes observees jusqu'ici (room 26 puis room 14, y=6144, hp=-1) et non un defaut de collision; exemple mesure en restant 100 frames sur la dalle OCB 120 de (1,2): n=150 debout 40130,256,52659; n=175 floor passe a 261; n=180 chute (room 12); n=190 room 14 hp=-1. (2) En restant mobile (saut d'entree + marche continue) Lara traverse la plateforme 43520,256,53731 -> 40037,256,53754 (colonne cx=4 puis cx=1, ligne cz=3) puis remonte vers z=52492 (ligne cz=2); mais a x~40107 la marche vers l'ouest ne progresse plus (state=2 puis state=1 speed=38 sans deplacement): la cellule (0,2) est un portail DOOR_TYPE vers la salle 25 dont le sol est a -1024, soit un mur de 1280 depuis la salle 8, infranchissable. La salle 8 est donc un cul-de-sac a l'ouest; la sortie de la zone (corniche + salle 8) est ailleurs, probablement la chute maitrisee depuis la corniche vers la salle 26 (pit_room=26, 2048 plus bas, survivable). (3) Test complementaire: depuis la corniche, saut+avant vers l'ouest ne declenche aucun saut (state=14 GRAB_TO_FALL puis state=2, position inchangee a 43109,768,52325). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum, salle 8 geographie vue a l'ecran: capture de la fenetre de jeu (import -window) a 40037,256,52736 room 8: Lara est sur une dalle carrelee, devant elle une marche montante vers un sol plus haut et une niche sombre a droite; le vide est lateral, pas dans l'axe. Recoupement avec les cellules decodees: (0,2) sol 0 (256 au-dessus de la dalle, franchissable), (0,3) sol -1024 (1280 au-dessus, mur), (0,1) aucun sol (-32512). Les essais precedents echouaient parce qu'a z=51712 (ligne cz=1) il n'y a rien a l'ouest (chute vers salles 26/14); il faut d'abord se decaler dans la ligne cz=2 (z entre 52224 et 53248) puis monter la marche de 256 dans (0,2). Observation importante: une sauvegarde patchee en 40037,256,52736 room 8 ne demarre pas en jeu, l'ecran se fige sur une cinematique (Lara derriere des barreaux) et l'image n'avance plus; ce n'est pas une boucle de GetFloor (un interrupt + bt montre la pile normale DrawOTag -> Emulator_EndScene -> WaitForTimestep). Les sauvegardes en room 12 demarrent normalement: garder les points de reprise en room 12 et entrer dans la salle 8 par le saut sur les dalles. Note: sous gdb et avec stdbuf, [EMU] Initialising Emulator peut sortir apres 60 a 200 s et la sortie standard est bufferisee, un log muet n'est pas une preuve de blocage. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

Correctif racine des entrees: Emulator_UpdateInput (et Emulator_UpdateInputDebug) fusionnait clavier et manette avec un ET: '((unsigned short*)padData[i])[1] = kbInputs & controllerInputs'. Les deux masques etant actifs au niveau bas (0xFFFF = rien), un ET exige le meme bouton sur le clavier ET sur la manette; des qu'une manette est presente (SDL_NumJoysticks()>0, cas de vpad) aucune des deux sources ne produit d'entree: symptome inputBusy=0 avec PadConnected=1 et Lara figee malgre les touches. Corrige en OU sur les deux chemins. Validation runtime (sauvegarde corniche, clavier xdotool): inputBusy passe de 0x0 a 0x1 (avant) puis 0x4 (gauche, state=20 TURN_FAST) et Lara se deplace (43364 -> 43109). Le pad virtuel vpad reste sans effet (RawPad=0), chemin separe non resolu, mais le clavier suffit au debug manuel. Regression verrouillee par tests/porting/test_input_merge.py. Note build: les objets emulateur sont dans l'archive statique build/.../EMULATOR/libPSX.a; apres modification de EMULATOR/EMULATOR.C il faut make -C build/porting/build-gameplay59/build/EMULATOR puis relancer sh CMakeFiles/TombRaiderChronicles_PSXPC_N.dir/link.txt avec LIBRARY_PATH 32 bits. Build-gameplay59 SHA256 9d152a50622831050b5db6a0fb339ff4762db53832f9fdfa300efba435d92a8a. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum, salle 8 traversee mesuree: avec input force (IN_FORWARD/IN_JUMP) depuis une sauvegarde patchee en 43520,768,51712 room 12 (Lara apparait dans la salle 8 a y=256 sur les CRUMBLING_FLOOR), la plateforme de dalles est traversable d'est en ouest de x=43520 a x=40037 a y=256 constant sans chute ni blocage (donc les CRUMBLING_FLOOR et le pont ANIMATING15_MIP de la cellule (4,2) portent bien Lara). A l'ouest la marche s'arrete a x=40037 (bord de la derniere dalle); un saut vertical a cet endroit ne progresse pas en x (speed=2) et fait tomber dans le puits: room 26 (y=3141, fall=147) puis room 14 (y=6144, state=8), chute d'environ 6000 unites donc mortelle. Le saut simple n'est donc pas la sortie. Piste restante: saut avec elan (garder IN_FORWARD pendant l'appui) depuis x~40500 pour couvrir les ~100 unites manquantes et retomber sur la cellule (0,2) (x 38912..39936, sol 0), ou acces par la salle 92 cote est. Note: la sauvegarde corniche contient room=0 (et non 12) avec 43364,768,52325 et y_rot=-16384; GetFloor retablit room 12 au chargement. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum, entree deterministe dans la salle 8: (1) le pad virtuel et xdotool ne produisaient plus aucune entree (inputBusy=0 alors que PadConnected=1); mise au point d'un pilotage reproductible en forcant input juste avant LaraControl (break LaraControl; set var input=...). Attention: 'set input = 1' echoue car gdb l'interprete comme la sous-commande set input-radix; il faut 'set var input'. Bits: IN_FORWARD=0x1, IN_BACK=0x2, IN_LEFT=0x4, IN_RIGHT=0x8, IN_JUMP=0x10, IN_ACTION=0x40, IN_WALK=0x80. (2) La sauvegarde corniche (43364,768,52325, room 12) est hors de la grille de cellules de la room 12 (fin a x=43008); la seule surface possible serait le pont ANIMATING15_MIP (item 21, 43520,0,52736) qui n'a pas de callback de sol (ni PC ni port), donc Lara s'arrete au bord du vide: ce n'etait pas un gel de controle. (3) Sauvegarde patchee en 43520,768,51712 room 12: Lara apparait dans la salle 8 a y=256 sur les CRUMBLING_FLOOR (item 15, OCB 80) et repond aux entrees forcees; saut + course mesurees (43520,256,51712 -> saut -> 43520,256,53659 -> course -> 43520,256,54171, arret au bord). La salle 8 est donc jouable, aucun handler ne manque pour s'y deplacer; l'entree reelle est le saut sur les dalles cx=4 a y=256. (4) Demarrage lent a ne pas confondre avec un blocage: avec des peripheriques uinput residuels, [EMU] Initialising Emulator peut prendre 110 a 200 s. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum, precision geometrique: les FLOOR_INFO de la salle 8 donnent pit_room=12 (la corniche est SOUS la salle 8) et sky_room=25 (la salle 25 est AU-DESSUS, y croit vers le bas) pour les cellules centrales; les deux cellules ouest (0,2) et (0,3) x=39424 n'ont pas de lien vertical et portent le portail door[0] vers la salle 25 (floor 0 puis -1024). La sortie de la salle 8 est donc un simple pas vers l'ouest avec une chute de 1024 dans la salle 25 puis la salle 92; aucun bouton ni interrupteur n'intervient, ce qui invalide l'hypothese du 'bouton du crawlspace'. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum: (1) nouvel outil scripts/porting/decode_level_floordata.py qui decode hors-ligne items/FLOOR_INFO/chaines floor_data/portails depuis un dump gdb de l'arene de niveau (room..floor_data+65536), avec --selftest synthetique et tests/porting/test_level_floordata.py. (2) Ce decodage etablit que les salles 8/12/14/25 sont empilees sur le meme x/z (altitudes 0/768/6144/-1024) et que les salles 8 et 25 n'ont AUCUN trigger de sol: le 'bouton du crawlspace' n'existe pas, la sortie de la salle 8 est le portail ouest vers la salle 25 puis remontee par la salle 92; les 114 triggers du niveau sont decodes sans ambiguite. (3) Matrice des handlers du niveau 3 lue a l'execution; ports/assignations de ce lot: FlameEmitterControl complet, InitialiseFlameEmitter, InitialiseFlameEmitter2, InitialiseScaledSpike (TRAPS.C), ItemNearLara (TOMB4FX.C), EarthQuake reel (OBJECTS.C), et assignations TRAPDOOR1..FLOOR_TRAPDOOR2, FLAME_EMITTER..FLAME_EMITTER3, WATERFALLMIST, EARTHQUAKE dans PortSetupGameplayObjects. Validation runtime: handlers non nuls, quake oscille f0 20<->106 avec camera.bounce -14..-101, flame actif, trapdoor state=1 anim=582, 160 frames sans SIGSEGV. Restent non assignes: TEETH_SPIKES (ControlScaledSpike/DrawScaledSpike stubs), ROLLINGBALL (ControlRollingBall stub), STEAM_LASERS, FISHTANK, TELEPORTER. 4177 tests PASS (+2). Build-gameplay59 SHA256 7051f2aca364a21177baabb06068cc07e1a55dac3616591915229dc783259585. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum FlipMap: flip_status etait inverse et affecte a chaque appel (flip_stats[n] = flip_stats[n]==0; flip_status = flip_stats[n]==0) au lieu de flip_stats[n]=!flip_stats[n]; flip_status=flip_stats[n] comme sur PC. Corrige. Validation runtime: FlipMap(3) fait passer flip_status 0->1 (flip_stats[3] 0->1); les zones ground_zone[..][flip_status] et les salles echangees (32<->76, 65<->82, 68<->33) sont coherentes. La corniche n'a pas de salle appariee pour FlipNumber 2, apparence inchangee. 4177 tests PASS, corniche 200 frames OK. Build-gameplay59 SHA256 1f70101d8941435cc732067fbbb5c747b32d43d5a1621cf9cdc4d28190b1f7b8. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum HK/crossbow: (1) precedence de condition dans LaraGun (GAME/LARAFIRE.C): 'state==0x47 || state==0x69 || state==0x6A && request==4 || request==6 || request==5' faisait que toute demande HK/crossbow (request 5/6) prenait la branche accroupi et l'arme n'etait jamais dessinee; corrige en regroupant les etats accroupis et les trois armes. (2) ControlCrossbow et CrossbowHitSwitchType78 (GAME/LARA1GUN.C) portes depuis lara1gun.cpp: deplacement du bolt, changement de salle, GetCollidedObjects, cible grappling, activation switchs 7/8 (GetSwitchTrigger, ExplodeItemNode). (3) CROSSBOW_BOLT assigne dans PortSetupGameplayObjects (control=ControlCrossbow, draw_routine=DrawWeaponMissile, using_drawanimating_item=FALSE, save flags). Validation: shotgun toujours fonctionnel apres correctif (statue 300->228, munitions 100->76); test HK/crossbow force dans le Colosseum plante dans mRotSuperPackedYXZ_CL car les objets HK/crossbow ne sont pas charges dans ce niveau; a valider dans un niveau qui les contient. 4177 tests PASS. Build-gameplay59 SHA256 7ea4b985123b9bf44c28b56a726fa6ed28e71d6bc5dbac7a6094742b99a735ec. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum shotgun/armes longues: deux bugs corriges. (1) draw_shotgun/undraw_shotgun (GAME/LARA1GUN.C) etaient des decompilations erronees (anim_index sans +1, etats STATE_LARA_RUN_FORWARD au lieu de 1/3, conditions inversees, frame_base=anims[item->frame_number].frame_ptr au lieu de anims[item->anim_number].frame_ptr); remplaces par les versions de lara1gun.cpp. (2) DEL_CalcLaraMatrices_Interpolated_ASM (CALCLARA.C:1792) passait la valeur s1[74] comme pointeur au lieu de &s1[74], causant a22=1 et SIGSEGV a la premiere frame de bras dessinee; corrige. Validation runtime: shotgun force par la sequence de draw reelle (request_gun_type=WEAPON_SHOTGUN, gun_status=LG_NO_ARMS) room90 face a ROMAN_GOD; draw_shotgun cree l'item 110 et passe LG_READY; tirs reels, munitions 100->70, cible 79, PV statue 300->210; aucun crash. 4177 tests PASS, corniche 200 frames OK. Build-gameplay59 SHA256 fa82913848f1cff77d4c0b1c1e29d2f19acc490306586c66e0870ed1967a9315. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum armes longues: port de RifleHandler et AnimateShotgun (GAME/LARA1GUN.C) depuis lara1gun.cpp. RifleHandler: LaraGetNewTarget (sauf crossbow sans laser), LaraTargetInfo, AimWeapon, torse/tete, AnimatePistols(WEAPON_REVOLVER) ou AnimateShotgun, flash dynamique (mains revolver, canon shotgun/HK). AnimateShotgun: fumee, etats 0/2/6/8, FireShotgun/FireHK/FireCrossbow, douilles shotgun, sons HK/silencieux, synchro frames de bras. Adaptations: W_SILENCER/W_AMMO1/W_AMMO2 -> WTYPE_SILENCER/WTYPE_AMMO_1/WTYPE_AMMO_2 (OBJECTS.H), LMX_HAND_R->LJ_RHAND, phd_sin/cos->SIN/COS, GF_MIRROR->GF_LVOP_MIRROR_USED, TriggerDynamic_MIRROR->TriggerDynamic, includes CAMERA.H/PSXINPUT.H/LARA2GUN.H/GAMEFLOW.H. Validation: 4177 tests PASS, corniche 200 frames OK. Test synthetique revolver sans draw normal declenche l'assertion DEL_CalcLaraMatrices_Interpolated_ASM (CALCLARA.C:1766) car frames bras/weapon_item non initialisees; a valider par la sequence reelle de sortie de l'arme. Build-gameplay59 SHA256 11db0025e7813856e032182d57a44a0c3bacd8b06ab9e7a0c7fc2ec1badb6f9b. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum combat complet: PistolHandler (GAME/LARA2GUN.C) remplace la version simplifiee par celle de lara2gun.cpp (LaraGetNewTarget, LaraTargetInfo, AimWeapon des deux bras, torse/tete selon locks, AnimatePistols(weapon_type) donc FireWeapon reel, flash dynamique aux mains via GetLaraJointPos/TriggerDynamic). Pipeline complet LaraGun->PistolHandler->AnimatePistols->FireWeapon->GetTargetOnLOS->degats actif. Correction critique ObjectOnLOS2 (SPEC_PSXPC_N/GETSTUFF.C): la boucle items faisait item=&items[r->item_number]; item_num=item->next_item a chaque iteration, la figeant sur le 2e item (while item->next_item != -1); depuis que GetTargetOnLOS l'appelle, cela bloquait le jeu au premier tir; corrige en item_num=item->next_item; while(item_num != -1). Validation runtime: statue ROMAN_GOD obj61 item79 room90, Lara pistolets, cible 79; AnimatePistols/FireWeapon tirent, PV statue 300->276->192->90, aucun crash/hang. 4177 tests PASS, corniche 200 frames OK. Build-gameplay59 SHA256 3f4aafa8109a786725285338666ff0b220f1460f45b73dc3a1daf12cebfb35b6. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum combat: port de GetTargetOnLOS (GAME/CONTROL.C) depuis control.cpp - LOS + ObjectOnLOS2, collision, shatter des meshes destructibles, ricochets, degats HitTarget, objets smashables, switchs explosifs SWITCH_TYPE7/8 (GetSwitchTrigger, ProcessExplodingSwitchType8), crossbow/laser, meshes statiques (ShatterObject, SmashedMesh). Adaptations: ITEM_INFO/MESH_INFO/GAME_VECTOR/PHD_VECTOR qualifies struct, phd_atan->phd_atan_asm, IFL_SWITCH_ONESHOT->IFLAG_UNK40, IFL_CODEBITS->IFLAG_ACTIVATION_MASK, GF_OFFICE->GF_LVOP_TRAIN, include LARAFIRE.H pour weapons/HitTarget. Validation: 4177 tests PASS, corniche 200 frames sans crash. Build-gameplay59 SHA256 2babbc6898792b180ffedff44a88267078175e3348c07d638f8e15627b32a95c. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum combat: port de DoProperDetection (GAME/LARAFIRE.C) depuis larafire.cpp - impacts de projectiles sur sols/pentes (BIG_SLOPE, DIAGONAL)/plafonds/murs, rebonds (fallspeed, speed, y_rot), changement de salle via ItemNewRoom (implementation PSXPC dans COLLIDE_S.C). Portage: ITEM_INFO/FLOOR_INFO qualifies struct, ushort->unsigned short, casts short(...)->(short)(...), includes COLLIDE.H/COLLIDE_S.H/ITEMS.H. Validation: 4177 tests PASS, corniche 200 frames sans crash. Build-gameplay59 SHA256 e4b074ccea108c072786c93aee96fae3cd251a537042be425e109883aefef98a. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum test flipmaps room 8: FlipMap(0..9) sur la sauvegarde room8 ne change rien, flip_status reste 0. La sortie n'est probablement pas un flipmap mais une porte/objet ou un TO_FLIPEFFECT declenche par le bouton du crawlspace. Le scan des triggers par cellule (trigger_index apres GetHeight) renvoie des mots qui ressemblent encore a des donnees de sol; il faudra un decodeur de triggers dedie ou reperer le bouton en jeu. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum precision porte room 8: verification runtime, ANIMATING15 (obj444 anim697) et ANIMATING15_MIP (obj445 anim698) ont des animations vides (frame_base=frame_end=0); meme actives (flags|REVERSE, status=ACTIVE, AddActiveItem) leur frame reste 0. Ce sont des decorations/grilles statiques, pas le mecanisme de sortie. Le bouton/trigger du crawlspace reste a identifier; piste: scan des donnees de trigger des cellules rooms 8/12/25/26/92 pour un TO_OBJECT visant la porte ou un flipmap. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum assignations generiques ANIMATING/PUZZLE_HOLE: PortSetupGameplayObjects n'assignait les controles ANIMATING que pour ANIMATING3_MIP/ANIMATING4 de Trajan's Markets; ajout des boucles de setup.cpp: PUZZLE_HOLE1..8 (ControlAnimatingSlots + PuzzleHoleCollision), PUZZLE_DONE1..8 (ControlAnimatingSlots + PuzzleDoneCollision), ANIMATING1..12_MIP (InitialiseAnimatingSlots, ControlAnimatingSlots, ObjectCollision, save flags, bones[0]|=8, bones[4]|=4), ANIMATING13..16_MIP (InitialiseAnimatingSlots, ControlAnimatingSlots, save flags, HitEffect=0). Cas special Trajan's garde prioritaire; boucles ANIMATING desactivees pour LVL5_TITLE pour preserver le plan du titre. Validation: room 8, objects[445].control et objects[444].control = ControlAnimatingSlots (ANIMATING15/ANIMATING15_MIP, mecanisme de sortie); la porte ne s'anime pas sans son trigger, bouton du crawlspace toujours a identifier. Sanity corniche 200 frames OK, 4177 tests PASS. Build-gameplay59 SHA256 a1ea77fa9809d94b26f09dd7b02c3d11eb2a9597a798680c9c793518999420fb. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-16

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-16T23:59:00+01:00. Linux32 provisoire.

The Colosseum room 8 (etage des grilles): cartographie runtime autour de 43364,256,51900: sol walkable boites 14-19 a y~1024 (f=4), reste NO_HEIGHT; objets CRUMBLING_FLOOR obj105 en damier, TELEPORTER 387, EARTHQUAKE 366, CAMERA_TARGET 409, PUZZLE_HOLE4 245, ANIMATING15_MIP 445 a 43520,0,52736 (probable porte/sortie de droite); aucun SWITCH_TYPE dans rooms 8/12, le bouton du crawlspace est un element anime/trigger d'une autre room (25/26 probable). Le vault depuis la corniche atteint la room 8 mais la sortie de droite reste fermee car le bouton n'a pas ete presse: le raccourci ne remplace pas hang->traverse->crawlspace->bouton. Sauvegarde /tmp/opencode/TOMB5.room8.sav. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum corniche: apres les corrections GetBestFrame/animation/AnimateItem, test runtime sur la sauvegarde corniche 43364,768,52325 room12. Si l'on remet GLOBAL_playing_cutseq=0, cutseq_trig=0, globoncuttrig=0 et bDisableLaraControl=0 a chaque frame (comme probe_free.gdb), Lara repond aux entrees; depuis 43364,768,51900, Up+Action (vault) franchit la marche de 512 et place Lara a 43364,256,51900 room 8 (etage superieur des grilles/dalles). C'est le pas de 512 qui bloquait TestLaraVault; la correction de GetBestFrame (branches inversees) semble avoir debloque la detection de rebord/vault. Etat sauvegarde /tmp/opencode/TOMB5.room8.sav (level 3, room 8, 43364,256,51900). L'exploration de l'etage 8 n'a pas encore trouve le crawlspace/le bouton; camera montre un couloir et des alcoves a y=256. Attention: sans reset des variables de cutscene, Lara reste figee apres le chargement de la corniche. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum rendu des shockwaves: DrawShockwaves PSXPC (DRAWSPKS.C) trace 48 points sur le rayon moyen (InnerRad+OuterRad)/2 relu en non signe pour retrouver 40960 depuis 0xA000, projection ecran, sprite DEFAULT_SPRITES+14, fondu sur les 8 dernieres frames; appele dans DrawPhase apres DrawLightning. Validation visuelle: shockwave injectee autour de Lara -> anneau jaune visible (swvis.png); rendu approximatif (anneau de sprites au lieu du quad texture PC). Remarque: le level select (PlayAnyLevel) affiche la selection mais choisir Trajan's Markets demarre encore le niveau 1 (save F5 level 1); chemin de debug non utilise pour la campagne, validation GUARDIAN reste synthetique. Build-gameplay59 SHA256 847b137c2ea5dd3ac23d811249ee94729344ef2a3cf197b915143badf7ccaf28, 4177 tests PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum mise a jour des effets + degats shockwave: UpdateSparks/UpdateFireSparks/UpdateSmokeSparks/UpdateBubbles/UpdateSplashes/UpdateDebris/UpdateBlood/UpdateDrips/UpdateGunShells/UpdateShockwaves/UpdateLightning etaient dans un bloc #if PC_VERSION non compile pour PSXPC et leurs appels dans la branche PSX de ControlPhase etaient commentes; les effets etaient crees mais jamais mis a jour (duree de vie figee, aucun degat). Corrections: garde #if PC_VERSION || PSXPC_TEST, appels reactivees dans ControlPhase (sparks, fire, smoke, bubbles, splashes, debris, blood, drips, gunshells, shockwaves, lightning), stubs Unimpl->UNIMPLEMENTED, UpdatePulseColour/UpdateSky gardes PC_VERSION (doublons PSXPC dans TEXT_S.C/DRAWSKY), TriggerRicochetSpark limite a PC_VERSION, EFFECT2.C.o obsolete sans TriggerRipple recompile, GetBestFrame (CALCLARA.C) branches inversees corrigees d'apres draw.cpp. Validation: attaque ROMAN_GOD etat 3, shockwaves mises a jour et infligent des degats (lara hp 1000->724); corniche 200 frames sans crash; 4177 tests PASS. Build-gameplay59 SHA256 3dc02e2826d56b657381f156220574b1862569b014434ac94e41d4ab27c32d9c. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum ROMAN_GOD attaques validees en partie: cartographie des animations (state1 560/569/570, state2 561, state3 562, state4 563, state5 564, state7 566/567/568, state9 571/572, state10 573, state11 574, state12 575, state13 576). Avec Lara a 800 unites et etat 3 force (anim 562): l'attaque s'execute, deux shockwaves creees a frame_base+34 (ShockWaves[0/1].life=48); l'IA enchaine etat 10 puis etat 2 et cree des eclairs (Lightning[0].Life=24); aucun crash sur 250+ iterations. Lara n'a pas perdu de PV: test vertical des shockwaves (sw->y vs bounds de Lara) ne passe pas dans ce montage, a valider en conditions reelles. DrawShockwaves non porte (seuls les eclairs sont dessines). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum deplacement des creatures: AnimateItem (GAME/CONTROL.C) omettait tout le bloc vitesse de control.cpp (velocity/acceleration/Xvelocity/Xacceleration -> item->speed puis translation pos.x/z via SIN/COS y_rot et y_rot+0x4000). Sans ce bloc aucune creature ne se deplacait (animation sur place), ce qui empechait aussi ROMAN_GOD de se rapprocher de Lara. Le else est implemente, la branche gravite reste inchangee. Validation: ROMAN_GOD se deplace reellement en etat 7 (51968,66043 -> 51924,65985 -> 51429,66041 -> 51708,65595); corniche 200 frames sans crash; tests 4177 PASS. Diagnostic AI: info.distance=27563485 (distance au carre), tbox=rbox=245; la statue reste trop loin (>2560) pour passer en attaque dans le montage synthetique, rapprochement/cheminement a verifier avec la sequence reelle du niveau. Build-gameplay59 SHA256 0925ce7e402e0928a375d6d0d1037bfead225b7bc4432e8fd0da0f3e5091247c. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum correction complete de l'animation interpolee: (1) iPushMatrix_AI (ANIMITEM.C) n'empilait que la matrice lumiere fp[21] alors que iPopMatrix_AI depile fp[20] (objet) et fp[21] (lumiere), comme iPushMatrix non-AI qui pousse iMatrix et Matrix; chaque os faisait descendre la pile objet de 8 ints et apres ~15 os fp[31..33] etait ecrase (pointeur de rotations sauvage -> SIGSEGV iRotSuperPackedYXZ_AI). iPushMatrix_AI empile maintenant les deux matrices. (2) erk_interpolated se terminait par //j loc_81714 assert(FALSE): le saut vers la finalisation (compteur matrices + mmPopMatrix_AI) n'etait pas implemente; le chemin interpole revient a l'appelant qui execute loc_81714 et le pop; les deux assert(FALSE) remplaces par return. Validation: ROMAN_GOD eveille (activation forcee state=1) plus de crash, etats 13->10->2->7, eclairs Life=24, 250 iterations DrawRooms; spawn room 6 Colosseum 60928,6400,49664 qui provoquait SIGSEGV InterpolateMatrix_AI: 201 frames sans crash (SANITY OK room 6 hp 1000); corniche 200 frames OK. Build-gameplay59 SHA256 a4d80b28fac639bbf6c35fa0d86b14f56b77ce96e1f3fcc78ce6dca6dbbf0ad4, 4177 tests PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum ROMAN_GOD + corrections animation: port complet GAME/ROMANGOD.C/.H depuis romangod.cpp (TriggerRomanGodSparks, TriggerRomanGodMissile, TriggerRomanGodLightningGlow, TriggerRomanGodPowerupFlames, TriggerRomangodGravel, InitialiseRomangod, RomangodControl); TriggerRomanGodMissileFlame deja dans EFFECT2.C (pas de doublon); struct RG_TARGET dans TYPES.H; assignation dans PortSetupGameplayObjects (CreatureCollision, hit_points 300, radius 256, pivot_length 50, object_mip 5120, intelligent, HitEffect 2, save flags, bones 24/52 |=8|4, 17 meshes MESHSWAP1); ROMANGOD.C.o ajoute au link.txt. Corrections: CreatureActive (BOX.C) etait inverse (ne renvoyait 1 que si IFLAG_KILLED) -> reecrit selon box.cpp (IFLAG_KILLED 0; status ITEM_INVISIBLE -> EnableBaddieAI + status ITEM_ACTIVE; sinon 1). InterpolateMatrix_AI (ANIMITEM.C): 4 ecritures utilisaient a3/t1/t3 comme pointeurs au lieu de a0 et les translations etaient ecrites en short au lieu d'int -> corrige (plus de SIGSEGV InterpolateMatrix_AI). Validation: sauvegarde corniche niveau 3 tourne 200 frames sans crash (SANITY OK); statue obj61 room90 48640,512,69120 initialisee au chargement (anim=anim_index+16, state=13, position decalee de 486); activation forcee EnableBaddieAI(79,1)+status=1+AddActiveItem(79) et Lara en 48640,512,70144 -> data alloue, controle demarre. Blocage restant: SIGSEGV iRotSuperPackedYXZ_AI (ANIMITEM.C:1422) pendant animation interpolee de la statue 17 os; fp[33] sort de la zone de frames (meme classe que le crash room 6). Build-gameplay59 SHA256 fff7b798ff64b25b9d497d011f815d66992b75a9785bae3cb60abf721be6dfb3, 4177 tests PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum effets + statue: ajout LIGHTNING_STRUCT/GUARDIAN_TARGET (TYPES.H), Lightning[16], spark_flags et CLRR/CLRG/CLRB/CLRA. Port de TriggerLightning (retourne un pointeur, Life = octet alpha de rgb), TriggerExplosionSparks, TriggerExplosionSmoke, TriggerShockwaveHitEffect, UpdateSparks (128 slots), UpdateShockwaves, UpdateLightning, mRotBoundingBoxNoPersp. Rendu PSXPC: S_DrawSparks (projection w2v_matrix+camera.pos+phd_persp, MGDrawSprite) et DrawLightning (32 points courbe PC, rubans POLY_FT4 sprite 28, fondu vie) appeles dans DrawPhase. Correction majeure: xLOS/zLOS etaient dans #if PC_VERSION non compile et les stubs UNIMPLEMENTED de SPEC_PSXPC_N/GETSTUFF.C etaient seuls lies (LOS toujours faux); garde passee a #if PC_VERSION || PSXPC_TEST et stubs supprimes; ClipTarget deja compile. GUARDIAN.C complet (InitialiseGuardian, TriggerGuardianSparks, TriggerBaseLightning, GuardianControl) et assigne dans PortSetupGameplayObjects (CreatureCollision, explodable_meshbits 6, HitEffect 3, save flags); deux gardes defensifs sur gt.elptr[i] evitant un null deref si aucun slot d'eclair. Validation runtime: eclair vertical injecte visible (corniche niveau 3); statue synthetique dans l'arene (item79 obj61 copie vers objet65, data reconstruite): LOS passe (f0 0->1), chute puis attaque (f0=2), TriggerBaseLightning cree des eclairs Life=50, eclairs verts visibles et halo dynamique vert sur Lara, >270 iterations sans crash. La statue reelle est dans Trajan's Markets (obj65 room69 45568,1792,43520); validation in-situ restante car le level select du port demarre le niveau 1 et aucune sauvegarde niveau 2 n'existe. Build-gameplay59 SHA256 55246b16ea9bbc6b87a59cb07aa0e6dde272b91fc0ec7961d6ff600effffc011, 4177 tests PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum pistolets: port de AnimatePistols (GAME/LARA2GUN.C) depuis lara2gun.cpp:110 - fumee SmokeCountL/R + TriggerGunSmoke, FireWeapon aux deux bras, recul p->RecoilAnim/winfo->recoil_frame, flash, douilles TriggerGunShell, sons, savegame.Game.AmmoUsed; joints LJ_LHAND/LJ_RHAND. Important: le port utilise encore son PistolHandler simplifie (ciblage direct + HitTarget), donc AnimatePistols/FireWeapon ne sont pas encore branches dans LaraGun; prets pour le basculement vers le pipeline PC. Build-gameplay59 SHA256 c8569e9784a70ed9e478b2847054ba82d79b45396e1f6c686dfdc8a31108e282, 4177 tests PASS. Reste guardian.cpp bloque par le sous-systeme lightning/effects (LIGHTNING_STRUCT, TriggerLightning retournant un pointeur, TriggerShockwave, mRotBoundingBoxNoPersp, rendu). Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum gladiateur: port de InitialiseGladiator et GladiatorControl (source gladiatr.cpp) dans GAME/LION.C (evite un nouvel objet au lien), assignation dans PortSetupGameplayObjects avec CreatureCollision, hit_points 20, radius 102, pivot_length 50, object_mip 5120, intelligent, HitEffect 1, save flags, bones 24/52 |=8|4, 16 meshes MESHSWAP1 (mesh_index+lp*2+1). Validation runtime item26 room15 49664,1024,54784 active (status=1, EnableBaddieAI(26,1)): deplacement/animation sans crash (49624,1024,55040)->(46580,1024,58567), state=1, hp=20; comme le lion il suit son trajet/patrouille, poursuite/attaque a valider. Build-gameplay59 SHA256 984219c308ef545a6dc6b99a6a2a31658112fe3806605a80c5fd07d57835fb32, 4177 tests PASS. Reste guardian.cpp (statue) et finitions combat. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum combat rayon: port de RayBoxIntersect et DoRayBox dans SPEC_PSXPC_N/GETSTUFF.C (signature PSXPC 10 args adaptee avec PHD_3DPOS local; mPushUnitMatrix/mRotY/Matrix->m* echelle 4096 + W2V_SHIFT 12, Normalise, GetSpheres, Slist/ShatterItem, ClosestItem/ClosestCoord/ClosestDist). Important build: les objets SPHERES.C.o et GETSTUFF.C.o doivent etre ecrits dans CMakeFiles/TombRaiderChronicles_PSXPC_N.dir/<nom>.C.o et non dans __/SPEC_PSXPC_N/, sinon le lien n'inclut pas les nouveaux symboles (corrige). Build-gameplay59 SHA256 b49584390388cd94cfd917cf243d1485b8253ca581870eceb9a07f82f1dac500, 4177 tests PASS. Restent GetTargetOnLOS, DoProperDetection, ObjectOnLOS2/DoRayBox branchement, AnimatePistols/RifleHandler, gladiatr.cpp/guardian.cpp. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum combat: port de xLOS/zLOS/ClipTarget (GAME/CONTROL.C) rendant LOS fonctionnel; port de GetSpheres (SPEC_PSXPC_N/SPHERES.C, matrices m*, Matrix->tx/ty/tz, TRX/TRY/TRZ); port de LaraTargetInfo, LaraGetNewTarget, FireWeapon (GAME/LARAFIRE.C, LJ_RHAND, baddie_slots, Slist, phd_GenerateW2V/phd_mxptr M20-M22). Etat: le port possede deja un PistolHandler simplifie (ciblage direct + HitTarget/CreatureDie, sans LOS) qui permet de tirer; FireWeapon/LaraTargetInfo dispo mais pas encore branches. Restent GetTargetOnLOS, DoProperDetection, ObjectOnLOS2/DoRayBox (DoRayBox stub), AnimatePistols/RifleHandler, puis gladiatr.cpp et guardian.cpp. Build-gameplay59 SHA256 8f3e47cf19238424110112c10224c8e0f77afa835899261baffaecb58f196139, 4177 tests PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum validation runtime lion: save patchee pres du lion de room17 (item29, spawn 46568,1024,54784) et activation forcee (status=1, EnableBaddieAI(29,1)); le lion se deplace et s'anime sans crash: (45562,1024,54875)->(42462,1024,58589), state=1, hp=40, puis s'arrete. Le coeur IA (CreatureAIInfo, CalculateTarget, CreatureAnimation, CreatureTurn, CreateZone) s'execute reellement. Poursuite/attaque de Lara non validee (le lion suit pour l'instant son trajet/patrouille); a tester avec ai_bits et combat. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum IA creatures: port du coeur depuis TOMB5pc game/box.cpp et lot.cpp - CreatureAIInfo, CalculateTarget, CreatureAnimation, CreatureTurn, CreatureMood, GetCreatureMood, CreatureKill, GetAITarget (BOX.C) et CreateZone (LOT.C). Adaptations phd_sin/cos->SIN/COS, phd_atan->phd_atan_asm, SQUARE->multiplications, AS_*->STATE_LARA_* (AS_MONKEY180->STATE_LARA_MONKEYSWING_TURNAROUND, AS_HANG2DUCK->STATE_LARA_CLIMB_TO_CRAWL), IFL_*->IFLAG_*, TOSSPAD dispo, ROOM_UNDERWATER->0x1. Assignation lion dans PortSetupGameplayObjects: InitialiseLion, LionControl, CreatureCollision, hit_points 40, radius 341, pivot_length 50, object_mip 5120, intelligent, HitEffect 1, save flags, bones 24/76 |=8. Build-gameplay59 SHA256 91ed84c3aa96a446406f2cced8644257e877ba1b7447378159222338ff7234d7, 4177 tests PASS. Validation runtime lion a faire; gladiateur (gladiatr.cpp) et statue (guardian.cpp) restent a porter, ainsi que le combat LARAFIRE. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum socle montant + poulie: port de InitialiseRaisingPlinth et ControlRaisingPlinth (GAME/TRAPS.C, sources init.cpp:1149 et andrea.cpp:480) avec correspondances IFL_TRIGGERED->IFLAG_TRIGGERED, IFL_CODEBITS->IFLAG_ACTIVATION_MASK, IFL_CLEARBODY 0x8000->IFLAG_KILLED; port de InitialisePulley (init.cpp:444); objects[HIGH_OBJECT1] initialise/control/collision=ObjectCollision/save_position/save_flags; objects[PULLEY] InitialisePulley/SwitchControl/PulleyCollision/save_flags/save_anim. Validation runtime (save patchee a la poulie room49 41472,2816,29500): apres 3 pressions Action, poulie status 1->0, socle HIGH_OBJECT1 monte de y=2304 a y=1536 (3x256) et gemme PUZZLE_ITEM4_COMBO2 suit de y=1792 a y=976 (socle-560). Chaine poulie->trigger->socle validee de bout en bout. Build-gameplay59 SHA256 a8a0915e1921d45d7a0247801243e3834fe5bdcd7e37936ce029eaef6f2a9769, 4177 tests PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum corde cote objet: port dans GAME/ROPE.C de CreateRope, InitialiseRope, GetRopePos, mDotProduct, vMul, mCrossProduct, phd_GetMatrixAngles, ModelRigidRope, ModelRigid, SetPendulumPoint, CalculateRope, RopeNodeCollision, AlignLaraToRope, RopeCollision, RopeControl, init_all_ropes (source TOMB5pc game/rope.cpp). RopeList->Ropes, phd_PushUnitMatrix/RotYXZ/PopMatrix->mPushUnitMatrix/mRotYXZ/mPopMatrix, phd_sin/cos->SIN/COS (echelle 4096 + W2V_SHIFT 12), phd_sqrt->phd_sqrt_asm, phd_atan->phd_atan_asm. Integration: objects[ROPE] initialise/control/collision, using_drawanimating_item=FALSE, save_flags=TRUE; init_all_ropes() au debut de PortSetupGameplayObjects; DelAlignLaraToRope (LARAMISC.C) appelle AlignLaraToRope. Build-gameplay59 SHA256 047825bd33bf22615b2b6059c0755773ce03b21b7fcbee37842707861f6d6e3d, 4177 tests PASS. Non porte: rendu DrawRopeList/ProjectRopePoints car ROPE_STRUCT PSX n'a pas Coords[24][3]; physique/controle en place mais corde invisible. Decouverte annexe: HIGH_OBJECT1 (socle montant, gemme Colosseum) n'a ni initialise ni control dans PortSetupGameplayObjects; InitialiseRaisingPlinth/ControlRaisingPlinth non portes. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum corde cote Lara: port de Straighten (GAME/ROPE.C, equivalent _Straighten+Normalise PC, 24 segments, SegmentLength<<16, phd_sqrt_asm), UpdateRopeSwing (GAME/LARA.C, source lara.cpp:4952: arcs avant/arriere, RopeDFrame, RopeFrameRate, LegsSwinging, SFX_LARA_ROPE_CREAK), LaraClimbRope (LARA.C, source rope.cpp:587: RopeCount/RopeOffset/RopeDownVel/RopeFlag, ANIMATION_LARA_ROPE_DOWN, retour STATE_LARA_ROPE_IDLE; RopeList->Ropes). Build-gameplay59 SHA256 ef794f243aba5d9933333c608a515b97e595eae1142e30ae3d82ca0ddc1e611d, 4177 tests PASS. Reste cote objet dans rope.cpp non porte: InitialiseRope, CreateRope, RopeControl, RopeCollision, CalculateRope, SetPendulumPoint, RopeNodeCollision, AlignLaraToRope + assignation objects[ROPE].initialise/control dans PortSetupGameplayObjects; sans cela le puzzle de corde du Colosseum reste inactif. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum inventaire: port de use_current_item (GAME/NEWINV2.C) depuis TOMB5pc game/newinv2.cpp:2249 (armes request_gun_type, flare IN_FLARE+LaraGun, jumelles BinocularRange/BinocularOldCamera, medipacks, et GLOBAL_inventoryitemchosen=gmeobject utilise par KeyHoleCollision/PuzzleHoleCollision pour cles/puzzles/crowbar; etats AS_* mappes sur STATE_LARA_* 71/80/81/84-86/88/105-106). Port de FindPlinth (GAME/PICKUP.C) depuis pickup.cpp:671 (socle statique puis item plinth, sentinelle PC NO_ITEM remplacee par -1). Build-gameplay59 SHA256 19e95b6420170bbde89734f357498da44819d64ee6122f90bad98a9e95d770e7, 4177 tests PASS, validation runtime insertion cle/medipack a faire. Sous-systeme corde non traite: ROPE.C ne fait que 58 lignes (SaveRope/LoadRope/Straighten vide/StraightenRope), il manque _Straighten, RopeControl/ControlRope, RopeList/Ropes, LaraClimbRope, UpdateRopeSwing, DelAlignLaraToRope (~700 lignes depuis rope.cpp) - chantier dedie. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum hang: port de LaraHangLeftCornerTest et LaraHangRightCornerTest depuis TOMB5pc game/lara.cpp (5492/5339). ANIM_GRABLEDGE PC96 -> ANIMATION_LARA_HANG_IDLE 96; calculs de coin ^1023, LeftClimbTab/RightClimbTab, IsValidHangPos, LaraFloorFront, lara.CornerX/Z; branches climb_status et hang simple conservees. Build-gameplay59 SHA256 d17c247b1a31b6d7847503c1967015b4adc1148176caf37e46cd55a4828fc303, 4177 tests PASS. Validation runtime de la transition STATE_LARA_CLIMB_CORNER_LEFT_INNER/OUTER encore a faire: le harnais force l'etat HANG mais le trigger CAMERA:0 de la corniche relance une cutscene qui court-circuite DrawRooms/LaraControl, donc l'entree n'est pas traitee; verifier en jeu normal sur une corniche avec un vrai coin. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum: TestLaraVault portee mais ne debloque pas la corniche. Au bord nord 43685,768,52325 face nord, Action+Up laisse state=2 sans deplacement. Raison dans TestLaraVault: slope=abs(left_floor2-right_floor2)>=60; autour de la corniche 1x1 les sols gauche/droite sont des puits a profondeurs differentes (room26/14), donc slope vrai et retour 0 avant le vault 2 clics; la marche de 512 (front_floor=-512) n'est pas grimpable ici. Sondes par sauvegarde: le patch TOMB5.SAV fonctionne mais apparition couloir room8 (42496,256,51712 ou 40835,256,51304 room8) -> boucle 100% CPU avant premier DrawRooms, ecran fige; apparition passage nord room12 (42000,2048,50600 ou 51000 room12) -> UpdateLaraRoom remonte Lara en room92 y=-1024. Ce n'est pas un couloir horizontal a 2048 mais un puits vertical vers room92. room92 observee: petit sol pierre -1024 derriere grille metallique donnant sur l'arene (balcon de la grande salle); room25 meme niveau -1024 ouverte sur room8. Conclusion: le doorsill n'est pas le passage nord a 2048, il implique room92/25 au-dessus; route exacte corniche->doorsill->crawlspace a etablir. Seule sauvegarde de reprise fiable: corniche 43364,768. Aucune correction gameplay speculative. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-15

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-15T23:59:00+01:00. Linux32 provisoire.

The Colosseum: port de TestLaraVault depuis la source PC (vault 2/3 clics, saut vertical, LaraTestClimbStance) - build-gameplay59 SHA256 2ee56425, 4177 tests PASS, validation runtime a faire. Harnais rapide: TOMB5_AUTOLOAD=1 recharge TOMB5.SAV au titre (PortSave_Read/ApplyPending), niveau 3 atteint en ~60s via vpad FIFO; format v4 offsets x8620 y8624 z8628 yrot8634 room8638 checksum8654 FNV-1a, patching de position possible. Demarrage instable: parfois blocage sur [New Thread] sans EMU init, relancer. Geometrie puits: corniche room12 43109,768 seule cellule floor=768; voisines floor=1024 pit_room=26 puis room26 pit_room=14; spawn 42000,1024,52224 chute a y=5888 room14 -> le grand sol visible est le fond du puits. Au-dessus sky_room=8; saut vertical atteint la grille room8 a y=256 (FallingBlockFloor item+256); sol room8 trou pit_room=12 couvert par 12 dalles CRUMBLING_FLOOR. Saut nord depuis corniche: LaraDeflectEdgeJump CT_FRONT front_floor=-512 front_ceiling=-4102, la sonde touche une dalle room8 a 43520,0,51712 (marche de 512 au-dessus) -> saut deflechi; le doorsill ne peut pas etre atteint depuis la corniche, il faut venir du couloir room8 y=256. Passage nord room12 xx3/4 zz0 floor=2048 ceiling=1024: candidat doorsill/crawlspace sous le couloir. Room92/25 floor=-1024 (room92 = balcon derriere grille sur l'arene), room26 ~2816-3072, room27 ~2816, room14 5120-6144 lave. Bouton room0 57400,7680,52736: salle sombre avec squelette, trigger r0 xx2 zz3 57344,52224 key=0; Action sur la cellule n'a pas lance l'animation (state=2), position exacte a determiner. Spawn room6 60928,6400,49664 -> SIGSEGV InterpolateMatrix_AI ANIMITEM.C:1502 (fragilite port). Prochaine etape: depuis le couloir room8 y=256, bord nord au-dessus du passage x40960..43008 z~51200, se laisser tomber/reculer avec Action pour accrocher le seuil a 2048, shimmy gauche, coin, crawlspace, bouton, issue. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum cause blocage corniche: corniche creux y=768 entoure de cellules floor=1024 (marche de 256); ni Up, ni Action+Up, ni Up+Saut (GRAB_TO_FALL) ne la franchissent. Cause identifiee: TestLaraVault GAME/LARA.C a tout le code PSX dans #if 0 et termine par return 0; c'est cette fonction qui gere le vault/step-up. Sans elle toute marche de 256 est un mur et les sauts sont deflechis. Prochain travail moteur: porter TestLaraVault depuis le bloc ASM PSX present dans le fichier (ou source PC), puis revalider la corniche et les marches du niveau. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum point de reprise rapide corniche: F5 fonctionne en jeu et ecrit TOMB5.SAV [SAVE] wrote TOMB5.SAV: level 3 room 12 X 43364 Y 768 Z 52325. F6 refuse pendant le jeu (load ignored during gameplay; press F6 at the title); rechargement rapide seulement au titre. Pour les experiences d'accroche: relancer le jeu et F6 au titre, plus court que refaire le gouffre. Corniche cul-de-sac a l'ouest (mur) et bordee de trous pit_room=26 au nord/sud (floor=1024, pit en zz1/zz3). Doorsill a chercher depuis la plateforme 1024 ou l'autre cote du puits. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum corniche mur franc ouest: depuis 43364,768 puis marche a 43109,768,52325 room12 yrot=-16384, la cellule xx4 41984..43008 est un mur (floor=1024 ceiling=0 masse pleine). Action+Up aucun deplacement state2; Up seul bloque state2; Up+Saut state15 puis state14 GRAB_TO_FALL, saut deflechi par LaraDeflectEdgeJump, pas d'accroche. Le passage ouest depuis la corniche n'est pas le hang attendu; la fosse visible en contrebas correspond aux rooms 26/14; le doorsill doit etre le rebord de la plateforme 1024, a atteindre depuis l'autre cote room8/relief ou via exploration nord/sud de la corniche. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum session visuelle dalles inertes: objects[CRUMBLING_FLOOR].control=0 au chargement niveau3 garde les dalles solides; Lara parcourt de facon fiable 40000,0 -> 43931,768 room12 sans mourir. Harnais: xdotool ne delivre les touches que si windowactivate --sync puis windowfocus --sync juste avant chaque touche; import vole le focus; le bp CF W w>=160 detache GDB trop tot. Cartographie: grande salle de pierre, grande porte bois/portcullis fermee (issue), banniere rouge, fenetre grillagee; fosse de lave au centre/bord avec corniche; de l'autre cote du petit gouffre le relief vert etoile + bloc rouge (deja atteint par chute); niches sombres laterales candidates crawlspace. Les sauts depuis le bord n'ont pas franchi le petit gap (Lara reste au bord). Prochain: saut lance de plus loin ou accroche du rebord d'en face puis shimmy vers la niche de gauche. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum reproductibilite franchissement (hangA/B/C-20261114): trois tentatives, le franchissement du gouffre est tres sensible au timing; selon le saut Lara retombe dans la fosse state=8 y~5888 avant la corniche. Le saut reussi de crumble6 n'est pas reproductible a volonte en temps reel; le teleport direct 43109,768 est reecrit par UpdateLaraRoom vers room8 42593,256 donc inutilisable. Pour etudier l'accroche: save/load F5/F6 apres corniche, ou desactiver les dalles pendant le test, ou pilotage par numero de frame. Les tentatives d'accroche (marche Action, saut Action, Action+Back) n'ont pas encore ete executees depuis la corniche reelle. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum precision accroche: LaraDeflectEdgeJump GAME/LARA.C; state=14 GRAB_TO_FALL observe en sautant depuis la corniche 43109,768 correspond a un saut qui heurte une face avant CT_FRONT avec mid_floor<=128: Lara rebondit et retombe, pas d'accroche. L'accroche reelle est dans lara_col_reach si IN_ACTION maintenu et LaraTestEdgeCatch renvoie une arete edge=(pos.y+bounds[2])&-STEP_L. Depuis cette corniche le saut avec Action percute le mur du puits; bonne approche a determiner (bord exact, saut sans Action puis Action, ou chute controlee) et a tester avec retour visuel. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum correction d'interpretation axe Y: dans le moteur TR Y croit vers le bas; les suites 2522->4095->5789->6144 apres le rebord sont une chute dans la fosse de lave, pas une propulsion. Morts a 43513,6015 / 41719,5980 / 40337,6144 = chutes au fond du puits. FallingBlock (pos.y_pos += item_flags[1]) fait bien descendre les dalles; l'interpretation montee des notes precedentes est corrigee. Route: apres le gouffre, marcher ouest depuis la corniche 43109,768 descend sur la plateforme floor=1024 puis les trous pit_room=26 de room12 jusqu'a la lave. Passage correct = accroche au rebord puis shimmy depuis le bord exact. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum cause racine afflux ItemNewRooms: RemoveActiveItem utilise une boucle predecesseur correcte mais KillItem et KillEffect utilisaient une boucle fautive qui ne retire pas l'element de la chaine (reecrit son propre next_active). L'element tue reste dans la liste active; item->active=FALSE puis AddActiveItem le reinsere => doublons chaque frame => FallingBlock appele des centaines de fois => ItemNewRoomNo>256. Correctif meme schema que PC/RemoveActiveItem: KillItem liste active + liste items de room; KillEffect liste active FX + liste FX de room. Validation watch4-20261114 build SHA256 74bcbe08beea961af02fc408b10fb118decba9c22f69924715735b7e74a27348: aucun INRN BAD (>200), aucun GFLC128, aucun DOLEVEL parasite, seul name=3 normal. Corruption memoire eliminee a la racine (garde-fou <256 conserve). Lara meurt ensuite a 40337,6144 room14 sur le chemin brulure/lave, probleme distinct. 4177 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum correctif debordement ItemNewRooms: watchpoint watch2-20261114 montre que pendant la chute des dalles FallingBlock->KillItem fait depasser ItemNewRoomNo 200 (201,202,203...) ; la file ItemNewRooms[256][2] deborde et ecrase gfLevelComplete a 128, gfCurrentLevel=18, DoLevel name=121, fin du process. Correctif defensif: toutes les ecritures ItemNewRooms bornees par ItemNewRoomNo<256 (EffectNewRoom, KillEffect, KillItem, ItemNewRoom dans GAME/ITEMS.C et SPEC_PSXPC_N/COLLIDE_S.C). Validation watch3-20261114: meme sequence, build SHA256 1276c879abd1b116efeae11152654c772de38bec1eb0bbad58f98736bfd1211c, aucun GFLC128, aucun DOLEVEL parasite, jeu reste niveau 3, Lara vivante 40037,256,52540. 4177 PASS. Cause racine de l'afflux (>200 entrees/frame) a identifier: boucle/doublons liste active des dalles. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum analyse statique transition corrompue: gfCurrentLevel=18 car gfStatus==3 fait gfCurrentLevel=gfLevelComplete et gfLevelComplete=128 (0x80), impossible pour une fin normale (gfCurrentLevel+1). gfCurrentLevel=18 sort de gfScriptOffset[] et DoLevel recoit un couple garbage (name=121). Aucune affectation normale de gfLevelComplete ne produit 128: corruption memoire (octet ecrase). Piste: instrumenter gfLevelComplete et structures voisines pendant l'effondrement/chute, ou build entierement propre. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum geometrie puits + exploration visuelle: dump grid3-20261114 rooms 8/12/14/26/27. Room12 corniche xx5/zz2 sol 768; cellules xx1..4 zz1..3 floor=1024 pit_room=26 (plateforme +256 et puits). Room8 sols 0 pit_room=12 sky=25. Room26 sols 1024-3072 pit_room=14. Room14 sols ~5120-6144 pit_room=26. Exploration manuelle probe_play2: teleport 43109,768,52540 ouest -> chute room8 42593,256 -> marche a 40314,256 devant relief etoile + bloc rouge (candidat bouton); Action non enregistree (input=0x0) puis DOLEVEL name=121 gfCurrentLevel=18 complete=128 et processus disparu: transition/rechargement corrompu, coherent avec le bug mort/rechargement. Le puits se franchit en tombant 768->256 room8; instabilite de transition = principal obstacle. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum shift-20261114: pendant REACH, ShiftItem ne produit aucun deplacement vertical (shift.y=0), seuls shift.x=-47 lateraux; pourtant pos.y monte 497->545->599->...->1715 et mid_floor decroit 5391->4173 => vitesse verticale negative (vers le haut) sur tout le REACH. Le saut Up+Action+Saut au bord a une trajectoire ascendante anormalement longue: Lara depasse le rebord, monte et meurt plus haut. Ce n'est ni ShiftItem ni un edge geant mais la vitesse du saut/fallspeed en REACH. Prochain essai: saut a l'arret sans Up ou chute controlee depuis le bord avec Action. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum edge2-20261114: au REACH sur le rebord pos=42914,1049,52224 fs=90 front_floor=-281 front_ceiling=-4383 mid_floor=4839 mid_ceiling=-4383 coll_type=1; LaraTestEdgeCatch renvoie 0 (hdif=pos.y+bounds[2] reste dans le meme octet apres fallspeed). Pas d'accroche sur cette frame; la montee observee vient des frames suivantes/ShiftItem dans l'empilement, pas d'un edge geant. La sonde finish a provoque un SIGSEGV artificiel au retour (eax=0): instrumentation non intrusive requise. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-14

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-14T23:59:00+01:00. Linux32 provisoire.

The Colosseum hang6-20261113: saut declenche a 42444,419, accroche state=11 a 42907,1145, puis meme avec input=0x0 Lara monte 2522->4095->5789 en state=9 et meurt a 43513,6015 rooms 26/14. Ce n'est pas le timing d'entree mais la collision/empilement des rooms 12/26/14 qui la propulse vers le haut pendant REACH. Prochaine investigation: lara_col_reach / GetLaraCollisionInfo / ShiftItem dans cet empilement avant toute automatisation hang/shimmy. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum hang5-20261113: avec Action+Up et tap Saut toutes les 0,6s, Lara ne passe jamais en state=10 HANG; chaque accroche state=11 est suivie d'un nouveau saut, d'ou montee du puits jusqu'a la mort 43513,6015,52224. Sequence correcte: un seul saut vers le rebord Action maintenue, puis arret des taps et relachement de Up pour etablir le hang, avant Left (shimmy) et Up+Action (retablissement). L'automatisation ne distingue pas le premier state=11 des suivants depuis le log; il faut un retour d'etat par frame (lecture memoire) au lieu du parsing de log. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum hang3/hang4-20261113: detection d'etat par log state=11 trop grossiere pour declencher le shimmy au bon moment; selon le timing Lara part en diagonale et retombe dans le puits state=8 a 41719,5980,54164 room14. Les accroches state=11 et la montee fonctionnent mais la sequence hang->shimmy->coin->pull-up exigera un pilotage par waypoints/captures au lieu d'un tap+lecture de log. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum suspension (hang2-20261113): avec Action+Up et Saut en boucle pendant la traversee, Lara enchaine les accroches state=11 REACH et monte le puits y258->419->1145->2522->4095->5789->6015 rooms 8/12/26/14 puis meurt state=8 a 43513,6015,52224. Les mecaniques accroche/relevement fonctionnent mais l'automatisation saut+Action grimpe trop haut au lieu du shimmy lateral prevu. Il faut une sequence controlee: une accroche, Left pour longer, passage du coin, Up+Action pour se retablir dans le conduit. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum apres le gouffre (crosswalk/climb-20261113): Lara poursuit jusqu'a 43931,768,52224 room12 puis bute sur l'issue fermee; sauts simples state15/28 retombent au meme point. Passage prevu = rebord au-dessus de la fosse de lave: saut vers l'est avec Action pour s'y suspendre, shimmy gauche, coin, retablissement dans le conduit. Crash intermittent DrawAggregatedSplits LIBGPU.C:436 via VSync->LOAD_VSyncHandler->DrawOTag et pile DEL_CDFS_Read/LoadLevel/DoTitle au demarrage du niveau 3 avant deplacement; le franchissement du gouffre a reussi dans crumble6. Ce crash de transition/rechargement est a traiter separement. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum premier gouffre franchi (crumble6-20261113): le trigger d'effondrement se prend face a l'est y_rot=0x4000. Depuis 40000,0,52224 room12, Lara entre room8, dalles status=1, saut state=3 pendant la chute, reception y=768, poursuite jusqu'a 43931,768,52224 room12. Items 6-12/14-18 actifs puis active=0 (tombes). Aucun SIGSEGV. Le crash FlameControl/DrawAggregatedSplits precedent venait de la direction opposee (marche ouest -> lave derriere le trigger -> mort -> rechargement de niveau corrompu). Le chemin est est franchissable. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum: recompilation TRAPS.C rendue possible (PSXINPUT.H + weak SetLaraPosition/MoveLaraPositionToItem copies de COLLIDE.C dans MOVEBLOK.C, car COLLIDE.C.o build57 les omet). build-gameplay59 SHA256 ef47e93331245163904e384a2c8a8ae92b15e44cf3dd6461e6598d67af7f66f1. Le crash change de forme (crumble4/crumble5-20261113): SIGSEGV reproductible dans DrawAggregatedSplits EMULATOR/LIBGPU.C:436 via VSync->LOAD_VSyncHandler->DrawOTag, taille DEL_CDFS_Read negative (-16388) et pile remontant a DoTitle/LoadLevel. Ce n'est plus FlameControl: l'effondrement+lave corrompent l'etat memoire (FallingBlock/KillItem/effects), symptome dependant de l'objet TRAPS lie. Prochain: instrumentation FallingBlock/KillItem/AddActiveItem/effects avec build entierement propre. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum crash effondrement isole (burn2-20261113): LaraBurn() force au demarrage du niveau cree l'effet de feu (lara.burn=1, effects valide) et ne provoque aucun SIGSEGV dans FlameControl sur 120s. Donc le crash de crumble2 n'est pas le chemin de brulure seul: il depend des items CRUMBLING_FLOOR/FallingBlock et des effets manipules pendant l'effondrement (FlameControl sur slot d'effet corrompu). Prochain: instrumentation FallingBlock/KillItem/RemoveActiveItem pendant l'effondrement avec backtrace registres+pile. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum sols qui s'effondrent: FALLING_BLOCK/FALLING_BLOCK2/CRUMBLING_FLOOR non assignes alors que FallingBlock/Collision/Floor/Ceiling existent dans TRAPS.C. PortInitialiseFallingBlock2 (mesh_bits=1) ajoute dans MOVEBLOK.C car TRAPS.C non recompilable (COLLIDE.C depend de MoveLaraPositionToItem absent des objets build57; GTEREG casse la compilation stricte). SETUP assigne control/collision/floor/ceiling + saves avec cast ABI long*->int*. Runtime crumble/crumble2-20261113: depuis 40000,0,52224 (room12 puis room8 y=256), trigger room14 active items 6-12/14-18 status=1 active=1, y tremble 0->2->7->9. Puis SIGSEGV dans FlameControl (GetLaraJointPos effet de brulure) via QuickControlPhase->ControlPhase: LavaBurn/FlameControl, chemin de brulure incomplet. Prochain correctif: securiser GetLaraJointPos/FlameControl. build-gameplay59 SHA256 9b604c38fceea138c2e96c7d2f6257e20a23ccc69a535108bab9ab5d9fecc965; 4177 PASS. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum premier secret valide (rose99h-20261113): apres push du bloc item100 z54784->53760, teleport Lara a 81408,4864,57400 (decalage collision +356 en Z -> 57756 = cible PickUpPosition item99 a 57856 z-100); maintien Action -> PickUpCollision MoveLaraPosition, state=39 STATE_LARA_PICKUP, item99.status=3 ITEM_INVISIBLE. Golden rose collectee. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-11-13

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-11-13T23:59:00+01:00. Linux32 provisoire.

The Colosseum premier secret: apres push du bloc item100 z54784->53760, Lara replaciee dans la case liberee 79360,4864,54784 face au sud-est marche jusqu'a 81570,4864,58071 room112 sans obstacle (rose99-20261113): passage ouvert. Ramassage golden rose item99 81408,4864,57856 echoue de peu (rose99b-20261113): PickUpCollision->MoveLaraPosition tolerance 256, cible z=57756, arret a z=58022 (delta 266), TestLaraPosition passe. Marche lente Shift_R inoperante dans l'automatisation (input=0x2c0 sans IN_FORWARD); 3 essais suivants bloques sur demarrage titre cutscene11 en boucle. Reste a rejouer en teleportant Lara sur 81408,4864,57756 puis Action. Aucun Done global.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

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

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Ordre du menu pause revalidé à la manette virtuelle : le D-pad doit être émis via les axes hat (ABS_HAT0Y), pas via BTN_DPAD_* que SDL ignore pour le mapping Xbox 360. Avec haty=+1, Game Settings est surligné puis A ouvre l'écran de réglages (moyenne 0,0895). Preuve build/porting/pause-gamepad2-20261029/. Ce n'est pas un défaut du port : les manettes réelles exposent le D-pad en hat. Build-pause SHA256 870166e1030a5399d88271eec135e66e59bbedff03ad485ca9f1827acaba1ae8. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-001 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Débordement SqrtTable trouvé par ASan pendant un soak PAL + manette : global-buffer-overflow dans mSqrt (MATHS.C:152), appelé par sub_2CL1 (LARA1.C:1555) avec un argument négatif. Correctif : clamp des entrées négatives à 0 dans mSqrt/mSqrt_2/phd_sqrt_asm/phd_sqrt_asm_CH/mSqrt_L et accès borné PortSqrtLookup() (0..209) dans MATHS.C/MATHS.H/LIGHT.C/CALCHAIR.C. Vérification GDB/ASan : toutes les variantes retournent 0 pour -1, mSqrt(INT_MAX)=46152, aucun rapport ASan ; soak ASan PAL + manette 571 s sans erreur (pal-asan-soak3-20261029/), crash initial documenté dans pal-asan-soak-20261029/. Smoke normal build-guard2 : scène de Rome rendue (guard-smoke2-20261029/). tests 4174 PASS. Build-pause SHA256 870166e1030a5399d88271eec135e66e59bbedff03ad485ca9f1827acaba1ae8. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Menu pause réordonné : Resume, Game Settings, Quit (Game Settings au-dessus de Quit). Le dispatch existant est conservé (case 2 = Quit, case 3 = Settings) par échange explicite 2↔3 après Requester. Vérifié au clavier : Game Settings ouvre bien SFX/Music/Configure Controls/Screen Adjust/Automatic Targeting ; Quit ouvre la confirmation « Are you sure you want to quit ? ». Preuves pause-order-kbd-20261029/ et pause-quit-20261029/. Build-pause SHA256 870166e1030a5399d88271eec135e66e59bbedff03ad485ca9f1827acaba1ae8; tests/porting+emulator 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Défaut reproductible lié aux stubs : sortir les armes (Y manette) rend la vue 3D entièrement noire, HUD visible ; rengainer (Y) restaure la scène. Cause : CombatCamera (GAME/CAMERA.C:1638) a son corps sous #if 0 || PC_VERSION et tombe sur UNIMPLEMENTED. NTSC : moyennes 0,1018 → 0 → 0,1025, 63 appels CombatCamera. Preuve build/porting/vpad-draw-20261029/. Le combat aux armes est inutilisable, en plus des pickups/interactions déjà bloqués. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-001 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

ASan PAL + manette virtuelle : avec ASAN_OPTIONS=detect_leaks=0, New Game (cutseq name: 1, 2153 occurrences), gamepad détecté et déplacement au stick, exit 0, aucune erreur AddressSanitizer (pal-asan2-20261029/). Avec LeakSanitizer actif, 189290 octets signalés dans libnvidia-glcore.so avec piles driver (aucune frame du port), donc bruit GL et non fuite du jeu (pal-asan-20261029/). Build ASan SHA256 ee0e15dca0cb3cdb8cd53e11932d1c51cbbe0a93ebde3a80caee9d9f3936cb2a. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Soak PAL de 10 minutes avec manette Xbox 360 virtuelle (boutons et stick gauche aléatoires après New Game) : 32 échantillons VmRSS, 74928 Ko constant sur 571 s, exit 0, aucune erreur fatale, scène de rue rendue à 360 s. Preuve build/porting/pal-gp-soak-20261029/. Matériel physique non testé. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Hotplug manette validé en synthétique : contrôleur Xbox 360 virtuel créé après le lancement du jeu, détecté via SDL_CONTROLLERDEVICEADDED ([INPUT] Gamepad 0: X360 Controller), puis A déclenche New Game (cutseq name: 1, 1610 occurrences) et la scène de Rome s'affiche. Preuve build/porting/vpad-hotplug-20261029/. Matériel physique toujours non testé, hot reload du keymap non validé. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Manette validée en synthétique : contrôleur Xbox 360 virtuel créé via /dev/uinput, détecté par SDL (GUID 030081b85e0400008e02000014010000, nom X360 Controller). Le bouton A déclenche New Game (cutseq name: 1) et le stick gauche déplace Lara vers l'arche ; captures 01-after-a.png / 02-after-forward.png. Preuve build/porting/vpad-20261029/. Ce n'est pas une manette physique : hotplug et matériel réel non testés. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

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

PORT-006 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

PAL (SLES_033.31) : New Game confirmé (cutseq name 1, allée de Rome) en maintenant C ~350 ms après un menu interactif vers 45 s ; un tap court est perdu à 50 Hz et laisse partir en DEMO MODE. Sauvegarde PAL round-trip : F5 à level 1 room 0 X 46592 Y 0 Z 31232 écrit 586 octets de niveau, relance + F6 restaure la même position et une scène identique (moyennes 0,1006 / 0,1009). Preuves pal-timing3-20261029/ et pal-save4-20261029/. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-001 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Soak RSS de 15 minutes sur build-cm avec entrées aléatoires et audio dummy : 47 échantillons VmRSS, 75112 → 75560 Ko (+448 Ko, plateau dès 150 s jusqu'à 871 s), états R/S, aucune erreur fatale, exit 0 ; captures à 300 s (inventaire) et 600 s (allée de Rome). Preuve build/porting/soak-rss-20261029/. Tests complets relancés : 4174 PASS avec CPLUS_INCLUDE_PATH/LIBRARY_PATH 32 bits ; sans ces variables les harnais C++ échouent sur bits/c++config.h (prérequis d'environnement). Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-006 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Mise à niveau v3→v4 au niveau 2 : L2.SAV (v3, level 2 room 50 X 91648 Y 0 Z 42496) chargé par F6, puis F5 réécrit le même fichier en v4 (606 octets de niveau, +12 octets d'état d'items). Relance et F6 restaurent le niveau 2, room 50, X 91648 Y 0 Z 42496, scène identique (moyennes 0,0885 / 0,0885). Preuve build/porting/level2-v4-20261029/. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b; tests/porting 497 PASS, tests/emulator 3677 PASS. Aucun Done.

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
