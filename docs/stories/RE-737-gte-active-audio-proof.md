# RE-737 — Retour audio actif de SayNo : obstacle COP2 levé

## Statut et progression

**Preuve cible acquise sur les chemins échantillonnés ; contrat C complet non ouvert.**
Suite directe de RE-736, sans nouvel audit terminal ni modification de production.

- [x] Descendants audio recoupés avec Ghidra et le payload authentifié.
- [x] Transferts de contrôle COP2 pris en charge avec la bibliothèque GTE existante.
- [x] Instructions CPU contrôlées contre le payload ; retour réel exigé.
- [x] Matrices et guards réexécutés intégralement par le parent.
- [x] Revue indépendante des scripts et réexécution partielle distincte.
- [x] Limites, dashboard et objectif suivant actualisés.
- [ ] Récupération, concurrence et réutilisation des voix étudiées.
- [ ] Contrat portable complet établi avant tests RED et reconstruction C.

## Méthode et preuves

Le pont utilise la bibliothèque `LIBGTE.C` existante pour les transferts CTC2/CFC2
sur trois registres de contrôle. Il ne remplace aucun retour de SayNo, du SDK
ou des fonctions audio. Les opérations non admises et les transferts en delay
slot sont rejetés. Ce pont n'est pas une émulation générale des opérations GTE.
Chaque cas réinitialise les états de l'expérience ; les instructions exécutées
sont authentifiées et l'exécution est bornée. Le chemin actif atteint les
écritures audio puis revient réellement vers le code d'entrée.

| Vérification réexécutée par le parent | Résultat |
|---|---:|
| Vecteurs de stockage et isolation du pont GTE | 3 027 / 3 027 |
| Matrice héritée SayNo, pilote désactivé | 768 / 768 |
| Matrice audio actif et témoins | 2 592 / 2 592 |
| Matrice modes et témoins | 1 728 / 1 728 |
| Guards | 5 / 5 |

Attention : seules 864 lignes de chacune des deux dernières matrices appellent
réellement l'audio et produisent des accès MMIO. Les autres sont des témoins,
notamment temporisation active et position inchangée. Ne pas présenter tous
ces cas comme des parcours audio actifs distincts.

Les assertions couvrent l'allocation de voix, certains états audio, les volumes
gauche/droite et les écritures de déclenchement. Dans ces fixtures, la valeur
volatile au retour de SayNo varie, puis le code d'entrée rétablit zéro ou deux
selon les conditions SDK testées ; les seize mots de couleur correspondent.
Cela ne prouve ni une constante universelle ni le contrat C complet.

Une banque de registres Python alternative reproduit les lignes complètes de
la matrice active. Ce recoupement conserve le même Unicorn et les mêmes
fixtures : il n'est pas une validation indépendante du CPU ou du matériel.

## Revue indépendante et limites

Le reviewer a inspecté les probes, le pont, les guards, les sorties et le
recoupement Ghidra. Il rapporte également une réexécution séparée de 81 cas
actifs et 144 cas modes, tous réussis. Verdict : obstacle COP2 de RE-736 levé
pour les chemins testés, preuve positive mais bornée.

Une voix libre est préchargée : le chemin de récupération des voix n'est pas
parcouru. Les canaux initialement libres ne couvrent pas toutes les situations
de concurrence ou de réutilisation. MMIO en RAM synthétique ; pas de SPU sonore,
DMA, interruptions, temporisation matérielle ou initialisation BIOS complète.
Toutes les écritures RAM ne sont pas assertées. Entrée puis couleur sont
appelées séparément ici : toutes les tranches appelantes de RE-736 ne sont pas
réexécutées. Aucun test C de reconstruction ni suite globale revendiqués.

## Reproduction locale et protection

Commande réellement exécutée avec succès par le parent :

```sh
bash build/reverse/autonomy-20260908/re737-gte-proof/reproduce.sh
```

Le script recompile le pont, exécute les matrices, le recoupement et les guards,
et vérifie leurs résultats. Les scripts expérimentaux, exports Ghidra, données
brutes et bibliothèque compilée restent exclusivement dans ce répertoire ignoré.
Ce jalon versionne seulement cette synthèse et le dashboard ; il ne promet pas
une reproduction depuis un clone dépourvu des entrées locales protégées.
Le rapport utilisateur non suivi reste intact.

## Handoff immédiat

Examiner dans Ghidra le recyclage et la réutilisation des voix, puis exécuter
les chemins authentifiés correspondants avec des états audio occupés. Revenir
ensuite aux tranches appelantes réelles pour borner le contrat de couleur.
Si cette piste s'épuise, sélectionner une autre unité cohérente ; cette preuve
partielle n'arrête pas l'autorisation autonome jusqu'au 8 septembre 2026 à
23 h 45, Europe/Paris. Aucun correctif spéculatif de couleur n'est autorisé par
les seuls résultats de ce jalon.
