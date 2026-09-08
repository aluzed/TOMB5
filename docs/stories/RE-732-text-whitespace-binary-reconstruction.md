# RE-732 — Mesure du texte : reconstruction des espaces et tabulations

## Statut et périmètre

**Terminé — implémentation et revue indépendante validées.**
Unité retenue : traitement des espaces et tabulations de `GetStringLength`
dans `SPEC_PSXPC_N/TEXT_S.C`, avec effets observables dans `GetStringDimensions`.
Ce n’est pas une reconstruction complète du rendu ou de tous les caractères.

Autorisation : autonomie avec recherche Ghidra jusqu’au 8 septembre 2026,
23:45 Europe/Paris. Cette preuve nouvelle est distincte de l’inventaire historique
clos RE-731 : aucun ancien CSV terminal ni refus historique n’est réécrit.

## Progression

- [x] Vérifier dépôt, identité locale, version du boot et exactitude du payload.
- [x] Reprendre le projet Ghidra terminé, sans processus concurrent ni verrou.
- [x] Décompiler le boot, la mesure, les dimensions et leurs appelants.
- [x] Recouper les instructions, delay slots, arguments, globale et tables.
- [x] Faire auditer indépendamment la preuve et restreindre le périmètre sûr.
- [x] Observer RED : 12 échecs comportementaux, 9 cas déjà conformes.
- [x] Corriger uniquement les deux branches prouvées ; GREEN : 21 cas.
- [x] Vérification complète : 3368 tests réussis ; revue indépendante approuvée.
- [x] Livraison préparée : sept fichiers sûrs explicitement indexés et contrôlés.

## Preuves acquises

La cible est le boot final PSX NTSC v1.0 `SLUS_013.11` documenté par
`CONTRIBUTING.md`, MD5 `4ef523e708d7a7d6571f39c6e47784f9`.
Le payload correspond exactement au boot sans son en-tête PS-X EXE.
L’import utilise la base basse et l’entrée réellement fournies par cet en-tête.
Le boot confirme les références basses et la construction explicite des alias
KSEG pour pile/heap : aucun rebasing arbitraire n’a été appliqué.

L’attribution ne repose pas seulement sur un commentaire d’adresse :

- Graphe d’appels : mesure utilisée par rendu texte, dimensions et requête UI.
- ABI : chaîne et deux sorties optionnelles, retour de largeur ; écritures de
  métriques sur 16 bits. Les dimensions appellent cette même mesure.
- Globale : même opérande relatif au GP pour le drapeau écrit par le rendu
  à partir du bit d’échelle et lu par la mesure ; initialisation du GP inspectée.
- Données : correspondance exacte des 106 entrées `CharDef` et des 46 paires
  `AccentTable` avec les tableaux déjà présents dans le dépôt, vérifiée
  indépendamment puis recoupée localement. Aucune donnée ajoutée.
- Contrôle : lecture directe des instructions et de leurs delay slots.
  Les globals suggérées par la décompilation automatique sont incohérentes
  pour le GP ; elles ne sont pas utilisées comme preuve d’identité.

### Décision d’implémentation

| Comportement | Preuve cible | Décision |
|---|---|---|
| Espace réduit | L’avance normale précède la réduction dans un delay slot ; résultat positif de six unités | Remplacer la soustraction isolée par l’avance correcte |
| Tabulation | Minimum vertical étendu jusqu’à moins douze ; conserve les valeurs déjà inférieures | Corriger le seuil, y compris minima préalables moins onze et moins dix |
| Largeur de tabulation, maximum vertical, drapeau | Comportement existant concordant | Inchangés, testés |
| Dimensions et sauts de ligne | Lectures signées des métriques et stockage final sur 16 bits | Source inchangée, effets du correctif testés |
| Accents et octets hauts | Substitution prouvée, mais certains indices sortent du tableau C | Aucun correctif spéculatif |

Les corrections ne changent ni signature, ni structure, ni données, ni marqueur
de reconstruction. Elles n’élargissent pas les entrées acceptées. Les défauts
préexistants du chemin accentué ne sont pas présentés comme corrigés.

## Vérification

`tests/emulator/test_text_measurement.py` compile le vrai fichier source avec
ses en-têtes habituels et élimination des sections de rendu inutilisées au lien.
Les glyphes utilisés par le harness sont **synthétiques**, jamais extraits.
Couverture : espaces normaux/réduits/répétés, tabulation après glyphes aux
bornes, sorties optionnelles, sentinelles verticales, conservation du drapeau,
chaînes vides, contrôles et composition multiligne.

- Baseline avant modification : 3346 tests emulator/reverse réussis.
- RED : 12 échecs attendus de valeurs, aucune erreur de compilation.
- GREEN ciblé : 21 tests réussis.
- Régression complète emulator/reverse : 3368 tests réussis, aucune régression.
- Revue indépendante de livraison : approuvée, aucun défaut bloquant.
- Guards des fichiers indexés : texte uniquement, aucune donnée brute ou lourde,
  aucun secret détecté ; `git diff --check` propre.
- Le dashboard historique conserve ses validations ; il pointe vers le suivi
  distinct `docs/reverse/reconstruction-progress.html`.

## Handoff de recherche — pas un arrêt du runner

Prochain objectif : **prouver le domaine des caractères et les accès aux
métriques des accents**, ou sélectionner un autre cluster cohérent si cette
piste n’est pas exploitable. Douze entrées de la table existante substituent
un espace, puis le binaire utilise la zone précédant le premier glyphe ; les
octets au-delà de la plage d’accents peuvent également excéder le tableau C.
Une transcription naïve en indexation de tableau serait indéfinie sur l’hôte.
Il faut établir les entrées réellement autorisées ou une représentation sûre
et fidèle avant de modifier ce chemin. Ne pas inventer un glyphe de secours.

Les lectures signées de `GetStringDimensions` ne justifient pas à elles seules
un nouveau micro-correctif : la conversion finale sur 16 bits peut rendre les
résultats existants équivalents ; démontrer d’abord une différence observable.

Les preuves détaillées et journaux restent uniquement dans le répertoire
ignoré `build/reverse/autonomy-20260908/` : `text-inspection.txt`,
`text-inspection.log`, `headless.log`, `text-red.log`, `baseline-tests.log`.
Ils contiennent des données de travail non publiables et ne doivent jamais
être ajoutés au commit. Aucun accès au rapport technique non suivi demandé.
