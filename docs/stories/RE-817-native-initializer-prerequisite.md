# RE817 — préalable initializer natif privé récupéré

Statut **RECOVERED_PRIVATE_NATIVE_INITIALIZER_PREREQUISITE_PASS**; revue indépendante
**PRIVATE_ONLY_PASS**. Acceptation du candidat privé uniquement; publication finale
encore en attente de revue parent séparée. Aucun GO production/intégration/activation.

## Preuve acceptée et provenance

Le producer timeout600 original reste **NON CERTIFIÉ**, inventaire historique
75 fichiers immuable. La première tentative du reviewer est rejetée pour erreur
instrumentale d’observation allocator; attempt01 reste conservée. La récupération
indépendante corrigée est distincte et ne certifie rétroactivement aucun timeout.
Verdict privé `292a83d4c523f0d1f9e05607f89c3800c93d6fccafad798faa28d2d72ff73141`;
manifest privé `eb338c1e1950dbfbd025ed65fb3856818d905d8ab3137a79a465717f4605ed76`
avec 235 entrées vérifiées. Candidat privé exact
`449d24af4532ee267f3ba07f8e9c2f7792cbdf0005d3d1d4f7b286ffe8b9f5dd`, jamais versionné.

Cible fraîche directe initializer depuis RAM RE816 archivée : 994 visites hooks
(non instructions retirées), 2992 octets sélectionnés. Registres de départ construits;
ce n’est ni la continuation CPU du caller ni une extraction nouvelle.
Actual-TU DOOR privé avec ITEMS, GETSTUFF et COLLIDE réels, normal et strict
ASan/UBSan failfast : baseline comportementale RED exit1 dans les deux modes,
candidat GREEN exit0 dans les deux modes. Stderr runtime vide, warnings legacy
compilation conservés. ShutThatDoor4, GetDoor5 et ItemNewRoom1 réels.
Projection indépendante 2980 octets natifs, 2980 corruptions mono-octet et
11 corruptions d’événement rejetées **dans chaque mode**; deux mutants code rejetés.

## Limites et readiness

Une fixture seulement : generic284, angle0, rooms0..3, portal2 et sentinelle255.
Allocation native82 contre cible92; projection déclarée et rebasing pointeurs,
pas identité ABI. L’allocateur natif est un **double déclaré**, non allocateur réel.
Entrée weak privée directe, **pas registration ni InitialiseItem natifs**.
Aucune preuve domaine général, composition caller native, startup, hardware,
wholeRAM, gameplay, sécurité mémoire générale, production ou GREEN global.
Les états pending historiques RE815/816 sont gelés, pas réécrits; cette preuve
met à jour seulement la frontière courante. BLOCKED-003/004/006 restent ouverts;
BLOCKED-001/002 supprimés ne sont pas recréés. Quatre échecs historiques
RE801/802 restent à comparer exactement, non à masquer.

## Tracker et acceptance suivante

- [x] Récupération indépendante privée distincte authentifiée, baseline RED/candidat GREEN.
- [x] Oracle projeté et événements discriminants, deux mutants code rejetés.
- [x] Publication metadata-only avec TDD, suffixe dashboard exact et CSV sûr.
- [ ] Revue finale indépendante de cette publication par parent.
- [ ] RE818 : préalable composition conditionnelle producer/caller **actual-native**,
  registration/callback et retour réels, oracle indépendant borné, RED/GREEN normal/strict,
  provenance exacte et revue séparée; travail non effectué ici.
- [ ] Allocateur réel, élargissement du domaine et revue d’intégration distincte.

Acceptance d’une preuve privée n’autorise aucune activation ou modification source.
