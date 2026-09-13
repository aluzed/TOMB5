# RE-770 — SOURCE GetHeight → item.floor

## Tracker

- [x] Preuve source et revue privée lues, attribution séparée.
- [x] RED documentaire observé avant story et dashboard.
- [x] Publication metadata-only ; source de production inchangée ; code_change_readiness=blocked.
- [x] revue finale de publication PASS au 13 septembre 2026 à 10:09 Europe/Paris, distincte du PASS privé.
- [ ] Collision amont et exécution cible GetHeight non établies.

## État et overview actif

État actif au 13 septembre 2026, Europe/Paris. Après RE-769 : alternative SOURCE GetHeight → item.floor caractérisée, PASS privé borné sur cette configuration locale. Le provider a refusé la collision binaire ; cette unité alternative n’est ni une correction ni une preuve de la cible. La cible historique non exécutée reste une limite explicite : RE769 reste le stop à l’entrée GetHeight. Les mentions actives datées des sections antérieures sont historiques ; ce nouvel overview actif et le handoff actif ci-dessous donnent l’état courant sans les réécrire.

63 observations : 21 appels directs GetHeight et 42 retours normaux complets UpdateLaraRoom, dont 21 alias et 21 non-alias. Matrice synthétique : sept géométries, trois points, trois modes. Base plate, TILT nul, quatre pentes signées/asymétriques et sentinelle anticipée ; bords locaux et coordonnées non-alias discriminants. La cellule issue de item est conservée, les coordonnées de pente issues de Lara sont employées : plat 3072 ; premier point asymétrique 3515 en direct/alias et 4364 en non-alias ; sentinelle -32512 stockée dans le long floor de l’item, pas dans l’autre Lara. Le trigger entrant reste conservé sur sentinelle et les quatre globaux scalaires sont remis à zéro ; sinon trigger nul sur ces fixtures.

TU entières actuelles SPEC_PSXPC_N/GETSTUFF.C et SPEC_PSXPC_N/COLLIDE_S.C compilées séparément, puis liées au support de données, sans wrapper, sans stub GetFloor/GetHeight/UpdateLaraRoom/ItemNewRoom, sans suppression des symboles non résolus. Élimination des sections inutilisées : pas de build du jeu entier. Deux processus auteur avec stdout identique, un seul build auteur ; une compilation fraîche et un processus natif propres au reviewer. Le retour short direct et le stockage long après retour complet sont des observables différents, pas une capture du registre intermédiaire du consommateur.

## Preuve consommée et attribution

Auteur : build/reverse/autonomy-20260913/getheight-native/HANDOFF.md. Son audit/rejeu était du même worker, pas une revue indépendante. Revue ultérieure : build/reverse/autonomy-20260913/getheight-review/RAPPORT.md, getheight-review/verdict.json et getheight-review/delivery-verification.json. Le reviewer délégué distinct a recompilé les TU inchangées et le harness byte-identique, exécuté quatre méthodes du contrat sur sortie fraîche, puis réalisé une reconstruction indépendante sans import de l’oracle auteur. Quatre méthodes ne signifient pas quatre cas : elles consomment les 63 observations.

Reconstruction entière des deux ITEM_INFO : 288 octets avant et après chaque observation, à partir des initialisations et du layout mesuré indépendamment, sans recopier les buffers observés. Sortie ordonnée entière égale à l’attendu indépendant et aux sorties auteur. Seul le champ floor du premier item change en modes consommateur ; aucun octet ne change en direct. Les autres zones : memcmp du harness seulement (salle, cellules, floor-data, lara, file, support et pointeurs), inspecté et exécuté par reviewer ; pas de reconstruction brute indépendante de ces zones, pas de comparaison mémoire globale entière ni de traçage des stores transitoires.

Parent : selon le contexte explicite de la délégation actuelle et le ledger lu build/reverse/autonomy-20260913/parent-review-verification.json, lecture du handoff, rapport, verdict et delivery-verification ; 49 hashes de livraison vérifiés sans mismatch à 09:56:19 le 13 septembre 2026. Aucun horaire de début/fin de replay n’en est déduit : aucun replay privé ni audit buffers parent. Le publisher : aucun rejeu privé, aucune recompilation native, aucun audit des buffers privés ; uniquement lectures des pièces nommées et tests publics documentaires/régression. Le PASS privé ne constitue pas une revue de ces nouveaux fichiers : revue finale de publication PASS au 13 septembre 2026 à 10:09 Europe/Paris, distincte du PASS privé.

