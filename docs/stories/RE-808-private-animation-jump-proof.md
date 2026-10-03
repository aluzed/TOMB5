# RE-808 — Preuve privée bornée animation jump/gravity

Auteur : AlexP — statut progress, aucune livraison production.

## Tracker
- [x] Verdict technique privé PASS et rapport vérifiés; 654 fingerprints producteur et 267 revue authentifiés.
- [x] Garde FIRST RED observée avant publication; dashboard antérieur entier épinglé.
- [x] Preuve revue : 12 retours authentiques, 1543 visites hooks, 16716 octets complets par cas.
- [x] actual-TU privée revue : baseline RED12, candidat GREEN12 normal/strict; mutants omit-jump5, link-before2, drop-x-second5.
- [x] Suite publique publication/provenance RE800–808 fraîche : 63 tests PASS; GetChange actual-TU 1440 cas normal et strict, zéro divergence, stderr runtime vide.
- [ ] Revue finale indépendante publication par le parent : pending.
- [ ] RE-809 : command3/removeactive ou dépendance suivante réellement nouvelle, planned-not-proven.
- [ ] Intégration, activation, registration, readiness et gameplay non autorisés.

## Contrat observé, pas reconstruction générale
Frame incrémentée : les contrôles restent à ou sous frame_end; seul dépassement strict consomme les anciennes commandes2 avant liaison animation, puis gravité et retour. Première opérande fallspeed, seconde speed, gravité armée avec autres flags conservés; deux commandes ordonnées, dernière gagne. Commande2 nouvelle seulement sautée. Gravity entrante ou remplacée; seuil signé128, incrément6 dessous sinon1. Réduction16 bits du fallspeed distincte de l’intermédiaire Y non réduit. Position X conserve la seconde contribution longitudinale authentique, même inhabituelle; composante latérale nulle ici, aucune correction intuitive. Décalages négatifs et narrowing seulement ABI/compilateur ELF32 mesurés. GetChange non atteint; commande1/TranslateItem du prédécesseur non re-prouvée.

Six buffers ITEM144 + ANIM80 + CHANGE12 + RANGE32 + COMMAND64 + TRIG16384 = 16716 octets. RAM cible finale comparée hors pile caller36, quatre substitutions GP déclarées, poison registres reviewer distinct. Pas de preuve stores transitoires, pile exacte, mémoire native arbitraire ou matériel. Hooks code/read seulement, aucun MEM_WRITE ni invariance instrumentation. Douze fixtures synthétiques, deux animations bornées par asserts; pas corps AnimateItem complet, pas corpus gameplay/startup, commandes4/5/6 et mouvements/accélérations généraux exclus. Aucun replay cible par le worker publication.

## Incidents conservés et checkpoint courant
Timeout wrapper producteur600s déclaré : aucun exit/log inventé. HANDOFF historique EN COURS et manifest IN_PROGRESS intacts. Le verdict indépendant courant permet seulement ce checkpoint technique privé, ne réécrit pas leur état. Premier gel reviewer sous sibling lock erroné puis correction canonique déclarée; aucune conformité rétroactive. Échecs préparation image/pile conservés en snapshots; stderr originaux seulement transcript outil, pas faux logs archivés. Baseline RED porte sur stub entier; mutants ciblés portent la causalité limitée.

## Publication et vérification séparée
Aucun patch source ni intégration; AnimateItem et DoorControl non activés, pas de GREEN global. GetChange public courant : actual-TU autonome 1440 cas par mode normal/strict vérifié fraîchement, zéro divergence et stderr runtime vide; logs dans le handoff publication, pas gameplay et pas répétition de la matrice cible. Aucun fullbuild/runtime lancé. Section nommée re808-private-animation-jump ajoutée dans conteneur historique RE803; retrait seul reconstruit tous les octets précédents. Exclusions nominatives RE808 seulement dans gardes RE807/806/805/803 après RED réel, hashes source et provenance inchangés.

## Préservation et calendrier
Sources, index, report-tech, histoires/métadonnées antérieures et suppressions utilisateur BLOCKED001/002 protégés. mutation.lock canonique bref; repo.lock parent owner857519 conservé. Aucun stage/commit/push. Paris : recherche11:25, revue11:45, owner11:55, deadline12:00; budget550s, commandes180s maximum. Frontière RE-809 planned-not-proven : preuve nouvelle seulement, aucune répétition des matrices fermées ou activation anticipée.
