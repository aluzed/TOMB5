# RMIG-022 — Anomalie d'ordre des canaux dans Emulator_StoreFrameBuffer

Status: **Todo** — priorité P2 — confiance Medium

Avancement : Constat documenté pendant le portage Vulkan ; comportement identique conservé entre GL et VK en attendant l'analyse.

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

- à produire (aucune mesure pour l’instant)

## Références

- `EMULATOR/EMULATOR.C:2593` (Emulator_StoreFrameBuffer (chemin GL, extraction des canaux))
- `EMULATOR/RENDERER_VK.C:1048` (RendererVK_StoreFrameBuffer (portage Vulkan))
- `SPEC_PSXPC_N/3D_OBJ.C:20` (CreateMonoScreen / GPU_SyncBothScreens)
