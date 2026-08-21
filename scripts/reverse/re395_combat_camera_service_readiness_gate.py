#!/usr/bin/env python3
"""Gate the RE-394 combat/camera candidate without reopening a proof domain."""
from __future__ import annotations
import argparse
import csv
from dataclasses import asdict, dataclass, fields
from pathlib import Path

RE394_HANDOFF = "docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-handoff.csv"
RE394_CANDIDATES = "docs/reverse/generated/re394-lara-combat-camera-post-lara-control-next-subcluster-selection-candidates.csv"
CANDIDATES_CSV = "docs/reverse/generated/re395-combat-camera-service-readiness-gate-candidates.csv"
GATES_CSV = "docs/reverse/generated/re395-combat-camera-service-readiness-gate-gates.csv"
SUMMARY_CSV = "docs/reverse/generated/re395-combat-camera-service-readiness-gate-summary.csv"
HANDOFF_CSV = "docs/reverse/generated/re395-combat-camera-service-readiness-gate-handoff.csv"
MD_OUTPUT = "docs/reverse/functions/re395-combat-camera-service-readiness-gate.md"
STORY = "docs/stories/RE-395-combat-camera-service-readiness-gate.md"
SELECTED_SUBCLUSTER = "combat-camera-service"
FOLLOWUP_CANDIDATE_ID = "0aaa76206517"
NEXT_TICKET = "RE-396"
NEXT_TOPIC = "combat-camera-service-candidate-proof-export"
COMBAT_CAMERA_TOKENS = ("Camera", "BodyPart", "Missile", "Detection")
FORBIDDEN_OUTPUT_FRAGMENTS = ("0x", "fun_", "word_le_hex", "payload_offset", "dump row", "opcode", "machine word", "call_address", "branch target", "call target", "hex-address-fragment", "raw_evidence", "source_line_text", "ghidra_entry", "ghidra_name", "unimplemented();")

@dataclass(frozen=True)
class CandidateRow:
    rank:int; source_rank:int; candidate_id:str; selected_narrow_subcluster:str; bridge_class:str; body_size_bucket:str; mapped_caller_count:int; mapped_callee_count:int; source_context_count:int; combat_camera_context_count:int; proof_signal_class:str; candidate_level_proof:str; readiness_gate:str; ready_to_reopen_domain:str; source_patch_authorized:str; next_probe:str; stop_condition:str
@dataclass(frozen=True)
class GateRow:
    rank:int; gate_class:str; candidate_count:int; representative_candidates:str; candidate_level_proof_count:int; gate_decision:str; ready_to_reopen_domain:str; source_patch_authorized:str; next_ticket:str; next_topic:str; stop_condition:str
@dataclass(frozen=True)
class Summary:
    story_id:str; topic:str; upstream_handoff:str; selected_narrow_subcluster:str; input_candidate_count:int; candidate_gate_count:int; candidate_level_proof_count:int; ready_to_reopen_domain_count:int; source_patch_authorized_count:int; selected_domain:str; selected_pivot:str; selected_followup_candidate_id:str; next_ticket:str; next_topic:str; metadata_work_readiness:str; code_change_readiness:str; stop_condition:str
@dataclass(frozen=True)
class Bundle:
    candidate_rows:list[CandidateRow]; gate_rows:list[GateRow]; summary:Summary

def read_csv(path:Path)->list[dict[str,str]]:
    with path.open(newline="",encoding="utf-8") as handle:return list(csv.DictReader(handle))
def one_row(repo:Path,rel:str)->dict[str,str]:
    rows=read_csv(repo/rel)
    if len(rows)!=1: raise ValueError(f"{rel} must contain exactly one row")
    return rows[0]
def validate_handoff(repo:Path)->None:
    row=one_row(repo,RE394_HANDOFF)
    expected={"story_id":"RE-394","next_ticket":"RE-395","next_topic":"combat-camera-service-readiness-gate","selected_followup_subcluster":SELECTED_SUBCLUSTER,"selected_candidate_count":"1","selected_candidate_ids":FOLLOWUP_CANDIDATE_ID,"ready_to_reopen_domain_count":"0","source_patch_authorized_count":"0","selected_domain":"none","selected_pivot":"none","metadata_work_readiness":"ready","code_change_readiness":"blocked"}
    for key,value in expected.items():
        if row.get(key)!=value: raise ValueError(f"RE-394 handoff drift: {key}={row.get(key)!r}")
def count_context(value:str)->int:
    return sum(any(token.lower() in symbol.lower() for token in COMBAT_CAMERA_TOKENS) for symbol in value.split(";") if symbol)
def require_metadata_only(text:str)->None:
    lowered=text.lower()
    for fragment in FORBIDDEN_OUTPUT_FRAGMENTS:
        if fragment in lowered: raise ValueError(f"Forbidden raw-evidence fragment: {fragment}")
