# RE-750 — Première salle et consommateur borné des roomlets

## Statut et progression

**Preuve différentielle bornée acquise ; aucun correctif de production.** Extension de RE-749, publication metadata-only. La qualification est locale au consommateur observé, pas une certification des 24 mots comme pointeurs.

- [x] Probes, assertions, provenance et dépendances examinés indépendamment.
- [x] Rejeu frais avant publication : 4 tests privés réussis, compilation réelle de la TU.
- [x] Première salle : data/door/floor/light/mesh reconstruits sur cible et host.
- [x] Consommateur : chargement du compte et trois tranches scalaires indépendantes.
- [x] Comparaison des résultats conservés et audit différentiel additionnel avec RE-749.
- [x] Publication TDD : RED constaté sur story absente, puis GREEN documentaire.
- [ ] Boucle complète du consommateur, corps GTE et atteignabilité depuis le renderer.
- [ ] Salles suivantes et dépendances natives après la boucle des salles.

## Extension réellement exécutée

Cas normal unique Name=0, secteurs authentiques, état initial synthétique. Le trajet S_LoadLevelFile → dispatch → LoadLevel conserve CPU/RAM/curseur sans reset entre appelant et suffixe. Boot et module authentifiés ; image relocalisée entière comparée à une relocation indépendante. Instructions rencontrées authentifiées, aucune instruction cible patchée. Les classes Target/ISO historiques sont réutilisées sans appeler ni désactiver leurs gardes historiques.

RE-749 s'arrêtait avant door. Ici la cible s'arrête **avant la deuxième salle**, après les cinq champs data/door/floor/light/mesh de la première, avec compteur de salle et prochain curseur vérifiés. Le buffer roomInfo entier correspond aux secteurs d'entrée avec **29 mots** transformés : cinq champs et les 24 ajouts. Comparaison additionnelle avec le résultat conservé RE-749 : seuls les quatre nouveaux champs door/floor/light/mesh diffèrent ; frames finales identiques.

| Observation | Résultat |
|---|---|
| Allocateur | 5 allocations, 3 libérations ; deux allocations persistantes |
| Entrées | 7 buffers utiles complets, 680 secteurs |
| Frames / roomInfo | 329 832 / 524 000 octets ; 116 salles, structure de 80 octets |
| Host/cible | Buffers entiers, état final, cinq champs et prochain curseur normalisés concordants |
| Descripteurs | Complets normalisés avant/après allocations et libérations, puis état final ; pas aux retours des lectures host |

## Qualification des 24 mots : portée exacte

Le compte lu vaut deux : **2 entrées actives**, **22 mots** hors de ces entrées. Les pointeurs actifs sont dans le bloc data ; les ordinaux **4, 16 et 24** restent hors allocation roomInfo après transformation. Cela ne prouve ni qu'ils sont des pointeurs utiles, ni leur innocuité pour tous les consommateurs.

Le consommateur est exécuté par **CPU/RAM frais** pour chaque tranche, avec le buffer produit copié et les compteurs/curseurs de frontière fournis explicitement. Une tranche charge réellement le compte ; trois autres testent les comptes restants deux, un et zéro. Les deux premières déréférencent respectivement les entrées un et deux. À compte zéro, le **troisième** mot est chargé dans le **delay slot**, mais sa valeur n'est pas déréférencée avant l'arrêt, situé avant l'écriture de sortie. Les lectures observées sont comparées exactement, sans filtrage limité au buffer.

**GTE non exécuté** : ni boucle complète, ni renderer complet, ni transition réelle entre ces états de frontière. Le décrément/backedge est authentifié statiquement, non exécuté dans ces tranches. Les mots hors allocation ne sont pas sélectionnés dans les cas exécutés ; aucune preuve universelle de non-déréférencement. Aucun différentiel natif de ROOMLET1.C revendiqué.

## Vraie TU et borne native

Compilation fraîche de **GAME/SETUP.C**, distincte du harness, ABI **32 bits** i386 O0, en-têtes normaux, DISC_VERSION=1, DEBUG_VERSION=0, PSX_VERSION=1 et PSXPC_TEST=1. Tailles pointeur/long, Level et room_info vérifiées. LoadLevel et LoadSoundEffects ne sont pas recopiés ; allocation/CD/GPU/SPU sont des doubles host.

