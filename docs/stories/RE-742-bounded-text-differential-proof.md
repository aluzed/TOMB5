# RE-742 — Contrat différentiel borné du texte

## Statut et progression

**Recherche exécutée ; modèle borné concordant sur la matrice testée, source de production divergente. Aucune reconstruction complète ni modification de production.**

- [x] État live et version cible relus ; HEAD de référence `18478c80`.
- [x] Reprise des expériences locales RE740/RE741, sans refaire les audits terminaux.
- [x] Inspection Ghidra en lecture seule et authentification de la mémoire cible.
- [x] Contrats de recherche écrits avant leur implémentation ; journaux RED conservés localement.
- [x] Suffixe du loader rejoué et vues réellement chargées consommées sans ajout de terminateur.
- [x] Comparaison exacte modèle C / MIPS des métriques, glyphes, événements et primitives.
- [x] Vraie unité `SPEC_PSXPC_N/TEXT_S.C` compilée sans modification avec ses en-têtes.
- [x] Quatre tests de recherche réussis ; modèle ASan/UBSan recompilé, 2 955 cas sans diagnostic.
- [x] Rejeu parent des quatre tests et du modèle instrumenté réussi.
- [x] Revue indépendante finale favorable : scripts et preuves lus, comptes et empreintes recalculés, modèle instrumenté réexécuté.
- [ ] Intégration production : non prête pour le contrat complet.

## Continuité et attribution

RE-739 demeure la dernière reconstruction de production. RE740 et RE741 désignent ici des expériences privées intermédiaires, pas des tickets publics fictivement clôturés. Leurs scripts, résultats et conclusions se trouvent dans les répertoires ignorés `re740-research` et `re741-language` sous `build/reverse/autonomy-20260908/`.

Cette unité reprend la cible US PSX attribuée au boot `SLUS_013.11`, avec le chargement vérifié lors des unités antérieures. La nouvelle inspection Ghidra du texte est conservée dans `re742-differential/ghidra-text.txt` avec son journal headless et le contrôle d'empreinte de la mémoire. Les instructions ne sont ni copiées ici ni substituées pendant les exécutions CPU. Les pointeurs, adresses et données des tables restent privés.

## Corpus chargé, pas seulement conteneur décodé

Le suffixe du loader est réexécuté avec les données authentiques ; fichiers chargés et preuve sont identiques aux archives RE741. Il commence après le chargement initial du script, avec contexte construit et doubles des services de longueur/chargement de fichiers : ce n'est pas une validation du CD, de l'allocation ni du démarrage complet.

Les **250 premières vues** contiennent un terminateur dans leurs bornes. La dernière entrée ne le contient plus après le décodage cible et est rejetée, sans réparation silencieuse. Le défaut connu du loader concerne des écritures hors zone textuelle nominale ; ni dépassement de l'allocation réelle ni corruption d'un objet vivant n'est établi ici.

Le corpus US ne contient pas de texte accentué élevé. Les accents et transitions combinées sont donc explicitement synthétiques.

## Résultats différentiels

| Domaine | Cas | Résultat |
|---|---:|---|
| Vues authentiques, huit combinaisons de drapeaux | 2 000 | Modèle / MIPS concordants |
| Accents admissibles, contrôles et lignes synthétiques | 848 | Modèle / MIPS concordants |
| Exécutions des fonctions cibles | 5 696 | Retour normal dans la borne d'instructions |
| Événements DrawChar et primitives comparés | 30 288 chacun | Aucun écart dans les champs comparés |

Comparaisons : largeur et bornes verticales de première ligne, sélection des glyphes de mesure, séquence/couleur/position des événements de rendu, coordonnées XY, UV et RGB des quatre sommets. Les teintes sont synthétiques et non uniformes pour détecter les erreurs de sélection. CPU et RAM sont restaurés entre cas ; les lectures de la zone de chaînes sont contrôlées contre la vue nominale.

Le modèle rejette les 12 substitutions sentinelles, 82 octets hors plage, neuf contrôles bas non admis, une vue sans terminateur, une couleur invalide, une borne invalide et une chaîne trop longue. Ces rejets constituent une **politique de sécurité expérimentale**, pas une équivalence cible pour les entrées rejetées. Le rejet avant émission est vérifié pour les neuf contrôles bas, pas exhaustivement pour toutes les classes.

