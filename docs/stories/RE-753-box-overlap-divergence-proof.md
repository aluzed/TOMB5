# RE-753 — Boxes / overlap : preuve de divergence bornée

Publication metadata-only de la preuve privée terminée ; aucune extension ni correction de production.

## Tracker

- [x] Revue qualifiée lue ; vérification parent antérieure à toute modification suivie.
- [x] Date avant unité : 9 septembre 2026, 11:26:45 Europe/Paris, avant 23:25.
- [x] RED documentaire observé : story absente, 1 échec attendu en 0,06 s.
- [x] Résultat de non-équivalence, bornes et attribution publiés sans données brutes.
- [x] GREEN documentaire : 1 test en 0,05 s ; suite publique RE752 étendue RE753 : 1 207 tests réussis en 50,31 s, exit 0.
- [ ] Preuve corrective test-first sur vraie TU, revue et patch éventuel : non exécutés ici.

## Résultat et cause

PASS de caractérisation bornée ; NON-ÉQUIVALENCE cible / vraie TU : un octet différent, conservé et expliqué, pas une égalité des buffers. 116 salles ; buffer de 524 000 octets reconstruit intégralement et séparément pour chaque comportement, avec 4 774 mots de pointeur normalisés ; frames de 329 832 octets identiques. Cible : boxes[0..628] ; vraie GAME/SETUP.C compilée : boxes[629..1]. La source écrit overlap[3], hors du bloc logique boxes mais à l’intérieur de l’allocation salle. boxes[0] omis est sans effet sur ce corpus car son champ est nul. Le CFG et les buffers établissent les domaines ; les indices des stores hôtes sont déduits du code compilé et de la reconstruction intégrale, pas une trace instrumentée distincte de tous les stores. Le reviewer a décodé indépendamment la tranche cible authentifiée et vérifié qu’aucune relocation ne la touche, puis recoupé le code natif avec son segment ELF. Le delay slot de boucle cible avance le pointeur. Aucun consommateur overlap/pathfinding exécuté : aucun impact gameplay démontré, ni crash ni dépassement d’allocation démontré. Aucun masque ne supprime l’écart ; aucun correctif de production dans cette publication.

## Comparaisons et compteurs

23 champs pointeurs et 9 scalaires suffixe comparés par le runner ; 23 symboles supplémentaires résolus dans le harness, outre les onze précédents, pas 32 symboles distincts. Le reviewer vérifie séparément les 15 événements intercalés : 7 lectures, 5 allocations, 3 libérations, leurs tailles, sept buffers entiers et curseurs sectoriels. Triplets normalisés avant/après allocations/libérations et état final égaux, mais pas aux retours de lecture hôtes, non capturés. Textures, table audio et données SPU vérifiées par le runner, pas par cette reconstruction indépendante du reviewer. 1 608 071 visites du hook, 52 246 visites overlay, 5 147 visites du suffixe, 64 interceptions et une visite d’arrêt : pas des instructions retirées. Les octets authentifiés à chaque visite ne sont pas un compte d’instructions exécutées. Même CPU/RAM/curseur depuis S_LoadLevelFile ; aucune reprise opportuniste au module.

## Borne native, cible et lien

Vraie GAME/SETUP.C et harness séparé sans copie de LoadLevel, i386 -m32 -O0 -g, en-têtes ordinaires ; PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DEBUG_VERSION=0, DISC_VERSION=1. Arrêt matériel GDB à SETUP.C:1274, audit CFG avant de continuer ; 34 symboles non nuls distincts. 282 instructions statiques et 10 branches : décodage complet, sans appel/retour ni branche indirecte ; destinations directes sur frontières internes ou sortie protégée. Le reviewer vérifie aussi les octets dans le nouvel ELF. Le contrôle des opérandes mémoire absolus nuls ne couvre pas tous les nuls calculés ni tous les accès invalides. Arrêt matériel SETUP.C:1429, capture puis destruction de l’inférieur ; marqueurs RE753_PREEXEC_NATIVE_AUDIT_PASS et RE753_CAPTURE_COMPLETE observés. Cible : appel de lecture objets et delay slot atteints, number_cameras stocké ; arrêt à l’entrée de DEL_CDFS_Read avant son corps et avant toute huitième lecture. Ce n’est pas le retour de cette lecture ; aucun retour LoadLevel prouvé. Le compteur cible est réaffecté après boxes. Le lien conserve --unresolved-symbols=ignore-all : ne jamais exécuter ce binaire autonome ni dépasser la borne ; les dépendances suivantes ne sont pas validées par le succès du lien.

## Revue et vérification parent

