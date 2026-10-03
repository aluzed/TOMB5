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
 start=b'<!-- start re811-removeactiveitem-integration -->';end=b'<!-- end re811-removeactiveitem-integration -->'
 if start in b or end in b:
  assert b.count(start)==b.count(end)==1
  a=b.index(start);z=b.index(end,a)+len(end)
  b=b[:a]+b[z:]
  assert hashlib.sha256(b).hexdigest()==PRECEDING
 return b