## Source réelle : divergences, pas faux GREEN

Le harness injecte les métriques privées authentiques dans la table de mesure et vérifie leur raccordement aux tables de rendu déjà présentes. **Aucun glyphe de rendu réécrit et aucune fonction de production copiée dans le harness.**

| Mode hôte / corpus authentique | Cas mesurés et rendus | Mesures divergentes | Rendus divergents |
|---|---:|---:|---:|
| signed char | 2 000 | 0 | 88 |
| unsigned char | 2 000 | 1 984 | 1 984 |

En signed, les 88 différences authentiques sont uniquement RGB, sans écart de nombre de primitives, XY ou UV. Les huit variantes de la séquence synthétique de contrôles diffèrent aussi en couleur. Les accents synthétiques produisent 544 mesures divergentes ; leur rendu signed n'est pas exécuté, car il risque d'utiliser une couleur invalide.

En unsigned, la largeur authentique reste inchangée, mais les bornes verticales et les positions divergent. Le changement de signe du champ `CHARDEF.YOffset` est une explication à vérifier isolément, **pas un correctif à appliquer globalement**. Parmi ces cas, 88 diffèrent aussi en UV/RGB ; leur cause n'est pas réduite ici au décalage vertical. Un cas accentué unsigned reproduit l'assertion existante dans `GetStringLength`, sans la supprimer.

Les tests de la source réussissent parce qu'ils **caractérisent ces divergences connues**, non parce que la source est équivalente au modèle. ASan/UBSan portent uniquement sur le modèle hôte et ne prouvent ni sécurité de la source ni validité des accès sur console.

## Reproduction et limites

Dossier privé : `build/reverse/autonomy-20260908/re742-differential/`.

Depuis ce dossier, séquentiellement :

```sh
PYTHONDONTWRITEBYTECODE=1 ../venv/bin/python test_contract.py
PYTHONDONTWRITEBYTECODE=1 ../venv/bin/python test_tu.py
cc -std=c11 -Wall -Wextra -Werror -g -O1 -fno-omit-frame-pointer -fsanitize=address,undefined -DSANITIZE_MAIN model.c -o model_sanitized
ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 ./model_sanitized cases.bin
```

Résultats vérifiés : trois tests de contrat et un test de caractérisation source ; 2 955 enregistrements instrumentés. Résumés détaillés : `summary.json`, `tu-summary.json`, `CONCLUSIONS.md`. Les journaux `parent-contract.log` et `parent-tu.log` attestent le rejeu parent après la première vérification.

Ces outils privés nécessitent les entrées authentifiées et le venv Unicorn. Ils exigent le HEAD de référence et comportent des gardes temporelles : arrêt de RE742 à 23h30 le 8 septembre 2026, dépendances à 23h45. Une relance après livraison/date différente nécessite réautorisation et adaptation explicite de ces gardes, pas leur contournement implicite. Le dépôt public seul ne reproduit pas cette matrice ; aucun asset ni dump n'est publié.

RAM, pile, appelant, teintes et buffers sont synthétiques. Coordonnées et couleur initiales fixes ; huit combinaisons de drapeaux, pas toutes les entrées possibles. Pas de GPU réel, de résultat visuel, d'accents authentiques localisés ni de boucle de jeu complète validés. La mesure différentielle vise `GetStringLength`, pas une nouvelle preuve complète de `GetStringDimensions`.

## Handoff concret

**Prochaine unité : établir puis intégrer un contrat cohérent de sélection et couleur des glyphes pour le backend PSXPC_N.** Repartir des écarts ci-dessus, isoler les conversions d'octets du signe des métriques, prouver les transitions de couleur et le raccordement des tables. Ajouter des tests publiables à métriques synthétiques sur la vraie unité avant toute correction ; confronter ensuite le résultat aux données privées et faire relire indépendamment.

Ne pas transformer le resolver expérimental en politique de rejet de production sans contrat d'entrée. Les sentinelles et la dernière chaîne mal terminée restent des limites distinctes à traiter explicitement. Aucun ancien inventaire terminal n'est rouvert et aucune impossibilité globale n'est déduite de ces limites. Dashboard actif mis à jour séparément ; historique terminal inchangé.
