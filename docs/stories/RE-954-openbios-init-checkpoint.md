# RE954 — producteur Init OpenBIOS, checkpoint comportemental privé

## Tracker
- [x] Unité14 : producteur OpenBIOS exact, tests sensibles et preuve privée.
- [x] Revue indépendante finie PASS, normal et UBSan failfast frais.
- [x] Contrat public metadata et dashboard sous tests.
- [ ] Gate indépendante de publication (snapshot auteur PENDING ; décision exacte conservée séparément).
- [ ] Intégration production : non autorisée par cette preuve finie.

## Progrès vérifié
Les corps ouverts épinglés `cdromInnerInit`, `resetAllCDRomIRQs` et `enableAllCDRomIRQs` produisent la commande Init, contrairement à la commande GetLocL construite de l'unité13. Six écritures sont routées par un proxy MMIO vers les méthodes CD attribuées ; la FIFO retient Init. Une boucle CPU construite produit ensuite les cycles du scheduler, qui exécute les vrais callbacks et la table de sélection jusqu'à une garde **avant** le corps genuine `cdlInit(start=true)`.

Le retour OpenBIOS **0 est un timeout**, pas un succès : aucune IRQ n'achève l'initialisation. Les cycles CPU mesurés avant/après cette attente host sont **0/0**. Le scheduler fonctionne seulement ensuite : deadline26993, arrivée26996. Les itérations host ne sont pas des cycles MIPS.

Revue indépendante : **16** compilations et **16** exécutions natives fraîches, normal/UBSan failfast ; oracle reviewer distinct, **14** mutants rejetés par assertion après native exit0. Ces résultats sont archivés ; les tests publics vérifient des métadonnées, pas un replay privé. Le mutant nommé `no_cpu_clock` désactive en réalité la garde scheduler : il ne constitue pas une ablation de l'horloge.

## Provenance et limites
Redux : `c313b116e6a55786bc127c9b3a07a90b55d97c21`, GPL-2.0-or-later. OpenBIOS/nugget : `7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30`, MIT. Pins des manifests privés et cardinalités204/191 dans les [métadonnées](../reverse/generated/re954_openbios_init_checkpoint.json).

**PASS fini ≠ strict/procédure : INCOMPLETE.** Warnings hérités et lacunes de ledger préflight maintenus. Extraits C compilés C++20, pas TU/ABI OpenBIOS entière ni exécution MIPS naturelle. MMIO hors CD, sections critiques, configuration/SDLdummy et boucle CPU restent des fixtures déclarées. Aucun succès injecté, aucun secteur, réponse ou IRQ CD prouvé ; aucun reset Sony, hardware ou gameplay global. Frontière globale OpenBIOS inchangée et non certifiée. Aucun patch production ni intégration.

## Prochaine frontière / blocker
Exécuter le corps genuine `cdlInit` et ses producteurs légitimes d'état/IRQ/scheduling, puis composer l'attente OpenBIOS avec le CPU temporel sans réponse arbitraire. L'identité Init est attribuée ; son corps et l'initialisation complète restent non prouvés. La fenêtre recherche s'arrête17:25 ; aucun nouveau producteur ne peut tenir avec son plafond600s à ce checkpoint. Ne pas reprendre GetLocL avec un buffer secteur inventé.

## Nettoyage et conservation
Zéro suppression. Archives essentielles, seals, premiers FAILs et assets conservés. Mesure de capacité et ledger de clôture dans `build/reverse/autonomy-20261014/coordinator-handler/`, ignoré. Les changements personnels préexistants et suppressions volontaires sont préservés. Aucun entretien, job ou successeur modifié.

[Dashboard courant](../reverse/tomb5-progress-dashboard-re954-v1.html). Le snapshot de publication PENDING n'est pas une approbation ; la gate indépendante doit épingler les quatre hashes exacts avant commit/push.
