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
 # RE818 exact approved metadata suffix only; inverse delta preserves old guard.
 start818=b'<!-- start re818-actual-tu-caller-prerequisite -->';end818=b'<!-- end re818-actual-tu-caller-prerequisite -->'
 if start818 in b or end818 in b:
  assert b.count(start818)==b.count(end818)==1
  a818=b.index(start818)
  assert hashlib.sha256(b[a818:]).hexdigest()=='133512b16df78502d62a52334174b04201d864b54165866985b5186b13b4ab8b'
  b=b[:a818]
  assert hashlib.sha256(b).hexdigest()=='ae791f9befe193f0370b68825cfe17d02616cc723661a8eaa07102caa2b75bc6'
 # Explicit RE817 only: exact suffix and entire preceding dashboard pinned.
 start817=b'<!-- start re817-native-initializer-prerequisite -->';end817=b'<!-- end re817-native-initializer-prerequisite -->'
 if start817 in b or end817 in b:
  assert b.count(start817)==b.count(end817)==1
  a817=b.index(start817)
  assert hashlib.sha256(b[a817:]).hexdigest()=='8e6e79b7750bab3ef10b63ddab3a5a2330794ae35f3eb49ad46e9549be5a124a'
  b=b[:a817]
  assert hashlib.sha256(b).hexdigest()=='b100509e34a75f6a8590bcce38b5c9430e818c8661a32858a0a94facf8b4e071'
 # Explicit RE816 only: authenticate exact suffix AND complete RE815 inverse.
 start816=b'<!-- start re816-initializer-composition -->';end816=b'<!-- end re816-initializer-composition -->'
 if start816 in b or end816 in b:
  assert b.count(start816)==b.count(end816)==1
  a816=b.index(start816)
  assert hashlib.sha256(b[a816:]).hexdigest()=='a1496dc4941eabba8228a5d0be95971a1b61e45e7848890999e77c87c7358343'
  b=b[:a816]
  assert hashlib.sha256(b).hexdigest()=='a714b8ad5482e776c416b785919efba2a1d99bad56045e4f48d7c986c21cd427'
 # Explicit RE815 only: exact suffix digest and inverse whole RE814 dashboard.
 start815=b'<!-- start re815-natural-registration -->';end815=b'<!-- end re815-natural-registration -->'
 if start815 in b or end815 in b:
  assert b.count(start815)==b.count(end815)==1
  a815=b.index(start815)
  assert hashlib.sha256(b[a815:]).hexdigest()=='d826a4249ebcb42fe75dddc1aec5fe5c98e2d1b4f72f1fc998cbcb7d0626d3fe'
  b=b[:a815]
  assert hashlib.sha256(b).hexdigest()=='7e48382152c975f8e876cb2f6ed573a797707013c6be8184846d623ed25614bf'
 # RE814 only: exact named suffix + inverse whole predecessor digest.
 start814=b'<!-- start re814-bounded-continuation -->';end814=b'<!-- end re814-bounded-continuation -->'
 if start814 in b or end814 in b:
  assert b.count(start814)==b.count(end814)==1
  a814=b.index(start814)
  assert hashlib.sha256(b[a814:]).hexdigest()=='6f173a0ece3975d02b65e2a6b60ede0d85c6a7652874be7137a5b86d535c21ef'
  b=b[:a814]
  assert hashlib.sha256(b).hexdigest()=='5c7b6d809cf6ffc00890ed0de5ee9744bc62579e10a742c67c218a13e943b081'
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
