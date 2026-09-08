# RE-746 — Allocation et lecture sectorielle : contrats différentiels

## Statut et progression

**Preuve comportementale bornée acquise et revue. Aucune reconstruction de production justifiée sur le périmètre comparé.**

- [x] Handoff RE-745 consommé ; nouvelle unité commencée le 8 septembre 2026 à 23 h 05 Paris, sur le HEAD de sa publication.
- [x] Projet Ghidra inspecté réellement en lecture seule, après contrôle des processus et verrous ; sortie réussie et marqueur final archivés.
- [x] Boot, payload, base du bloc, initialisation GP et alias de pile/tas SDK recoupés ; aucune normalisation globale arbitraire.
- [x] Allocateur cible et lecteur sectoriel exécutés face aux vraies unités hôtes, avec conservation d’état entre opérations.
- [x] Trois tests privés réussis après RED de l’API de recherche ; seconde exécution différentielle avec ASan/UBSan réussie.
- [x] Story, tracker et dashboard de reconstruction actualisés avec test de publication d’abord RED.
- [x] Revue indépendante favorable ; parent : trois tests privés, passage sanitized et 1 200 tests publics réussis.
- [ ] Transaction complète de chargement, propagation des erreurs et durée de vie des allocations depuis de vrais appelants.

## Ce qui est nouveau depuis RE-745

RE-745 exécutait le chargeur et ses services sur une seule trajectoire de chargement réussie, sans comparaison des services avec les unités hôtes. RE-746 quitte le texte : les contrats d’initialisation du tas, d’épuisement sans mutation, de libération LIFO et de progression sectorielle sont maintenant comparés directement entre instructions cibles et code hôte.

La décompilation fraîche couvre `init_game_malloc`, `game_malloc`, `game_free`, `DEL_CDFS_Read`, `FILE_Length` et `FILE_Load`, avec leurs dépendances. Les globales GP inventées par le décompilateur ne sont pas prises pour des adresses fiables : les opérandes sont recoupés avec le démarrage. Les instructions et delay slots confirment notamment le retour nul d’allocation insuffisante, sans mise à jour du descripteur.

**Unités hôtes effectivement compilées et exécutées : `SPEC_PSXPC_N/MALLOC.C` et `SPEC_PSXPC_N/CD.C`.** Elles sont compilées séparément avec leurs en-têtes normaux, pas copiées dans le harness. Le code de production reste inchangé.

## Résultats

| Contrat comparé | Résultat |
|---|---:|
| Séquences d’allocation indépendantes | 5 |
| États allocation/remise à zéro/libération et tas complet comparés | 65 |
| Allocations insuffisantes, retour nul et descripteur inchangé | 10 |
| Séquences de lecture indépendantes | 8 |
| Appels de lecture comparés | 11 |
| Attentes occupées du lecteur parcourues | 11 |
| Écarts d’état, de tas, de tampon ou d’événements SDK comparés | 0 |

Les préfixes de script synthétiques couvrent un tas vide, des débuts non alignés, un tas presque plein et un tas plein. L’initialisation conserve exactement le préfixe et remet à zéro le reste. Les allocations sont arrondies, les libérations ne nettoient pas les octets, et une nouvelle initialisation efface les écritures synthétiques hors préfixe. Les demandes nulles, l’allocation exacte de l’espace disponible et les échecs sont inclus. Les cinq séquences comparent tous les octets du tas à chaque étape, pas seulement ses compteurs.

Le lecteur couvre les transferts nuls, partiels, exactement sectoriels et mixtes, ainsi que les transitions de mode et les attentes occupées. **Deux petites lectures successives avancent chacune d’un secteur entier ; elles ne constituent pas un flux d’octets contigus.** Les données attendues sont extraites directement des secteurs ISO, indépendamment du tampon temporaire du lecteur. Les retours, curseurs, changements de mode, événements SDK et tampon complet entourant la destination concordent avec l’hôte. Ce comportement est déjà présent dans le source ; aucune correction n’est nécessaire.

Le second passage compile les mêmes unités avec ASan/UBSan et rejoue le différentiel : aucune divergence ni diagnostic d’exécution. La compilation conserve un avertissement préexistant de conversion de chaîne constante dans `InitNewCDSystem`, fonction non appelée par ce harness.

## Attribution et limites