GDB s'arrête par breakpoint matériel à la première ligne du corps de la deuxième salle, avec i=1 et j=24 ; les captures confirment les cinq champs et le prochain curseur. L'inférieur est ensuite détruit, sans retour LoadLevel. Un second breakpoint protège l'après-boucle. Le commentaire initial du harness mentionne encore l'ancienne borne « avant door » : c'est un libellé périmé, pas la borne exécutée ; le contrôle GDB et capture.py font foi.

Le lien conserve **`--unresolved-symbols=ignore-all`**. Le désassemblage frais montre toujours des écritures absolues nulles après la boucle des salles. Ne pas exécuter hors debugger ni prolonger la borne sans résoudre ces dépendances. Deux warnings extern-initialized historiques et -Wno-narrowing ; **pas de sanitizer**, ni sûreté mémoire générale, ni égalité de tous les registres/RAM revendiquée. Les compteurs sont des visites du hook, interceptions et arrêt inclus, pas des instructions retirées.

## Revue indépendante et provenance

Revue indépendante du 9 septembre 2026, démarrée à 08:52 Paris. Exécution fraîche avant toute modification suivie : **4 tests en 24,773 s, tous réussis** (garde, producteur, host, consommateur). Le producteur est rejoué trois fois par cette suite ; une compilation native fraîche. **41 fichiers** JSON/CSV/bin comparés à leur sauvegarde pré-rejeu, tous identiques ; ce nombre comprend des métadonnées conservées, pas 41 nouvelles exécutions. Les 24 lignes qualification.csv correspondent champ par champ au résultat consommateur frais. Aucun écart comportemental trouvé dans cette portée.

Preuves privées : `build/reverse/autonomy-20260909/re750/`, notamment `review-fresh-tests.log`, `review-audit.json`, `review-baseline/`, `host-command.json`, `host-output.log` et `consumer-summary.json`. Python optimisé a été rejeté réellement, journal `review-optimized-rejection.log`.

La garde vérifie le **HEAD prépublication**, les différences suivies/indexées contre HEAD, 19 dépendances épinglées, l'ignorance du probe et la fenêtre du 9 septembre jusqu'à 23:25 Paris. Elle est vérifiée à l'import/début des runs, pas continuellement ; les fichiers non suivis ne sont pas une garantie de propreté. La publication rend les anciens runs volontairement non rejouables tels quels : ne pas affaiblir la garde. Une nouvelle unité autorisée avec provenance propre serait requise.

```sh
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python -m unittest discover -s build/reverse/autonomy-20260909/re750 -p 'test_*.py' -v
python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

Le test public est uniquement documentaire, pas une preuve binaire. RED observé : une assertion « publication missing ». Les résultats GREEN et de régression sont archivés dans `publication-green.log` et `publication-suite.log` du dossier privé.

## Limites et Handoff

Pas de preuve matérielle, boot complet, timing, concurrence, audio/GPU réel, erreurs ou autres niveaux. Pas de retour final du chargeur, ni de validation sémantique de tous les champs reconstruits. Comparaisons des buffers utiles entiers, pas des octets adjacents ni de tous les accès du producteur. Aucune correction spéculative du commentaire critique de production.

## Handoff

Étendre une unité bornée aux salles suivantes et/ou établir le trajet réel du consommateur au-delà des tranches scalaires, avec dépendances et état explicités. Ne pas remplacer la preuve manquante GTE par une conclusion de sûreté. Dashboard actif mis à jour ; historiques figés et production inchangés. Vérification parent effectuée : 41 fichiers privés comparés octet pour octet à la sauvegarde indépendante, tous identiques ; journal des 4 tests privés et synthèse host contrôlés. Aucun nouveau rejeu binaire parent après publication (gardes prépublication préservées). Suite publique rejouée par le parent : **1 204 tests réussis en 50,82 s**, avec la commande ci-dessus ; `git diff --check` propre.
