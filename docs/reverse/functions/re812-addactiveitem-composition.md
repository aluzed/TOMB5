# RE812 — AddActiveItem / composition : caractérisation privée

Statut : **PRIVATECHARACTERIZATIONPASS**, distinct de production-ready.
Source inchangée : `4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f`.
Verdict privé indépendant : `43d1beb61e28a71ed2611421d3bc069923cdeb69e2f4cd1ddcaa1c8ab09f202b`.

## Preuve et domaine

Revue privée fraîche passée : 48 séquences continues Add/Add/Remove/Add,
192 retours cible et 192 comparaisons par mode natif normal/strict ASan+UBSan,
4860 visites hooks cible. Zéro échec, exit 0 et stderr vide dans les deux modes.
Contrôles : présence control NULL/nonNULL × active 0/1 × status 0/1/2/3 ×
longueur initiale 0/1/2. Cible item 3, toujours en tête lorsqu'actif.
Buffers natifs complets de 642 octets (arène incluant guards + head);
oracle indépendant de RAM complète de 2 MiB à chaque retour cible.
CPU/RAM conservés entre appels. Pointeurs natifs non comparés aux adresses cible.
Si active=1/control=NULL, active et chaîne conservés, status remis à zéro.
Control est seulement une présence de pointeur, callbacks jamais invoqués.

## Décision NO PATCH et limites

Pas de régression production démontrée sur ce domaine, donc aucun candidat ni
patch justifié et aucun behavioral RED. Le RED de publication vérifie seulement
l'absence de métadonnées, pas un bug du jeu. Retrait intérieur/queue non couvert
(RE811 séparé); listes synthétiques finies acycliques seulement. Comparaison aux
retours, pas trace des stores transitoires. Oracle logiciel Unicorn/MIPS, pas
hardware ni certification des autres configurations. Compilation privée de
GAME/ITEMS.C i386 sous PSXPC_TEST/PSX_VERSION/USE_32_BIT_ADDR; aucun fullbuild
RE812, runtime jeu, gameplay, accessibilité naturelle ni GREEN global.
AnimateItem et DoorControl ne sont pas activés.

Incident historique : première écriture du run.py producteur hors mutation lock,
conservée; historical_lock_compliance=false, aucune certification rétroactive.
Premier child bloqué après lectures non utilisé comme preuve. PASS limité au
contenu/replay privé, pas approbation d'intégration ou de publication publique.
La revue indépendante finale de ces fichiers de publication reste pending.

## Frontier

RE813 planned-not-proven : nouvelle preuve caller/registration et provenance de
control, puis composition réelle. Pas de répétition de matrice ni activation
globale AnimateItem/DoorControl. BLOCKED-006 existant couvre toujours la
natural reachability; aucun nouveau blocker nécessaire.
