# RE-949 — CD init : registres et production de queue, checkpoint privé

Scope fini accepté séparément par deux revues indépendantes ; verdicts stricts refusés, procédure **INCOMPLETE**. `integration=false`, `production_patch=false`. Cette publication ne certifie ni les procédures historiques ni une intégration.

Autorisation directe du 14 octobre 2026 : développement autonome jusqu’à 18h Europe/Paris. Suite comportementale de RE948, sans republier ses fichiers non suivis ni réécrire ses acquis.

## Tracker
- [x] Attribuer index, masque et acquittement CD aux sources ouvertes épinglées.
- [x] TDD comportemental privé et oracle scalaire C++ compilé distinct.
- [x] Replays continus fresh/restored, refus atomiques et mutants sensibles.
- [x] Revues indépendantes des deux projections finies ; refus stricts conservés.
- [ ] Prouver la timebase CPU et le dispatch CDRFIFO avant callback.
- [ ] Initialisation CD complète, intégration production et gameplay : non prouvés.

## Progrès exécuté, et limites
Unité01 : cinq accès CD exécutés, projection des registres index/masque/ack comparée à un oracle extrait des sources ouvertes. Le modèle refuse ensuite la première commande. La revue identifie toutefois que le scheduler natif intervient déjà pendant l’ack : la frontière commande ne constituait pas une preuve du périphérique complet.

Unité02 : ack → enqueue CDRFIFO réellement produit, délai source 797 µs / 26993 cycles, target/lowest/masque conservés. Arrêt immédiatement après cet enqueue, avant la prochaine instruction et avant tout callback : la timebase CPU héritée n’est pas justifiée pour livrer l’événement. Aucun callback, commande, secteur ou succès CD injecté.

Les replays fresh/restored concordent sur RAM complète 2 Mio, GPR et CP0 ; unité02 compare aussi la queue et le suffixe des PCs. Les chronologies brutes distinctes et le contexte pré-entrée restent conservés, pas normalisés en identité globale. Entrée OpenBIOS et FIFOs vides construites ; pas de reset matériel/Sony ni preuve load-delay/cache ou fidélité CPU globale. Oracle scalaire extrait compilé, pas actual-TU/ABI complet ni oracle matériel.

## Tests et revue : attribution
Ces résultats sont ceux des exécutions du tick conservées dans les archives privées, non un replay effectué par le test public de metadata.
- Unité01 : 273 comparaisons oracle, six refus et six mutants ; revue indépendante recompilation et quatre replays, plus 10374 accès acceptés et 14202 refus atomiques.
- Unité02 : 12 timings producteur, quatre refus et cinq mutants ; revue indépendante recompilation, 36 cas timing/lowest/ack répété, quatre refus atomiques et contrôle clear nonvide, six mutants et six replays.
- Verdicts stricts `passed=false` : bootstrap/argv et diagnostics avant mutex non certifiés, dépassements de budgets demandés conservés ; la deuxième revue conserve aussi son mauvais probe initial et un diagnostic écrasé. Les plafonds transport de 600 s restent distincts des budgets demandés.
- Metadata et dashboard publics possèdent leurs propres tests RED/GREEN ; ils ne prouvent pas un nouveau comportement CPU/CD. Leur revue de publication est distincte de l’acceptation des preuves privées.

## Provenance et frontière utile
PCSX-Redux commit c313b116e6a55786bc127c9b3a07a90b55d97c21, GPL-2.0-or-later ; nugget/OpenBIOS commit 7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30, MIT. Sources consommées comparées aux blobs épinglés ; firmware hérité authentifié, pas recompilé. Aucune donnée jeu ou instruction propriétaire publiée.

Prochain travail causal : attribuer les incréments CPU et l’arbitrage branchTest, puis dispatch CDRFIFO/runCommand, avec tests sensibles et arrêt à la dépendance réelle suivante. Ne pas rejouer des revues documentaires pour blanchir la procédure ; ne pas imposer un polling constant ou une réponse favorable.

[Metadata et pins des quatre bundles](../reverse/generated/re949-cd-init-checkpoint.json) · [Dashboard RE949](../reverse/tomb5-progress-dashboard-re949-cd-init-v1.html).

## Nettoyage
DONE pour ce checkpoint : zéro suppression ; toutes preuves uniques, premiers FAILs, sources épinglées et seals conservés. Mesures et ledgers privés dans les unités et leurs revues ; aucune récupération physique revendiquée. État utilisateur, suppressions volontaires et publications non suivies antérieures préservés. Les bundles privés restent sous build/reverse/autonomy-20261014 ; cette story ne les exporte pas.
