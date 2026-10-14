# RE-951 — contrats audio provider/device : checkpoint metadata-only

## Tracker
| Étape | État |
|---|---|
| Contrats audio05/06/07 et revues indépendantes privées | PASS fini scoped |
| Publication documentaire auteur | Vérification metadata-only ; zéro nouvelle exécution CPU/TU |
| Revue indépendante des quatre hashes publics | PENDING — ne constitue pas une approbation publique |
| Global / procédure | NON PROUVÉ / INCOMPLETE ; strict passed=false conservé |
| Intégration | integration=false ; production_patch=false |

## Contrats revus
### audio05 — producteur worker, goal atomique, composition compteur
Cinq fonctions amont extraites exactement et sdlaudio.h complet, pas TU audio/SPU entière ; psxcounters.cc entier inchangé. 5 tests par suite, deux suites fraîches reviewer, 70 projections séquentielles sur sept fixtures speed (10 étapes), 82 lignes : 70 + 5 wait + 5 pending + 1 worker + 1 composition. Huit mutants rejetés par assertion. Worker réel sleep_until/advanceFrames, stop/join/restart discontinu ; configuration NTSC/VSyncWAfalse et delta CPU338688 construits, jamais replay CPU. Getter frames initialisé réellement ; wait charge triggered avant store goal ; advance compare le OLD fetch_add, égalité sensible, same-goal ne réveille pas encore. wait [128,0] contient un zéro littéral après join : PAS une mesure de done. HAS_ATOMIC_WAIT=1, un writer choisi ; pas fallback/wrap/concurrence globale. scheduleInterrupt exact exécuté ; pending initialfalse et exchange fixtures, pas branchTest ni IRQ interrupt réel. Constructor bypass et uninit stop-only.

### audio06 — callback exact, vrais rings et SDL stream
Callback extrait exactement avec header/Circular réels ; SDL3 3.2.28 stream compilé et utilisé réellement. 64 cas, 65760 scalaires stéréo et 66016 assertions de champs ; deux observations wait et 40 répétitions supplémentaires reviewer. Six mutants par assertion. n0/1/3/2051, speed1/3, mono/mute/NullSync ; requête non-frame et chunks discriminants, résidus/clock comparés par files indépendantes. Invocation directe callback, constructeur bypass/settings construits/uninit stop-only : pas device naturel. FAIL UBSan initial null-source memcpy length0 de fixture conservé ; fixture vide à pointeur valide GREEN ensuite, callback source inchangé. SDL lié non instrumenté par UBSan ; pas validation sanitizer universelle.

### audio07 — causalité constructeur/événements/device
sdlaudio.cc lignes32–420 exactes, header complet, vrais Settings et EventBus intrusif ; pas TU audio entière, System façade, logger réel, Lua abort-only et ADPCM hors chemin. JSON Backend dummy, Device invalide, Speed1 construits ; NullSync defaultfalse réellement lu. Chaîne constructor → SettingsLoaded(false) → init → Run/Pause/Run → vrai callback device SDL → wait goal. Deux devices logiques dummy réels, silence sous-flux, aucun ring feed/sample comparé. 12 GREEN et 180 propriétés relationnelles (15/run), timings/frames non comparés à des constantes archivées. Deux mutants pause/reset rejetés par assertion ; no_advance exit7 TIMEOUT est contrôle causal SEULEMENT, pas mutant sensible par assertion. Pas injection frames/deadline/pending CPU.

## Frontière et licences
NATURAL_SYSTEM_SETTINGS_LOAD_VIDEO_CONFIG_AND_CPU_AUDIO_COUNTER_CONSUMER

Le frontend construit progresse, mais System settings load naturel, config vidéo et consumer CPU audio-counter restent non prouvés. CPU inchangé : aucun gain CPU attribuable, branchTest03 NON CERTIFIÉ, aucun CD callback/secteur, reset Sony, gameplay ou hardware. PASS fini ≠ global ≠ procédure ≠ intégration. PC et clock privés ne sont pas publiés.

Redux c313b116e6a55786bc127c9b3a07a90b55d97c21 GPL-2.0-or-later ; nugget historique MIT uniquement ; Circular MIT ; SDL3 3.2.28 Zlib. Noms, compteurs et hashes seulement ; aucun code GPL copié, dump, opcode ou adresse brute.

## FAILs et budgets préservés
05 conserve setup ERROR et lacunes bootstrap/wrong-lock/nested-recorder. 06 conserve FAIL UBSan première fixture et seal initial rejeté pour symlinks, retry distinct ; durées tâche510.88/outer510.93 >480. 07 conserve erreurs initiales et holder mutation expiré/absent au postcheck d’écriture ; réparation ultérieure ne rétrocertifie pas cet intervalle. Durées tâche564.78/outer564.82 >480, sous600. Revues06 323.50/323.55 et07 226.74/226.78 séparées. Les strict verdicts des trois reviewers sont false, procédures INCOMPLETE : jamais blanchis par acceptance finie true.

## Gate indépendante
Auteur self-check metadata-only, review PENDING. La revue parent doit vérifier exactement les quatre chemins/hashes finaux, schéma récursif exact (bool ≠ int), compteurs/pins, contenu safety et tous liens locaux ; reconstruire le prédécesseur RE950 byte-identique par retrait du seul suffixe RE951 ; exécuter tests951/950/949 dans un export public-only sans preuves privées. Cette vérification ne refait ni source TU ni CPU. Parent a authentifié inventaires187/144,2747/2834,114/153 ; auteur vérifie seals/counts et membership/hash/taille des HANDOFF/verdict/acceptance/scopes/audit sélectionnés, pas inventaire raw intégral. Seule une décision indépendante distincte peut accepter ces hashes publics ; elle ne modifie pas les anciennes décisions et ne débloque pas l’intégration.

## Nettoyage
zéro suppression. Aucun stash/reset/clean/stage/commit/push, aucun sourceprod modifié, cache préexistant conservé, README et dashboards historiques inchangés. Ledgers privés prospectifs pour writers/output/export/tests sous mutex mutation canonique par opération ; repo lock parent vivant/contention jamais acquis ni tué. Découverte read-only et authoring temporaire initial exclus de certification exhaustive. Inventaire et HANDOFF terminés avant seal ; completion hors racine. Capacités mesurées privées ; pas de claim cleanup global.

## Mesures et liens publics
- [Métadonnées RE951](../reverse/generated/re951-audio-provider-checkpoint.json)
- [Dashboard RE951 versionné](../reverse/tomb5-progress-dashboard-re951-audio-provider-v1.html)
- [Tests publics RE951](../../tests/reverse/test_re951_audio_provider_checkpoint.py)
- [Story prédécesseur RE950](RE-950-cpu-timebase-root-counter-checkpoint.md)
- [Dashboard prédécesseur RE950](../reverse/tomb5-progress-dashboard-re950-cpu-counter-v1.html)

Prochaine action : prouver production naturelle System/settings/vidéo puis consumer CPU conservant sa provenance ; pas activation spéculative.
