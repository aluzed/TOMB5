# RE-747 — Transaction cible de préparation et relocation du module de niveau

## Statut et progression

**Preuve bornée acquise et revue ; aucun correctif de production justifié.**

- [x] Handoffs RE-745/746 et attribution RE-735 consommés ; sources inchangées.
- [x] Nouvelle inspection Ghidra en lecture seule, sans processus Java concurrent ni verrou de projet détecté ; marqueur final et sortie réussie archivés.
- [x] Test privé d'abord RED : API absente, puis contrat de comparaison hôte absent.
- [x] S_LoadLevelFile exécuté depuis son entrée jusqu'à l'instruction de dispatch indirect, avant son exécution.
- [x] LOAD_Start exécute sa logique cible d'allocation, lecture, transformation et libération ; frontières graphiques déclarées ci-dessous.
- [x] Relocation comparée à un interpréteur indépendant et à la vraie unité SPEC_PSXPC_N/FILE.C compilée en 32 bits.
- [x] Test de publication d'abord RED ; story et dashboard actualisés.
- [x] Revue indépendante favorable ; rejeu parent du test privé et des 1 201 tests publics réussi.
- [ ] Exécution du corps LoadLevel, retour du chargeur et durée de vie après dispatch.
- [ ] Comparaison de la transaction complète avec ROOMLOAD.C et backend hôte par défaut.

## Nouvelle preuve

Contrairement à RE-735, la relocation n'est pas appelée isolément avec un module déjà placé. Le véritable appelant sélectionne l'entrée de niveau, remet le tas à zéro, appelle LOAD_Start, charge le module dans le tampon graphique fourni puis appelle son relocateur. Le curseur sectoriel et le pointeur de dispatch sont produits par ces instructions, pas injectés après coup.

Une trajectoire normale, Name=0, est exécutée sur le même boot US PSX authentifié. L'en-tête du conteneur provient des secteurs ISO ; son placement initial dans la globale reste synthétique. Le module chargé concorde intégralement avec l'extraction privée RE-735, indépendamment retrouvée depuis l'entrée du conteneur et le volume d'images consommé par LOAD_Start.

| Observation | Résultat |
|---|---:|
| Sélection cible de l'entrée | 1 |
| Allocation puis libération temporaire dans LOAD_Start | 1 / 1 |
| Lectures cibles : images puis module | 2 |
| Appel cible du relocateur | 1 |
| Relocations interprétées, quatre catégories exercées | 263 |
| Catégories de relocation | 18 / 64 / 64 / 117 |
| Écarts entre module relocalisé cible, modèle et vraie TU | 0 |

Le descripteur de tas revient à l'état vide après la libération LIFO ; le suffixe du tas hors allocation temporaire reste nul. Le bloc temporaire libéré n'est pas déclaré effacé : LOAD_Start l'a transformé. Le module réside dans un tampon graphique distinct, pas dans cette allocation. Le module complet, sa table de relocation inchangée et une garde après le module sont contrôlés. Le pointeur chargé pour le dispatch correspond à l'entrée relocalisée attendue. Cela ne prouve ni toute la RAM ni le corps appelé.

## Comparaison hôte et limites

`SPEC_PSXPC_N/FILE.C` est compilé séparément avec ses en-têtes normaux, `DISC_VERSION=1`, `DEBUG_VERSION=0` et ABI **32 bits**, puis son vrai RelocateModule traite les octets authentiques au même placement synthétique. Les octets du module entier concordent avec le résultat cible. Il ne s'agit pas d'une copie de fonction dans le harness. Pas de passage sanitizer dans cette unité ; aucune équivalence de l'ABI native 64 bits ou de ROOMLOAD.C complet n'est revendiquée.

**Pas de preuve matérielle** : tas, pile, tampon graphique, préfixe vide, mode normal et globales de démarrage fournis par le probe. Les instructions du boot rencontrées sont authentifiées ; aucune instruction n'est patchée. Les corps de DrawSync, VSync, GPU_UseOrderingTables, PutDrawEnv, LoadImage et LOAD_DrawEnable sont remplacés par des retours explicites. CdControlB, CdRead et CdReadSync sont des frontières modélisées ; les transferts utilisent les vrais secteurs ISO. Aucune validation GPU, timing CD, interruption, erreur de lecture ou échec d'allocation depuis cet appelant.

Arrêt explicite par hook avant le dispatch : pas de démarrage réel, de corps LoadLevel, de LOAD_Stop ni de retour final. La première méthode d'arrêt Unicorn par adresse laissait le PC sur l'instruction précédente ; le hook d'arrêt explicite remplace cette méthode sans modifier le code cible. Les premiers RED établissent un contrat de recherche manquant, pas un défaut de production.

## Preuves et reproduction

Tout le brut reste ignoré dans `build/reverse/autonomy-20260908/re747-transaction/` : `InspectTransaction.java`, `headless.log`, `ghidra-transaction.txt`, `transaction.py`, `test_transaction.py`, `host.cpp`, `host-command.json`, `host-build.log`, `events.json`, `summary.json`, `red.log`, `host-red.log`, `green.log` et `docs-red.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260908/re747-transaction/test_transaction.py
python3 -m pytest tests/reverse/test_re747_transaction_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

Un test privé intégrant exécution cible et compilation hôte fraîche réussi ; **1 201 tests publics réussis** (suite emulator, publication RE-747 et dashboard), sans diagnostic. Le probe réutilise la classe CPU RE-746 et le décodeur ISO RE-745, sans appeler leurs gardes historiques ni modifier leurs fichiers. Sa propre garde fixe le HEAD initial RE-747 et expire le 8 septembre 2026 à 23 h 45 Paris. Elle n'est pas un guard complet de dérive des sources ; les sources sont vérifiées séparément par Git. Aucun asset ni adresse cible versionné. Aucun commit/push effectué.

Revue indépendante dans `review.md` ignoré : test privé rejoué avec compilation fraîche de `FILE.C`, ELF 32 bits et symbole contrôlés ; 51 tests de publication/dashboard réussis. Le parent a ensuite rejoué le test privé et les **1 201 tests publics**. Les compteurs exacts sont observés dans les résultats, mais ne disposent pas tous d'assertions dédiées ; le test public contrôle la publication, pas la preuve binaire.

## Handoff

Prochaine unité cohérente : franchir le dispatch dans LoadLevel avec les pointeurs et le curseur conservés, établir ses premières allocations et dépendances, puis comparer les vraies unités concernées. Ne pas transformer la concordance du relocateur en validation du chargeur hôte complet. La recherche reste autorisée jusqu'à l'échéance globale ; la présente unité s'arrête pour revue parent.
