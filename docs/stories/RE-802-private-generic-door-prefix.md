# RE-802 — Préfixe générique non-lift DoorControl privé

## Verdict et frontière
**PASS technique privé strictement borné**, pas approbation de publication ou d'intégration. Revue indépendante fraîche cible/native, pas seulement archivale. DoorControl et AnimateItem production restent **stub**; ProcessClosedDoors non implémenté, registration inactive, callback naturel bloqué : **pas de GREEN global**. Aucun runtime, fullbuild, full-game-link ou gameplay dans cette publication.

Le chemin generic/non-lift exécute le vrai TriggerActive cible et le vrai corps CONTROL.C natif renommé, avec wrapper d'observation entrée/résultat. Arrêt cible **avant la première instruction de AnimateItem**; natif AnimateItem observe l'entrée puis lève une exception sans retour, non un retour simulé. Aucun corps AnimateItem ni retour cible DoorControl prouvé. Ordre vérifié : TriggerActive entrée → résultat → AnimateItem entrée.

## Exécution et discrimination
40 cas indépendants synthétiques, 20 actifs / 20 inactifs, 12 changements timer, 2408 visites de hooks (pas instructions retirées), 120 événements ordonnés. CPU/RAM neuves par cas; instructions et arrêt/ABI authentifiés. Quatre builds ELF32 i386 frais, baseline et candidat chacun normal et strict ASan+UBSan fail-fast : baseline build 0/run 1, 40 divergences événements et 26 état, zéro input erroné; candidat build 0/run 0, 40/40 GREEN par mode, stderr d'exécution vide. detect_leaks désactivé.

Cinq **mutants du code** recompilés/rejoués en normal seulement, tous build 0/run 1. Couples état/événements : status 20/0, goal 20/0, polarity 40/0, no-trigger 26/40, no-animate 0/40. goal touche aussi un autre site non atteint; pas mutant mono-site global. La revue fraîche compte 360 cas natifs avec les mutants.

Reconstruction indépendante de dix régions : 2293 octets cible / 2283 natifs par cas. Projection retire dix octets padding DOOR_DATA et reloge seulement champs pointeurs déclarés. Comparaison RAM cible finale complète sauf 32 octets pile appelant; buffers natifs projetés complets et événements ordonnés. Probe ABI compilé/exécuté séparément sous headers actuels; pointeurs i386, layouts packed vérifiés. 1896 hashes originaux tous vérifiés; 42 stdout/stderr des 21 ledgers préservés.

## Incidents conservés
Producteur timeout après preuves, aucun succès implicite. HANDOFF producteur 00:59 obsolète reste immuable; ledgers GREEN ultérieurs et revue fraîche font foi. Premier span cible omet delay slot, premier link définition multiple items, projection native initialement erronée et diagnostic : setup/checker RED séparés du RED comportemental. Scripts pré-correction non conservés comme versions distinctes, pas reproduction prétendue des échecs initiaux. Audit same-author non utilisé comme revue indépendante.

## Limites
- Domaine construit borné et états corrélés, pas domaine universel ni callers réels ou gameplay; pas séquences multi-frame.
- Arrêt AVANT première instruction AnimateItem; aucun retour cible DoorControl prouvé, autres branches exclues.
- AnimateItem natif observe entrée puis exception sans retour; corps production stub, pas service réel AnimateItem.
- RAM cible finale complète sauf pile appelant; pas trace exhaustive des écritures transitoires.
- Unicorn logiciel, aucune validation hardware indépendante.
- Projection retire uniquement padding cible et reloge champs pointeurs déclarés; pas identité des layouts.
- Adresses allocations enregistrées par harness frais, pas mesure indépendante par debugger.
- i386 -O0 et defines archivés seulement; pas LP64, autres plateformes ou NDEBUG.
- Assertions de domaine candidat privé, pas politique de sécurité production.
- Mutants du code normaux seulement; mutant goal touche aussi un site non atteint, pas mono-site global.
- ASan+UBSan fail-fast baseline/candidat, detect_leaks désactivé; pas preuve leaks.
- Pas intégration, activation registration, callback naturel, fullbuild, runtime ou GREEN global.

## Métadonnées et authentification
`docs/reverse/generated/re802-private-door-prefix.json` publie uniquement comptes, symboles, hashes et readiness; preuves/source candidat/harness restent privées ignorées.
- Candidat SHA256 : `bf1ed5dc4c15f1d02d72c7a98b639d3ad40079937cfa68c8030dfec43fe2d0a1`.
- Verdict indépendant SHA256 : `d975a3b7049dce5eaa94a7a1391e6960d76546a086398bcd094dab372b6657db`.
- Baseline production enregistrée : `a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff`.

## RE-803 — prochain minimum réel, planifié/non prouvé
Prouver le minimum de corps/prérequis **AnimateItem réel**, authentifier entrée/retour cible et dépendances réellement exercées, puis actual-TU RED comportemental avant candidat privé, GREEN borné et revue indépendante. Dépendance absente = BLOCKED-004, pas retour simulé. Ne pas répéter matrices du préfixe fermé; aucune intégration ou registration implicitement autorisée. Initializer RE-798 élargi, autres branches DoorControl et ProcessClosedDoors restent distincts.
Autorité parent existante : échéance 03:00 Paris le 3 octobre 2026; recherche coupée 02:20, revue 02:40, owner 02:50. Commandes enfants au plus 900 s et bornées au temps restant; publication présente au plus 550 s. Aucun renouvellement implicite.

## Tracker
- [x] Préfixe non-lift privé, TriggerActive réel et arrêt avant AnimateItem authentifiés.
- [x] Baseline RED comportemental puis candidat GREEN normal/strict; cinq code mutants sensibles.
- [x] Revue indépendante fraîche et conservation des échecs/historique.
- [ ] RE-803 AnimateItem minimum réel, DoorControl complet et ProcessClosedDoors.
- [ ] Intégration acceptée séparément, initializer élargi, registration cohérente et callback naturel.
- [ ] Fullbuild, runtime et gameplay global.
