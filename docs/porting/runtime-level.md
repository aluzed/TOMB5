> Suite vérifiée le 19 septembre : [commandes, transition et correctif local du regard](runtime-controls.md). Le jalon ci-dessous est conservé comme historique.

# Linux32 — première scène et boucle de retour au titre

19 septembre 2026, source jeu inchangée depuis `73faba47`. Cible PSXPC_N/i386
**provisoire**, pas acceptation définitive de plateforme. PORT-001/002/003 restent
**In progress** ; aucun Done. PORT-004 et suivants restent bloqués pour leur
recette intégrée, malgré une observation partielle de locomotion.

## Résultat vérifié, pas de correctif loader

Un nouveau processus a parcouru le chemin réel titre → New Game → niveau 1 →
avance et rotation de Lara → pause → Quit → confirmation Yes → titre, puis
fermeture normale de fenêtre. Aucun saut, appel forcé ou écriture de variable
jeu dans GDB ; entrées clavier XTest. Le loader **ne restait pas bloqué** à
60 secondes : il termine vers 71 secondes sur ce lancement. L'ancienne image de
Lara derrière des barreaux était bien un chargement, pas la scène jouable.

La récupération des preuves privées du 18 septembre a révélé des observations
postérieures au dernier résumé versionné : scène, locomotion, pause/reprise et
retour titre. Sept tests d'archives ont été rejoués avec succès ; ce rejeu ne
constitue pas quatre nouveaux lancements. Le parcours décrit ci-dessous est,
lui, un lancement frais le 19 septembre.

## Tracker — comportements réellement observés

- [x] Menu titre visible à 29 secondes ; Down/Up puis `c` sélectionnent New Game.
- [x] Entrée naturelle dans DoLevel(1), retour LoadLevel vers 70,807 secondes
  (horloge GDB ; légèrement différente de celle du recorder de captures).
- [x] Scène rendue avec Lara visible à 80 secondes ; à 85/89/95 secondes,
  caméra et position évoluent après les entrées, sans changer l'état via GDB.
- [x] `Up` 82–84 s, `Left` 87–88 s, `Up` 92–94 s : état initial
  `(46592, 0, 31232 ; rotation 0)`, final `(46181, 0, 34086 ; rotation -22791)`.
  Ces coordonnées sont des observations source, pas une preuve d'équivalence cible.
- [x] Pause visible à 98 s ; confirmation Quit à 102 s ; titre revenu à 140 s.
- [x] Fermeture WM_DELETE_WINDOW à 143 s ; **application exit 0, GDB wrapper exit 0**.
- [x] Quinze captures du lancement frais inspectées sous forme de planche contact :
  splash, titre, chargement illustré, scène, pause, confirmation et retour titre.
- [ ] Saut, interactions, combat, transitions de salles et niveau complet.
- [ ] Manette physique, sauvegarde/reprise, fidélité caméra/collision/audio.
- [ ] Build fraîchement recompilé pendant cette unité : binaire existant du
  correctif précédent réutilisé et authentifié avant lancement.

## Preuves et tests

Dossier privé : `build/reverse/autonomy-20260919-1000/unit01-0757/` (identifiant
opaque ; les heures exactes sont enregistrées dans les invocations).

- `replay/provenance.json`, `replay/invocation.json` : hash binaire et CUE/BIN,
  commandes, répertoire courant, horodatages, fenêtre, événements clavier,
  captures hashées et exit du wrapper.
- `replay/gdb.log` : entrées/retours loader, états Lara/menu/pause et exit applicatif.
- `runtime-quit.py`, `runtime-quit.gdb` : copies privées de la recette antérieure,
  garde d'autorisation renouvelée uniquement dans la copie du nouveau lot.
- `replay/contact.png` et captures originales : privées, jamais versionnées.
- `archive-tests.log` : sept tests des preuves du 18 septembre, sans relancer le jeu.
- `milestones-red.log` : neuf échecs attendus du nouveau contrat documentaire avant
  implémentation ; ce RED **n'est pas un RED du jeu**.

