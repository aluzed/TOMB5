# RE814 — InitialiseItem : continuation bornée

Statut **BOUNDED_CONTINUATION_CHARACTERIZATION**. Revue privée indépendante fraîche
**PASS_scoped**, pas validation de publication/intégration ni production-ready.
Verdict : `b4c4ded966675715a1096e98ef9571351f59703e43a16c3c2ce0fb788f7cbfd7`.
Manifest corrigé : `7bcd98de7a6bb4dc9b7f7932205a84748102e571249571fc1d1e2608b686fc02`.

## Preuve et limites

Huit cas nouveaux construits object 284/285 × room 0/1 × activation absente/complète,
loaded 1 fixe. Registration par producteur littéral authentique initializer/controller,
sans injection t7/t8; seuls t9, GP et SP construits. L'entrée complète ObjectObjects
et le startup naturel ne sont pas exécutés; hashes hérités, pas extraction disc fraîche.
Quatre retours cible complets MIP (pile restaurée), quatre stops **BEFORE initializer**
generic-door; 3696 visites hooks, pas instructions retirées. Le natif termine :
**frontières sémantiques différentes**, aucune équivalence universelle callback.

Vrais GAME/SETUP.C et GAME/ITEMS.C : i386 O0 normal + ASan/UBSan failfast uniquement,
huit retours par mode; status/room/floor concordent 8/8. Snapshot complet comparé
items + activehead + roomheads de 582 octets : égalité 6/8 et deux écarts attendus
active/head par mode car registration native absente. Insertion room, floor signé
et box précèdent callback. Après Add NULL, status réécrit ITEM_ACTIVE sans activation
active/head : status actif n'implique pas insertion dans la liste active.

Original RE814 scellé **FAILED/noncertifié** : printf floor reçoit long via format
incorrect; correction indépendante séparée, aucune certification rétroactive.
Original RE813 **FAILED reste FAILED**. Aucun candidat source ni behavioral RED :
RED/GREEN de cette publication concerne les artefacts metadata seulement.
Aucune activation AnimateItem/DoorControl, initializer/controller non exécutés;
pas startup complet, wholeRAM, hardware, fullbuild, runtime jeu, gameplay ou GREEN global.
La preuve privée existante n'est pas rejouée par ce générateur portable.

## Frontière

BLOCKED-006 existant reste applicable, pas de résurrection BLOCKED-001/002.
RE815 : atteindre naturellement le producteur depuis l'entrée ObjectObjects/startup,
puis composer initializer generic-door et ses dépendances allocation/floor/navigation.
**Non exécuté**, aucune nouvelle RE/matrice; source inchangée, NO PATCH.
