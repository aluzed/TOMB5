# RE-948 — implémentation BLOCKED-007A : SPU minimal, continuation kernel, handler RAM et retour RFE

FINITE_SCOPE_PASS · REVIEWÉ (A, B, C) · INTEGRATION_NOT_YET. Production inchangée ; `integration=false`,
`production_patch=false` ; statuts global/procédure historiques maintenus.

Implémentation du relais [BLOCKED-007A](blocked/BLOCKED-007A-spu-kernel-rfe-handoff.md) en trois lots, chacun
avec preuve d'exécution réelle, oracle compilé indépendant, mutants comportementaux, contrôles négatifs et
revue indépendante sur copie isolée. Preuves privées non versionnées sous
`build/reverse/autonomy-20261014/` (ignoré par git) ; raw RAM et payloads restent privés.

## Lot A — sous-ensemble SPU minimal
Frontière SPU de RE930 (`0xbfc07928`, écriture `0x1f801d86`) franchie. Le modèle range les écritures SPU
dans le `regArea` de `registers.cc`, relit la valeur rangée, et **refuse atomiquement** toute lecture
calculée (CTRL/STAT/ADDR/DATA/IRQADDR/ENDX, ENVX/boucle) et toute écriture à effet de bord. Frontière
suivante : `DIVU` (SPECIAL funct 27) à `0xbfc07668`. Contrôle négatif `--no-spu` → reproduit la frontière
RE930. Oracle `spu_witness.cc` + 6 mutants détectés.
- Seal producteur `2afb97b3…258cd5` (82 membres) ; revue indépendante seal `6c45849c…e8e49` (PASS).

## Lot B — continuation kernel, handler RAM et RFE
Ajout de `DIV`/`DIVU` (`alu.py`, sémantique `psxinterpreter.cc`) et des compteurs racine 0/2 (`counters.py`,
contrat réduit : le kernel ne fait que les remettre à zéro). Le replay (`fresh` et `restored`) atteint
**naturellement** le vecteur général RAM `0x80000080`, le handler noyau `0x2700`, et revient par **RFE
`0x29d0`** (deux syscalls : un depuis la ROM, un depuis la RAM). Aucun handler/thread/RA injecté, BEV non
effacé à la main. Prochaine frontière : écriture CD-ROM `0x1f801800` en RAM `0x145c` (hors acceptation).
Contrôles négatifs : `--no-divu` → `0xbfc07668` ; `--no-counters` → Timer0 `0x1f80104`/`0x1c68` ;
`--no-rfe` → RFE `0x29d0`. Oracles `divu_witness.cc` et `counter_witness.cc` (4014 paires DIV/DIVU) +
8 mutants détectés.
- Seal producteur `689fe643…1ce972f` (136 membres) ; revue indépendante seal `a8909360…aab983` (PASS,
  composition A→B : `spu.py` byte-identique).

## Lot C — gate de fidélité et d'intégration
Écarts classés (`fidelity.json`) : load-delay, invalidation de cache et mirroring 8 Mio **non pertinents
dans le scope fini** ; byte-identité RAM, reset naturel/BIOS Sony, CD/GPU/audio/DMA et second algorithme
CPU **bloquants pour des revendications plus fortes**, non revendiqués. Naturalité démontrée **dans
l'entrée OpenBIOS construite** uniquement. Aucune fidélité globale revendiquée.
- Seal gate `46e8b31d…825fe` ; revue indépendante seal `2beee4a4…d2d8069` (PASS, `logic_errors=[]`).

## Reproductibilité (privé)
Depuis `build/reverse/autonomy-20261014/blocked007a-lotA-spu/`, `…/blocked007a-lotB-kernel/`,
`…/blocked007a-lotC-fidelity-gate/` : `python3 guard.py` rejoue chaque plan sous les locks canoniques
(recompile les oracles `g++ -m32`, `tests.py`, `mutants.py`, replays et scelle). Chaque `manifest.json`
scelle tous les membres ; `seal.json` couvre le manifest.

## Limites
Entrée construite (pas de reset matériel/Sony BIOS) ; contrat compteur réduit (aucun tick/IRQ/gate) ;
pas de load-delay/invalidation de cache/mirroring ; RAM intermédiaire non revendiquée byte-identique ;
CD-ROM/GPU/audio/DMA non modélisés. BLOCKED-007 reste partiellement bloqué ; AUCUN commit/push.

[Dashboard BLOCKED-007A versionné](../reverse/tomb5-progress-dashboard-re948-blocked007a-v1.html).
