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

## 32. Début de l’abstraction renderer (RMIG-008)

`EMULATOR/RENDERER.H` définit `RendererBackend`, l’interface consommée par
l’émulation GPU PSX (`LIBGPU.C`) : begin/end de scène, blit VRAM, upload
VRAM, clear, texture, blending, vertex buffer et draw.

`EMULATOR/RENDERER_GL.C` branche l’implémentation OpenGL historique
(`Emulator_*`) derrière cette interface ; `g_renderer` pointe dessus par
défaut. `LIBGPU.C` appelle désormais `g_renderer->...` pour le chemin de
rendu.

Validation : la capture déterministe RMIG-007 (niveau 3, 1800 frames)
reste **exactement identique** après refactor :
`sha256 675e2c8da064bfefb4dcb4347f7629d5e114026bb0082c78b584ede61a9b651b`.
Builds 32/64 verts, 4188 tests PASS.

Reste pour terminer RMIG-008 : déplacer les appels GL hors de
`EMULATOR.C` dans le backend, puis ajouter la sélection d’un backend
Vulkan. Les fonctions `Emulator_CopyVRAM` restent directes pour préserver
le harnais de test PSX existant.

## 33. Smoke test Vulkan (RMIG-009)

`tools/vulkan_smoke.cpp` valide la chaîne Vulkan minimale hors du jeu :

- instance + extensions SDL2/X11 ;
- sélection d’un device et d’une queue graphics/present ;
- `SDL_Vulkan_CreateSurface`, swapchain 640x480 (4 images), image views,
  render pass clear, framebuffers, command buffers, sémaphores/fence ;
- 60 frames `vkAcquireNextImageKHR` / `vkQueueSubmit` /
  `vkQueuePresentKHR`, puis arrêt propre.

Exécution validée :

```
[VK] instance/device/swapchain OK: 640x480, 4 images
[VK] presented, shutting down
```

Script : `scripts/porting/vulkan_smoke.sh`.

Le squelette sert de base à `RENDERER_VK.C` ; l’intégration du pipeline
PSX (VRAM, vertex buffer, ordering tables, shaders) reste RMIG-010/011.

## 34. Backend Vulkan intégré au jeu (RMIG-009 terminé)

`RENDERER_VK.C` implémente un backend Vulkan sélectionnable par
`TOMB5_RENDERER=vulkan` :

- fenêtre créée avec `SDL_WINDOW_VULKAN` (pas de contexte GL) ;
- instance, surface SDL2/X11, device + queue graphics/present ;
- swapchain 640x480 (4 images), render pass clear, sémaphores/fence ;
- `RendererVK_BeginScene/EndScene` acquièrent et présentent l’image.

`TOMB5_VK_CLEAR=1` force une couleur de test : la fenêtre affiche un bleu
640x480, le jeu continue de simuler (logs `[DRAW] lvl=3 room=20`,
`[LARA] anim=103`) **sans aucun contexte OpenGL**. Le backend GL reste le
défaut : la capture déterministe RMIG-007 est toujours
`sha256 675e2c8d…`.

CMake : `find_package(Vulkan)` et `HAVE_VULKAN=1` pour le build 64 bits ;
le 32 bits compile des stubs et garde GL.

Le pipeline PSX Vulkan (VRAM 16 bits, vertex buffer, ordering tables,
blit, shaders 4/8/16 bits) est RMIG-010/011.

## 35. Pipeline PSX Vulkan : la scène 3D est rendue (RMIG-010)

Le backend Vulkan rend désormais la scène 3D réelle, sans OpenGL :

- texture VRAM 1024×512 `R8G8_UNORM` alimentée depuis `vram` à chaque
  frame ;
- vertex buffer `Vertex` (20 o) alimenté par `vkCmdUpdateBuffer` par
  ordering table ;
- shaders SPIR-V 4/8/16 bits + CLUT + dither, compilés par
  `scripts/porting/gen_vk_shaders.py` (glslc) et embarqués dans
  `EMULATOR/SHADERS_VK.H` ;
- blends PSX (aucun, average, add, subtract, quarter) ;
- render pass par OT avec conservation de l’image (`LOAD`) et clear au
  premier OT ;
- projection 512×240 codée dans `psx.vert` (le push constant n’a pas été
  fiable ; à remplacer par un UBO).

Validation : niveau 3, room 20, ~3500 vertices/1170 triangles par frame,
Lara et HUD visibles. Le sampler doit être en `REPEAT` (comme GL) : sinon
d’énormes bandes de texture apparaissent.

La capture GL de référence reste **identique**
(`sha256 675e2c8d…`), builds 32/64 verts, 4188 tests PASS.

Restent : blit VRAM (titres/menus), perspective PGXP, capture/readback
Vulkan, et le warping pré-existant des grands polygones.

## 36. Blit VRAM : écran-titre rendu en Vulkan

`RendererVK_BlitVRAM` utilise le pipeline `pipelines[0]` (blit.vert /
blit.frag, SPIR-V) pour dessiner le framebuffer PSX 1024×512 avant la
scène 3D. Le sampler est en `REPEAT` et le vertex buffer de blit est
alimenté par `memcpy` + barrière avant le render pass.

Validation : l’écran-titre complet (**TOMB RAIDER CHRONICLES**, menu
New Game / Special Features / F6 CONTINUE) s’affiche en Vulkan, sans
OpenGL. La scène 3D niveau 3 reste correcte avec le blit activé.

RMIG-011 reste en cours pour la vérification des formats 8/16 bits, la
perspective PGXP et le readback/capture Vulkan.

## 37. Capture Vulkan et première mesure de parité

`RendererVK_RequestCapture` / `Emulator_RequestScreenshot` permettent de
capturer la swapchain en BMP : copie image→buffer host, flip vertical,
`SDL_SaveBMP`. Le harnais RMIG-007 (`TOMB5_CAPTURE`) fonctionne donc
aussi en mode Vulkan.

Première comparaison avec la référence GL au même état de jeu
(`pos=(90642,4608,52736) room=20 anim=103 frame=1611`) :

```
sha256 GL 675e2c8d…
sha256 VK c305201f…
mean_abs_diff=50.406
global_gain=0.630455
pixels_within_8_after_gain=4.08%
```

L’image GL de cette frame est **bleutée** (probable fondu/overlay de
cinématique) alors que VK montre la scène de base **orangée**. L’écart
n’est donc pas encore une simple différence de filtrage : il faut rendre
les primitives non texturées / fondus 2D et aligner le timing de
cinématique avant de conclure sur la parité des textures.

## 38. Parité visuelle Vulkan / OpenGL : pixel-identique (RMIG-011)

Le §37 concluait à un écart « bleu contre orangé » entre les deux
backends. La cause n’était **pas** le rendu : les deux captures étaient
correctes géométriquement, mais **la capture OpenGL inversait rouge et
bleu**.

### Cause racine

`Emulator_TakeScreenshot` lisait le framebuffer avec
`glReadPixels(..., GL_RGBA, ...)` (octets R,G,B,A) puis créait la surface
SDL avec des masques **nuls** :

```c
SDL_CreateRGBSurfaceFrom(pixels, w, h, 32, w*4, 0, 0, 0, 0);
```

SDL applique alors ses masques par défaut (`R=0x00FF0000`), qui décrivent
un tampon **BGRA** : le canal rouge lu était écrit comme bleu. Toutes les
captures de référence RMIG-007 (dont `ref32.png` / `ref64.png`) étaient
donc R/B inversées. La fenêtre, elle, était correcte — d’où l’impression
que seul Vulkan « changeait » les couleurs.

Le backend Vulkan avait le même type de bug : les masques du BMP étaient
codés en dur pour du BGRA alors que la swapchain choisie est
`VK_FORMAT_B8G8R8A8_UNORM`… avec un traitement incohérent, et l’alpha de
la swapchain (déclarée `OPAQUE`, donc non défini) finissait dans le BMP.

Corrections :

- masques SDL explicites côté GL (`R=0x000000FF`, `G=0x0000FF00`,
  `B=0x00FF0000`) ;
- masques déduits du format réel de la swapchain côté Vulkan ;
- alpha forcé à 255 dans la capture Vulkan (swapchain `OPAQUE`).

### Autres écarts corrigés au passage

