## Progression vérifiée du 2026-10-28

PORT-006 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Sauvegarde rapide de port : F5 écrit TOMB5.SAV (magic T5P2, savegame_info, position/rotation/salle/animation de Lara, checksum FNV-1a) ; F6 au titre recharge et reprend. Preuve réelle : partie Rome, marche, F5 room 2 X46592 Y0 Z35826, fermeture normale exit 0, relance, F6, application de la même position et scène identique ; exits 0. Limites : RestoreLevelData non implémenté, les objets/portes/pickups du niveau repartent de l'état initial, seuls Lara et son inventaire/santé sont restaurés ; pas de carte mémoire PSX, pas de chargement en jeu, pas de slots multiples, écriture non atomique. Preuves privées : build/porting/port006-20261028 et port006b-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

# PORT-006 — Sauvegarder et reprendre après relancement

[Tracker](README.md) · [Tableau HTML](index.html#PORT-006)

Status: Blocked

Priorité : P1

Motif : Recette intégrée bloquée tant que PORT-005 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-005

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Retrouver une partie sauvegardée après fermeture complète de l’application.

## Faits existants — base eac6d930

LoadGame/SaveGame existent côté PSXPC_N ; RestoreLevelData est un stub dans GAME/SAVEGAME.C. La présence des menus ne vaut pas restauration du monde. Le stockage carte mémoire passe par EMULATOR/LIBMCRD.C.

## Portée

Un emplacement de sauvegarde local, cycle complet save/exit/relaunch/load, état de Lara et d’un objet représentatif.

## Exclusions

Compatibilité universelle avec sauvegardes originales, migration de versions, synchronisation cloud et tous slots exclus.

## Tâches — implémentation non commencée

- [ ] Définir un état avant/après et isoler le stockage de test des sauvegardes utilisateur.
- [ ] Caractériser sérialisation, restauration et taille des buffers avant correction.
- [ ] Faire le cycle avec processus neuf puis tester annulation et fichier invalide sur copies.

## Critères d’acceptation futurs

- [ ] Après relancement, niveau, position, santé, inventaire et état d’un objet correspondent aux valeurs sauvegardées.
- [ ] Un déplacement après sauvegarde n’est pas confondu avec l’état restauré.
- [ ] Annulation/fichier invalide n’écrasent pas la sauvegarde valide et produisent une réponse compréhensible.

## Validation et capture attendues

Captures privées avant/après, comparaison structurée des états et hashes des fichiers privés ; aucune sauvegarde originale en Git.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Format, checksum, validité des chemins et logique de restauration ; aucune corruption réelle prétendue sans reproduction.

## Estimation indicative

5–20 jours-personne exploratoires ; compatibilité externe à estimer séparément. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `SPEC_PSXPC_N/LOADSAVE.C:119` — LoadGame.
- `GAME/SAVEGAME.C:52` — sgRestoreGame et RestoreLevelData.
- `EMULATOR/LIBMCRD.C:78` — Stockage carte mémoire.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
