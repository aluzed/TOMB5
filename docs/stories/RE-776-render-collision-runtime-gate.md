# RE-776 — Chemins de rendu et borne de collision du niveau ELF32

24 septembre 2026, Europe/Paris. **Après RE-775**, trois **sessions distinctes** du même exécutable source ELF32 ont sondé le rendu puis la limite du déplacement avant. La source de production inchangée ; `code_change_readiness=blocked`. Il s’agit d’un contrôle natif borné, non d’une équivalence avec les instructions PlayStation ; gameplay complet non validé.

## Rendu : chemins atteints, visibilité non établie

Sous `build/reverse/autonomy-20260924-render-0112/` ignoré, `session.json`, `samples.jsonl`, `gdb.log` et trois captures privées lient l’exécutable, les pressions XTest et les entrées GDB du premier niveau. Les points d’arrêt dénombrent 960 entrées chacun dans `DrawRooms`, `DrawLaraL1`, `DrawRoomletListAsmRL1` et `GPU_EndScene`, et zéro dans les autres variantes sondées. Lara est chargée, ses maillages actifs et les sélecteurs de dessin valent 1 dans les lignes échantillonnées. Le champ privé nommé `poly_words` représente en réalité **un écart de pointeurs en octets** (`char*`, entre `db.polyptr` et `db.curpolybuf`) : son écart positif en fin de scène n’est **pas un compte de primitives**, ni une preuve de pixels corrects, de sûreté du tampon ou d’équivalence cible.

Les PNG privés changent et contiennent des pixels non noirs ; la fenêtre demeure sombre et l’OCR ne permet pas d’identifier de manière fiable le niveau ou Lara : **capture non interprétable** au sens d’une validation visuelle du gameplay. La capture `level-idle.png` précède même la première ligne GDB filtrée sur le premier niveau et ne peut pas lui être attribuée par cette sonde seule. Le premier essai de ce pilote s’est interrompu côté Python avant toute capture ; ses journaux distincts sont conservés dans `failed-1/`, sans les fusionner avec la session retenue.

## Collision : témoin temporel corrigé par un appui maintenu

Sous `build/reverse/autonomy-20260924-collision-0116/` ignoré, la **première sonde** enregistre une unique entrée `LaraCollideStop` avec `CT_FRONT` juste **après** le relâchement de la flèche avant ; elle ne démontre donc pas une décision pendant l’appui. Le contrôle répété sous `build/reverse/autonomy-20260924-collision-held-0121/` (`session.json`, `collision.jsonl`, `gdb.log`, `held-at-limit.png` et témoins) maintient la touche plus longtemps. À l’entrée de `LaraDeflectEdge`, pendant `IN_FORWARD` et **avant relâchement**, le contact devient `CT_FRONT` à z=38813 ; `front_floor=-2048`, `mid_floor=0`, `hit_static=0`. Dans les entrées suivantes, `LaraControl` observe z=38813, vitesse nulle et **état d’arrêt** pendant l’appui ; les entrées échantillonnées de `lara_col_stop` portent aussi `CT_FRONT`. `GAME/COLLIDE.H` définit ce type et `GAME/LARA.C` contient la branche de déflexion correspondante. Dans **cette** répétition, `LaraCollideStop` n’est jamais entré : ne pas attribuer la borne à cet autre helper ni prétendre avoir tracé toutes les écritures ou démontré la destination de scénario. La position finale varie légèrement entre sessions ; ce sont des observations natives distinctes, non une matrice de déterminisme cible.

Les deux sondes de collision et la sonde de rendu sont trois processus du port, pas une exécution du binaire cible. Pour chacune, `exit 124` est la limite de temps du **wrapper GDB**, ni succès applicatif ni crash attesté. Toutes les captures restent uniquement sous `build/` ; **aucun asset public**, aucun binaire, code machine, dump, image ou primitive brute dans Git. Une revue indépendante en lecture seule a vérifié les deux premières sondes et signalé le relâchement prématuré ainsi que l’unité erronée `poly_words` ; la répétition sous appui maintenu est vérifiée ici par ses journaux et mesures, sans lui attribuer cette revue.

## Vérification et readiness

Test documentaire RE-776 écrit avant story/dashboard : RED attendu, 3 échecs (story, section et index absents), `doc-red.log`, exit 1 ; **RED documentaire**, pas RED comportemental moteur. Les tests publics vérifient les qualifications, l’ajout append-only de la section, le tracker et l’index déterministe. Source de production inchangée ; preuve cible manquante de l’ABI/comportement de collision **GetHeight** et aucune justification de patch. `code_change_readiness=blocked` ; scène interprétable, progression et gameplay complet non validé.

## Tracker

- [x] Chemin du rendu source et écart de pointeurs mesurés sans assimiler les octets à des primitives affichées.
- [x] Première sonde de collision invalidée pour l’attribution « pendant appui » ; répétition pendant l’appui avec `CT_FRONT` et position stable.
- [x] Captures natives privées, manifeste horodaté et RED documentaire ; pas de source de production modifiée.
- [ ] Rendu visuellement interprétable, équivalence cible/ABI GetHeight, progression et gameplay complet non validés.

## Handoff

**Après RE-776** : une décision de contact frontal native est observée pendant le contrôle avant ; ce n’est pas une preuve de comportement cible ni de niveau jouable. Prochaine preuve intégrée : isoler pourquoi la scène reste visuellement difficile à interpréter en rapprochant une capture identifiable des primitives réellement soumises à l’émulateur (pas seulement la taille du tampon), puis valider un trajet et une progression observable. Pour une correction de collision, attribuer d’abord sur binaire cible le contrat GetHeight et les préconditions appelantes avec un vrai RED sur l’unité source ; ne pas patcher à partir de cette seule mesure runtime.