1. **Projection par push constant** : `vkCmdPushConstants` était appelé
   avant tout `vkCmdBindPipeline`, donc ignoré. Une fois l’ordre corrigé,
   l’image restait noire pour une autre raison : la matrice copiée était
   celle d’OpenGL. En Vulkan le NDC `y` pointe vers le bas et `z` doit
   rester dans `[0, 1]` ; avec `z = -1` tout le décor était écrêté par le
   plan proche. La projection est maintenant calculée dans les
   conventions Vulkan (`b = +2/h`, `c = -1`, `z = 0`) et passée par push
   constant : plus de `512×240` codé en dur dans `psx.vert`.
2. **Dithering** : `gl_FragCoord.y` part du bas en OpenGL et du haut en
   Vulkan. La matrice 4×4 était donc appliquée en miroir vertical
   (±3/±5 par pixel sur toute l’image). Les shaders utilisent désormais
   `pc.Screen.y - gl_FragCoord.y`, ce qui reproduit exactement la
   position du dither OpenGL.
3. **Identifiants de texture** : en mode Vulkan, `Emulator_Initialise`
   ne crée pas les textures GL, donc `whiteTexture` et `vramTexture`
   valaient tous deux 0. `AddSplit` fusionnait alors des groupes de
   primitives que OpenGL séparait (`texture VRAM` vs `texture blanche`).
   Deux identifiants logiques distincts (`PORT_TEXTURE_WHITE`,
   `PORT_TEXTURE_VRAM`) rétablissent un découpage identique.
4. **`read_vram` / `copy_vram`** : ils étaient vides côté Vulkan alors
   que la VRAM PSX reste une image CPU (`vram`). `StoreImage` (utilisé
   par `GPU_SyncBothScreens`) renvoyait donc des données non
   initialisées et la logique du jeu divergeait. Ils opèrent maintenant
   sur `vram`, comme le backend GL.
5. **Validation Vulkan** : `loadOp = LOAD` exige une `initialLayout`
   définie. La render pass utilise `PRESENT_SRC_KHR`, avec une barrière
   `UNDEFINED → PRESENT_SRC` à la première utilisation de chaque image de
   swapchain. Plus aucune erreur de validation (hors avertissements de
   performance sur les attributs inutilisés du pipeline de blit).

### Preuves

Instrumentation ajoutée (harnais temporaires, activés par variable
d’environnement) :

- `TOMB5_DUMP_VERTS=<fichier>` : trace binaire des données réellement
  envoyées au backend (en-tête `splitIndex`, `vertexIndex`, puis
  `Vertex` et `VertexBufferSplit`) à chaque ordering table ;
- `TOMB5_DUMP_VRAM=<fichier>` : dump de la VRAM PSX à la frame de
  capture.

Résultats (niveau 3, 300 frames, `TOMB5_SKIP_CUTSCENE=1`) :

- dump des vertices : **1277 enregistrements identiques octet par octet**
  entre GL et Vulkan (aucune différence de position, couleur, texture,
  blend ou format) ;
- captures 640×480 : `mean_abs_diff = 0.000`, `global_gain = 1.000`.

Résultats sur la scène de référence RMIG-007 (niveau 3, 1800 frames,
`TOMB5_CAPTURE`) :

```
GL 64 bits : 5dbbb25184d54d96c95aed1c96494ade0e390956e7c0de1da262180779e269a8
Vulkan     : 5dbbb25184d54d96c95aed1c96494ade0e390956e7c0de1da262180779e269a8
cmp        : identiques
```

La capture Vulkan est **octet pour octet identique** à la capture
OpenGL 64 bits de la scène de référence (307 200 pixels, zéro pixel
différent). Le pipeline PSX Vulkan peut donc servir de base fiable pour
la suite (SSR, raytracing, retrait d’OpenGL).

Les formats réellement exercés par la scène de référence sont 4 bits
(588 groupes) et 16 bits (977 groupes) ; aucun groupe 8 bits n’y
apparaît, ce format reste donc à couvrir par une scène dédiée.

## 39. Formats de texture, StoreFrameBuffer et harnais de contrainte

### Format 8 bits

La scène de référence n’exerce que deux profondeurs (mesure sur le dump
des splits : 4 bits = 588 groupes, 16 bits = 977 groupes, 8 bits = 0).
Un harnais `TOMB5_FORCE_TEXFMT=4|8|16` force la profondeur dans
`AddSplit` : l’image devient volontairement fausse, mais elle doit être
identique entre backends.

En 8 bits forcé (niveau 3, 300 frames) :

```
GL  45210c966601bf9213e771457500844c4d64cb900c8fe692106e1e2479908f2e
VK  ba7c0ef7f60b67804c5166fd79e52422c485929af5b9f26bf3e79825d63bac5b
mean_abs_diff=0.142   pixels_within_8=99.82 %
```

Le résidu (795 pixels) vient des égalités de `nearest` sur les frontières
de texel : en 8 bits, `v_texcoord.x` est divisé par deux et tombe
exactement sur des bords de texel, où deux implémentations peuvent
arrondir différemment. Un epsilon identique à celui du shader 4 bits a
été ajouté **dans les deux backends** pour la sélection d’index
(`mod(v + 0.0001, 2.0)`), ce qui réduit l’écart sans le supprimer. Ce
format n’étant pas utilisé par les scènes jouées, le ticket RMIG-011
reste ouvert sur ce seul point.

### `Emulator_StoreFrameBuffer` porté sur Vulkan

`GPU_SyncBothScreens` / `CreateMonoScreen` stockent la trame affichée
dans la VRAM (`StoreImage`, effet mono/sépia). En mode Vulkan,
`Emulator_StoreFrameBuffer` appelait `glReadPixels` sans contexte GL :
la VRAM recevait des données indéfinies et l’effet était cassé.

Le backend Vulkan copie désormais l’image présentée vers un buffer hôte
à chaque frame (`vkCmdCopyImageToBuffer`, buffer cohérent), puis
`RendererVK_StoreFrameBuffer` applique **la même conversion 16 bits** que
le chemin OpenGL (échantillonnage `windowWidth/w`, `windowHeight/h`,
puis extraction des canaux) avant d’écrire dans `vram`.

Vérifications :

- appel unique par chargement de niveau : `x=0 y=240 w=512 h=240` ;
- la capture de référence 4 bits reste **bit-identique**
  (`sha256 5dbbb251…`) après ce portage ;
- l’extraction des canaux reproduit l’anomalie existante du chemin GL
  (le rouge PSX vient de l’alpha, le vert du bleu) : elle est suivie par
  **RMIG-022** pour ne pas modifier le rendu de référence sans preuve.

Harnais de diagnostic associé : `TOMB5_NO_STOREFB=1` court-circuite la
copie framebuffer → VRAM, ce qui permet de mesurer son impact (sur le
niveau 3 le simple fait de la désactiver change l’image de ~22 niveaux
moyens, donc le chemin est bien actif).

## 40. D'où vient réellement l'écart 32 bits / 64 bits

Le §38 a montré que l'écart « bleu contre orangé » était un artefact de
capture. Restait l'écart 32/64 (`mean_abs_diff=18.730`, 26 % de pixels à
±8, 64 bits plus sombre HUD compris). Mesure faite avec le dump des
vertices (300 frames, même scène) :

- les **977 premiers ordering tables** (chargement, intro, écrans de
  transition) sont **identiques octet par octet** entre 32 et 64 bits ;
- les **300 ordering tables suivantes** (les frames de jeu) diffèrent
  toutes : la version 32 bits émet un groupe de texture supplémentaire
  (3 splits au lieu de 2) et ~99 vertices de plus par frame, dont 6
  vertices en blend soustractif ;
- en comparant les journaux `[DRAW]`, l'état de jeu diverge dès le début :
  le build 32 bits affiche `fade=239/0 fading=1` là où le 64 bits est à
  `fade=0/0 fading=0`, et les valeurs `persp` diffèrent (306 contre 256).

Conclusion : l'écart 32/64 n'est **pas** un écart de pipeline de couleur
(les vertices identiques donnent des pixels identiques ; le backend
Vulkan reproduit OpenGL au pixel près). C'est une **divergence d'état de
jeu / d'effets** entre les deux largeurs de pointeur : fondu d'intro,
nombre de primitives d'effet par frame, valeur de perspective. Cela
relève du portage 64 bits, pas de la migration Vulkan, et est suivi dans
RMIG-012 avec cette analyse comme point de départ.

