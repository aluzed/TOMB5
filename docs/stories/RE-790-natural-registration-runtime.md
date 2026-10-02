# RE-790 — Registration naturelle observée dans le moteur

2 octobre2026, parent RE789, baseline publique `02e91b8e`. **Progression concrète : relink et runtime neufs ; producteur atteint naturellement.** Aucun correctif moteur nouveau.

## Tracker
- [x] Date/propriétaire vérifiés et verrou exclusif acquis ; suppressions utilisateur et rapport non suivi préservés.
- [x] Quatre TUs actuelles compilées fraîchement : GETSTUFF, SETUP, OBJECTS, BRIDGE_CALLBACKS ; link i386 réussi.
- [x] Démarrage et contrôles réels, deux appels ObjectObjects observés ; slots enregistrés sans substitution.
- [x] Rome : 151 items, aucun bridge ; 750 draws, contrôle libéré naturellement au draw300, captures inspectées.
- [x] Corpus RE791 puis BASE RE792 exécutés plutôt que reproduire une matrice synthétique.
- [ ] Callback bridge naturel et effet consommé : toujours absents. Handoff RE-794.

## Preuves et portée
Archives privées `build/reverse/autonomy-20261002/re790-runtime/`. Relink mixte, pas fullbuild : quatre TUs fraîches, autres objets historiques. Exécutable, 124 inputs explicites, quatre sources et 127 headers déclarés contrôlés ; inputs implicites et closure historique complète non attestés.

920 paires GetCeiling et100 collisions retenues/recomptées. Totaux finaux de breakpoint15874/623 : compteurs archivés, pas trace intégrale ni nombre de tests. Aucun callback parmi les douze entrées surveillées. L’absence de bridges dans cet inventaire explique pourquoi cette route ne peut fournir le témoin recherché.

run01 : TypeError de sonde conservé ; run02 : GDB wrapper0, jeu tué volontairement au checkpoint, displays/groupes nettoyés. Worker timeout600s après résultat utilisable ; récupération parent, pas fin de fenêtre. Captures réelles livrées directement, pas assets dans Git.

Revue large `re790-review/verdict.json` **FAILED conservée** : pas d’approbation sécurité/provenance globale. La revue ultérieure RE792 accepte seulement sélection/registration BASE. **pas de GREEN global** sanitaire/gameplay.

## Handoff
RE-794 : navigation native vers une dépendance bridge authentique, observation callback puis consommation, sans injection. Autorisation deadline existante jusqu’au2octobre23h ; pas de GO par lot ni cron ajouté.
