# Inventaire assets disque / GAMEWAD / CODEWAD

Date: 2026-06-14
Story: `docs/stories/RE-006-assets-gamewad-codewad.md`
Status: inventaire disque et GAMEWAD validé; assets lourds non versionnés

## Commande reproductible

Depuis la racine du repo:

```bash
python3 scripts/reverse/assets_inventory.py
```

Le script écrit uniquement des inventaires texte/JSON versionnables:

- `docs/reverse/generated/disc-files.txt`
- `docs/reverse/generated/gamewad-files.txt`
- `docs/reverse/generated/assets-summary.json`

Les fichiers extraits lourds restent sous `build/reverse/re006/`, ignoré par git via `/build/reverse/*`.

## Résumé disque

Source runtime locale:

- `TOMB5.BIN` / `TOMB5.CUE`
- CUE: `TRACK 01 MODE2/2352`
- ISO de travail généré: `build/reverse/re006/tomb501.iso`

Inventaire ISO:

- fichiers disque listés: `30`
- taille totale listée: `567511833` octets
- exécutable boot: `SLUS_013.11` (`608256` octets)
- conteneur principal: `GAMEWAD.OBJ` (`55355392` octets)
- metadata runtime: `SYSTEM.CNF`, `SCRIPT.DAT`, `US.DAT`
- FMV: `8` fichiers `.STR` (`FMV0.STR` à `FMV7.STR`)
- audio XA: `17` fichiers `.XA` (`XA1.XA` à `XA17.XA`)

Détail complet: `docs/reverse/generated/disc-files.txt`.

## Résumé GAMEWAD.OBJ

`GAMEWAD.OBJ` a été extrait depuis l'ISO de travail, puis parsé avec le même format de header que `scripts/gamewad.py` / `SPEC_PSX/CD.H`:

- entrées attendues: `51`
- entrées non vides: `30`
- entrées réservées vides: `21`
- entrées niveau avec assets de chargement + `CODE.WAD` embarqué: `15`
- entrée setup partagée: `SETUP.MOD` (`42012` octets)
- storyboard extras: `3`
- écrans legal: `8`
- logos TR4: `2`

Détail complet: `docs/reverse/generated/gamewad-files.txt`.

## CODE.WAD

Il n'y a pas de fichier `CODE.WAD` autonome à la racine du disque. Le code du repo indique que les modules code sont embarqués dans chaque entrée de niveau de `GAMEWAD.OBJ`:

- `TOOLS/GAMEWAD_Unpack/GAMEWAD.CPP` calcule un segment `CODE.WAD` après l'image de chargement, l'icône CD, `SETUP.MOD`, les données niveau et un padding/offset.
- `TOOLS/CODEWAD_Unpack` / `TOOLS/CODEWAD_Pack` sont prévus pour décomposer/recomposer ce segment.
- L'inventaire détecte `15` entrées de niveau contenant un segment compatible `CODE.WAD`.
- Taille détectée pour chaque segment embarqué: `430108` octets.

Entrées niveau concernées:

- `TITLE.PSX`
- `ANDREA1.PSX`, `ANDREA2.PSX`, `ANDREA3.PSX`
- `JOBY2.PSX`, `JOBY3.PSX`, `JOBY4.PSX`, `JOBY5.PSX`
- `ANDY1.PSX`, `ANDY2.PSX`, `ANDY3.PSX`
- `RICH1.PSX`, `RICH2.PSX`, `RICHCUT2.PSX`, `RICH3.PSX`

## Chemins runtime attendus

### `DISC_VERSION=1`

Mode validé par RE-005 pour lire directement l'image disque:

- placer `TOMB5.BIN` et `TOMB5.CUE` à la racine d'exécution / racine repo selon le lancement;
- compiler avec `-DDISC_VERSION=ON` pour obtenir `DISC_VERSION=1`;
- le runtime cherche `\\GAMEWAD.OBJ;1` sur le disque via `SPEC_PSX/CD.H`.

Ce mode ne nécessite pas de committer les assets extraits.

### `DISC_VERSION=0`

Mode assets bruts décrit dans `CONTRIBUTING.md`:

- extraire `GAMEWAD.OBJ` avec `GAMEWAD_Unpack` ou `scripts/gamewad.py`;
- placer les fichiers extraits dans un dossier `DATA/` à côté du binaire `MAIN`;
- extraire les segments `CODE.WAD` embarqués si un workflow niveau/module brut en a besoin;
- garder `GAMEWAD.OBJ`, les `.PSX`, `.RAW`, `.JIZ`, `.XA`, `.STR`, `.WAD` hors git.

## Vérifications effectuées

- `bchunk TOMB5.BIN TOMB5.CUE build/reverse/re006/tomb5` génère l'ISO de travail.
- `7z l build/reverse/re006/tomb501.iso` liste les `30` fichiers disque.
- `7z x ... GAMEWAD.OBJ SYSTEM.CNF SCRIPT.DAT US.DAT` extrait les metadata de travail sous `build/reverse/re006/iso_extract/`.
- `python3 scripts/gamewad.py unpack ...` extrait `GAMEWAD.OBJ` en zone non versionnée.
- `python3 scripts/reverse/assets_inventory.py` régénère les inventaires versionnés.

## Sécurité copyright / git

Ne pas versionner les assets extraits ni l'ISO de travail. Les seuls livrables à committer pour RE-006 sont:

- documentation;
- scripts de génération;
- inventaires texte/JSON légers.
