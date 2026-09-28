# BLOCKED-001 — Clôture bornée RE-783 (contrat GetCeiling + registration bridges)

Auteur : DeepSeek V4.1 Flash via OpenCode. Reviewer : Hermes / revue indépendante.
Date : 28 septembre 2026. Périmètre : borné (contrat consommateur + registration). Aucun raw/adresse.

## Statut
Clôture **technique bornée** : correction source + composition **acceptées bornées** ; revue
indépendante **favorable (narrow_merge_ready=true)** ; sélection fraîche **84 PASS exit 0**
(81 tests parent RE-782 + 3 nouveaux). **Publication/fusion Git : PENDING — opération coordinateur**
(non effectuée ici). Ancienne copie `BLOCKED-001-getceiling-consumer-registration.md` laissée
**non suivie** (non publiée) ; la présente clôture prend préséance pour le périmètre borné.

## Tracker
- [x] Contrat consommateur cible authentifié (probe cible v10 / lot19 : 128 cas / 128 callbacks,
  vrais corps BridgeFlat/Tilt1/Tilt2) ; producteur arrêté au préfixe cible, **gameplay non validé**.
- [x] Correction `GetCeiling` + registration six slots (ObjectObjects, MIP 3072) sous guard
  `PSX_VERSION && PSXPC_TEST`, adaptateurs exactement typés, legacy conservé, corps RE-781/782 intacts.
- [x] Preuves publiques rerunnables : composition current 296/0 vs baseline 296/52 ; observer
  current 514/0 vs baseline 514/132 ; UBSan idem. `SKIP_calls` = marqueur d'installation absente,
  **pas un compteur littéral d'appels**.
- [x] Revue indépendante favorable ; 84 PASS frais (prepublication).
- [ ] Publication/fusion Git : **PENDING coordinateur**. NOTE : PENDING = seule opération publication/fusion.
- [ ] Gameplay, ABI autres backends, dette sanitaire préexistante : **dus**.

## Dettes explicites (non résolues)
Gameplay non validé ; autres backends ABI non traités ; dette sanitaire préexistante (décalage
signé GetFloor) et 7 échecs RE-778 / FAIL fade maintenus. Historique erroné conservé privé
(non revendu PASS). Modèle logiciel synthétique ; pas de buffer RAM complet.