Prochaine étape pour ce point : instrumenter le type de primitive
(histogramme des codes de prim par ordering table) pour identifier les
primitives d'effet émises seulement en 32 bits, puis corriger la cause
LP64 correspondante sans toucher au rendu commun.

### Histogramme des primitives (suite du §40)

Un second harnais (`TOMB5_PRIMHIST=1`) imprime, par ordering table,
l'histogramme des codes de primitive et le nombre de vertices. Comparaison
32 / 64 bits sur 300 frames :

```
32 bits : [PH] ot=977 nv=2706 34=434 3C=221 50=11 60=1 62=1 E1=1
64 bits : [PH] ot=977 nv=2607 34=403 3C=221 50=11 60=1
```

Les 977 premiers OT sont identiques ; à partir du premier OT de jeu, le
build 32 bits ajoute **31 triangles gouraud semi-transparents (`0x34`)**,
**un sprite semi-transparent (`0x62`)** et **un DR_TPAGE (`0xE1`,
changement de page de texture)**, toutes les autres primitives (`0x3C`,
`0x50`, `0x60`) étant identiques. C'est donc un effet rendu avec sa propre
page de texture qui n'est pas émis en 64 bits. Il n'y a donc pas d'abandon de chaîne : c'est un jeu de
primitives d'effet qui n'est pas émis en 64 bits.

