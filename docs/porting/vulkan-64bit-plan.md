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

## 12. RMIG-017 : conversions supplémentaires (17 novembre 2026)

Ajouté au chemin LP64 de `LoadLevel` (le chemin 32 bits est intact) :

- `struct anim_struct_file` (40 o, `frame_ptr` en 32 bits) +
  `static_assert`, conversion vers `anims[]` avec
  `frame_ptr = frames + offset` ;
- `struct item_info_file` (144 o, `data` en adresse 32 bits) +
  `static_assert`, conversion vers `items[256]` ; les drapeaux
  (`active`, `status`, `ai_bits`…) sont dépliés **bit par bit** depuis le
  mot 32 bits du fichier, un bitfield n'ayant pas d'adresse ;
- `meshes[]` : lecture du tableau 32 bits du fichier et construction du
  tableau de pointeurs hôtes (base `mesh_base` + offset) ;
- `relocationPtr` typé `psx_i32*` : en `long*`, chaque champ de la table de
  modules était lu sur 8 octets, ce qui donnait des tailles et offsets nuls.

Résultat mesuré : le chargement 64 bits **dépasse** meshes/anims/items et
s'arrête maintenant dans `RelocateModule`. Diagnostic précis :

```
ptr == ptr2 == 0x4019724c        (deux allocations de taille 0)
level->numAiModules = 5  aiModuleIndices[0] = 15   (corrects)
relocationPtr[0..4] = 0,0,0,0,0  → table vide
```

La lecture des 1920 octets de la table de modules
(`DEL_CDFS_Read` dans `tsv_buffer[256]`) ne remplit pas le buffer : c'est le
prochain point à instruire (positionnement CD vs lecture), pas un problème
de layout.

## 13. Sonde CD : la lecture ne ramène que des zéros (17 novembre 2026)

Instrumentation temporaire de `DEL_CDFS_Read`, `CdControlB(CdlSetloc)` et
`CdReadSync`, puis exécution comparée (instrumentation retirée ensuite,
arbre revenu à `HEAD`).

**En 64 bits** (chargement du niveau titre, `Name=0`) :

```
[CD] Setloc sector=2492 off=5861184 fseek=0 ftell=5861184
[CD] CdReadSync fread=1 pos=5863536
[CD] DEL_CDFS_Read addr=0x555555755d60 size=1920
[CD] copied 1920 bytes dst=00000000 src=00000000
```

Le seek et le `fread` **réussissent**, mais les données du secteur sont
nulles : `src` (buffer de pile) est déjà à zéro. Ce n'est donc ni un
problème de pointeur ni de layout.

**En 32 bits**, sur la même session : **aucun** `copied` n'apparaît, c'est-à-
dire qu'aucune lecture non multiple de 2048 octets n'a lieu — le bloc
`if (level->numAiModules != 0)` n'est pas exécuté. Autrement dit, le niveau
titre se charge avec `numAiModules == 0` en 32 bits et `== 5` en 64 bits.

Conclusion : la lecture CD n'est pas cassée ; c'est **le chemin de chargement
du niveau titre qui diffère** avant ce point (les deux binaires ne lisent pas
la même chose), et en 64 bits la table demandée tombe sur une zone nulle de
l'image. Prochaine investigation : comparer pas à pas la séquence de
`DEL_CDFS_Read`/`Setloc` des deux binaires pendant `S_LoadLevelFile(Name=0)`
pour trouver la première divergence de position.

Le reste est inchangé : 32 bits vert et **hash `b9d8e710…`** restauré, 64 bits
vert.

## 14. Le header de niveau lu en 64 bits est déjà corrompu (17 novembre 2026)

Instrumentation temporaire de `S_LoadLevelFile` et du début de `LoadLevel`
(retirée ensuite ; arbre revenu à `HEAD`, hash 32 bits `b9d8e710…` restauré).

**64 bits**, chargement du niveau titre :
```
[LVL] S_LoadLevelFile Name=0
[LVL] header ver=-225 numRooms=116 numAiModules=5 numLevelItems=38 anims=576
```

`objectVersion = -225` (0xFFFFFF1F) n'est pas une version valide : **le
header du niveau est déjà lu au mauvais endroit**. La divergence est donc
*dans `S_LoadLevelFile`*, avant `LoadLevel` :

1. `DEL_CDFS_OpenFile(Name + TITLE)` positionne `cdCurrentSector` à partir de
   `gwLba + (gwHeader.entries[filenum].fileOffset >> 11)` ;
