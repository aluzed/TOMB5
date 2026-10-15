# BLOCKED-007A — relais SPU/périphériques → handler RAM → RFE

Status: `Implémenté` (2026-10-14) — lots A/B/C livrés PASS bornés et revus indépendamment ; BLOCKED-007 reste partiellement bloqué (boot matériel/CD/GPU/audio hors acceptation).
Parent : [BLOCKED-007](BLOCKED-007-re930-provider-refusal.md).
Owner : autre agent désigné par Alexandre ; Hermes prépare uniquement ce relais documentaire.
Autorisation : demande directe du 13 octobre 2026 de séparer les travaux restants de BLOCKED-007 dans un ticket. Ce document ne lance aucun worker, ne prolonge aucune fenêtre d'autonomie et n'autorise aucun contournement de refus fournisseur.

## Intention et point de départ

Faire avancer le backend de remplacement OpenBIOS depuis la frontière SPU réellement observée jusqu'à un handler noyau RAM et un retour RFE naturellement obtenus. Séparer la preuve de continuation, la fidélité du modèle et l'autorisation d'intégration.

**Acquis à ne pas refaire comme nouvelle livraison :** l'autre agent a franchi la frontière BIU/cache de RE928 ; initialisation ROM froide/exception, transitions cache isolé/normal, CP0, copie des données, BSS, pile, taille RAM et traces POST/EXP2 ont une preuve bornée et une revue séparée. Ce PASS ne couvre pas le reste du boot.

**Frontière restante constatée dans les HANDOFF :** premier accès SPU non pris en charge ; handler RAM et retour RFE non atteints. Le modèle est cacheless et l'état initial est construit : aucune preuve de reset matériel naturel ni de BIOS Sony.

## Inputs et preuves existants

Chemins relatifs à `/var/www/projects/TOMB5`, preuves privées ignorées :
- `build/reverse/autonomy-20261013/re930-biu-kernel/HANDOFF.md`
- `build/reverse/autonomy-20261013/re930-biu-kernel/execute.py`
- même racine : `scope.json`, `verdict.json`, `fresh.json`, `restored.json`, contrôles négatifs, `biu_witness.cc`, `ledger.jsonl`, `manifest.json`, `seal.json`, `closeout.json`.
- `build/reverse/autonomy-20261013/re930-biu-kernel-review/HANDOFF.md` et `verdict.json`.
- Sources OpenBIOS / PCSX-Redux déjà épinglées par ces preuves : résoudre leurs chemins, versions et licences depuis les inputs existants, sans inventer de chemin ou télécharger un BIOS propriétaire.
- Incident historique : `build/reverse/autonomy-20261012/re930-provider-incident-checkpoint/` ; le conserver distinct des résultats techniques ultérieurs.

La revue séparée existante rapporte un PASS du scope fini BIU/cache. Elle liste encore comme non prouvés notamment : handler/RFE, RAM intermédiaire byte-identique, fidélité CPU complète, load-delay, invalidation du cache, mirroring RAM, reset naturel et second algorithme CPU complet. Ne pas transformer cette revue en acceptation globale.

## Découpage confié à l'autre agent

### Lot A — SPU : franchir uniquement la prochaine frontière
- [ ] Authentifier les inputs et l'état courant sans muter les archives scellées.
- [ ] Attribuer le premier accès SPU : largeur, état, producteur et sémantique à partir des références ouvertes épinglées.
- [ ] Implémenter dans une nouvelle copie privée le sous-ensemble SPU minimal réellement nécessaire. Aucune réponse constante de succès choisie seulement pour faire avancer le replay.
- [ ] Rejouer les départs fresh/restored et contrôler l'état RAM/CP0/périphérique pertinent ; conserver les écarts et premiers FAILs.
- [ ] Ajouter un oracle ou témoin indépendant et un contrôle négatif sensible à la nouvelle sémantique.
- [ ] Identifier le premier nouvel accès/polling non pris en charge et arrêter à cette frontière ; ne pas appeler cela émulation SPU/audio complète.
- [ ] Revue indépendante du lot A avant composition avec le lot B.
- [ ] Nettoyage : garder les inputs, scripts, preuves uniques et FAILs ; ledger exact des suppressions et mesure d'espace avant/après.

