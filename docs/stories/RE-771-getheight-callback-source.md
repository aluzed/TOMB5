# RE-771 — SOURCE GetHeight TRIGGER/callback → item.floor

Publication metadata-only du 13 septembre 2026, Europe/Paris. **PASS privé : caractérisation SOURCE uniquement ; pas d’équivalence cible.** La revue finale de publication PASS au 13 septembre 2026 à 10:40 Europe/Paris est distincte du PASS privé. Au snapshot avant revue, aucune mise en index ni commit de cette publication n’a été effectué par le publisher.

## Résultat et matrice réellement observés

Les TU entières non modifiées `SPEC_PSXPC_N/GETSTUFF.C` et `COLLIDE_S.C` montrent que les sorties callback ne sont pas propagées au retour de GetHeight : il reste **3072**, puis le vrai consommateur UpdateLaraRoom écrit **3072 dans item.floor** et retourne normalement. Les effets globaux persistent. Ce constat porte sur le source et les fixtures retenus, pas sur un défaut du binaire historique.

**24 cas = 12 directs + 12 UpdateLaraRoom alias** Lara/item : slot absent/présent × inhibition homogène par masque 32768 active/inactive × trois couples y/payload × deux modes. Deux items déclencheurs, indices 1 puis 2, partagent le slot de l’objet 0 et le même état de flags. Six lignes éligibles produisent **12 appels callback**, observés par **24 événements ordonnés** entrée/sortie. x=1131, z=1757, y=628/1701/4096 ; payload item1=777/-2222/70000 puis item2=878/-2121/70101. Les grandes sorties callback ne sont pas des retours rétrécis : elles restent locales et le retour est toujours 3072.

Signature exacte : `void(ITEM_INFO*,int,int,int,int*)`, affectée au slot sans cast et contrôlée par assertion de type compilée du reviewer. Le callback écrit sans lire l’ancienne valeur du local non initialisé : le passage de ce pointeur ne démontre donc pas une lecture indéfinie sur ces chemins. Il ne modifie aucun item. Le source ne copie pas cette sortie locale vers son accumulateur de retour.

Avant callback1, les quatre globaux sont zéro et trigger_index désigne le mot1. Après callback1 et à l’entrée callback2 : [101,201,301,401], mot14 ; après callback2 : [102,202,302,402], mot14. Ces globaux persistent après retour ; sans appel : [0,0,0,0], mot1. Les callbacks observent encore floor123456 avant l’écriture finale du consommateur.

## Buffers, compilation et limites d’observation

Chaque snapshot contient **432 octets**, soit **trois ITEM_INFO de 144 octets** chacun, taille ABI mesurée. Le reviewer délégué distinct a fait une reconstruction indépendante des buffers initiaux et finals complets depuis la sentinelle et les affectations connues, avec son propre programme de mesure ABI, sans import du producteur ni de son oracle. Seuls les quatre octets floor de l’item0 changent dans le mode Update. Les contrôles entrée/sortie callback comparent aussi les buffers items complets.

Les autres zones : memcmp du harness (rooms, cellules, floor-data, objects, Lara, queue ItemNewRooms) et vérifications de pointeurs/supports réellement exécutés ; pas de reconstruction indépendante de ces autres buffers, pas de surveillance mémoire générale. Limites : pas de sanitizer et pas de preuve générale d’absence d’UB. Géométrie positive : une salle, seize cellules, cellule5, hauteur12, plafond0, liens255, TRIGGER/actions terminants et indices valides ; pas de porte ni de traversée verticale. La conversion du masque vers short est celle du compilateur retenu. Couverture limitée : pas d’inhibition mixte, pas de callback jeu, pas de non-alias et pas de triangles dans cette unité ; pas de roomchange ni de données de jeu exécutées.

Compilation privée fraîche g++, C++17, **-m32 -O0**, mêmes macros/includes et ABI chez le reviewer. Compilation complète des deux TU, sans wrapper et sans symboles non résolus tolérés ; `--gc-sections` élimine les sections inutilisées au lien. Le vrai GetFloor puis GetHeight est appelé ; le désassemblage natif reviewer confirme l’extension signée du short et le store floor. Ce n’est pas de build du jeu entier. Les dépendances sont distinctes par TU ; les headers système sont hashés après compilation, pas présentés comme un snapshot antérieur. Les 287 sources/headers sont restés identiques selon les vérifications privées.

## RED privé, revue et attributions

