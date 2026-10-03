# RE815 — ObjectObjects : entrée authentique, registration bornée

Statut **REGISTRATION_PREFIX_PASS_NATIVE_REQUIREMENT_RED**. Revue privée indépendante
**PASS_scoped**, aucune approbation de publication/intégration ou production.
Verdict privé : `91a64b4efe5c16fbe416806feb46073a5bccd63404c43f2c341f428ef9dc5460`.
Manifest privé : `0784525f0d9eb2cd020554acf15bf23d0b79a745b5032574ebf3d4d8ffb173e8`,
33 entrées vérifiées individuellement avant émission.

## Preuve et limites

Entrée binaire authentique ObjectObjects attribuée par le caller InitialiseObjects
et son ordre Baddy/Object/Trap/Hair/Effects; ce caller entier n'est pas exécuté.
Une fixture synthétique RAM 2MiB, placement authentifié hérité, sans extraction disc fraîche.
Le préfixe produit lui-même t7/t8/t9, **aucune injection**; seuls GP/SP/RA sont construits.
Le producteur réel choisit une base différente du framework construit RE814 :
la comparaison historique n'est pas une certification rétroactive de celui-ci.
14 slots génériques enregistrés, 601 visites hooks (pas instructions retirées),
stop avant la famille suivante; **pas de retour ObjectObjects cible complet ni startup**.
Oracle indépendant des 14 records, 896 octets; 896 corruptions mono-octet rejetées,
70 stores génériques reconstruits. Égalité RAM entre replays ≠ oracle indépendant wholeRAM,
ni couverture des stores transitoires ou preuve hardware.

Vrai GAME/SETUP.C inchangé, i386 normal et ASan/UBSan failfast :
14 slots poison restent inchangés après retour natif. **Requirement RED exit1**
dans les deux modes; **characterization PASS exit0** dans les deux modes.
Ces assertions sont différentes : aucun GREEN comportemental natif, aucune correction.
Stderr des quatre runtimes vide; warnings legacy de compilation conservés.
Cible loaded=1/autres flags zéro versus natif bytes poison et pointeurs typés :
entrées sensibles différentes, frontières préfixe cible/retour natif différentes;
aucune équivalence universelle. InitialiseGenericDoor et DoorControl seulement enregistrés,
jamais invoqués. Aucune composition item/allocation/floor/navigation dans RE815.

## Progression et frontière

RE813 original FAILED et RE814 original FAILED/noncertifié restent inchangés.
RE814 demeure un checkpoint historique; RE815 avance son objectif d'entrée productrice,
pas l'objectif startup. BLOCKED-006 existant reste applicable; BLOCKED-001/002 supprimés
restent supprimés. Aucun patch production/source, activation, fullbuild, runtime jeu,
gameplay, startup ou GREEN global. Le générateur ne rejoue pas les preuves privées :
RED/GREEN de publication metadata est distinct du requirement natif RED.

Prochain objectif : **RE816 composition privée déjà exécutée, revue indépendante pending**.
Ce n'est ni une preuve approuvée ni une publication RE816; ne pas inventer de RE817.

## Tracker

- [x] Contrat publication testé RED avant générateur, log archivé.
- [x] Approval privé exact hashes et 33 pièces vérifiés; publication metadata seulement.
- [x] Functiondoc/CSV/story et dashboard versionné append-only avec inverse exact.
- [ ] Revue indépendante distincte des hashes de cette publication par le parent.
- [ ] Revue indépendante RE816; aucune intégration ou startup autorisés.
