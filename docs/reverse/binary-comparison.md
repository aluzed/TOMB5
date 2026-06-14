# Comparaison binaire / désassemblage PS1

Date: 2026-06-14
Story: `docs/stories/RE-007-comparaison-binaire-disassembly.md`
Status: Done

## Progress tracker

- [x] Définir un format de dump de désassemblage par fonction.
- [x] Extraire les bytes/instructions originales par nom ou adresse.
- [x] Documenter comment produire un artefact recompilé comparable.
- [x] Créer un outil de diff par fonction/plage extraite.
- [x] Documenter les différences acceptables et les limitations.
- [x] Lier le workflow aux marqueurs `(**)`, `(F)`, `(D)` et `(ND)`.

## Périmètre et règle de versionnement

Les instructions/bytes originaux du jeu restent du contenu original. Les dumps produits par RE-007 sont donc écrits par défaut sous:

```text
build/reverse/re007/
```

Ce répertoire est ignoré par git via `/build/reverse/*`. Ne pas committer:

- dumps CSV/Markdown contenant des instructions originales;
- payload `SLUS_013.11.payload.bin`;
- projets Ghidra;
- binaires recompilés ou extraits lourds.

Les fichiers versionnés pour RE-007 sont uniquement les scripts et cette documentation.

## Entrées utilisées

- Mapping repo/Ghidra: `docs/reverse/generated/repo-function-map.csv`
- Payload original local ignoré: `build/reverse/extracted/SLUS_013.11.payload.bin`
- Text base: `0x80010000`
- Adresses de référence: voir `docs/reverse/psx-exe-layout.md`
- Conventions de marqueurs: voir `docs/reverse/conventions.md`

## Format de dump

`scripts/reverse/disasm_extract.py` produit un CSV par fonction avec les colonnes:

- `index`: index instruction dans la fonction.
- `ram_address`: adresse PSX KSEG0.
- `payload_offset`: offset dans le payload sans header `PS-X EXE`.
- `word_le_hex`: mot instruction 32-bit lu little-endian.
- `instruction`: décodage MIPS minimal et stable.

Le dump Markdown associé rappelle la fonction, le fichier source et les adresses, mais reste dans `build/reverse/re007/`.

## Extraire une fonction originale

Exemples:

```bash
python3 scripts/reverse/disasm_extract.py SaveLevelData
python3 scripts/reverse/disasm_extract.py 0x80053f10 --max-bytes 128
python3 scripts/reverse/disasm_extract.py S_UpdateInput --out-dir build/reverse/re007/original
```

Résultat typique:

```text
build/reverse/re007/original/SaveLevelData_80053f10.csv
build/reverse/re007/original/SaveLevelData_80053f10.md
```

Le sélecteur peut être:

- nom de fonction repo;
- nom Ghidra;
- adresse PSX finale, par exemple `0x80053f10`.

Si plusieurs lignes repo correspondent à la même adresse, le script choisit la première entrée mappée avec `body_size` disponible et affiche un avertissement.

## Comparer deux dumps

Une fois un dump comparable généré pour la version recompilée, utiliser:

```bash
python3 scripts/reverse/compare_function.py \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  build/reverse/re007/rebuilt/SaveLevelData_80053f10.csv \
  --name SaveLevelData
```

Le rapport est écrit par défaut sous:

```text
build/reverse/re007/compare/SaveLevelData.csv
build/reverse/re007/compare/SaveLevelData.md
```

`compare_function.py` compare:

- `word_le_hex` pour une équivalence binaire stricte;
- `instruction` pour signaler un éventuel match assembleur textuel même si les mots diffèrent.

Le script retourne `0` uniquement si toutes les instructions ont un match exact de mot 32-bit.

## Produire un dump recompilé comparable

Le repo actuel ne produit pas encore un binaire PS1 final complet directement comparable au `SLUS_013.11` de référence. Le workflow RE-007 prépare donc l'interface de comparaison et documente la marche à suivre lorsqu'un artefact comparable existe.

Options attendues:

1. Build PS1/toolchain historique produisant un objet/exécutable MIPS little-endian avec les mêmes options que l'original.
2. Extraction d'une plage `.text` ou d'un objet relogeable déjà normalisé.
3. Conversion de cette plage vers le même format CSV que `disasm_extract.py`:
   - `index`
   - `ram_address`
   - `payload_offset`
   - `word_le_hex`
   - `instruction`

Le point important est de comparer des mots machine MIPS little-endian, pas du pseudocode C.

## Interprétation des résultats

### Pour `(**)`

`(**)` exige un match strict:

- même nombre d'instructions;
- mêmes `word_le_hex`;
- mêmes adresses/plages comparées;
- options de compilation et source de l'artefact documentées.

Un simple match textuel approximatif ou un raisonnement fonctionnel ne suffit pas.

### Pour `(F)`

`(F)` peut être justifié par une comparaison instructionnelle plus souple:

- branches et delay slots expliqués;
- accès mémoire et types/bit-fields vérifiés;
- appels et constantes cohérents avec Ghidra;
- code repo compile encore.

`(F)` ne prétend pas nécessairement à un binaire identique.

### Pour `(D)`

`(D)` ajoute une preuve fonctionnelle:

- chemin runtime testé, ou blocage documenté précisément;
- cas limites raisonnés;
- différence binaire acceptée seulement si le comportement est équivalent.

### Pour retirer `(ND)`

Ne retirer `(ND)` que si la fonction a été couverte par:

- comparaison suffisante avec l'original;
- ou test/debug qui démontre le comportement attendu.

## Différences acceptables hors `(**)`

Acceptables pour `(F)`/`(D)` si documentées:

- registres temporaires différents sans changement de valeurs observables;
- scheduling différent compatible avec les delay slots;
- padding/nops hors corps logique;
- offsets de relocation ou adresses reconstruites différemment dans un build non final;
- réordonnancement local qui conserve les effets mémoire et les branches.

Non acceptables sans investigation:

- instruction de branche différente;
- cible de call/jump différente;
- chargement/store à offset différent;
- constante immédiate différente;
- delay slot modifié;
- taille de fonction différente sans explication.

## Validation RE-007

Validation locale effectuée:

```bash
python3 -m py_compile scripts/reverse/disasm_extract.py scripts/reverse/compare_function.py
python3 scripts/reverse/disasm_extract.py SaveLevelData --max-bytes 64
python3 scripts/reverse/compare_function.py \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  build/reverse/re007/original/SaveLevelData_80053f10.csv \
  --name SaveLevelData_selftest
```

Le self-test compare le dump original à lui-même et doit retourner `exact_match=yes`.

## Limitations connues

- Le décodeur MIPS intégré est volontairement minimal; les mots non reconnus restent en `.word`.
- Les dumps générés contiennent du code original: garder sous `build/reverse/re007/`.
- La comparaison binaire stricte dépend d'un artefact recompilé PS1 réellement comparable; le build Linux `PSXPC_N` n'est pas un substitut.
- Les overlays/modules `.MOD` nécessiteront un text base et une relocalisation propres avant d'utiliser le même workflow.
