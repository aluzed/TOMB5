# RE-866 — intégration native bornée mRotY

Statut: candidat intégré non committé; independent finalreview pending.

## Progression
- [x] Verdict privé RE865 SCOPED_PASS_MROTY_ONLY relu et hash exact authentifié.
- [x] Régression publique actual-TU synthétique écrite avant toute mutation production.
- [x] RED UBSan ELF32 et ELF64 sur source publique inchangée; comportement normal
  déjà correct sur ces 36 cas: aucun écart comportemental inventé.
- [x] Delta minimal mRotY uniquement, identique au hash privé examiné.
- [x] GREEN 36 cas × 8 configurations ELF32/ELF64, O0/O2 normal/UBSan failfast.
- [x] RED documentaire observé avant création de cette story/dashboard.
- [ ] Revue indépendante finale des hashes publics; aucun stage, commit ou push.

## Contrat public
Trois matrices et douze angles, table CAMERA.C versionnée, aucune donnée protégée.
MATHS.C et LIBGTE.C complets compilés; fonctions étrangères retirées par section GC,
liaison stricte sans symboles non résolus. Neuf shorts attendus calculés par oracle
scalaire indépendant (produits MAC, division plancher puis narrowing, pas IR saturé).
608 mots: projections fixes des deux piles et trois banques GTE; SP et index
Matrix préservés. Les queues natives supplémentaires des piles sont explicitement
vérifiées octet par octet: sizeof(MATRIX3D) n'est pas supposé égal à 32.
Baseline normal avant delta et tous les GREEN identiques sur les 608 mots.
ELF64 utilise fpermissive pour le cast legacy mmPushMatrix hors chemin;
aucune portabilité générale du jeu n'est revendiquée.

Le hash MATHS.C attendu est
`59e70b260ae67d613e5fa74486c728a63bd3bb7ae4727537e293d4c057d9b7fa`.
Le gate backend préexistant de MATHS.C est conservé, comme mRotX/mRotZ.

## Limites et blocage maintenu
RE858 global FAIL et rawGTE FAIL restent inchangés. integrationGetSpheres=false:
GetSpheres production reste stub. Aucun CALCLARA privé ni buffer de preuve publié.
D9 upper16 reste divergent dans la composition privée; count<=0 diverge aussi.
Flags2/3 et interpolation non validés. Aucun oracle hardware, nouveau replay cible,
startup, reachability naturelle, runtime gameplay ou GREEN global.
Les incidents historiques et timing producteur RE865 restent non certifiés;
le PASS de contenu étroit n'est pas leur réhabilitation.

## Vérification exécutée
Sélection publique RE866 + RE859 + RE862 + tests/emulator: **3689 passed in
116.10s, exit 0**; ledger relevant-suite.command.json. Build Debug ELF32
incrémental: MATHS.C recompilé, MAIN relié, exit 0. Ce build n'est ni runtime
ni portabilité ELF64. Setup initial rejected: hypothèse sizeof(MATRIX3D)==32
fausse (44 observé); tentative conservée actualTU, corrigée par vérification
explicite des queues natives avant nouveau RED/GREEN actualTU-v2.

## Documentation compatible et livraison
Dashboard ajouté sous le seul marqueur re866-mroty-integration. Guards RE859/RE862
conservent leurs hashes historiques et excluent uniquement ce delta nommé;
guard RE866 épingle intégralement le dashboard antérieur et rejette tout autre ajout.
Les suppressions utilisateur BLOCKED-001/002 et report-tech restent intouchées.
Preuves locales et ledgers: build/reverse/autonomy-20261010/re866-integration.
HANDOFF et manifeste exacts destinés au coordinateur pour revue finale indépendante.
Prochain objectif: revue de cette intégration seulement; GetSpheres reste bloqué.
