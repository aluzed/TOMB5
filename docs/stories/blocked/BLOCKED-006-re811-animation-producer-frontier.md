# BLOCKED-006 — Frontier après RE-811
AlexP — blocked. Le correctif RemoveActiveItem ne valide pas AnimateItem/DoorControl stubs, ni la reachability naturelle des producteurs.
## Acceptation avant activation
- [ ] Attribution naturelle du dispatch et des prérequis producteurs.
- [ ] Régression publique actual-TU RED sensible avant tout nouveau delta.
- [ ] Preuve bornée indépendante des buffers complets et événements ordonnés.
- [ ] Revue indépendante et autorisation distincte avant intégration.
Aucune activation, runtime/gameplay, plateforme alternative ou GREEN global revendiqué.

## RE818 — evidence metadata-only, blocker maintenu ouvert
Revue privée indépendante scoped PASS: inscription initializer284 par SETUP privé,
InitialiseItem production réel puis DOOR privé et GETSTUFF/COLLIDE/ITEMS réels;
aucune injection postregistration. Baseline normal/strict RED1, candidat GREEN0,
mutants registration/caller RED1; projection2980/6 régions,11 événements,17 snapshots.
Archive cible RE816 seulement; framework construit, allocateur double82 vs cible92,
une fixture generic284 angle0 portal2/255. Timeout338 fichiers NON CERTIFIÉ.
- [ ] Allocateur réel et extension sensible de domaine sur caller actual-TU.
- [ ] Dispatch/producer naturellement atteints, hors composition conditionnelle.
- [ ] Régression publique comportementale et revue d’intégration séparée.
La preuve privée bornée ne coche pas les critères globaux ci-dessus. Aucune activation
AnimateItem/DoorControl ni production-ready. Voir RE-818-actual-tu-caller-prerequisite.

## RE819 — allocateur réel privé borné; blocker toujours ouvert
MALLOC.C réel compilé/lié/exécuté dans composition SETUP privé → InitialiseItem
production → DOOR privé → ITEMS/GETSTUFF/COLLIDE réels. Baseline double RED1
82 contre84; candidat normal/strict GREEN0, mutant rounding RED1. Native84 vs
cible92 ABI distinctes; projection2980/whole buffer1088324,17 événements/snapshots.
Contrôles malloc/free cible frais3 séquences, natifs6, prefixes0/63/64; arrondi
taille seul, pas réalignement pointeur. Caller ARCHIVE_RE816 via RE818, pas
replay caller frais/startup/matériel/gameplay. Timeout240 fichiers NON CERTIFIÉ.
- [ ] Provenance caller naturellement atteint et compatibilité ABI/layout.
- [ ] Domaine caller général et régression comportementale publique.
- [ ] Revue union publique exacte puis intégration séparée; aucune activation.
PASS privé ne ferme pas le blocker; publication pending revue. Voir RE-819-real-allocator-prerequisite.

## RE830 — provenance table LIFTS; readiness blocked

Progression : attribution du producteur RelocPtr[MOD_LIFTS], pas activation.
DEPENDENCY_BLOCKED; readiness=blocked; publication_review=PENDING_FINAL_REVIEW;
publication_review_approved=false; integration_approved=false; production_patch=false;
natural_startup_proven=false; gameplay_proven=false; behavioral_GREEN=false.

Huit modules réellement loader-produits et huit buffers relocalisés complets
comparés dans les archives privées. Le header du niveau3 choisit les descripteurs
30/23/29/17/12/2/7/49 → module_ids22/15/21/9/4/1/2/41.
Index de descripteur != identifiant logique module : MOD_LIFTS49 existe au
descripteur57 NON sélectionné; le choix49 produit module41, pas LIFTS49.
RelocPtr[MOD_LIFTS] reste NULL; aucun pointeur/module substitué pour obtenir GREEN.
ObjectObjects inchangé : 620 visites archivées, arrêt gardé avant NULL, pas retour
complet; runner exit0 / contrat comportemental exit1, donc PAS GREEN fonctionnel.

Comparaison RAM complète8MiB au delta RE829 réutilisé : neuf différences stack;
pas whole-RAM GREEN ni oracle whole-RAM indépendant. Cause sauvegardes loader
plausible, non observée dynamiquement. Framework/GP/SP/heap construits, services
CD doublés; suffixe loader, pas LoadLevel entier. Pas startup naturel, native frais,
gameplay, cohérence upstream ou intégration prouvés par cette publication.

Revue indépendante addendum : PASS contenu fini, security_concerns=[] et
logic_errors=[]; sans replay/build nouveau. FAIL reviewer initial préservé
(erreur de comparaison reviewer, pas régression cible); FAIL procéduraux historiques
RE829/RE830 inchangés, historical_procedural_acceptance=false. Aucune approbation publique
finale ni audit/replay parent revendiqué; parent a lu rapports/verdict, vérification
du manifest parent non encore revendiquée.
Verdict addendum SHA256 : 12fd8f2ec92803b88c5dc3fb123c0b2dc002c7d7e40fb840f42fb5e8ebac73b6.
Rapport addendum SHA256 : 509490f26a07ec46fc37a8a16a1a16c726fcc24b992a8891e8839746fc17c2c9.
Provenance locale : build/reverse/autonomy-20261004/re830-table-provenance-proof/HANDOFF.md
et build/reverse/autonomy-20261004/re830-independent-review-addendum/RAPPORT.md;
archives consommées, aucun nouveau runtime cible/native ni générateur historique.

### Vérification documentaire après réparation des gardes historiques
Sélection littérale RE819 + RE820 + RE821 + RE830 : 57 passed, exit0 observé.
Douze régressions successor-only foreign/duplicate/altered/missing/history/unknown
et reconstruction exacte du seul delta RE830 de test819 : GREEN documentaire.
Les empreintes anciennes et assertions historiques restent inchangées; aucun
append futur générique accepté. Premier résultat littéral 32 passed / 2 failed,
exit1, préservé dans re830-publication/literal-predecessors-plus-new.json; les
archives de première publication FAIL ne sont pas réécrites ni requalifiées.
Résultat frais : build/reverse/autonomy-20261004/re830-publication-guard-repair02/sensitive-green.json.
Ce GREEN metadata-only ne prouve aucun comportement cible/native ni acceptation
procédurale historique. Revue indépendante exacte des six fichiers + manifest
PENDING_FINAL_REVIEW; aucune intégration/activation approuvée.

### Acceptation manquante / prochaine frontière (autorisation séparée)
- [ ] Réconcilier sélection naturelle niveau/header/modules et objects réellement
  chargés en amont, sans flags hérités ni injection de pointeur/module.
- [ ] Ou établir un niveau authentique sélectionnant le descripteur MOD_LIFTS57
  avant registration, avec domaine objects cohérent et producteur naturellement atteint.
- [ ] Régression publique comportementale actual-TU RED sensible puis preuve bornée
  indépendante des buffers complets et événements ordonnés dans ce domaine naturel.
- [ ] Revue finale indépendante des six fichiers publics exacts : PENDING_FINAL_REVIEW.
- [ ] Revue et autorisation distinctes avant intégration; aucune activation
  AnimateItem/DoorControl, aucun startup/gameplay ou GREEN global revendiqué.

Les critères historiques restent ouverts. La frontière est sélection naturelle
module/objects, pas un nouveau caller construit répétitif ni substitution57 à49.
[Progression RE830 / overview actif](../../reverse/tomb5-progress-dashboard.html#re830-publication).
