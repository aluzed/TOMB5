# Migration 64 bits + backend Vulkan (plan)

Décision du 17 novembre 2026 : **migrer d'abord en 64 bits**, puis remplacer
OpenGL par Vulkan, avec un menu debug ImGui (F12) et, à terme, du
raytracing matériel + des niveaux de reflets.

## 1. Pourquoi 64 bits d'abord : preuve mesurée

Sonde Vulkan compilée dans les deux largeurs (`32`/`64`), sur la machine
cible (RTX 2080 Ti, driver 580.178, Vulkan 1.4.312) :

| binaire | GPU | extensions RT |
| --- | --- | --- |
| **-m32** | RTX 2080 Ti (233 ext) | **aucune** : pas de `VK_KHR_acceleration_structure`, `VK_KHR_ray_query`, `VK_KHR_ray_tracing_pipeline` |
| -m32 | llvmpipe (CPU) | toutes (RT logiciel, hors temps réel) |
| **-m64** | RTX 2080 Ti (248 ext) | **toutes** + `VK_NV_ray_tracing`, `VK_NV_ray_tracing_invocation_reorder` |

NVIDIA ne fournit donc plus de RT dans son ICD 32 bits : le raytracing
matériel **exige** un binaire 64 bits. Utilitaire de vérification :
`/tmp/opencode/vkprobe/probe2.c` (même source compilée `-m32` et `-m64`).

## 2. État mesuré de la compilation 64 bits

Inspection `-m64 -fsyntax-only` sur les sources du jeu :

- **GAME/** : 200 fichiers compilés, **4 en erreur**, 16 erreurs au total :
  | fichier | erreurs |
  | --- | --- |
  | `GAME/COLLIDE.C` | 7 (dont `EMULATOR/GTEREG.H:33` + `anims` non déclaré) |
  | `GAME/SWITCH.C` | 5 (`TestCollision`, `GLOBAL_inventoryitemchosen`, `GLOBAL_enterinventory`) |
  | `GAME/NEWINV2.C` | 3 (`LaraGun`, `bUseSpotCam`, `bTrackCamInit`) |
  | `GAME/OBJLIGHT.C` | 1 (`GetFloor`) |
- Volume `long` : ~**995** occurrences dans `GAME/*.C` + `SPEC_PSXPC_N/*.C`.
- En-têtes de données PSX : `SPEC_PSXPC_N/STYPES.H` 52 `long` + 39
  `unsigned long`, `GAME/TYPES.H` 148 + 14 — **c'est là que se situe le
  vrai risque** (layout des structures relogées/lues depuis le niveau).

Commande de reproduction :

```sh
g++ -m64 -fsyntax-only -fpermissive -w \
  -DBETA_VERSION=0 -DDEBUG_VERSION=0 -DDISC_VERSION=1 -DNTSC_VERSION=1 \
  -DPSXPC_TEST=1 -DPSX_VERSION=1 -DRELOC=0 -DUSE_32_BIT_ADDR=1 \
  -I SPEC_PSXPC_N -I GAME -I EMULATOR -I /usr/include/SDL2 -std=c++11 GAME/CONTROL.C
```

## 3. Risques réels (au-delà de la compilation)

1. **Layouts PSX** : `long` (64 bits en LP64) dans `ITEM_INFO`,
   `room_info`, `FLOOR_INFO`, `ANIM_STRUCT`, `BOX_INFO`, `OBJECT_INFO`,
   `SAVEGAME_INFO`… Ces structures sont relogées depuis le fichier de
   niveau (`LoadLevel`) et comparées par `sizeof`. Sur LP64, les tailles
   changent ⇒ décalages silencieux.
2. **Conversions pointeur↔entier** : `(long)ptr`, `(int)ptr`,
   stockage de pointeurs dans des champs `long`.
3. **Adresses émulées** : `USE_32_BIT_ADDR` concerne l'espace
   d'adressage PSX (tags GPU, scratchpad `0x1F800000`), pas les pointeurs
   hôtes — à ne pas confondre, mais à vérifier champ par champ.
4. **Assembleur/ intrinsics** : `GTEREG.H`, matrices `MATHS`, `CALCLARA`
   (assembleur PSX réécrit) — contrôler les registres supposés 32 bits.
5. **Sauvegardes** : format `T5P2` v4 (8658 octets) avec des offsets
   fixes ; il devra rester lisible (ou être versionné).

## 4. Stratégie de migration (ordre proposé)

**Étape A — types à largeur fixe (mécanique, vérifiable).**
Introduire dans les en-têtes de données PSX des typedefs explicites
(`psx_i32`, `psx_u32`) et convertir **uniquement les structures de données
PSX** (`STYPES.H`, `TYPES.H`), pas les `long` locaux. Après chaque en-tête
converti : vérifier les tailles avec des `static_assert` sur les structures
critiques (elles portent déjà les offsets en commentaire, ce qui fournit la
référence).

**Étape B — code qui manipule ces champs.**
`LoadLevel`/relocation, `sgRestoreGame`, `ITEM_INFO` writers,
`room_info`. Puis les 4 fichiers en erreur de compilation.

**Étape C — pointeurs.**
Remplacer `(long)ptr` / `(int)ptr` par `(uintptr_t)`/`(intptr_t)`.

**Étape D — cible de build 64 bits.**
Nouvelle option CMake (`-DTOMB5_64=ON`) : pas de `-m32`, SDL2 64 bits
(système, 2.30), **pas de GLEW** (Vulkan le remplace), Vulkan loader
`/usr/lib/x86_64-linux-gnu`.

**Étape E — backend Vulkan** (le renderer GL ne survit pas au 64 bits faute
de GLEW 64 bits dans l'environnement, donc E accompagne D) :
- abstraction `renderer_*` : init, frame begin/end, `draw_triangles`
  (start, count), `set_blend`, `present` ;
- reprise de l'architecture existante : VRAM 1024×512 en une texture
  (R8G8), un VBO dynamique par frame, **un draw call par passe d'ordering
  table**, pas de depth, blending PSX ;
- shaders GLSL actuels (`gte_shader_4/8/16`, `blit_shader`) portés en
  SPIR-V, correction de perspective comprise ;
- présentation : swapchain SDL2/Vulkan (ou `VK_KHR_xlib_surface`).

**Étape F — ImGui** (toujours compilé, bascule **F12**) : overlay
SDL2+Vulkan, toggles RT/reflets/qualité, stats de frame, plus tard
inspection VRAM/GTE.

**Étape G — reflets et RT.**
1. SSR (post-process, indépendant du GPU) avec presets « off / bas / moyen /
   haut » ;
2. RT matériel derrière détection d'extension (`VK_KHR_ray_query` +
   `VK_KHR_acceleration_structure`), qualité par presets, fallback SSR
   automatique (indispensable : llvmpipe et le 32 bits n'ont pas la même
   exposition d'extensions).

## 5. Validation

- `pytest tests/porting tests/emulator` (4183 tests) à chaque étape ;
- sondes runtime existantes (`probe_sanity.gdb`, corniche 201 frames) ;
- comparaison pixel à pixel GL (32 bits) vs Vulkan (64 bits) sur une
  capture figée, avant de supprimer définitivement l'ancien chemin ;
- suivi dans `docs/porting/backlog.json` (`runtime_milestones`).

## 6. État actuel

Aucune modification de code n'a encore été faite pour cette migration :
ce document est le point de départ, avec l'inventaire mesuré ci-dessus.
