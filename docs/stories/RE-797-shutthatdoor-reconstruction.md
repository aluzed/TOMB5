# RE-797 — ShutThatDoor intégré, GREEN strictement borné

## Source concrète et résultat testé
GAME/DOOR.C contient uniquement les includes BOX.H/LOT.H et le corps ShutThatDoor acceptés, sous gate PSX_VERSION && PSXPC_TEST && defined(__i386__). La branche alternative conserve UNIMPLEMENTED; aucune autre fonction door reconstruite, aucune registration activée. Régression publique contre la TU production entière avec headers réels, liaison normale i386 et buffers synthétiques: 144/144 normal et 144/144 ASan+UBSan, aucun diagnostic dans la fixture corrigée. Le baseline stub avait 120 échecs comportementaux sur 144.

La preuve cible comporte 144 appels authentiques complets et comparaison des régions complètes. Le helper ferme floor/navbox, invalide exactement cinq LOT et ferme les meshes selon le gate primaire, même si floor est absent; fx/stopper, voisins, tails, door/item et pointeurs globaux sont contrôlés. Les pointeurs atteints sont rebased vers objets natifs réels dans la fixture; pas de suppression de symboles non résolus.

## Historique conservé, pas de réhabilitation
Le verdict RE797 original FAILED reste intact. Son claim sanitizer clean est invalide: stores short** mal alignés dans des membres pointeurs packed du harness, avec diagnostic UBSan malgré exit0. La correction est dans la fixture (affectations directes des membres), pas un défaut du candidat. La revue finale indépendante reconstruit stub, candidat exact et version gateée avec sanitizer fail-closed; la source intégrée est ensuite testée. Ni le verdict FAILED ni l’ancien claim ne sont réécrits.

## Domaine accepté
i386 backend testé seulement, floor atteint valide, blocs non-sentinelle en limites, cinq creatures valides et meshes cohérents avec troisième pointeur obligatoire lorsque le premier est présent. Aliasing arbitraire, pointeurs malformés, blocs hors limites, autres architectures, full-project link et gameplay non prouvés. GREEN helper seulement, pas de GREEN global.

## Tracker
- [x] Actual-TU RED baseline discriminant et preuve cible 144 établis.
- [x] Revue finale indépendante et source helper gateée intégrée.
- [x] Fixture publique corrigée, normal et ASan+UBSan GREEN bornés.
- [ ] Reconstruire InitialiseDoor, DoorControl, OpenThatDoor et ProcessClosedDoors.
- [ ] Activer registration puis établir runtime naturel et gameplay.

## Suite
RE-798: initialiseur privé actual-TU et fermeture des dépendances, ou preuve OpenThatDoor bornée si nécessaire. Voir BLOCKED-004-door-production-prerequisites et le manifeste metadata-only; aucun nouveau GO implicite, aucun fullbuild ou runtime ajouté par cette publication.
