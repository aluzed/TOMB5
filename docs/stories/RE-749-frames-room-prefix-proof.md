# RE-749 — Frames et première reconstruction roomInfo

## Statut et progression

**Preuve différentielle bornée acquise ; aucun correctif de production.** Extension réelle de RE-748, pas une répétition du préfixe audio/textures. Publication metadata-only ; contrats historiques figés inchangés.

- [x] État distant vérifié ; RE-748 déjà publié, son handoff et sa revue consommés.
- [x] Nouvelle unité privée autorisée, provenance et garde propres ; historiques inchangés.
- [x] Tests privés RED sur API absente puis GREEN cible et vraie TU.
- [x] Continuité S_LoadLevelFile → dispatch → LoadLevel → allocations persistantes et première reconstruction.
- [x] Revue indépendante favorable, rejeux frais et comparaisons additionnelles.
- [x] Vérification parent à 08:15 Europe/Paris le 9 septembre : 2 tests cible et 1 test host réussis, compilation fraîche.
- [x] Publication test-first : RED observé sur story absente, puis GREEN ciblé et suite publique.
- [ ] Qualification des mots transformés et de leurs consommateurs.
- [ ] Reconstruction door/floor/light/mesh et progression aux salles suivantes.

## Résultat exécuté

Un cas normal Name=0 avec secteurs authentiques et état initial CPU/RAM/pile/tas synthétique. Une nouvelle instance est créée par rejeu indépendant ; dans chaque trajet, CPU/RAM/curseur sont conservés sans reset ni substitution entre appelant, dispatch et suffixe. Boot et module authentifiés, relocation réelle comparée sur toute l'image à l'interpréteur indépendant des 263 entrées. Les visites de code sont authentifiées contre boot ou overlay relocalisé ; aucune instruction cible patchée. Pas de nouvelle certification de l'ISO entier.

| Observation | Résultat |
|---|---|
| Allocations depuis LoadLevel | 5 allocations : trois temporaires et deux persistantes |
| Libérations par taille | 3 libérations, aucune persistante |
| Lectures | 7 buffers complets comparés aux secteurs ISO indépendants |
| Frames | 329 832 octets ; contenu final inchangé |
| roomInfo | 524 000 octets ; 116 salles, structure de 80 octets |
| Tas final | 853 832 octets utilisés, 231 608 disponibles |
| Progression | 680 secteurs depuis LoadLevel, dont 418 dans le nouveau suffixe |
| Première reconstruction | room[0].data puis ajout de sa base aux 24 mots suivants |

Le buffer roomInfo final entier correspond à l'entrée avec exactement 25 remplacements dans l'état final. Les descripteurs cible sont observés avant/après allocations, frees et lectures, avec invariants et retour au tas vide après les temporaires. Le différentiel host compare les **descripteurs complets normalisés** au début du tas, avant/après les cinq allocations et trois frees, et l'état final. Il ne compare pas les descripteurs aux retours des lectures ; ces descripteurs host proviennent du double allocateur, pas de la vraie TU MALLOC.C.

Les autres comparaisons couvrent les sept buffers entiers, frames finales, roomInfo final normalisé uniquement aux 25 mots transformés, positions relatives des allocations/data/prochain ptr, nombre de salles, contrôle/sélecteurs, ClutStartY, AnimFilePos/Len, curseur, textures/rectangles, séquences draw/SPU, table audio et bloc SPU complet. Aucun écart sur ces observations ; pas d'égalité absolue des pointeurs ni de tout l'état machine revendiquée.

## Transformation réelle, pas une validité de pointeurs

Les ordinaux **4, 16 et 24** des 24 mots donnent des valeurs **hors allocation** roomInfo, sur la cible et sur le host après normalisation. Aucun de ces résultats n'est déréférencé avant l'arrêt. Les autres valeurs dans l'allocation ne sont pas davantage certifiées pointeurs valides. Cela établit une transformation, **pas une validité de pointeurs**, un crash atteint ou une corruption générale. Qualifier le format et les consommateurs avant tout correctif.

