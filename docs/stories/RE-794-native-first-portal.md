# RE-794 — Premier portail natif réellement observé

## Résultat testé
Le run03 du relink natif existant observe un premier changement de room au draw94 sans input joueur. Une commande XTest Up réelle est ensuite tenue pendant 60 draws; arrêt volontaire au draw161 par debugger, pas sortie naturelle du jeu. Aucun téléport, appel ni écriture de l’inférieur. Un seul portail est revendiqué; aucun callback bridge naturel.

Quatre observations comparées: 169 rooms, 11459 cellules et 16944 bytes de floor_data par observation, cellules et stockage portal_storage identiques au corpus. Seuls les champs immuables de room et les buffers explicitement comparés sont couverts; pas égalité des records runtime entiers. La sélection de cellule/portail est corroborée indépendamment, sans trace entrée/retour GetFloor/GetDoor. Les 20 observations ProcessClosedDoors sont plafonnées, pas un total d’appels.

## Revue et historique
PASS indépendant strictement borné: cohérence des archives run03 et checker; aucune nouvelle exécution runtime par la revue. run01 incomplet et run02 interrompu restent archivés; le manque de capture portal_storage de run02 ne démontre pas un bug moteur. Ancien verdict RE794 incohérent non réhabilité. Relink de provenance mixte, pas fullbuild, pas de GREEN global.

## Tracker
- [x] Première traversée naturelle et commande réelle établies sur le runtime natif.
- [x] Comparaisons de buffers revues dans leur périmètre explicite.
- [ ] Attribuer les helpers par trace dédiée; poursuivre une route bridge bornée.
- [ ] Valider gameplay global et fullbuild.

## Suite
RE-795 établit le producteur door manquant; RE-796 et RE-797 bornent les preuves. RE-798: reconstruction privée de l’initialiseur et fermeture des dépendances; callback bridge naturel toujours bloqué. Voir BLOCKED-004-door-production-prerequisites et le manifeste metadata-only re794-re797-door-progress.json.