2. `DEL_CDFS_Read(mod, gwHeader.entries[NONE].fileSize)` lit le SETUP.MOD ;
3. `LoadLevel()` lit ensuite `sizeof(struct Level)` (228 o, identique dans les
   deux ABIs).

`struct GAMEWAD_entry`/`GAMEWAD_header` sont `#pragma pack(1)` et ne
contiennent que des `int` : leur layout ne change pas. Les suspects
restants sont donc en amont, dans la séquence CD du démarrage (lecture du
gameflow, `InitNewCDSystem`, position du GAMEWAD), qui diverge entre 32 et
64 bits.

**Prochain test ciblé** : imprimer `gwLba`, `gwHeader.entries[5].fileOffset`,
`gwHeader.entries[NONE].fileSize` et `cdCurrentSector` juste avant la
lecture du header, dans les deux binaires. Si l'entrée GAMEWAD diffère, la
lecture du GAMEWAD est en cause ; si elle est identique, c'est la position CD
héritée du gameflow.

État : 32 bits vert et hash inchangé, 64 bits vert mais toujours en échec au
chargement (702 `Unhandled primitive type` avant le SIGSEGV).

## 15. Premier rendu 64 bits stable : écran titre DEMO MODE (17 novembre 2026)

Série de corrections LP64 déclenchées par le chargement puis le rendu du
niveau titre. Toutes les branches 32 bits sont conservées à l'identique
(`#if defined(__LP64__)` / `#else`).

### Chaine de chargement

1. **Objets/statics** : `LEVEL_OBJECT_DATA_SIZE` utilisait
   `sizeof(struct object_info)` = 96 en LP64, alors que le fichier stocke
   64 octets par objet. La position CD était décalée de 14 720 octets.
   Lecture via `object_info_file` puis conversion (RMIG-018).
2. **Relocalisation** : `RelocateModule` lisait des `unsigned long`
   (8 octets) au lieu de mots 32 bits → offsets aberrants
   (`0x40000000 + Module`). Lecture explicite en `unsigned int`.
3. **Arène** : le niveau titre consomme ~1 061 000 octets en LP64 contre
   ~922 000 en 32 bits ; l'arène LP64 passe à 4 Mio (toujours `MAP_32BIT`).
4. **Salles** : après conversion, `ptr` n'avançait pas au-delà des blocs de
   salle copiés, donc `floor_data`, `meshes`, `anims` et `items` étaient lus
   au milieu des `room_info` brutes. `ptr = blockptr` corrige la position.
5. **Bones** : convertis en tableau de `long` hôtes (sinon `bone += 4`
   avançait de 32 octets au lieu de 16).
6. **Piles de frames** : `GetFrames_CL` écrit deux pointeurs de 8 octets
   dans un `int[2]` (8 octets) → stack smashing ; tableaux de pointeurs
   dédiés en LP64.

Résultat : la trace `TOMB5_TRACE_CD=1` du niveau titre est **identique aux
32 premières lignes du 32 bits** (mêmes `open`/`read`, mêmes secteurs).

### Chaine de rendu

- `unsigned long` vaut 8 octets en LP64 : `P_TAG` passait de 12 à 20 octets
  et `POLY_F3` de 24 à 32, alors que le jeu écrit des primitives PSX 32 bits.
  Introduction de `PSX_ULONG` (32 bits en LP64, `unsigned long` sinon) pour
  les structures de primitives.
- Les buffers GPU (ordering tables, polygones, `tsv_buffer`), les
  scratchpads de rendu (`ANIMITEM`, `ROOMLET*`, `LIGHT`, `DRAWOBJ`) et les
  matrices temporaires (`temp_rotation_buffer`) sont alloués sous 4 Gio via
  `PORT_LowAlloc` (`mmap(MAP_32BIT)`), car le code PSX les tronque en `int`.
- Les listes stashees (`STASHEDOBJ`/`STASHEDDAT`) sont indexées par numéro
  au lieu de pointeurs tronqués.
- Les accès aux matrices globales `lara_matrices` (au-dessus de 4 Gio) ne
  passent plus par un `int`.
- `meshes`/`bones` sont parcourus avec les pas hôtes (macro `ANIM_MESH_PTR`).

### Preuve

- `sizeof(P_TAG) = 12`, `sizeof(POLY_F3) = 24` en 64 bits, identiques au 32 bits.
- Exécution 64 bits de 35 s du mode attractif : **aucun SIGSEGV**, capture
  de fenêtre montrant `DEMO MODE`.
- Les `Unhandled primitive type` passent de **702** à **0–77** selon la
  frame (suivi RMIG-019).
- Suite de tests : **4188 PASS**. Build 32 bits fraîchement configuré et
  compilé (`build/porting/build32-check`) : vert, exécution 40 s sans crash.

