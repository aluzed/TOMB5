# Render migration (64 bits / Vulkan) — suivi

Backlog vivant de la migration du rendu : passage en 64 bits, remplacement d'OpenGL par Vulkan, overlay ImGui (F12), puis reflets SSR et raytracing matériel. Distinct du lot initial figé du 13 septembre (`backlog.json`) : ici les statuts évoluent et chaque ticket doit porter une preuve avant d'être déclaré Done.

| id | ticket | statut | prio |
| --- | --- | --- | --- |
| [RMIG-001](render/RMIG-001.md) | Étude 32 vs 64 bits du raytracing Vulkan | Done | P0 |
| [RMIG-002](render/RMIG-002.md) | Cible de build 64 bits sans dépendance 32 bits | Done | P0 |
| [RMIG-003](render/RMIG-003.md) | Typedefs PSX à largeur fixe et garde de tailles (STYPES.H) | Done | P0 |
| [RMIG-004](render/RMIG-004.md) | Conversion des structures de GAME/TYPES.H | Done | P0 |
| [RMIG-005](render/RMIG-005.md) | Code manipulant les champs convertis | In progress | P1 |
| [RMIG-006](render/RMIG-006.md) | Pointeur↔entier et fichiers en erreur en -m64 | Done | P0 |
| [RMIG-007](render/RMIG-007.md) | Harnais de comparaison 32 bits / 64 bits | Done | P1 |
| [RMIG-008](render/RMIG-008.md) | Abstraction renderer (interface + sélection) | Done | P1 |
| [RMIG-009](render/RMIG-009.md) | Backend Vulkan : instance, device, swapchain, présentation | Done | P1 |
| [RMIG-010](render/RMIG-010.md) | Backend Vulkan : pipeline PSX (VRAM, VBO, ordering tables) | Done | P1 |
| [RMIG-011](render/RMIG-011.md) | Shaders GLSL → SPIR-V (4/8/16 bits, blit, perspective, dither, CLUT) | In progress | P1 |
| [RMIG-012](render/RMIG-012.md) | Parité visuelle et retrait du chemin OpenGL | Done | P1 |
| [RMIG-013](render/RMIG-013.md) | ImGui F12 : overlay, stats et interrupteurs | Done | P1 |
| [RMIG-014](render/RMIG-014.md) | Reflets screen-space à presets | Done | P2 |
| [RMIG-015](render/RMIG-015.md) | Raytracing matériel (ray_query) avec repli SSR | Blocked | P2 |
| [RMIG-016](render/RMIG-016.md) | Menu debug avancé et budget de performance | Done | P2 |
| [RMIG-017](render/RMIG-017.md) | Relocalisation 64 bits des tableaux de pointeurs du fichier | Done | P0 |
| [RMIG-018](render/RMIG-018.md) | Rendu 64 bits : mots PSX 32 bits et buffers bas | Done | P0 |
| [RMIG-019](render/RMIG-019.md) | Zero primitive PSX non geree en 64 bits | Done | P1 |
| [RMIG-020](render/RMIG-020.md) | Cutscene d intro du niveau 1 en 64 bits | Done | P1 |
| [RMIG-021](render/RMIG-021.md) | Campagne 64 bits : parcours du Colosseum | In progress | P1 |
| [RMIG-022](render/RMIG-022.md) | Anomalie d'ordre des canaux dans Emulator_StoreFrameBuffer | Done | P2 |
| [RMIG-023](render/RMIG-023.md) | Écart 32 bits / 64 bits : primitives d'effet et fondu d'écran | Done | P1 |

19/23 terminés.
