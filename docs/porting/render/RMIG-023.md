# RMIG-023 — Écart 32 bits / 64 bits : primitives d'effet et fondu d'écran

Status: **Todo** — priorité P1 — confiance Medium

Avancement : Analysé et localisé (voir plan §40) : primitives d'effet 0x34/0x62/0xE1 et état de fondu divergents. Correction à faire.

## Objectif

Rendre au build 64 bits les primitives d'effet émises par le build 32 bits (et l'état de fondu) pour que les deux builds affichent la même scène.

## Faits établis

Sur la scène de référence (niveau 3, 300 frames), les 977 premiers ordering tables sont identiques entre 32 et 64 bits ; à partir du premier OT de jeu le 32 bits émet 31 triangles gouraud semi-transparents (0x34), 1 sprite semi-transparent (0x62) et 1 image-load (0xE1) de plus par frame, toutes les autres primitives (0x3C, 0x50, 0x60) étant identiques. Le journal [DRAW] montre en 32 bits fade=239/0 fading=1 contre fade=0/0 fading=0 en 64 bits, et persp 306 contre 256. PC_VERSION n'est pas défini dans SPEC_PSXPC_N, donc Fade() s'exécute dans les deux builds. Ce n'est pas un écart de pipeline couleur : à vertices identiques, les pixels sont identiques (Vulkan == GL 64 bits au pixel près).

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

- à produire (aucune mesure pour l’instant)

## Références

- `GAME/TOMB4FX.C:950` (Fade() et l'état ScreenFade/dScreenFade)
- `GAME/TOMB4FX.C:137` (SetScreenFadeOut / SetScreenFadeIn)
- `EMULATOR/LIBGPU.C:894` (ParsePrimitive / histogramme des codes)
- `SPEC_PSXPC_N/DRAWPHAS.C:332` (journal [DRAW] (fade, persp))
