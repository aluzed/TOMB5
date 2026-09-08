# RE-739 — Contrat portable de couleur héritée PSXPC_N

## Statut et progression

**Unité reconstruite en TDD ; revue indépendante approuvée et 125 tests hôte réexécutés par le parent.**
Suite des preuves RE-734 à RE-738, sans rouvrir l'inventaire terminal.

- [x] Attribution et preuves producteur cascades RE-735 relues.
- [x] Preuves SDK, CFG complet et conclusions locales RE-739 relues ; reproduction cible déjà réussie par le parent avant délégation.
- [x] Cinq enchaînements appelants vérifiés avant édition de production.
- [x] RED comportemental réellement exécuté avant toute édition de production.
- [x] Deux producteurs et consommateur reconstruits ensemble, backend PSXPC_N seulement.
- [x] Rejet du type manette non supporté corrigé dans ce backend seulement.
- [x] GREEN ciblé et régression de tous les tests émulateur exécutés.
- [x] Dashboard, handoff et contrôle des modifications incidentes actualisés.
- [x] Revue indépendante favorable, sans erreur bloquante ; tests réexécutés par le parent.
- [x] Livraison Git autorisée après contrôle des fichiers indexés (résultat communiqué dans le bilan du runner).

## Preuve cible et attribution

La preuve locale `build/reverse/autonomy-20260908/re739-sdk-contract/CONCLUSIONS.md`
complète RE-738 : après retour normal de `S_UpdateInput`, la couleur héritée vaut
**2 si et seulement si cette invocation appelle `PadSetAct(0, Motors, 2)`, sinon 0**.
Les résultats publics des fonctions SDK ne sont pas eux-mêmes des couleurs.
L'alignement réussi ou l'état de préparation active l'envoi pour l'appel suivant,
pas pour l'appel courant. Un `send` non nul est vrai, sans restriction à la valeur 1.

Le CFG authentifié établit que tous les chemins admis traversent la dernière
interrogation du mode étendu, qui efface la valeur volatile précédente. Les
appels audio antérieurs n'invalident donc pas ce contrat s'ils retournent
normalement en respectant les registres sauvegardés. Hypothèses : pile et contexte
valides, callbacks SDK installés par l'initialiseur étudié, sans remplacement des
callbacks ni corruption mémoire. La preuve ne suppose pas une synchronisation
matérielle des lectures SDK successives.

La reproduction cible, **effectuée par le parent avant cette implémentation**,
comprend 1 536 cas d'état SDK, 256 identifiants courants, 65 536 identifiants
étendus, 768 cas d'alignement et 10 728 chaînes complètes entrée/couleur. Ce sont
les instructions authentifiées avec RAM synthétique, sans doubles SDK/audio.
Cette délégation n'a pas réexécuté ces matrices ; elle a exécuté les tests C
ci-dessous. Les scripts et résultats bruts restent ignorés.

RE-734/735 établissent séparément la valeur finale de boucle cascade :
`(-4 * GlobalCounter) & 63`, y compris lorsqu'aucun objet n'est chargé. Le
consommateur copie le mot hérité dans les seize entrées secondaires ; sa rangée
de gris et son compteur cyclique sont indépendants.

## Choix d'intégration minimal

- `SPEC_PSXPC_N/SPECIFIC.H` déclare `uint32_t SecondaryPulseColour` et la capacité
  de backend `PSXPC_N_INHERITED_PULSE_COLOUR`. Elle n'est pas liée à l'option
  de test `PSXPC_TEST` et n'est définie dans aucun autre en-tête de plateforme.
- `SPEC_PSXPC_N/PSXINPUT.C` publie zéro à l'entrée et deux dans la branche d'envoi
  des moteurs. L'admission exige désormais un état non nul **et** un type supporté.
- `GAME/OBJECTS.C` publie la phase finale sous cette seule capacité de backend.
  L'initialisation des textures et leurs mises à jour RE-735 sont inchangées.
- `SPEC_PSXPC_N/TEXT_S.C` possède cet état et le consomme sans recalcul depuis
  `GlobalCounter`. Les canaux sont écrits explicitement, sans cast aliasant un
  `CVECTOR` en entier et sans dépendance à l'ordre des octets de l'hôte.

Les signatures publiques et les cinq sites restent inchangés. Un état explicite
partagé évite de propager un changement d'API aux backends distincts ; il représente
le dernier producteur dans l'exécution séquentielle étudiée. Il ne promet pas la
réentrance. Le backend PC et ses couleurs spéculaires ne sont pas modifiés.

| Appelant source | Producteur immédiatement pertinent | Consommateur |
|---|---|---|
| `GAME/CONTROL.C`, chemin PSX | `AnimateWaterfalls` | `UpdatePulseColour` |
| `GAME/NEWINV2.C`, boucle inventaire | `S_UpdateInput` | `UpdatePulseColour` |
| `GAME/NEWINV2.C`, sous-boucle inventaire | `S_UpdateInput` | `UpdatePulseColour` |
| `SPEC_PSXPC_N/SPECIFIC.C`, `sub_62190` | `S_UpdateInput` | `UpdatePulseColour` |
| `SPEC_PSXPC_N/SPECIFIC.C`, `S_Death` | `S_UpdateInput` | `UpdatePulseColour` |

