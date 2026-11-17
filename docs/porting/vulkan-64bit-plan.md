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

## 7. Suivi par tickets

Le plan est découpé en tickets vivants dans
[`render-backlog.json`](render-backlog.json), rendus dans
[`render/index.html`](render/index.html) (tableau de statut) et une fiche
par ticket (`render/RMIG-xxx.md`). Mise à jour :

```sh
python3 scripts/porting/render_tickets.py          # régénère les fiches
python3 scripts/porting/render_tickets.py --check  # échoue si dérive
```

Règles du backlog : statuts `Todo` / `In progress` / `Blocked` / `Done`,
dépendances explicites et sans cycle, et **un ticket ne passe `Done`
qu'avec une preuve** (entrée `evidence` datée). Les tests
`tests/porting/test_render_backlog.py` verrouillent ces règles et la
non-dérive des fichiers générés.

Chaîne de dépendances principale :

```
RMIG-001 (fait)
RMIG-002 -> RMIG-003 -> RMIG-004 -> RMIG-005
        \-> RMIG-006 -> RMIG-007
        \-> RMIG-008 -> RMIG-009 -> RMIG-010 -> RMIG-011
                                                \-> RMIG-012 (retrait GL)
                                                \-> RMIG-013 (ImGui F12)
                                                      \-> RMIG-014 (SSR)
                                                            \-> RMIG-015 (RT)
                                                      \-> RMIG-016 (debug avancé)
```

## 8. Avancement (17 novembre 2026)

`RMIG-002` et `RMIG-006` sont terminés.