Revue indépendante fraîche le 9 septembre 2026 : runner exit 0 de 11:20:57 à 11:21:16 Paris, 5 tests producteurs/gardes puis 1 test d’audit après les producteurs ; review_check.py indépendant exit 0 à 11:23:29. Il reconstruit depuis l’en-tête et le buffer lu sans importer les modèles du worker ni leurs listes de normalisation. Le snapshot reviewer conserve 285 fichiers ; après rejeu seuls PID, durées et horodatages de quatre logs/métadonnées varient, buffers et exécutable byte-identiques malgré une recompilation fraîche réelle. Vérification parent distincte avant publication de 11:25:56 à 11:26:16 Paris : run_verified.py puis review_check.py, chacun exit 0. Parent : 5 tests en 18,637 s puis 1 test en 0,116 s, soit six méthodes unittest ; deux exécutions cible et une recompilation/exécution de la vraie TU, pas six compilations. Les 11 sous-processus directs ne sont pas 11 tests. Audit CLI supplémentaire après les producteurs ; review_check.py n’est pas un septième test unittest. Python optimisé rejeté, exit 1 attendu. La mention parent non effectué dans review.md décrit la revue antérieure, pas les vérifications parent ultérieures. Lire les logs ici n’est pas un nouveau rejeu.

## Provenance et exclusions

HEAD prépublication 1676c4d75d92ec8e11081f00545443cf7dcde0e8 ; autorisation du 9 septembre 2026 jusqu’à 23:25 Paris. 341 dépendances authentifiées et 11 fichiers de code sauvegardés/vérifiés avant et après runner ; fermeture par TU séparée, 53 setup et 27 harness, chemins canonicalisés. Les en-têtes système, outils et bibliothèques ne sont pas épinglés hermétiquement : environnement non hermétique. Deux warnings extern-initialized existants, compilation/GDB exit 0, stderr GDB vide. Gardes HEAD/arbre suivi/index propres, temps et assertions conservées ; gardes historiques inchangées. Après publication, ne pas rejouer ou resealer : nouvelle unité explicitement autorisée avec provenance propre nécessaire. Corpus unique Name=0, état synthétique, doubles allocation/CD/SDK hôtes ; helpers cible authentiques jusqu’aux frontières matérielles doublées. Même émulation CPU chez worker et reviewer, pas d’oracle matériel indépendant. Pas de boot complet/navigation/UI, matériel, concurrence, comparaison ROOMLOAD.C, GTE, objets/skins, consommateur pathfinding ; pas de sanitizer. Pas de validation générale des comptes signés/extrêmes, charges malformées, offsets mesh négatifs/impairs, autres ABI/optimisations. Les 1 155 fixups hors allocation restent inactifs ; des débuts de pointeurs dans les blocs ne prouvent ni que les objets complets y tiennent ni leur sûreté de déréférencement : pas de sûreté mémoire générale. Le décodeur indépendant est spécialisé à cette entrée positive, pas un parseur universel.

## Traces et commandes privées historiques

Preuves sous `build/reverse/autonomy-20260909/re753/` : `handoff.md` qualifié par `review.md`, `parent-replay.log`, `parent-check.log`, `green.log`, `audit-green.log`, `execution-commands.json`, `host-command.json`, `host-build-exit.json`, `debug-command.json`, `debug-exit.json`, `review-execution.json`, `review-check.json`. Les temps et exits parent sont ceux de l’exécution communiquée par le parent et des logs lus. Le rédacteur ne relance aucun probe privé. Invocations réellement exécutées par le parent, archivées ici pour attribution, pas à relancer après publication :

```sh
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260909/re753/run_verified.py > build/reverse/autonomy-20260909/re753/parent-replay.log 2>&1
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260909/re753/review_check.py > build/reverse/autonomy-20260909/re753/parent-check.log 2>&1
```

## Validation publique

Test uniquement documentaire ; il ne prouve pas l’exécution privée. Journaux RE753 : `publication-red.log`, `publication-green.log`, `publication-suite.log` ; commandes exactes, cwd et exits dans `publication-commands.json`. Suite publique exacte RE752 avec ajout du nouveau test (sans générateur historique relancé volontairement) :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/reverse/test_re753_boxes_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py -q
```

## Handoff

**Après RE-753 : preuve corrective bornée proposée, avant tout patch suivi.** Nouvelle unité explicitement autorisée et provenance propre, sans modifier les gardes ou artefacts RE753. Écrire d’abord un test différentiel RED sur la vraie TU, égalité intégrale attendue sur le corpus authentique, échec localisé à overlap[3]. Ajouter des fixtures étiquetées synthétiques : 0, 1 et plusieurs boxes ; premier et dernier élément avec/sans BOX_LAST, sentinelle overlap sensible ; vérifier traitement de boxes[0] et absence d’accès à boxes[n]. Essayer une correction uniquement dans une copie privée de la vraie TU, recompiler et auditer le CFG avant exécution sous le même stop. Vérifier l’état vivant du compteur de boucle sans assouplir arbitrairement la capture, disparition du seul écart et absence de nouvelles différences sur buffers, frames, pointeurs, scalaires et événements. Revue avant proposition de patch minimal attribué au backend prouvé. Ne pas étendre la lecture objets ou prétendre un effet gameplay.

Historique et générateurs figés, production inchangée ; aucun commit/push au moment de la rédaction initiale, aucun nouveau job. Suite publique réexécutée ensuite par le parent : 1 207 tests réussis en 50,84 s, exit 0 (`parent-publication-suite.log`). Rapport exclu ni ouvert ni modifié. Aucune adresse, opcode, dump source ou donnée brute publiée.
