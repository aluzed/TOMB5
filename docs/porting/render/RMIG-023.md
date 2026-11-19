# RMIG-023 — Écart 32 bits / 64 bits : primitives d'effet et fondu d'écran

Status: **Todo** — priorité P1 — confiance Medium

Avancement : Deux causes racines corrigées : `MULFP` non tronquée à 32 bits (caméras flyby) et deux décalages de pointeurs sur `short** meshes[]` (natte : +4 shorts/+8 shorts au lieu de +2/+4 pointeurs ; holsters : `s0 += 8` en `int*`). Écart 32/64 sur la scène de référence : mean_abs_diff 18.730 → **0.225**, pixels à ±8 : 26.12 % → **99.63 %**. Référence 32 bits inchangée (51d3a1c7…), référence 64 bits régénérée (bcc8a642…). Reste 28 triangles 0x34 (et 1 0x3C) non émis en 64 bits, hors des meshes déjà vérifiés identiques — probablement la section armes/back_gun ou la seconde boucle de peau.

## Objectif

Rendre au build 64 bits les primitives d'effet émises par le build 32 bits (et l'état de fondu) pour que les deux builds affichent la même scène.

## Faits établis

Sur la scène de référence (niveau 3, 300 frames), les 977 premiers ordering tables sont identiques entre 32 et 64 bits ; à partir du premier OT de jeu, le 32 bits émet 31 triangles gouraud semi-transparents (0x34), 1 sprite semi-transparent (0x62) et 1 DR_TPAGE (0xE1, changement de page de texture) de plus par frame, toutes les autres primitives (0x3C, 0x50, 0x60) étant identiques. Autrement dit : un effet rendu avec sa propre page de texture n'est pas émis en 64 bits. Le journal [DRAW] montre en 32 bits fade=239/0 fading=1 contre fade=0/0 fading=0 en 64 bits, et persp 306 contre 256 au démarrage. PC_VERSION n'est pas défini dans SPEC_PSXPC_N, donc Fade() s'exécute dans les deux builds. Ce n'est pas un écart de pipeline couleur : à vertices identiques, les pixels sont identiques (Vulkan == GL 64 bits au pixel près).

## Périmètre

Trouver pourquoi l'état de fondu (ScreenFade/dScreenFade/ScreenFading) et les primitives d'effet associées diffèrent au chargement du niveau, puis corriger la cause LP64 sans modifier le rendu commun.

Hors périmètre : Différences de couleur dues au rendu (déjà traitées par RMIG-011/012).

## Tâches

- [ ] Tracer SetScreenFadeIn/SetScreenFadeOut, ScreenFade et dScreenFade au chargement du niveau dans les deux builds.
- [ ] Identifier le code qui émet les primitives 0x34/0x62/0xE1 et pourquoi il est inactif en 64 bits.
- [ ] Corriger la cause (arithmétique LP64, pointeur tronqué, état non initialisé) et revérifier l'égalité des dumps TOMB5_DUMP_VERTS / TOMB5_PRIMHIST.

## Critères d’acceptation

- Les dumps de vertices et les histogrammes de primitives sont identiques entre 32 et 64 bits sur la scène de référence.
- La capture 32 bits et la capture 64 bits (Vulkan) ne diffèrent plus que par les écarts de couleur déjà connus, ou plus du tout.

## Validation

TOMB5_DUMP_VERTS + TOMB5_PRIMHIST + capture_compare.py sur la scène niveau 3 / 1800 frames.

## Inconnues

L'effet peut être déclenché par un compteur de frames ou une temporisation, auquel cas la différence peut être un simple décalage temporel plutôt qu'un bug.

## Estimation

1 à 2 jours-personne.

## Dépendances

- RMIG-012

## Preuves

- 2026-11-19 : Chaîne de preuves : VRAM textures identiques (différences uniquement framebuffer) ; histogramme de prims → 31 triangles 0x34 de plus en 32 bits dont 28 dans la plage Lara ; [LS] anim=103 frame identiques, frac=0 rate=4 identiques, pos/rot/mesh_bits identiques ; hash des données d’animation identique (7b26e60b) ; hash de `bones` différent (af81e4cb vs a7f7b6f6) avec décalage visible ; matrices de joints sensiblement différentes ([MJ] j0/j7). Correctif annexe : TOMB5_SKIP_CUTSCENE appliqué de façon identique dans les deux builds (le bloc GAMEFLOW était sous #if __LP64__).
- 2026-11-19 : Comparaison frame par frame du harnais [LS] (caméra, hash MatrixStack, hash matrices, pos Lara) : identique de n=0 à n=32, première divergence à n=33 (caméra 64 bits à 88576,3200,52736 puis 96854,-867,52573 contre 86572,4076,52735 en 32 bits), retour à la position de n=31 en 64 bits mais décalage persistant. Table `bones` relue correctement (160 entrées, `long` hôte) : identique — l’hypothèse squelette du message précédent est infirmée.
- 2026-11-19 : MULFP (SPEC_PSXPC_N/GETSTUFF.C) : `((result >> 32) << 16)` conservait des bits au-delà de 32 en LP64 ; troncature explicite en 32 bits signés. Preuve : [SC] spline=281474976713275 (64 bits) vs 2619 (32 bits) avant, identiques après ; captures 1800 frames : mean_abs_diff 18.730 → 0.314, 26.12 % → 99.41 % de pixels à ±8. La référence 32 bits ne change pas (51d3a1c7…), la 64 bits devient a1f3d3a6…
- 2026-11-19 : Pointeurs de meshes : natte (s4 + 4 shorts = 2 pointeurs, s1 += 8 shorts = 4 pointeurs) et holsters (s0 = (int*)&meshes[i]; s0 += 8 = 32 octets) convertis en arithmétique d’entrées (short**). Captures 1800 frames : mean_abs_diff 0.314 → 0.225, 99.41 % → 99.63 % à ±8 ; histogramme : 35 → 28 triangles 0x34 manquants. La référence 32 bits ne change pas (51d3a1c7…).

## Références

- `GAME/TOMB4FX.C:950` (Fade() et l'état ScreenFade/dScreenFade)
- `GAME/TOMB4FX.C:137` (SetScreenFadeOut / SetScreenFadeIn)
- `EMULATOR/LIBGPU.C:894` (ParsePrimitive / histogramme des codes)
- `SPEC_PSXPC_N/DRAWPHAS.C:332` (journal [DRAW] (fade, persp))