Le hash de référence 32 bits `b9d8e710…` n'est pas reproductible depuis un
autre répertoire de build (les chemins DWARF entrent dans le binaire) ; la
non-régression est vérifiée par la compilation fraîche, l'exécution et les
4188 tests.

### Suite

- RMIG-019 : ramener les primitives non gérées à zéro.
- RMIG-007 : harnais déterministe 32/64 (capture + hash).
- Puis RMIG-008 → 011 (abstraction renderer et Vulkan).

## 16. Zéro primitive non gérée (17 novembre 2026)

Après RMIG-018 il restait 46–77 `Unhandled primitive type` par session
(types `0x10`, `0x8C`, `0xFC`, `0xFF`). Le diagnostic gdb a montré que le
parseur lisait des **instructions MIPS** (`27bdffd0`, `afb20018`, …) : la
chaîne de primitives avait dérivé hors du poly buffer.

Cause : les structures `DR_ENV` / `DR_MOVE` / `DR_AREA` / `DR_TPAGE` et les
macros de `LIBGPU.H` utilisaient encore `u_long`, qui vaut 8 octets en
LP64. `sizeof(DR_ENV)` valait 128 au lieu de 64, donc chaque paquet
d'environnement décalait le pointeur de 64 octets et le parseur finissait
dans le code du module AI.

Correction : tous les `u_long` de `EMULATOR/LIBGPU.H` et `LIBGPU.C` sont
remplacés par `PSX_ULONG` (32 bits en LP64), et `setaddr` tronque
explicitement via `uintptr_t` vers le champ 32 bits.

Tailles vérifiées identiques 32/64 bits :

| type | 32 bits | 64 bits |
|---|---|---|
| P_TAG | 12 | 12 |
| POLY_F3 | 24 | 24 |
| POLY_F4 | 28 | 28 |
| POLY_FT3 | 36 | 36 |
| POLY_FT4 | 44 | 44 |
| POLY_GT3 | 44 | 44 |
| POLY_GT4 | 56 | 56 |
| TILE | 20 | 20 |
| SPRT | 24 | 24 |
| DR_ENV | 64 | 64 |
| DR_MOVE | 28 | 28 |

Exécution 64 bits de **120 s** du mode attractif : **0** primitive non
gérée, **0** SIGSEGV. Build 32 bits frais vert et exécuté 40 s sans erreur.

## 17. Niveau 1 atteint en 64 bits, cutscene d'intro bloquée (17 novembre 2026)

Avec des appuis clavier **maintenus** (`xdotool keydown` puis `keyup`), le
menu 64 bits répond : `New Game` lance `DoLevel(Name=1)`, les lectures CD du
niveau se terminent (dernières lectures `12` octets secteur 18231 et `8`
octets secteur 18232). Trois crashs LP64 supplémentaires ont été corrigés
pour arriver là :

1. `SoundEffect` stockait `&LaSlot[...]` dans un `int` : `LaSlot` est
   désormais alloué sous 4 Gio (`PORT_LowAlloc`).
2. `InterpolateMatrix_CL` (chemin interpolé de Lara) passait par
   `t8[13] = (int)lara_matrices` ; les pointeurs hôtes sont utilisés
   directement en LP64.
3. `S_DrawPickup` chaînait l'OT principal vers `&db.pickup_ot[255*2]`
   calculé avec un pas de 8 octets ; l'arithmétique est faite en mots
   32 bits.

