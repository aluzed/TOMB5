# RE-701 — identité fonctionnelle des marqueurs source non implémentés

## Progress tracker

- [x] Handoff RE-700 validé fail-closed, y compris ses compteurs et ses blocages.
- [x] Chaque marqueur `UNIMPLEMENTED()` actif est rattaché à une fonction source par son périmètre lexical.
- [x] L’export ne contient que chemin, symbole source et compteurs ; il n’ajoute aucune preuve comportementale, ABI ou binaire.
- [x] Aucune unité de production n’est sélectionnée ou autorisée.

## Décision

L’identité lexicale réduit l’inventaire à des fonctions nommées, mais elle ne prouve pas leur comportement ni leur ABI. RE-702 devra refuser toute sélection tant qu’un contrat comportemental source-backed manque.
