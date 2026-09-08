# RE-734 — Couleurs pulsées et animation des cascades : preuve cible exécutée

## Statut et progression

**Recherche effectuée et auditée ; intégration source non prête.** Ce jalon ne
clôt pas l'autonomie autorisée jusqu'au 8 septembre 2026 à 23 h 45, Europe/Paris.
Il ouvre une preuve de producteur de textures, pas un nouvel audit terminal.

- [x] État live contrôlé : RE-732 et RE-733 déjà livrées ; aucune duplication.
- [x] Projet Ghidra disponible sans processus concurrent ; accès read-only.
- [x] Nouvelle décompilation de la couleur pulsée, de ses appelants et des
  prédécesseurs `S_UpdateInput` et `AnimateWaterfalls`.
- [x] Boot identifié par son empreinte attendue ; payload égal au corps du boot.
- [x] Instructions cibles réellement exécutées avec Unicorn et RAM synthétique.
- [x] Audit indépendant : probe réexécuté et conclusions recoupées.
- [ ] Producteur PSX des textures de cascades prouvé et restauré.
- [ ] Dépendance de couleur après l'entrée manette complètement caractérisée.
- [ ] TDD de la véritable unité C, reconstruction et revue d'intégration.

## Preuves nouvelles

### Couleur pulsée : dépendance au contexte appelant

Le corps cible met à jour le compteur cyclique et remplit les seize entrées de
la ligne de gris. Il recopie aussi **le mot entrant entier du troisième registre
d'argument** dans chacune des seize entrées de la ligne de couleur secondaire.
Il ne calcule pas lui-même l'expression à partir de `GlobalCounter` présente dans
`SPEC_PSXPC_N/TEXT_S.C`.

Les cinq appels directs identifiés sont précédés soit de `S_UpdateInput`, soit
d'`AnimateWaterfalls`, sans préparation explicite de cet argument. Un prototype
C à trois paramètres inféré par le décompilateur ne démontre donc pas un contrat
public à trois paramètres. La valeur héritée doit être prouvée par chemin.

L'examen complet et l'exécution du prédécesseur cascade corrigent une première
hypothèse insuffisante : la phase calculée au début ne reste **pas** la phase de
sortie. Avant la dernière cascade, le registre prend la phase du second groupe,
indépendamment des objets chargés. La chaîne cascade puis couleur conserve cette
phase. Elle ne justifie pas l'expression C actuelle. **Aucune correction locale
de couleur n'est appliquée tant que les autres chemins ne sont pas établis.**

### Cascades : unité de comportement délimitée

L'analyse et les expériences établissent :

- six objets, chacun conditionné par son indicateur de chargement ;
- une phase pour les cinq premiers et une autre pour le dernier ;
- deux enregistrements de texture pour les quatre premiers, un pour les suivants ;
- coordonnées verticales basses décalées de 63 par rapport aux hautes, avec
  stockage sur un octet, et non masquage des coordonnées finales sur six bits ;
- conservation des autres octets des blocs de texture testés.

Les structures PSX de texture du dépôt correspondent aux champs utilisés. Mais
la boucle qui alimente `AnimatingWaterfalls` et `AnimatingWaterfallsV`, dans
`GAME/SETUP.C`, est désactivée. Les définitions PSX initialisent les tableaux à
zéro ; les producteurs PC ont des types différents. Activer isolément
`GAME/OBJECTS.C` pourrait donc déréférencer un pointeur nul. Fournir des textures
synthétiques dans un test C ne prouverait pas cette intégration.

## Exécution et limites

Unicorn 2.1.4 est installé dans un environnement virtuel ignoré. Le probe charge
le payload authentifié, exécute ses instructions MIPS, impose un budget
instructionnel et vérifie le retour effectif. Il ne copie pas les fonctions C.

| Expérience | Cas réussis | Portée |
|---|---:|---|
| Couleur pulsée | 1 536 | Toutes les valeurs initiales d'un octet de compteur, six mots entrants ; deux lignes et octets voisins vérifiés |
| Cascade puis couleur | 11 | Compteurs représentatifs, cascades non chargées ; phase héritée et ligne secondaire |
| Cascades chargées | 704 | Tous les 64 masques de chargement, onze compteurs ; six blocs synthétiques comparés intégralement |

Ces cas utilisent de la RAM et des textures **synthétiques** : ce n'est ni un
lancement du jeu ni une validation matériel/SDK. Le producteur manette n'est pas
émulé ici. La conservation mémoire ne porte que sur les blocs explicitement
comparés. Il ne s'agit pas de tests RED/GREEN d'une implémentation C nouvelle :
Aucun code de production n'a été changé.

Régression exécutée après rédaction : `python3 -m pytest tests/emulator
tests/reverse -q` — **3 383 tests réussis**. `git diff --check` est propre.

Les preuves détaillées, scripts privés, résultats, journaux et décompilations
restent exclusivement sous `build/reverse/autonomy-20260908/`, ignoré par Git.
Aucun dump, donnée de texture, instruction ou adresse cible n'est versionné dans
ce jalon. Le rapport technique non suivi reste intact et non consulté.

## Handoff immédiat

**Prochaine unité : prouver le producteur PSX des textures de cascades dans
`LoadLevel`, puis traiter initialisation et animation comme une seule unité
cohérente.** Identifier l'overlay/version du producteur, établir la lecture du
maillage et la sélection de texture, puis écrire les tests d'intégration avant
activation. Si l'overlay exige une extraction, la réaliser sous `build/`.
L'absence de cette preuve n'autorise ni un patch partiel ni l'arrêt du runner.

En parallèle logique mais sans patch de couleur : remonter les sorties de
`S_UpdateInput` et ses appels SDK pour caractériser la valeur héritée. Ne pas
remplacer cette dépendance par une constante ou une formule supposée.

La sélection des glyphes/accentuation de RE-733 reste une piste différée ; les
corrections de texte précédemment livrées ne sont pas modifiées.
