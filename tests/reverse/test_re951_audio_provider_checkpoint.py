"""Public-only documentary contract: no private imports, source build or CPU replay."""
import copy
import hashlib
import json
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PATHS = ['docs/stories/RE-951-audio-provider-device-checkpoint.md', 'docs/reverse/generated/re951-audio-provider-checkpoint.json', 'docs/reverse/tomb5-progress-dashboard-re951-audio-provider-v1.html', 'tests/reverse/test_re951_audio_provider_checkpoint.py']
EXPECTED = {'schema': 're951.audio-provider.checkpoint.v1', 'integration': False, 'production_patch': False, 'global_acceptance': False, 'procedure': 'INCOMPLETE', 'publication_review': 'PENDING', 'author_self_check': 'PUBLIC_METADATA_ONLY', 'new_cpu_replays': 0, 'new_source_tu_builds': 0, 'cpu_frontier_unchanged': True, 'branchTest03_certified': False, 'sources': [{'name': 'PCSX-Redux', 'revision': 'c313b116e6a55786bc127c9b3a07a90b55d97c21', 'license': 'GPL-2.0-or-later'}, {'name': 'nugget', 'revision': '7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30', 'license': 'MIT', 'role': 'historical predecessor only'}, {'name': 'Circular', 'license': 'MIT', 'role': 'exact private header; no copied code'}, {'name': 'SDL3', 'version': '3.2.28', 'license': 'Zlib'}], 'units': [{'name': 'audio05', 'finite_acceptance': True, 'strict_review_passed': False, 'procedure': 'INCOMPLETE', 'producer_members': 187, 'producer_manifest_sha256': '5fbac37f5ae30b454aa67100f18fa37022f306c5f597fdf50e9ca319f00733b1', 'producer_selected_hashes': {'HANDOFF.md': '7536b2f6b74d6671b4755c0d31076ccf3c6dd845efdbb3906111ccf5fbff20dc', 'verdict.json': '0f04c4d78a04da05623b9df4d062b9b075b6463394d85814fdd72a2c6be32cd9'}, 'review_members': 144, 'review_manifest_sha256': '1f9ef1c648a663c97f1fd75c88bc2323836b5cc40ddc4145944c4ed725e56ab4', 'review_selected_hashes': {'HANDOFF.md': '7c74ef09812442671593abb89e859bdc04748c817acfd66427a5e36b9f9e8743', 'verdict.json': '1e18c055ef75bc8109e2ccacd60638d9c9f85a08be4bf790d87eeaf8dab4b37f', 'acceptance.json': 'd19dbb169132e96b057e2a87e5aefe9273decbc85e8f1fff083abac03d378453', 'audit.json': '191c73f41a9fd679a22b02692dba83324f6d6c5ffc7b85aa2375e2221f3cc70b'}, 'counts': {'test_methods': 5, 'projection_rows': 70, 'total_rows': 82, 'wait_rows': 5, 'pending_rows': 5, 'worker_rows': 1, 'composition_rows': 1, 'assertion_mutants': 8, 'fresh_reviewer_suites': 2, 'constructed_cpu_delta': 338688}}, {'name': 'audio06', 'finite_acceptance': True, 'strict_review_passed': False, 'procedure': 'INCOMPLETE', 'producer_members': 2747, 'producer_manifest_sha256': '2668c285e6218c6b8bbc307e5c790e2108bf9689df255efbc94a4995a15ce1ba', 'producer_selected_hashes': {'HANDOFF.md': '92470479e6ccceaf80ec3263845dbad8c482cb9b707ce10c1bb0c884a8e26b57', 'verdict.json': 'd51d6b10d65acd54e1cb8c7da5ed20fffa0c0ad3dccc36b9fa5b8b8eb51fe720'}, 'review_members': 2834, 'review_manifest_sha256': '223310e733edc03824890e672957886f22c104cdd6961e1445931d2137cc4606', 'review_selected_hashes': {'HANDOFF.md': 'db126f0a02828fc7fc28d2bb41fa5b554f76e815fc370ae97b511c977c4940de', 'verdict.json': 'e6eb5ea6500eb0e4c31de3930d7968b9abaa4007560b61f067a43ac13288ec24', 'acceptance.json': 'd620f15dee27b0d2f3e9283c0dfb1e21c4fc61456e815d0cf963002ff4ffa2b7', 'scopes.json': '2f7b5a6965e19de11370cab5cc68b7af6aff55a8dc75f70a3819c1e6f2196fe4'}, 'counts': {'cases': 64, 'stereo_scalars': 65760, 'field_assertions': 66016, 'wait_observations': 2, 'additional_wait_runs': 40, 'assertion_mutants': 6}, 'timing_seconds': {'producer_task': 510.88, 'producer_outer': 510.93, 'review_task': 323.5, 'review_outer': 323.55, 'requested': 480}}, {'name': 'audio07', 'finite_acceptance': True, 'strict_review_passed': False, 'procedure': 'INCOMPLETE', 'producer_members': 114, 'producer_manifest_sha256': '7367be281a4e27dce661ad50bdcd647487317487b6001eb7f026771c39575542', 'producer_selected_hashes': {'HANDOFF.md': '56226c7501ff90804bd27f49f9ce3a76a3056e87cac5406cbd1c71b5d903be9e', 'verdict.json': 'ac911fb76a2393776a43cb5284bf3cbb1d5ebc14712ea41564ccf4e839fb8541'}, 'review_members': 153, 'review_manifest_sha256': '2b876a71dd5a95d77ab9910e8406c67d7b815373c48d5a90a7c932387b4fa614', 'review_selected_hashes': {'HANDOFF.md': 'fe6aa6eeefacb270a89fd13f925f060cbbffe30d02884d310c3614fed4737fe4', 'verdict.json': 'cd85f117714096fc31c9e35fe2a712743da749a4e4bd54aa079dad03a1ad9ded', 'acceptance.json': 'f89af0238df3afaef614480299583e1dbbc8d20db25b433423161373ac93405d', 'scopes.json': '11de1999893a0c4eb2acb826ea1aa10297ed38ef1d8cfeb811a23975119946f4'}, 'counts': {'green_runs': 12, 'relational_properties': 180, 'properties_per_run': 15, 'assertion_mutants': 2, 'causal_timeout_controls': 1, 'causal_timeout_exit': 7}, 'timing_seconds': {'producer_task': 564.78, 'producer_outer': 564.82, 'review_task': 226.74, 'review_outer': 226.78, 'requested': 480}}], 'dashboard_predecessor': {'path': 'docs/reverse/tomb5-progress-dashboard-re950-cpu-counter-v1.html', 'bytes': 1916, 'sha256': '73d079f8d089de3b172ff9d764de0dba35554ede7ef639a009bbdef4dc9bb29a'}, 'next_frontier': 'NATURAL_SYSTEM_SETTINGS_LOAD_VIDEO_CONFIG_AND_CPU_AUDIO_COUNTER_CONSUMER', 'excluded': ['natural System settings load', 'natural video configuration', 'CPU audio-counter consumer', 'global branchTest03', 'CD callback and sectors', 'Sony reset', 'gameplay', 'hardware', 'global concurrency', 'atomic-wait fallback'], 'historical_failures': ['05 setup ERROR and bootstrap/nested recorder gaps', '06 initial UBSan null empty fixture FAIL; corrected valid empty fixture GREEN', '06 initial seal rejected symlinks; distinct retry retained', '07 expired or absent mutation holder after bootstrap write; later repair not retro-certification', '06 and 07 requested480 exceeded; below ceiling600'], 'authentication_scope': 'Selected manifest members and seals checked; full raw inventories parent-authenticated, not freshly replayed'}
SUFFIX = '<!-- RE951-AUDIO-PROVIDER-V1-BEGIN -->\n<section id="re951-audio-provider-v1"><h2>RE951 — contrats audio05/06/07 revus</h2><p>Publication metadata-only · PENDING · INCOMPLETE · Non intégré. Trois PASS finis indépendants ; strict passed=false, global non prouvé. Zéro replay CPU et zéro compilation TU dans cette publication.</p><h3>05 — worker et goal atomique</h3><p>5 tests, 70 projections / 82 lignes, 8 mutants par assertion ; cinq fonctions exactes et header complet, pas TU audio entière. psxcounters.cc entier. Stop/join/restart discontinu ; NTSC/VSyncWAfalse et delta338688 construits. wait [128,0] : zéro littéral, pas mesure de done.</p><h3>06 — callback direct / rings / stream</h3><p>64 cas, 65760 scalaires stéréo, 40 répétitions wait, 6 mutants. Vrais Circular et SDL3 stream ; constructeur bypass, pas device. FAIL UBSan fixture vide null conservé puis fixture vide valide GREEN ; source inchangée.</p><h3>07 — constructeur, événements et vrai device</h3><p>sdlaudio.cc lignes32–420 et header/settings/EventBus réels ; System façade. JSON Backend dummy, Device invalide, Speed1 construits ; NullSync défautfalse. Constructor → SettingsLoaded(false) → init → Run/Pause/Run → vrai callback SDL device → wait goal. 12 GREEN, 180 propriétés relationnelles ; 2 mutants pause/reset par assertion. no_advance exit7 TIMEOUT : contrôle causal seulement.</p><p>CPU inchangé, aucun gain CPU. Frontière : NATURAL_SYSTEM_SETTINGS_LOAD_VIDEO_CONFIG_AND_CPU_AUDIO_COUNTER_CONSUMER. Loader System/config vidéo/consumer CPU non prouvés ; ni CD/secteur/Sony reset/gameplay/hardware, branchTest03 non certifié. Procédures et FAILs historiques conservés, y compris holder mutation expiré/absent et budgets510.88/510.93 et564.78/564.82 &gt;480. Réparation ≠ rétrocertification.</p><p><a href="../stories/RE-951-audio-provider-device-checkpoint.md">Story RE951</a> · <a href="generated/re951-audio-provider-checkpoint.json">Métadonnées RE951</a> · <a href="tomb5-progress-dashboard-re950-cpu-counter-v1.html">Prédécesseur figé RE950</a></p></section>\n<!-- RE951-AUDIO-PROVIDER-V1-END -->\n'
PRE = EXPECTED['dashboard_predecessor']['path']

