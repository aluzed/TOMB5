# RE-789 — Cible : registration → roof → callbacks bridge réels

2 octobre 2026, parent RE-788, baseline publique `52187daa`. Statut : **composition authentifiée bornée validée en RAM synthétique**, aucun nouveau patch moteur. Cette unité lève l'absence de comparaison cible de RE-788 pour sa cohorte ; elle **ne lève pas l'atteinte naturelle ni le gameplay**.

## Tracker
- [x] RE-788 livré, preuve source et handoff relus ; même propriétaire exclusif, date contrôlée avant commandes.
- [x] Premier essai cible réellement exécuté : dépendance capstone absente, exit 1 avant extraction, zéro cas ; snapshot et log d'échec conservés. Installation isolated venv Unicorn/Capstone, aucun asset public.
- [x] Boot extrait du disque et authentifié fraîchement ; 15 copies identiques du module SETUP, vraie relocation exécutée, puis préfixe de registration réel à base synthétique.
- [x] Deux préfixes loaded : slots empoisonnés remplacés par les six vrais callbacks, RAM finale complète conforme ; aucune substitution des slots après préfixe.
- [x] **13824** queries GetCeiling → trois vrais ceilings et helper GetOffset : instructions visitées authentifiées, CPU/RAM restaurés par cas, arguments et sorties observés ; run parent exit 0 en 24,03 s.
- [x] Revue indépendante PASS borné : replay neuf **13824** en 23,75 s, deux préfixes rejoués séparément, comparaison exhaustive aux deux matrices source courantes archivées, zéro écart dans la projection définie.
- [x] Contrat metadata-only et fingerprint ordonné cible ; RED public avant artifacts, puis compilation native fraîche current/baseline × normal/UBSan, cinq tests ciblés PASS en 2,81 s avant inscription documentaire.
- [x] Cinq guards historiques RED après append, puis GREEN avec seule section RE789 explicitement exclue et digests anciens inchangés. Guard RE789 protège tous les bytes précédents.
- [x] Sélection héritée RE788 étendue aux sept tests RE789 : **129 tests PASS en 19,94 s**, exit 0, aucun document réécrit par la suite (`re789-suite.ledger.json`). Pas suite globale.
- [ ] Route réelle depuis le démarrage, rotations autres que zéro, floors exécutés, traversées/corpus et hardware : non validés ; RE-790 reste ouvert.

## Preuve nouvelle et comparaison directe
Le préfixe authentifié de SETUP installe les callbacks. Les queries suivantes conservent ces slots : seuls les pointeurs de fixtures floor-data/items sont préparés, pas les callbacks. La cible exécute continûment GetCeiling et les vrais BridgeFlatCeiling, BridgeTilt1Ceiling, BridgeTilt2Ceiling ; les deux derniers passent naturellement par GetOffset. Aucun faux retour/callback de service introduit.

Même matrice ordonnée que RE-788 : deux états loaded × six types roof × 32 premiers offsets et second décalé de 17 modulo 32 × deux coordonnées discriminantes × trois familles × seuils sous/égal/au-dessus × inhibition = **13824 queries**. Parmi elles 6912 appellent un corps ; entrée/sortie donnent 13824 événements, distincts des queries. Le helper comporte **4608** visites observées. Le champ historique `helper_entry_candidate` du probe désigne une instruction interne de delay slot, **pas son entrée** ; la revue a authentifié l'entrée réelle et les appels. Pas de surestimation de fonctions ou d'instructions retirées.

Chaque préfixe : **148 visites** de hook, **46 événements d'écriture**, 130 octets modifiés ; le replay indépendant conserve images avant/après. Les 4945 visites du relocateur et les visites des queries ne sont pas comptées comme instructions retirées. Les autres zones sont initialement synthétiques, certains états hors slots zéro ; pas preuve de tous effets sur des états initiaux arbitraires.

La revue compare directement toutes les lignes cible et source current normales/UBSan : clés, entrées corps, sorties corps, appels et retour final short concordent. Les adaptateurs natifs n'ont pas de correspondant ABI séparé dans le binaire PSX : leur égalité au corps est contrôlée côté source, puis projetée vers les événements corps cible. Les autres effets de SETUP diffèrent entre architectures et ne sont pas normalisés pour prétendre une RAM moteur équivalente.

Baseline GETSTUFF `243c16ac` avec autres TUs courantes : **3456** entrées divergentes par mode ; 1152 masquées par l'écriture du callback, 2304 uniquement par le retour short. **Zéro divergence du retour final**. Ne pas confondre ce masquage avec une correction complète ni avec les retours sensibles de TwoBlockPlatformCeiling en RE-787. Les cas inhibés ne fournissent pas d'observation d'entrée callback.

## Contrat rerunnable et limites
`docs/reverse/generated/re789-target-composition-proof.json` conserve comptes, scopes et hashes sûrs. Fingerprint SHA256 du JSON compact ordonné : neuf champs de clé, entrée corps ou null, nombre d'appels, sortie corps ou null, retour short réel. Le contrat est dérivé du replay indépendant approuvé, pas d'une formule source inventée. Les nouveaux tests compilent à nouveau les six TUs réelles via le runner RE-788 : current doit égaler le fingerprint ; baseline doit être rejetée pour son entrée fautive, même si son retour final concorde. Les preuves cibles brutes restent privées ; ces tests publics ne rejouent pas le disque.

Chronologie conservée : cinq RED initiaux avant metadata/story ; premier checker public a confondu colonne événement et hauteur de requête, deux échecs de schema conservés, correction du checker sans changer le résultat cible ; contrôle baseline RED avant branchement de la baseline réelle, puis cinq ciblés PASS. Ce n'est pas un RED de production et aucun patch moteur n'est motivé par ces incidents.

Archives `build/reverse/autonomy-20261002/re789-target/` et `re789-review/`. Revue `re789-review/verdict.json` relue, 61 empreintes effectivement vérifiées par le coordinateur. Rejeu cible neuf du reviewer et trace séparée du préfixe ; source courante **archivée** dans cette revue, puis **compilée fraîchement par les nouveaux tests publics**. Full RAM query finale comparée hors 96 octets de pile ; SP/RA et trois registres sauvegardés contrôlés, pas tous registres ni stores transitoires. Unicorn logiciel, pas oracle matériel. Zéro rotation seulement, pas traversée.

**pas de runtime jeu**, pas relink/fullbuild, donc pas capture neuve ; **pas de GREEN global** sanitaire/gameplay. Sources moteur inchangées. Les suppressions utilisateur et rapport non suivi demeurent intacts, aucun ancien blocker ressuscité ; raw/assets/dumps/opcodes uniquement en build ignoré.

## Handoff — RE-790
La composition cible/source bornée est désormais directement comparée, mais on ne connaît toujours pas une route naturelle sensible où le jeu installe puis consomme ces callbacks. Critères : binaire moteur frais ou relink attribué, observation du producteur et du callback via des entrées réelles, préconditions rooms/items/flags et consommation observable séparément. Tout runtime nécessite capture, inspection et livraison MEDIA directe. Ne pas multiplier la même matrice pour remplacer cette preuve de reachability.

RE-790 : audit de l'atteinte naturelle du producteur/callback et de l'effet consommé ; si aucun cas réel n'est sensible, documenter ce blocage précisément et pivoter sur une divergence utile. Reprise autorisée sans GO supplémentaire jusqu'au 2 octobre23h, avec date/propriétaire contrôlés ; pas de nouvelle exploration après l'échéance. Checkpoint d'exécution ≠ travail sans pause garanti.
