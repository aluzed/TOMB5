# RE-777 — Soumission native et géométrie projetée du niveau ELF32

24 septembre 2026 (Europe/Paris). **Après RE-776**, deux **sessions distinctes** sur le même ELF32 source (empreinte privée vérifiée) ont interrogé la chaîne entre primitive, sommets, émulateur et capture. Résultat : l'hypothèse limitée « aucun triangle natif soumis » est réfutée sur les fenêtres échantillonnées ; **capture non interprétable** avec confiance comme scène jouable, cause de sa lisibilité toujours non attribuée. Aucun correctif source.

## Tracker
- [x] RED documentaire (3 échecs attendus avant story/index), contrat d'append-only et de sécurité.
- [x] Session 1 : compteurs de `DrawAggregatedSplits`, `Emulator_DrawTriangles`, `Emulator_EndScene` et captures de la fenêtre source.
- [x] Session 2 : métadonnées agrégées des **sommets projetés**, triangles et rectangle de rendu, sans publier les enregistrements de sommets.
- [x] Source de production inchangée ; documentation metadata-only et captures sous `build/reverse/` ignoré.
- [ ] Rasterisation, textures/éclairage, pose caméra et image de niveau lisible démontrés ; équivalence cible/non-cible, `GetHeight` en contexte et gameplay complet non validé.

## Observations et limites
1. Session de soumission `build/reverse/autonomy-20260924-render-submit-0130/` : le journal `submit.jsonl` contient des appels avec des demandes de triangles **non nulles** à `Emulator_DrawTriangles` et des passages à `Emulator_EndScene`. Près de `forward-observed.png`, échantillons voisins à 0,22 seconde : tampon préparé de 2 829 sommets ; sortie d'émulateur suivante avec un appel positif et 943 triangles demandés. Ce sont des demandes à l'API de rendu, **pas une preuve de rasterisation**, ni un décompte de triangles réellement visibles ou de pixels valides. Une fenêtre X11 est constatée, pas une navigation validée.
2. Session géométrique distincte `build/reverse/autonomy-20260924-vertex-0133/` : `vertex-metadata.jsonl` dérive des comptes et bornes des sommets natifs sans en conserver les enregistrements. À 1,05 seconde de `forward-vertices.png` : 2 820 sommets / 940 groupes de triangles, 854 **triangles non dégénérés**, 937 boîtes de triangles recoupant le **rectangle de rendu** 512 × 240 ; 2 703 sommets à l'intérieur et des canaux RGB non nuls. Le recoupement de boîtes n'est pas une garantie de couverture, orientation, visibilité ou couleur finale. Aucune synchronisation pixel/triangle d'une même frame n'est démontrée.
3. Les captures privées des deux sessions sont prises de la fenêtre sous Xvfb ; leurs empreintes correspondent aux entrées `session.json`, les pixels diffèrent entre les prises, sans authentifier à l'œil un niveau lisible. `forward-vertices.png` ne prouve pas un écran de gameplay. `gdb_wrapper_exit=124` (exit 124) dans les deux sessions signifie limite volontaire à 105 secondes ; le wrapper GDB a expiré tandis que le runner Python termine à zéro, ce qui ne transforme pas le timeout en succès de l'application.
4. **source de production inchangée** ; aucun asset public, aucune image intégrée ni dump/instruction brut. Ni la collision native de RE-776, ni ces métriques de rendu n'ouvrent une correction PlayStation, un ABI cible ou une validation de progression. `code_change_readiness=blocked`.

## Handoff
**Après RE-777** : sur une même frame source, attribuer le défaut de lisibilité entre texture/VRAM, éclairage/raster ou pose caméra, avec image de niveau interprétable et attribution des buffers/états GPU ; comparer à une référence cible seulement si authentifiée. Ensuite, reprendre la preuve `GetHeight` / collision et progression sur un itinéraire réel. Garder gameplay complet non validé et source patch bloqué tant que cette preuve manque.
