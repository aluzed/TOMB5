# RE-711 — cohérence directionnelle du handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal autoritaire RE-702, le dashboard et les protections RE-703 à RE-710 ont été relus avant modification.
- [x] L'inventaire des handoffs RE-420+ ne présente aucune direction incohérente : une clôture utilise `TBD` et `none`, une reprise utilise un ticket `RE-<nombre>` et un sujet explicite.
- [x] Des tests RED couvrent un ticket non canonique, une clôture avec sujet de reprise, et une reprise sans sujet.
- [x] Le générateur rejette désormais ces états au lieu de les afficher comme un backlog ambigu; le dashboard RE-702 reste déterministe et terminal.

## Décision

Cette protection metadata-only et fail-closed ne réouvre pas RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.