État : la cutscene d'intro reste bloquée sur `Handle cutseq triggering
name: 1` (écran noir avec l'icône de chargement), alors qu'en 32 bits la
salle s'affiche et la séquence passe au nom 3. Le niveau est donc chargé
et le processus stable, mais le gameplay niveau 1 n'est pas encore atteint
en 64 bits (RMIG-020).

Tests : **4188 PASS** ; builds 64 et 32 bits verts ; aucune primitive non
gérée sur les sessions de référence.

### 17.1 Diagnostic du rendu noir (niveau 1)

Sonde `TOMB5_DRAWDBG=1` ajoutée dans `DrawRooms` (nom du niveau, salle,
position caméra, taille de salle, `number_draw_rooms`, fade) et
`TOMB5_CUTDBG=1` dans `handle_cutseq_triggering`.

- 64 bits : `gfCurrentLevel=1`, `number_rooms=242`, caméra salle 0
  `(46592,-960,30080)`, `number_draw_rooms=3`, `ScreenFade=0`,
  `ScreenFading=0`. La boucle, le chargement et la fade sont donc normaux,
  mais l'image reste noire (seule une icône 2D apparaît).
- 32 bits, même scénario de touches : `gfCurrentLevel=3` (125 salles, salle 8)
  et la salle s'affiche. Les deux exécutions ne chargent pas le même niveau
  (sélection de menu 32 bits déjà connue comme fragile, `byte_46`).

Prochain test : forcer le niveau 1 côté 32 bits via le level select, puis
comparer caméra/`number_draw_rooms`/fade et, si l'écart persiste, vérifier
la projection LP64 (matrices GTE, `SetGeomScreen`/`SetGeomOffset`).

### 17.2 Projection 3D corrigée, crash restant dans SubPolyGT4RL1

Le rendu noir venait de la **matrice monde→vue** : `matrix_stack`,
`w2v_matrix` et `phd_mxptr` étaient des `long` (8 octets en LP64). Les
écritures (`matrix_stack[9] = ...`) et les lectures (`phd_mxptr[3]`)
n'utilisaient donc plus le même pas, et toute la projection 3D était
fausse. Ils sont maintenant en mots 32 bits (`int`) en LP64.

Autres corrections LP64 de la chaîne de rendu des salles :

- Les roomlets lisaient `x/y/z` et `left/right/top/bottom` via
  `((int*)a1)[5/6/7/14/15]`, offsets valides seulement pour le layout
  32 bits. Ils utilisent désormais les champs nommés (RMIG-020).
- `SubPolyGTLoopRLx` reçoit directement le pointeur de table au lieu de
  déréférencer `t0[0]` (l'adresse d'une variable pointeur globale était
  tronquée) ; les appels ne prennent plus `&QuadVertTableRLx`.
- Les tables de subdivision restent des globales, mais leur valeur est
  passée en pointeur complet.

Résultat : `DrawMeshRL1` est atteint et produit des appels
`SubPolyGT4RL1`. Le crash restant est dans `SubPolyGT4RL1` sur un pointeur
de table tronqué (`0x5572f1fc` au lieu de `0x55555572f1fc` sous gdb).
Prochain pas : tracer la valeur exacte de `QuadVertTableRL1` /
`QuadVertTables[gp]` à l'appel et supprimer le dernier cast `int` de la
chaîne.

#### Outil de test déterministe

`TOMB5_START_LEVEL=<n>` saute le menu et démarre directement le niveau
`n` (chemin de diagnostic, disponible dans les deux builds). Cela réduit
une reproduction de ~90 s à ~40 s.

## 18. La 3D du niveau 1 s'affiche (partiellement)

Après RMIG-020, la chaîne de rendu des salles atteint enfin
`DrawMeshRL1` et dessine des polygones en 64 bits (capture avec surfaces
bleues). Corrections supplémentaires :

- `matrix_stack`, `w2v_matrix`, `phd_mxptr` en mots 32 bits (matrice
  monde→vue correcte).
- Roomlets : `x/y/z` et `left/right/top/bottom` lus par champs nommés.
- `SubPolyGTLoopRLx` reçoit directement le pointeur de table ; plus de
  `t0[0]` sur l'adresse d'une globale.
- `s6 = (int)t0; t0 = (int*)s6;` remplacé par `intptr_t` (sauvegarde du
  curseur de table sans troncature).
- `calc_animating_item_clip_window` : `s1[1]` (porte) et
  `s1[5/7/8/9]` (x/z/minfloor/maxceiling) remplacés par les champs hôtes
  de `room_info`.

Mesure : `[OT] verts=3717 splits=111`, capture avec géométrie visible.
Anomalie restante : la bbox des sommets vaut
`(-32632,-130)-(30848,15472)` au lieu de rester dans
`0..512 × 0..240` ; une partie des polygones a des coordonnées écran
invalides, ce qui laisse la scène majoritairement noire. Prochain pas :
comparer `SXY`/`SZ` des premiers polygones au même endroit que le 32 bits
(même salle/caméra), puis corriger la dernière erreur de projection ou de
base de vertices.

## 19. Le niveau 1 s'affiche correctement en 64 bits

Cause principale des polygones déformés restants : **23 occurrences de
`sizeof(unsigned long)`** utilisées comme pas de primitive
(`a3 += sizeof(POLY_GT4) / sizeof(unsigned long)`, boucle de copie
`MISC.C`, etc.). En LP64 `unsigned long` vaut 8 octets : les primitives
avançaient de 28 octets au lieu de 56, se chevauchaient, et le parseur
lisait des coordonnées UV/couleurs comme des coordonnées écran
(`[VBAD] quad code=3c ... (8224,32)`).

Remplacement global par `sizeof(PSX_ULONG)` (4 octets dans les deux
ABIs).

Résultat :

- `[OT] bbox = (-174,-154)-(628,354)` au lieu de `±32000` ;
- plus aucun `[VBAD]` ;
- capture du niveau 1 : **couloir de Streets of Rome correctement rendu**
  (textures, éclairage, géométrie), 3717 sommets / 111 splits.

Reste à valider : avancée de la cutscene et affichage/contrôle de Lara en
64 bits.

## 20. Niveau 1 rendu, chaîne Lara atteinte

Corrections supplémentaires :

- **Drapeaux d'objets** : `object_info_file.flags` (mot 16 bits) est converti
  vers les bitfields hôtes (`loaded`, `intelligent`, `save_*`, `HitEffect`,
  `undead`, `save_mesh`). Sans cela `objects[LARA].loaded` restait à 0 et
  Lara n'était jamais dessinée.
- **Scratchpads** : tous les buffers locaux `int scratchPad[N]` sont placés
  sous 4 Gio via une **référence de tableau** (`int (&scratchPad)[N]`), ce
  qui préserve exactement la sémantique `scratchPad[i]` / `&scratchPad[i]`
  sans troncature de pointeur.
- `DrawSkyMesh` lit l'entrée d'ordering table avec `PSX_ULONG`.
- `S_CalculateLight` utilise `&scratchPad[21]`.

État mesuré :

- `DrawLaraL1` est atteint sans crash ;
- `lara.mesh_ptrs[0]` / `[7]` valides, `mesh_bits = 0xFFFFFFFF` ;
- 4911 sommets générés, aucune primitive non gérée, processus stable 40 s ;
- mais Lara n'apparaît pas encore dans l'image et la bbox conserve des
  sommets aberrants (`-32768`, `1023`), probablement dans la
  transformation/éclairage de ses meshes.

## 21. Lara : logique et génération OK, image encore absente

- `DrawLaraL1` est appelé, `db.polyptr` avance d'environ **15 Ko** par frame
  (les primitives sont bien générées).
- `lara_item->pos = (46592,0,31232)`, `mesh_bits = 0xFFFFFFFF`,
  `lara.mesh_ptrs[0]` valide ; l'en-tête du mesh est **identique au 32 bits**.
- `lara_matrices[0]` est cohérente (`m00 = 4095`, translations faibles).
- Les entrées d'OT de Lara sont désormais indexées en mots 32 bits
  (`(PSX_ULONG*)db.ot + n`) au lieu de `db.ot + n*8`.
- Les sommets aberrants `-32768` observés viennent du décor (`lara=0`),
  pas de Lara.

Lara n'apparaît toujours pas à l'écran. Les 12 premiers polygones GT3
échantillonnés ont des `SXY` très compacts dans **les deux builds**
(`008000e7`), donc ils ne représentent pas le corps : il faut instrumenter
**par mesh** (pointeur `meshp`, nombre de polygones, min/max SXY) pour
identifier ceux du corps et comparer 32/64.

## 22. Gameplay niveau 1 en 64 bits : Lara visible et déplaçable

Cause de l'invisibilité de Lara : après la lecture contiguë du bloc
objets/skin/scratch, le loader 32 bits déplace `m_SkinVertNums + 480` vers
`m_ScratchVertNums`. En LP64, les deux blocs sont **déjà** copiés
séparément (`object_block + LEVEL_OBJECT_DATA_SIZE` et `+ 480`), donc ce
`memmove` écrasait `ScratchVertNums` avec des zéros. Les sommets skinnés
se repliaient alors tous sur un point (`SXY ≈ 0x008000e7`) et Lara
disparaissait.

Le `memmove` est maintenant limité au chemin 32 bits
(`#if !defined(__LP64__)`).

