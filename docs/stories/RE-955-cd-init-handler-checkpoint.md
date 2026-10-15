# RE955 — corps Init CD, checkpoint construit documenté

## Tracker
- [x] Unité15 : preuves privées archivées authentifiées, sans nouveau rejeu.
- [x] Revue indépendante finie SCOPED_PASS : 10 builds et 10 natifs frais archivés.
- [x] TDD documentaire : test avant metadata/story/dashboard ; pas RED comportemental.
- [ ] Publication : snapshot auteur PENDING, revue séparée des hashes exacts requise.
- [ ] Intégration production : integration=false, production_patch=false.

## Progrès réel et attribution
Le vrai producteur ouvert `cdromInnerInit` → MMIO → FIFO → horloge CPU construite → branchTest/table/callback atteint maintenant le corps genuine `cdlInit(start=true)`, contrairement à la garde avant corps de RE954. ACK cause3 payload[2] au cycle26996, puis schedule120ms =4064256cycles ; commands callback appelle `cdlInit(false)` et produit Complete cause2 payload[2] au cycle4091252. Les handlers ouverts produisent les réponses dans le fixture construit : pas de secteur réel, pas de réponse préseedée ni état succès injecté.

Le retour0 de innerInit reste un **timeout host avant CPU**, pas un succès OpenBIOS. Les cycles pendant l'attente host restent0/0. Memory::setIRQ est une façade OR : start4, final5 inclut counter1 ; ce n'est **pas une livraison IRQ réelle au BIOS**. La complétion CD dans le fixture ne prouve pas la réussite de l'attente OpenBIOS.

## Résultats archivés, non rejoués ici
Reviewer : normal/UBSan, 10 compilations +10 exécutions natives ; 2 contrôles oracle PASS ; 8 mutants sensibles (no_schedule/wrong_delay/no_irq/wrong_complete ×2), natif exit0 puis AssertionError exit1. Chaque contrôle vérifie2045626 fetches et1906 hsyncs. Auteur : six mutants ×2 =12 rejets archivés, pas nouvelle matrice fraîche. Aucun build ni natif pour cette publication.

## Provenance et limites
Redux GPL-2.0-or-later : c313b116e6a55786bc127c9b3a07a90b55d97c21 ; OpenBIOS/nugget MIT : 7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30. Manifests complets254/183 membres authentifiés ; pins dans les [métadonnées](../reverse/generated/re955_cd_init_handler_checkpoint.json). Extraits sources et providers construits ≠ full CD TU/ABI, démarrage naturel, Sony, hardware ou gameplay. Aucun opcode, dump ou asset propriétaire publié.

**Fini SCOPED_PASS ≠ strict INCOMPLETE ≠ procédure INCOMPLETE.** Timeout worker600s ; recovery246.28s dépasse budget240s. Reviewer491.03s depuis dispatch rapporté, réserve100s non respectée (renderer vers447s). Les premières erreurs, gaps de ledger et warnings restent conservés ; aucune rétrocertification. L'auto-vérification publique ne vaut pas revue indépendante de publication.

## Prochaine frontière / blocker explicite
Coexécuter l'attente OpenBIOS avec le CPU et un producteur IRQ réel ; non exécuté, non autorisé par ce checkpoint. L'absence de livraison IRQ BIOS bloque une affirmation de succès OpenBIOS. Aucun nouveau blocker redondant créé ; aucune frontière globale blanchie. Recherche parent18h00, revue18h20, livraison18h35, autorisation18h45 ne prolongent pas le budget auteur HARD400s.

## Nettoyage et conservation
Zéro suppression ; archives, FAILs, avertissements et fichiers personnels conservés. Espace et membership export mesurés dans le bundle auteur ignoré, avec ledger et HANDOFF avant seal. README, index, dashboard RE954 et coordinator/preflight.json inchangés. Quatre nouveaux chemins seulement ; rollback = retirer uniquement ces quatre chemins. Aucun job, stage, commit, push, build ni intégration.

[Dashboard RE955](../reverse/tomb5-progress-dashboard-re955-v1.html). Gate publication PENDING : reviewer séparé doit accepter les quatre hashes exacts, pas ce texte prospectif.