Les guards prétraitent les **vraies unités** avec la configuration PSXPC_N,
comptent ces cinq sites, vérifient leur producteur et n'admettent entre eux que
les affectations/diagnostics inventaire existants. Ils n'exécutent pas les boucles
appelantes complètes ; les quatre tranches cibles RE-738 constituent une preuve
distincte, elle aussi bornée.

## RED / GREEN réellement observés

Commande du RED, avant modification des quatre fichiers de production :

```sh
python3 -m pytest tests/emulator/test_pulse_colour.py -q --tb=short
```

**5 échecs, code de sortie 1** : `reject` échoue sur `PadConnected == admitted` ;
`matrix`, `transitions`, `phases` et `waterfall` échouent sur les canaux de la
rangée secondaire. Le cas cascade démarre sans objet chargé. Les erreurs de
montage initiales du harness ont été corrigées avant ce RED comportemental.

Même commande après reconstruction : **5 réussites**, puis **9 réussites** avec
les quatre guards d'intégration supplémentaires. Régression finale :

```sh
python3 -m pytest tests/emulator -q --tb=short
```

**125 tests réussis.** Les logs du RED, premier GREEN et de la régression sont
respectivement `c-red.log`, `c-green.log`, `c-regression.log` dans le répertoire
local de preuve RE-739. Aucun générateur historique n'a été exécuté ; aucun
artefact généré versionné n'a changé. `git diff --check` est propre.

`tests/emulator/test_pulse_colour.py` compile le vrai fichier entrée inclus dans
son harness et lie les vrais `OBJECTS.C` / `TEXT_S.C`, avec les en-têtes normaux.
Aucune fonction de production n'est copiée. Les fixtures vérifient :

- tous les états-octets, types supportés et rejet des autres types-octets ;
- identifiant étendu nul/non nul, `send` nul, un et non canonique, alignement faux/vrai ;
- transitions persistantes préparation/alignement, envoi ultérieur, absence
  d'identifiant étendu, rejet, reconnexion et remise à zéro ;
- les 65 536 valeurs du compteur global, alternance entrée/cascade/entrée,
  et les 256 valeurs initiales du compteur de gris ;
- les seize entrées des deux rangées, les autres rangées inchangées,
  et les RGB des quatre sommets des primitives émises par le vrai `DrawChar`.

`tests/emulator/test_waterfalls.py` lie désormais aussi `TEXT_S.C`, propriétaire
du nouvel état. La première régression avait signalé cette dépendance manquante
au lien ; elle est corrigée sans remplacer l'état de production par une fixture
et sans supprimer les assertions de conservation des textures.

## Limites explicites

Les doubles SDK contrôlés du test C ne sont **pas** la preuve SDK cible. L'entrée
SDL est neutralisée, les boutons sont relâchés, et un appel audio inattendu fait
échouer le harness. L'accès test au `send` local utilise le nom de symbole GCC de
la vraie variable, sans hook de production ; cette fixture est spécifique au
compilateur hôte. Les maillages, textures et glyphes sont synthétiques.

Pas de console, BIOS complet, périphérique physique, interruption/réentrance,
validation sonore, sélection des glyphes ni partie complète exécutée. Les
préconditions des fonctions appelantes entières restent hors preuve. La
compilation des TU utilise les adaptations hôte existantes ; des avertissements
hérités subsistent dans SETUP. Le prétraitement complet des anciens backends a
été tenté mais bloque sur leurs en-têtes absents ; seul le confinement du nouveau
code par la capacité exclusive et l'absence de modification de leurs sources
sont vérifiés, pas leur build natif.

Le script local `reproduce.sh` recompilant aussi un témoin C contre la source
courante, son ancien résultat de couleur C décrit l'état **avant correction**.
Le relancer après ce patch actualiserait ce témoin ; il ne faut pas le confondre
avec une divergence des matrices d'instructions cibles. Les archives n'ont pas
été réécrites ici. Aucun asset, dump ou adresse cible n'est ajouté aux livrables.
Le rapport utilisateur non suivi n'a été ni lu ni touché.

## Handoff immédiat

**Revue indépendante favorable avant livraison Git.** Le reviewer a vérifié le
confinement backend, le lien de l’état partagé, les cinq sites et la séparation
preuves cibles/tests SDK doubles ; réexécuter les tests ciblés. Ne pas déclarer
`S_UpdateInput`, l'inventaire ou le texte entièrement reconstruits sur cette base.
Après validation, choisir une prochaine unité cohérente attribuée ; la sélection
des glyphes et le domaine des caractères restent différés. Aucune RE-740 n'est
ouverte par cette délégation. Autorisation temporelle rappelée : 8 septembre 2026,
23 h 45 Europe/Paris ; aucun job, commit ou push lancé.
