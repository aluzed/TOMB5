# Fondations caméra — 20 septembre 2026

PORT-004 / PORT-005 : **In progress**, aucun Done. Autorisation autonome jusqu'au
20 septembre à 12h Europe/Paris. Linux32/PSXPC_N reste une cible provisoire.
Cette note distingue les corrections intégrées des reconstructions privées.

## Deux corrections de production, pas une caméra réparée

1. **GetLaraJointPos conserve maintenant les 16 bits de R22.** La vraie TU
   CALCLARA et la vraie LIBGTE i386 sont utilisées par les tests. RED public
   **66 failed / 18 passed**, puis GREEN **84 passed**, mêmes cas synthétiques.
   Les positions calculées sont inchangées ; la divergence était uniquement
   dans la matrice restaurée. Une exécution privée de la fonction cible entière
   concorde après correction. Revue indépendante : recompilation RED/GREEN et
   audit des archives cible, pas nouveau replay cible par ce reviewer.
2. **mgLOS traite correctement deux obstacles** : plafond trop éloigné pour
   être repoussé et volume plafond supérieur ou égal au sol après un point
   valide. RED public **28 failed / 83 passed**, puis GREEN **111 passed**.
   Retour, destination complète, room et événements géométriques ordonnés sont
   comparés. La correction partagée est limitée par
   `PSX_VERSION && PSXPC_TEST`, validation i386 ; les autres branches restent
   inchangées. La preuve cible utilise des services sol/plafond synthétiques.
   Revue indépendante : recompilation native et décodeur entier MIPS séparé,
   111 résultats/traces conformes. Pas une preuve des vrais services géométriques.

Les fixtures publiques mgLOS sont des coordonnées et événements construits,
**sans donnée du jeu, instruction, adresse cible ou trace machine**.
Suite publique après ces corrections : **446 passed**, exit 0 ; les tests
supplémentaires de cette note sont documentaires et comptés séparément.

## Build et parcours réellement rejoués

GLEW et jeu recompilés dans un dossier neuf : ELF32 i386, exit 0.
Le premier essai a échoué sur un chemin d'archive absent ; le second a utilisé
l'archive locale dont le hash est vérifié par le driver. Rien n'a été masqué.

Un seul nouveau runtime de ce tick, sur ce build corrigé : titre → New Game →
chargement terminé vers 71 s → scène et déplacement → regard → relâchement →
pause → Quit/Yes → titre → fermeture WM_DELETE_WINDOW. Application et GDB
**exit 0**. Entrées XTest réelles, aucune écriture d'état du jeu ni saut de niveau.

**13 captures inspectées** : chargement à 60 s, scène à 81 s, déplacement à
88/93 s, écran noir à 104/107 s pendant le regard, scène revenue à 112 s,
pause à 117 s, confirmation à 122 s et titre à 163 s. Pas de nouvelle validation
campagne, sauvegarde, audio matériel ou collisions étendues. **LookCamera reste
stub dans la source de production : le regard noir persiste.** Les captures
privées sont jointes par MEDIA au bilan, jamais versionnées.

## Reconstruction privée réellement avancée, non intégrée

Les unités de recherche ont produit et exécuté les étapes suivantes. Leurs
harnesses synthétiques ne constituent pas un parcours du jeu ; les chiffres
ne doivent pas être additionnés comme des tests indépendants de gameplay.

| Étape privée | Résultat mesuré | Limite |
|---|---|---|
| CameraCollisionBounds cible entière / vraie TU | 4 812 accords ; aucun patch nécessaire | Géométrie doublée, pas tous les chemins |
| Corps LookCamera reconstruit dans une TU privée | RED stub 57/57, puis 57 accords | Services encore doublés à cette étape |
| Corps + vrais helpers collision/LOS | 81 accords ; mutants sensibles | Joints, vue, géométrie et dispatch encore doublés |
| Vue complète phd_LookAt / GetVectorAngles / GenerateW2V | 368 accords avec vraie TU + LIBGTE | GTE logiciel partagé, pas oracle matériel |
| Corps + joint/vue/collision/LOS réels | **79/79 accords fonctionnels** | **12/79 écarts GTE bruts** maintenus ; niveaux 11/12 exclus |
| Module spécial des niveaux 11/12 | 239 accords avec reconstruction native privée | Structures privées, pas ABI/TU moteur validée |

La dernière composition concorde sur caméra, matrices de vue, microphone,
angles restaurés et événements, mais diffère sur les hauts bits du stockage
logiciel IR1 dans 12 cas. **Pas de GREEN intégral ni de correctif GTE annoncé.**
La matrice joint est synthétique : le producteur animé n'est pas prouvé.
Géométrie/RNG restent des doubles ; le même logiciel GTE est utilisé des deux
côtés, non un oracle matériel indépendant. Ces nouvelles unités de composition
restent privées, non intégrées ; leurs rapports ne valent pas revue externe.

Le dispatch 11/12 est attribué à MOD_T12 et à un service de correction caméra
contre des static meshes. Son corps natif moteur est absent sur PSXPC_N : il
faut adapter/tester les trois fonctions privées aux vrais layouts. Appeler
un pointeur de code MIPS depuis x86, ou remplacer LookCamera arbitrairement
par MoveCamera, n'est pas une solution.

## Tracker et prochain plus petit travail

- [x] Restauration R22 prouvée, testée et corrigée dans le backend natif.
- [x] Deux omissions mgLOS fermées ensemble, preuves et régression actual-TU.
- [x] Build neuf et parcours natif de non-régression borné, captures inspectées.
- [x] Reconstruction privée LookCamera avec dépendances réelles exécutées.
- [ ] Expliquer/borner les différences GTE brutes sans affaiblir les assertions.
- [ ] Porter MOD_T12 sur les vraies structures moteur et fermer son dispatch.
- [ ] Établir producteur joint et géométrie sur un parcours réel, puis intégrer
      LookCamera après revue et refaire la recette visuelle du regard.
- [ ] Interactions, sauvegarde/reprise, audio, collisions étendues et campagne.

Preuves privées et commandes/exits : `build/reverse/autonomy-20260920-1200/`.
Unités 01/03 : corrections et revues indépendantes ; unités 02/04–09 : analyses
et reconstructions privées ; `runtime/run01/` : chronologie, captures et traces.
Les résultats du 19 septembre restent historiques dans les notes précédentes.
