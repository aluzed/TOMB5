# RE-788 — Registration réelle source → roof → plafonds bridge

2 octobre 2026. Baseline de reprise `22f190ea`, comparaison locale GETSTUFF `243c16ac` avec les autres TUs courantes. Statut : **preuve source-only synthétique validée ; aucun nouveau correctif moteur**. Backend **PSX_VERSION && PSXPC_TEST**, g++ Linux **i386**. Cette unité répond au handoff RE-787 côté source sans prétendre atteindre la registration depuis le démarrage ou le gameplay.

## Tracker
- [x] Date et absence de propriétaire concurrent contrôlées ; verrou exclusif `build/reverse/autonomy-repo.lock` acquis par le coordinateur.
- [x] Quatre tests écrits avant runner/harness : RED initial pour absence des fichiers, conservé.
- [x] ObjectObjects réel installe les six slots bridge et MIP 3072 : deux états loaded, slots empoisonnés, voisins et table objects complète contrôlés. Les pointeurs attendus ne sont jamais recopiés dans la table réelle.
- [x] Composition réelle GetCeiling → adaptateurs BRIDGE_CALLBACKS → trois corps ceiling OBJECTS ; ordre entrée/sortie et accumulateur observés sans callback de fixture substitué.
- [x] Quatre matrices fraîches current/baseline × normal/UBSan strict, **13824 cas chacune**, quatre tests pytest PASS. Baseline : **3456** entrées divergentes, **zéro divergence de retour** ; current : zéro écart dans les champs vérifiés.
- [x] Revue indépendante source PASS borné, quatre compilations/exécutions matrices neuves ; empreintes des trois fichiers vérifiées par le coordinateur.
- [x] RED documentaire trois absences, puis quatre guards historiques RED après append ; uniquement RE788 explicitement exclu de ces guards, digests historiques inchangés et nouveaux bytes protégés par le guard RE788.
- [x] Sélection héritée RE787 étendue aux sept nouveaux tests RE788 : **122 tests PASS en 17,16 s**, exit 0, aucun document réécrit par la suite (`re788-suite.ledger.json`). Pas suite globale.
- [x] Tracker/dashboard append-only et revue metadata-only persistée.
- [ ] Atteinte naturelle de la registration et de ces callbacks depuis le jeu ; preuve cible de cette nouvelle composition ; autres ABI/rotations/traversées : non validées.

## Ce qui progresse réellement
La fixture RE-787 plaçait un adaptateur dans une table construite. Ici, la vraie TU SETUP exécute **ObjectObjects**, puis GetCeiling utilise les slots effectivement installés, les adaptateurs de production et les vrais corps BridgeFlatCeiling, BridgeTilt1Ceiling et BridgeTilt2Ceiling. Aucun slot n'est réassigné après registration. Les six TUs complètes sont compilées avec headers normaux et liées normalement, sans symboles non résolus ignorés. Ce sont des exécutables de test neufs, **pas un fullbuild moteur**.

Cohorte exacte : deux états loaded × six types roof × 32 valeurs du premier champ et second décalé de 17 modulo 32 × deux coordonnées qui distinguent les diagonales × trois familles bridge × trois requêtes sous/égale/au-dessus du seuil × deux états inhibition = **13824 cas par matrice**. Les deux champs sont sélectionnés selon le type et la coordonnée. Rotations nulles uniquement ; frontières diagonales, couples offset exhaustifs, traversées sky/pit et corpus réels exclus. Les floors sont enregistrés et leur identité contrôlée, mais seuls les trois chemins ceiling sont exécutés.

La baseline transmet un surplus de 65536 sur certains offsets négatifs : **3456** cas observés à l'entrée de l'adaptateur réel puis à l'entrée du corps. Dans cette cohorte les bridges écrivent surface + 256 uniquement lorsque la requête dépasse leur surface ; sinon le retour short masque le surplus. Donc **zéro divergence de retour**, même pour la baseline. Ceci ne reproduit pas les 309 écarts de retour de RE-787 avec TwoBlockPlatformCeiling et **ne prouve pas un impact gameplay des bridges**. L'entrée fautive demeure sensible et la correction RE-787 l'élimine ici aussi.

## Observation, invariants et validation
Les hooks compilateur observent les frames cdecl des deux seules TUs OBJECTS et BRIDGE_CALLBACKS instrumentées ; options O0, frames conservées, i386. Ordre attendu : entrée adaptateur, entrée corps, sortie corps, sortie adaptateur. Ce mécanisme est dépendant du compilateur/ABI, pas une API portable ni une trace exhaustive des stores. La revue a inspecté les frames réellement compilées. La fixture compare intégralement les tableaux objects, rooms, cells, items, floor-data, bones, lara et ItemNewRooms qu'elle possède, ainsi que les globals sélectionnés ; **pas toute la mémoire moteur**.

Archives privées : `build/reverse/autonomy-20261002/re788-source/`. RED initial quatre absences ; compléments RED séparés pour globals de registration, hauteur de requête et coordonnées discriminantes ; versions GREEN antérieures ne sont pas attribuées au contrat final. Le child a atteint son timeout de 600 secondes après sa dernière correction ; le coordinateur a récupéré les fichiers et refait **4 tests PASS en 2,79 s**, exit 0. Ce timeout n'est pas une fin de la fenêtre d'autorisation.

Revue indépendante : `build/reverse/autonomy-20261002/re788-review/verdict.json`, **4 tests frais PASS en 2,77 s**, exit 0 ; recomptage des lignes, logs bruts, hashes des sources/153 headers/binaires et observation cdecl. Résumé public sûr : `docs/reverse/generated/re788-source-review.json`, empreintes des trois fichiers sous test. Le reviewer a vérifié le modèle source et les archives produites par ses nouveaux runs, **pas exécuté de cible MIPS pour cette unité**.

**pas de runtime jeu**, pas de relink/fullbuild, donc aucune nouvelle capture de jeu ; **pas de GREEN global** sanitaire ou gameplay. Aucun asset, dump, instruction ou pseudocode original versionné. Les deux suppressions utilisateur et le rapport non suivi sont préservés, pas restaurés ni embarqués. Les anciens échecs runtime ne sont pas levés par ces tests.

## Handoff — RE-789
Blocage restant : la registration est une vraie exécution de source mais son invocation par le harness et les rooms/items/triggers sont synthétiques. Critères de reprise : identifier dans le binaire natif frais un producteur réellement atteint, suivre un callback enregistré et ses préconditions via une route naturelle ou un préfixe authentifié clairement borné, distinguer argument sensible et résultat effectivement consommé. Capturer/inspecter/livrer directement toute nouvelle capture lors d'un runtime. Ne pas patcher le moteur sur la seule divergence d'entrée masquée au retour.

Prochaine unité **RE-789** : attribution de la route producteur/consommateur réellement atteinte, ou preuve cible continue de cette composition si aucune route naturelle sensible n'est disponible. Aucun GO supplémentaire nécessaire avant l'échéance autorisée du 2 octobre à 23h ; chaque reprise doit vérifier heure, propriétaire et handoff. Après checkpoint le cron peut reprendre mais n'établit pas un travail sans pause. Les anciens handoffs datés restent historiques.