def build_combat_camera_service_readiness_gate(repo:Path)->Bundle:
    repo=Path(repo); validate_handoff(repo)
    source=read_csv(repo/RE394_CANDIDATES)
    if [row.get("candidate_id") for row in source] != [FOLLOWUP_CANDIDATE_ID]: raise ValueError("RE-394 candidate set drift")
    row=source[0]
    expected={"narrow_subcluster":SELECTED_SUBCLUSTER,"readiness_gate":"blocked-needs-candidate-level-proof","ready_to_reopen_domain":"no","source_patch_authorized":"no","next_probe":"readiness-gate"}
    for key,value in expected.items():
        if row.get(key)!=value: raise ValueError(f"RE-394 candidate drift: {key}={row.get(key)!r}")
    context_count=count_context(row["representative_source_context"])
    if context_count != 6: raise ValueError(f"combat/camera context drift: {context_count}")
    candidates=[CandidateRow(1,int(row["source_rank"]),row["candidate_id"],SELECTED_SUBCLUSTER,row["bridge_class"],row["body_size_bucket"],int(row["mapped_caller_count"]),int(row["mapped_callee_count"]),int(row["source_context_count"]),context_count,"caller-combat-camera-context-only","no","blocked-no-candidate-level-proof","no","no","candidate-proof-export","candidate-level source-symbolic proof is required before proof-domain selection")]
    gates=[GateRow(1,"candidate-level-source-symbolic-proof-missing",1,FOLLOWUP_CANDIDATE_ID,0,"request-still-narrower-export","no","no",NEXT_TICKET,NEXT_TOPIC,"candidate-level source-symbolic proof is required before proof-domain selection")]
    summary=Summary("RE-395","combat-camera-service-readiness-gate","RE-394",SELECTED_SUBCLUSTER,1,1,0,0,0,"none","none",FOLLOWUP_CANDIDATE_ID,NEXT_TICKET,NEXT_TOPIC,"ready","blocked","combat/camera candidate lacks candidate-level proof; export still narrower proof context before proof-domain selection")
    return Bundle(candidates,gates,summary)
def write_csv(path:Path,rows:list[object],row_type:type[object])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=[field.name for field in fields(row_type)],lineterminator="\n"); writer.writeheader()
        for row in rows: writer.writerow(asdict(row))
def render_md(bundle:Bundle)->str:
    s=bundle.summary
    text=f"""# RE-395 combat camera service readiness gate

## Purpose

Gate the RE-394 `{s.selected_narrow_subcluster}` candidate before any proof-domain or source-patch decision.

## Decision

No proof-domain is reopened. The candidate has combat/camera source-symbolic context only and no candidate-level proof.

## Handoff

- Selected follow-up candidate: `{s.selected_followup_candidate_id}`
- Next ticket: `{s.next_ticket}`
- Next topic: `{s.next_topic}`
- Code readiness: `{s.code_change_readiness}`
"""; require_metadata_only(text); return text
def render_story(bundle:Bundle)->str:
    s=bundle.summary
    text=f"""# RE-395 combat camera service readiness gate

## Goal

Gate the RE-394 combat-camera-service candidate and decide whether it can reopen proof-domain selection or authorize a source patch.

## Inputs

- Upstream handoff: `{RE394_HANDOFF}`
- Candidate rows: `{RE394_CANDIDATES}`

## Progress tracker

- [x] RE-394 combat-camera handoff validated.
- [x] Selected candidate checked for drift.
- [x] Candidate-level proof requirement evaluated.
- [x] Domain/source-patch authorization denied.
- [x] Still-narrower proof export handoff emitted.

## Generated artifacts

- `{CANDIDATES_CSV}`
- `{GATES_CSV}`
- `{SUMMARY_CSV}`
- `{HANDOFF_CSV}`
- `{MD_OUTPUT}`

## Readiness decision

The `{s.selected_narrow_subcluster}` candidate remains source-symbolic. Domain and pivot stay `{s.selected_domain}` / `{s.selected_pivot}`, and code readiness remains `{s.code_change_readiness}`.

## Follow-up ticket breakdown

- `{s.next_ticket}` / `{s.next_topic}`: export still-narrower candidate proof context for `{s.selected_followup_candidate_id}`.
  - Stop condition: without candidate-level proof, source/code readiness stays blocked.

## Validation commands

- `python -m pytest tests/reverse/test_re395_combat_camera_service_readiness_gate.py -q`
- `python scripts/reverse/re395_combat_camera_service_readiness_gate.py --repo .`
- `python -m pytest tests/reverse -q`
"""; require_metadata_only(text); return text
def write_all_artifacts(bundle:Bundle,repo:Path)->dict[str,Path]:
    repo=Path(repo); outputs={"candidates_csv":repo/CANDIDATES_CSV,"gates_csv":repo/GATES_CSV,"summary_csv":repo/SUMMARY_CSV,"handoff_csv":repo/HANDOFF_CSV,"md":repo/MD_OUTPUT,"story":repo/STORY}
    write_csv(outputs["candidates_csv"],bundle.candidate_rows,CandidateRow); write_csv(outputs["gates_csv"],bundle.gate_rows,GateRow); write_csv(outputs["summary_csv"],[bundle.summary],Summary); write_csv(outputs["handoff_csv"],[bundle.summary],Summary)
    outputs["md"].parent.mkdir(parents=True,exist_ok=True); outputs["md"].write_text(render_md(bundle),encoding="utf-8")
    outputs["story"].parent.mkdir(parents=True,exist_ok=True); outputs["story"].write_text(render_story(bundle),encoding="utf-8")
    for path in outputs.values(): require_metadata_only(path.read_text(encoding="utf-8"))
    return outputs
def main()->None:
    parser=argparse.ArgumentParser(); parser.add_argument("--repo",default=".",type=Path); args=parser.parse_args(); repo=args.repo.resolve()
    for key,path in write_all_artifacts(build_combat_camera_service_readiness_gate(repo),repo).items(): print(f"{key}: {path.relative_to(repo)}")
if __name__=="__main__": main()
