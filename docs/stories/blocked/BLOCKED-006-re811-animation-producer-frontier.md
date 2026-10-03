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
