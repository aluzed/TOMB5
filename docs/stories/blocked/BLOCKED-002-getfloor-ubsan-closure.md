# BLOCKED-002 — Clôture bornée : décalage négatif GetFloor (UBSan)

Auteur : DeepSeek V4.1 Flash via OpenCode. Revue indépendante : PR `re/blocked-002-getfloor-ubsan`.
Date : 28 septembre 2026. Périmètre : borné (GetFloor, `SPEC_PSXPC_N/GETSTUFF.C`). Aucun raw/adresse cible.

## Statut
Défaut **reproduit**, **attribué** (dette ancienne, arithmétique cible authentifiée) et **corrigé**
de façon fidèle. RED UBSan `exit 1` conservé ; GREEN `exit 0` avec **assertions comportementales
inchangées** (288 cas, 0 échec, sortie byte-identique) et sanitizer maintenu en -O0 et -O2.
Revue indépendante déléguée à la PR. Aucune validation sanitaire globale n'est revendiquée.

## Tracker
- [x] Agent assigné, HEAD revalidé (`929a8f78ebec66468864cb1082c1b705d9992a94`), périmètre borné.
- [x] Invocation sanitizer exacte retrouvée ; échec original préservé (archive RED).
- [x] Reproduction sur vraie TU avec les mêmes flags ; baseline attribuable ; dette ancienne qualifiée.
- [x] Contrat arithmétique cible établi (valeurs négatives et frontières signées).
- [x] RED puis correction minimale ; GREEN, assertions inchangées, sanitizer maintenu.
- [x] Non-régression vérifiée sur la matrice RE-783 (composition/observer × current/baseline).
- [x] Ticket et index actualisés ; limites non couvertes documentées.

## Reproduction exacte (RED)
Harnais RE-781 (contrat callback) compilant le **TU réel** `SPEC_PSXPC_N/GETSTUFF.C`, `COLLIDE_S.C`
et `OBJECTS.C`, avec `-fsanitize=undefined -fno-sanitize-recover=all` :

```
python3 tests/reverse/fixtures/re781/run_test.py --root . \
  --source SPEC_PSXPC_N/GETSTUFF.C --output <out> --ubsan
```

Résultat conservé avant correction : `exit 1`, diagnostic
`SPEC_PSXPC_N/GETSTUFF.C:338:27: runtime error: left shift of negative value -32`.
La cause est `(floor->ceiling << 8)` : `ceiling` est un `char` signé (décalage à gauche d'une
valeur négative = non défini en C/C++).

## Préexistence (pas une régression)
La ligne est introduite le 2020-06-01 (commit `271a4077`), bien antérieure à RE-781/782/783. La
baseline égale au HEAD de reprise (`929a8f78`) recompile le **même** diagnostic `exit 1` : dette
ancienne, non créée par les correctifs callback/registration.

## Contrat arithmétique cible
Désassemblage PSX `SPEC_PSX/GETSTUFF.MIP`, comparaison plafond de GetFloor (bloc terminal) :
`lb` (chargement d'octet **signé**, offset 7 = `ceiling`) suivi de `sll 8` (décalage logique
gauche 32 bits). Le chargement de `floor` (offset 5) suit le même schéma signé, tandis que
`pit_room`/`sky_room` utilisent un chargement non signé. La valeur cible est donc
**sign-extension puis multiplication par 256**, sans perte de bits pour un `char` signé.
Cette arithmétique est identique aux **quatre** comparaisons signées de GetFloor (lignes 297, 329,
338, 371) ; n'en corriger qu'une laisserait les trois autres en UB latent.

## Correction (minimale, fidèle)
Les quatre `field << 8` signés deviennent `((signed char)field * 256)` :

```
- if (y >= floor->floor << 8)              + if (y >= (signed char)floor->floor * 256)
- if (y < (floor->floor << 8))             + if (y < ((signed char)floor->floor * 256))
- if (y >= (floor->ceiling << 8))          + if (y >= ((signed char)floor->ceiling * 256))
- } while (y < (floor->ceiling << 8));     + } while (y < ((signed char)floor->ceiling * 256));
```

Multiplication par 256 après conversion signée explicite : définie, sans débordement
(domaine -32768..32512 pour un `char` signé) et **bit-identique** à `sll 8`.

## Preuves rerunnables
- RED (baseline `929a8f78`) + UBSan : `exit 1`, diagnostic ci-dessus.
- GREEN (source corrigé) + UBSan : `exit 0`, `SUMMARY checks=288 failures=0`, stderr vide, en
  `-O0` et `-O2`.
- **Assertions inchangées** : sortie standard du source corrigé **byte-identique** à la baseline
  non instrumentée (288 PASS).
- **Équivalence exhaustive** : sur les 256 valeurs de `char` signé, l'expression corrigée égale
  `(int)((uint32_t)(int)c << 8)` (sémantique cible `lb`+`sll`) — programme privé sous `build/`.
- **Non-régression RE-783** : composition current 296/0, baseline 296/52 ; observer current 514/0,
  baseline 514/132 ; identique en normal et UBSan ; aucun diagnostic sanitizer.
- Test public ajouté : `tests/reverse/test_blocked002_getfloor_negative_shift.py` (RED baseline
  épinglée, GREEN source courant). Le harnais RE-781 reçoit un mode optionnel `--ubsan`.

Preuves brutes (ignorées par Git) : `build/reverse/blocked-002-getfloor-ubsan/`
(`red-baseline/`, `green-fixed/`, `baseline-normal/`, `equiv/`, `commands.sh`).

## Limites non couvertes
Le même motif de décalage signé subsiste, **hors périmètre de ce ticket**, dans GetCeiling et
GetHeight de `SPEC_PSXPC_N/GETSTUFF.C` ainsi que dans les chemins GetFloor de `GAME/CONTROL.C`.
Registration native, gameplay et autres backends/ABI ne sont pas couverts ici. Aucun GREEN UBSan
global n'est revendiqué.
