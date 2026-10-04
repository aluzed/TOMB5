"""RE830 portable documentary contract; no private imports/builds/replays."""
import hashlib
import re
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BLOCKER = "docs/stories/blocked/BLOCKED-006-re811-animation-producer-frontier.md"
DASHBOARD = "docs/reverse/tomb5-progress-dashboard.html"
BEFORE_BLOCKER = "a9c5a04d69c030a8e8c47915a345223e44a32eecadaa5c6cd5f7d20e8bbb4a59"
BEFORE_DASHBOARD = "5b8c2a8776586b87a54d8774803cd0896b438d72ead7e024f1557978247c1608"
VERDICT = "12fd8f2ec92803b88c5dc3fb123c0b2dc002c7d7e40fb840f42fb5e8ebac73b6"
APPEND = """
## RE830 — provenance table LIFTS; readiness blocked

Progression : attribution du producteur RelocPtr[MOD_LIFTS], pas activation.
DEPENDENCY_BLOCKED; readiness=blocked; publication_review=PENDING_FINAL_REVIEW;
publication_review_approved=false; integration_approved=false; production_patch=false;
natural_startup_proven=false; gameplay_proven=false; behavioral_GREEN=false.

Huit modules réellement loader-produits et huit buffers relocalisés complets
comparés dans les archives privées. Le header du niveau3 choisit les descripteurs
30/23/29/17/12/2/7/49 → module_ids22/15/21/9/4/1/2/41.
Index de descripteur != identifiant logique module : MOD_LIFTS49 existe au
descripteur57 NON sélectionné; le choix49 produit module41, pas LIFTS49.
RelocPtr[MOD_LIFTS] reste NULL; aucun pointeur/module substitué pour obtenir GREEN.
ObjectObjects inchangé : 620 visites archivées, arrêt gardé avant NULL, pas retour
complet; runner exit0 / contrat comportemental exit1, donc PAS GREEN fonctionnel.

Comparaison RAM complète8MiB au delta RE829 réutilisé : neuf différences stack;
pas whole-RAM GREEN ni oracle whole-RAM indépendant. Cause sauvegardes loader
plausible, non observée dynamiquement. Framework/GP/SP/heap construits, services
CD doublés; suffixe loader, pas LoadLevel entier. Pas startup naturel, native frais,
gameplay, cohérence upstream ou intégration prouvés par cette publication.

Revue indépendante addendum : PASS contenu fini, security_concerns=[] et
logic_errors=[]; sans replay/build nouveau. FAIL reviewer initial préservé
(erreur de comparaison reviewer, pas régression cible); FAIL procéduraux historiques
RE829/RE830 inchangés, historical_procedural_acceptance=false. Aucune approbation publique
finale ni audit/replay parent revendiqué; parent a lu rapports/verdict, vérification
du manifest parent non encore revendiquée.
Verdict addendum SHA256 : 12fd8f2ec92803b88c5dc3fb123c0b2dc002c7d7e40fb840f42fb5e8ebac73b6.
Rapport addendum SHA256 : 509490f26a07ec46fc37a8a16a1a16c726fcc24b992a8891e8839746fc17c2c9.
Provenance locale : build/reverse/autonomy-20261004/re830-table-provenance-proof/HANDOFF.md
et build/reverse/autonomy-20261004/re830-independent-review-addendum/RAPPORT.md;
archives consommées, aucun nouveau runtime cible/native ni générateur historique.

### Vérification documentaire après réparation des gardes historiques
Sélection littérale RE819 + RE820 + RE821 + RE830 : 57 passed, exit0 observé.
Douze régressions successor-only foreign/duplicate/altered/missing/history/unknown
et reconstruction exacte du seul delta RE830 de test819 : GREEN documentaire.
Les empreintes anciennes et assertions historiques restent inchangées; aucun
append futur générique accepté. Premier résultat littéral 32 passed / 2 failed,
exit1, préservé dans re830-publication/literal-predecessors-plus-new.json; les
archives de première publication FAIL ne sont pas réécrites ni requalifiées.
Résultat frais : build/reverse/autonomy-20261004/re830-publication-guard-repair02/sensitive-green.json.
Ce GREEN metadata-only ne prouve aucun comportement cible/native ni acceptation
procédurale historique. Revue indépendante exacte des six fichiers + manifest
PENDING_FINAL_REVIEW; aucune intégration/activation approuvée.

### Acceptation manquante / prochaine frontière (autorisation séparée)
- [ ] Réconcilier sélection naturelle niveau/header/modules et objects réellement
  chargés en amont, sans flags hérités ni injection de pointeur/module.
- [ ] Ou établir un niveau authentique sélectionnant le descripteur MOD_LIFTS57
  avant registration, avec domaine objects cohérent et producteur naturellement atteint.
- [ ] Régression publique comportementale actual-TU RED sensible puis preuve bornée
  indépendante des buffers complets et événements ordonnés dans ce domaine naturel.
- [ ] Revue finale indépendante des six fichiers publics exacts : PENDING_FINAL_REVIEW.
- [ ] Revue et autorisation distinctes avant intégration; aucune activation
  AnimateItem/DoorControl, aucun startup/gameplay ou GREEN global revendiqué.

Les critères historiques restent ouverts. La frontière est sélection naturelle
module/objects, pas un nouveau caller construit répétitif ni substitution57 à49.
[Progression RE830 / overview actif](../../reverse/tomb5-progress-dashboard.html#re830-publication).
"""
SECTION = """
<!-- RE830 PUBLICATION BEGIN -->
<section id="re830-publication" data-readiness="blocked" data-private-review="PASS_CONTENT_FINITE" data-publication-review="PENDING_FINAL_REVIEW" data-integration-approved="false">
<h2>ACTIVE RE830 — provenance table LIFTS, progression / readiness blocked</h2>
<p><a href="../stories/blocked/BLOCKED-006-re811-animation-producer-frontier.md#re830--provenance-table-lifts-readiness-blocked">BLOCKED-006 / RE830 / acceptation manquante</a>. DEPENDENCY_BLOCKED; publication_review_approved=false; production_patch=false; behavioral_GREEN=false. Aucun critère global coché ni activation.</p>
<p>Overview courant limité à RE830. Le bloc RE821 et son pending historique sont conservés byte-identiques : ils ne décrivent pas la revue courante ni le prochain front RE830; aucune clôture rétroactive de RE821 revendiquée.</p>
<p>Huit modules loader-produits, huit buffers relocalisés complets comparés. Header niveau3 : descripteurs30/23/29/17/12/2/7/49 → module_ids22/15/21/9/4/1/2/41. MOD_LIFTS49 existe au descripteur57 NON sélectionné; choix49 → module41, RelocPtr[MOD_LIFTS] reste NULL. ObjectObjects : 620 visites, arrêt gardé avant NULL, pas retour complet; runner exit0 / contrat exit1, PAS GREEN fonctionnel.</p>
<p>RAM complète8MiB contre delta RE829 réutilisé : neuf différences stack, pas whole-RAM GREEN ni oracle whole-RAM indépendant. Cause sauvegardes loader plausible, non observée dynamiquement. Framework/GP/SP/heap construits, services CD doublés; suffixe loader, pas LoadLevel entier/startup naturel/native frais/gameplay/cohérence upstream.</p>
<p>PASS contenu fini addendum indépendant, security_concerns=[] / logic_errors=[]; sans replay/build. FAIL reviewer initial et FAIL procéduraux historiques RE829/RE830 préservés; historical_procedural_acceptance=false. Pas audit/replay parent revendiqué; manifest parent non encore revendiqué vérifié. Verdict SHA256 : 12fd8f2ec92803b88c5dc3fb123c0b2dc002c7d7e40fb840f42fb5e8ebac73b6. Revue des six fichiers publics exacts PENDING_FINAL_REVIEW; intégration distincte non approuvée.</p>
<p>Vérification documentaire après réparation : sélection littérale RE819 + RE820 + RE821 + RE830, 57 passed / exit0 observé; douze régressions successor-only et reconstruction exacte du seul delta test819, empreintes historiques inchangées. Premier résultat littéral 32 passed / 2 failed exit1 conservé dans les archives de première publication, sans réécriture. GREEN metadata-only, pas GREEN comportemental ni acceptation procédurale historique. Six fichiers + manifest à revoir indépendamment : PENDING_FINAL_REVIEW.</p>
<p>Prochaine frontière proposée, autorisation séparée : réconcilier sélection naturelle niveau/header/modules et objects réellement chargés en amont, ou niveau authentique sélectionnant MOD_LIFTS57 avant registration avec objects cohérents. Exiger régression publique actual-TU RED sensible, buffers complets/événements indépendants et revue distincte avant intégration. Pas de flags hérités, pointeur/module injecté, substitution57 à49 ou nouveau caller construit répétitif. AnimateItem/DoorControl non activés; aucun GREEN global. <a href="../stories/blocked/BLOCKED-006-re811-animation-producer-frontier.md">Blocker ouvert</a>.</p>
</section>
<!-- RE830 PUBLICATION END -->
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def preceding_blocker(data):
    assert data.endswith(APPEND.encode()), "RED: RE830 blocker append absent or altered"
    before = data[:-len(APPEND.encode())]
    assert digest(before) == BEFORE_BLOCKER
    return before


def preceding_dashboard(data):
    suffix = SECTION.encode() + b"</html>"
    assert data.endswith(suffix), "RED: RE830 dashboard section absent or altered"
    assert data.count(b"<!-- RE830 PUBLICATION BEGIN -->") == 1
    assert data.count(b"<!-- RE830 PUBLICATION END -->") == 1
    before = data[:-len(suffix)] + b"</html>"
    assert digest(before) == BEFORE_DASHBOARD
    return before


def safe_added_output(text):
    assert not re.search(r"0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b|\b(?:1efa94|11502c|b17f8|b18e4)\b", text)
    assert not re.search(r"(?:integration_approved|publication_review_approved|production_patch|gameplay_proven|natural_startup_proven)=true", text)


def test_re830_blocker_append_exact_and_readiness():
    data = (ROOT / BLOCKER).read_bytes()
    preceding_blocker(data)
    text = data[-len(APPEND.encode()):].decode()
    safe_added_output(text)
    assert "- [x]" not in text and text.count("- [ ]") == 5
    assert VERDICT in text and "PENDING_FINAL_REVIEW" in text


def test_re830_dashboard_exact_inverse_and_current_links():
    data = (ROOT / DASHBOARD).read_bytes()
    preceding_dashboard(data)
    safe_added_output(SECTION)
    assert "ACTIVE RE830" in SECTION and "pending historique" in SECTION
    assert (ROOT / "docs/reverse" / "../stories/blocked/BLOCKED-006-re811-animation-producer-frontier.md").is_file()
    assert "../../reverse/tomb5-progress-dashboard.html#re830-publication" in APPEND
    assert "PENDING_FINAL_REVIEW" in SECTION and VERDICT in SECTION


@pytest.mark.parametrize("path,inverse,addition", [(BLOCKER, preceding_blocker, APPEND), (DASHBOARD, preceding_dashboard, SECTION)])
def test_re830_inverse_rejects_history_and_suffix_mutants(path, inverse, addition):
    data = (ROOT / path).read_bytes()
    inverse(data)
    for mutant in [data+b"foreign", data+addition.encode(), data.replace(b"620", b"621"), data.replace(addition.encode(), b""), b"foreign"+data]:
        with pytest.raises(AssertionError):
            inverse(mutant)


@pytest.mark.parametrize("forbidden", ["0x12345678", "FUN_123456", "payload_offset", "word_le_hex", "data:image", "```mips", "integration_approved=true", "11502c"])
def test_re830_added_output_safety_rejects_forbidden_mutants(forbidden):
    with pytest.raises(AssertionError):
        safe_added_output(APPEND + forbidden)


def test_re830_predecessor_contracts_on_explicit_historical_projection(monkeypatch):
    # Explicit projection separately verifies historical preservation.
    # Current literal acceptance is exercised separately, without monkeypatch.
    old_dashboard = preceding_dashboard((ROOT / DASHBOARD).read_bytes())
    old_blocker = preceding_blocker((ROOT / BLOCKER).read_bytes())
    original = Path.read_bytes
    def projected(path):
        if path.resolve() == (ROOT / DASHBOARD).resolve():
            return old_dashboard
        if path.resolve() == (ROOT / BLOCKER).resolve():
            return old_blocker
        return original(path)
    monkeypatch.setattr(Path, "read_bytes", projected)
    re821 = runpy.run_path(str(ROOT / "tests/reverse/test_re821_publication.py"))
    re821["test_re821_documentary_publication_and_exact_historical_inverse"]()
    re819 = runpy.run_path(str(ROOT / "tests/reverse/test_re819_publication.py"))
    re819["test_append_only_dashboard_blocker_and_exact_inverse_code"]()


def test_re830_literal_predecessor_contracts_without_projection():
    re819 = runpy.run_path(str(ROOT / 'tests/reverse/test_re819_publication.py'))
    re821 = runpy.run_path(str(ROOT / 'tests/reverse/test_re821_publication.py'))
    re819['test_append_only_dashboard_blocker_and_exact_inverse_code']()
    re821['test_re821_documentary_publication_and_exact_historical_inverse']()


@pytest.mark.parametrize('index', [0, 1, 2])
@pytest.mark.parametrize('mutation', ['altered', 'duplicate', 'missing'])
def test_re830_test819_delta_reconstruction_fail_closed(index, mutation):
    re820 = runpy.run_path(str(ROOT / 'tests/reverse/test_re820_publication.py'))
    text = (ROOT / 'tests/reverse/test_re819_publication.py').read_text()
    inverse = re820['original_test819_before_re830']
    assert digest(inverse(text).encode()) == '69bebe456d9326bd154e1fcea6149f92afcbc3ecca3d17132cc80e9594ecf59c'
    old, new = re820['RE830_TEST819_DELTAS'][index]
    replacements = {'altered': new.replace('RE830', 'RE83X', 1) if 'RE830' in new else new.replace('blocker_before_re830', 'blocker_before_re83x', 1),
                    'duplicate': new + new, 'missing': old}
    mutant = text.replace(new, replacements[mutation], 1)
    assert mutant != text
    with pytest.raises(AssertionError):
        inverse(mutant)


def test_re830_test819_unapproved_change_rejected_by_original_pin():
    re820 = runpy.run_path(str(ROOT / 'tests/reverse/test_re820_publication.py'))
    g = re820['api']()
    path = 'tests/reverse/test_re819_publication.py'
    text = (ROOT / path).read_text()
    inverse = re820['original_test819_before_re830']
    assert digest(g['inverse_code'](inverse(text), path).encode()) == g['OLD'][path]
    for mutant in [text + '# foreign\n', text.replace('NON CERTIFIÉ', 'CERTIFIÉ', 1)]:
        with pytest.raises(AssertionError):
            assert digest(g['inverse_code'](inverse(mutant), path).encode()) == g['OLD'][path]