def exact(actual, expected):
    if type(actual) is not type(expected): raise AssertionError('exact type drift')
    if isinstance(expected, dict):
        if set(actual) != set(expected): raise AssertionError('schema drift')
        for key in expected: exact(actual[key], expected[key])
    elif isinstance(expected, list):
        if len(actual) != len(expected): raise AssertionError('length drift')
        for a, e in zip(actual, expected): exact(a, e)
    elif actual != expected: raise AssertionError('value drift')

def leaves(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items(): yield from leaves(item, path+(key,))
    elif isinstance(value, list):
        for key, item in enumerate(value): yield from leaves(item, path+(key,))
    else: yield path, value

def safety(path, text):
    if path not in PATHS[:3]: raise AssertionError('path rejected')
    if len(text.encode()) > 100000 or '\0' in text: raise AssertionError('heavy/binary')
    if re.search(r'0[xX][0-9a-fA-F]+|word_le_hex|raw_opcode|payload_offset|build/reverse|BEGIN .*PRIVATE KEY|api_key\s*=', text): raise AssertionError('raw/secret')
    if re.search(r'<(?:script|iframe|img|link)\b|\bsrc\s*=', text, re.I): raise AssertionError('active content')

def links(path, text):
    p=ROOT/path
    found=re.findall(r'\]\(([^)]+)\)|href="([^"]+)"',text)
    for md,html in found:
        link=md or html
        if ':' in link or link.startswith('/') or '\\' in link: raise AssertionError('unsafe link')
        target=(p.parent/link).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file(): raise AssertionError('unresolved link')
    return len(found)

def inverse(text):
    if text.count(SUFFIX)!=1: raise AssertionError('suffix drift')
    original=text.replace(SUFFIX,'',1)
    pin=EXPECTED['dashboard_predecessor']
    if len(original.encode())!=pin['bytes'] or hashlib.sha256(original.encode()).hexdigest()!=pin['sha256']: raise AssertionError('history drift')
    if text != original.replace('</html>',SUFFIX+'</html>',1): raise AssertionError('suffix location drift')
    return original

class Checkpoint(unittest.TestCase):
    def test_metadata_exists_and_exact(self):
        self.assertTrue((ROOT/PATHS[1]).is_file(), 'metadata missing')
        exact(json.loads((ROOT/PATHS[1]).read_text()),EXPECTED)
    def test_every_leaf_drift_and_numeric_alias(self):
        for path,value in leaves(EXPECTED):
            variants=[not value] if type(value) is bool else [value+1] if type(value) in (int,float) else [value+'-drift']
            if type(value) is bool: variants += [int(value)]
            if type(value) is int: variants += [bool(value),float(value)]
            for new in variants:
                mutant=copy.deepcopy(EXPECTED); parent=mutant
                for key in path[:-1]: parent=parent[key]
                parent[path[-1]]=new
                with self.subTest(path=path,type=type(new).__name__):
                    with self.assertRaises(AssertionError): exact(mutant,EXPECTED)
        mutant=copy.deepcopy(EXPECTED);mutant['unknown']=False
        with self.assertRaises(AssertionError): exact(mutant,EXPECTED)
    def test_story_substantial_tracker_limits_links(self):
        self.assertTrue((ROOT/PATHS[0]).is_file(),'story missing')
        text=(ROOT/PATHS[0]).read_text()
        for marker in ('## Tracker','## Nettoyage','## Gate indépendante','## Contrats revus','65760','180','[128,0]','338688','INCOMPLETE','PENDING','production_patch=false','zéro suppression','holder','TIMEOUT','GPL',EXPECTED['next_frontier']): self.assertIn(marker,text)
        self.assertGreaterEqual(links(PATHS[0],text),4)
    def test_dashboard_inverse_exact_predecessor(self):
        self.assertTrue((ROOT/PATHS[2]).is_file(),'dashboard missing')
        text=(ROOT/PATHS[2]).read_text()
        self.assertEqual(inverse(text),(ROOT/PRE).read_text())
        self.assertGreaterEqual(links(PATHS[2],text),5)
        for bad in (text.replace(SUFFIX,''),text.replace(SUFFIX,SUFFIX+SUFFIX),text+'trailing',text.replace('RE950','RE999',1),text.replace('65760','65761',1),text.replace('</html>','<section>unknown</section></html>')):
            self.assertNotEqual(bad,text)
            with self.assertRaises(AssertionError): inverse(bad)
    def test_output_safety(self):
        for path in PATHS[:3]:
            self.assertTrue((ROOT/path).is_file(),path)
            safety(path,(ROOT/path).read_text())
    def test_same_allowed_path_safety_negative_controls(self):
        path=PATHS[0];safety(path,'Benign symbolic audio counts 64 GPL MIT')
        for bad in ('0x1234','word_le_hex','raw_opcode','payload_offset','build/reverse/x','BEGIN RSA PRIVATE KEY','api_key = secret','<script>alert(1)</script>','binary\0','a'*100001):
            with self.assertRaises(AssertionError): safety(path,bad)
    def test_links_benign_and_bad_same_path(self):
        path=PATHS[0]
        self.assertEqual(links(path,'[valid](../reverse/generated/re951-audio-provider-checkpoint.json)'),1)
        for bad in ('../reverse/generated/missing-re951.json','../../../../etc/passwd','https://example.com','/etc/passwd'):
            with self.assertRaises(AssertionError): links(path,'[bad]('+bad+')')

if __name__ == '__main__': unittest.main()