**Configuration 64 bits reproductible** : `scripts/porting/configure64.sh`
construit une cible 64 bits sans `-m32`, avec SDL2 x86-64 du système et un
GLEW 64 bits compilé depuis les sources vendored (`-DGLEW_NO_GLU`, car
`libglu1-mesa-dev` n'est pas installé). Sortie : **ELF 64-bit LSB pie
executable**, `ldd` entièrement x86-64, build complet vert.

**Corrections de portabilité** (16 erreurs `-m64` → 0) :

| fichier | cause | correctif |
| --- | --- | --- |
| `SPEC_PSXPC_N/GETSTUFF.H` | macro `B` de `GTEREG.H` qui dévore les paramètres `DIVFP/MULFP(long A, long B)` | paramètres renommés `X, Y` |
| `GAME/SWITCH.C` | `TestCollision`, `GLOBAL_enterinventory`, `GLOBAL_inventoryitemchosen` non déclarés | ajout `SPHERE.H`, `NEWINV2.H` |
| `GAME/NEWINV2.C` | `LaraGun`, `bUseSpotCam`, `bTrackCamInit` non déclarés | ajout `SPOTCAM.H`, `LARAFIRE.H` |
| `GAME/OBJLIGHT.C` | `GetFloor` non déclaré | ajout `GETSTUFF.H` |
| `GAME/COLLIDE.C` | `anims` non déclaré | ajout `DRAW.H` |

**Première exécution du binaire 64 bits** : il démarre (init émulateur,
audio, vidéo) puis s'arrête sur
`EMULATOR/LIBGPU.C:1141: int ParsePrimitive(uintptr_t): Assertion FALSE`
avec des `Unhandled primitive type: 10/08/07/06/05`. C'est exactement la
signature d'un **décalage de layout** dans le flux de paquets GPU : la
suite logique est `RMIG-003`→`RMIG-005` (conversion des structures PSX),
pas un ajustement du parseur.

**Aucune régression 32 bits** : arbre recompilé vert (0 erreur) et binaire
de hash inchangé (`b9d8e710…`), les correctifs n'ajoutant que des
déclarations.

## 9. RMIG-003 : largeur fixe dans `STYPES.H` (17 novembre 2026)

- `typedef int32_t psx_i32; typedef uint32_t psx_u32;` puis conversion des
  champs de `SPEC_PSXPC_N/STYPES.H` (seul `long` restant : les pointeurs de
  `DB_STRUCT`, structure hôte de buffers, hors données PSX).
- `static_assert` de layout : `DRIP_STRUCT` 24, `TEXTURE` 16,
  `static_info` 28, `REQUESTER` 20, `ITEM_LIGHT` 48 — valables **toutes
  ABI**. Et `room_info` 80, `ITEM_INFO` 144, `object_info` 64,
  `creature_info` 228 **uniquement hors LP64** : ces structures embarquent
  des pointeurs hôtes, leur taille change donc légitimement en 64 bits.
- **Conséquence de conception** (à retenir pour RMIG-004/005) : il ne faut
  pas forcer `sizeof` sur ces structures, mais **lire le format fichier via
  une structure dédiée** (pointeurs 32 bits) et convertir vers la structure
  hôte au chargement.

Résultats mesurés :

| cible | build | binaire | comportement |
| --- | --- | --- | --- |
| 32 bits | vert (0 erreur) | **hash inchangé** `b9d8e710…` | référence intacte |
| 64 bits | vert (0 erreur) | ELF64 | affiche l'écran de démarrage Tomb Raider Chronicles ; plus d'assertion `ParsePrimitive`, il reste des `Unhandled primitive type` (507 en 20 s) |

## 10. RMIG-004 : `GAME/TYPES.H` en largeur fixe (17 novembre 2026)

- Typedefs `psx_i32`/`psx_u32` désormais définis dans `GAME/TYPES.H`
  (inclus par `STYPES.H`) et conversion des 148 `long` + 14 `unsigned long`
  du fichier : `PHD_VECTOR`, `PHD_3DPOS`, `FLOOR_INFO`, `LIGHTINFO`,
  `MESH_INFO`, `OBJECT_VECTOR`, `SPOTCAM`, `lara_info`, `savegame_info`…
- `static_assert` sur les structures sans pointeur : `PHD_VECTOR` 12,
  `PHD_3DPOS` 20, `FLOOR_INFO` 8, `LIGHTINFO` 32, `MESH_INFO` 20,
  `OBJECT_VECTOR` 16, `SPOTCAM` 40 — elles gardent donc le format PSX en
  64 bits.
- Correction induite : `UpdateLightning` (`GAME/CONTROL.C`) parcourait les
  points avec un `long*` ; typé `psx_i32*`.

Résultats :

| cible | build | binaire | rendu |
| --- | --- | --- | --- |
| 32 bits | vert | **hash inchangé** `b9d8e710…` | référence |
| 64 bits | vert | ELF64 | écran de démarrage correct, mais **~594 `Unhandled primitive type` en 20 s** |

Conclusion : le rendu 2D/sprite passe, le flux **3D** reste mal interprété.
Le prochain levier n'est plus le typage des structures de jeu mais la
**lecture du format fichier** : `LoadLevel` caste le buffer de salles
directement en `struct room_info`, qui contient cinq pointeurs (8 octets en
LP64) → décalage de tous les champs suivants. C'est l'objet de RMIG-005
(structure de format à pointeurs 32 bits + conversion).

## 11. RMIG-005 : chargement du format fichier (17 novembre 2026)

Deux mécanismes supposaient des adresses 32 bits. Le premier est traité, le
second est mesuré et découpé.

**1. Arène de jeu sous 4 Gio (fait).** `MALLOC.C` alloue désormais
`malloc_buffer` par `mmap(MAP_32BIT)` en LP64 (allocation statique
inchangée en 32 bits). Les adresses 32 bits stockées dans les blocs relogés
restent donc valides, comme le suppose le moteur.

**2. Format fichier des salles (fait).** `struct room_info_file`
(80 octets, pointeurs en `psx_u32`) décrit le format PSX, avec
`static_assert(sizeof == 80)`. `LoadLevel` lit ce format puis convertit
champ par champ vers `struct room_info` (chemin LP64 uniquement), les blocs
étant relocalisés depuis leur position **dans le fichier**.

**3. Relocalisation des tableaux de pointeurs (reste à faire).** Le binaire
64 bits atteint maintenant `GAME/SETUP.C:1838` et y plante :

```c
((int*)&meshes)[i] += (int)mesh_base + ((((int)meshes[i] + ((int)meshes[i] >> 31)) >> 1) << 1);
```

C'est la première d'une famille `*(int*)&array[i] += base` qui traite des
**tableaux de pointeurs** comme des tableaux d'`int`. En LP64 l'élément fait
8 octets : la lecture et l'écriture sont fausses et la mémoire est corrompue.
Mesure : **487 occurrences de `(int*)&`** dans `GAME/` et `SPEC_PSXPC_N/`
(toutes ne sont pas concernées — certaines portent sur de vrais `int32`).

Ce reste est découpé dans le ticket **RMIG-017** : lister les tableaux
réellement issus du fichier (`meshes`, `frame_ptr` des animations, `models`),
introduire un helper « base + offset 32 bits » et convertir au chargement.
Critère de sortie : un niveau se charge en 64 bits **sans SIGSEGV et sans
`Unhandled primitive type`**, positions d'items identiques à la référence
32 bits.

État des builds à cette étape : 32 bits vert et **hash inchangé**
(`b9d8e710…`), 64 bits vert (compile) mais plante au chargement comme décrit.
