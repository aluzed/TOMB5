# RE818 — préalable privé de composition caller actual-TU

**RECOVERED_PRIVATE_ACTUAL_TU_CALLER_COMPOSITION_PREREQUISITE_PASS**.
Revue indépendante privée bornée PASS, publication metadata-only en attente de
revue finale parent distincte. Aucune autorisation production, intégration ou activation.

## Gain concret sur RE817
RE817 appelait directement un initializer privé weak, sans registration ni
InitialiseItem. RE818 recompile et exécute SETUP privé qui inscrit uniquement
initializer284, puis **InitialiseItem de production**, DOOR privé et les dépendances
GETSTUFF/COLLIDE/ITEMS réelles. Aucun pointeur attendu injecté après registration.
Le contrôle poison reste inchangé. SETUP est une recette partielle privée, pas une
restauration complète ObjectObjects. Cette composition remplace la preuve de callee
isolé par un dispatch réellement effectué sur les TUs; elle ne prouve pas startup.

## Preuve indépendante acceptée
Candidat normal/strict ASan/UBSan fail-fast GREEN exit0; baseline comportementale
normal/strict RED exit1, respectivement114/113 octets divergents. Les mutations de
registration et caller sont RED exit1. Stderr runtime vide; warnings legacy conservés.
Projection native indépendante2980 octets sur six régions complètes déclarées,
11 événements ordonnés (allocation1, GetDoor5, ShutThatDoor4, ItemNewRoom1),
17 snapshots; sensibilité mono-octet2980. Les hooks sortie sont pré-épilogue,
pas une trace exhaustive des stores. ELF et symboles actual-TU vérifiés indépendamment.

La cible est **l’archive RE816 authentifiée**, sans replay cible frais ici:
préfixe registration601 visites hooks puis caller1147 visites, CPU/RAM conservés;
seuls A0/RA changés pour la composition conditionnelle. Framework bases/GP/SP
construits, pas startup naturel ni retour complet ObjectObjects; visites ne signifie
pas instructions retirées. Projection/rebasing explicites, pas identité ABI.
Une fixture generic284 angle0 rooms0..3 portal2/absence255 uniquement.
Allocateur natif **double82**, allocation cible92; tail/canaries déclarés.

## Refus historiques conservés
Le producer timeout600 original (338 fichiers) reste NON CERTIFIÉ, sans HANDOFF
ni manifest; l’inventaire immuable est conservé. La première revue refusée omettait
le callback poison99 dans l’attente baseline. Ledger réel [10,11,20,99,21], sans
initializer privé; correction de l’attente dans la revue seulement, pas réécriture du
refus ni certification rétroactive. Protocole flock documenté des commandes
récupérées, pas observation système rétroactive des verrous historiques.

## Provenance exacte
Verdict privé `f0cddda154ee0577dd9f1c09571fc01e7f0fc65fdad49ecad9ff7ba93ee77786`.
Manifest privé `881c6e34d4eacd4721adfafe04ff5825ac979324e91aa3322171e40d755b0335`:
184 empreintes vérifiées; seal privé
`672bcbbf6baa4e9c115ec02ed2e75bc29e911c4b3c8f2805e622cf53a998c226`.
Aucun binaire, trace brute, snippet propriétaire ou candidat privé publié.

## Readiness et prochain minimum
BLOCKED-003/004/006 restent ouverts; BLOCKED-001/002 supprimés par utilisateur
ne sont pas recréés. AnimateItem/DoorControl globaux non activés; aucune preuve
matérielle/gameplay, allocateur réel, domaine général, intégration ou GREEN global.
Suite locale RE800–818: comparer les échecs historiques exacts, pas annoncer GREEN.

**RE819 proposé, non effectué**: remplacer uniquement le double allocator par le
plus petit chemin réel d’allocation et ses producteurs de descripteur sur actual-TU,
puis comparer taille/alignement, descripteur complet, tail/canaries et événements à
la cible attribuée. Garder registration→InitialiseItem réel et pointeurs non injectés.
Après cette dépendance, étendre le caller à un angle non nul et une variante portail
asymétrique avec baseline/mutants sensibles, RED avant tout delta privé et revue
indépendante séparée. Aucun GO intégration même si ce minimum devient GREEN.

## Tracker
- [x] Revue privée indépendante et empreintes consommées avant publication.
- [x] TDD metadata RED avant générateur; artifacts déterministes et guards exacts.
- [x] Composition registration/caller actual-TU privée explicitement distinguée de RE817.
- [ ] Revue finale de publication parent distincte.
- [ ] Allocateur réel et extension de domaine caller prouvés.
- [ ] Attribution startup naturelle, intégration et activation autorisées séparément.
