from pathlib import Path

from scripts.reverse.re427_ghidra_second_window_rank_28_narrow_export import build, write


def test_re427_exports_rank_28_without_raw_symbolic_artifacts(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    result = build(repo)

    assert result['selected_candidate_id'] == '61b63f61c1fd'
    assert result['selected_rank'] == '28'
    assert result['source_symbol_context_count'] == '10'
    assert result['safe_context_status'] == 'filtered-raw-symbolic-artifact'
    assert result['next_ticket'] == 'RE-428'

    outputs = write(result, tmp_path)
    forbidden = ('0x', 'fun_', 'sub_', 'word_le_hex', 'payload_offset', 'opcode')
    assert outputs
    assert all(not any(token in path.read_text(encoding='utf-8').lower() for token in forbidden) for path in outputs)