La cible s'arrête **avant door**, après le dernier delay slot de la boucle des 24 ajouts et avant la reconstruction des champs door/floor/light/mesh. Le prochain pointeur a déjà avancé de la taille du premier bloc data. Les compteurs sont des visites de hook, interceptions et arrêt inclus, pas des instructions retirées par le CPU. Budget d'exécution borné ; aucune équivalence complète du chargeur.

## Vraie TU, ABI et frontière native

Compilation fraîche de **GAME/SETUP.C**, séparément du harness, avec ses en-têtes normaux, ABI **32 bits**, i386, debug O0, DISC_VERSION=1, DEBUG_VERSION=0, PSX_VERSION=1 et PSXPC_TEST=1. Assertions de taille pointeur/long, Level et room_info ; pas de copie de LoadLevel/LoadSoundEffects.

Les nouvelles globales atteintes sont définies dans le harness, dont frames, room, number_rooms et le curseur CD. Le host ne s'arrête plus par exception au troisième free : **breakpoint matériel** GDB avant door, avec première salle et boucle des 24 mots achevée, capture puis destruction de l'inférieur. Aucun retour normal LoadLevel revendiqué.

**Le lien conserve `--unresolved-symbols=ignore-all` pour la suite non atteinte.** Des écritures absolues nulles subsistent après la boucle des salles. Le scan des opérandes n'est pas une preuve générale de sûreté du lien. Ne jamais exécuter ce binaire sans le debugger et sa borne ; résoudre les dépendances avant extension. Deux warnings historiques extern-initialized et l'option locale -Wno-narrowing subsistent ; **pas de sanitizer**, ni de preuve générale d'absence d'UB.

## Limites

**Pas de preuve matérielle**, de boot complet ou de retour final du chargeur. Les services host allocation/CD/GPU/SPU sont des doubles, sans nouvelle comparaison des TU MALLOC.C/CD.C/ROOMLOAD.C. Le helper LoadSoundEffects est réel ; les services SDK SPU demeurent synthétiques. Pas de validation audio/GPU/DMA/MMIO, timing, interruptions, concurrence, erreurs ou autres niveaux. Les comparaisons intégrales concernent les buffers utiles, pas les octets adjacents ni tous les accès RAM.

## Revue indépendante et vérification

Revue indépendante le 9 septembre, contrôles terminés à 08:13 : **2 tests cible et 1 test host réussis**, nouveau CPU/RAM et nouvelle compilation i386 dans un répertoire de rejeu séparé. **29 fichiers identiques**, six comparaisons additionnelles exactes, 62 entrées du manifeste originales intactes et 11 dépendances épinglées vérifiées. Audit complémentaire du delay slot et de la borne native ; rejet de Python optimisé confirmé. Verdict favorable sans correction bloquante, uniquement pour cette portée.

Le parent a ensuite exécuté à 08:15, depuis la racine :

```sh
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260909/re749-frames/test_frames.py
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260909/re749-frames/test_host.py
```

Résultats parent : **2 tests en 8,069 s**, puis **1 test en 8,728 s**, tous réussis ; compilation fraîche et nouveau run cible. Les preuves et revue restent privées dans ce dossier ignoré. Les gardes sont épinglées au **HEAD prépublication**, aux dépendances et à la fermeture du 9 septembre à 23:25 Paris ; vérification à l'import/début du run, non continue dans le hook. Un futur rejeu exige une nouvelle unité autorisée avec provenance propre, **sans désactiver les anciennes gardes** ni modifier les probes historiques.

Test public : contrôle documentaire, pas preuve binaire. RED observé sur story absente ; **1 203 tests publics réussis en 50,83 s**, sans diagnostic. GREEN et régression publique exécutés avec :

```sh
python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

## Handoff

Qualifier les 24 mots et leurs consommateurs, puis étendre de manière bornée aux champs door/floor/light/mesh de la première salle et aux suivantes. Préserver CPU/RAM/curseur, authentifier les instructions et résoudre les dépendances natives nouvellement atteintes. Aucun patch spéculatif ni reconstruction globale déduit de cette preuve. Le dashboard actif est mis à jour ; les dashboards/gates terminaux historiques restent inchangés.
