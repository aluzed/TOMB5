# État du portage 64 bits (novembre 2026)

Synthèse opérationnelle : ce qui fonctionne, comment le vérifier, ce qui
reste. Détail chronologique dans `vulkan-64bit-plan.md`, suivi ticket par
ticket dans `render-backlog.json` / `render/`.

## En une phrase

Le jeu tourne en **64 bits**, rendu **exclusivement en Vulkan** (OpenGL a
été retiré du binaire), et les builds 32 et 64 bits produisent désormais
**la même image, octet pour octet**, sur la scène de référence.

## Ce qui fonctionne

| domaine | état |
| --- | --- |
| Chargement, niveau, sauvegardes F5/F6 | 64 bits |
| Rendu Vulkan (pipeline PSX complet) | 4/8/16 bits, CLUT, dither, blends, ordering tables, blit VRAM |
| Parité 32 ↔ 64 bits | **captures byte-identiques** sur deux scènes : niveau 3 (`63041e5c…`) et niveau 4 (`5793e2e1…`, costume 6) |
| Overlay debug F12 (ImGui) | stats, profilage GPU par passe, budget, dithering, formats, reflets, capture BMP, aperçu VRAM |
| Reflets écran à presets | aucun / faible / moyen / fort, preset « aucun » = image de référence exacte |
| Campagne | Streets of Rome → Colosseum terminés, transition vers le niveau 4 re-validée, niveaux 4 et 5 rendus |
| FMV (intros) | lecture vérifiée : extraction + décodage hors ligne, `TOMB5_FMV_DIR` → `ffplay` (vidéo seule) |
| Cinématiques in-engine | cut 8 joué en entier (1538 frames) puis retour au jeu ; caméra et image identiques 32/64 pendant la lecture |
| Couverture tests | **4191 tests PASS** |

## Comment lancer

```bash
# build 64 bits (Vulkan par défaut)
cd build/porting/build64 && make -j4
cd build/porting/data-ntsc && ../build64/SPEC_PSXPC_N/MAIN

# build 32 bits (OpenGL, référence)
cd build/porting/build32-check && make -j4
```

Variables utiles :

| variable | effet |
| --- | --- |
| `TOMB5_START_LEVEL=n` | sauter le menu, charger le niveau `n` |
| `TOMB5_SKIP_CUTSCENE=1` | ne pas déclencher les cinématiques in-engine |
| `TOMB5_FORCE_CUT=n` | force une cinématique in-engine (cut `n`) |
| `TOMB5_CUTDBG=1` | trace `[CUT]`, `[CUTL]`, `[CUTF]`, `[CUTPOS]` |
| `TOMB5_START_POS="x,y,z,room,rot"` | place Lara au premier frame (32 et 64 bits) |
| `TOMB5_FMV_DIR=<dir>` | joue les intros `FMV<n>.avi` avec `ffplay` (voir `scripts/porting/prepare_fmvs.py`) |
| `TOMB5_FMV_SECONDS=n` | borne la lecture d'une FMV (tests) |
| `TOMB5_FMVDBG=1` | trace `[FMVREQ]`, `[FMV]`, `[GFMV]` |
| `TOMB5_FRAMES=n` + `TOMB5_CAPTURE=f.bmp` | harnais déterministe : n frames puis capture et sortie |
| `TOMB5_DUMP_VERTS=f.bin` | dump des vertices/splits envoyés au backend |
| `TOMB5_DUMP_VRAM=f.bin` | dump de la VRAM à la frame de capture |
| `TOMB5_FORCE_TEXFMT=4/8/16` | force la profondeur de texture (validation) |
| `TOMB5_RENDERER=gl` | refusé en 64 bits (message explicite), accepté en 32 bits |
| `TOMB5_VK_DEBUG=1` | validation layers Vulkan |

Overlay F12 : `Reflets`, `Dithering`, profondeur de texture forcée, aperçu
VRAM, bouton de capture. Les entrées du jeu sont bloquées quand il est
ouvert.

## Vérifier la parité en une commande

```bash
./scripts/porting/check_parity.sh          # 1800 frames, niveau 3 (référence)
./scripts/porting/check_parity.sh 300      # contrôle rapide, niveau 3
./scripts/porting/check_parity.sh 300 4    # seconde scène (niveau 4, costume 6)
```

Le script lance le build 64 bits (Vulkan) puis le 32 bits (OpenGL) sur la
scène de référence, compare les deux BMP et sort en erreur si l'image
diffère. Sur la scène de référence il affiche
`PARITE OK : captures identiques octet pour octet` ; sur des durées plus
courtes il tolère le pixel de bord isolé (en le signalant).

