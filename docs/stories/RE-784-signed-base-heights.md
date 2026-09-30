# RE-784 — Décodage signé des hauteurs de base

30 septembre 2026, Europe/Paris. Baseline `73f994f0`. Correction source bornée des conversions de base **GetHeight** et **GetCeiling**, sous `PSX_VERSION && PSXPC_TEST` ; calcul par multiplication définie plutôt que décalage gauche d'un négatif. Le test de sentinelle relit l'accumulateur déjà calculé. Branche legacy conservée ; aucune modification globale du mode char ni des marqueurs d'équivalence.

## Tracker
- [x] Nouveau probe cible authentifié depuis l'exécutable du disque, sans réexécuter les anciens jobs/probes.
- [x] Deux RED actual-TU stricts UBSan, compilation et liaison réussies, avant correction.
- [x] Même fixture : GREEN sol/plafond sur tous les octets, modes char signé/non signé et normal/UBSan.
- [x] Régressions actual-TU RE-780/781/782/783 et ancienne correction GetFloor conservées.
- [x] RED documentaire avant story/dashboard ; historique dashboard byte-exact conservé.
- [x] Revue source indépendante PASS borné : 16 recompilations, dix tests frais et interpréteur MIPS indépendant 512 cas ; rapport écrit avant timeout CLI 124, verdict JSON final non produit par ce premier processus.
- [x] Revue finale indépendante PASS borné (`review-seal/verdict.json`) ; livraison à vérifier séparément, aucun PASS global anticipé.
- [ ] Parcours réels, triangles, callbacks et gameplay non validés par cette unité.

## Preuve et correction
Le nouveau probe privé exécute **512 appels directs**, soit **256 valeurs** de chaque champ : domaine signé complet de -128 à 127. Cellules terminales sans pit/sky et **index nul**. Les instructions exécutées sont authentifiées, CPU/RAM reconstruits par appel, retour et pile vérifiés, record cellule inchangé. Les deux chargements sont signés avant multiplication par 256. Ce modèle logiciel n'est pas un oracle matériel ; comparaison RAM complète indépendante non revendiquée.

La sentinelle -127 devient -32512. GetHeight remet ses quatre globals scalaires à zéro mais préserve trigger_index sur cette sentinelle ; sur les autres valeurs à index nul, trigger_index devient nul. GetCeiling ne modifie pas ces globals dans cette cohorte. La fixture actual-TU vérifie retour short promu, état et record entier ; elle ne prétend pas capturer le registre entier cible ni tous les buffers moteur.

Les RED du 11:49 sont deux exécutions natives strictes **UBSan**, chacune exit 1 sur le décalage gauche de -128, après compilation/lien normaux. Le RED pytest avant patch a **4 échecs et 6 réussites** : deux diagnostics stricts en mode signé, plus perte du comportement sentinelle GetHeight en mode unsigned-char (normal et UBSan). L'égalité des retours short ordinaires en unsigned-char ne masquait pas ce témoin d'état.

Après patch minimal, **15 tests PASS** à 11:52, exit 0 : les dix RE-784 et cinq régressions ciblées. Les huit matrices RE-784 courantes ont chacune 256 cas, sans diagnostic UBSan ; les deux tests baseline conservent l'échec strict attendu. Ce nombre de cas ne s'ajoute pas au nombre de tests pytest. Aucun flag global unsigned-char n'est proposé : d'autres plain-char dans le moteur ont des contrats distincts.

## Revue et validation courantes
La sélection exacte du dernier ledger public RE-783 (84 tests), augmentée seulement de GetFloor et des douze nouveaux tests RE-784, a **97 tests PASS** à 11:57, exit 0 (`suite-green.ledger.json`). Ce n'est pas la suite reverse globale. RED documentaire deux échecs attendus, puis GREEN documentaire deux réussites.

Le reviewer CLI distinct a recompilé 16 combinaisons current/baseline, repris dix tests publics et écrit `review-source/REPORT.md` : PASS source borné, aucune préoccupation bloquante. Son interpréteur séparé, sans import du probe auteur ni Unicorn, reconstruit les 512 chemins terminaux, valeurs et globals, puis compare les visites auteur ; 77 instructions distinctes. Il authentifie l'exécutable extrait par hash et identité byte-exact du payload. Le coordinateur lit ce rapport et vérifie résultats/digests ; aucune exécution supplémentaire du reviewer ne lui est attribuée. Le wrapper CLI atteint réellement timeout **124** après le rapport et avant verdict JSON : lacune de clôture conservée, pas transformée en exit0 ni en défaut comportemental. La revue finale de publication doit encore sceller le snapshot et son verdict machine.

## Portée, archives et handoff
Fixtures publiques : `tests/reverse/fixtures/re784/` ; tests `test_re784_signed_base_heights.py` et `test_re784_signed_height_publication.py`. La TU GETSTUFF entière est compilée avec headers normaux, g++ Linux/i386, C++17, sans suppression de symboles non résolus ; élimination des sections inutilisées au lien. **pas de runtime** jeu, pas de fullbuild/relink, aucun screenshot nouveau à livrer.

Preuves privées sous `build/reverse/autonomy-20260930-13h/` : extraction/probe neuf, traces et authentication ; ledgers `target-simple`, `floor-red`, `ceiling-red`, `pytest-red`, `pytest-green`, `doc-red`. Aucun asset/opcode/dump/pseudocode brut versionné. Les deux suppressions blocked utilisateur et le rapport technique protégé restent hors livraison.

Limites : index nul, cellules terminales et appels synthétiques seulement ; aucune validation des pentes/triangles, traversées, callbacks, corruption, extrêmes coordonnées ou toutes architectures/optimisations. La correction précédente GetFloor est testée sans rouvrir son ancien ticket supprimé. Dette historique de suites et FAIL fade non levés : **pas de GREEN global**. Prochaine preuve utile : consumer GetCeiling avec floor-data terminal et suffixe non pertinent rendu sensible, avant tout nouveau patch. Aucun ancien ticket blocked recréé.
