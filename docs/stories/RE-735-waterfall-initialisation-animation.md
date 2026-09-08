# RE-735 — Initialisation et animation des cascades PSX

## Statut et progression

**Unité reconstruite et revue indépendante approuvée.** Succède à la preuve
consommateur RE-734, sans rouvrir la chaîne d'inventaire terminale.

- [x] Overlay producteur retrouvé, version et chargement recoupés.
- [x] Relocation par les instructions du boot authentifié, puis décompilation Ghidra.
- [x] Arguments, globals, sélection de texture et contrôle du chargement vérifiés.
- [x] Exécution cible du producteur et de la chaîne producteur/animation.
- [x] RED puis GREEN sur les vraies unités source et placement dans LoadLevel.
- [x] Reconstruction conjointe de l'initialisation et de l'animation PSX.
- [x] Dashboard de reconstruction et handoff actualisés.
- [x] Suite complète finale : **3 410 tests réussis** ; guards propres.
- [x] Revue indépendante de livraison approuvée, aucun défaut bloquant ;
  80 tests ciblés et preuves cibles réexécutés par le reviewer.
- [x] Validation préalable au commit/push terminée ; livraison Git vérifiée dans
  le compte rendu d'exécution (hors auto-attestation du présent fichier).

## Attribution et nouvelles preuves

L'ancien fichier extrait sous le nom de SETUP.MOD dans le travail RE-006 était
l'en-tête du conteneur, et non l'overlay exécutable : l'entrée concernée portait
une taille mais ne désignait pas le corps du code. Le module réel a été extrait
à partir des entrées de niveaux. Les quinze copies examinées ont la même
empreinte. Le contexte du chargeur boot confirme l'en-tête du module, les
arguments de relocation et la sélection de son entrée LoadLevel.

La routine de relocation du boot authentifié a été **réellement exécutée** sous
Unicorn, à un emplacement synthétique en RAM libre. Ce placement ne prétend pas
être celui d'une session de jeu. Le code relocalisé a été importé et décompilé
avec Ghidra. Les tableaux écrits par le producteur sont ceux lus par l'animation
déjà étudiée dans RE-734. Un deuxième agent a recoupé l'extraction, le chargeur,
la relocation et leurs empreintes, puis réexécuté les expériences.

Le producteur traite les six objets chargés, lit le compte signé dans l'en-tête
**original** du maillage, puis sélectionne la texture avec un indice signé.
Le décalage arithmétique est exprimé en C par une division arrondie vers le bas,
sans décalage négatif indéfini. Le pointeur texture n'est pas multiplié deux fois
par la taille du type. Les objets non chargés conservent leurs entrées.

Le consommateur applique deux phases négatives différentes, met à jour deux
textures pour les quatre premiers objets et une pour les deux derniers. Les
coordonnées verticales basses sont distantes de 63 des hautes et sont stockées
sur un octet ; les coordonnées finales ne sont pas réduites à six bits.

## Reconstruction et tests

- `GAME/SETUP.C` : helper interne `InitialiseWaterfalls`, invoqué dans LoadLevel
  sous `PSX_VERSION`, en remplacement de la boucle désactivée incorrecte.
- `GAME/OBJECTS.C` : `AnimateWaterfalls` activé et corrigé conjointement.
- `tests/emulator/test_waterfalls.py` : vraies unités SETUP/OBJECTS et en-têtes du
  dépôt, textures et maillages synthétiques, contrôle de la conservation mémoire.

RED observé : textures inchangées avec le consommateur désactivé ; API producteur
absente, puis helper vide incapable de fournir le pointeur attendu ; absence
d'appel dans LoadLevel. GREEN ciblé : **27 tests réussis**.

Exécutions des instructions cibles réexécutées par le parent : **4 992 cas du
producteur et 704 chaînes producteur/consommateur réussis**. Le hook du producteur
vérifie toutes ses écritures contre les champs autorisés. Pour la chaîne, le
hook a été désactivé après une exception reproductible de l'émulateur ; six blocs
complets de texture sont comparés, pas toute la RAM.

Une régression de quatre tests historiques a été reproduite : le scanner RE-701
incluait des copies C ignorées sous build et réécrivait son inventaire pendant la
suite. Les tests RE-702 utilisent désormais une fixture du contrat historique
versionné, avec les mêmes assertions et empreintes, au lieu du résultat mutable
d'un scan live. Aucun générateur ni verrou de sécurité terminal n'est affaibli.
Ces changements sont exclusivement une réparation de tests ; aucun nouvel audit
terminal n'est effectué. Les réécritures incidentes des CSV sont exclues du commit.

## Limites

Le fragment producteur est exécuté, **pas le chargement complet d'un niveau**.
Le test C appelle le helper interne puis le vrai consommateur ; un guard séparé
contrôle le placement dans LoadLevel. Les entrées signées adversariales utilisent
de la RAM rembourrée : elles ne prouvent pas la validité de tous les assets.

La compilation hôte utilise les adaptations existantes et émet des avertissements
hérités. Le prétraitement PSXPC est inchangé ; la compilation PC native reste hors
portée de cet environnement dépourvu de ses en-têtes Windows/Direct3D. Aucune
validation console, SDK complet ou rendu en jeu n'est revendiquée.

La couleur pulsée dépendant d'un registre volatil n'est **pas** reconstruite par
ce correctif. Son code reste inchangé. Le contrat portable de cette couleur reste
à établir ; l'activation des cascades ne prétend pas résoudre cette dépendance.

Les extractions, projets, décompilations, probes et preuves brutes restent sous
`build/reverse/autonomy-20260908/re735-producer/`, ignoré par Git. Aucun asset,
dump, adresse cible ou mot machine n'est ajouté aux livrables versionnés.

## Handoff immédiat

**Caractériser les chemins de sortie de S_UpdateInput et de ses appels SDK qui
précèdent la couleur pulsée**, puis confronter les valeurs héritées aux cinq
appelants identifiés dans RE-734. Ne pas remplacer la dépendance par une formule
ou une constante non prouvée. Si cette piste exige du matériel inaccessible,
examiner une autre unité cohérente dans le binaire avant de conclure à un blocage.
L'autonomie reste autorisée jusqu'au 8 septembre 2026 à 23 h 45, Europe/Paris.
Les accents et la sélection des glyphes restent différés.
