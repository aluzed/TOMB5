# RE-947 — préparation correction arithmétique RNG

PRIVATE_ACCEPTED · PUBLIC_REVIEW_PENDING · INTEGRATION_NOT_YET. Production inchangée.

Domaine fini authentifié : 8 sequences, 208 events (176 générations, 32 seeds), empreinte fixtures/oracle `b2ce731009c8142ae9a5ade7a5be73a93d7e60d6d464bfef6a6c03f766b62384`. SOURCE fingerprint baseline `cc943333afdcb2777a70f3f8db744257ab39004f2ae109f0787a97c6ac82c989`, proposé `81928509ec45fe9c4a66d771886e131eac1bc6b91754fde116a49fb44fd0ce32`.

Actual-TU complet, vrais headers, GCC i386 C++11 O0, gc-sections avec defs, pas ignore-unresolved. Prérequis publics : g++ multilib, headers SDL2, Python3 (stdlib; pytest facultatif).

Reproduction : `python3 tests/reverse/test_re947_rng_actual_tu.py --output /tmp/re947-fresh-absent`. RE945 : `python3 tests/reverse/test_re945_rng_actual_tu.py --output /tmp/re945-fresh-absent`. Les tests refusent une source inconnue; inverse exact autorisé uniquement en copie privée pour préserver RE945 avant-RNG.

Historique RED normal : 87 différences Draw sur 208 événements; RED strict : overflow Control, Draw vérifié séparément. Candidat GREEN normal/strict sur 208 événements chacun, pas preuve global-TU-clean. Cinq mutants exacts avec identités d'événements figées : overflow Control, overflow Draw, extraction >>15, propriétaires d'états échangés sans changer seeds, multiplication historique (label draw-multiply mais modifie les DEUX returns). stdout historique strict peut être tamponné : zéro ligne observée ne signifie pas zéro instruction exécutée.

Oracle indépendant Python entiers arbitraires : modulo 2^32, quotient 2^16 modulo 2^15; non dérivé de sortie candidat. Produit maximum 4739561886808924620 < 2^64; réduction uint32; stockage signed via soustraction int64 dans [-2147483648,-1], conversion dans plage long32, seed idem. Sortie high15 unsigned, aucun shift négatif requis.

FAILs historiques conservés (overflow et erreur de schéma reviewer corrigée dans recovery); revue privée acceptée n'est PAS revue publique ni autorisation d'intégration. Parent seul applique après revue indépendante des hashes exacts. natural excluded : callers RNG complets, gameplay, SDK, hardware, HI/LO, bootstrap et gaps. globalprocedure=false. RE930 BIU/kernel/SPU et unités refusées, RE944 cmd1 TranslateItem/LoadLevel/equivalence STOP; aucune matrice fermée rejouée.