## Limites source, montage et comportement

Configuration locale GCC 13.3.0, C++17, -m32 -O0, char signé, little endian, long/int/pointeurs 32 bits et short 16 bits. PSX_VERSION=1 et PSXPC_TEST=1 ; dépendances générées par TU, headers non tous épinglés avant le premier compilateur, bibliothèques runtime non hermétiques. Le shift gauche négatif est non portable et potentiellement indéfini en C++17 ; le shift droit négatif est qualifié par la configuration mesurée. Les résultats sont empiriques pour ce compilateur et ces flags, pas une garantie de langage. Pas d’autres optimisations ; pas de sanitizer.

RED setup/contrat source historique : native.log absent, FileNotFoundError dans setUpClass, exit 1, zéro méthode exécutée ; pas un RED comportemental de production. Contrat écrit avant harness et inchangé, première exécution géométrique verte, aucune correction source. Trois corruptions en mémoire des observations détectées par auteur ne sont pas des mutants source compilés ni des contrôles rejoués par reviewer. L’audit auteur initial attendait à tort 296 au lieu de 288 octets : incident d’audit conservé, pas bug du jeu. Première compilation de l’outil layout reviewer échouée pour includes manquants, corrigés dans cet outil seulement avec nouveau label ; harness et TU inchangés.

Domaine : salle inchangée ; ItemNewRoom non exécuté bien que lié. Pas de porte, pit/sky, triangle, callback, overflow short, coordonnées extrêmes, données authentiques. Y constant : pas de preuve discriminante indépendante de son forwarding. Sélection de cellule discriminée par la géométrie témoin, pas instrumentée dans le consommateur. Non-alias atteignable en jeu non établi ; pas de gameplay, pas de matériel, pas d’équivalence cible ni universelle. source de production inchangée ; code_change_readiness=blocked.

Gardes et anciennes preuves non rejouées ni altérées : gardes historiques inchangées. Les échéances antérieures ne sont pas renouvelées par cette publication. L’autorisation courante d’autonomie jusqu’à 11h Europe/Paris, avec pas de preuve longue à 10h30 et clôture à 10h45, ne démontre pas qu’une prochaine preuve a commencé. Au snapshot de publication avant revue : aucun stage, commit ou job ; rapport-tech non suivi préservé volontairement sans lecture de contenu.

## Tests publics et archives

Racine ignorée exclusive build/reverse/autonomy-20260913/re770-publication/ : red.log, green.log, suite.log et ledgers JSON exclusifs avec commande exacte, cwd, environnement, horaires, exit, durée processus monotone, hashes publics avant/après et hash de log, persistés immédiatement. Lectures exploratoires/préflight dans le transcript outil, pas présentés comme invocations de preuve. Le contrat public lit story et seule section RE770, sans lire/importer les preuves privées. Retirer entièrement la nouvelle section restaure tous les bytes HEAD du dashboard, y compris l’historique et les fermetures.

RED documentaire observé à 09:58:26 Europe/Paris : exit 1, un échec attendu pour story absente et un test historique réussi en 0,08 s pytest. La suite publique est l’exacte sélection argv de RE769/suite.json avec seulement le nouveau test ajouté et une basetemp neuve sous la présente racine. Les assertions de texte vérifient la publication, pas la vérité historique de la preuve privée. GREEN observé : 09:59:55.633835–09:59:55.898766 +02, exit 0, 2 tests réussis en 0,06 s pytest. Suite publique exacte RE769 avec seul test RE770 ajouté : 10:00:02.622883–10:01:02.268967 +02, exit 0, 3763 tests réussis en 59,21 s pytest (59,645617 s processus). Test byte-identique entre RED et GREEN. Résultats inscrits après exécution ; revalidation finale après inscription archivée séparément dans final-suite.json et final-suite.log, sans annoncer son résultat à l’avance. Les fichiers publics étaient alors figés pour revue ; résultats finaux et manifeste de ce snapshot restent dans le HANDOFF privé.

## Handoff

Après RE-770 : PASS privé SOURCE borné publié metadata-only ; revue finale de publication PASS au 13 septembre 2026 à 10:09 Europe/Paris. Prochaine vraie preuve : collision amont/cible GetHeight, notamment préconditions alias/caller puis exécution et usage du retour sur un état cohérent. Recherche proposée, non commencée dans cette unité ; ne pas déduire de l’alternative source que la frontière cible a avancé. Ce handoff actif ne lance pas cette recherche et n’autorise pas de patch.
