# RE-807 — Preuve privée bornée du consommateur commande animation 1

Auteur : AlexP — statut : progress, pas une livraison production.

## Tracker
- [x] Preuve producteur et revue indépendante consultées; verdict PASS strictement privé borné, 184 fingerprints vérifiés sur les octets réels par le worker publication.
- [x] Garde publication FIRST, RED observé avant métadonnées/story/section; empreinte de tous les octets précédents du dashboard épinglée.
- [x] Six cas de retour, 1080 visites authentifiées et 16716 octets de buffers complets dans la preuve revue archivée.
- [x] actual-TU privée : baseline RED six divergences normal/strict, candidat GREEN six cas par mode, mutant omission quatre divergences; contrôles zéro et trois PASS.
- [ ] Revue finale indépendante de cette publication et de ses digests par le parent.
- [ ] RE-808 : nouveau discriminant commande2 jump/gravity ou autre branche réellement nouvelle, planned-not-proven; ne pas répéter les matrices fermées.
- [ ] Intégration, activation AnimateItem/DoorControl, registration, readiness et gameplay : non autorisés.

## Portée exacte de la preuve revue
Six fixtures synthétiques, commande1 / TranslateItem seulement, counts zéro à deux, deux animations stationnaires sans gravité. Le consommateur end-frame sélectionne les commandes de l'ancienne animation; frame incrémentée avant comparaison à frame_end. Arguments signés, rotation et division entière par4096 exercés par le vrai helper, événement ordonné avec position AVANT chaque appel; changement d'animation après les commandes. Commande1 de la nouvelle animation seulement sautée pendant le parcours per-frame. Deux contrôles gardent des tables non-nulles sans appel (old0/new1, old2 avant end-frame); old2/new1 discrimine ordre et positions. Six appels au total, angles signés et masquage16-bit. Retour réel, restauration des registres ABI, CPU/RAM recréés pour chaque cas, borne2500 et limite Unicorn2s dans la revue; pas un replay frais effectué par ce worker.

GetChange non atteint ici malgré liaison réelle de la source courante corrigée; number_changes zéro. TranslateItem et table trig réels liés depuis les unités production, observation native via wrapper appelant le vrai helper sans simuler sa sémantique. ABI i386 ptr4/short2/int4, ITEM144/ANIM40/CHANGE6/RANGE8. Comparaison intégrale : ITEM144 + ANIM80 + CHANGE12 + RANGE32 + COMMAND64 + TRIG16384 = 16716 octets. Tables entières inchangées; RAM cible finale2MiB comparée hors pile caller36 octets. Aucune garantie des stores transitoires, pile exacte, mémoire native arbitraire, ni pointeurs natifs sérialisés.

## Résultats et causalité limitée
Revue indépendante : normal et strict ASan+UBSan fail-fast, baseline build0/run1 et six divergences; candidat build0/run0 et six PASS, stderr exécution vide. Baseline RED = stub AnimateItem entier, pas causalité TranslateItem isolée. Omission TranslateItem build0/run1, quatre divergences et deux contrôles PASS : discriminant spécifique. Candidat privé avec asserts sur fixtures, sans validation générale des commandes/pointeurs : pas un contrat de sécurité production. Aucun code source ni service hardware ajouté à cette publication.

## Incidents et limites honnêtes
MEM_WRITE : anomalie d'instrumentation Unicorn reproduite par la revue indépendante (visite retour dupliquée, boucle écourtée). Tentatives/échecs conservés dans l'archive; PASS limité aux hooks code+read déclarés. Aucune invariance sous instrumentation, aucune preuve write-hook ni couverture des stores transitoires.

stderr original indisponible : les stderr scellés producteur sont vides. Le ledger exit1 et les snapshots failed-first sont les originaux retenus; la revue a fraîchement reproduit l'échec de compilation faute déclaration externe TranslateItem. Ce diagnostic frais est conservé dans la revue, ne doit jamais être présenté comme le stderr original. Correction privée exactement limitée à l'extern. Première sonde ABI revue échouée pour macro PC_VERSION non définie puis corrigée, états conservés. Ces incidents ne sont ni supprimés ni réécrits par la publication.

Commandes2/4/5/6, gravité, mouvement général, loader et corpus gameplay exclus. Aucun fullbuild nécessaire pour ce checkpoint documentaire; aucun lancement jeu, aucune image runtime. AnimateItem et DoorControl non activés, aucun patch source ni intégration, pas de GREEN global. Le GetChange public courant doit être vérifié séparément par son unittest actual-TU, 1440 cas normal/strict : ce n'est ni la matrice cible RE807 ni une preuve d'activation des appelants.

## Préservation et calendrier
Section exactement nommée re807-private-animation-command, ajout nominatif dans le conteneur historique RE803 après RE805, sans modifier aucun octet antérieur; retirer uniquement cette section reconstruit exactement le dashboard entier antérieur. Exclusions RE807 nominatives dans gardes RE806/RE805/RE803 seulement après leur RED réel, sans affaiblir hashes source/provenance ou assertions comportementales. Stories/métadonnées historiques non éditées; BLOCKED001/002 restent supprimés, report-tech et index protégés. mutation.lock bref, repo.lock parent owner857519 non touché; aucun stage/commit/push. Autorisation Paris : recherche stop11:25, revue11:45, owner11:55, deadline12:00; budget worker550s et commandes bornées extérieurement.

## Frontière RE-808
planned-not-proven : commande2 jump/gravity ou autre nouveau discriminant atteint, oracle indépendant et nouveau RED/GREEN privé puis revue. Aucune répétition des matrices stationnaires/GetChange fermées, aucune autorisation d'intégration ou activation anticipée.
