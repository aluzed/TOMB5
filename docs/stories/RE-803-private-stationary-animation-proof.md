# RE-803 — Animation stationnaire privée bornée et composition de porte synthétique

## État courant
**PASS privé de fixtures seulement**, revue indépendante fraîche distincte. RE-802 reste un checkpoint historique de préfixe générique non-lift, arrêté avant AnimateItem : 40 cas, 2408 visites et 120 événements. RE-803 ne réécrit pas ces faits; il exécute réellement AnimateItem et le retour DoorControl sur un nouveau domaine synthétique restreint.

16 appels directs AnimateItem, 1716 visites cible: huit avances frame3→4, huit sauts animation0→1/frame8→2. Quatre compositions DoorControl→TriggerActive→AnimateItem, 642 visites, services réels et retour réel, sans saut. Baseline actual-TU RED16/16 et composition4/4, candidat privé GREEN16/16 et4/4 dans les modes normal, ASan, UBSan et ASan+UBSan. La revue refait 19 compilations et19 exécutions natives, plus cible directe et composition; 271 hashes originaux inchangés. Trois CODE mutants normaux frame/jump/touch donnent16/8/16 échecs comportementaux, pas erreurs sanitizer. Oracle indépendant des indices: buffers224 octets entièrement reconstruits.

**DoorControl et AnimateItem production restent stub**, ProcessClosedDoors absent. Aucun source lift/intégration, registration, fullbuild, runtime ou gameplay : **pas de GREEN global**. Revue technique privée n'autorise ni intégration ni publication owner automatiquement.

## Limites explicites
- Acceptation des 16 fixtures seulement, pas domaine stationnaire universel ni gameplay; deux positions initiales seulement, pas 16 branches sémantiques.
- Huit avances frame3→4 et huit sauts animation0→1/frame8→2; aucun self-loop sur la même animation, ni frontière frame7→8 sans saut.
- Composition synthétique seulement: quatre cas sans saut, deux branches TriggerActive et orientations différentes; pas tout DoorControl.
- DOOR cible92/natif82: normalisation exacte des champs synthétiques nuls, pas preuve de DOOR arbitraire.
- Buffers directs ITEM144 et deux ANIM40 entièrement comparés; composition pointeur item.data seulement relogé; pas identité de layouts.
- RAM cible finale comparée hors pile autorisée36/68 octets, pas trace exhaustive des écritures transitoires.
- Unicorn logiciel, aucun hardware ou jeu exécuté.
- i386 C++11 O0 et assertions actives, pas LP64, NDEBUG ni autres plateformes.
- ASan detect_leaks désactivé, avertissements de compilation DOOR; stderr des runs frais vide, pas preuve de fuites.
- Les harness archivés ne vérifient pas tous fread/fopen; tailles et hashes des fixtures valides vérifiés par revue.
- Aucun GetChange authentique exercé; commandes, son, effets, déplacement, gravité exclus.
- Loader, registration, ProcessClosedDoors, callback naturel, fullbuild, runtime et gameplay exclus; pas de GREEN global.
- Ordre historique RED avant candidat attesté seulement par archives; revue fraîche attribue ses nouveaux RED/GREEN aux sources exactes.

## Échecs et provenance conservés
- Premier oracle target-first erroné sur required_state conservé, archive seule non rejouée.
- Échec initial mutant-touch et mutants-setup-failed conservés, non rejoués; mutants corrigés CODE frais discriminants.
- Premier reviewer bloqué fournisseur après lectures: aucun verdict; reviewer final distinct PASS frais.
- Audit original non relancé pour préserver preuve; verdict provisoire non approuvé remplacé par verdict final après recompilations.

## Hashes publics sûrs
- Candidat privé AnimateItem SHA256: `d60ca859dc9e12bfef8f2e0c47ce05bbffd488fbfed19e646839a1d32488f896`.
- Verdict final distinct SHA256: `db511cd1da0a5a1272c709053b6d7747952b3ccf738e7d8b604f115e6d3124f4`.
- Baseline production SHA256: `5a24abe8b574054875a1fd2e4d66499400cbbfa427d2b0a1f7aa3956000b4158`.
Métadonnées: `docs/reverse/generated/re803-private-stationary-animation.json`. Comptes, symboles et hashes seulement; aucun binaire, dump cible, source extraite, opcode ou asset public.

## Prochaine frontière RE-804
Planifiée, non prouvée: **GetChange authentique**, nouvelle branche/prérequis réellement atteint; authentifier entrée/retour et dépendances, RED comportemental actual-TU avant candidat, GREEN borné puis revue indépendante. Ne pas répéter les fixtures closes ni simuler un retour. BLOCKED-004 reste ouvert.
Deadline parent 3 octobre 2026 **03:00 Paris**; recherche stop **02:20**, revue **02:40**, owner **02:50**. Aucun prolongement implicite.

## Tracker
- [x] RED publication observé avant story et métadonnées.
- [x] Corps AnimateItem et composition synthétique bornée privés, RED/GREEN et CODE mutants.
- [x] Revue indépendante fraîche PASS privé, échecs conservés.
- [ ] GetChange RE-804 authentique et domaine élargi.
- [ ] Intégration source, ProcessClosedDoors, registration et gameplay global.
