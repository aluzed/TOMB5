# RE816 — registration naturelle puis composition conditionnelle initializer

Statut **CONDITIONAL_INITIALIZER_COMPOSITION_PASS_NATIVE_REQUIREMENT_RED**.
Revue privée indépendante **PASS_scoped**, non approbation de publication,
d'intégration, production ou activation. Publication union RE815+RE816 en attente
d'une revue finale distincte; les mentions pending RE815 restent historiques.
Verdict privé : `808046ae20f2f7df911cebdedbceb00fdbf34e44f311eee8a6c50cfe24957014`.
Manifest privé : `6115bc3346b89bb941bd4ddb804fba82587f60a90f0dfc8357f5a130d4945563`,
49 entrées authentifiées individuellement avant génération.

## Preuve bornée et frontières

Une fixture synthétique, binaires hérités authentifiés, aucune extraction fraîche.
Préfixe ObjectObjects naturel : 14 slots, 601 visites hooks, pas instructions retirées;
GP/SP/RA construits initialement, t7/t8/t9 produits sans injection.
ObjectObjects suspendu avant la famille suivante : **ni retour complet ni startup**.
Dispatch conditionnel extérieur InitialiseItem : A0/RA construits, même CPU/RAM
et SP du préfixe suspendu conservés. Callback lu naturellement depuis la table
et initializer cible complet, retour au caller puis retour caller : 1147 visites.
Ce n'est pas une preuve d'appel naturel depuis le startup.
Allocateur réel : allocation complète 92 octets; copy4, GetDoor5, shut4,
navigation et ItemNewRoom réellement exécutés, sans hooks de remplacement.
Oracle indépendant : sélection 2992 octets, 2992 corruptions mono-octet rejetées,
ledger immuable 35 événements et ordre vérifiés. Régions sélectionnées seulement,
pas wholeRAM/memory safety/hardware. Entrée initializer authentique; état
préinitializer caller non reconstruit intégralement par un oracle indépendant.

## Natif, readiness et écarts conservés

Vrais SETUP/ITEMS inchangés, i386 normal et strict ASan/UBSan failfast.
**Requirement RED exit1** dans chacun des deux modes; **characterization PASS
exit0** dans chacun. Stderr des runtimes vide, warnings de compilation distincts.
DOOR compilé puis dead-stripped au link : **initializer natif absent**, pas exécuté.
SETUP ObjectObjects natif signale Unimplemented sur stdout; aucun enregistrement
natif de porte prouvé. Characterization d'absence n'est pas GREEN comportemental.
Checker natif cell9 non discriminant; caller cell12, porte cell11, floor uniforme :
aucune équivalence floor-mutation/initializer/native revendiquée.
Deux incidents privés conservés : hypothèse SP corrigée vers SP sauvegardé;
coordonnée fixture/oracle porte corrigée avant natif. Pas de modification d'opcodes,
ni certification rétroactive des échecs RE813/RE814 originaux.
Pas controller, gameplay, activation, fullbuild, intégration ou GREEN global.

## Progression et critères

- [x] Preuve privée distincte approuvée scoped, 49 entrées vérifiées.
- [x] Publication metadata-only préparée sous contrat TDD; sources inchangées.
- [ ] Revue finale exacte du manifest PUBLIC UNION RE815+RE816.
- [ ] Implémentation/équivalence initializer native avant activation (BLOCKED-006).
- [ ] Startup, hardware, fullbuild/intégration : non prouvés; BLOCKED-003/004 restent.

RE817 privé concurrent, revue indépendante pending, non approuvé; aucun résultat
RE817 revendiqué et aucune recherche supplémentaire exécutée par cette publication.
BLOCKED-001/002 restent absents; report utilisateur non suivi préservé.
