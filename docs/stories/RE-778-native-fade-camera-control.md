# RE-778 — Fondu natif, intro caméra et contrôle libéré

24 septembre 2026 (Europe/Paris). **Après RE-777**, les nouvelles archives du même ELF32 expliquent la capture noire et l'absence initiale de mouvement : **fondu natif transitoire puis intro caméra normale**, sans défaut persistant démontré sur ce parcours. Après la fin naturelle de l'intro, scène texturée et Lara visible, puis déplacement réel sous flèche Haut. **Aucun correctif source.**

## Tracker
- [x] RED documentaire réel : trois échecs avant création de la story, de la section et du jalon actif ; contrat append-only et metadata-only.
- [x] Lire les archives same-frame, temporelles et contrôle ; distinguer compteurs, essais diagnostiques et déroulement natif.
- [x] Attribuer le noir au split de fondu sur la frame run03 ; documenter sa disparition naturelle sur deux nouveaux lancements.
- [x] Documenter producteur et terminaison du verrou SpotCam, réception clavier et déplacement mémoire après libération.
- [x] source de production inchangée ; aucun asset public, aucun dump ou image versionné.
- [x] Tests publics de publication : 68 PASS ciblés (RE-773 à RE-778 et live index) ; suite reverse complète : 3347 PASS, 7 FAIL, mêmes identifiants d'échec connus du prédécesseur. Fichier généré RE-367 restauré octet pour octet après la suite.
- [x] Revue indépendante de publication PASS borné au snapshot du 24 septembre 2026 à 07:40 Europe/Paris ; tests du worker publication consignés séparément des preuves runtime.
- [ ] Collisions correctes, `GetHeight` en contexte, progression complète et équivalence cible non validée ; gameplay complet non validé.

## Trois preuves complémentaires, pas un correctif

### 1. Attribution sur une même frame
`build/reverse/autonomy-20260924-sameframe-recovery-0705/`, `run03/result.json`, `overlay-proof.json`, `analysis.json` et `reviewer/review.md` : le dernier split plein écran, six sommets en `BM_SUBTRACT`, RGB 239, masque la scène. Retirer ce seul split ou mettre à zéro ses seuls RGB produit exactement la même image texturée visible, avec 305596 pixels non noirs. Native, replay et replay final restent identiques octet par octet ; VRAM CPU/GPU et VBO contrôlés. Les interventions sont des contrôles diagnostiques privés, **pas le comportement natif sans intervention**, ni une autorisation de supprimer le fondu.

La revue indépendante donne **PASS borné à cette causalité et à la cohérence des archives**. Le HANDOFF racine same-frame est intermédiaire : la conclusion finale vient de run03 et du reviewer. Sa revue d'archives a exécuté 11 méthodes : 9 réussies, 2 échecs run01 conservés (observation GPU absente et erreur GL 1282). Aucun jeu relancé par ce reviewer. Pas de restauration transactionnelle complète GL/compteurs ni de reprise du jeu prouvée ; conservation caméra ne signifie pas pose correcte.

**988 visites de DrawAggregatedSplits, pas 988 frames de gameplay post-fade**, et non 998 : `level_draw_hits` est filtré sur le niveau sans origine au `SetScreenFadeIn`. Ce n'est pas un nombre d'appels GL attestant autant de frames noires. L'état 239, cible zéro, vitesse 16 concorde avec le premier pas du fondu, pas avec un blocage persistant.

### 2. Fondu natif observé dans le temps
`build/reverse/autonomy-20260924-fade-temporal-0714/`, HANDOFF, `verification.json` et sessions : deux lancements sans mutation ni replay de rendu, compteurs `DrawPhaseGame` initialisés au `SetScreenFadeIn`. Les 80 et 83 draws donnent respectivement 80 et 83 couples entrée/retour de Fade : 255 → 239 → … → 15 → 0, premier zéro **frame 16** dans les deux cas. La frame initiale est noire ; à zéro et au draw 40, le couloir texturé est visible. Lara n'est pas encore visible dans ces captures.

