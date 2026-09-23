# RE-775 — Avant et arrière observés dans une session continue du niveau

24 septembre 2026, Europe/Paris. **Après RE-774**, même binaire source ELF32 (`TombRaiderChronicles_PSXPC_N`) ; source de production inchangée ; `code_change_readiness=blocked`. Un lancement sous Xvfb et GDB suit, dans **la même session**, le niveau initial sans entrée, puis `IN_FORWARD`, une pause sans entrée, `IN_BACK`, enfin une seconde pause. Ce jalon établit une réponse directionnelle observable ; **gameplay complet non validé**.

## Preuve privée et comparaison

- Preuve primaire ignorée : `build/reverse/autonomy-20260924-runtime-0051/`, notamment `session.json`, `samples.jsonl`, `gdb.log`, `idle-settled.png`, `forward-held.png`, `idle-between.png`, `back-held.png` et `idle-final.png`. Le manifeste lie à une seule invocation Xvfb/GDB la touche C, les pressions et relâchements XTest, les captures horodatées et le hash du binaire déjà construit ; les échantillons GDB sont pris à l'entrée de `LaraControl`. **aucun asset public** : ni images ni binaire ni journaux bruts dans Git ou HTML.
- Après stabilisation, `input=0`, Lara est en chambre 0, z=31232 et la position reste constante sur les échantillons avant la première direction. Flèche haut tenue : `input=1` (`IN_FORWARD`), z atteint 38818 et Lara passe en chambre 2 ; la caméra change également de position et de chambre. Après relâchement, `input=0`, z reste à 38818 sur la fenêtre échantillonnée.
- Flèche bas tenue ensuite dans **la même session** : `input=2` (`IN_BACK`), z redescend jusqu'à 29797 et Lara revient en chambre 0. Au relâchement, `input=0` et cette position demeure stable sur les échantillons restants. Les changements de chambre sont observés dans le record natif ; ils n'établissent ni destination de scénario ni progression validée.
- Les cinq captures de fenêtre réelle existent et leurs empreintes correspondent au manifeste. Les pixels changent, mais l'analyse de pixels et l'OCR disponibles ne suffisent pas à déclarer le niveau **visuellement interprétable** ou le personnage correctement rendu. L'OCR relève parfois un texte de diagnostic caméra ; ce n'est pas une lecture fiable de la scène. La variation de caméra pendant l'initialisation sans entrée interdit de l'attribuer toute entière aux touches. **collision non prouvée** : les arrêts de z sous touche maintenue n'identifient pas un contact ou une décision de collision, malgré la stabilité observée.
- `gdb_wrapper_exit=124` : exit 124 de `timeout` qui borne le **wrapper GDB** à 150 secondes ; ce n'est ni une fin réussie de l'application ni un crash attesté. Les échantillons sont périodiques et aux transitions d'entrée, pas une trace exhaustive de chaque frame ou écriture. Le premier essai du jour (`build/reverse/autonomy-20260924-runtime-0047/`) pressait l'avant avant la première entrée dans le niveau ; son témoin arrière et son état initial sont conservés, mais ses mesures avant ne sont pas utilisées pour la comparaison principale. Une revue indépendante en lecture seule des preuves de la seconde invocation confirme cette attribution bornée ; elle n'a lancé ni jeu ni tests.

## Vérification et readiness

Test documentaire RE-775 écrit avant cette publication : RED observé, trois échecs attendus (story, section active et index absents), `red.log`, exit 1. Ce RED **documentaire** n'est pas un RED comportemental du jeu. Après publication, sélection RE-770→775 : **15 réussis** (`targeted.log`, exit 0). Suite fraîche `tests/reverse/` : **3338 réussis, 7 échecs** (`suite.log`, exit 1), exactement les sept noms déjà consignés en RE-774 (RE-165, RE-340, RE-699/700/701) ; elle n'est **pas verte**. Le seul CSV historique réécrit incidemment a été examiné puis restauré. La source de production et les marqueurs ne changent pas ; pas de correctif déduit de ce seul runtime. La preuve cible/ABI GetHeight et sa traversée complète demeurent ouvertes ; `code_change_readiness=blocked`.

## Tracker

- [x] Même binaire ELF32, session continue Xvfb/GDB, captures privées et commandes horodatées.
- [x] Témoin sans entrée, `IN_FORWARD`, témoin sans entrée, `IN_BACK`, témoin final observés dans `LaraControl`, avec z, chambre et caméra.
- [x] Revue en lecture seule de la preuve et RED documentaire avant publication.
- [ ] Collision non prouvée ; progression non validée ; rendu interprétable et gameplay complet non validé ; aucun patch source autorisé.

## Handoff

**Après RE-775** : le contrôle directionnel et la variation de chambre sont établis dans cette fenêtre source native, pas l'équivalence cible ni le gameplay complet. Prochaine preuve utile : capturer et inspecter visuellement une scène identifiable (et les primitives/caméra associées si elle échoue), puis distinguer sur un trajet sensible une limite géométrique/collision d'une animation ou d'un état d'entrée. Ne pas inférer une collision des seuls plateaux de z. La progression de niveau, la jouabilité prolongée et la preuve amont/cible GetHeight restent ouvertes ; demander une attribution et un vrai RED comportemental avant tout patch.
