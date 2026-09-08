# RE-745 — Chargeur cible et consommateur du texte chargé

## Statut et progression

**Preuve d’exécution bornée acquise et revue ; aucune reconstruction de production supplémentaire.**

- [x] État live et identité Git vérifiés après RE-744, le 8 septembre 2026 à partir de 22 h 26 Paris.
- [x] Deux inspections Ghidra réussies : chargeur, services fichiers et cache CD ; détails privés conservés.
- [x] Chargeur exécuté depuis son entrée jusqu’au retour avec services fichiers et parseur de répertoire cibles.
- [x] Cache de répertoire comparé à une analyse indépendante de l’ISO.
- [x] Branche DisplayConfig exécutée sur les pointeurs et octets conservés du chargeur.
- [x] Six tests privés rejoués par le parent et par une revue indépendante ; neuf sorties reproduites à l’identique par la revue.
- [x] Régression publique : 1 199 tests réussis, sans diagnostic.
- [ ] Atteignabilité des accents et de la vue non terminée depuis d’autres chemins réels.
- [ ] Contrat portable complet du texte : non prouvé ; aucune activation spéculative.

## Nouvelle preuve, distincte des matrices précédentes

RE-744 utilisait le suffixe de chargement et des doubles de services fichiers. Cette unité exécute le chargeur depuis son entrée, les routines FILE_Length et FILE_Load, la recherche et la construction du cache CD ainsi que l’allocation cible. Les services fichiers ne sont plus remplacés par des retours préparés. Les secteurs proviennent de l’ISO américain examiné ; les 30 entrées produites par le parseur cible concordent avec l’analyse ISO indépendante.

Même boot US PSX authentifié que RE-744 ; contrôle des instructions du payload rencontrées contre les octets de référence dans les deux phases. Les journaux Ghidra incluent leurs marqueurs de fin et une sortie réussie ; les avertissements de recouvrement interdisent de prendre le pseudo-C seul comme preuve. Aucun patch d’instruction n’est introduit. Les frontières modélisées ci-dessous sont exclues de cette affirmation d’exécution authentique.

Le chargeur teste successivement les cinq premiers noms de langue absents, puis sélectionne US.DAT. Ce disque contient ce seul fichier parmi les langues candidates du script. **Cela ne prouve pas l’absence d’autres éditions du jeu.** L’inventaire privé de plusieurs chemins ISO retrouve une même identité de contenu, sans prétention d’exhaustivité globale.

## Résultats vérifiés

| Observation | Résultat |
|---|---:|
| Entrées de répertoire cible concordantes | 30 |
| Appels de longueur / recherches CD / chargements | 7 / 9 / 2 |
| Vues chargées terminées dans leurs bornes | 250 |
| Vue non terminée dans ses bornes | 1 |
| Octets accentués dans les vues terminées | 0 |
| Impressions de la branche DisplayConfig | 16 |
| Libellés chargés distincts utilisés | 8 |
| Primitives CPU produites | 48 |
| Accents et glyphes sentinelles sur ce chemin | 0 |

Les sorties du chargeur concordent avec l’expérience antérieure. La vue non terminée n’est ni réparée ni utilisée comme chaîne C sûre. La branche DisplayConfig conserve les pointeurs et données du chargeur : ce lien producteur/consommateur est plus fort qu’un simple passage de copies de chaînes à PrintString.

## Limites explicites

- Tas, pile, état initial CD et configuration UI synthétiques. DisplayConfig est lancé directement après le chargeur, pas par un démarrage complet ni une navigation réelle du jeu.
- Deux comparaisons BIOS sont modélisées ; les commandes de positionnement, transferts de secteurs et synchronisations CD sont modélisés. Les transferts utilisent les secteurs authentiques. Ce n’est pas une exécution intégrale du BIOS, du SDK ou du lecteur.
- Couleurs et tampons graphiques synthétiques ; primitives CPU, pas rendu matériel GPU.
- Zéro dépassement observé parmi les lectures de texte surveillées. Le hook ne classe que les accès commençant dans le bloc chargé : ce n’est pas une garantie générale de sûreté mémoire.
- Zéro accent/sentinelle signifie absence sur ce chemin, non validation de leur traitement. Cette preuve ne résout pas les divergences et dépendances adjacentes de RE-744.
- Les contrôles initiaux RED portaient sur l’API de recherche absente et des champs de résultat manquants, pas sur un défaut de production démontré.

## Reproduction et revue

Preuves exclusivement dans `build/reverse/autonomy-20260908/re745-reachability/` ignoré : scripts Ghidra, journaux de décompilation, `reachability.py`, `caller.py`, `test_reachability.py`, résultats et `review.md`. Aucun secteur, instruction, table ou décompilation versionné.

```sh
PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260908/re745-reachability/test_reachability.py
python3 -m pytest tests/emulator tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

Parent : **6 tests privés réussis**, puis **1 199 tests publics réussis**. Revue indépendante : lecture des scripts et sorties Ghidra, rejeu des six tests en interceptant uniquement les écritures de résultats en mémoire ; neuf sorties identiques octet pour octet. Les limites ci-dessus incorporent ses réserves. Ghidra n’a pas été relancé par le reviewer.

Les probes sont liés au HEAD antérieur à cette publication et expirent le 8 septembre à 23 h 20 Paris. Une réexécution ultérieure exige une adaptation autorisée de ces gardes, sans perdre leur provenance. Ils dépendent d’assets privés et ne constituent pas une CI publique autonome.

## Handoff

La piste des autres langues n’apporte pas de corpus accentué supplémentaire sur l’ISO disponible. Ne pas multiplier les variantes de cette matrice. **Prochaine unité cohérente : changer de domaine vers les services de chargement/allocation effectivement attribués ici, comparer leurs contrats et dépendances aux vraies unités hôtes, puis choisir une reconstruction seulement sur écart comportemental prouvé.** Une piste de texte ne doit être rouverte que par un nouvel appelant ou une nouvelle entrée authentique, pas par une autre combinaison de caractères construits.

Le dashboard de reconstruction est actualisé ; les inventaires terminaux RE-702/731 restent inchangés. La recherche globale reste autorisée jusqu’au 8 septembre 2026 à 23 h 45 Paris.
