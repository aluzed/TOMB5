# RE821 — composition caller nonzero, sans portail ni flip

**private-reviewed : PASS_SCOPED de caractérisation privée bornée. Publication metadata-only PENDING_FINAL_REVIEW.**

integration_approved=false; publication_review_approved=false; production_patch=false;
natural_startup_proven=false; gameplay_proven=false. Aucun GREEN global ni
nouvelle intégration source. Le PASS indépendant privé ne vaut pas approbation
publique exacte ou production. Cette publication ne relance aucun probe privé.

## Domaine et progression depuis RE820

Quatre fixtures **construites** objet284 : -32768, 16384, -16384, 1 ; cellules
porte 13, 7, 17, 17. Sans portail ni flip. RE820 appelait directement
l'initializer privé ; RE821 compose `InitialiseItem` puis cet initializer,
après registration native privée partielle. Le caller réinitialise les champs
empoisonnés, conserve y_rot nonzero et utilise un secteur sol distinct du
secteur porte orienté. Angle1 est une branche logicielle construite non cardinale.
Ce contrôle de champs/validité/mathématiques ne prouve ni provenance naturelle
des angles, ni startup, ni gameplay.

Côté cible : préfixe registration suspendu puis **dispatch externe conditionnel**
du caller, sur le même CPU/RAM ; seuls argument item et retour sentinelle sont
changés. Callback enregistré, entrée initializer, continuation et retour
sentinelle contrôlés ; pas de retour ObjectObjects complet ni d'enchaînement
naturel du caller. Les visites de hooks ne comptent pas les instructions retirées.

## Résultats privés consommés, pas réexécutés ici

- Producteur : huit cas natifs i386 frais (quatre normal, quatre ASan+UBSan
  fail-fast), exit0, stderr runtime vide ; quatre compositions cible authentifiée.
- Buffer natif complet **1088324 octets**, entrée initializer **464 octets**,
  projection cible **2980 octets** : comparaisons dans ce domaine, avec rebasing
  explicite des pointeurs, poison/tails et heap native inclus. RAM entière
  archivée n'est pas un oracle exhaustif de toute RAM.
- Allocateur réel : demande native82/consommation84 contre cible92/consommation92 ;
  projection ABI i386 packed vers MIPS32, pas identité brute d'allocation.
- Deux mutants bypass réellement compilés/exécutés exit0 puis contrats exit1,
  **34 octets** différents chacun et snapshot caller incorrect. Ce RED
  comportemental distingue l'appel direct de la composition caller ; le setup
  RED initial (résultat absent) n'est pas une régression comportementale.
- Reviewer : huit nouveaux cas natifs, quatre nouveaux replays cible et quatre
  observations cible supplémentaires indépendantes. Reconstruction des buffers
  caller/initializer et décodage du dispatch sans oracle producer pour ces
  contrôles. Le replay byte-identique seul n'est pas un oracle indépendant.
- Ordre registration/caller/initializer/allocation/GetDoor deux fois/
  ShutThatDoor deux fois/sorties confirmé ; absence ItemNewRoom dans ce domaine.

## Limites de preuve et attribution

Snapshots exit **PRE-EPILOGUE**, pas preuve **post-RET** native ni de chaque store
transitoire. ShutThatDoor est le corps **DOOR privé**. ITEMS/GETSTUFF/MALLOC réels
compilés et chemins atteints ; **COLLIDE lié mais non invoqué** pour navigation.
**137 dépendances** épinglées **après compilation** : pas certification
historique **précompile** ou avant/après de la closure headers/SDK.

Objects/anims/floor_data hors dump final ; pas d'orientations générales, portail,
flip, activation, AnimateItem, OOM, SDK/GTE/matériel, lifetime ou absence générale
d'UB prouvés. Sanitizers limités aux chemins exercés, leakchecking désactivé.
Registration native partielle seulement. Budget historique producer et chaque
ancienne acquisition de lock non certifiés par la revue indépendante.

L'observateur reviewer mémoire-écriture a échoué avec une exception Unicorn ;
essai conservé. Observation par décodage des stores réussie ensuite ; cause
interne exacte non démontrée, sans attribution à un codebug jeu.

## Provenance privée et incident fournisseur

Documents locaux consommés (pas de liens HTTP prétendument vérifiés) :

- `build/reverse/autonomy-20261004/re821-caller-proof/HANDOFF.md`
  SHA256 `51aa28f59932ee007d6d477f658706c269281d531430abc5a0e8a414b4115a1e`.
- `build/reverse/autonomy-20261004/re821-independent-review/review.md`
  SHA256 `90534c3d05096702396b8c3782babc46b9fdbcf40b5adc6caedb9a38e4873f26`.
- Verdict indépendant SHA256
  `690dafaf7487cc1b453e883fe3db3ab949e9a2ac7ffae3e65cdf968510258fe8` :
  passed=true, integration_approved=false, production_approved=false.

**Incident provider résolu** selon le contexte parent : première délégation
signalée après lectures seulement (26 s), seconde reformulée fonctions jeu
réussie (503.64 s). Ce refus fournisseur n'est pas un test exécuté ni un codebug.
Pas de blocage provider actuel : aucun nouveau ticket, aucune inscription de
blocage persistant à BLOCKED-006 nécessaire. BLOCKED-006 reste ouvert pour les
frontières jeu/provenance existantes ; sa story historique reste inchangée.

## Acceptation / prochain front autorisé séparément

- [x] Caractérisation privée finie de composition caller nonzero.
- [x] Revue indépendante privée PASS_SCOPED consommée et documents hash-vérifiés.
- [x] Publication documentaire sous TDD : RED story absente, puis GREEN borné.
- [ ] Revue finale de ces trois fichiers publics exacts ; publication encore pending.
- [ ] Provenance naturelle et domaine élargi avant activation partagée.
- [ ] Intégration/production explicitement autorisée et validée séparément.

Frontière suivante : **corpus authentique d’angles OU domaine portail/flip distinct**
avant activation partagée ; **pas de nouveau caller construit répétitif**.
Aucune nouvelle recherche, aucun build jeu/media, aucun stage/commit/push/job
n'est réalisé dans cette unité metadata-only.
