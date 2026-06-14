# Layout PS-X EXE et adresses TOMB5 PS1

Date: 2026-06-14
Story: `docs/stories/RE-008-conventions-reverse-ps1-tr5.md`
Status: Done

## Progress tracker

- [x] Documenter les champs utiles du header `PS-X EXE`.
- [x] Documenter les valeurs vérifiées pour `SLUS_013.11`.
- [x] Documenter les conversions adresse RAM / offset payload / offset fichier.
- [x] Documenter le workflow d'import Ghidra.
- [x] Documenter les overlays `.MOD` / `.BIN` et la relation avec `RELOC`.

## Baseline vérifiée

Executable de référence:

- Nom: `SLUS_013.11`
- Source: `SYSTEM.CNF` contient `BOOT=cdrom:\SLUS_013.11;1`
- Version: PSX NTSC v1.0
- MD5 attendu: `4ef523e708d7a7d6571F39C6E47784F9` dans `CONTRIBUTING.md`
- MD5 vérifié par le workflow: `4ef523e708d7a7d6571f39c6e47784f9`

Les fichiers extraits du disque restent sous `build/reverse/` et ne doivent pas être versionnés.

## Header `PS-X EXE`

Un executable PlayStation `PS-X EXE` commence par un header de `0x800` octets. Pour ce projet, `scripts/reverse/prepare_ghidra_psx.py` lit les champs utiles suivants:

- magic à offset `0x00`: `PS-X EXE`;
- PC / entrypoint raw à offset `0x10`;
- text base raw à offset `0x18`;
- text size à offset `0x1c`;
- stack raw à offset `0x30`.

Le script normalise les adresses inférieures à `0x80000000` en KSEG0 par OR avec `0x80000000`. Exemple: `0x00010000` devient `0x80010000`.

## Valeurs vérifiées pour `SLUS_013.11`

Valeurs issues de `docs/reverse/ghidra-workflow.md` et du parseur `prepare_ghidra_psx.py`:

- entrypoint: `0x8007663c`
- text base: `0x80010000`
- text size: `606208` octets (`0x94000`)
- stack: `0x801ffff0`
- header size: `0x800`
- payload importé dans Ghidra: `SLUS_013.11.payload.bin`, taille `0x94000`

Plage RAM principale du payload:

- début inclus: `0x80010000`
- fin exclue: `0x800a4000`

Calcul: `0x80010000 + 0x94000 = 0x800a4000`.

## Conversions d'adresses

Pour une adresse RAM dans le payload principal:

```text
payload_offset = ram_address - 0x80010000
psx_exe_file_offset = 0x800 + payload_offset
```

Exemples:

- `0x80010000` → payload offset `0x0`, fichier `PS-X EXE` offset `0x800`.
- `0x8007663c` → payload offset `0x6663c`, fichier `PS-X EXE` offset `0x66e3c`.
- `0x800a3fff` → payload offset `0x93fff`, fichier `PS-X EXE` offset `0x947ff`.

Si l'adresse est écrite sans préfixe KSEG0 dans un commentaire repo, le mapping la normalise:

- `60D54` → `0x80060d54`.
- `80060D54` → `0x80060d54`.

## Import Ghidra canonique

Ghidra headless ne charge pas directement le `PS-X EXE` dans cet environnement. Le workflow canonique est:

```bash
python3 scripts/reverse/prepare_ghidra_psx.py
```

Ou, explicitement:

```bash
analyzeHeadless build/reverse/ghidra-projects tomb5_psx_ntsc \
  -import build/reverse/extracted/SLUS_013.11.payload.bin \
  -processor MIPS:LE:32:default \
  -cspec default \
  -loader BinaryLoader \
  -loader-baseAddr 0x80010000 \
  -analysisTimeoutPerFile 300 \
  -deleteProject
```

Points importants:

- Importer le payload sans le header `0x800`.
- Utiliser `MIPS:LE:32:default`.
- Utiliser `-loader-baseAddr 0x80010000`.
- Ne pas committer le projet Ghidra généré.

## Mapping repo ↔ Ghidra

Le script `scripts/reverse/map_ghidra_to_repo.py`:

1. prépare ou réutilise le payload;
2. exporte les fonctions Ghidra avec `ExportGhidraFunctions.java`;
3. parse les commentaires de fonctions C;
4. normalise les adresses vers `0x80xxxxxx`;
5. mappe principalement sur l'adresse final PSX.

Commentaire type:

```c
void S_LoadLevelFile(int Name)//60188(<), 60D54(<) (F) (*) () (D) (D)
```

Dans ce commentaire:

- beta: `0x80060188`;
- final: `0x80060d54`;
- l'adresse final est celle utilisée comme clé de rapprochement principale avec Ghidra.

## Overlays et modules

`MODULE.md` décrit deux formats importants:

### `.MOD`

Fichier externe généré par `DEL2FAB.EXE /c+`, utilisé comme overlay PlayStation chargé/déchargé à runtime.

Structure conceptuelle:

```c
struct MOD
{
    unsigned int* pRel;   // pointeur relatif à l'offset 0x8 vers les infos de relocation
    unsigned int relSize; // taille des infos de relocation
    // section header optionnelle, souvent table de fonctions
    char* binData[];     // code/data MIPS overlay
    unsigned int* relData[];
};
```

### `.BIN` overlay standard

Structure conceptuelle:

```c
struct BIN
{
    // section header optionnelle
    char* binData[];
};
```

## Relation avec `RELOC`

Dans `PSXPC_N`, les macros par défaut documentées par `CONTRIBUTING.md` incluent:

- `PSX_VERSION=1`
- `PSXPC_TEST=1`
- `RELOC=0`
- `USE_32_BIT_ADDR=1`

Conséquence pratique:

- Si `RELOC=1`, le code peut relocaliser un module/overlay via les données `.REL`.
- Si `RELOC=0`, il ne faut pas appeler la relocation sur des données PSX brutes comme si elles étaient des pointeurs hôtes.

Le correctif RE-005 applique cette règle dans `SPEC_PSXPC_N/ROOMLOAD.C`: l'appel à `RelocateModule()` sur `SETUP.MOD` est gardé par `#if RELOC`, comme le chemin `SPEC_PSX`.

## Données disque 32-bit vs structures hôtes

Le disque PSX encode des pointeurs/offsets 32-bit little-endian. En build Linux x86_64, les pointeurs C et `long` sont 64-bit. Ne pas supposer qu'une structure C hôte peut être castée directement sur un blob disque PSX.

Symptôme connu RE-005:

```text
LoadLevel() at GAME/SETUP.C:1204
*(int*)&ptr[4 + (j * 4)] += (*(int*)&room[i].data);
ptr = 0x5555642761af <error: Cannot access memory at address ...>
```

Interprétation: le code a progressé au-delà de l'ancien crash `RelocateModule()`, mais le chargement de room finit par reconstruire un pointeur invalide en x86_64.

Pistes de correction futures:

1. Rendre un build Linux 32-bit reproductible pour respecter les hypothèses historiques.
2. Ou séparer les structures disque 32-bit des structures runtime hôtes, puis convertir explicitement offsets/adresses.

## Checklist Ghidra pour une adresse

Pour analyser une fonction à partir d'un commentaire repo:

1. Lire l'adresse final dans le commentaire, pas seulement la beta.
2. Normaliser en `0x80xxxxxx` si nécessaire.
3. Vérifier que l'adresse est dans la plage `0x80010000..0x800a4000` pour le payload principal.
4. Si elle est hors plage, suspecter un overlay, une donnée, une adresse beta, ou un commentaire incomplet.
5. Dans Ghidra, aller à l'adresse RAM normalisée.
6. Comparer le nom et la signature avec le fichier source repo.
7. Avant de renommer ou marquer `(F)/(D)`, vérifier les bit-fields et tailles de types.

## Fichiers générés acceptables

Les rapports versionnés sous `docs/reverse/generated/` sont des synthèses textuelles/CSV/JSON:

- `ghidra-functions.csv`
- `repo-functions.csv`
- `repo-function-map.csv`
- `mapped-functions.md`
- `repo-only-functions.md`
- `unmapped-ghidra-functions.md`
- `function-map-summary.json`

Les extractions et projets complets restent sous `build/reverse/` et ne sont pas à committer.