Résultat :

- décor de Streets of Rome correct ;
- **Lara visible**, déplacement `Up` opérationnel ;
- **F5 écrit `TOMB5.SAV`** : `level 1 room 0 X 46592 Y 0 Z 34346`,
  `level data 586 bytes` ;
- processus stable.

Reste à valider le chemin normal (menu → cutscene → gameplay) sans le
raccourci `TOMB5_START_LEVEL`.

## 23. Chemin normal (menu → cutscene → niveau) stabilisé

Le parcours normal a révélé trois nouvelles tables globales tronquées :

- `div3tab` / `div4tab` : `s4 = (int)&div3tab[0]` dans `SubDiv3`/`SubDiv4`
  (`DrawAllAnimatingItems`). Copies basses ajoutées en LP64.
- `dword_2C` : `sub_658L4` construisait des pointeurs couleur à partir de
  `(int)&dword_2C[0]`. Copie basse ajoutée.

Après correction, le parcours **menu → New Game → cutscene → niveau**
reste stable (processus vivant après ~60 s, aucun SIGSEGV). La capture
montre le décor ; Lara n'est pas encore visible dans cette phase
(caméra/cutscene), alors que `TOMB5_START_LEVEL=1` affiche Lara, permet le
déplacement et la sauvegarde F5.

