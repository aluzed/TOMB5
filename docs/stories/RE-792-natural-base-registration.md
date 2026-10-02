# RE-792 — BASE chargé naturellement, bridges réellement enregistrés

2 octobre2026, parents RE790/791. **PASS indépendant borné : sélection naturelle BASE et registration réelle. Aucun callback consommé prouvé.** Moteur mix-relink courant, pas fullbuild.

## Tracker
- [x] Vrais inputs titre : Up, LeftShift/L1 et C/Cross ; réception SDL et pad natif observée, New Game non verrouillé à confirmation.
- [x] Loader naturel sélectionne niveau moteur4, entrée conteneur5 ; aucune écriture mémoire, call injecté ou téléportation.
- [x] 177items/169rooms, huit BRIDGE_FLAT réellement chargés ; inventaire complet concorde avec corpus frais, objets/rooms/positions/rotations et flags bridges.
- [x] Deux ObjectObjects réels ; six slots installés,12 comparaisons d’adresses/symboles et champs bruts conformes dans la revue privée.
- [x] Runtime452draws, contrôle libéré draw2, inputs de déplacement réels ; PNG capturés et inspectés.
- [x] Revue indépendante étroite PASS persistée ; six tests corpus rejoués, cleanup vérifié, échecs historiques préservés.
- [ ] Zéro entrée des douze callbacks/adaptateurs surveillés ; effet bridge et gameplay demeurent bloqués. RE-794.

## Comptages et preuve
GetHeight964 paires retenues, GetCeiling840, GetCollisionInfo100 :1904 paires recomptées, sans retour manquant. Totaux finaux17149/13367/450 : compteurs instrumentés archivés, **pas** reconstruction indépendante exhaustive de leurs visites. 452draws ne sont ni452images archivées ni tests. Les bridges existent dans d’autres rooms que celles du parcours observé ; leur présence et registration ne prouvent pas leur consommation.

Archives `build/reverse/autonomy-20261002/re792-base-runtime/`. run01 échoue Xauthority avant lancement ; run02 confirmation tardive alors que le titre est verrouillé ; run03 réussi. Les échecs ne sont pas effacés. Nouveau display à cookie Xauthority sans accès libre, root bwrap read-only sauf sortie ; pas sandbox générale hermétique. Application terminée par debugger-kill borné, wrapper0/Xvfb0 ; tous groupes/PIDs et display vérifiés absents.

Revue `re792-review/verdict.json` : PASS exclusivement sélection BASE, inventaire et registration. La **FAILED large RE790 reste inchangée**. Quatre TUs fraîches et reste historique, inputs implicites/link closure non approuvés. **pas de GREEN global** sanitaire/gameplay et pas de preuve ABI universelle, hardware ou effet des bridges.

## Validation publique
Six tests metadata-only écrits avant artifacts : RED six absences conservé, puis GREEN6. Suite héritée RE789 plus ces six tests : **135 PASS en20,20s**, exit0, aucun document réécrit. Cette suite inclut les compilations actual-TU existantes, pas un nouveau runtime ni suite globale. Premier append : six digests historiques RED et deux contrôles heading RED ; seules sections successeur RE790 exclues, digests historiques inchangés, nouveau guard protège tous les bytes antérieurs. Heading successor borné adapté sans affaiblir le contrôle ancien. Logs/commande exacts sous `build/reverse/autonomy-20261002/re790-suite.ledger.json` ; revalidation après texte finale requise.

## Handoff
RE-794 : capter état naturel door/flip/secteur et rejoindre une référence bridge par contrôles légitimes, puis suivre entrée/sortie callback et effet consommé. Deadline autorisée jusqu’au2octobre23h, aucun GO distinct requis pendant cette fenêtre.
