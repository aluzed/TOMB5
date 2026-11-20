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
| Couverture tests | **4188 tests PASS** |

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
| `TOMB5_SKIP_CUTSCENE=1` | ne pas déclencher les cinématiques (lecteur sans données) |
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

- **Cinématiques** : le lecteur retombe sur `CUTSEQ.JIZ`, absent de l'image
  fournie (aucune chaîne `CUTSEQ` ni `.JIZ` dans `TOMB5.BIN`). Blocage de
  données. En attendant : `TOMB5_SKIP_CUTSCENE=1`.
- **`LARA6`** : le module dédié n'est pas porté ; le costume 6 est dessiné
  en entier via le chemin L1 (rendu correct, costume non exact).
- **Raytracing matériel (RMIG-015)** : impossible sans géométrie monde ni
  normales — le flux PSX ne contient que des coordonnées écran. Les reflets
  livrés sont des reflets écran stylisés.
- **Résidu 8 bits (RMIG-011)** : 662 pixels en mode forcé, hors des shaders
  de texture (bande à droite de l'image, chemin 2D/blit).
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

1. Fournir la source des cinématiques (`CUTSEQ.JIZ` ou disque d'origine)
   pour activer les intros.
2. Porter le module `LARA6` (nécessite la fonction d'origine).
3. Instruire la bande 2D du résidu 8 bits (RMIG-011).
4. Poursuivre la campagne au-delà du niveau 5.
