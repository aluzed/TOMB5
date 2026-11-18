# RMIG-010 — Backend Vulkan : pipeline PSX (VRAM, VBO, ordering tables)

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Débloqué par RMIG-009 : le backend Vulkan est sélectionnable et présente. Reste le pipeline PSX complet (texture VRAM 16 bits, vertex buffer, ordering tables, blends, blit).

## Objectif

Rendre la scène PSX complète en Vulkan : une texture VRAM, un vertex buffer dynamique, un draw par passe.

## Faits établis

L'implémentation actuelle garde la VRAM 1024×512 en une texture RG8, pousse les Vertex (position, uv+couleur+dither, couleur, z, w) dans un VBO dynamique et émet un glDrawArrays par ordering table, sans depth test, avec glBlendFunc variable.

## Périmètre

Texture VRAM, transfert des vertices par frame, pipelines par mode de blend, absence de depth, préservation de l'ordre des OT.

Hors périmètre : Compilation des shaders (ticket suivant), SSR/RT.

## Tâches

- [ ] Uploader la VRAM comme texture persistante et gérer les mises à jour partielles.
- [ ] Créer le buffer dynamique de vertices et les pipelines de blending PSX.
- [ ] Émettre un draw par ordering table et vérifier l'ordre d'affichage.

## Critères d’acceptation

- La scène s'affiche sans artefacts de transparence ni d'ordre.
- Le nombre de draw calls par frame reste égal au nombre d'ordering tables utilisées (pas d'explosion).

## Validation

Comparaison d'image avec la référence RMIG-007 + compteur de draw calls.

## Inconnues

Gestion du dithering et des coordonnées 16 bits dans le format de vertex.

## Estimation

3 à 5 jours-personne.

## Dépendances

- RMIG-009

## Preuves

- à produire (aucune mesure pour l’instant)

## Références

- `EMULATOR/EMULATOR.C:2244` (buffer dynamique)
- `EMULATOR/EMULATOR.C:3220` (modes de blending)
