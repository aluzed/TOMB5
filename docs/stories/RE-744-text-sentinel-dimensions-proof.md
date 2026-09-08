# RE-744 — Sentinelle graphique et dimensions du texte

## Statut et progression

**Recherche réellement exécutée, revue indépendante favorable avec limites. Aucun correctif de production ; contrat complet des accents toujours ouvert.**

- [x] État live après RE-743 et identité cible vérifiés, le 8 septembre 2026 à partir de 21 h 48 Paris.
- [x] Nouvelle inspection Ghidra headless du texte, sans accès concurrent au projet ; journal complet avec fin d'inspection et code retour nul.
- [x] Expérience causale sur les lectures de teintes des glyphes sentinelles, sans remplacement d'instruction.
- [x] Comparaison de GetStringLength et GetStringDimensions sur la vraie unité source, métriques privées authentiques.
- [x] Quatre tests de caractérisation privés réussis ; expériences réexécutées par le parent.
- [x] Audit indépendant en lecture seule : agrégats recomptés depuis les lignes, empreintes recoupées, aucune erreur relevée.
- [ ] Contrat d'entrée réel des accents/sentinelles et état vivant des données adjacentes.
- [ ] Représentation portable fidèle de la chaîne complète, avant reconstruction.

## Attribution et méthode

Même boot US PSX que RE-743, payload authentifié par SHA-256 et mémoire Ghidra concordante. Le chargement bas provient de l'en-tête et des vérifications précédentes, sans substitution par une base KSEG supposée. L'inspection fraîche et ses détails restent dans `build/reverse/autonomy-20260908/re744-sentinel/`, ignoré.

La sentinelle précédant les glyphes ordinaires recouvre la fin d'une routine cible ; elle n'est pas une fiche graphique indépendante que l'on pourrait recopier aveuglément. Son contenu diffère du préfixe historique hôte sur deux champs de métrique. L'égalité des tables ordinaires ne prouve donc pas l'équivalence de ce préfixe.

Le probe restaure CPU et RAM avant chaque appel, borne l'exécution et ne remplace aucune instruction. Deux exécutions ne diffèrent que par le remplissage synthétique d'une zone immédiatement après la table de teintes. Les événements de glyphes et les primitives décodées sont comparés ; seules les coordonnées XY, UV et les couleurs RGB sont couvertes, pas tous les champs des paquets ni une image matérielle.

## Résultat causal : mesure, géométrie et couleur séparées

| Famille | Cas | Lectures hors table de teintes | Variation des couleurs après perturbation |
|---|---:|---:|---:|
| Accents sans sentinelle | 2 720 | Aucune lecture observée | 0 cas |
| Accents sélectionnant la sentinelle | 960 | Présentes dans les 960 cas | 960 cas |

Les 46 entrées accentuées testées comprennent 12 sélections sentinelles. La matrice parcourt dix couleurs et huit combinaisons de drapeaux ; **14 720 appels cibles** couvrent mesure/rendu et les deux remplissages. Les assertions établissent l'invariance des mesures et de la géométrie XY/UV entre remplissages, mais pas des couleurs sentinelles.

Cela démontre une dépendance aux données adjacentes dans le dispositif synthétique, **pas les couleurs réellement présentes en jeu**. La mémoire synthétique lisible ne rend pas une indexation C hors tableau valide.

## GetStringDimensions : nouvelle équivalence bornée, pas reconstruction complète

Le suffixe authentique du loader est rejoué avec ses doubles de services fichier déjà déclarés. Ses sorties sont identiques à celles de l'expérience antérieure : 250 vues terminées utilisables, une vue non terminée exclue sans réparation.

Le harness compile la vraie `SPEC_PSXPC_N/TEXT_S.C` en mode `signed char`, avec ses en-têtes ordinaires et des métriques authentiques conservées uniquement en privé. Il vérifie l'accord des tables ordinaires avant comparaison. Quatre valeurs de ScaleFlag, chaînes chargées, séquences synthétiques de blancs/contrôles et longues transitions de lignes sont parcourues.

