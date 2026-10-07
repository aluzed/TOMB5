from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[2]
def test_re859_story_and_append_only_dashboard():
 story=(R/'docs/stories/RE-859-mrotx-defined-bit32.md').read_text()
 assert 'RE858 global FAIL' in story and 'mRotZ' in story
 assert 'ELF64' in story and 'fpermissive' in story and '72' in story
 data=(R/'docs/reverse/reconstruction-progress.html').read_bytes()
 begin=b'<!-- start re859-mrotx-defined-bit32 -->';end=b'<!-- end re859-mrotx-defined-bit32 -->'
 assert data.count(begin)==data.count(end)==1
 first=data.index(begin);last=data.index(end)+len(end)
 historical=data[:first]+data[last:]
 assert hashlib.sha256(historical).hexdigest()=="0af3e5af6447f96207c619493f6c7c47139c18bac550e4567ccc631eaa7bd61f"
 assert b'RE-859' in data[first:last]
