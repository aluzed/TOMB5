# RE819 — préalable privé allocateur réel

**RECOVERED_PRIVATE_REAL_ALLOCATOR_PREREQUISITE_PASS**. Revue indépendante privée
SCOPED_PRIVATE_PASS; publication metadata-only **PENDING_REVIEW**, intégration BLOCKED.
Aucune autorisation production, activation, startup, matériel, gameplay ou GREEN global.

## Gain concret sur RE818
Le double allocateur est remplacé dans la preuve privée par le véritable MALLOC.C
fraîchement compilé, lié et exécuté: SETUP privé initializer284 → InitialiseItem
production → DOOR privé → ITEMS/GETSTUFF/COLLIDE/MALLOC réels. Pas de patch production.
init_game_malloc natif est exécuté; game_malloc effectue une allocation réelle.
Baseline double normal/strict RED comportemental exit1 (82 contre84), compilations et
exécutions réussies; candidat normal/strict GREEN exit0. Mutant rounding réel RED exit1.
Descripteur entier, tail/canaries et whole buffer1088324 octets comparés, projection
indépendante2980 octets,17 événements caller et17 snapshots;11 événements dépendances.
Sensibilité2980 octets/17 événements/8 frontières par mode,255 descripteurs contrôles:
corruptions d'observations distinctes du mutant de code effectivement exécuté.

## Contrôles frais et ABI
Six exécutions natives normal/strict et trois séquences CPU cible malloc/free fraîches,
17 lignes chacune (51 opérations cible), prefixes0/63/64. Demandes0,1,2,3,4,5,82,17 puis
OOM demande1 et libération LIFO. Buffers natifs2170880 et RAM cible2097152 octets
intégralement comparés aux frontières. Arrondi de taille seulement, **pas réalignement
pointeur**: prefix63 conserve mod4=3, sans déréférencement. Native82 demandés/84 consommés
contre cible92 demandés/consommés; layout DOOR natif packed14/82 contre cible16/92.
Projection déclarée, pas identité ABI brute. Une fixture construite generic284 angle0,
quatre salles, portail2/absence255; aucune extension générale de domaine caller.

## Provenance et limites
Caller cible **ARCHIVE_RE816** authentifié via RE818: préfixe suspendu composition
conditionnelle CPU/RAM, pas replay caller frais, pas retour complet ObjectObjects.
Seuls malloc/free cible frais; init cible exclu, descripteur initial construit.
Hooks entrée/sortie pré-épilogue, pas chaque store ni tous arguments natifs;
égalité RAM aux frontières ne prouve pas absence de stores transitoires.
ASan/UBSan fail-fast sans diagnostic runtime sur les chemins exercés seulement;
warnings legacy archivés, pas certification du programme entier.
Exclus: tailles négatives/débordement signé, gfScriptLen invalide, free non-LIFO,
caller door OOM sans garde NULL, DEBUG_VERSION/backend diagnostic.
Original timeout600,240 fichiers **NON CERTIFIÉ**, HANDOFF/manifest originaux absents;
aucune réparation rétroactive. Recovery indépendante distincte, hashes épinglés.
Échec import unicorn Python système puis retry venv accepté; erreur syntaxe finalizer
sans action conservée. La publication ne rejoue ni cible ni binaries privées.

## Acceptation bornée / frontier ouverte
- [x] Revue privée indépendante allocateur réel bornée PASS, données authentifiées.
- [x] Métadonnées sans raw payload/adresses/opcodes; provenance et limites explicites.
- [ ] Revue indépendante de l'union publique exacte; pending, non approuvée ici.
- [ ] Provenance/prérequis caller naturel et compatibilité ABI/layout avant activation.
- [ ] Domaine général, startup naturel, matériel/gameplay et régression intégration.
BLOCKED-006 demeure ouvert. Ces résultats ne cochent pas ses critères globaux.
