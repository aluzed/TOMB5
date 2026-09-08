# RE-738 — Voix occupées et retour couleur dans les tranches appelantes

## Statut et progression

**Preuve cible étendue au recyclage et à la contention séquentielle ; aucune reconstruction C supplémentaire.** Suite de RE-737.

- [x] Projet Ghidra existant ouvert en lecture seule après contrôle des processus/verrous.
- [x] Identité du boot et du payload vérifiée ; instructions exécutées authentifiées.
- [x] Recyclage, refus, remplacement et réutilisation étudiés dans Ghidra puis exécutés.
- [x] Quatre tranches appelantes réelles exécutées, dont leurs instructions de passage vers la couleur.
- [x] Séquences avec état CPU/RAM conservé et temporisation réellement exécutée.
- [x] Toutes les matrices et les guards réexécutés par le parent.
- [x] Revue indépendante ; décalage de libellé des résultats corrigé par régénération.
- [x] Dashboard et handoff actualisés.
- [ ] Contrat portable complet du producteur de couleur et de ses consommateurs établi.
- [ ] Tests RED sur le code C réel puis reconstruction si ce contrat est démontré.

## Preuves acquises

Le boot local est authentifié, son header est vérifié et son payload comparé octet pour octet avec l'entrée utilisée. Le projet Ghidra existant est traité en lecture seule. Le harness vérifie les octets de chaque instruction CPU exécutée, borne le nombre d'instructions et exige le retour réel. Le pont COP2 reste limité aux transferts de contrôle déjà étudiés dans RE-737 ; aucun retour audio ou SDK n'est remplacé.

Les chemins testés distinguent récupération d'une ou plusieurs voix terminées, allocation depuis la pile libre, refus quand les voix occupées ne sont pas remplaçables, choix de remplacement et réutilisation d'un doublon. L'exclusion de la voix zéro du scan de remplacement et le choix du plus grand indice à égalité sont corroborés par les instructions et les assertions. Le cas de doublon plus fort actualise les enregistrements logiciels sans écriture MMIO sur le chemin observé : cela ne démontre pas un effet sonore immédiat.

| Vérification réexécutée par le parent | Résultat |
|---|---:|
| Matrice de voix occupées | 864 / 864 |
| Quatre matrices de tranches appelantes | 864 / 864 chacune |
| Séquences persistantes de remplissage, pression et réutilisation | 4 / 4 |
| Demandes audio dans ces séquences | 136 |
| Frames d'entrée dans ces séquences | 3 964 |
| Contrôles négatifs d'authentification et de bornage | 6 / 6 |
| Comparaison avec une banque alternative de transferts COP2 | 864 lignes intégralement identiques |

Les séquences partent d'un allocateur synthétique vide cohérent, rempli ensuite par les appels cibles. Elles ne réinitialisent ni la pile libre, ni les canaux, ni la temporisation entre demandes. Les changements externes d'enveloppe SPU sont injectés explicitement et enregistrés. Les canaux logiciels, le compteur libre, les appels de libération et certaines écritures MMIO sont assertés.

Dans ces fixtures, la valeur volatile issue de l'audio est de nouveau écrasée par le code d'entrée. Le passage réel vers le consommateur de couleur conserve les valeurs attendues et les seize mots de couleur correspondent. Ce résultat s'applique aux conditions SDK échantillonnées, pas à tout état d'entrée possible.

## Revue et limites

Le reviewer a inspecté les probes, les données et les portions pertinentes de l'export Ghidra. Il a réexécuté indépendamment les 864 cas voix et les quatre séquences. Un libellé ancien persistait dans les résultats des séquences ; la reproduction complète du parent a régénéré ces résultats depuis les scripts actuels.

La « contention » désigne ici des voix occupées dans une exécution séquentielle : ni interruption, ni réentrance, ni exécution parallèle ne sont validées. Les quatre tranches ne prouvent pas les fonctions appelantes complètes ou leurs préconditions dans le jeu. Les fixtures sont non spatialisées ; elles ne couvrent pas toutes les branches audio. MMIO en RAM, enveloppes synthétiques, aucun SPU physique ou rendu sonore. La pile libre et le masque logiciel sont enregistrés mais moins complètement assertés que les canaux et le compteur. La banque alternative garde le même CPU émulé et les mêmes fixtures : ce n'est pas un second oracle matériel.

Aucun changement de production, aucun test C de reconstruction ni suite globale revendiqués. Les sorties volumineuses restent ignorées. Le rapport utilisateur non suivi est préservé.

## Reproduction locale

Commande exécutée par le parent avec code de sortie zéro :

```sh
bash build/reverse/autonomy-20260908/re738-voice-proof/reproduce.sh
```

Cette commande recompile le pont, réexécute les matrices, les séquences, les guards et la comparaison de banque. Probes, Ghidra, traces et résultats bruts restent dans ce répertoire ignoré. La synthèse versionnée n'est pas une promesse de reproduction depuis un clone sans les entrées locales protégées.

## Handoff immédiat

La récupération des voix n'est plus le manque de preuve immédiat pour les chemins étudiés. Examiner maintenant le domaine complet des retours SDK qui atteignent le consommateur de couleur et la représentation C de son producteur : prouver les branches restantes et les préconditions des appelants, puis écrire les tests RED sur l'unité C réelle si un contrat portable cohérent se dégage. Ne pas convertir la valeur observée sur ces fixtures en constante universelle. Si cette unité ne peut être attribuée de façon sûre, changer de cible cohérente plutôt que multiplier les variantes de matrices audio. L'autorisation autonome reste valable jusqu'au 8 septembre 2026 à 23 h 45, Europe/Paris.
