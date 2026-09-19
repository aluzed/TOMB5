# Linux32 — préconditions du regard et frontière de preuve

19 septembre 2026 ; base `5f13f99a`. PORT-003/004 restent **In progress**.
Linux32/PSXPC_N est provisoire. **Aucun nouveau correctif du jeu dans cette unité.**
Cette analyse prolonge [runtime-controls.md](runtime-controls.md) sans réécrire
les constats précédents. La caméra de regard n'est pas réparée.

## Nouveau parcours réel

Un processus neuf du binaire construit pendant l'unité précédente a suivi
le titre → New Game → déplacement → regard → relâchement → pause → Quit/Yes
→ titre → fermeture normale. Entrées XTest réelles ; aucune écriture de l'état
jeu, aucun saut de niveau, aucun service remplacé. Binaire et captures hashés ;
pas de nouvelle compilation dans cette unité.

- Treize captures inspectées : à 60 s, illustration de **chargement** ; à 81 s,
  scène réelle ; déplacement ensuite. Les traces identifient la room 2 pendant
  le regard, les images seules ne déterminent pas les numéros des salles.
- Aux captures 104/107 s, vue noire avec interface ; à 112 s, scène revenue.
  Pause à 117 s, confirmation Quit à 122 s, titre à 163 s.
- Sept observations à l'entrée réelle de `LookCamera` : niveau 1, room 2,
  argument `item == lara_item`, type Look, ancien type Chase, bounce nul.
  La rotation de tête varie après l'entrée directionnelle ; les matrices du
  joint 8 sont présentes et évoluent. Cela ne prouve pas leur équivalence cible.
- Mesures dans ce binaire i386 : `sizeof(CAMERA_INFO)=118`,
  `sizeof(ITEM_INFO)=144`, `sizeof(lara_info)=342`, matrice joint = 32 octets.
  Ces tailles ne prouvent pas une identité de layout MIPS/native.
- **Application exit 0 et wrapper GDB exit 0**, après fermeture de fenêtre.

## Analyse cible réellement exécutée

Trois exports Ghidra neufs en lecture seule couvrent treize fonctions autour
 du joint, de ses producteurs et de la vue. Chaque export compare le payload
complet au binaire authentifié ; les marqueurs de fin et exits sont vérifiés,
les empreintes du projet sont inchangées. Les pseudo-globales Ghidra ne sont
pas prises pour des adresses fiables : le GP provient du startup authentifié.

Le préfixe cible de `LookCamera` prépare les angles et son premier vecteur,
puis entre dans le vrai `GetLaraJointPos`. **384 cas construits**, répartis
entre deux frontières :

| Portée | Cas | Arrêt / limite |
|---|---:|---|
| CPU cible sans pont COP2 | 192 | Avant le premier transfert de contrôle COP2 |
| Transferts COP2 explicitement modélisés | 192 | Avant la première opération arithmétique GTE |

Chaque cas réinitialise CPU/RAM ; comparaison avec un interpréteur entier
séparé des registres généraux, RAM complète et séquence de visites. Un rejeu
neuf du parent reproduit les 384 lignes. Les visites incluent l'arrêt et les
transferts interceptés : ce ne sont pas des instructions retirées mesurées.
Le pont et l'interpréteur partagent la même convention synthétique de registres
COP2 ; leur accord n'est pas un oracle matériel. L'interpréteur ne modélise
pas les délais de chargement du processeur physique.

Ces cas isolent aussi l'argument `item` d'entrée et vérifient les matrices
inchangées par le préfixe, ainsi que la lecture du joint sélectionné dans la
portée étendue. **Les matrices et angles synthétiques ne proviennent pas du
parcours natif.** Aucun calcul GTE arithmétique, producteur d'animation complet,
sol/plafond, collision, vue complète ou comparaison actual-TU n'est validé ici.

## Candidat suivant, pas correctif acquis

La lecture du suffixe cible et de `GetLaraJointPos` source signale un masque
tronqué lors de la restauration d'un composant de matrice. C'est une divergence
statique candidate : pas de RED actual-TU, pas d'effet gameplay établi, donc
**aucun patch**. Restaurer ce composant seul ne reconstruirait pas `LookCamera`.

Le chemin complet du regard dépend encore de la géométrie GTE, des requêtes
sol/plafond, de collisions, de la vue et d'un dispatch conditionnel non fermé.
Le prochain travail sûr est une preuve de conservation de matrice sur la TU
réelle et la cible, puis l'extension cohérente du regard depuis ses préconditions
observées. Ne pas transformer les préfixes synthétiques en recette du jeu.

## Tracker et provenance

- [x] Préconditions réelles du regard et matrices joint observées sans injection.
- [x] Exports Ghidra authentifiés et préfixes cibles réellement exécutés.
- [x] Rejeu parent identique ; captures inspectées ; fermeture normale.
- [ ] Restauration de matrice : preuve corrective actual-TU encore nécessaire.
- [ ] `LookCamera` complet, collisions étendues, interactions, sauvegarde et audio.
- [ ] Acceptation intégrée des tickets : aucun Done attribué.

Preuves privées : `build/reverse/autonomy-20260919-1000/unit03-look-0923/`.
`run01/` contient chronologie, traces et images ; `target/` les exports et
préfixes ; `parent-audit.json` leur vérification. Le worker d'analyse a expiré
sans HANDOFF : le parent a récupéré et revérifié les artefacts, sans traiter
l'expiration comme une réussite globale. Un premier échec d'environnement
Unicorn est conservé ; le rejeu utilise le venv existant.

La suite publique `tests/porting` est distincte : tests documentaires,
préflight et harnesses natifs ne valident pas davantage de gameplay.
Aucun asset, dump, opcode, pseudo-code brut ou screenshot n'est versionné.
