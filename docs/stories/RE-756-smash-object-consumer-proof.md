# RE-756 — SmashObject : preuve consommateur bornée

## Tracker

- [x] Préflight 9 septembre 2026, 13:52:57 Paris ; HEAD et arbre suivi vérifiés, rapport interdit non ouvert/non modifié/non stagé.
- [x] Preuve privée, revue indépendante PASS et preuves parent lues avant publication.
- [x] RED documentaire observé avant les docs : story absente, 1 échec en 0,07 s, exit 1, 13:54:09.228702–13:54:09.498551 Paris.
- [x] Caractérisation privée bornée acquise, NON-ÉQUIVALENCE conservée explicitement.
- [x] GREEN public puis suite exacte RE-755 + RE-756 réussis ; détails observés ci-dessous.
- [ ] Correction du wrapper et domaine élargi non exécutés dans cette unité.

## Résultat et progression

PASS de caractérisation bornée ; NON-ÉQUIVALENCE de SmashObjectControl. 12 cas synthétiques : 6 appels directs SmashObject égaux, 6 wrappers dont 4 divergences aux indices 1/2 ; indice zéro égal et masquant le défaut. Chaque cas compare intégralement B=32, I=432, F=48 octets et les événements ordonnés. Dans les quatre divergences, I diffère de 12 octets ; B de 2 octets seulement si BOX_LAST présent ; F identique partout. Consumer borné caractérisé, wrapper défectueux non corrigé : aucun correctif source, aucune équivalence globale acquise.

## Cause et exécution

La vraie TU GAME/OBJECTS.C a été fraîchement compilée i386 avec host.cpp : douze processus natifs et douze exécutions cible par replay, deux méthodes unittest PASS, pas douze tests unitaires. Le wrapper source décale à gauche puis convertit en short ; le binaire host appelle SmashObject avec zéro pour ces indices. La cible conserve l’indice signé inchangé, delay slot compris. Trois services, SoundEffect, ExplodingDeath2 et RemoveActiveItem : trois doubles ABI sans effets mémoire, côté cible et natif ; aucun corps authentique de ces services exécuté. Retour sentinelle, pile et liens vérifiés ; budget de 1000 visites par cas et timeout une seconde.

## Attribution indépendante et parent

La revue indépendante review/review.json et review/review.md conclut PASS de caractérisation, pas correction : replay frais du 9 septembre 2026 à 13:47:17–13:47:19 Paris, exit 0, compilation réelle puis audit indépendant des buffers et du wrapper, exit 0. Le parent a exécuté séparément avant publication : parent-replay.json consigne 13:46:23–13:46:25 Paris, exit 0, deux méthodes unittest ; parent-audit.json porte passed=true et douze lignes. Le JSON de cet audit confirme passed=true ; son exit processus et son intervalle propre ne sont pas archivés dans ce fichier. Le handoff initial sans revue/parent est antérieur à ces validations. Le rédacteur lit ces preuves : aucun rejeu privé dans cette publication metadata-only.

## Provenance et instrumentation

HEAD prépublication 562ed7cd55fe6c1e921d543e9893717a15ed9009, 314 fichiers sources projet scellés ; dépendances projet des deux TU vérifiées séparément par la revue, en-têtes système et toolchain non scellés, environnement non hermétique. Boot du disque et payload Ghidra authentifiés indépendamment. Ghidra frais chez le worker, hérité et non relancé par la reprise, le reviewer ou le rédacteur : END_RE756 présent, exit historique non retrouvé ; aucun exit 0 headless revendiqué. 1084 visites de hooks incluent 32 entrées et 32 delay slots des doubles : pas des instructions retirées. Les 96 stores inférés préexécution sont bornés, pas une trace mémoire native. Comparaison des 2 Mio RAM avant/après dans le probe rejoué ; images RAM non archivées, donc pas de comparaison indépendante a posteriori de ces images. Égalité finale seule insuffisante pour exclure les écritures transitoires restaurées, pas de contrôle général des lectures.

## Reprise et limites

Le snapshot préalable est conservé ; interruption/timeout puis recovery aboutie, pas verdict d’échec de la preuve. Le hook mémoire perturbait empiriquement le delay slot sous Unicorn ; il a été remplacé par stores inférés et contrôle RAM finale, sans assouplir les assertions comportementales ni prétendre diagnostiquer le bug interne de l’émulateur. Domaine : indices 0/1/2 seulement, inactif corrélé à l’indice 1, BOX_BLOCKED initialement présent dans tous les cas, BOX_LAST présent/absent. Pas de produit cartésien complet indice/état/flags, indices négatifs et extrêmes exclus. Fixtures synthétiques, un room, six secteurs, quatre boxes ; pas de sauvegarde réelle, de caller runtime réel, de matériel ou de chargeur complet. pas de sûreté mémoire générale ; pas de preuve gameplay ; aucun sanitizer revendiqué. Les références statiques candidates ne prouvent pas tous les appels indirects.

## Borne et prochaine unité

Gardes de HEAD/arbre/date propres prépublication, gardes historiques inchangées. Après publication ne pas relancer, assouplir ou resealer le replay historique. Autorisation courante du 9 septembre 2026 : recherche jusqu’à 23:25 Paris, livraison jusqu’à 23:45 Paris. Prochaine unité corrective privée sous cette autorisation, non exécutée ici : RED réel sur la vraie TU avant patch, indices et états découplés, flags indépendants BOX_LAST/BOX_BLOCKED, correction minimale sur copie privée puis GREEN des buffers complets et événements et nouvelle revue indépendante. Aucun nouveau GO demandé tant que la borne courante couvre cette unité ; aucune exécution corrective ni patch de production. Aucun staging ou commit/push au moment de la rédaction ; livraison autorisée après revue finale. Aucun reset/clean ou nouveau job.

## Validation publique

Le test public contrôle la story et seulement la nouvelle section RE-756, avec le handoff actif séparé ; il ne lit ni n’importe de preuve privée. Ancres et sections historiques préservées, générateur non relancé volontairement. La suite est exactement celle de RE-755 augmentée du nouveau test ; les tests émulateur préexistants restent découverts par leur dossier. GREEN documentaire : 1 test réussi en 0,05 s, exit 0, 13:55:36 Paris. Suite exacte RE-755 plus RE-756 : 1 217 tests réussis en 51,19 s, exit 0, intervalle 13:55:44.938581–13:56:36.403438 Paris (durée processus 51,464772 s). Revalidation documentaire après insertion des résultats : 60 tests réussis en 0,56 s, exit 0, 13:56:59 Paris (publication/final.log).

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/reverse/test_re756_smash_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py -q
```

Cwd `/var/www/projects/TOMB5`. Journaux immédiats sous `build/reverse/autonomy-20260909/re756/` : `publication/red.log`, `publication/green.log`, `publication/suite.log`, `publication/final.log`, `publication/commands.json`. Chaque commande a son JSON start/end/exit et sa sortie conservée ; le ledger est mis à jour immédiatement après chaque fin. La revalidation documentaire a suivi l’insertion des résultats observés ; un dernier passage final-text.log contrôle aussi la mention de cette revalidation. Les tests documentaires prouvent la cohérence publiée, pas une nouvelle exécution binaire.

## Handoff

Après RE-756 : caractérisation publiée, wrapper NON-ÉQUIVALENT, aucun correctif source. Prochaine unité corrective privée bornée selon les conditions ci-dessus, non exécutée ici. Livraison limitée à cette story, la nouvelle section dashboard avec date/handoff et le nouveau test public ; revue finale de publication à effectuer par le parent.
