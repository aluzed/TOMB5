# BLOCKED-007 — interruption fournisseur RE930

Status: `Blocked` — owner : prochain agent autorisé, aucun worker de recherche actif revendiqué.
Parent : [RE929](../RE-929-cpu-exception-proof-publication.md). Baseline livrée : `0edd91701bff3dcc37dab8948812fce503f296ca`.
Objectif suspendu : continuation BIU/cache et initialisation CPU/kernel/thread du backend de remplacement OpenBIOS, sans effacer BEV ni injecter un thread.

## Progression
- [x] Refus fournisseur conservé et frontière d'exécution inspectée.
- [x] Checkpoint historique authentifié : cinq membres, tailles/SHA, seal et ensemble exact.
- [x] Handoff durable, index et dashboard incident séparé publiables ; tests documentaires RED puis GREEN.
- [ ] Résolution légitime du refus / accès fournisseur approprié.
- [ ] Nouvelle preuve exécutable et revue indépendante avant toute intégration.

## Incident observé
Le 12 octobre 2026 vers 03h16 Europe/Paris, la délégation `deleg_d079cd72` (openai-codex, gpt-6.1-sol) a renvoyé `PROVIDER_SAFETY_FILTER_BLOCKED` après 17.06 secondes. Le message fournisseur indique un filtrage de sécurité et une voie d'accès Daybreak ; ce n'est ni un exit de compilateur ni une impossibilité technique démontrée. Les lectures de skills/HANDOFF/date/status/pwd sont attestées ; ZERO nouveau build, ZERO nouvelle exécution CPU, aucune preuve RE930 obtenue.

Conformément à l'instruction utilisateur : aucun contournement, aucune reformulation/reprise de l'unité refusée, aucun changement fournisseur, aucune exécution équivalente dans le contexte parent. Cette publication est uniquement documentaire ; elle ne reprend pas la recherche suspendue.

## Preuves
Archive locale : `build/reverse/autonomy-20261012/re930-provider-incident-checkpoint/`.
- `incident.json` : statut fournisseur, durée et limite du scope.
- `subagent-transcript.log` : transcript réel, SHA256 `c2300e5f95adfd5407976e7abf2bcdfc8afad85d207a9f8f43843b98e99385cc`.
- `manifest.json` : SHA256 `e5f06b395ac1fd5dcb2b15889bd19099194e12f6d49aefdc76fc7fe922046b16`, cinq membres.
- `seal.json`, `verification.json`, `HANDOFF.md` et `ledger.jsonl` préservés ; aucun seal historique modifié.
Vérification documentaire fraîche : `build/reverse/autonomy-20261012/re930-durable-blocker/incident-readback.json`. Les données brutes restent locales, non versionnées.

## Frontière technique inchangée
RE928 a franchi SYSCALL et s'est arrêté AVANT le store BIU, via le vecteur ROM / flushCache. Le retour naturel du handler RAM et l'initialisation kernel/thread restent non prouvés. Les preuves OpenBIOS MIT / PCSX-Redux GPL-2.0-or-later décrivent explicitement un backend de remplacement ; elles ne prouvent pas une adresse RA de BIOS Sony. Boot reset naturel, CD naturel, GPU/hardware/gameplay non validés ; integration=false, production_patch=false, global/procedure FAIL historiques maintenus. Aucun asset ni source tierce ajouté ici.

## Critères de réouverture
- [ ] Le refus est résolu par un mécanisme légitime du fournisseur ou un périmètre explicitement accepté ; pas par une reformulation visant à contourner le filtre.
- [ ] Vérifier l'autorisation courante et la fin du HANDOFF, exclure un autre owner vivant et prendre les deux locks canoniques.
- [ ] Reprendre ensuite seulement les inputs pinés et l'état cohérent existants, sans RA arbitraire, faux secteur réussi, BEV effacé ou thread injecté.
- [ ] Produire exécution réelle bornée, ledger prospectif, tests sensibles, revue indépendante, HANDOFF final et inventaire exhaustif avant seal.
- [ ] Toute intégration production exige sa propre preuve et revue ; un PASS documentaire ne l'autorise pas.

Fenêtre utilisateur du 11 octobre vers 23h21 : jusqu'au 2026-10-12T05:00:00+02:00 ; recherche 04h20, revues 04h40, livraison 04h50, locks libérés avant 04h55. Ce checkpoint ne révoque pas cette fenêtre et ne crée aucun job/successeur. Suppressions BLOCKED-001/002, report utilisateur, cache préexistant, assets/cold archives/first FAILs/seals/RE893 partial préservés.

[Dashboard incident versionné](../../reverse/tomb5-progress-dashboard-re930-incident-v1.html). Le dashboard maintained RE929 et ses empreintes historiques restent inchangés.

## RE930 — reprise technique bornée (2026-10-13)

Autorisation : l'utilisateur a demandé la reprise technique réelle de ce ticket. Périmètre accepté : un fournisseur/modèle distinct reprend l'unité pinée ; aucune reformulation visant à contourner un filtre, aucun refus réouvert en place, aucun contournement. Le statut reste `Blocked` tant que les critères de réouverture ne sont pas tous satisfaits.

Résultat borné PASS producteur : la frontière BIU/cache de RE928 (arrêt avant le store BIU_CONFIG) est franchie, et l'init froide/exception ROM s'exécute réellement (flushCache avec fenêtre cache isolé puis cache normal, initialisation des registres CP0, copie de données, effacement BSS, pile, registre de taille RAM, traces POST/EXP2). Exécutions fresh et restored reproduites, transitions BIU identiques, oracle BIU compilé concordant, contrôle négatif « cache isolé dès le départ » en échec de préfixe conservé.

Frontière suivante honnête : initialisation SPU (registre SPU, demi-mot, depuis ROM) — premier périphérique matériel hors sous-ensemble authentifié. Handler noyau RAM et retour RFE naturel NON obtenus. integration=false, production_patch=false, FAIL global/procédure historiques maintenus.

Preuves locales non versionnées : `build/reverse/autonomy-20261013/re930-biu-kernel/` — `execute.py` étendu (BIU_CONFIG, taille RAM, EXP2/POST, CP0 génériques), `fresh.json`/`restored.json`, contrôles négatifs, oracle `biu_witness.cc` compilé, `HANDOFF.md`, `scope.json`, `verdict.json`, `ledger.jsonl`, `manifest.json`, `seal.json`. Revue indépendante : PASS borné ; deux défauts de scellement (manifest/ledger, HANDOFF non couvert) détectés puis corrigés et re-scellés.

- [x] Périmètre de résolution légitime accepté (fournisseur/modèle distinct ; pas de contournement).
- [x] Frontière BIU/cache franchie avec preuve d'exécution réelle bornée et oracle BIU compilé.
- [ ] Atteinte naturelle du handler noyau RAM / retour RFE (frontière suivante : SPU et périphériques).
- [ ] Preuve et revue indépendantes distinct-auteur avant toute intégration.

[Dashboard RE930 BIU/kernel versionné](../../reverse/tomb5-progress-dashboard-re930-biu-kernel-v1.html).