## 24. Chemin normal validé et Colosseum chargé

Le parcours **menu → New Game → cutscene → niveau 1** fonctionne :
`[LARA] type=1 lvl=1 pos=(46592,0,31232)`, Lara visible, déplacement
`Up` opérationnel, `F5` écrit `TOMB5.SAV` (level 1, room 0,
`46592,0,34346`). RMIG-020 passe **Done**.

Le niveau 3 (**The Colosseum**) se charge également via
`TOMB5_START_LEVEL=3` : 125 salles, `[LARA] pos=(90642,4608,52736)
room 20`, 3897 sommets, décor rendu et processus stable après déplacement.
Le rendu du sable reste partiellement déformé et la caméra peut regarder un
mur sombre ; le parcours complet du Colosseum est suivi par **RMIG-021**.

## 25. Colosseum : chargement et reprise à la corniche

- `TOMB5_START_LEVEL=3` charge The Colosseum (125 salles), décor rendu,
  Lara déplaçable, processus stable.
- Nouvel outil de diagnostic : `TOMB5_START_POS=x,y,z,room,rot` place Lara
  après le chargement du niveau. Reprise testée à la corniche :
  `43364,768,52325,12,-16384`, salle 12. Le déplacement `Up` fait passer
  Lara en salle 14 puis la caméra en salle 26 ; une chute depuis la
  corniche déclenche un **GAME OVER attendu** (pas un SIGSEGV).
- Le rendu de sable/grands polygones est **également déformé en 32 bits**
  au même endroit : ce n’est pas une régression 64 bits, mais un défaut
  pré-existant du rendu à corriger séparément.

Le parcours complet du Colosseum reste à dérouler (RMIG-021).

## 26. Colosseum : salles clés validées en 64 bits

Via `TOMB5_START_LEVEL=3` + `TOMB5_START_POS`, les salles clés du
Colosseum se chargent et se rendent sans crash :

| salle | position de test | résultat |
| --- | --- | --- |
| 15 | `48640,1024,58880` | bannières/colonnes rendues, gladiateur présent |
| 90 | `48640,512,70144` | arène/arches/ciel rendus, Lara visible |
| 102 | `49664,512,62976` | porte/serrure rendues |

Coordonnées extraites du niveau 3 : R15 `x=45056 z=53248`, R90
`x=46080 z=65536`, R102 `x=48128 z=60416` ; le Roman God (obj 61,
item 79) est en `48154,512,69120`, le pickup final (obj 220) en
`55808,7936,70144` (salle 70).

Le parcours/puzzle complet reste à dérouler ; le rendu de certains grands
polygones/sable reste déformé, y compris en 32 bits.

### 26.1 Reprise en room 12 : cinématique de niveau

`TOMB5_START_POS=40448,1023,51712,12,-16384` (position valide de la
corniche) place bien Lara en room 12, mais le démarrage du niveau la
repositionne immédiatement en room 14 (`y=6144`, anim 25). Même avec
`TOMB5_SKIP_CUTSCENE=1` (qui force `GLOBAL_playing_cutseq=0`,
`cutseq_num=0`, `cutseq_trig=0`), la cinématique/le start trigger reprend
la main.

Les reprises **directes** dans les rooms 15/90/102 restent valides et ont
servi à valider le rendu. Pour rejouer le parcours depuis la corniche, il
faut soit jouer en 64 bits, soit restaurer une sauvegarde 64 bits native ;
la compatibilité des sauvegardes 32 bits reste un point ouvert.

### 26.2 Outils de saut de cinématique

Ajout de `TOMB5_SKIP_CUTSCENE=1` (force `GLOBAL_playing_cutseq`,
`cutseq_num`, `cutseq_trig` à 0 à chaque frame) et
`TOMB5_START_POS_HOLD=n` (force la position de départ pendant `n` frames).
Avec `hold=600`, Lara reste bien en room 12, mais le niveau reste en
`ScreenFade=239 / fading=1` et ne progresse pas : le start trigger/la
cinématique reprend la main. Les reprises directes dans les rooms
15/90/102 restent la méthode fiable pour tester le rendu en 64 bits.

