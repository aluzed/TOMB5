# RE-736 — Entrées manette, SDK et valeur héritée par la couleur

## Statut et progression

**Preuve partielle acquise par exécution cible ; reconstruction C non ouverte.**
Cette recherche succède au handoff RE-735, sans relancer les audits terminaux.

- [x] Boot, payload et mémoire Ghidra recoupés ; projet ouvert en lecture seule.
- [x] S_UpdateInput, appels SDK, initialisation et tranches appelantes inspectés.
- [x] Instructions authentifiées exécutées sans remplacement des routines SDK.
- [x] Matrices manette et quatre tranches appelantes réexécutées par le parent.
- [x] SayNo et descendants audio décompilés ; matrice dédiée réexécutée.
- [x] Limites et objectif suivant reportés dans le dashboard.
- [ ] Chemin audio actif jusqu'au retour prouvé avec prise en charge du GTE.
- [ ] Contrat portable complet établi, puis tests RED et reconstruction C.

## Preuves acquises

L'initialisation réelle du SDK est exécutée après son effacement BIOS, sur RAM
explicitement initialisée. Les routines SDK sont les instructions du boot, pas
des mocks. Cela ne constitue pas une initialisation console complète.

La matrice manette vérifie le registre volatil transmis à la couleur et les
seize mots de sortie. Dans les états échantillonnés, la valeur est zéro ou deux,
selon le chemin d'interrogation et d'envoi aux actionneurs. Les tranches réelles
entre appel d'entrée et appel de couleur sont également exécutées. Deux
séquences successives montrent la transition zéro, deux, deux ; une constante
universelle ne peut donc pas être déduite de cette expérience.

Vérification parent :

| Expérience cible | Résultat |
|---|---:|
| Appels directs entrée puis couleur | 384 cas réussis |
| Quatre tranches appelantes | 384 cas réussis |
| États SDK transitoires | 512 cas réussis |
| Boutons, axes et modes échantillonnés | 912 cas réussis |
| Tranche cascade puis couleur | 11 cas réussis |
| SayNo et chemins audio | 672 réussites, 96 exceptions sur 768 cas |

Pour SayNo, une seconde matrice restaure le contexte CPU complet et la RAM à
chaque cas. Un guard vérifie chaque instruction exécutée contre le payload
original et interdit toute exécution hors de celui-ci. Les branches d'audio
inactif, pause, échantillon absent, volume nul, rejet aléatoire et échantillon
négatif reviennent réellement. Le RNG et certains effets mémoire sont vérifiés.
La valeur du registre au retour de SayNo varie ; les cas revenus passent ensuite
par le code d'entrée qui rétablit la valeur attendue avant la couleur.

Les cas avec volume positif et échantillon valide lèvent tous une exception
Unicorn sur le chemin COP2/GTE. Aucun faux retour n'a été injecté. Le registre PC
rapporté après exception est réinitialisé par l'émulateur : l'identification de
l'instruction fautive s'appuie sur la dernière instruction tracée et le dump,
non sur cette valeur PC après exception.

## Revue et limites

Une revue indépendante a vérifié l'authenticité et les premières matrices,
ainsi que l'absence de stubs SDK. Elle a demandé la couverture SayNo, réalisée
ensuite. La matrice SayNo a été réexécutée par le parent ; elle n'est pas présentée
comme ayant reçu une seconde revue indépendante.

Les premières matrices restaurent la mémoire mais pas tout le contexte CPU ;
les axes y varient ensemble. La matrice SayNo corrige cette isolation pour son
propre périmètre seulement. Aucun résultat ne signifie couverture exhaustive.
RAM manette et audio synthétique, absence d'interruptions, de BIOS complet, de
manette physique, de SPU et de GTE : aucune validation matérielle revendiquée.
Les assertions des probes sont des expériences cible, pas de nouveaux tests de
régression C. Aucun code de production changé, aucune suite globale annoncée.

Tous les projets, exports, probes et résultats détaillés restent ignorés sous
`build/reverse/autonomy-20260908/re736-input-proof/`. Les traces et emplacements
bruts ne sont pas versionnés. Le rapport utilisateur non suivi reste intact.

## Handoff immédiat

**Prendre en charge ou recouper le chemin GTE/audio actif de SayNo**, en examinant
les instructions COP2 et une solution d'émulation GTE existante, sans simuler
arbitrairement un retour SDK. Vérifier les effets mémoire et le retour réel avant
d'énoncer un contrat complet de couleur. Ajouter les témoins position inchangée
et temporisation active, non couverts par cette matrice.

Le défaut COP2 de cette expérience n'est pas un arrêt global de l'autonomie.
Si la piste exige réellement du matériel indisponible après recherche de
solutions, sélectionner une autre unité cohérente du binaire. L'autorisation
reste valable jusqu'au 8 septembre 2026 à 23 h 45, Europe/Paris.