Le renderer ajoute des jalons sans modifier les anciens blocs de progression ou
leurs échéances. Ses tests valident uniquement les documents et leurs garde-fous.
Les tests publics actual-TU du wrapper audio conservent leur portée antérieure ;
ils ne prouvent ni la scène ni le son matériel.

## Suite cohérente

Étendre le parcours réel aux commandes de base et à une transition de salle,
avec traces et captures, avant toute correction. S'il apparaît un défaut,
reproduire puis établir l'attribution cible/ABI et un RED actual-TU avant patch.
Ne pas inventer un correctif de chargement pour un arrêt d'observation trop court.


## Analyse géométrie empilement 5D Trajan's Markets (données, 2026-11-08)

Source : NTSC USA `TOMB5.BIN` (data), Trajan's Markets = LBA 18404 (252 rooms). Parsing via `offsetRoomInfo`/`roomInfoLength` du header niveau (`ver=-225`), puis table `room_info` 80 octets + sous-blocs `[data,door,floor,light,mesh]` (tailles sur disque dans les champs pointeur), `floorData` à la suite. `FLOOR_INFO` 8 octets (`index, fx:4/box:11/stop:1, pit_room, floor, sky_room, ceiling`), hauteurs en clicks signés (`room.y - click*256`). **Données statiques, non validées en jeu.**

### Puits 207→201→199→200 (impraticable en montée)
- 207 (75776,43008,-1024, mf=0, 6x4) : intérieur x=1-4,z=1-2 `fl=0 ceil=-4 sky=201 pit=255` (sol monde -1024).
- 201 (-2048) : `fl=-4 ceil=-8 sky=199 pit=207` (sol monde -1024 **mais `pit=207`**) — aucun atterrissage.
- 199 (-4096) : `fl=-8 ceil=-16 sky=200 pit=201`. 200 (-6146, mf=-4096) : `fl=-16 ceil=-24 sky=255 pit=199`.
Conclusion : le saut 207→201 atteint 201 en vol mais retombe (confirmé runtime) ; le puits est entièrement `pit` vers le bas.

### Connectivité / piles verticales
- 207 portails 10,219 (+201 au-dessus). 10 (75776,38912,-1024, `sky=209`) ↔ 209 (-2048, `sky=11 pit=10`, portails 10/11/201/206/210/213). 209↔11 (-4096, `sky=13 pit=209`) ↔ 13 (-6144, `pit=11`).
- Nord : 209↔213 (-2048, `sky=45 pit=9`)↔214 (-2048, `sky=12 pit=46`). 213↔9/45 ; 214↔46/12. 45 (-4096, `pit=213 sky=202`) ; 12 (-4096, `pit=214 sky=202`) ; 202 (-6144).
- Est : 209↔210 (`sky=48 pit=0`)↔211 (`sky=49 pit=54`)↔212 (`sky=5 pit=50`). 212↔50 (départ niveau 2, -1024, `sky=212`) et ↔5 (-4096, `pit=212`). 48/49/5 à y=-4096.
- Ouest : 209↔206 (`pit=208`)↔208 (`sky=206`).
- Aucun secteur `CLIMB`/`MONKEY` (floor_data) dans wx 74000-84000, wz 34000-49000 ; `CLIMB` du niveau uniquement rooms 16,95,222. Transitions ~+256u (10→209) à ~+1024u (209→11,214→12,213→45,210→48/211→49/212→5) : saisie de rebord selon géométrie de collision, à valider en jeu.

### Route plausible (à valider)
`207 → 10` (plat) → `209` (saut +256u par `sky=209`/`pit=10`) → monter `213→45` ou `214→12` (nord, vers couche -4096/`202`) ou `210→48`/`211→49`/`212→5` (est). Le puits `207/201` ne mène nulle part en atterrissage.
