"""Fail-closed named RE811 successor; preserve every historical byte/hash."""
import hashlib
BASELINE='5e9d3337f1c49282520a822d8d9672185fca6ef6d5b681f845307c36c9b12a27'
CANDIDATE='4e4374916bf454fd577fb92d89e7160a1b818e5a744e9244ad89c44fbb0ef84f'
PRECEDING='03f2851e4eb00274cc8d68b26648529a27f4a1e98ac6e255e61a440ca6863418'
TRANSFORMS=[(b'\t\t\tfor (linknum = items[next_item_active].next_active; linknum != -1; linknum = items[linknum].next_active)\n', b'#if defined(__i386__) && PSXPC_TEST && PSX_VERSION && USE_32_BIT_ADDR\n\t\t\tfor (linknum = next_item_active; linknum != -1; linknum = items[linknum].next_active)\n#else\n\t\t\tfor (linknum = items[next_item_active].next_active; linknum != -1; linknum = items[linknum].next_active)\n#endif\n'), (b'\t\t\t\tif (linknum == item_num)\n', b'#if defined(__i386__) && PSXPC_TEST && PSX_VERSION && USE_32_BIT_ADDR\n\t\t\t\tif (items[linknum].next_active == item_num)\n#else\n\t\t\t\tif (linknum == item_num)\n#endif\n')]
def baseline_from_approved_source(b):
 assert hashlib.sha256(b).hexdigest()==CANDIDATE
 for old,new in TRANSFORMS:
  assert b.count(new)==1
  b=b.replace(new,old,1)
 assert hashlib.sha256(b).hexdigest()==BASELINE
 return b
def historical_items(b):
 if hashlib.sha256(b).hexdigest()==BASELINE:return b
 return baseline_from_approved_source(b)
def dashboard_before_re811(b):
 # Only explicitly named RE813: exact suffix digest + inverse baseline.
 start813=b'<!-- start re813-conditional-producer-gap -->';end813=b'<!-- end re813-conditional-producer-gap -->'
 if start813 in b or end813 in b:
     assert b.count(start813)==b.count(end813)==1
     a813=b.index(start813)
     assert hashlib.sha256(b[a813:]).hexdigest()=='1b17a1f1e76b2da1b5546202fd247559fbb52817c3f222895dada65ab652c3f6'
     b=b[:a813]
     assert hashlib.sha256(b).hexdigest()=='dd5ea56cc15c10cbe319154b2def1209b0e54d4ca017294ace0df5242097096d'
 # RE812 only: exclude the uniquely named successor, pin ALL preceding bytes.
 start812=b'<!-- start re812-addactiveitem-characterization -->';end812=b'<!-- end re812-addactiveitem-characterization -->'
 if start812 in b or end812 in b:
  assert b.count(start812)==b.count(end812)==1
  a812=b.index(start812);z812=b.index(end812,a812)+len(end812)
  assert b[z812:]==b'\n'
  b=b[:a812]+b[z812+1:]
  assert hashlib.sha256(b).hexdigest()=='7629485a524ee5cf87041374b6e50acedbbe42b10dd18325b9ff088471b690ac'
 start=b'<!-- start re811-removeactiveitem-integration -->';end=b'<!-- end re811-removeactiveitem-integration -->'
 if start in b or end in b:
  assert b.count(start)==b.count(end)==1
  a=b.index(start);z=b.index(end,a)+len(end)
  b=b[:a]+b[z:]
  assert hashlib.sha256(b).hexdigest()==PRECEDING
 return b
