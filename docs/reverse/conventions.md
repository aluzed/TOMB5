# Conventions de reverse PS1/TR5

Date: 2026-06-14
Story: `docs/stories/RE-008-conventions-reverse-ps1-tr5.md`
Status: Done

## Progress tracker

- [x] Relier les conventions aux sources existantes du repo.
- [x] Documenter la convention d'adresses beta/final PSX.
- [x] Documenter les marqueurs de progression `(F)`, `(D)`, `(**)`, `(ND)`.
- [x] Documenter les pièges Ghidra/PS1 les plus fréquents.
- [x] Définir une checklist avant de changer un marqueur de fonction.

## Sources de référence

- `CONTRIBUTING.md`: format des commentaires de fonctions, marqueurs et versions de base.
- `TIPS.md`: notes historiques sur les bit-fields.
- `MODULE.md`: format `.MOD` / `.BIN` des overlays.
- `docs/reverse/ghidra-workflow.md`: workflow Ghidra reproductible, import raw MIPS LE, mapping repo.
- `docs/reverse/progress.md`: définitions générées des statuts de progression.
- `scripts/reverse/map_ghidra_to_repo.py`: parsing réel des commentaires repo et normalisation des adresses.

## Versions et périmètre

La baseline PSX utilisée par les scripts est:

- Disc boot executable: `SLUS_013.11`
- Version repo attendue: PSX NTSC v1.0
- MD5 attendu: `4EF523E708D7A7D6571F39C6E47784F9` dans `CONTRIBUTING.md`; les scripts comparent en minuscule.

Le workflow Ghidra actuel cible le payload MIPS little-endian du `PS-X EXE` final NTSC. Les commentaires du code peuvent aussi contenir une adresse beta interne.

## Commentaires de fonctions

Format canonique observé:

```c
int main()//10064(<), 10064(<) (F) (*) (D) (ND)
```

Interprétation:

- Première adresse: adresse PSX internal beta.
- Deuxième adresse: adresse PSX final.
- Si une seule adresse est présente, les scripts l'utilisent comme beta et final.
- `(<)` indique que le code appartient à cette version selon la convention historique du repo.
- Les marqueurs entre parenthèses suivent les adresses.
- `*` peut apparaître dans les commentaires historiques comme placeholder / état intermédiaire; ne pas le confondre avec `(**)`.

Les scripts normalisent les adresses courtes vers KSEG0:

- `10064` devient `0x80010064`.
- `0x80010064` reste `0x80010064`.

Pour le mapping Ghidra ↔ repo, l'adresse final PSX est la clé principale utilisée dans `scripts/reverse/map_ghidra_to_repo.py`.

## Marqueurs de progression

Définitions issues de `CONTRIBUTING.md` et des rapports générés:

- `(**)`: la recompilation produit un code identique à l'original. Niveau le plus strict. Ne pas utiliser sans comparaison binaire/désassemblage fiable.
- `(F)`: fonction considérée finalisée / pleinement décompilée.
- `(D)`: fonction debugguée et fonctionnellement équivalente à l'original. Dans le reporting, c'est au moins aussi fort que `(F)` pour le suivi.
- `(ND)`: fonction non debugguée; peut ne pas être fonctionnellement équivalente.
- absence de `(F)`/`(D)`/`(**)`: fonction encore à traiter ou seulement nommée/mappée.

Règle pratique pour le niveau 1: `(**)` est hors scope tant que RE-007 n'a pas mis en place une comparaison binaire/désassemblage robuste.

## Nommage Ghidra et repo

Quand une fonction Ghidra est mappée à une fonction repo:

1. Conserver le nom C du repo si l'adresse final correspond.
2. Ne pas renommer une fonction Ghidra auto (`FUN_`, `SUB_`, `LAB_`, `loc_`, `DAT_`, `PTR_`, `switchD_`) vers un nom inventé sans preuve.
3. Si le rôle est seulement supposé, préférer une note ou un nom temporaire explicite plutôt qu'un nom définitif.
4. Quand deux adresses ou deux fonctions semblent se chevaucher, vérifier beta/final et les overlays avant de renommer.
5. Garder la signature C proche du code existant: éviter les refactors d'architecture; le repo privilégie la comparabilité avec le MIPS original.

## Pièges Ghidra / PS1

### Import PS-X EXE

Dans cet environnement, Ghidra headless n'importe pas directement le `PS-X EXE` original. Le workflow vérifié strippe le header `0x800` puis importe le payload brut:

```bash
analyzeHeadless build/reverse/ghidra-projects tomb5_psx_ntsc \
  -import build/reverse/extracted/SLUS_013.11.payload.bin \
  -processor MIPS:LE:32:default \
  -cspec default \
  -loader BinaryLoader \
  -loader-baseAddr 0x80010000
```

