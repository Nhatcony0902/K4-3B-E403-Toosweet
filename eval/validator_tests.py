"""Deterministic checks for validator gates required by CP3."""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from codebase.ai_tutor import KNOWLEDGE_BASE, validate  # noqa: E402

SEGMENT = KNOWLEDGE_BASE[4]
HIT = [{"segment": SEGMENT, "score": 3}]

CASES = [
    (
        "valid_grounded",
        {"status": "GROUNDED", "reason_code": "", "claims": [{"text": "Embedding là vector.", "citation_ids": ["c1"]}], "citations": [{"id": "c1", "lesson_id": SEGMENT.lesson_id, "segment_id": SEGMENT.segment_id, "quote": SEGMENT.quote}]},
        0,
        False,
    ),
    (
        "fake_citation_segment",
        {"status": "GROUNDED", "claims": [{"text": "Có căn cứ.", "citation_ids": ["c1"]}], "citations": [{"id": "c1", "lesson_id": SEGMENT.lesson_id, "segment_id": "S99P9", "quote": SEGMENT.quote}]},
        0,
        True,
    ),
    (
        "claim_without_citation",
        {"status": "GROUNDED", "claims": [{"text": "Ý ngoài nguồn.", "citation_ids": []}], "citations": []},
        0,
        True,
    ),
    (
        "second_clarify_blocked",
        {"status": "CLARIFY", "claims": [], "citations": [], "clarification_question": "Bạn muốn hỏi phần nào?"},
        1,
        True,
    ),
    (
        "no_source_has_draft",
        {"status": "NO_SOURCE", "claims": [{"text": "bịa", "citation_ids": []}], "citations": []},
        0,
        True,
    ),
]


def main():
    rows = []
    for name, candidate, clarify_count, should_fail in CASES:
        result, errors = validate(candidate, HIT, clarify_count)
        passed = bool(errors) == should_fail
        rows.append({"case": name, "passed": passed, "validator_status": result["status"], "reason": result["reason_code"], "errors": errors})
    report = {"total": len(rows), "passed": sum(r["passed"] for r in rows), "failed": sum(not r["passed"] for r in rows), "rows": rows}
    (ROOT / "eval" / "validator_results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
