# RE-781 — contrat callback, actual-TU

Invocation publique (répertoire output absent) :

    python3 tests/reverse/fixtures/re781/run_test.py --root . --source SPEC_PSXPC_N/GETSTUFF.C --output build/reverse/re781-manual-new

288 cas synthétiques, deux consommateurs (GetHeight direct, UpdateLaraRoom réel), deux bridges ordonnés, inhibition indépendante, trois bases et trois hauteurs de requête. GETSTUFF.C, COLLIDE_S.C et OBJECTS.C entiers sont compilés avec les headers normaux, Linux/i386 et macros PSX_VERSION/PSXPC_TEST. Liaison avec élimination des sections inutilisées, sans ignorer les symboles non résolus. Le tableau entier des trois items et les globals énumérés sont contrôlés.

Le vrai BridgeFlatFloor déclare long/long*, le slot int/int*. Un adaptateur typé explicite et un temporaire long évitent casts incompatibles et lecture de l'output non initialisé de la baseline. Ce test ne valide pas la registration native réelle, les autres callbacks, tous backends ou le gameplay. Le temporaire sentinelle borne le domaine : les hauteurs testées ne prennent pas LONG_MIN.

La baseline a 114 échecs comportementaux sur 288 cas ; la correction bornée a zéro échec. Ce ne sont pas 288 tests pytest. Le test pytest compile production et archive ses logs sous build ignoré. Les probes cible privés apportent l'attribution séparée ; le harness public ne contient aucun asset ni donnée extraite.

UBSan échoue sur un décalage négatif préexistant de GetFloor ; ce défaut reste non réparé, aucun PASS sanitaire global. Le runtime relink acquis ne visite pas le callback dans son témoin et ne prouve pas l'effet gameplay. Voir la story RE-781 pour les preuves et limites.
