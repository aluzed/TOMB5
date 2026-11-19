# RMIG-023 — Écart 32 bits / 64 bits : primitives d'effet et fondu d'écran

Status: **Todo** — priorité P1 — confiance Medium

Avancement : Cause localisée : ni le rendu, ni les textures (VRAM identique hors framebuffer), ni les données d’animation (hash identique). Les inputs de Lara sont identiques (anim/frame/frac/pos/rot/mesh_bits) mais la table `bones` diffère (hash af81e4cb vs a7f7b6f6, décalage visible mot à mot) et les matrices de joints divergent (~1,7° de rotation, ~0xA3 de translation) : les tests d’écrêtage de sub_658L1 éliminent donc un nombre différent de triangles. Le tableau `bones` est converti en `long` hôtes (8 octets) depuis les mots 32 bits du fichier ; un code qui le lit/écrit avec des hypothèses 32 bits décale les rotations. Reste : auditer les accès à `bones` (CALCLARA.C, DELSTUFF.C, HAIR.C, SETUP.C) et revérifier l’égalité des dumps.

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

## Références

- `GAME/TOMB4FX.C:950` (Fade() et l'état ScreenFade/dScreenFade)
- `GAME/TOMB4FX.C:137` (SetScreenFadeOut / SetScreenFadeIn)
- `EMULATOR/LIBGPU.C:894` (ParsePrimitive / histogramme des codes)
- `SPEC_PSXPC_N/DRAWPHAS.C:332` (journal [DRAW] (fade, persp))
