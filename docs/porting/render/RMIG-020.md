# RMIG-020 — Cutscene d intro du niveau 1 en 64 bits

Status: **In progress** — priorité P1 — confiance Medium

Avancement : En cours : niveau 1 charge et boucle de rendu stable (ndraw=3, fade=0), mais ecran noir en 64 bits. La comparaison 32 bits a charge un autre niveau (gfCurrentLevel=3) ; il faut forcer le meme niveau pour conclure.

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

## Références

- `GAME/DELTAPAK.C:3993` (Handle cutseq triggering name)
- `SPEC_PSXPC_N/DELTAPAK_S.C:91` (DrawCutSeqActors)