### Lot B — continuation kernel : handler RAM et retour RFE
Dépendance : lot A accepté. Chaque nouveau périphérique rencontré constitue une sous-unité explicitement bornée, pas une permission de simuler tout le matériel.
- [ ] Inventorier les dépendances effectivement rencontrées et implémenter uniquement les sémantiques justifiées, avec source/licence et oracle explicités.
- [ ] Prouver que le programme produit naturellement les tables/vecteurs et l'état kernel nécessaires ; attribuer leurs écritures et leurs consommateurs.
- [ ] Atteindre le handler noyau RAM, puis son chemin de retour RFE, avec PC, CP0, pile, registres et RAM cohérents.
- [ ] Distinguer l'entrée construite OpenBIOS de la provenance reset naturel ; un retour naturel depuis cette entrée ne prouve pas un boot matériel complet.
- [ ] Produire replay fresh/restored, comparaison indépendante et contrôles négatifs pertinents ; nommer toute fidélité CPU manquante qui limite le résultat.
- [ ] Si un input, un état ou une sémantique manque, publier la frontière exacte et le plus petit input/preuve nécessaire ; ne pas injecter un état convenable.
- [ ] Revue indépendante du lot B et de la composition A→B.
- [ ] Nettoyage explicite avec conservation essentielle, ledger et mesures avant/après.

### Lot C — décision de fidélité et d'intégration (gate séparée)
Dépendance : preuves finies des lots précédents ; pas d'activation transitive.
- [ ] Évaluer les gaps CPU/cache/RAM réellement nécessaires au chemin observé, notamment load-delay, invalidation/cache et mirroring. Les classer prouvés, non pertinents dans le scope ou bloquants, sans revendiquer une fidélité globale.
- [ ] Réexécuter indépendamment le scope candidat et vérifier les oracles, contrôles négatifs et inventaires.
- [ ] Émettre un verdict explicite : scope fini, naturalité démontrée, limites, revue, `integration`, `production_patch` et statut global/procédural séparés.
- [ ] Toute intégration production exige ses propres tests et revue distincte. Jusqu'à ce gate : `integration=false`, `production_patch=false`.
- [ ] Mettre à jour la progression et le dashboard approprié sans réécrire les premiers refus/FAILs/seals.
- [ ] Nettoyage et livraison des seuls scripts/docs/tests/metadata sûrs ; aucun asset ou dump propriétaire versionné.

## Préflight et règles communes

1. Lire les derniers checkpoints des autres agents ; vérifier autorisation et propriétaire vivant. Les anciennes échéances sont historiques, pas une autorisation courante.
2. Utiliser les locks canoniques `build/reverse/autonomy-repo.lock` (ownership) et `build/reverse/autonomy-mutation.lock` (mutations par opération), vérifier PID vivant et contention. Ne pas tuer un autre owner et ne pas imbriquer un outer mutex autour d'un outil qui prend déjà ce mutex.
3. Authentifier seals/manifests avec leur schéma réel. Créer une nouvelle racine ignorée par lot ; ne pas éditer `re930-biu-kernel/` ou ses reviews scellés.
4. Tenir un ledger prospectif des commandes/argv/exits et des budgets réellement exécutés. Tests RED/GREEN et mutants doivent être sensibles au comportement, pas seulement à un schéma documentaire.
5. Aucun BEV effacé manuellement, thread/handler injecté, RA arbitraire, secteur CD réussi fictif ou polling détourné pour obtenir un PASS.
6. Réutiliser les implémentations ouvertes déjà disponibles ; si une dépendance manque, effectuer une recherche bornée légitime d'implémentations ouvertes avant de conclure à un blocage. Déclarer source, version, licence, scope et fidélité ; pas de substitut non attesté.
7. Un refus fournisseur n'est pas un FAIL technique. Stopper l'unité refusée, conserver l'incident et utiliser uniquement une voie d'accès légitimement acceptée ; pas de reformulation, découpage ni changement de fournisseur visant à contourner le filtre.
8. Préserver les modifications personnelles, suppressions BLOCKED-001/002, preuves essentielles, archives froides et assets ignorés. Ne pas faire de reset/clean/stage global. RE944 et autres unités refusées ne font pas partie de ce ticket.

## Livrables attendus par lot