## 27. Colosseum : clignotement de Lara corrigé (interpolation LP64)

Symptôme observé en 64 bits : Lara était visible une frame sur quatre environ,
et apparaissait étirée sur certaines frames. Le symptôme est absent en 32 bits.

Diagnostic (17-18 novembre 2026) :

- `DrawLaraL1` produit bien ses primitives à chaque frame
  (`[LF] delta=13..19 Ko`) et l'émulateur GPU les parse bien
  (`[OTF] laraPrims=286..418, laraVerts=1098..1584`) ;
- en revanche la bbox écran des vertices de Lara alterne entre le corps
  complet `(223,81)-(284,206)` et un sous-ensemble `(247,90)-(273,153)` ;
- forcer la pose clé (`TOMB5_NO_LARA_INTERP=1`, donc
  `DEL_CalcLaraMatrices_Normal_ASM` au lieu de la version interpolée) rend
  Lara stable et complète : le défaut est dans
  `DEL_CalcLaraMatrices_Interpolated_ASM` ;
- la translation de `lara_matrices[0]` oscillait sur 4 frames
  (`t=3420`, `2359`, `1296`, `4482`) au lieu de rester autour de `(-8,155,1295)`.

Cause racine (LP64) :

1. L’adaptation LP64 affectait `s0 = lara_matrices` **avant**
   `mTranslateXYZ_CL(s0[6], s0[7], s0[8])`. `s0` devait encore pointer sur
   les données de frame (`frame1`) à cet endroit : la translation de la
   frame était donc lue dans les rotations de la matrice. Correction :
   garder `s0` sur la frame et utiliser un pointeur séparé `m0` pour
   `lara_matrices`/`lara_joint_matrices`.
2. L’arithmétique du squelette utilisait `short*` (`s1[2]`, `s1 += 8`,
   `s1[50]`, …) alors que le tableau hôte `bones` est un tableau de `long`
   (8 octets par mot en LP64). Correction : pointeur `long* b1` avec les
   index en mots (`b1[1]`, `b1 += 4`, `b1[25]`, `b1[53]`, `b1[29]`,
   `b1[33]`, `b1[37]`, `b1[41]`, `b1[45]`, `b1[49]`, `b1[26]`), ce qui est
   équivalent au code 32 bits.

Validation :

- bbox de Lara désormais pleine à chaque frame, translation stable ;
- captures successives stables (plus de clignotement, plus d’étirement) ;
- build 32 bits reconstruit et rendu inchangé ;
- outils de diagnostic ajoutés : `TOMB5_LARAFRAME=1` (`[LF]`, `[OTF]`) et
  `TOMB5_NO_LARA_INTERP=1` (force la pose clé).

## 28. Fin des disparitions du processus : épuisement du pool bas

Après la correction de l'interpolation, le processus disparaissait encore
après 2 à 3 minutes de jeu, sans message de crash. Reproduit sous gdb :
l'inférieur sortait avec le code 1 après

```
PORT_LowAlloc: pool exhausted (16777056 + 1024 > 16777216)
```

Le pool `PORT_LowAlloc` (mmap `MAP_32BIT`, 16 Mio, bump allocator sans
libération) était saturé. Cause : plusieurs fonctions de rendu allouaient
leurs scratchpads **à chaque appel** au lieu d'une seule fois :

- `ROOMLET1.C`, `ROOMLET2.C`, `ROOMLET3.C`, `ROOMLET4.C`, `ROOMLETB.C`
  (`scratchPad` 1 Kio + `scratchPad2` 2 Kio par appel) ;
- `ANIMITEM.C` / `CalcAllAnimatingItems_ASM` (1 Kio par frame).

Le bloc `#else` contenait déjà le code de cache statique prévu pour LP64,
mais il était rendu inatteignable par un `#if defined(__LP64__)` extérieur
qui allouait directement. Correction : allocation **unique** via un
pointeur statique local à chaque fonction, puis réutilisation.

Validation : la séquence de reproduction sous gdb (marche, rotations,
animations pendant plusieurs minutes) survit désormais sans épuisement du
pool ; build 32 bits inchangé.

## 29. Colosseum : fin de niveau atteinte, téléport runtime F9

Nouvel outil de diagnostic : **F9** lit `/tmp/tomb5_teleport`
(`TOMB5_TELEPORT_FILE` pour changer de chemin, format `x,y,z,room,rot`)
et place Lara à cette position **sans redémarrer le jeu**. Contrairement à
`TOMB5_START_POS`, appliqué au chargement, il intervient dans une partie
déjà initialisée et réinitialise la caméra (`InitialiseCamera()`).

