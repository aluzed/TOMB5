# RE-786 — GetCeiling : sélection de la famille roof triangle

30 septembre 2026. Baseline `fd74fbb9`. Correction minimale sous **PSX_VERSION && PSXPC_TEST** : sélectionner la seconde diagonale pour le **type 10**. La cible compare le sous-intervalle 15..16 sans signe ; la condition source signée acceptait aussi 10 après soustraction. Branche legacy préservée, aucun marqueur d'équivalence promu.

## Tracker
- [x] Extraction/authentication neuves depuis le disque, exécution cible bornée avec helper réel et delay slot de retour.
- [x] **1536** appels directs synthétiques, six types et tous les offsets de cinq bits.
- [x] RED actual-TU normal et **UBSan** strict avant correction : **256** divergences type 10 par matrice, invariance des cellules/data/globals.
- [x] GREEN actual-TU après correction ; 18 tests ciblés avec RE784/785 PASS.
- [x] RED documentaire avant inscription, préservation historique sous test.
- [x] Revue source indépendante PASS borné, replay1536 et recompilations fraîches.
- [x] Revue finale de publication PASS borné (`review-roof-seal/verdict.json`) ; livraison à vérifier séparément.
- [ ] Gameplay, traversées et consommateurs des offsets négatifs non validés.

## Contrat et preuves
Le probe neuf de `build/reverse/autonomy-20260930-15h/roof-target01/` couvre types 9, 10, 15, 16, 17, 18 × 32 valeurs du champ offset × huit coordonnées asymétriques. Les deux champs offset ont volontairement la même valeur ; la sélection de l'un versus l'autre n'est donc pas discriminée. Corners synthétiques asymétriques, cellules sans sky/pit, records terminaux. Coordonnées de chaque côté des diagonales et témoins à égalité ; comparaison stricte conservée. Retours cible de ces 1536 cas identiques à la formule séparée du test public. Le helper arithmétique cible est exécuté réellement, y compris l'ajustement de retour dans le delay slot ; aucune fonction native substituée à ce helper.

Le probe authentifie chaque instruction visitée, restaure CPU/RAM par cas, vérifie SP/RA et les buffers cellule/data sélectionnés. Le hook lecture est installé mais ne couvre que les lectures commençant dans le petit buffer déclaré ; aucune RAM complète, sûreté globale ou validation matérielle n'est établie. Un premier lancement a échoué avant tout probe : dépendance Unicorn absente ; venv privé neuf créé avec versions fixées puis commande réussie, aucun ancien job relancé.

La fixture publique compile GETSTUFF entière et headers normaux avec g++ i386/C++17, lien normal et sections inutilisées éliminées. Baseline byte-exact extraite de Git, pas de copie réécrite de la fonction. Les quatre tests recompilent séparément current/baseline et normal/UBSan ; la baseline attend ses 256 écarts sensibles, les autres familles servent de contrôles. Return short promu, cellule complète, data complet et cinq globals contrôlés. RED `roof-red.ledger.json` : deux échecs current attendus et deux contrôles baseline PASS, compilation/liens réussis ; GREEN `roof-green.ledger.json` : 18 PASS, exit0 avec régressions RE784/785. Ce nombre de tests n'est pas le nombre d'appels.

## Validation documentaire et régressions
RED documentaire : deux absences attendues. Après append, quatre tests documentaires PASS et deux guards historiques RED ; leurs digests sont conservés, seul successor RE786 nommé exclu et protégé par son propre guard byte-exact. GREEN documentaire six tests PASS. Première sélection étendue : deux tests RE779 FAIL parce que le nouveau titre était h2 ; seul le nouveau titre est passé à h3, aucun test RE779 affaibli. Même sélection reconstruite depuis le ledger précédent, augmentée de RE785 et RE786 : **109 tests PASS**, exit0 (`roof-suite-green02.ledger.json`), pas suite globale. Échecs initiaux préservés.

## Revue source indépendante
Reviewer CLI distinct, exit0 : `review-roof-source/verdict.json` PASS borné et listes bloquantes vides. Interpréteur MIPS entier indépendant du probe auteur et d'Unicorn, extraction fraîche du boot authentifiée, replay1536 avec parité des résultats/traces/lectures ; piles et registres sauvegardés restaurés, stores interprétés confinés au frame construit. Vérification explicite des branches strictes et du delay slot. Le reviewer a recompilé quatre matrices natives current/baseline × normal/UBSan et repris 18 tests publics ciblés frais. Il qualifie son modèle non cycle-accurate, aucune validation matérielle. Le coordinateur a lu ces artifacts et vérifié leurs 53 digests ; aucune exécution du replay reviewer ne lui est attribuée. Publication finale PASS borné (`review-roof-seal/verdict.json`), livraison à vérifier séparément.

## Offsets et limites
Les **offsets négatifs** sont couverts du point de vue du retour short final : le décodage unsigned-short actuel peut ajouter un multiple de 65536 à l'accumulateur, puis le retour court masque ce surplus. Ce résultat ne prouve pas l'accumulateur int transmis à un éventuel callback. **callbacks exclus** de cette cohorte ; aucun patch offset spéculatif effectué et aucune assertion de sanitizer global ajoutée. La correction porte seulement sur la sélection type 10.

**pas de runtime** jeu, pas de fullbuild/relink, aucune capture nouvelle. **pas de GREEN global**, pas de corpus/collision/gameplay, pas de tous couples offset ni toutes architectures/modes char. Pas de raw opcode/dump/pseudocode/asset versionné. Suppressions blocked utilisateur et rapport interdit préservés, aucun ancien ticket recréé.

## Handoff
Prochaine preuve utile : rendre distincts les deux champs offset et mesurer l'accumulateur transmis au consommateur callback réel pour offsets négatifs, avant une éventuelle correction cohérente. Obstacles restants documentés ici : manque de preuve du consommateur et de l'effet observable de son entrée int. Critères handoff : appels cible authentifiés continus, actual-TU RED sensible sur entrée/retour callback et contrôles positifs/négatifs, puis replay indépendant. Autorisation courante jusqu'à 15h Europe/Paris ; aucun nouveau secteur après14:35, clôture dès14:40. Revue/livraison de cette unité avant nouvelle correction.
