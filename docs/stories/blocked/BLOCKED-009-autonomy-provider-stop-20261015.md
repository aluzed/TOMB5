# BLOCKED-009 — autonomie interrompue par refus fournisseur

## État et progression
**OPEN — accès fournisseur / recherche arrêtée pour cette tentative.** Ce blocage n'est pas une impossibilité technique et ne résout pas BLOCKED-008. Aucun nouveau ticket RE ni gain comportemental n'est revendiqué.

- [x] Reprise autorisée et heure réelle Europe/Paris contrôlées le 15 octobre 2026.
- [x] HEAD initial `727a90d6dc9151f78eb13a6cf79c8888c2bc3bfb`, préexistants et hashes dirty préservés dans le snapshot privé.
- [x] Archives unité18 / revue18 : respectivement 270 et 123 membres vérifiés par taille et SHA256. Ce contrôle de membres ne revendique pas une nouvelle revue ni une authentification exhaustive de tous les inventaires historiques.
- [x] Tentative de délégation arrêtée ; refus conservé, sans contournement.
- [ ] Reprise technique autorisée et compatible avec les règles du fournisseur.
- [ ] Producteur allocateur réellement débloqué puis rejoué et revu indépendamment.

## Intent, inputs et tentative constatée
Objectif non atteint : débloquer la tentative allocateur MIPS décrite dans [BLOCKED-008](BLOCKED-008-re956-mips-allocator-engine-handoff.md), sans changement du code de production. Les sources ouvertes et le précédent protocole restent disponibles ; ce constat ne les transforme pas en preuve nouvelle.

Délégation `deleg_68f36480`, démarrée **13:32:47**, terminée **13:33:22 Europe/Paris**, durée rapportée **34.88 s**. Le retour de l'outil indique un refus du filtre de sécurité du fournisseur `openai-codex`, modèle `gpt-6.1-sol`, et le message « This content was flagged for possible cybersecurity risk. ». Le wrapper indique aussi `max_iterations` : ne pas le réinterpréter comme un exit d'émulateur ou un diagnostic technique.

La trace visible contient des vérifications et lectures uniquement. **Aucun replay**, compilation ou test comportemental nouveau observé ; le root prévu unité19 est absent. Aucun patch, faux état ou résultat de succès n'a été produit. `integration=false`, `production_patch=false`. Pas de gameplay, boot matériel ou succès global OpenBIOS validé.

## Preuves locales pour opérateur
Racine ignorée `build/reverse/autonomy-20261015/` : `coordinator-1330/preflight.json`, `coordinator-1330/input-authentication.json`, puis `provider-stop-1330/refusal.json`, copie de trace `delegation-transcript.txt` et ledger documentaire. Le dossier prévu `cd-init-unit19` n'existait pas lors du constat parent. La trace originale reste dans le cache de délégation. Ne pas relancer de writer dans les archives scellées.

Les seuls tests nouveaux vérifient ce document, le dashboard de pause et leurs liens. Leur RED est documentaire (fichiers absents), pas un RED fonctionnel MIPS. Le jalon technique publié reste [RE956](../RE-956-cd-init-reviewed-frontiers.md).

## Handoff et acceptation de reprise
1. Lire ce blocage et BLOCKED-008, ainsi que le checkpoint partagé courant ; vérifier date réelle, autorisation et propriétaires vivants avant toute action.
2. **Ne pas reformuler la requête refusée pour contourner le filtre, ne pas changer de fournisseur ni relancer la même recherche ailleurs.** Une résolution doit passer par les voies d'accès/support appropriées et une autorisation conforme, sans présumer son succès. Ce document n'est pas une recette de contournement.
3. Si l'obstacle d'accès est légitimement levé, respecter l'autorisation en vigueur et les cutoffs ; relire alors les conditions techniques de BLOCKED-008. Aucun résultat de l'unité19 n'est disponible à reprendre.
4. Exiger une nouvelle exécution attribuée et une revue indépendante avant toute revendication de progrès ; les succès historiques ne certifient pas cette tentative.

Autorisation utilisateur initiale : autonomie jusqu'au **15 octobre 2026 à 18h45 Europe/Paris**, recherche/implémentation avant 18h00, revues avant 18h20, livraison avant 18h35, aucune mutation après 18h45. L'interruption actuelle est anticipée, pas une expiration ni une prolongation. Aucun nouveau job ni modification de l'entretien ; aucune activité continue entre ticks annoncée. Les prochains ticks ne doivent pas retenter automatiquement cette recherche refusée.

## Cleanup et publication
Zéro suppression : aucune redondance supprimable démontrée ; FAILs, trace et preuves uniques conservés. Préexistants personnels exclus de la livraison ; aucun asset ni trace privée exposé. Revue documentaire exacte et publication sont des gates séparées du refus et ne constituent pas une revue technique de l'unité19.

[Dashboard de pause](../../reverse/tomb5-progress-dashboard-re956-provider-pause-v1.html) · [Blocage technique précédent](BLOCKED-008-re956-mips-allocator-engine-handoff.md)
