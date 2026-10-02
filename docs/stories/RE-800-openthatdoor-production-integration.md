# RE-800 — OpenThatDoor : intégration production bornée

## Résultat livré
Après acceptation indépendante explicite du **patch exact**, OpenThatDoor est **intégré dans GAME/DOOR.C** sous gate effectif `PSX_VERSION && PSXPC_TEST && __i386__`. Include standard gated et remplacement de ce seul stub : aucune activation ObjectObjects, aucun changement des autres corps. Le parent a exécuté la régression publique sur la **TU complète réelle** après intégration : **3328/3328 normal et 3328/3328 ASan+UBSan**, sans diagnostic runtime. Vrais headers i386, link normal avec **gc-sections**; pas link complet du jeu.

Régression publique `tests/reverse/test_re800_openthatdoor.py` et fixture synthétique `tests/reverse/fixtures/re800/openthatdoor.cpp`, sans asset ou archive cible nécessaire. RED comportemental avant intégration préservé : build0/run1 et **2944 échecs / 3328** dans les deux modes. Revue indépendante : cinq **mutants du code** rejetés (copie floor, gate LiftDoor, reset LOT, priorité axe, signe); ShutThatDoor **144/144** dans les deux modes. Cela ne transforme pas les mutations de résultats RE-799 en mutants code.

## Attribution et limites honnêtes
La revue RE-800 a décodé fraîchement **131 words** du payload authentifié et reconstruit indépendamment les **3328 archives historiques**; **pas de rejeu cible frais** dans cette revue. Le rejeu cible RE-799 reste historique, avec contexte loader/GP hérité. Les sweeps publics font agir les quatre meshes, contrairement aux masques RE-799; même comportement source historique, pas identité des matrices.

Préconditions : buffers valides et **disjoints**, `d == &dd.d1`, floor null ou valide et sauvegarde disjointe; bloc sentinel 2047 ou index valide sélectionné 0/7/15, cinq creatures accessibles lorsque requis; troisième mesh obligatoire si premier actif, deuxième/quatrième optionnels et trois shorts accessibles; LiftDoor 0/1. ABI native packed DOORPOS14/DOOR82, projection depuis cible DOORPOS16/DOOR92. Seul premier sous-record exercé.

Égalité de l'état final des régions sélectionnées, **pas ordre de stores**, alias, write-set exhaustif ou mémoire globale : ordre mesh cible 1,3,2,4 contre natif 1,2,3,4; memcpy limité aux zones disjointes. Ni autres ABI/backends, matériel, startup, runtime ou gameplay prouvés. **pas de GREEN global**. Initializer générique seulement privé et borné, domaines élargis non fermés; DoorControl et ProcessClosedDoors bloqués; registration non activée et callback bridge naturel bloqué.

## Tracker
- [x] Régression publique actual-TU avant patch; RED comportemental conservé.
- [x] Acceptation indépendante du patch exact, mutants code et ShutThatDoor discriminants.
- [x] Production OpenThatDoor intégrée sous gate borné; GREEN public réel du parent.
- [x] Publication metadata-only sous régression écrite d'abord; historique dashboard préservé octet pour octet hors ajout nommé.
- [ ] Initializer élargi et intégré, DoorControl et ProcessClosedDoors prouvés.
- [ ] Registration cohérente puis callback naturel, fullbuild et gameplay.

## Preuves publiques sûres
Verdict privé `build/reverse/autonomy-20261002/re800-integration-review/verdict.json`, SHA256 **e094a56b62539a224d18642850248900aaace1fd404644b909ac9237d48c45a9**. Source exacte acceptée/intégrée au checkpoint SHA256 **a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff**; digest historique, pas gel permanent de la TU mutable. Métadonnées `docs/reverse/generated/re800-openthatdoor-integration.json`. Archives RED, revue et traces restent privées; aucune adresse, bytes bruts, dump ou asset publié. L'acceptation technique du patch n'est pas une revue automatique de cette publication ultérieure.

## RE-801 — Plus petite preuve réelle suivante / Critères de reprise
**DoorControl**, planifié seulement, pas déjà prouvé : sélectionner **une branche réellement atteignable** sur un objet synthétique valide. Authentifier l'entrée/retour cible et les dépendances effectivement appelées; fixer un état initial et l'oracle minimal distinguant le stub (état sélectionné et trace d'appels). Écrire d'abord le test privé **actual-TU**, capturer un **RED comportemental**, puis seulement un candidat privé de cette tranche. Une dépendance absente devient un blocker précis, jamais un retour simulé vendu comme équivalence. Exiger GREEN normal/ASan+UBSan et revue indépendante de portée avant tout nouveau patch. Ne pas répéter les anciennes matrices Open/Shut/initializer pour prétendre avancer DoorControl; ne pas activer registration. Si attribution/branche non fermée, conserver RED et limites, sans élargissement implicite.

Autorisation renouvelée transmise par le parent : échéance absolue **2026-10-03 03:00 +02**, recherche **02:20**, revue **02:40**, clôture owner **02:50**; cutoff de ce worker **00:10**. Les stories RE-798/799 et leurs échéances historiques restent inchangées. Ce handoff ne prolonge ni n'élargit l'autorisation; aucune exécution runtime nouvelle.
