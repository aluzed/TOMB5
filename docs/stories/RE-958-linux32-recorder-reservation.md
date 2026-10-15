# RE-958 — Linux32 : finaliser les collisions de journaux

Status: Done — correctif fini d’outillage, acceptation du portage non acquise.

[Dashboard](../reverse/tomb5-progress-dashboard-re958-v1.html) · [Recette Linux32](../porting/linux32.md)

## Intention, entrées et indépendance
Conserver un diagnostic terminé quand le recorder refuse un fichier `.log` déjà existant, sans écraser les preuves ni démarrer l’enfant. Entrées : `scripts/porting/linux32.py`, tests Python publics et processus hôte synthétiques ; aucune donnée de jeu. Autorisation Alexandre du15 octobre vers23h37 jusqu’au16 octobre2026 07h00 Europe/Paris, cutoffs06h15/06h35/06h50. Ce checkpoint n’annonce pas d’activité continue.

BLOCKED-008 et BLOCKED-009 restent exclus et ouverts ; RE944 et leur chaîne dépendante ne sont pas repris. Aucun allocateur, MIPS, Unicorn ou objectif refusé rejoué. `integration=false`, `production_patch=false` pour le jeu : seul l’outil Python change, pas les sources du jeu. Aucun nouveau boot/menu/gameplay validé.

## Diagnostic et étapes
1. `ledger.open('x')` réservait le JSON, puis l’ouverture exclusive du log se trouvait **avant** le try/finally. Une collision log levait bien FileExistsError et préservait le fichier mais laissait le nouveau JSON sans erreur, fin ni durée.
2. RED comportemental réel : deux collisions (fichier et répertoire existants) échouent sur « log reservation failure left an unfinished ledger » ; trois contrôles déjà GREEN caractérisent ledger préexistant et démarrages impossibles (exécutable ou cwd absent). Ces trois cas ne sont pas des régressions corrigées ici.
3. Correction minimale : déplacer l’ouverture du log dans le try existant. OSError est consignée, le finally termine le nouveau ledger, puis l’exception originale est propagée. Aucun `exit` natif inventé si aucun enfant n’a démarré. La réservation JSON reste hors try pour ne jamais réécrire un ledger préexistant.
4. Mêmes cinq cas : **5 passed**, exit0. Régression auteur `tests/porting` : **459 passed**, exit0, avant ajout des deux tests documentaires. Elle inclut des fixtures actual-TU ordinaires préexistantes ; ce n’est ni un build complet ni un runtime jeu.
5. RED documentaire séparé : deux tests FAIL parce que story/dashboard absents ; ce n’est pas un défaut comportemental. Tests vérifient scope/limites et résolution des liens locaux. Gate indépendante exacte avant publication ; verdict, tests attribués et observations Git/HTTP dans le HANDOFF privé.

## Preuves et acceptation
Racine ignorée nouvelle `build/reverse/autonomy-20261016-night/unit02/` : `preflight.json`, `claim.json`, `ledger.jsonl`, `red-reservation.stdout`, `green-reservation.stdout`, `green-porting.stdout`, `red-publication.stdout`, puis revue et livraison. Les archives unité01 et historiques ne sont pas réécrites.

- [x] Deux vrais RED collision conservés, cinq mêmes cas GREEN après correctif.
- [x] Ancien log fichier/répertoire et ancien ledger conservés octet à octet ; enfant non démarré.
- [x] Exécutable/cwd absent : erreur et temps enregistrés, log vide, aucun exit natif fictif (caractérisation).
- [x] Régression porting459 passée ; story/dashboard versionnés avec tests.
- [x] Cleanup explicite : zéro suppression, aucune redondance démontrée ; FAILs et preuves uniques conservés.
- [ ] Acceptation du portage complet, menu et gameplay (hors unité).

## Limites et prochaine frontière indépendante
Le refus de réservation n’est pas un succès applicatif. Si le dossier de sortie lui-même manque, si la première création JSON échoue, ou si l’écriture finale échoue (disque plein/permissions), aucun ledger final fiable n’est garanti. La paire JSON/log n’est pas une transaction atomique et les symlinks/modifications concurrentes d’un tiers dans un répertoire non privé ne sont pas sécurisés ici. L’outil impose déjà une sortie privée neuve au CLI ; ne pas réutiliser un dossier de preuves. Les limites d’interruption de RE957 restent inchangées.

Prochaine unité utile possible : vérifier séparément la validation des noms de labels de l’API interne ; non acquis ici, pas de patch spéculatif. Avant reprise : heure réelle, autorisation, contention et HANDOFF. Aucun runtime graphique exécuté : pas de capture fictive.
