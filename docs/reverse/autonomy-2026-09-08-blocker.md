# Arrêt autonome du 8 septembre 2026 — preuve insuffisante

Statut : **bloqué ; aucune reconstruction source autorisée**.

## Tracker de progression

- [x] Date contrôlée avant travail : fenêtre autorisée jusqu'au 8 septembre 2026 à 23h45 Europe/Paris.
- [x] Git live vérifié : base `6d6f1089`, synchronisée avec upstream après fetch ; seul le rapport utilisateur non suivi est présent.
- [x] RE-702 et RE-731 relus : contrat comportemental et autorisation de patch absents ; domaine/pivot non sélectionnés.
- [x] Audit indépendant en lecture seule des alternatives et des métadonnées locales effectué.
- [x] Suite complète exécutée : `python3 -m pytest tests/reverse -q` — **3293 passed**.
- [x] Décision : arrêter la progression plutôt que créer une nouvelle série de tickets de durcissement.

## Blocage précis et alternatives examinées

Le handoff terminal requiert un contrat comportemental attribuable à la cible et une preuve ABI suffisante. Les identités lexicales et relations d'appels disponibles ne remplissent pas ce contrat.

L'audit indépendant a examiné la mesure du texte : `GetStringDimensions` est un stub dans `SPEC_PSXPC/TEXT_S.C`, avec une implémentation alternative dans `SPEC_PSXPC_N/TEXT_S.C`. La concordance des prototypes ne prouve pas l'ABI cible. La dépendance `GetStringLength` de la branche destinataire nécessite elle aussi une preuve du contrat de métriques et des caractères de contrôle ; copier l'enveloppe seule n'est pas une reconstruction cohérente. Les gates RE-167/168 ne fournissent pas l'équivalence manquante.

Autres pistes examinées par l'audit : `Straighten` ne dispose pas d'une attribution binaire suffisante ; `init_water_table` contient déjà un corps et le complément PC ne peut pas être déduit de preuves PSX ; `RestoreLevelData` reste bloquée sur les identités, largeurs et ordres de restauration. Aucune de ces pistes n'a été déclarée patch-ready. Cette revue bornée n'est pas une preuve d'impossibilité globale.

## Conditions de reprise

Apporter ou établir, pour une unité cohérente, l'attribution à la version cible, le contrat observable et les identités/types/largeurs ABI nécessaires. La mesure du texte est une hypothèse concrète, **pas un prochain ticket autorisé ni prêt**. Le handoff RE-731 et le dashboard restent terminaux et inchangés.

Aucun changement production, aucun nouveau générateur, aucune modification de marqueur, aucun artefact protégé produit. Le rapport non suivi `report-tech-2026-08-30-10h.md` n'a pas été ouvert ni modifié. La suppression du runner identifié par la liste des jobs est une opération de clôture, à vérifier dans le rapport de livraison.
