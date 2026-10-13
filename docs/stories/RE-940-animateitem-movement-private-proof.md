# RE-940 — mouvement AnimateItem : preuve privée, régression publique exécutable

**PUBLICATION_REVIEW_REQUIRED — integration=false, production_ready=false.**

## Tracker
- DONE : nouvelle branche nonstationnaire sans gravité, huit fixtures construites ; preuve privée producteur/reviewer acceptée dans son domaine fini.
- DONE : publication authored C++/Python ; builds publics frais du CONTROL.C courant complet, candidat test-only remplaçant AnimateItem seul, table réelle CAMERA.C et CONTROL_S.C réels.
- OPEN : revue indépendante des hashes exacts de cette publication. Aucun commit/stage/push autorisé ici.
- BLOCKED : provenance naturelle RE939, startup/gameplay, activation production. AnimateItem reste UNIMPLEMENTED.

## Reproduire sans données privées
Depuis la racine : `python3 -B tests/reverse/test_re940_animateitem_movement.py`.
Prérequis publics : compilateur C++ compatible GCC avec multilib i386, headers SDL2 et GLEW. Aucune dépendance aux inputs ignorés, assets, binaire cible, Unicorn ou venv ; temporaires supprimés par TemporaryDirectory. Le test reconstruit huit buffers complets de 16716 octets (ITEM144, ANIM80, CHANGE12, RANGE32, COMMAND64, TRIG16384), ne publie pas ces buffers.

Les tests Python sont GREEN parce qu’ils exigent **baseline comportementale RED8**, candidat normal/strict **GREEN8**, puis deux mutants causaux **6 différences / 2 contrôles chacun** ; ils ne prétendent pas avoir intégré AnimateItem. Le candidat inclut assertions de fixture et domaine fini, sans gravité, animation0, zéro commandes/changements et frame interne. Le produit latéral X écrasé est conservé conformément à l’attribution privée, non corrigé intuitivement.

## Empreintes reconstructibles et attribution
SHA256 concaténation ordonnée des huit inputs : `bc0206e069646c4e98cd25403e9928b731e3458bfd9ff567df328955c601f4bd`.
SHA256 concaténation ordonnée des huit expected : `51f8f6e630819f938dfa23a6b018fc655924b984d1c05acfe773eb35a6c9eb12`.
Le checker Python reconstruit ces empreintes avec arithmétique largeur32/narrowing16 et la table repo source, indépendamment des sorties du candidat. Pins dérivés des buffers target-approved archivés, pas réponse simulée ni copie de code cible.
Verdict reviewer privé SHA256 : `a41f4eca43f6c6822d452689034ba833959e3f838d48c401918e33567ff96257` ; candidat privé accepté : `efea3c9b4c882e59da942e38fd3f04af42f632c2fc5349fdc422236a7c488b4e`.
Parent a authentifié seals/membership producteur193/reviewer241. Publication vérifie les membres sélectionnés ; aucune revendication de nouvel audit intégral privé.

## Résultats et limites distincts
La preuve cible est **archivale** : huit retours et801 visites hooks, non instructions retirées. Cette publication ne rejoue ni cible ni ancienne matrice ; les builds actual-TU publics sont un nouveau livrable frais.
Domaine construit : GP/SP/RAM, frame interne, pas provenance naturelle. Oracle logiciel entier et table authentifiée commune ne sont pas preuve hardware. Native projection des régions complètes sélectionnées, pas toute RAM ni trace stores transitoires. Le test observe pointeurs globaux inchangés ; events non revendiqués.
ABI i386/GCC O0 ; conversions unsigned vers signed et shifts négatifs implementation-defined ne constituent pas équivalence universelle. Strict ASan/UBSan fail-fast, leaks désactivés, pas GREEN global. Commandes1..6, changements, fin-frame/linking, gravité, object metadata et corps général exclus.
**globalprocedure.passed=false** conservé : bootstrap/transport/host et liveness de chaque ancien writer non exhaustifs. Le PASS privé fini n’efface pas ces réserves, ni la revue publique PENDING.

## Cleanup et suite
Cleanup logique DONE : aucun patch production ni résidu d’activation. Cleanup disque DONE : temporaires de tests supprimés, preuves essentielles/RED et logs conservés, zéro suppression des archives historiques ; aucun gain net revendiqué. Mesures avant/après, manifest public allowlist, HANDOFF et seal sont privés et ne sont pas une acceptation indépendante.
Prochain travail unique, non autorisé implicitement : commande4 end-frame, attribution de flags/status et ABI objet avant nouvel oracle/actual-TU ; ne pas présenter la répétition de ces huit fixtures comme nouvelle preuve cible. RE930 BIU/kernel/SPU et unité historiquement provider-refused horsscope.

[Dashboard RE940](../reverse/tomb5-progress-dashboard-re940-v1.html)