- Même boot US PSX que RE-745, extrait et comparé à celui de l’ISO ; empreintes privées. Les octets de chaque entrée d’instruction rencontrée sont authentifiés avant traitement. Aucun patch d’instruction. Aux frontières SDK déclarées, le corps n’est pas exécuté : le contrôle de ses octets d’entrée n’est pas une preuve du SDK.
- CPU et RAM restaurés entre séquences indépendantes ; conservés entre opérations d’une séquence. Tas, pile, préfixes et état de lecteur synthétiques. Les lectures utilisent de vrais secteurs ; les tailles sont des cas construits, pas une nouvelle trace d’appelants.
- `CdControlB`, `CdRead`, `CdReadSync` et `VSync` sont des frontières explicitement modélisées. Les helpers cibles de position et de copie sont exécutés. Le modèle hôte de position est distinct de ces instructions, mais les doubles CD communs ne constituent pas un oracle matériel indépendant.
- **Pas de preuve matérielle**, de démarrage complet, d’interruptions, de concurrence ou d’erreurs de transfert. La comparaison du tampon entourant la destination ne prouve pas une sûreté générale de toutes les écritures mémoire.
- Allocation : tailles non négatives bornées, préfixes valides et libérations LIFO valides. Entiers débordants, tailles négatives et libérations invalides exclus ; aucune nouvelle politique de rejet n’est inventée.
- Comparaison hôte avec `DEBUG_VERSION=0` et **`DISC_VERSION=1`**. Le **backend fichiers par défaut** est distinct : CMake désactive le mode disque. Les chemins `FILE_Length`/`FILE_Load` sont inspectés, mais pas comparés par le nouveau harness. Leurs erreurs et leur ABI hôte ne sont pas déclarées équivalentes.
- Les variantes historiques `SPEC_PSX/MALLOC.C` et `SPEC_PSXPC/MALLOC.C` ont été lues ; leur variable de retour non initialisée hors debug n’est pas celle de l’unité hôte active, qui initialise déjà le retour nul. Elles ne sont ni exécutées ni modifiées ici.
- Le RED privé démontre l’absence initiale de l’API de preuve, pas un défaut de production. Les tests de caractérisation concordants n’autorisent pas à annoncer une reconstruction supplémentaire.

## Reproduction et preuves privées

Tous les octets, secteurs, adresses, instructions, sorties Ghidra et harness restent dans `build/reverse/autonomy-20260908/re746-services/`, ignoré. Fichiers principaux : `InspectServices.java`, `headless.log`, `ghidra-services.txt`, `services.py`, `host.cpp`, `test_services.py`, `allocation.json`, `reader.json`, `summary.json` et variantes `-sanitized`.

```sh
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260908/re746-services/test_services.py
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260908/re746-services/services.py --sanitize
python3 -m pytest tests/emulator tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

Le probe vérifie le HEAD de départ RE-746 et expire le 8 septembre à 23 h 45 Paris. La garde locale ne détecte que les modifications non indexées des deux sources : elle ne couvre ni les changements déjà indexés ni les en-têtes. La revue a vérifié séparément l’absence de dérive actuelle et un index vide ; cette limitation ne doit pas être confondue avec une protection exhaustive. Il réutilise uniquement le décodeur ISO privé de RE-745, sans exécuter ses gardes historiques ni modifier ses preuves. Une réexécution après livraison ou expiration exige une adaptation explicitement autorisée conservant cette provenance. Ce n’est pas une CI autonome sans assets privés.

Revue indépendante archivée dans `review.md` : trois tests privés et passage sanitized rejoués, huit sorties JSON identiques aux archives. Les exécutables existants ont été réutilisés, sans recompilation fraîche par le reviewer. Le parent a confirmé les mêmes résultats et **1 200 tests publics réussis**. La vérification préalable des processus/verrous est rapportée par l’auteur mais non établie par les seuls fichiers de preuve inspectés par la revue.

## Handoff

Ne pas prolonger ces résultats par une autre matrice de tailles isolées. **Prochaine hypothèse cohérente : une transaction réelle de chargement de module/niveau reliant sélection/positionnement, allocation, lecture et relocation, avec contrôle des bornes et de la durée de vie des blocs depuis son appelant.** RE-735 fournit une attribution antérieure du producteur et de la relocation, RE-745 celle des services fichiers ; les séquences RE-746 apportent leurs contrats locaux mais pas cette intégration. Choisir une reconstruction seulement si ce lien révèle un écart observable dans la vraie unité hôte.

L’absence d’écart local n’est pas un obstacle global à la recherche. L’inventaire terminal RE-702/731 et son dashboard historique restent inchangés. Aucun commit ni push effectué par cette unité.