Ne pas analyser le fichier avec son header `PS-X EXE` comme si le code commençait à offset `0`.

### Adresses fichier vs RAM

- Offset fichier payload `0x0` correspond à `0x80010000` en RAM.
- Pour convertir une adresse RAM vers offset payload: `offset = addr - 0x80010000`.
- Pour convertir vers offset dans le `PS-X EXE` complet: `exe_offset = 0x800 + offset`.

### Types 32-bit vs hôte 64-bit

Le code PS1 et plusieurs chemins `PSXPC_N` supposent des pointeurs/adresses 32-bit. Sur Linux x86_64, les types hôtes (`long`, pointeurs C) font 64 bits, ce qui peut casser les structures disque et les casts pointeur ↔ `int`.

Exemple récent RE-005: le runtime 64-bit progresse jusqu'à `LoadLevel()` mais reconstruit un pointeur de room invalide parce que des structures disque PSX 32-bit sont lues dans des champs hôtes.

Convention: lorsqu'une donnée vient du disque ou d'un overlay PSX, distinguer mentalement:

- représentation disque: champs 32-bit little-endian, offsets/adresses PSX;
- représentation runtime hôte: pointeurs C du processus Linux;
- conversion explicite nécessaire entre les deux.

### Bit-fields

`TIPS.md` rappelle que les bit-fields sont souvent affichés par les décompilateurs comme un champ agrégé, puis manipulés par masques `AND`/`OR`.

Exemple simplifié de `COLL_INFO`:

```c
unsigned short slopes_are_walls : 2; // offset=132.0
unsigned short slopes_are_pits : 1;  // offset=132.2
unsigned short lava_is_pit : 1;      // offset=132.3
unsigned short enable_baddie_push : 1; // offset=132.4
unsigned short enable_spaz : 1;        // offset=132.5
```

Interprétation des masques courants:

- `value &= 0xFFDF` efface le bit `0x20`, donc `enable_spaz = 0` pour ce layout.
- `value &= 0xFFEF` efface le bit `0x10`, donc `enable_baddie_push = 0`.
- `value |= 0x10` pose `enable_baddie_push = 1`.

Checklist bit-field:

1. Identifier le type conteneur (`unsigned short`, `unsigned long`, etc.).
2. Repérer l'offset byte.bit dans le header (`offset=132.4`, etc.).
3. Convertir le masque hex en bits.
4. Vérifier l'ordre little-endian attendu par le compilateur ciblé.
5. Comparer avec les headers `TYPES.H` / `STYPES.H` / `SPECTYPES.H` avant de renommer un accès.

## Checklist avant de modifier un statut de fonction

Avant d'ajouter `(F)`:

- [ ] L'adresse final du commentaire correspond à la fonction Ghidra attendue.
- [ ] La signature et les types ont été comparés aux appels et aux headers.
- [ ] Les branches, early returns et switchs ont été rapprochés du MIPS.
- [ ] Les accès mémoire/structs ne dépendent pas d'un type hôte 64-bit incorrect.
- [ ] Les bit-fields ont été vérifiés par masque, pas seulement par pseudocode.
- [ ] Le code compile encore.

Avant d'ajouter `(D)`:

- [ ] Tout ce qui est requis pour `(F)` est vrai.
- [ ] Le comportement a été testé ou raisonné contre le chemin original.
- [ ] Les cas d'erreur et chemins rares ont été couverts.
- [ ] S'il s'agit d'un chemin runtime `PSXPC_N`, le test/point de blocage est documenté.

Avant d'ajouter `(**)`:

- [ ] Ne pas le faire dans le niveau 1 sauf preuve externe.
- [ ] Une comparaison binaire/désassemblage reproductible existe.
- [ ] Les options de compilation, versions et overlays comparés sont documentés.
- [ ] La preuve est liée depuis le ticket ou le rapport de reverse.

Avant de retirer `(ND)`:

- [ ] La fonction a été réellement debugguée ou couverte par une preuve suffisante.
- [ ] Le ticket ou la doc indique pourquoi elle n'est plus considérée non-debugguée.

## Règles de versionnement

Ne pas committer les fichiers du jeu ni les extractions lourdes:

- pas de `TOMB5.BIN` / `TOMB5.CUE`;
- pas de `SLUS_013.11` extrait;
- pas de `GAMEWAD.OBJ` / `CODE.WAD`;
- pas de niveaux/assets extraits;
- pas de projet Ghidra généré sous `build/reverse/`.

Les fichiers acceptables dans git sont les scripts, docs, CSV/JSON/Markdown de synthèse et inventaires textuels qui ne contiennent pas d'assets copyrightés.