## Scène de référence

Niveau 3, 1800 frames, aucune entrée (`TOMB5_START_LEVEL=3`,
`TOMB5_FRAMES=1800`, `TOMB5_CAPTURE=…`).

```
32 bits : 63041e5cbf6dcbbd27377b78d6c63e9593743b17690b3c310fefa146e48e3a9b
64 bits : 63041e5cbf6dcbbd27377b78d6c63e9593743b17690b3c310fefa146e48e3a9b
mean_abs_diff = 0.000     (307 200 / 307 200 pixels identiques)
```

Historique : l'écart était de `mean_abs_diff=18.730` (26 % de pixels à ±8)
avant la série de correctifs LP64 (voir ci-dessous).

## Correctifs LP64 qui ont amené la parité

| bug | symptôme | où |
| --- | --- | --- |
| `MULFP` non tronquée à 32 bits | caméras flyby à des positions absurdes | `SPEC_PSXPC_N/GETSTUFF.C` |
| natte / holsters : décalages en octets sur `short** meshes[]` | mauvais meshes de Lara | `SPEC_PSXPC_N/LARA1.C` |
| joints de peau : `s1 += 4` sur `short*` | 28 triangles manquants | `SPEC_PSXPC_N/LARA1.C` |
| ordre des canaux de `StoreFrameBuffer` | mono/sépia avec rouge et bleu inversés | `EMULATOR/EMULATOR.C`, `RENDERER_VK.C` |

Règle générale : **tout décalage écrit en octets ou en `short*` sur un
tableau de pointeurs est faux en LP64** ; il faut raisonner en entrées.

## Limites connues

- **Cinématiques in-engine** : fonctionnelles. Deux bugs LP64 corrigés —
  la table de `CUTSEQ.JIZ` était lue en `long` (8 octets) et les `PACKNODE`
  des acteurs étaient alloués sur 84 octets au lieu de `sizeof` (96). Le cut 8
  joue ses 1538 frames au niveau 2 et rend la main au jeu ; `TOMB5_FORCE_CUT`
  permet de le rejouer. La caméra est identique 32/64.
- **FMV** : les intros sont jouées via `ffplay` (dépendance externe), pas par
  un décodeur MDEC natif ; les `FMV*.STR` sont **vidéo seule** (sous-en-tête
  CD-XA `0x48`), l'audio éventuel vient des pistes XA et n'est pas couvert.
- **`LARA6`** : le module n'existe pas dans le build PSX (5 variantes Lara
  seulement, cf. §61 du plan) ; le costume 6 utilise le chemin L1, comportement
  conforme à l'original.
- **Raytracing matériel (RMIG-015)** : impossible sans géométrie monde ni
  normales — le flux PSX ne contient que des coordonnées écran. Les reflets
  livrés sont des reflets écran stylisés.
- **Résidu 8 bits (RMIG-011)** : 662 pixels en mode forcé, hors des shaders
  de texture (bande à droite de l'image, chemin 2D/blit).
- **Décor niveau 2 (RMIG-024)** : sur la salle 194, une lampe suspendue et un
  relief de dragon manquent en 64 bits (`mean_abs_diff=0.268`, 3 379 pixels).
  Reproduit sans cinématique via `TOMB5_START_POS` ; items et caméra identiques.
- **Sauvegardes 32 ↔ 64** : incompatibles (checksum), chaque binaire crée
  la sienne.
- **Comparaison 32/64 limitée au niveau 3** : sur le niveau 5 (195 salles),
  le build **32 bits rend un écran noir** (fenêtre et capture noires, alors
  que `[DRAW]` montre `lvl=5 room=23 nrooms=195 rdt=2`), tandis que le build
  64 bits rend la scène correctement. Le 32 bits n'est donc une référence
  fiable que sur les scènes qu'il sait rendre ; la parité mesurée porte sur
  le niveau 3.
- Quelques éléments de gameplay non portés (télépodes, lasers, poissons,
  `DrawScaledSpike`, `DrawWeaponMissile`, cordes, `UpdateGunShells`) —
  sans effet sur le parcours validé.

## Prochaines étapes utiles

1. Corriger la divergence de décor du niveau 2 (RMIG-024).
2. Remplacer le pont `ffplay` par un décodeur MDEC natif et couvrir l'audio
   XA des FMV.
3. Instruire la bande 2D du résidu 8 bits (RMIG-011).
4. Poursuivre la campagne au-delà du niveau 5.