Piste : ces trois codes ensemble correspondent à l'effet d'écran
(fondu / voile) piloté par `ScreenFading` / `dScreenFade`, dont l'état
diverge déjà au premier `[DRAW]` (`fade=239/0 fading=1` en 32 bits contre
`fade=0/0 fading=0` en 64 bits). `Fade()` n'est pas neutralisé ici
(`PC_VERSION` n'est pas défini dans ce dossier), donc la divergence vient
de l'état du fondu, pas d'un `#if`.

Prochaine étape : tracer `S_SetScreenFade` / `dScreenFade` au chargement
du niveau dans les deux builds pour trouver pourquoi le fondu n'est pas
lancé en 64 bits.

## 41. Vulkan devient le backend par défaut du build 64 bits

Le rendu Vulkan étant octet pour octet identique à OpenGL 64 bits sur la
scène de référence (et vérifié sur le niveau 4), il devient le backend
**par défaut** en 64 bits :

- `MAIN` sans variable d’environnement → Vulkan ;
- `TOMB5_RENDERER=gl` (ou `opengl`, ou `0`) → chemin OpenGL historique,
  conservé pour les comparaisons ;
- pas de repli silencieux : si l’initialisation Vulkan échoue, le
  programme s’arrête avec un message explicite (un backend ne doit pas
  être remplacé sans le dire).

Vérifications après bascule :

| scénario | résultat |
| --- | --- |
| `MAIN` seul (écran-titre) | `[VK] backend ready: 640x480, 4 images`, logo et menu rendus |
| niveau 3, 300 frames, GL explicite | sha256 `d05c8394…` = capture GL précédente (aucune régression) |
| niveau 3, 1800 frames, Vulkan | sha256 `5dbbb251…` = référence GL (`cmp` identique) |
| niveau 4 (Colosseum), 600 frames, Vulkan | scène rendue, aucune erreur de validation |

Le build 32 bits reste sur OpenGL. Le retrait effectif du code
OpenGL/GLEW du build 64 bits est la dernière étape de RMIG-012.

## 42. Overlay de debug ImGui (F12, RMIG-013)

Dear ImGui `v1.91.5` est vendoré dans `external/imgui` (voir
`external/imgui/README-VENDORED.md`) et compilé uniquement pour le chemin
Vulkan 64 bits (`imgui_overlay`, lié à `Emulator_`). Le 32 bits garde son
chemin OpenGL sans ImGui.

Intégration :

- `EMULATOR/DEBUGUI.C/.H` : contexte ImGui, backends SDL2 + Vulkan,
  panneau, statistiques et interrupteurs ;
- `RendererVK_Init` initialise l'overlay après la render pass ; `F12`
  (traité dans `Emulator_DoPollEvent`) l'ouvre et le ferme ;
- `RendererVK_EndFrame` dessine l'overlay dans un render pass `LOAD`
  ouvert pour l'occasion (le jeu ferme le sien à chaque ordering table),
  et `ImGui::Render()` est appelé même quand rien n'est dessiné ;
- `SPEC_PSXPC_N/DRAWPHAS.C` alimente les statistiques de jeu (niveau,
  salle, position de Lara, animation), le backend fournit vertices,
  triangles, draws et ordering tables.

Contenu du panneau :

- renderer, FPS lissé et temps de frame ;
- niveau / salle / nombre de salles, position de Lara, animation ;
- compteurs de rendu de la frame ;
- interrupteur **Dithering PSX** (push constant `pc.Dither`, appliqué
  immédiatement dans les shaders 4/8/16 bits) ;
- sélecteur de **profondeur de texture forcée** (normal / 4 / 8 / 16 bits,
  même mécanisme que le harnais `TOMB5_FORCE_TEXFMT`) ;
- champ + bouton **Capture BMP** (appelle `Emulator_RequestScreenshot`) ;
- rappel des tickets SSR/RT (RMIG-014/015).

Blocage des entrées : quand l'overlay est visible, le jeu ne reçoit plus
rien — `UpdateKeyboardInput*` renvoie le masque « aucune touche »
(0xFFFF) et `InputMap_PollActions` renvoie 0 (la keymap utilisateur
court-circuite le pad PSX, il fallait bloquer les deux chemins).

Vérifications :

| test | résultat |
| --- | --- |
| F12 | `[IMGUI] overlay visible` / `[IMGUI] overlay masque` |
| rendu inchangé | capture 300 frames identique avant/après intégration (`sha256 63b778f1…`) |
| entrées bloquées | overlay ouvert + « Up » maintenu 3 s : `pos=(90642, 4608, 52736)` inchangée |
| entrées rendues | overlay fermé + « Up » 3 s : `pos=(81363, …)` (Lara avance) |
| interrupteur | « Dithering : OFF » → libellé et image changent immédiatement (écart moyen 2,3 niveaux sur la scène) |
| bouton capture | écrit `/tmp/tomb5_capture.bmp` (640×480) |

Capture de référence de l'overlay : `docs/porting/render/imgui-f12.png`.

## 43. Retrait d'OpenGL et de GLEW du build 64 bits (RMIG-012)

Le build 64 bits ne contient plus **aucun** code OpenGL : ni GLEW, ni
libGL dans les dépendances, ni symbole `gl*` dans le binaire.

Mise en œuvre :

- `EMULATOR_PLATFORM_SETUP.H` définit `PORT_VULKAN_ONLY` en 64 bits
  (échappatoire `PORT_ALLOW_GL` pour reconstruire un binaire 64 bits avec
  OpenGL), ce qui supprime la définition de `OGL`/`GLEW` ;
- `EMULATOR.H` fournit des identifiants de texture « logiques »
  (`unsigned int`) quand `PORT_VULKAN_ONLY` est défini ;
- `EMULATOR.C` : les fonctions GL/D3D qui n'ont plus de sens
  (`Emulator_CreateGlobalShaders`, `Emulator_Ortho2D`, `Emulator_SetShader`,
  `Emulator_SetTexture`, `Emulator_DestroyTexture`, `Emulator_Clear`,
  `Emulator_SetViewPort`, `Emulator_SetRenderTarget`,
  `Emulator_UpdateVertexBuffer`, `Emulator_DrawTriangles`,
  `Emulator_StoreFrameBuffer`…) compilent un chemin neutre ; `g_renderer`
  est désormais défini par `RENDERER_VK.C` ;
- `RENDERER_GL.C` se réduit à un message explicite ; `Renderer_SelectGL()`
  ne sélectionne plus rien ;
- `TOMB5_RENDERER=gl` sur le build 64 bits affiche
  « OpenGL n'est pas compile dans ce build 64 bits ; utilisation de
  Vulkan » et continue en Vulkan (pas de repli silencieux, pas de crash) ;
- CMake : OpenGL/GLEW ne sont plus recherchés ni liés en 64 bits.

Vérifications :

| test | résultat |
| --- | --- |
| `ldd` du binaire 64 bits | aucune entrée `libGL`/`libGLEW` |
| symboles `gl*` non résolus | 0 |
| rendu | capture 300 frames `63b778f1…` identique à avant le retrait |
| `TOMB5_RENDERER=gl` | message explicite puis Vulkan |
| build 32 bits | compile et tourne toujours avec OpenGL (référence conservée) |

## 44. Correctif : retournement vertical de `StoreFrameBuffer` en Vulkan

`RendererVK_StoreFrameBuffer` (porté au §39) échantillonnait la trame
avec `sy = fy` alors que le chemin OpenGL applique `FLIP_Y = h - fy - 1`
(conséquence de `glReadPixels`, qui renvoie les lignes bas-en-haut). La
VRAM stockée était donc retournée verticalement en Vulkan. Corrigé
(`sy = ((h - fy - 1) * fh) / h`).

La capture de référence reste identique (`sha256 5dbbb251…`), ce qui
confirme que la zone stockée n'est pas visible dans cette scène ; le
correctif compte pour l'effet mono/sépia (`CreateMonoScreen`).

## 45. Cible hors-écran, profondeur et reflets à presets (RMIG-014)

### Infrastructure

La scène n'est plus rendue directement dans l'image de swapchain :

1. **Cible hors-écran** `sceneImage` (format de la swapchain) + `depthImage`
   (`D32_SFLOAT`), avec sa propre render pass (couleur + profondeur, `LOAD`,
   contenu conservé entre les ordering tables) ;
2. la profondeur est écrite par les pipelines PSX avec
   `depthCompareOp = ALWAYS` et `depthWriteEnable = TRUE` : l'ordre de
   l'ordering table (peintre) est conservé, mais chaque fragment laisse une
   profondeur exploitable ;
3. **profondeur par vertex** : `g_vertexDepth` dans `LIBGPU.C` reçoit, pour
   chaque primitive, la position de son bucket d'ordering table normalisée
   (`0` = le plus éloigné, `1` = le plus proche). Elle est envoyée au backend
   via un second vertex buffer (attribut 3, `R32_SFLOAT`) et écrite dans
   `gl_Position.z` ;
4. **passe finale** : un triangle plein écran lit la couleur par
   `texelFetch` (aucun filtrage) et écrit l'image de swapchain. L'overlay
   ImGui est dessiné dans la même passe, au-dessus.

Le passage par une cible intermédiaire devait rester **exact** : c'est
vérifié, les captures sont identiques à l'octet près
(`63b778f1…` à 300 frames, `5dbbb251…` à 1800 frames, c'est-à-dire la
référence RMIG-007).

### Reflets

`post.frag` applique un reflet écran : miroir vertical de l'image avec
distorsion horizontale proportionnelle à la profondeur, masqué par
`1 - smoothstep(0.10, 0.90, depth)` (les surfaces proches ne réfléchissent
pas) et atténué en haut de l'écran. Quatre presets dans l'overlay F12 :
`aucun`, `faible` (0,35), `moyen` (0,60), `fort` (0,85), poussés au shader
par push constant (`vec4 Params`). Le preset `aucun` remet l'intensité à 0,
donc l'image de référence exacte.

Mesures (niveau 3, captures à ~2 s d'intervalle, zone de scène hors
overlay) — les presets changent bien l'image :

```
faible : écart moyen 1,36 niveau  vs aucun
moyen  : écart moyen 0,96 niveau  vs aucun
fort   : écart moyen 1,72 niveau  vs aucun
```

Le coût est négligeable (60 FPS stables, ~16,5 ms par frame avec le preset
`fort`, comme sans reflets).

### Limite honnête

Ce n'est **pas** un SSR physique : le flux de vertices PSX ne contient que
des coordonnées **écran** (x, y), sans position monde ni normale, et la
profondeur n'est qu'un indice de bucket (pas une distance view-space). Un
vrai SSR (raymarch dans le depth buffer avec normales) et a fortiori le
raytracing matériel (RMIG-015, qui exige une BVH en espace monde) ne sont
pas réalisables avec ces données. L'effet livré est donc un reflet écran
stylisé, réglable et sans risque pour le rendu d'origine ; RMIG-015 reste
bloqué pour cette raison, documentée dans le ticket.

## 46. Profilage par passe et budget de frame (RMIG-016)

L'overlay F12 expose maintenant le coût réel de chaque passe :

- **GPU** : trois requêtes de timestamp par frame (`VK_QUERY_TYPE_TIMESTAMP`,
  pool de 3) — début de frame, fin de la passe de scène, fin de la passe
  finale. Les résultats sont relus à la frame suivante, après l'attente du
  fence, et convertis avec `timestampPeriod`.
- **CPU** : durée de la frame complète (horloge SDL), à côté du FPS lissé.
- **Budget** : curseur 4–33 ms ; le total GPU passe en vert sous le budget,
  en rouge au-dessus.

Relevé en jeu (niveau 3, salle 20, 640×480) :

```
GPU scene 0.50 ms
GPU post  0.07 ms
CPU frame 16.80 ms
GPU total 0.57 ms (budget 16.6)
```

La passe de scène domine largement (tout le pipeline PSX) ; la passe finale
est marginale. C'est exactement l'information demandée par le ticket
(« identifier la passe la plus coûteuse sans profiler externe »).

**Coût nul overlay fermé** : tant que l'overlay n'a jamais été ouvert,
`DebugUI_NewFrame` ne construit aucune frame ImGui (`frameActive = 0`) et
`DebugUI_Render` ne fait rien — pas de `ImGui::NewFrame`/`Render`, pas de
draw data. Vérifié : la capture de référence reste identique
(`sha256 63b778f1…` à 300 frames) et l'ouverture/fermeture répétée de F12 ne
déclenche plus l'assertion de sanity check d'ImGui.

**Inspection VRAM** : le bouton `VRAM : ON` affiche la VRAM 1024×512 dans le
panneau via `ImGui_ImplVulkan_AddTexture` (vue brute des canaux R/G, la
VRAM étant en `R8G8_UNORM` : l'octet bas du mot PSX apparaît en rouge,
l'octet haut en vert). L'inspection GTE n'est pas couverte par ce ticket.

## 47. RMIG-023 : la divergence 32/64 vient du squelette de Lara

Chaîne d'investigation (niveau 3, `TOMB5_SKIP_CUTSCENE=1`, 300 frames) :

1. **VRAM** : les textures sont identiques entre les deux builds ; seules
   les zones framebuffer diffèrent (conséquence du rendu). Ce n'est donc
   pas un contenu de texture.
2. **Histogramme des primitives** (avec marquage des primitives Lara via
   `port_lara_prim_lo/hi`) : le 32 bits émet 31 triangles gouraud
   semi-transparents (`0x34`) de plus, dont 28 dans la plage Lara, plus un
   sprite (`0x62`) et un `DR_TPAGE` (`0xE1`) hors plage Lara.
3. **État de Lara** (harnais `TOMB5_LARASTATE`) : `anim=103`, `frame`
   identiques à chaque frame, `frac`/`rate` identiques (`frac=0`, donc pas
   d'interpolation), position/rotation/mesh_bits identiques.
4. **Données d'animation** : le hash des 96 premiers shorts de la frame
   d'animation est **identique** (`7b26e60b`).
5. **Table `bones`** : le hash diffère (`af81e4cb` en 64 bits contre
   `a7f7b6f6` en 32 bits) — et le dump mot à mot montre que la table est
   décalée/altérée à partir du 5e élément.
6. **Matrices de joints** : elles diffèrent sensiblement (rotation ~1,7°,
   translation ~0xA3), ce qui change les tests d'écrêtage de
   `sub_658L1` et donc le nombre de triangles émis.

**Correction du diagnostic** (mesure suivante) : la table `bones` a été
relue avec la bonne largeur (`long` hôte) sur 160 entrées — elle est
**identique** entre les builds. L'ancien hash comparait des `int` sur un
tableau d'`long`, ce qui n'avait pas de sens. Ce n'était donc pas le
squelette.

En revanche, le même harnais `[LS]` montre que **la caméra diverge** : les
frames 0 à 32 sont strictement identiques (matrices, `MatrixStack`, caméra,
Lara), puis à la frame 33 le build 64 bits place la caméra à
`(88576, 3200, 52736)` et `(96854, -867, 52573)` pendant deux frames, alors
que le 32 bits continue en douceur (`86572, 4076, 52735`). Le 64 bits
revient ensuite à la position de la frame 31, mais l'historique de lissage
est différent : la caméra reste décalée, donc la matrice de vue aussi, donc
les matrices de Lara, les tests d'écrêtage et le nombre de triangles
émis.

Conclusion : l'écart 32/64 vient d'un **changement de caméra de deux frames
au démarrage du niveau** (caméra fixe/scriptée ou bascule de `camera.type`)
qui n'a lieu qu'en 64 bits. Tout le reste (textures, données d'animation,
`bones`, état de Lara) est identique.

Piste de correction : instrumenter `camera.type`, `UseForcedFixedCamera`,
`TriggerCamera` et `cutseq_trig` autour de la frame 33 dans les deux builds
pour identifier la bascule, puis corriger la cause LP64.

Harnais ajoutés (tous activés par variable d'environnement, coût nul sinon) :
`TOMB5_LARASTATE` (`[LS]`, `[MP]`, `[MB]`), `TOMB5_LARAMESH` (`[LM]`,
octets par mesh), `TOMB5_LARABONES` (dump de la table `bones`).

Correctif annexe : `TOMB5_SKIP_CUTSCENE` était appliqué dans GAMEFLOW
uniquement sous `#if defined(__LP64__)` alors que DRAWPHAS l'appliquait
toujours — les deux builds ne sautaient donc pas la cinématique de la même
façon. Le bloc est maintenant commun (le lecteur de cinématique n'étant pas
porté non plus en 32 bits).

## 48. RMIG-023 : cause racine trouvée et corrigée (`MULFP`)

La chaîne d'éliminations du §47 a fini par désigner la **caméra** : à partir
de la frame 30 le build 32 bits passait en caméra *flyby* (`TO_FLYBY` →
`bUseSpotCam`) et la caméra 64 bits partait dans des positions absurdes
(`(96854, -867, 52573)` puis retour en arrière), avec une position de spline
à `281474976713275` au lieu de `2619`.

Cette valeur est `2^48 + 2619` : un défaut de troncature. `MULFP`, la
multiplication fixe PSX, était implémentée ainsi :

```c
long MULFP(long X, long Y)
{
    unsigned long long result = (long long)(int)X * (long long)(int)Y;
    return ((result >> 32) << 16) | ((result & 0xFFFFFFFF) >> 16);
}
```

Sur PSX, `multo` renvoie un **registre 32 bits** : `(lo >> 16) | (hi << 16)`.
En LP64 le `long` de retour fait 64 bits et `hi << 16` conserve des bits
au-delà de la 32e : les appelants qui gardent le résultat dans un `long`
(la position de spline, accumulée par `+= cspeed`) voient apparaître ces
bits hauts. En ILP32 c'était naturellement tronqué, d'où un bug **invisible
en 32 bits**.

Correctif :

```c
long long product = (long long)(int)X * (long long)(int)Y;
unsigned int hi = (unsigned int)((unsigned long long)product >> 32);
unsigned int lo = (unsigned int)product;
unsigned int value = (lo >> 16) | (hi << 16);
return (long)(int)value;   /* 32 bits signé, comme sur PSX */
```

### Effet mesuré

| métrique (niveau 3, 1800 frames) | avant | après |
| --- | --- | --- |
| positions de spline flyby | `281474976713275` (64 bits) vs `2619` | **identiques** |
| écarts de vertices 32/64 | 300 enregistrements | **300** mais structure de splits identique, Lara identique mesh par mesh |
| `mean_abs_diff` 32 vs 64 | 18.730 | **0.314** |
| pixels dans ±8 | 26.12 % | **99.41 %** |

La référence 32 bits est inchangée (`51d3a1c7…`) ; la référence 64 bits
devient `a1f3d3a6…` (elle inclut le correctif).

Reste : 35 triangles de la **seconde boucle de `DrawLaraL1`** (peau/stash,
`lara_underwater_skin_sweetness_table`) ne sont toujours pas émis en 64 bits
— c'est l'écart résiduel de 0,59 % de pixels.

## 49. RMIG-023 (suite) : pointeurs de meshes de Lara

Deux décalages de pointeurs supposaient des pointeurs 32 bits dans un
tableau `short**` :

- **natte** (`DrawLaraL1`, section cheveux) : `s4 + 4` (shorts) puis
  `s1 += 8` par segment valaient 2 puis 4 **pointeurs** sur PSX, mais 1 puis
  2 en LP64 (8 octets par pointeur) — la natte dessinait de mauvais meshes ;
- **holsters** : `s0 = (int*)&meshes[...]; s0 += 8;` avançait de 32 octets,
  soit 4 pointeurs en LP64 au lieu de 8.

Corrigés en raisonnant en **entrées** (`short**` + 2 / + 4 / + 8), ce qui
donne le même résultat en 32 bits (vérifié : la référence 32 bits reste
`51d3a1c7…`).

Résultat sur la scène de référence (1800 frames) :

| métrique | avant `MULFP` | après `MULFP` | après pointeurs |
| --- | --- | --- | --- |
| `mean_abs_diff` | 18.730 | 0.314 | **0.225** |
| pixels dans ±8 | 26.12 % | 99.41 % | **99.63 %** |
| triangles `0x34` en moins (64 bits) | 31 | 35 | **28** |

Référence 64 bits régénérée : `bcc8a642…`.

Reste : 28 triangles `0x34` (et un `0x3C`) toujours absents en 64 bits. Les
meshes de Lara sont désormais identiques mesh par mesh ; le reste vient
d'une autre section de `DrawLaraL1` (armes/`back_gun` ou la seconde boucle
de peau), à instrumenter de la même façon.

## 50. RMIG-023 résolu : 32 et 64 bits au pixel près

Troisième et dernier correctif de la série : le mesh des **joints de peau**
(`LARA_SKIN_JOINTS`) était indexé avec `s1 += 4` sur un `short*`, soit 2
pointeurs sur PSX mais un seul en LP64. Ce mesh est dessiné pour chaque nœud
de peau (14 nœuds × 2 triangles = 28), d'où exactement les 28 triangles
manquants. Corrigé en `short** s1j = &meshes[...] + 2`.

Histogramme de primitives sur la frame de référence : **identique**
(`nv=3519 34=627(L229) 3C=273(L82)` dans les deux builds).

Captures 1800 frames :

```
32 bits : 63041e5cbf6dcbbd27377b78d6c63e9593743b17690b3c310fefa146e48e3a9b
64 bits : 63041e5cbf6dcbbd27377b78d6c63e9593743b17690b3c310fefa146e48e3a9b
mean_abs_diff=0.000   pixels identiques : 307200 / 307200 (100 %)
```

Les deux builds produisent désormais **le même BMP, octet pour octet**. Les
dumps de vertices ne diffèrent plus que sur 87 des 2777 enregistrements
(phase d'introduction), la frame de référence étant identique.

### Récapitulatif de la série de bugs LP64 corrigés

| bug | effet | commit |
| --- | --- | --- |
| `MULFP` non tronquée à 32 bits | caméras flyby dans des positions absurdes (`2^48 + 2619`) | `8c3263ba` |
| natte : `s4 + 4` / `s1 += 8` sur `short*` | mauvais meshes de cheveux | `f57726cf` |
| holsters : `s0 += 8` sur `int*` | meshes de holsters décalés | `f57726cf` |
| joints de peau : `s1 += 4` sur `short*` | 28 triangles manquants | ce commit |

Écart 32/64 : `mean_abs_diff` **18.730 → 0.000**, pixels à ±8 : 26.12 % →
**100 %**.

## 51. RMIG-022 : ordre des canaux de `StoreFrameBuffer` corrigé

`Emulator_StoreFrameBuffer` recopie l'image affichée dans la VRAM PSX (effet
mono/sépia de `CreateMonoScreen`). La conversion 32 bits → RGB555 inversait
rouge et bleu : `glReadPixels(GL_RGBA)` donne les octets R,G,B,A, dont on
tirait `r5 = R`, `g5 = G`, `b5 = B`, puis on écrivait
`b5 | (g5 << 5) | (r5 << 10)` — soit **B dans les bits 0-4 et R dans les
bits 10-14**, à l'envers du format PSX (R en 0-4, G en 5-9, B en 10-14).

Le portage Vulkan avait reproduit l'anomalie (en utilisant en plus l'alpha
pour le rouge, puisque la lecture hôte est en B,G,R,A).

Correction dans les deux chemins :

```c
/* GL  : c = R | G<<8 | B<<16 | A<<24 */
*data_dst++ = (r5) | (g5 << 5) | (b5 << 10) | 0x8000;

/* Vulkan : memoire B,G,R,A */
dst[fx] = (R >> 3) | ((G >> 3) << 5) | ((B >> 3) << 10) | 0x8000;
```

Vérifications : les captures de référence des deux builds restent
**identiques octet pour octet** (`sha256 63041e5c…`, `mean_abs_diff=0.000`),
ce qui confirme que la scène de référence n'affiche pas l'écran mono. La
preuve visuelle de l'effet demanderait une scène qui l'affiche (inventaire) ;
la correction est vérifiée par construction (mapping RGB555 documenté) et par
la conservation de la parité 32/64.

## 52. Lecteur de cinématique : point de blocage identifié

Diagnostic (niveau 4, sans `TOMB5_SKIP_CUTSCENE`) :

- la scène se rend correctement — l'intro n'affiche plus un écran noir, elle
  **ne joue simplement pas** ;
- `handle_cutseq_triggering` est appelé à chaque frame (trace
  « Handle cutseq triggering name: 4 »), arme `cutseq_trig` puis lance un
  fondu (`SetScreenFadeOut`) ;
- `Load_and_Init_Cutseq` n'aboutit pas : `init_resident_cutseq` n'est jamais
  atteint, et le repli `PCopen("\\CUTSEQ.JIZ")` échoue (fichier absent).

Vérification sur l'image disque fournie (`TOMB5.BIN`, 622 Mo) : les chaînes
`CUTSEQ`, `CUTSEQ.JIZ` et `.JIZ` sont **absentes** du binaire. Les
cinématiques ne sont donc pas dans cette image sous cette forme : le
lecteur ne peut pas être activé sans la source de données correspondante
(disque PC ou fichier extrait), qui n'est pas dans le dépôt.

Conclusion : le lecteur de cinématique n'est pas « à moitié porté », il lui
manque **sa source de données**. Le jeu reste jouable en le sautant
(`TOMB5_SKIP_CUTSCENE=1`) ; l'état est consigné dans RMIG-021.

## 53. Costume 6 (LARA6) : le repli L1 n'a plus besoin de masquer des meshes

Le repli `LaraDrawType=6 → DrawLaraL1` masquait les meshes optionnels
(`mesh_bits = 0x80000000`) parce qu'une pièce « étirait un polygone noir sur
l'écran ». Ce symptôme a disparu avec les correctifs LP64 de RMIG-023
(pointeurs de la natte, des holsters et des joints de peau) : le même pièce
était lue au mauvais endroit et produisait un polygone aberrant.

Vérifications faites avec `TOMB5_LARAMESH`/F11 (override `ffffffff`, qui
prime désormais sur le masque) puis sans masque du tout :

- niveau 4 (The Great Wall) : modèle complet, aucune pièce aberrante ;
- niveau 5 : modèle complet, rendu correct ;
- scène de référence (niveau 3, costume 1) : **capture inchangée**
  (`sha256 63041e5c…`), le masque ne concernait que le type 6.

Le masquage est donc retiré : le costume 6 est dessiné en entier via le
chemin L1. Le module `LARA6` dédié reste absent (le portage exact du costume
demanderait la fonction d'origine), mais le rendu n'est plus amputé.

Capture : `docs/porting/render/lara-costume6-complet.png`.

## 54. RMIG-011 : le résidu 8 bits n'est pas dans le shader

Mesure fine du mode forcé `TOMB5_FORCE_TEXFMT=8` (niveau 3, 300 frames) :
`mean_abs_diff=0.159`, 99,79 % de pixels à ±8, et surtout **662 pixels
seulement** diffèrent, tous situés dans la zone `x ∈ [511, 608]`,
`y ∈ [47, 479]` (bord droit de l'image), avec un écart maximal de 166.

Autrement dit le shader 8 bits (décodage de l'index, CLUT, dither) est
**exact** : les pixels qui divergent ne sont pas des texels 8 bits mais une
bande à droite de l'image (élément 2D/blit rendu par un autre chemin).

Deux tentatives pour rendre l'échantillonnage 8 bits totalement déterministe
(biais d'un millième de texel sur `uv` et sur la position de CLUT, dans les
deux backends) ont été mesurées : **sans effet** (0.159 et 662 pixels
avant/après), puis retirées. Le résidu n'est donc pas une égalité de
`nearest` sur un bord de texel.

RMIG-011 reste ouvert pour cette bande de 662 pixels, à instruire côté
primitives 2D/blit (et non côté shaders de texture).

## 55. Le build 32 bits ne rend pas le niveau 5

En étendant la comparaison 32/64 au niveau 5 (195 salles, costume 6), la
capture 32 bits est **entièrement noire** (vérifié aussi en capturant la
fenêtre avec `import`, donc ce n'est pas un artefact de `glReadPixels`),
alors que `[DRAW]` indique `lvl=5 room=23 nrooms=195 rdt=2` et que le build
64 bits rend la scène normalement.

Le build 32 bits n'est donc pas une référence fiable sur cette scène (il a
probablement une limite de buffers/mémoire sur un niveau de cette taille).
Conséquence pratique : la parité 32/64 se mesure sur le **niveau 3**, où
elle est exacte ; sur les niveaux 4/5 la référence est le rendu Vulkan
64 bits lui-même.

## 56. Script de vérification de parité

`scripts/porting/check_parity.sh [frames]` automatise le contrôle : il lance
le build 64 bits (Vulkan) et le build 32 bits (OpenGL) sur la scène de
référence, puis compare les deux BMP.

- sans argument : 1800 frames (scène officielle) → attendu
  `PARITE OK : captures identiques octet pour octet` ;
- avec un nombre de frames plus court : tolère un pixel de bord isolé, en le
  signalant (`PARITE OK (a 1 pixel pres)`), car seul le run complet de la
  référence est garanti identique à l'octet.

Vérifié : `./scripts/porting/check_parity.sh` →
`63041e5c…` dans les deux builds, `mean_abs_diff=0.000`,
307 200/307 200 pixels identiques.

## 57. Pourquoi le build 32 bits rend noir au niveau 5

Comparaison des compteurs de primitives sur le niveau 5 (195 salles,
`RoomDrawType=2`) :

```
32 bits : [PH] nv=7251  34=371(L298)  3C=1008(L70)  2E=6  3E=8  62=1  E1=1
64 bits : [PH] nv=3102  34=348(L298)  3C=335(L70)   3E=8
```

Le build 32 bits émet **trois fois plus de quads** (`3C` : 1008 contre 335)
pour le même niveau, avec un total de vertices 2,3× supérieur — donc des
primitives en trop, qui recouvrent l'écran (rendu noir) alors que le 64 bits
émet le jeu correct.

Les primitives Lara sont équivalentes (`34(L298)` et `3C(L70)` identiques),
donc le problème est dans le **chemin roomlet** du 32 bits pour
`RoomDrawType=2` (`ROOMLET2.C`), pas dans le rendu ni dans le jeu commun.

Conséquence : le build 32 bits n'est pas une référence fiable sur ce
niveau ; ce n'est **pas** une régression introduite par le portage 64 bits
(le 64 bits rend la scène correctement). À instruire seulement si l'on veut
que le binaire 32 bits de référence couvre tous les niveaux.

## 58. Niveau 5 en 32 bits : piste écartée

Le pointeur `cdb` transmis par les registres GTE `LG2`/`LG3` (technique PSX
pour survivre à un `docop2`) a été vérifié : dans le build 32 bits,
`a1 == (uintptr_t)cdb` (`ok=1`), et `a3` (polyptr) / `s0` (ordering table)
tombent bien dans les buffers bas. Ce n'est donc pas là que le build 32 bits
égare ses primitives.

Le surplus de quads (`3C=1008` contre `335`) reste inexpliqué à ce stade ;
la piste restante est la construction de la liste de salles dessinées
(`number_draw_rooms` / `draw_rooms[]`) ou la boucle roomlet elle-même, qui
pourrait parcourir deux fois la même liste. Instrumentation laissée en
place : `TOMB5_RL2DBG=1` imprime `[RL2] cdb/a1/a3/s0`.

Ce défaut n'affecte que le binaire 32 bits de référence ; le 64 bits rend le
niveau correctement.

## 59. Parité confirmée sur une seconde scène (niveau 4)

La parité 32/64 ne se limite pas au niveau 3. Sur le **niveau 4**
(The Great Wall, 169 salles, `LaraDrawType=6`, c'est-à-dire le chemin du
repli L1 pour le costume 6) :

```
32 bits : 5793e2e1b0997bfdbf61e77c7879f940f763b48849c33418216976f5ffde79e0
64 bits : 5793e2e1b0997bfdbf61e77c7879f940f763b48849c33418216976f5ffde79e0
cmp     : identiques octet pour octet
```

Le script `check_parity.sh` accepte maintenant un niveau en second argument :

```bash
./scripts/porting/check_parity.sh 300 4    # niveau 4
```

Résultat : `PARITE OK : captures identiques octet pour octet`. La parité
couvre donc deux scènes et deux chemins de rendu de Lara (costume 1 et
costume 6 via le repli L1).

## 60. Cinématiques : la donnée existe dans GAMEWAD.OBJ

Correction du §52 : `CUTSEQ.JIZ` **n'est pas absent du disque**, il est
stocké dans `GAMEWAD.OBJ` (entrée 1 de l'archive), pas comme fichier
ISO visible — d'où l'échec du `grep` sur l'image.

Extraction (script ponctuel, hors dépôt) :

```python
# TOMB5.BIN = image MODE2/2352 ; GAMEWAD.OBJ = LBA 24, 55 355 392 octets
# en-tête = 51 entrées { int32 offset; int32 size; }
# entrée 1 (CUTSEQ) : offset 2048, taille 3 299 328
```

Le fichier extrait commence par la signature `(C) DEL!` suivie d'une table
d'offsets/tailles, ce qui correspond à ce qu'attend
`Load_and_Init_Cutseq` (`PCopen("\\CUTSEQ.JIZ")` → `headerbuf[0/1]`).

État du chemin :

- `handle_cutseq_triggering` est appelé à chaque frame mais avec
  `cutseq_num == 0` (`[CUT] name=4 num=0 trig=0`) : la fonction sort
  immédiatement. Elle ne déclenche une cinématique que lorsque
  `NeatAndTidyTriggerCutscene` a armé `cutseq_num` via un trigger
  `TO_CUTSCENE` du niveau ;
- `Load_and_Init_Cutseq` n'est donc jamais atteint au démarrage du niveau 4
  (vérifié par instrumentation `[CUTL]`/`[CUTP]`) ;
- les intros de niveau de TR5 sont des **FMV** : le disque contient
  `FMV0..FMV7.STR` (jusqu'à 62 Mo chacun). Le port n'a pas de lecteur
  MPEG/STR, c'est **cette** fonctionnalité qui manque, pas seulement la
  donnée.

Conclusion : les cinématiques *in-engine* sont désormais data-ready (fichier
extrait ; instrumentation `TOMB5_CUTDBG` en place : `[CUT]`, `[CUTL]`,
`[CUTP]`, `[CUTI]`, `[CUTF]`), mais l'affichage des intros demande un lecteur
FMV (STR/MPEG1 + audio XA), chantier à part entière.

## 61. LARA6 : le module n'existe pas dans le build PSX

Reconnaissance du code d'origine (archive `GAMEWAD.OBJ` → `COD.EWAD`
embarqué, identique pour tous les niveaux, 430 108 octets) :

- en-tête : 96 enregistrements de 20 octets
  `{codeOffset, codeSize, relocOffset, relocSize, slot}` ;
- **59 modules** non vides répartis sur les slots 0..50 ;
- tri par nombre d'instructions `COP2` (GTE) : les cinq modules les plus
  denses sont **tous dans le slot 1** — 14432 à 6812 octets, 178 à 268
  instructions GTE chacun. Ce sont les **cinq variantes de dessin de Lara**
  (L1..L5), celles que le port a déjà portées ;
- **il n'y a pas de sixième module Lara** dans le CODE.WAD du build NTSC
  américain.

Autrement dit : `laraDrawType` est un champ de 3 bits (0..7) et la valeur 6
n'a pas de routine dédiée dans l'original — le jeu retombe sur la routine
standard, exactement comme le fait le port. Le « module LARA6 » que le
commentaire du port appelait de ses vœux **n'a jamais existé** côté PSX.

Ce qui avait fait croire à un modèle cassé :

1. le masquage `mesh_bits = 0x80000000` du repli (retiré, cf. §53) ;
2. les bugs de pointeurs LP64 de la natte/holsters/joints de peau
   (corrigés en RMIG-023), qui faisaient dessiner une pièce aberrante.

Le costume 6 est donc rendu correctement par le repli L1, avec les meshes
du niveau — c'est le comportement attendu. Rien à porter.

## 62. FMV : décodage hors ligne + lecteur branché

Le port n'a pas de décodeur MDEC : `S_PlayFMV` était un stub `return -1`.
Les cinématiques du disque sont bien des **STR (MDEC + XA)**, pas du MPEG1
ISO — `ffmpeg`/`ffprobe` ne savent pas les lire (chaque secteur 2048 porte
un sous-en-tête CD-XA `0x0160` suivi du flux MDEC).

Chaîne mise en place (hors ligne) :

1. extraction des 8 `FMV*.STR` de `TOMB5.BIN` (mode2/2352 → données 2048) ;
2. conversion avec **jpsxdec v2.1** (`java -jar jpsxdec.jar -f FMVn.STR
   -a video -quality high`) → `FMVn.STR[0].avi` (970 frames pour FMV7 en
   1,4 s, ~339 Mo pour les huit) ;
3. hook dans `S_PlayFMV` : si `TOMB5_FMV_DIR` est défini, le jeu lance
   `ffplay -autoexit` sur `<dir>/FMV<n>.avi` et attend la fin ; sinon le
   comportement historique (`-1`, cinématique sautée) est conservé ;
4. `PLAY_FMVS=1` ajouté aux options CMake pour que les entrées `GF_FMV` du
   script gameflow soient réellement lues (`fmv_to_play`).

Vérifié : la parité 32/64 reste **byte-identique** sur la référence après
l'ajout de `PLAY_FMVS` (`63041e5c…`, `PARITE OK`), donc l'analyse du script
n'a rien changé au rendu.

Limite constatée : sur les scénarios testés (démarrage niveau 4, transition
Colosseum → niveau 4), **aucun `S_PlayFMV` n'est appelé** — le déclencheur
(entrée `GF_FMV` du niveau, ou fin de cinématique in-engine) ne s'active pas
dans ces parcours. Le lecteur est donc prêt et testable (menu « Special
Features » ou transition qui déclenche une FMV), mais je n'ai pas encore
trouvé le point d'entrée qui les joue en jeu.

## 63. FMV : déclencheur trouvé, lecture vérifiée

Le §62 concluait qu'aucune FMV n'était déclenchée. C'était faux, pour deux
raisons matérielles :

1. l'option `PLAY_FMVS` ajoutée à `SPEC_PSXPC_N/CMakeLists.txt` n'avait pas
   été appliquée au build (le `flags.make` ne contenait pas
   `-DPLAY_FMVS=1`) : `DoGameflow` sautait donc les entrées `GF_FMV` et,
   surtout, les deux appels d'intro ;
2. `ffplay` retourne **0** quand le fichier demandé n'existe pas (vérifié :
   `ffplay -autoexit -loglevel quiet /nonexistent.avi; echo $?` → `0`), donc
   le `rc=0` du §62 ne prouvait rien. Le nom généré par jpsxdec est
   `FMV0.STR[0].avi`, alors que le hook cherchait `FMV0.avi`.

Correctifs :

- `OPTIONAL_DEFINE(PLAY_FMVS … ON)` effectivement compilé (`-DPLAY_FMVS=1`
  dans `flags.make`) ;
- `S_PlayFMV` vérifie l'existence du fichier avant de lancer le lecteur et
  accepte les deux noms (`FMV<n>.avi` et `FMV<n>.STR[0].avi`) ;
- `TOMB5_FMV_SECONDS=n` borne la lecture (tests) ;
- fenêtre `ffplay` mise à l'échelle 640×480 (`-x 640 -y 480`).

Résultat au démarrage, sans aucune entrée :

```
[FMVREQ] seq=0 flag=0 triggered=00000000
[FMV] lecture de FMV0 (/tmp/opencode/fmv/out/FMV0.avi)
[FMV] fin de FMV0 (rc=0)
[FMVREQ] seq=1 flag=0 triggered=00000001
[FMV] lecture de FMV1 (/tmp/opencode/fmv/out/FMV1.avi)
[FMV] fin de FMV1 (rc=0)
[REPLAY] active frames=30
```

Ce sont les deux intros de `DoGameflow` (`FMV_COPYRIGHT_INTRO` puis
`FMV_GAME_INTRO`), jouées avant l'écran-titre. Captures d'écran prises
pendant la lecture : logo « P R E S E N T S » (FMV0) puis l'intro du jeu
(FMV1). Après la fin des deux films, le jeu reprend la main, atteint le
titre et se termine proprement sous le harnais (`TOMB5_FRAMES=30`).

Le script `SCRIPT.DAT` du disque a par ailleurs été parsé (18 niveaux,
18 noms, 1195 octets de bytecode) : il ne contient **aucune** commande
`GF_FMV` (0x80). Les seules FMV du jeu sont donc ces deux intros ; il n'y a
pas de film par niveau à déclencher.

Outillage reproductible :

```bash
# extraction des 8 FMV*.STR + décodage jpsxdec (Java requis)
python3 scripts/porting/prepare_fmvs.py \
    --disc build/porting/data-ntsc/TOMB5.BIN \
    --out build/porting/fmv \
    --jpsxdec /chemin/vers/jpsxdec.jar
TOMB5_FMV_DIR=build/porting/fmv ./MAIN
```

Le script reconnaît les images MODE2/2352 et ISO 2048, normalise les noms
en `FMV<n>.avi`, et n'écrit jamais de donnée de jeu dans les fichiers
suivis. Trois tests unitaires construisent une image ISO synthétique
(`tests/porting/test_prepare_fmvs.py`).

Limites : le lecteur reste un pont externe (`ffplay`), pas un décodeur MDEC
natif ; les `FMV*.STR` sont vidéo seule (sous-en-tête CD-XA `0x48`, aucun
canal audio), l'audio des films n'est donc pas couvert.

## 64. Cinématiques in-engine : deux bugs LP64, et elles jouent

Le §60 concluait que le déclencheur n'était jamais armé. En forçant
`cutseq_num` (`TOMB5_FORCE_CUT`), le chemin PSX de
`handle_cutseq_triggering` s'est révélé **implémenté** (fade, chargement,
`Load_and_Init_Cutseq`, contrôle, fin), mais il tombait sur deux bugs LP64.

### Bug 1 : table de `CUTSEQ.JIZ` lue en `long`

```c
long* headerbuf = (long*)&tsv_buffer[num];
DEL_CDFS_Seek(headerbuf[0]);
packed = cutseq_malloc(headerbuf[1]);
```

`struct TSV` fait 8 octets (`{offset, taille}`, deux mots 32 bits). En
LP64, `headerbuf[1]` lit l'entrée **suivante** (et `headerbuf[0]` mélange
les deux mots) : pour le cut 7, la taille devenait 1 556 480 au lieu de
84 068, `cutseq_malloc` renvoyait `NULL` et `DEL_CDFS_Read(NULL, …)`
provoquait un SIGSEGV (`CdReadSync`, `DEL_CDFS_Read`, `Load_and_Init_Cutseq`).

Correctif : `int* headerbuf` (les deux branches `DISC_VERSION` et
`PC_VERSION`).

### Bug 2 : `PACKNODE` alloué avec la taille 32 bits

```c
actor_pnodes[n] = cutseq_malloc((pda_nodes + 1) * 84);
```

`84` est `sizeof(struct PACKNODE)` en 32 bits ; en LP64 la structure fait
96 octets (trois pointeurs de 8 octets). Chaque `InitPackNodes` écrivait
donc 12 octets au-delà de chaque nœud, dans l'allocation suivante — et
`camera_pnodes` est alloué juste après les nœuds d'acteurs. La caméra de
cinématique se corrompait dès la frame 2 :

```
f=0  cam=(54134,-646,29938)   (32 et 64 identiques)
f=60 64 bits cam=(57830,1264,31902)   <- divergence
f=60 32 bits cam=(55096,-734,29654)
```

Après `sizeof(struct PACKNODE)`, les positions 32/64 sont identiques à
chaque frame et la capture à 600 frames est **byte-identique**
(`mean_abs_diff=0.000`).

### Harnais

- `TOMB5_FORCE_CUT=<n>` : arme `cutseq_num` une fois, après la fin du
  fondu de chargement (`ScreenFading == 0`) ; sinon `SetScreenFadeOut`
  est ignoré et le déclencheur reste bloqué.
- `TOMB5_CUTDBG=1` : `[CUT]`, `[CUTL]`, `[CUTP]`, `[CUTI]`, `[CUTF]`,
  `[CUTPOS]` (caméra/cible/Lara pendant la cinématique).
- `TOMB5_START_POS="x,y,z,room,rot"` : désormais commun aux builds 32 et
  64 (il était sous `#if defined(__LP64__)`), avec `InitialiseCamera()`
  pour un cadrage déterministe. Utile pour rejouer une vue sans cutscene.

### Validation

Cut 8 (« ANDREA3 », Larson) forcé au niveau 2, où Larson existe :

```
[CUTF] frame=1531 numframes=1538 playing=1 trig=2
[CUT]  name=2 num=8 trig=4 frame=1538 nframes=1538 play=1
[CUT]  name=2 num=0 trig=0 frame=1538 nframes=1538 play=0
```

La cinématique joue ses 1538 frames, le fade de fin s'exécute, puis le
contrôle revient au jeu sans crash. Forcer le même cut au niveau 3 (le
Colosseum, où Larson **n'est pas** un item du niveau) plante dans
`andrea3_end` : c'est un forçage hors contexte, pas un bug du lecteur.

Après la cinématique, les états d'items (151), la caméra, la salle (194),
`ndraw=16` et `draw0` sont identiques entre 32 et 64. Il reste une
divergence de **décor** dans cette vue (lampe suspendue et relief de
dragon absents en 64 bits), mais elle se reproduit **sans cutscene** avec
`TOMB5_START_POS=55808,0,30208,117,-32768` : `mean_abs_diff=0.268`,
3 379 pixels. C'est un bug de rendu du niveau 2, ouvert en RMIG-024, sans
lien avec les cinématiques.

## 65. FMV : un effet de bord VRAM corrigé (retour à 63041e5c)

En activant `PLAY_FMVS`, le boot appelle `S_PlayFMV(FMV_COPYRIGHT_INTRO)`
puis `S_PlayFMV(FMV_GAME_INTRO)`. Même sans `TOMB5_FMV_DIR` (donc sans
lecture), ces appels exécutaient `FMV_InitialiseVRAM()` **avant** le test
du fichier : la VRAM était effacée sur `(0,0,512,256)` et `(0,240)`. Le
chargement du niveau ne réuploadait pas l'icône d'arme, d'où :

- référence niveau 3 : `63041e5c…` → `5aecb72d…` ;
- écart localisé à `x∈[505,611]`, `y∈[38,115]` (icône pistolets),
  2 443 pixels à plus de 8 ;
- **les deux builds identiques** (5aecb72d), donc pas une régression 32/64.

Diagnostic : rebuild avec les changements cinématique remisés → toujours
`5aecb72d` ; rebuild avec les deux appels d'intro désactivés → retour à
`63041e5c`. C'était donc bien l'effet de bord de `S_PlayFMV`.

Correctif : le bloc `FMV_InitialiseVRAM()` / `VSync(0)` / `DispEnv` est
déplacé **dans** la branche de lecture, après la vérification d'existence
du fichier. Une FMV qui n'est pas jouée ne touche plus à l'état PSX.

Après correction : `63041e5c…` de nouveau dans les deux builds, et la
lecture FMV fonctionne toujours (`TOMB5_FMV_SECONDS=2` : `FMV0` puis
`FMV1`, `rc=0`, retour au jeu).
