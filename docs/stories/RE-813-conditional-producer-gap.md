# RE813 — Producer gap conditionnel / caller Add / Remove

Statut : **CONDITIONAL_PRODUCER_GAP_CHARACTERIZATION**, pas production-ready.
Revue producteur originale **FAILED**, jamais convertie rétroactivement en PASS.
Verdict rejeté : `cf6dbe95e14610a15b96cde970f29f761c449c78aaa7eacfc766963b6a851009`.
Original FAILED préservé : `6851e65789ac5a52951bd1a15cd99983dde8c349806036f1d13315fec410b01a`.
Verdict indépendant séparé, fixture corrigée à stockage static : **PASS_scoped**,
`16ce302f58d9c55e00c53893240937adc32d26f29f228e4ecd9997d4011b66ab`.
Ce verdict n'approuve ni publication ni intégration; revue de publication pending.

## Comptages et écart réel

Quatre cas corrélés construits loaded 0/1 × object 284/285, quatre slices
registration, quatre entrées caller Add et quatre Remove. Deux contrôleurs cible
nonNULL contre zéro installation native dans le vrai ObjectObjects.
GAME/SETUP.C garde la registration generic-door désactivée sous #if0, confirmé
par préprocessing frais. Ce manque de producteur natif explique deux divergences
Add sur active/head dans chacun des modes; quatre égalités Remove dans chacun.
Comparaison oracle indépendant items+head complet : 578 octets par snapshot.
1334 visites hooks non-stopping; 12 stops avant exécution, soit 1346 visites
au total : pas un nombre d'instructions retirées.
Exécution fraîche cible et vrais GAME/SETUP.C / GAME/ITEMS.C natifs,
**i386 O0 normal + ASan/UBSan failfast only**; aucune certification globale.
Aucun correctif source ni activation : le gap est caractérisé, pas résolu.

## Rejet préservé et limites

Le sceau producteur contient 191 entrées, 190 concordent : HANDOFF divergent.
Le fixture producteur utilise un tableau automatique modifié après setjmp puis
lu après longjmp, invalide pour établir cette preuve. stderr vide/exit zéro ne
répare pas cette faute. Fixture originale et sceau restent rejetés et inchangés.
La correction est exclusivement celle du harness indépendant à stockage static.
369 hashes revérifiés avant publication, aucun écart; ce n'est pas un nouveau
sceau d'acceptation du producteur.

Registration conditionnelle démarre avec registres entrants construits, dont
le pointeur de contrôleur fourni; stores authentiques, pas démarrage naturel ni
appel ObjectObjects complet cible. Le DoorControl enregistré n'est pas invoqué.
Add est observé avant épilogue; caller suspendu, pas InitialiseItem retourné.
Remove est une invocation directe séparée conservant la pile caller suspendue,
pas continuation naturelle ni preuve de restauration de pile.
Oracle complet des 578 octets; RAM archivée reproduite, mais pas oracle déclaratif
indépendant de toute la RAM ni trace exhaustive des stores transitoires.
Payload/relocation hérités authentifiés, pas extraction/relocation fraîche ni
nouvelle authentification disque; émulation logicielle, pas hardware.
Quatre cas seulement, pas corpus gameplay, retrait intérieur/queue non couvert.
Warnings compilation privée conservés; runtime stderr vide des modes bornés,
pas fuite/ABI/optimisation alternative ni global sanitizer clearance.

## Source et frontier

GAME/ITEMS.C inchangé : `4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f`.
GAME/SETUP.C inchangé : `4c0de40b6aa06d1206971a15041ca76e2b164e213377a02d3fb31017d6a07720`.
Aucun runtime jeu, gameplay, fullbuild RE813, GREEN global ou readiness globale.
AnimateItem et DoorControl ne sont pas activés. BLOCKED-006 reste applicable :
attribution naturelle du dispatch/producteur, actual-TU behavioral RED avant
nouveau delta, preuve indépendante et autorisation distincte avant activation.
Le RED présent concerne la publication metadata absente, pas un bug corrigé.
Les récits RE812 restent historiques; cette section RE813 les complète sans
réécrire leurs statuts ni supprimer les quatre échecs historiques RE801/RE802.

## Tracker

- [x] Rejet producteur original et diagnostics préservés.
- [x] Fixture indépendante corrigée séparée PASS_scoped, digest exact épinglé.
- [x] RED public metadata observé avant générateur et docs.
- [x] CSV/functiondoc et dashboard append-only; source inchangée.
- [ ] Revue indépendante finale de ces hashes de publication.
- [ ] Producteur natif naturel, dispatch et continuation caller acceptés.
- [ ] Behavioral RED actual-TU et autorisation avant delta/activation.
- [ ] Runtime/gameplay/fullbuild/global readiness : non revendiqués.
