# RE-772 — Build complet → runtime observable, sans patch

Publication documentaire du 13 septembre 2026, Europe/Paris. **Le build/runtime observable progresse : build64 complet mais crash LoadLevel ; build32 complet avec GLEW privé et fenêtre réelle de 30 secondes sans SIGSEGV observé. Le menu interactif et gameplay non validés restent la limite centrale.** La revue finale de publication PASS au snapshot du 13 septembre 2026 à 11:16 Europe/Paris est distincte des résultats runtime archivés.

## Overview actif et résultat intégré

Cet overview actif remplace la lecture opérationnelle du jalon précédent, sans réécrire son historique. Après RE-771, ce jalon réunit build complet, démarrage graphique, capture réelle et premier obstacle observable ; il ne découpe pas une nouvelle série de microtickets. Même HEAD court d63b1440 pour les deux builds, source de production inchangée. Cible construite : TombRaiderChronicles_PSXPC_N, DISC_VERSION=ON, Debug ; DEBUG_VERSION reste une option séparée et vaut zéro dans le build64 documenté.

### Build64 : démarrage graphique puis crash

La preuve runtime-1049 établit un build64 ELF64 neuf, build exit 0 de 10:51:03 à 10:51:07. Le lancement Xvfb de 10:51:23 à 10:51:46 termine en exit 139, SIGSEGV avant la limite de 30 secondes. Le lancement de capture distinct termine en exit -11 côté application, malgré le wrapper exit 0. La capture privée à 20 secondes montre seulement le splash/logo doré et le copyright sur fond noir, sans options de menu ni scène jouable.

Le diagnostic est localisé dans LoadLevel, GAME/SETUP.C:1225, appelé par S_LoadLevelFile puis DoTitle. GDB exit 1 : le crash est capturé, puis la commande sizeof(ROOM_INFO) échoue parce que ce nom de type n’existe pas. La vérification séparée de struct room_info réussit : taille 120 octets et pointeur 8 octets. Les avertissements de fonctions non implémentées ne sont pas automatiquement la cause du crash. Les conversions 32-bit/adresses natives et le layout étayent une incompatibilité ABI, sans preuve générale ni autorisation de correctif source.

### Build32 : dépendance privée résolue, observation bornée

La première configuration -m32 dans runtime-1049 échouait faute de GLEW. Dans runtime-1058, apt-get update réussit, mais la simulation apt de libglew-dev:i386 échoue (exit 100) ; aucun apt install n’a été exécuté. GLEW 2.2.0 est ensuite fourni par compilation privée de l’archive officielle téléchargée, sans installation système ni symbole factice. Pas de certification indépendante de signature éditeur. Le premier argument CMake de bibliothèque partagée ne correspondait pas au FindGLEW du dépôt ; l’argument effectif GLEW_LIBRARY résout la configuration sans modifier ce module.

Le build32 ELF32 neuf, -m32, aboutit : build exit 0 de 10:59:33 à 10:59:38. Le log file/ldd identifie le binaire Intel 80386 et la bibliothèque GLEW ELF32 privée réellement résolue. Le lancement capturé de 10:59:52 à 11:00:22 dure 30 secondes et termine en exit 124 : limite temporelle atteinte, pas une réussite fonctionnelle. Le wrapper exit 0 signifie seulement que le dispositif de capture a terminé. Aucun SIGSEGV n’est observé dans cette fenêtre ; ce n’est pas la preuve qu’un crash ne surviendra jamais.

Le log atteint TRIGGERING TITLE SPOTCAM puis des itérations GLOBAL_PLAYING_CUTSEQ. La capture privée à 20 secondes montre le splash/logo, le copyright et un symbole circulaire, sans menu visible. Conclusion : menu interactif et gameplay non validés. Les données locales et la couche EMULATOR servent au binaire compilé depuis les sources, pas à une exécution de l’original présentée comme reconstruction.

Le diagnostic GDB distinct de 11:00:48 à 11:01:19 termine aussi en exit 124. L’échantillon est obtenu par SIGINT volontaire du timeout, pas par un crash et pas un deadlock démontré. La pile passe par pthread_cond_wait, Mesa/Gallium, GLX/SDL, Emulator_SwapWindow, Emulator_EndScene et DrawOTag. L’absence de menu validé reste l’obstacle observable, cause exacte non établie. GDB mesure pointeur 4 octets et struct room_info 80 octets ; le progrès 32-bit ne prouve pas la résolution de tous les défauts.

