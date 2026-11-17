# RMIG-020 — Cutscene d intro du niveau 1 en 64 bits

Status: **In progress** — priorité P1 — confiance Medium

Avancement : En cours : la 3D du niveau 1 s affiche partiellement en 64 bits (3717 sommets, 111 splits, capture avec surfaces bleues) mais de nombreux sommets sont hors ecran (±32000) et la scene reste majoritairement noire. La cutscene n avance toujours pas.

## Objectif

Faire avancer et rendre correctement la cutscene d introduction du niveau 1 en 64 bits, puis atteindre le gameplay.

## Faits établis

Avec les entrees clavier maintenues (xdotool keydown/keyup), le menu 64 bits s ouvre et New Game lance le niveau 1 (DoLevel Name=1). La sequence CD du niveau se termine (dernieres lectures 12/18231 et 8/18232) mais l ecran reste noir avec l icone de chargement et le log repete 'Handle cutseq triggering name: 1' toutes les frames ; en 32 bits, la meme sequence affiche la salle sombre de la cutscene et passe au nom 3. Corrections deja faites pour arriver la : LaSlot en zone basse (SoundEffect), lara_matrices/lara_joint_matrices accedees sans cast int (InterpolateMatrix_CL), OT de pickup en mots 32 bits (S_DrawPickup).

## Périmètre

GAME/DELTAPAK.C (TriggerCutscene/cutseq), SPEC_PSXPC_N/DELTAPAK_S.C, DrawCutSeqActors, chargement des donnees cutseq en LP64.

Hors périmètre : Vulkan, audio humain.

## Tâches

- [ ] Comparer la progression de cutseq_num/GLOBAL_cutseq_frame entre 32 et 64 bits pour le niveau 1.
- [ ] Verifier les pointeurs de cutseq (GLOBAL_cutme, actor_data, tables de frames) et l affichage des acteurs.
- [ ] Atteindre le gameplay (controle de Lara) sans blocage de cutscene.

## Critères d’acceptation

- La cutscene du niveau 1 avance (nom suivant) et la geometrie de la salle est visible en 64 bits.
- Le gameplay niveau 1 est atteignable et stable au clavier en 64 bits.

## Validation

Execution comparee 32/64 avec captures et log de cutseq.

## Inconnues

La boucle peut venir du timing audio XA (dummy) ou d un pointeur cutseq converti incorrectement.

## Estimation

1 a 2 jours-personne.

## Dépendances

- RMIG-018
- RMIG-019

## Preuves

- 2026-11-17 : 64 bits : New Game -> DoLevel(Name=1), lectures CD du niveau terminees, log repete "Handle cutseq triggering name: 1" pendant 50 s, ecran noir avec icone ; aucun SIGSEGV. 32 bits sur la meme sequence : salle de cutscene visible, nom 3.
- 2026-11-17 : Diagnostic DRAWDBG (env TOMB5_DRAWDBG=1) : en 64 bits, gfCurrentLevel=1, number_rooms=242, camera room 0 pos (46592,-960,30080), number_draw_rooms=3, ScreenFade=0, ScreenFading=0 -> la boucle et la fade sont normales mais l image reste noire (seule une icone 2D apparait). En 32 bits, le meme scenario de touches charge gfCurrentLevel=3 (125 salles, camera room 8) et affiche la salle : les deux executions ne comparent pas le meme niveau. Le menu 32 bits a un defaut de selection deja connu (byte_46). Prochain test : forcer le niveau 1 en 32 bits (level select) et comparer camera/ndraw/fade, puis verifier la projection LP64 (matrices GTE) si l ecart persiste.
- 2026-11-17 : Corrections LP64 : matrix_stack/w2v_matrix/phd_mxptr passent de long a int (les ecritures matrix_stack[9] et lectures phd_mxptr[3] n avaient plus le meme pas, toute la projection 3D etait fausse) ; les roomlets lisent x/y/z et left/right/top/bottom par nom au lieu des offsets int 5/6/7/14/15 qui dependent du layout ; SubPolyGTLoopRLx recoit directement le pointeur de table (plus de t0[0] sur l adresse d un pointeur global) et les appels ne prennent plus &QuadVertTableRLx/&TriVertTableRLx. Resultat : DrawMeshRL1 est atteint et genere des appels SubPolyGT4RL1 ; crash restant dans SubPolyGT4RL1 sur un pointeur de table calcule/tronque (0x5572f1fc au lieu de 0x55555572f1fc sous gdb). Prochain pas : tracer la valeur de QuadVertTableRL1/QuadVertTables[gp] au moment de l appel et corriger le dernier cast int.
- 2026-11-17 : Apres correction de matrix_stack/w2v (mots 32 bits), des champs de salle lus par nom, des tables SubPolyGT passees en pointeur complet, de s6 en intptr_t et du pointeur door dans calc_animating_item_clip_window, le niveau 1 dessine de la geometrie : [OT] verts=3717 splits=111, capture montrant des surfaces bleues. Anomalie restante : bbox des sommets (-32632,-130)-(30848,15472) au lieu de rester dans 0..512x0..240, donc une partie des polygones a des coordonnees ecran invalides et la scene reste surtout noire. Prochain pas : comparer les SXY/SZ des premiers polygones avec le 32 bits au meme endroit (meme salle/camera) pour isoler la derniere erreur de projection ou de base de vertices.

## Références

- `GAME/DELTAPAK.C:3993` (Handle cutseq triggering name)
- `SPEC_PSXPC_N/DELTAPAK_S.C:91` (DrawCutSeqActors)
