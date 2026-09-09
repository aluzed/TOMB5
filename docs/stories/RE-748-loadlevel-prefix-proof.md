# RE-748 — Preuve bornée du préfixe LoadLevel

## Statut et progression

**Preuve bornée acquise et revue ; aucun correctif de production justifié.** Publication metadata-only, sans modification des sources ni des contrats historiques terminaux.

- [x] Handoff RE-747 et preuves privées RE-748 consommés.
- [x] Tests privés d'abord RED (API/module absent), puis GREEN cible et vraie TU hôte.
- [x] S_LoadLevelFile, préparation RE-747, dispatch indirect et préfixe LoadLevel exécutés avec CPU/RAM/curseur conservés, sans réinitialisation entre ces étapes.
- [x] Vrai LoadSoundEffects exécuté jusqu'au retour ; arrêt avant la suite persistante.
- [x] Revue indépendante favorable sous correction de formulation ; corrections incorporées ci-dessous.
- [x] Vérification parent le 9 septembre 2026 à 07:51 Europe/Paris : 3 tests cible et 1 test host réussis, avec compilation fraîche.
- [x] Test public écrit d'abord : RED observé sur story absente ; publication story/dashboard, puis GREEN vérifié.
- [ ] Preuve des allocations frames puis roomInfo et des premières reconstructions de pointeurs.
- [ ] Retour final du chargeur, ROOMLOAD.C complet et frontières matérielles.

## Constats bornés

Une seule trajectoire normale Name=0, avec état initial synthétique, utilise les secteurs authentiques de l'ISO. Le boot et le module sont authentifiés ; la relocation réelle est comparée sur toute l'image à un calcul indépendant des 263 entrées et quatre catégories. Les instructions rencontrées sont authentifiées contre le boot ou l'image relocalisée attendue ; aucune instruction n'est patchée. Les compteurs du probe sont des **visites du hook**, y compris interceptions et arrêt, **pas des instructions exécutées** ; aucun compteur de retraite CPU n'est revendiqué. L'ISO entier n'est pas nouvellement certifié.

| Observation depuis l'entrée LoadLevel | Résultat |
|---|---|
| En-tête conservé et comparé intégralement | 228 octets |
| Audio authentique, non effacé ni contourné | 4 effets sonores ; bloc de 7 616 octets |
| Temporaires | 3 allocations ; 3 libérations par taille |
| Entrées disque | 5 lectures : en-tête, table audio, bloc audio, deux textures |
| Textures | Deux buffers de 262 144 octets et rectangles concordants |
| Progression sectorielle arrondie par appel | 262 secteurs |

Chaque plage utile lue est comparée intégralement aux secteurs ISO extraits indépendamment du lecteur cible. Les libérations audio suivent l'ordre table puis bloc : il s'agit de free par taille, pas de free(pointer). Le descripteur cible vide est restauré après les temporaires ; l'audit contrôle ses trois composantes et invariants intermédiaires. Ces tailles alignées ne prouvent pas tous les cas de durée de vie ou de sûreté mémoire.

Le différentiel original compare les tailles et le **compteur d’octets utilisés** lors des allocations/libérations, **pas un descripteur host complet** ni les adresses absolues des pointeurs. Il compare les cinq buffers utiles lus, la progression du curseur, les deux buffers/rectangles graphiques, la séquence draw, les appels SDK SPU et la table audio. Les champs contrôle/sélecteurs étaient confrontés au header/aux constantes, et non initialement au résultat cible. L'observateur indépendant complète pour ce seul cas la comparaison du bloc transmis au double SPU, de la globale d'adresse synthétique, du contrôle final nul et des sélecteurs décodés. Aucun « zéro écart sur tous les états » n'est déduit.

## Vraie TU hôte et frontière d'arrêt indispensable

Compilation fraîche de **GAME/SETUP.C** comme TU distincte avec ses en-têtes normaux, ABI **32 bits**, DISC_VERSION=1, DEBUG_VERSION=0, PSX_VERSION=1 et PSXPC_TEST=1. ELF i386, symboles LoadLevel/LoadSoundEffects et désassemblage contrôlés par la revue ; aucune copie de ces fonctions dans le harness. Les services allocation/CD/GPU/SPU du host restent des doubles : ce n'est pas une nouvelle comparaison des TU MALLOC.C/CD.C ni de ROOMLOAD.C.

