# RE956 — Deux gains revus, un blocage exécutable transférable

## Décision
Jalon documentaire metadata-only. Publication : snapshot **PENDING**, à qualifier par revue indépendante des hashes de livraison ; ce statut historique ne sera pas réécrit après revue. Fini 16/17 : **SCOPED PASS** ; tentative 18 : **SCOPED PASS diagnostique seulement**, objectif producteur→consommateur **INCOMPLETE**. Strict/procédure **INCOMPLETE** ; integration=false, production_patch=false. Aucun rejeu natif ni nouvelle RE dans ce jalon.

## Gains acceptés, non composés
- **16** : véritables réponses ACK puis Complete produites, consommées par les corps OpenBIOS authentifiés via **HOST polling conditionnel** après CPU. Revue neuve historique : cinq builds/runs, normal et UBSan positifs, trois mutants normaux native0/oracle1. Ce n'est pas une IRQ CPU naturelle ; adaptation de lecture volatile abandonnée qualifiée par mutant.
- **17** : véritable Memory IRQ issue du ACK cdlInit → vrai caller CPU branchTest → tail architectural d'exception → vecteur MIPS assemblé/lié (quatre instructions) puis quatre NOP handler. **8 instructions exécutées ; neuvième adresse de fetch tentée, non retirée.** Revue neuve historique : quatre builds/runs, deux contrôles normal/UBSan, deux mutants normaux native0/oracle1 ; ELF réassemblé identique et effet CP0 vérifié. Status initial activé, placement/copie vectoriels et handler sont des fixtures, pas boot naturel. Oracle architectural distinct mais événement/input partagés, pas second modèle CDROM.
- **Aucune composition 17→16** : le vecteur17 n'exécute pas le handler16, ne consomme pas Complete, pas RFE cible. innerInit retourne0 **avant CPU**, jamais preuve d'initialisation réussie.

## Blocage18 reproduit, pas GREEN
Nouveau moteur Unicorn2.1.4, **pas continuation du CPU17**. TU threads.c et alloc.c entières inchangées compilées MIPS R3000 o32 little-endian, lien GC ; caller/heap/table/linker privés de fixture, psxprintf diagnostic. Chemin kern_initheap → initThreads → B0Handler → kern_malloc visité, store processBlockSize=4 puis UC_ERR_EXCEPTION après105 visites hook. Visite ne signifie pas retirement ; pointeurs process/thread nuls, aucun consumer exécuté. ELF frais reviewer identique ; native0/**oracle1**, zéro GREEN fonctionnel. EXCP_RI20 est un numéro interne moteur, **pas CP0 Cause matériel**. Dernière branche légale, micro-branche passe mais état complet non résolu ; enlever lecture PC hook n'aide pas. O2/24KC/data séparées n'aident pas. UBSan compile cible mais lien runtime échoué : **pas PASS UBSan**.

## Limites et suite
Pas de TU CPU complète, ABI Sony, matériel ou gameplay. Les FAIL bootstrap/timeout/doublelock/oracle, warnings read3 et qualifications postseal17 restent conservés ; aucun échec rétrocertifié. Blocage global **non terminal** : isoler état moteur/delay slot ou moteur alternatif validé, même ELF/entrées, vrais retours allocateur et pointeurs avant consumer. Pas patch allocateur de contournement, faux pointeurs ou injections de succès.

## Livraison et conservation
Cinq nouveaux fichiers publics seulement, export minimal autonome, tests documentaires/guards. README, suppressions volontaires et RE955 immuables préservés. Aucune suppression : 0 fichier/0 octet ; mesures espace et preuves essentielles conservées dans bundle auteur privé scellé. Aucun stage/commit/push/job. Les résultats natifs cités sont historiques, non rejoués ici.

[Metadata](../reverse/generated/re956_cd_init_reviewed_frontiers.json) · [Dashboard](../reverse/tomb5-progress-dashboard-re956-v1.html) · [Handoff autre modèle](blocked/BLOCKED-008-re956-mips-allocator-engine-handoff.md)