- HANDOFF français : intent, inputs authentifiés, étapes réellement exécutées, commandes/exits, frontière de sortie, limites et prochain unblocker.
- Tests/oracle/contrôles négatifs et verdict producteur ; revue indépendante avec attribution de ce qui a réellement été réexécuté.
- Ledger prospectif, inventaire complet et seal final ; observations de release hors racine scellée.
- Story/metadata publics légers et progression lisible ; raw RAM, instructions, payloads, captures lourdes et assets restent privés ignorés.
- Sous-tâche cleanup DONE ou OPEN motivée, mesurée sans confondre octets logiques et espace physique récupéré.

## Implémentation 2026-10-14 (relais RE948)

Exécution réelle bornée des trois lots, chacun avec oracle compilé indépendant, mutants comportementaux,
contrôles négatifs et revue indépendante sur copie isolée. Preuves privées non versionnées sous
`build/reverse/autonomy-20261014/`.

- **Lot A (SPU minimal)** : frontière SPU de RE930 franchie ; prochaine frontière `DIVU` funct 27 à
  `0xbfc07668`. Contrôle `--no-spu` → reproduit `0xbfc07928`. Oracle `spu_witness` + 6 mutants détectés.
  Seal `2afb97b3…258cd5` (82 membres) ; revue indépendante seal `6c45849c…e8e49` PASS, défaut latent
  (accès 32 bits chevauchant la fenêtre SPU) corrigé puis re-vérifié.
- **Lot B (continuation kernel)** : `DIV`/`DIVU` + compteurs racine 0/2 ; vecteur général RAM
  `0x80000080` → handler `0x2700` → **RFE `0x29d0`** obtenus naturellement (2 syscalls), sans injection.
  Prochaine frontière CD-ROM `0x1f801800` en RAM `0x145c` (hors acceptation). Contrôles `--no-divu` /
  `--no-counters` / `--no-rfe` ; oracles `divu_witness`/`counter_witness` + 8 mutants détectés.
  Seal `689fe643…1ce972f` (136 membres) ; revue indépendante seal `a8909360…aab983` PASS, harnais
  mutants corrigé puis re-vérifié ; composition A→B (`spu.py` byte-identique).
- **Lot C (gate fidélité/intégration)** : écarts classés (`fidelity.json`), naturalité démontrée
  seulement dans l'entrée construite, `integration=false`, `production_patch=false`, statuts
  global/procédure maintenus. Seal `46e8b31d…825fe` ; revue indépendante seal `2beee4a4…d2d8069` PASS,
  `logic_errors=[]`.
- Nettoyage : aucun fichier scellé modifié, aucune suppression (ajouts privés ignorés) ; mesures dans
  `blocked007a-lotC-fidelity-gate/cleanup.json`. Story publique : [RE-948](../RE-948-blocked-007a-spu-kernel-rfe.md).
  Aucun commit/push.

## Acceptation globale du relais

- [x] Acquis BIU/cache et limites relevés dans les HANDOFF existants, sans les revendiquer comme nouveau replay.
- [x] Suite séparée en lots A, B et C avec dépendances et critères explicites.
- [x] Lot A accepté : SPU minimal et prochaine frontière attestée (`DIVU` `0xbfc07668` ; revue PASS).
- [x] Lot B accepté : handler RAM (`0x2700`) et retour RFE (`0x29d0`) obtenus sans injection, dans un scope explicitement borné (revue PASS).
- [x] Lot C accepté : verdict de fidélité/intégration indépendant et limites persistées (`integration=false`, `production_patch=false` ; revue PASS).
- [x] Nettoyage de chaque lot achevé ou report motivé avec preuve (`cleanup.json` ; aucune suppression, aucune archive modifiée).

**Ne pas fermer BLOCKED-007 sur le seul franchissement SPU.** Un lot peut être livré PASS fini tandis que le parent reste partiellement bloqué. CD naturel, GPU, audio complet, reset matériel, BIOS Sony et gameplay global sont hors acceptation de ce relais sauf nouveau périmètre expressément approuvé.

## Nettoyage du ticket documentaire

DONE : création d'un unique document de relais, aucun build/runtime/recherche ni suppression d'archives. La copie temporaire de transport est supprimée après écriture et contrôle de lecture. Aucune récupération d'espace significative n'est revendiquée. Aucun commit/push demandé ou exécuté par ce ticket.