La cible s'arrête par hook à la première instruction suivant le retour du **troisième free**, avant son exécution et avant les écritures/allocations persistantes. Côté host, une **exception** dans le double game_free arrête après mise à jour de l'état, sans retour normal de LoadLevel. Le lien utilise **--unresolved-symbols=ignore-all** pour les dépendances non atteintes : le désassemblage confirme des accès absolus nuls **immédiatement après** cette frontière. Ce binaire n'est pas une application complète utilisable ; résoudre les dépendances avant toute extension de l'arrêt est impératif.

Deux warnings historiques extern-initialized subsistent. Le narrowing de données historiques a nécessité l'option locale -Wno-narrowing, sans modification de la TU. Aucun sanitizer dans cette unité.

## Doubles et limites

**Pas de preuve matérielle**, de boot complet ni d'équivalence complète du chargeur. CPU/RAM initiaux, pile, tas, tampon graphique, mode normal et Name=0 sont synthétiques. Une nouvelle instance cible est créée pour chaque rejeu indépendant ; la continuité dans une exécution n'implique pas l'immuabilité de la RAM pendant les modifications normales du programme.

Les helpers graphiques RE-747 et les services SDK CD sont des doubles explicites ; CdRead transporte les vrais secteurs. Les deux commandes LoadImage ne produisent pas de pixels GPU réels. **LoadSoundEffects lui-même est le véritable helper, pas un stub**. En revanche, SpuMalloc, SpuIsTransferCompleted, SpuSetTransferStartAddr et SpuWrite sont des doubles SDK SPU : cinq appels rencontrés, succès d'allocation synthétique et transferts immédiats. La table audio est correcte sous ce contrat, pas une mesure SPU.

Ni allocateur/transfert SDK internes, DMA/MMIO, timing, interruptions, concurrence, échecs, anciens samples non vides, ni son matériel ne sont prouvés. Pas de garde générale de RAM ou des octets voisins des buffers ; « intégralement » ne concerne que les plages utiles explicitement comparées. Pas de retour final LoadLevel, de frames ou de roomInfo dans cette unité.

## Revue indépendante, provenance et vérification

La revue du 9 septembre 2026, 07:44–07:49 Europe/Paris, a rejoué les tests originaux inchangés dans un répertoire séparé : **4 tests réussis**, dont deux exécutions cible indépendantes et compilation/exécution fraîche de la TU hôte. Elle a vérifié 35 empreintes, 20 résultats/fixtures identiques et 37 fichiers originaux inchangés. Un observateur additionnel contrôle les slots retardés, champs finaux, entrée SPU complète, invariants du descripteur et arrêt. Le PASS comportemental était conditionné à la correction des compteurs et à la portée exacte des comparaisons ; ces corrections sont appliquées ici. Le rejeu parent à 07:51 est distinct de cette revue.

Les preuves restent privées et ignorées dans `build/reverse/autonomy-20260909/re748-loadlevel/` : `final-handoff.md`, `review.md`, tests cible/host, journaux RED/GREEN, résumés et artefacts de revue. Aucun octet d'asset, adresse cible, opcode ou extrait privé n'est publié. Le test public valide la publication, pas la preuve binaire.

La garde est épinglée au **HEAD prépublication** et aux empreintes de quatre dépendances historiques ; elle rejette la dérive suivie/indexée et expire le 9 septembre 2026 à 23:25 Europe/Paris. Les assertions supposent Python sans -O ; l'heure est vérifiée au début du run, pas continuellement dans le hook. Après publication, les commandes privées ne sont donc pas des replays inconditionnels : tout futur rejeu exige une **nouvelle unité explicitement autorisée**, avec provenance propre, **sans désactiver les anciennes gardes** ni modifier les probes historiques.

Publication TDD : **1 test en échec attendu (RED)** sur l'absence de cette story, puis **1 202 tests publics réussis (GREEN), en 50,56 s**, suite emulator, publications RE-747/748 et dashboard. Aucun diagnostic. Vérification publique, sans régénérer le dashboard terminal historique :

```sh
python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

## Handoff

Prochaine preuve cohérente : conserver CPU/RAM/curseur au-delà du préfixe, établir l'allocation frames puis roomInfo et leurs premières reconstructions de pointeurs, après résolution des dépendances hôtes hors préfixe. Une autre frontière utile serait le vrai allocateur/transfert SDK SPU correctement initialisé. Aucune de ces extensions n'est exécutée ici ; aucune nouvelle tâche planifiée. Livraison limitée à cette publication, après revue et vérification parent. Les contrats et gates historiques restent clos et inchangés.