Le contrat privé précédait le harness. Son **RED setup/contrat** était l’absence de native.log : exit1, **zéro test exécuté**, pas un RED comportemental. Première exécution native verte sur source inchangée ; **quatre méthodes** de test privées PASS chez le producteur puis chez le reviewer. Les neuf corruptions de copies en mémoire rejetées testent la sensibilité du contrat ; ce ne sont pas des contre-exemples source ni des sorties natives.

Le producteur a exécuté son audit distinct dans le même sous-agent. Le reviewer délégué distinct a recompilé dans sa propre racine, exécuté les quatre méthodes auteur et sa reconstruction indépendante ; stdout frais byte-identique à l’historique. Son incident de normalisation de chemins de dépendances (KeyError, exit1) a été conservé puis résolu dans son seul vérificateur (exit0), sans modifier les attentes, les sources ou les preuves auteur.

Références sous `build/reverse/autonomy-20260913/` : `getheight-callback/HANDOFF.md`, `getheight-callback-review/REVIEW.md`, `getheight-callback-review/verdict.json`, `getheight-callback-review/post-report.json`. Le verdict privé utilise **verdict/erreurs/remarques**, pas un booléen passed=true ; PASS SOURCE et erreurs vides ne signifient aucune validation de schéma booléen ni autorisation de patch.

Attribution : selon le contexte explicite de cette délégation, le parent a lu handoff/rapport/verdict/postrapport et vérifié trois hashes (rapport, verdict, manifest reviewer) à **10:28:51** le 13 septembre 2026 Europe/Paris, consignés dans `callback-parent-verification.json` : aucun replay privé ni audit buffers parent. Le publisher a relu ces éléments et comparé ces trois hashes, pas les buffers privés ; publisher : aucun rejeu privé. Le reviewer a vérifié 60 fichiers de preuve, 287 sources/headers et 1293 autres livraisons, dont le rapport technique uniquement hashé. Le publisher préserve volontairement ce rapport sans l’ouvrir ; cette préservation n’est pas attribuée à une interdiction utilisateur. Les anciennes preuves et gardes historiques inchangées ne sont ni rejouées ni rescellées ici.

## Vérification documentaire de publication

Tests documentaires écrits avant cette story et la section dashboard. **RED documentaire : deux échecs attendus**, story et section absentes, exit1 dans `re771-publication/red.log` et `red.json`. Ce RED documentaire est distinct du RED setup privé et ne prouve pas un défaut comportemental. Résultats observés après exécution : GREEN, 2 tests PASS en 0,06 s pytest, exit0 ; suite exacte RE770 + nouveau test, 3765 tests PASS en 59,28 s pytest, exit0. Les commandes, intervalles, logs et hashes avant/après sont dans green.log/green.json et suite.log/suite.json sous re771-publication. Le test est byte-identique entre RED et GREEN. Ces résultats sont inscrits avant la revalidation finale ciblée RE771/RE770/RE769 ; final-doc.json et final-doc.log en établiront le résultat réel, non présumé ici. La sélection complète est reprise littéralement du ledger RE770 `re770-publication/final-suite.json`, avec ce seul nouveau test ajouté et basetemp relocalisé. Après inscription des résultats, une revalidation documentaire ciblée suffit ; sa commande exacte, son exit et les hashes finaux seront archivés séparément, sans rejouer une seconde suite complète.

## Tracker

- [x] Après RE-770 : caractérisation SOURCE GetHeight TRIGGER/callback → item.floor terminée ; source de production inchangée.
- [x] PASS privé SOURCE uniquement, reconstruction reviewer et vérification parent attribuées séparément.
- [x] Overview actif / overview actif du 13 septembre 2026 placé dans la section RE-771 append-only ; tous les bytes HEAD du dashboard restaurables en retirant cette seule section.
- [x] Revue finale : revue finale de publication PASS au 13 septembre 2026 à 10:40 Europe/Paris, distincte du PASS privé.
- [ ] collision amont/cible GetHeight : la preuve authentique reste manquante ; code_change_readiness=blocked.

## Handoff

**Après RE-771 — handoff actif :** la vraie preuve collision amont/cible GetHeight reste manquante. La cible historique non exécutée dans cette unité ne peut être remplacée par le PASS SOURCE ; RE769 reste le stop à l’entrée GetHeight. Aucun résultat de hauteur cible complète, aucune équivalence cible et aucun gameplay ne sont établis ici. Source de production inchangée ; code_change_readiness=blocked. **Aucun nouveau sujet : aucun nouveau topic ouvert.** Ce handoff clôt la publication des résultats existants, sans démarrer de nouvelle preuve, ni patch, job, mise en index ou commit.