## Provenance et limites de cette publication

Références privées, sous /var/www/projects/TOMB5/build/reverse/autonomy-20260913/ :

- runtime-1049/RAPPORT.md ; runtime-1049/build64.json ; runtime-1049/launch64-xvfb.json ; runtime-1049/capture64-app.json ; runtime-1049/gdb64.log et gdb64.json ; layout64.log.
- runtime-1058/RAPPORT.md ; runtime-1058/glew-build32.json ; runtime-1058/configure32-private.json ; runtime-1058/build32.json ; runtime-1058/binary32-before.log ; runtime-1058/capture32-app.json et capture32-app.log ; runtime-1058/gdb32.json et gdb32.log.

Attribution de cette unité : publisher : lecture des rapports, logs et ledgers ; comparaison des hashes des manifestes privés et inspection visuelle des deux captures à 20 secondes. C’est une vérification documentaire et d’intégrité, pas un audit des buffers. Ici, aucun rejeu runtime, aucune recompilation du jeu complet, aucune nouvelle RE privée. Les builds, lancements et commandes système ci-dessus sont ceux des ledgers runtime antérieurs, non ceux de cette publication. Aucune vérification supplémentaire n’est attribuée au parent, ni aucune revue indépendante prétendue achevée au moment de la publication initiale. La revue documentaire indépendante ultérieure est archivée dans re772-review/RAPPORT.md et verdict.json ; 8 tests frais PASS, sans rejeu runtime.

Les captures restent privées : aucun asset public, aucune image embarquée ni diffusion HTTP. Limites : pas d’équivalence cible, pas de validation matérielle, pas de pourcentage global d’achèvement. La nouvelle preuve n’autorise pas de patch : source de production inchangée, code_change_readiness=blocked. Les preuves collision amont/cible GetHeight ne sont pas remplacées par ce runtime : la preuve authentique reste manquante.

## Vérification documentaire

Le test est écrit avant story et section active. RED setup documentaire : deux échecs attendus (story et section absentes), exit 1, dans re772-publication/red.log et red.json. Ce n’est pas un RED comportemental ni un défaut corrigé du jeu. Résultats exécutés : GREEN, 2 tests PASS en 0,06 s pytest, exit 0 (11:07:57) ; suite publique précédente exacte + nouveau test, 3767 tests PASS en 59,28 s pytest, exit 0 (11:08:01 à 11:09:01). Les fichiers green.log/green.json et suite.log/suite.json conservent sorties, argv, intervalles et hashes avant/après. Le test est byte-identique entre RED et GREEN. Les tests publics ne constituent pas un nouveau lancement du jeu. La sélection de suite est l’argv exact de re771-publication/suite.json, avec le seul test RE772 ajouté et basetemp relocalisé. Après cette inscription, la revalidation ciblée RE772/RE771/RE770/RE769 est consignée séparément dans final-doc.json et final-doc.log ; son résultat n’est pas présumé ici.

## Tracker

- [x] Build/runtime observable consolidé : crash 64-bit attribué, dépendance 32-bit résolue, lancement et captures réels bornés.
- [x] Logs, ledgers, manifestes privés et deux captures à 20 secondes inspectés, sans rejouer les preuves.
- [x] Overview actif et handoff actif placés dans la seule section RE-772 ajoutée à la fin du dashboard ; retrait de cette section restaure tous les bytes historiques et balises finales.
- [x] Revue finale : revue finale de publication PASS au snapshot du 13 septembre 2026 à 11:16 Europe/Paris.
- [ ] Menu interactif, niveau jouable et cause précise de l’absence de menu non établis ; pas de patch autorisé.

## Handoff

Après RE-772 — handoff actif : prochaine preuve utile à proposer séparément, un jalon intégré de démarrage 32-bit jusqu’à un menu réellement interactif ou un obstacle reproductible attribué, avec entrée, rendu et capture observables. Ce n’est pas une autorisation de lancer ce travail ni de corriger source/ABI. Après RE-771, la collision amont/cible GetHeight demeure également ouverte au sens de preuve manquante, pas de nouvelle exécution engagée. Aucun nouveau runtime, sujet privé, job, partage HTTP, staging ou commit dans cette publication. Revue finale de publication PASS au snapshot du 13 septembre 2026 à 11:16 Europe/Paris ; les résultats runtime ne valent pas approbation de la livraison documentaire.
