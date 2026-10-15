# RE-957 — Linux32 : interruption du recorder et fermeture des enfants

Status: Done — correction finie de l’outillage uniquement, pas du portage.

[Dashboard](../reverse/tomb5-progress-dashboard-re957-v1.html) · [Recette Linux32](../porting/linux32.md)

## Intention et indépendance
Éviter qu’une interruption du recorder laisse ses commandes de compilation ou de lancement actives, avec un journal incomplet. Entrées : outil Python versionné `scripts/porting/linux32.py`, tests porting publics et sous-processus Python synthétiques. Aucun asset, moteur MIPS, allocateur ni archive scellée utilisés. Autorisation renouvelée le15 octobre2026 vers23h37 Europe/Paris, jusqu’au16 octobre07h00 ; ce jalon ne promet aucune activité continue entre ticks.

BLOCKED-008 et BLOCKED-009 restent ouverts et exclus ; aucune tentative de contournement ou nouvelle compilation/relecture de leur chaîne. `integration=false`, `production_patch=false` : seul l’outil Python est corrigé, pas une source du jeu. Aucun boot/menu/gameplay nouveau validé.

## Diagnostic, étapes et preuves
1. Lecture du recorder : seul `TimeoutExpired` déclenchait destruction de la session et attente de l’enfant. `KeyboardInterrupt` ou `SystemExit` traversaient le finally de journalisation sans fermer ces processus.
2. RED comportemental réel : deux cas échouent avec « interruption left child/session descendant running », exit1. Chaque test démarre un recorder, son enfant et un petit-enfant Python ; le nettoyage de test les ferme également en cas de RED.
3. Correction minimale : toute exception de `wait()` ferme le groupe par SIGKILL, attend l’enfant direct, enregistre son code natif et propage l’exception originale. Le timeout conserve `timed_out=true` ; les autres interruptions enregistrent leur classe sous `interrupted`, avec `timed_out=false`. Groupe déjà disparu : `ProcessLookupError` toléré.
4. Mêmes deux tests : GREEN2, exit0. Régression `tests/porting` avant ajout des tests de publication : **452 passed**, exit0. Ces tests exécutent de vrais processus hôte, pas le jeu ni un replay natif cible.
5. RED documentaire séparé : deux fichiers publics absents, deux FAIL exit1 ; ces échecs ne sont pas des défauts du recorder. Tests de publication vérifient le périmètre, les statuts et les liens locaux.

Preuves privées nouvelles : `build/reverse/autonomy-20261016-night/` ; `red-interruption.stdout`, `green-interruption.stdout`, `green-porting.stdout`, `red-publication.stdout`, ledger prospectif argv/cwd/exits/durées et snapshot préexistant. Revue exacte indépendante exigée avant commit ; ses résultats et les observations Git/HTTP sont consignés dans le HANDOFF privé sans réécrire les archives précédentes.

## Critères et progression
- [x] Deux interruptions réellement reproduites avant correction, mêmes cas GREEN après.
- [x] Vérifier disparition exécutable de l’enfant et du descendant, pas uniquement l’exit du recorder.
- [x] Vérifier journal final : interruption, signal de sortie, temps, absence de faux timeout ; SystemExit17 conservé.
- [x] Régression porting452 réussie, échecs originaux conservés.
- [x] Story, dashboard et tests de liens ajoutés au même lot.
- [x] Cleanup explicite : zéro suppression, aucune redondance démontrée ; FAILs et preuves uniques conservés.
- [ ] Acceptation fonctionnelle complète de PORT-001, du menu et du gameplay (hors ce lot).

## Limites et reprise indépendante
Linux/POSIX seulement : tests `/proc` distinguent zombie et processus exécutable. L’enfant direct est reapé par `wait()` ; le descendant tué peut brièvement rester zombie jusqu’à récollection par son parent adoptif. Les descendants ayant quitté le groupe ne sont pas couverts. SIGKILL appliqué au recorder lui-même, mort machine, seconde interruption pendant cleanup et erreurs du système pendant cleanup ne sont pas garantis par ce correctif.

Le test SystemExit utilise volontairement un handler SIGTERM Python qui fait `sys.exit(17)` ; le driver n’installe **pas** de handler SIGTERM par défaut. Ne pas annoncer ce test comme prise en charge du SIGTERM natif non intercepté. Aucun nouveau runtime graphique : pas de capture fictive.

Prochaine frontière indépendante possible : tester les échecs de démarrage et les collisions des fichiers de preuve du recorder, sous une unité distincte ; aucun statut acquis pour ces cas ici. Lire heure, autorisation, claims et HANDOFF courant avant reprise. La chaîne refusée n’est pas une suite de ce ticket.