La touche Haut est reçue par SDL dans run02, mais l'input jeu reste nul et Lara immobile : `bDisableLaraControl=1` masque alors l'entrée. Le fichier `tests-green.log` contient réellement **1 PASS, 1 FAIL** : le test exigeant un input jeu non nul reste en échec, sans affaiblissement. Le vérificateur d'archives auteur distingue correctement temporalité et entrée ; son exit zéro ne transforme pas cet échec en succès gameplay. Le mouvement de caméra précédant la touche ne lui est pas attribué.

### 3. Fin naturelle de l'intro et mouvement Lara
`build/reverse/autonomy-20260924-control-release-0722/`, HANDOFF, `run01/events.jsonl`, `result.json`, `session.json` : un lancement supplémentaire, 378 draws contigus. Le watchpoint attribue l'activation du verrou à `InitialiseSpotCam(Sequence=10)` et sa levée à `CalculateSpotCams`, après le draw 299, avant la **frame 300**. `bUseSpotCam` revient également à zéro : terminaison normale de l'intro, pas un breakout, un verrou du menu titre ni une désactivation forcée.

Aucune flèche avant la capture libérée ; ensuite input jeu égal à 1 sur 76 draws (302–377), puis zéro après relâchement au draw 378. Position native Lara : (46592, 0, 31232) → (46592, 0, 34682), **Δz=3450** unités moteur. Déplacement établi par mémoire, pas déduit du seul cadrage. Les images privées `released.png` et `after-arrow.png`, inspectées par le worker runtime, montrent la scène et **Lara visible** de dos dans la ruelle puis plus loin sous l'arche. Le fichier nommé `frame300.png` correspond en réalité au draw 301 ; `released.png` au draw 300.

`tests-strengthened.log` et `tests-strengthened-invocation.json` attestent **3 tests PASS** exécutés par le worker contrôle (après deux tests initiaux PASS). `verify-final-invocation.json` atteste son vérificateur auteur exit zéro, **pas une revue indépendante**. Le worker publication n'a pas rejoué ces tests runtime ; leurs exécutions auteur et reviewer sont distinctes des tests documentaires. La revue indépendante temporelle/contrôle donne PASS borné aux archives : 4 PASS et 1 FAIL temporel conservé sur 5 méthodes, sans nouveau runtime ni validation de collision/gameplay.

## Limites et provenance
Les lancements temporels et contrôle ont un wrapper GDB exit zéro, avec arrêt volontaire par le debugger : **pas une sortie naturelle du jeu**. Les captures natives temporelles/contrôle sont des présentations X11 après swap ; leurs RGB ne sont pas des dumps GPU/VRAM. Les tests de publication sont uniquement documentaires, sans lancement de jeu ni replay privé. Leurs commandes, dates et sorties sont archivées dans `build/reverse/autonomy-20260924-publication-0729/` ; la suite ciblée du prédécesseur couvre RE-773 à RE-777, complétée par RE-778 et les tests du live index. La suite reverse globale du prédécesseur avait sept échecs connus ; aucun succès global nouveau n'est présumé.

La capture noire transitoire relève du fondu normal et les contrôles initialement inhibés de l'intro SpotCam normale sur ce parcours observé. **source de production inchangée**, `code_change_readiness=blocked`. Les messages `Unimplemented!`, notamment collision et audio, restent des limites. Déplacement réel ne valide ni collisions, ni `GetHeight`, ni gameplay complet : **gameplay complet non validé**, **équivalence cible non validée**. Aucune référence cible authentifiée ajoutée, aucun asset public.

## Handoff
**Après RE-778** : consolider un itinéraire réel après l'intro et la preuve de collision/GetHeight avec préconditions, ABI et référence cible authentifiée avant tout correctif. Ne pas retirer le fondu ou forcer le contrôle pour masquer une séquence normale. **Revue indépendante de publication PASS borné au snapshot** ; aucun stage, commit ou push par le worker publication.