Salles validées en 64 bits avec ce téléport (captures stables, Lara
visible, aucun SIGSEGV) :

| salle | position | rendu |
| --- | --- | --- |
| 15 | `47616,1024,55808` | sol orné, bannières, porte, ciel |
| 90 | `47616,512,68096` | autel du Roman God, dallage |
| 102 | `49664,512,64000` | bannières, porte noire, socle |
| 70 | `55808,7936,70144` | pickup final (`obj 220`, `ocb 66`) |

Le téléport sur le pickup final de la salle 70 a déclenché la prise de
l'objet et la **transition vers le niveau 4** : le jeu charge 169 salles et
affiche `lvl=4 room=70`. La fin de The Colosseum fonctionne donc en 64 bits.

Blocage suivant : l'introduction du niveau 4 (The Great Wall) reste sur un
écran noir (`ndraw=1`, caméra à `12288,2048,49152`, aucune action `c` ne la
fait avancer) ; le lecteur de cinématique n'est pas encore porté.

## 30. Niveau 4 : costume Lara type 6 (module LARA6 absent)

Après la fin du Colosseum, le niveau 4 se charge mais Lara **n'était pas
dessinée** : `LaraDrawType = 6`, et le `switch` de `DrawPhaseGame` ne
couvrait que les types 1 à 5. Les types connus sont 1 (normal), 2 (young),
3 (bunhead), 4 (catsuit), 5 (divesuit) ; le type 6 correspond à un sixième
module PSX (`LARA6`) non porté.

Repli temporaire :

- type 6 -> `DrawLaraL1()` ;
- ce repli dessine bien le corps, mais une pièce du modèle (skin non gérée
  par les tables de L1) étire un grand polygone noir sur l'écran ;
- en masquant les meshes optionnels pendant le draw
  (`mesh_bits = 0x80000000`), le polygone disparaît et le corps reste
  visible. La valeur d'origine est restaurée après le draw pour ne pas
  perturber la logique de jeu.

Outils de diagnostic ajoutés :

- **F10** : lit `/tmp/tomb5_laradraw` (entier 1..5) et force le type de
  draw Lara, pour comparer les modules sans recompiler ;
- **F11** : lit `/tmp/tomb5_meshbits` (hex) et force `lara_item->mesh_bits`,
  pour isoler une pièce de modèle.

État du niveau 4 : avec `TOMB5_START_LEVEL=4 TOMB5_SKIP_CUTSCENE=1`, la
salle 99 se charge, Lara est visible (repli type 6) et **contrôlable**
(déplacement mesuré : `(35328,-4096,29596)` -> `(33893,-4096,30019)`).
L'introduction du niveau reste un écran noir sans `SKIP_CUTSCENE` : le
lecteur de cinématique n'est pas porté. Le vrai correctif est de porter le
module `LARA6` (skin/tables propres au costume).

## 31. Harnais déterministe 32/64 bits (RMIG-007)

Le jeu accepte maintenant une exécution déterministe pilotée par
l’environnement, dans `DoLevel` :

- `TOMB5_FRAMES=n` : exécuter `n` frames de contrôle après le chargement ;
- `TOMB5_CAPTURE=chemin.bmp` : capturer l’image à la dernière frame puis
  quitter ;
- `TOMB5_REPLAY=fichier` : entrées scriptées `frame pad_hex` (pad PSX actif
  haut), appliquées avant `QuickControlPhase`.

La capture passe par `Emulator_TakeScreenshot()` (lecture du framebuffer),
avec un chemin configurable. Les captures sont comparées par
`scripts/porting/capture_compare.py` et archivées dans
`docs/porting/replay/`.

Scène de référence : niveau 3, 1800 frames, aucune entrée.

Résultats :

| build | sha256 (2 runs identiques) |
| --- | --- |
| 32 bits | `083d24a01588e14023b5f2ddb654dcaee278a58d9ce9e4a7fa443a6d7f7750b6` |
| 64 bits | `675e2c8da064bfefb4dcb4347f7629d5e114026bb0082c78b584ede61a9b651b` |

L’état de jeu est identique (`Lara pos=(90642,4608,52736) room=20
rot=-16384 anim=103 frame=1611`). L’écart image 32/64 est
`mean_abs_diff=18.730`, gain global `0.965`, `26.12 %` de pixels à ±8
après gain : le 64 bits est globalement plus sombre, **HUD compris**.
L’écart n’est donc pas seulement l’éclairage 3D ; il est reporté dans
RMIG-012 pour la parité Vulkan.

RMIG-007 est terminé ; RMIG-008 (abstraction du renderer) est débloqué.
