# RMIG-008 — Abstraction renderer (interface + sélection)

Status: **Blocked** — priorité P1 — confiance Medium

Avancement : Bloqué par la cible 64 bits.

## Objectif

Isoler les neuf points d'entrée du rendu derrière une interface, pour brancher Vulkan sans toucher au jeu.

## Faits établis

Le rendu est déjà regroupé dans EMULATOR/EMULATOR.C (init, upload VRAM, vertex buffer, draw triangles, blending, swap) avec des #if OGL/D3D. Aucune abstraction commune n'existe.

## Périmètre

Interface renderer_* (init, frame begin/end, upload texture, update vertices, draw, blend, present) et implémentation OpenGL existante branchée dessus.

Hors périmètre : Vulkan lui-même.

## Tâches

- [ ] Définir l'interface et ses invariants (un draw par ordering table, pas de depth, blending PSX).
- [ ] Brancher l'implémentation OpenGL actuelle derrière l'interface sans changer le rendu.
- [ ] Vérifier la parité visuelle avec la référence RMIG-007.

## Critères d’acceptation

- Le jeu se comporte à l'identique via l'interface (capture identique à la référence).
- Aucun appel GL ne subsiste hors de l'implémentation du backend.

## Validation

Capture comparée + grep des appels GL hors backend.

## Inconnues

Fuites d'état GL (blend, scissor) entre passes.

## Estimation

1 à 2 jours-personne.

## Dépendances

- RMIG-002

## Preuves

- à produire (aucune mesure pour l’instant)

## Références

- `EMULATOR/EMULATOR.C:3534` (Emulator_DrawTriangles)
- `EMULATOR/EMULATOR.C:2240` (texture VRAM)
