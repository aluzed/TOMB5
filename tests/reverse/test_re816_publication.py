"""RE816 portable metadata TDD; private proof not required by tests."""
import csv, hashlib, io, re, runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
SECTION='<!-- start re816-initializer-composition --><section id="re816"><h2>RE-816 — CONDITIONAL_INITIALIZER_COMPOSITION_PASS_NATIVE_REQUIREMENT_RED</h2><p>Revue privée indépendante PASS_scoped : préfixe registration naturel 601 visites, dispatch conditionnel externe sur même CPU/RAM, initializer et caller retournent, 1147 visites. Allocation réelle 92 octets, copy4, GetDoor5, shut4, navigation et ItemNewRoom exécutés. Oracle indépendant sélectionné 2992 octets, 2992 corruptions rejetées; ledger immuable 35 événements.</p><p>SETUP/ITEMS natifs réels normal/strict : requirement RED exit1, characterization PASS exit0. DOOR compilé puis dead-stripped, initializer natif absent. Checker cell9 non discriminant, aucune équivalence floor-mutation. Pas retour ObjectObjects/startup, wholeRAM, hardware, activation, production ou intégration. RE815 historique pending conservé; RE816 privé désormais approuvé scoped, publication union RE815+RE816 pending revue finale séparée. BLOCKED-003/004/006 restent; RE817 privé concurrent non approuvé, aucun résultat revendiqué. <a href="../stories/RE-816-initializer-composition.md">Story</a> · <a href="functions/re816-initializer-composition.md">Contrat</a> · <a href="generated/re816-initializer-composition.csv">CSV</a>.</p></section><!-- end re816-initializer-composition -->\n'
PRECEDING='a714b8ad5482e776c416b785919efba2a1d99bad56045e4f48d7c986c21cd427'
NAMES=['re811_provenance','re812_publication','re813_publication','re814_publication','re815_publication']
def api():
 p=R/'scripts/reverse/re816_publication.py'
 assert p.exists(), 'RED: safe RE816 generator absent'
 return runpy.run_path(str(p))
def test_exact_metadata_and_artifacts():
 g=api();d=g['metadata']();g['validate'](d)
 assert d['private_verdict_sha256']=='808046ae20f2f7df911cebdedbceb00fdbf34e44f311eee8a6c50cfe24957014'
 assert d['private_manifest_sha256']=='6115bc3346b89bb941bd4ddb804fba82587f60a90f0dfc8357f5a130d4945563'
 assert d['status']=='CONDITIONAL_INITIALIZER_COMPOSITION_PASS_NATIVE_REQUIREMENT_RED' and d['private_review']=='PASS_scoped'
 assert [d[k] for k in ['manifest_entries','prefix_visits','caller_visits','selected_bytes','corruptions_rejected','immutable_events','allocation_bytes','copy_calls','getdoor_calls','shut_calls','native_requirement_exit','strict_requirement_exit','native_characterization_exit','strict_characterization_exit']]==[49,601,1147,2992,2992,35,92,4,5,4,1,1,0,0]
 for k in ['same_cpu_ram','initializer_target_return','caller_target_return','native_runtime_stderr_empty']:assert d[k] is True
 for k in ['source_patch','integration_approved','publication_review_approved','production_ready','global_green','startup_proven','objectobjects_full_return','native_initializer_invoked','controller_invoked','whole_ram_oracle','hardware_proven','activation_approved','floor_mutation_equivalent','re817_approved']:assert d[k] is False
 assert d['dispatch']=='conditional external A0 RA; retained prefix SP' and d['native_door']=='compiled then dead-stripped; initializer absent'
 assert g['SECTION']==SECTION and g['PRECEDING']==PRECEDING
 for p,k in g['OUTPUTS'].items(): assert (R/p).read_text()==g[k]
 assert list(csv.DictReader(io.StringIO(g['CSV_TEXT'])))==[g['csv_row']()]
 assert '- [x]' in g['STORY'] and '- [ ]' in g['STORY']
 for text in [g[k] for k in g['OUTPUTS'].values()]+[SECTION]:assert not re.search(r'0x[0-9a-fA-F]+|(?:FUN|DAT|LAB)_[0-9a-fA-F]{6,}|payload_offset|word_le_hex|data:image|```(?:asm|mips|cpp|c)\b',text)
def test_schema_fail_closed():
 g=api();good=g['metadata']()
 for k,v in good.items():
  bad=dict(good);bad[k]=not v if type(v) is bool else v+1 if type(v) is int else v+'changed'
  with pytest.raises(ValueError):g['validate'](bad)
 for bad in [{**good,'raw_opcode':'forbidden'},{k:v for k,v in good.items() if k!='prefix_visits'},{**good,'prefix_visits':601.0},{**good,'native_requirement_exit':True}]:
  with pytest.raises(ValueError):g['validate'](bad)
def composed():
 b=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 # Only named RE817: verify full exact suffix and preceding RE816 before test composition.
 if b'<!-- start re817-native-initializer-prerequisite -->' in b or b'<!-- end re817-native-initializer-prerequisite -->' in b:
  successor=runpy.run_path(str(R/'scripts/reverse/re817_publication.py'))
  assert successor['PRECEDING']=='b100509e34a75f6a8590bcce38b5c9430e818c8661a32858a0a94facf8b4e071'
  b=successor['dashboard_before_re817'](b)
 if SECTION.encode() not in b:b+=SECTION.encode()
 return b
def mutants(b):
 start=b'<!-- start re816-initializer-composition -->';end=b'<!-- end re816-initializer-composition -->'
 return [b+b'foreign',b+SECTION.encode(),b.replace(end,b'',1),b.replace(start,b'',1),b.replace(start,b'TEMP',1).replace(end,start,1).replace(b'TEMP',end,1),b.replace(b'2992 octets',b'2993 octets',1),b.replace(b'RE-809',b'RE-xxx',1),b+ b'<!-- start re817-unknown -->foreign<!-- end re817-unknown -->']
def test_named_successor_predecessors():
 b=composed()
 for n in NAMES:
  old=runpy.run_path(str(R/('scripts/reverse/'+n+'.py')));fn=old['dashboard_before_'+n[:5]]
  assert hashlib.sha256(fn(b)).hexdigest()==old['PRECEDING']
  for m in mutants(b):
   with pytest.raises(AssertionError):fn(m)
def test_append_only_inverse():
 g=api();b=composed();before=g['dashboard_before_re816'](b)
 assert hashlib.sha256(before).hexdigest()==PRECEDING and b==before+SECTION.encode()
 for m in mutants(b):
  with pytest.raises(AssertionError):g['dashboard_before_re816'](m)
