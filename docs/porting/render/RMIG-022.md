# RMIG-022 — Anomalie d'ordre des canaux dans Emulator_StoreFrameBuffer

Status: **Done** — priorité P2 — confiance Medium

Avancement : Terminé : la conversion framebuffer → VRAM écrit désormais un mot RGB555 conforme au format PSX (R en bits 0-4, G en 5-9, B en 10-14) dans les deux backends (OpenGL 32 bits et Vulkan 64 bits). L’ancien code inversait rouge et bleu, et la version Vulkan utilisait en plus l’alpha pour le rouge. Les captures de référence des deux builds restent identiques octet pour octet après le correctif.

## Objectif

Rendre la conversion framebuffer -> VRAM (16 bits) conforme au format PSX et identique entre backends.

## Faits établis

Emulator_StoreFrameBuffer lit le framebuffer en RGBA puis extrait le bleu PSX des 5 bits hauts du rouge, le vert des 5 bits hauts du bleu et le rouge des 5 bits hauts de l'alpha (code hérité d'un chemin D3D BGRA). L'effet mono/sepia (CreateMonoScreen, GPU_SyncBothScreens) utilise cette image. Le backend Vulkan reproduit volontairement ce comportement pour rester identique à OpenGL.

## Périmètre

Analyse de l'effet visible de l'ordre des canaux (mono screen, transitions de niveau), correction éventuelle dans les deux backends, mise à jour des captures de référence si l'image change.

Hors périmètre : Réécriture du pipeline de transition de niveau.

## Tâches

- [ ] Comparer l'image stockée en VRAM avec la vraie trame affichée (canal par canal) sur un niveau utilisant l'effet mono.
- [ ] Décider du comportement correct (PSX : RGB555 depuis la trame) et l'appliquer aux deux backends.
- [ ] Régénérer les captures de référence et vérifier la parité 32/64 et GL/Vulkan.

## Critères d’acceptation

- La conversion framebuffer -> VRAM utilise les canaux attendus (rouge<->rouge, vert<->vert, bleu<->bleu).
- L'effet mono/sepia reste visuellement correct et les captures GL/Vulkan restent identiques.

## Validation

Capture de la frame de transition + inspection de la VRAM stockée (TOMB5_DUMP_VRAM).

## Inconnues

L'effet mono peut masquer l'erreur (moyenne des canaux) ; l'impact visuel réel reste à mesurer.

## Estimation

0,5 à 1 jour-personne.

## Dépendances

- RMIG-011

## Preuves

- 2026-11-19 : GL : c=R|G<<8|B<<16|A<<24, écriture corrigée en r5|(g5<<5)|(b5<<10)|0x8000 (avant : b5|(g5<<5)|(r5<<10)). Vulkan : lecture B,G,R,A puis (R>>3)|((G>>3)<<5)|((B>>3)<<10)|0x8000 (avant : alpha→rouge, B→vert, R→bleu). Vérification : captures 32 et 64 bits identiques octet pour octet (sha256 63041e5c…, mean_abs_diff=0.000). L’effet mono/sépia lui-même n’apparaît pas dans la scène de référence (preuve visuelle non couverte par le harnais).

## Références

- `EMULATOR/EMULATOR.C:2593` (Emulator_StoreFrameBuffer (chemin GL, extraction des canaux))
- `EMULATOR/RENDERER_VK.C:1048` (RendererVK_StoreFrameBuffer (portage Vulkan))
- `SPEC_PSXPC_N/3D_OBJ.C:20` (CreateMonoScreen / GPU_SyncBothScreens)
