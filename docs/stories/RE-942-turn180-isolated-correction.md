# RE942 — turn180_effect, correction isolée — DRAFT

**Statut : DRAFT, revue publique indépendante attendue.**
`integration_turn180_patch_pending_public_review=true` ; **AnimateItem integration=false** ; `globalprocedure=false` (réserve historique conservée).

## Delta et attribution

Une seule expression dans [GAME/EFFECTS.C](../../GAME/EFFECTS.C) :
```cpp
item->pos.y_rot = (short)((unsigned short)item->pos.y_rot - 32768u);
```
La négation de x_rot est inchangée. ANGLE(180) donne 32767 dans cette configuration ; le callback exige un demi-tour exact de 32768 modulo 65536. L'attribution privée RE942 command6 a été relue : sept instructions, axes indépendants et retour avec dernier store. Aucun dump, opcode, adresse cible, actif propriétaire ni preuve ignorée ne devient une dépendance des tests publics.

Trois états distincts : **preuve privée command6 finie** (candidate CONTROL seulement, non publiée), **correction source isolée** ici, **entrées naturelles / intégration AnimateItem bloquées**. La revue privée a autorisé uniquement ce delta GCC i386 ; elle n'autorise ni activation AnimateItem ni approbation gameplay globale. Le [prédécesseur RE941](RE-941-animateitem-command4-private-proof.md) et son [dashboard figé](../reverse/tomb5-progress-dashboard-re941-v1.html) restent inchangés.

## Régression publique autonome et TDD frais

[Runner pytest](../../tests/reverse/test_re942_turn180_actual_tu.py) et [harness C++](../../tests/reverse/re942_turn180_actual_tu.cpp).
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider -q tests/reverse/test_re942_turn180_actual_tu.py
```
Prérequis externes : Linux, GCC/g++ multilib i386, binutils, pytest, en-têtes SDL2 système. Le runner découvre la racine via son propre fichier, compile EFFECTS.C entière avec ses en-têtes publics, lie normalement la vraie table statique slot0. Aucun CONTROL.C ni appel AnimateItem. Les dépendances `-MM` sont découvertes sur la source canonique, leurs hashes sont enregistrés avant compilation puis contrôlés après ; aucun hash complet de TU n'est figé dans le test. Les sorties sont neuves dans tmp_path (ou RE942_OUTPUT). RE942_MUTATION_LOCK permet de désigner le mutex canonique absolu en export public ; ne pas envelopper le runner dans un flock extérieur.

Domaine : 65 536 couples diagonaux couvrant chaque axe 16 bits, plus 49 couples cartésiens critiques, soit **65 585 entrées**, un/deux appels directs et via la table réelle dans les deux ordres. Oracle bytewise modulaire indépendant, comparaison complète des 144 octets ITEM_INFO, invariance FXType. L'indépendance des axes explique la couverture par axe, **pas une énumération des 2^32 couples**. Le mutant xneg distingue 65 569 entrées avec 16 contrôles.

TDD observé avant delta production : normal **RED 65 585**, strict ASan+UBSan **RED 65 585** (pytest exit1). Après delta : normal et strict **GREEN 65 585** ; baseline inverse créée uniquement en scratch **RED 65 585**, mutant xneg scratch **RED 65 569 / 16 contrôles**. Un test qui rejette un mutant RED peut être GREEN ; l'exécutable mutant reste exit1. Les avertissements hérités de compilation sont retenus explicitement, stderr runtime doit être vide ; sanitaires fail-fast, leaks désactivés.

Les symboles EFFECTS non sélectionnés sont reliés à une frontière abort documentée et inventoriée : leur non-exécution est une propriété finie, pas une validation des autres callbacks/services. Conversion signed-short vérifiée sur GCC i386, aucune promesse ISO C++ universelle ou autre plateforme. Pas de nouvelle exécution cible/hardware, BIOS/disque/startup, gameplay naturel, animation transitions, gravité ou autres commandes.

## Tracker et cleanup

- [x] RED public frais avant l'expression production.
- [x] GREEN normal/strict et mutants finis.
- [x] Export minimal des dépendances publiques, sans .git/build initial ni assets ignorés ; replay autonome.
- [x] Story et [dashboard RE942 versionné v1](../reverse/tomb5-progress-dashboard-re942-v1.html), liens relatifs vérifiés.
- [x] État utilisateur/prédécesseurs protégés, cleanup limité aux objets neufs avec mesure avant/après dans la livraison privée.
- [ ] Revue publique indépendante exacte par le parent, puis décision d'intégration.

Aucun stage/commit/push. Les ledgers, RED initiaux, hashes, verdict et HANDOFF de production sont des sorties privées de livraison sous la racine unique annoncée ; les tests publics n'en lisent aucun fichier. `globalprocedure=false` historique demeure : bootstrap et journaux des anciennes preuves ne sont pas rétroactivement certifiés par ce replay neuf.