| Matrice | Cas | Écarts GetStringLength | Écarts GetStringDimensions |
|---|---:|---:|---:|
| Sans octets accentués | 4 300 | 0 | 0 |
| Accents construits | 552 | 184 | 552 |

Les résultats sont identiques en compilation normale et sous ASan/UBSan, sans diagnostic sur ces appels de mesure. **9 704 appels cibles** ont été exécutés. Il s'agit d'une équivalence bornée sur le sous-ensemble sans accents et d'une caractérisation des divergences sur l'autre sous-ensemble ; les tests qui attendent les divergences ne sont pas des tests d'équivalence complète.

## DrawChar réel : diagnostic distinct de l'atteignabilité

Un appel direct à la vraie fonction avec une copie locale de la fiche sentinelle déclenche un débordement global sous ASan et un accès hors dimension interne de la table de teintes sous UBSan. Le témoin avec glyphe ordinaire réussit dans les deux modes. Les sorties sentinelles non nulles sont attendues par ces tests de caractérisation.

Ce harness **ne démontre pas qu'un appelant réel du jeu fournit ce pointeur**. Il montre qu'une simple représentation locale de la fiche sentinelle ne suffit pas à rendre son rendu sûr. Aucun remplacement des données adjacentes par une couleur arbitraire, aucun changement global du signe de char et aucune politique de rejet ne sont intégrés.

## Vérification et reproduction privée

Depuis `build/reverse/autonomy-20260908/re744-sentinel/` :

```sh
PYTHONDONTWRITEBYTECODE=1 ../venv/bin/python test_dimensions.py
PYTHONDONTWRITEBYTECODE=1 ../venv/bin/python probe.py
```

Parent : **4 tests réussis**, puis expérience sentinelle réussie avec les compteurs ci-dessus. Régression publique : `python3 -m pytest tests/emulator tests/reverse/test_generate_tomb5_progress_dashboard.py -q` — **1 199 tests réussis**, aucun diagnostic. Revue indépendante : lecture des scripts, setup hérité et journaux ; recomptage de `sentinel-rows.json` et `dimensions-rows.json` ; pas de réexécution par le reviewer. Les mesures des deux remplissages ne sont pas archivées séparément : leur invariance repose sur les assertions effectivement rejouées.

Preuves privées : `InspectSentinel.java`, `ghidra-text.txt`, `headless.log`, `probe.py`, `sentinel-summary.json`, `sentinel-rows.json`, `test_dimensions.py`, `dimensions.py`, `tu_harness.cpp`, `dimensions-summary.json`, `dimensions-rows.json`, journaux de compilation et d'instrumentation. Les tests privés imposent certains seuils plutôt que tous les comptes exacts ; ceux publiés ici ont été recomptés par la revue.

Ces scripts sont liés au HEAD de RE-743 et refusent après 23 h 10 Paris le 8 septembre 2026. Leur réexécution après publication demande une nouvelle adaptation explicitement autorisée des gardes ; ils ne constituent pas une CI autonome sans assets. Seuls cette note et le dashboard sont destinés à la publication, sans tables, dumps ou instructions.

## Handoff

**Prochaine unité cohérente :** établir quels appelants et quelles chaînes réellement chargées peuvent sélectionner la sentinelle, puis attribuer l'état vivant des données de teintes adjacentes avant de choisir une représentation portable. Les 250 vues chargées de cette expérience ne contiennent aucun octet accentué ; les cas accentués restent construits. Si cette piste ne fournit pas le contrat, changer de domaine de reconstruction plutôt que multiplier ses variantes.

GetStringDimensions dispose désormais d'une preuve bornée sans accents, mais sa dépendance au décodage accentué interdit de la déclarer entièrement reconstruite. Ce résultat ne bloque pas la recherche autonome globale autorisée jusqu'à 23 h 45 Paris. Les inventaires terminaux historiques restent inchangés.
