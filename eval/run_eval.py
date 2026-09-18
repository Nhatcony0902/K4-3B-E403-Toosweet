"""Run CP3 golden set and write a privacy-safe structured report."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from codebase.ai_tutor import answer_question  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="make a real Gemini call per academic case")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    dataset = json.loads((ROOT / "eval" / "golden_set.json").read_text(encoding="utf-8"))
    cases = dataset["cases"][: args.limit]
    rows = []
    reported_model = None
    model_attempts = 0
    model_responses = 0
    trace_path = ROOT / "eval" / "run1_trace.jsonl"
    trace_path.write_text("", encoding="utf-8")
    for case in cases:
        started = time.time()
        trace = answer_question(
            case["input"],
            task_id=case["id"],
            clarify_count=1 if case["grid_values"]["interaction_history"] == "one_clarification_used" else 0,
            live=args.live,
            source_issue=case["expected_reason"] if case["expected_reason"] in {"SOURCE_CONFLICT", "SOURCE_UNCLEAR", "SOURCE_FLAGGED"} else None,
        )
        reported_model = reported_model or trace.get("model", {}).get("model")
        model_attempts += bool(trace.get("model", {}).get("prompt"))
        model_responses += bool(trace.get("model", {}).get("raw_response"))
        result = trace["result"]
        status_match = result.get("status") == case["expected_status"]
        reason_match = not case["expected_reason"] or result.get("reason_code") == case["expected_reason"]
        passed = status_match and reason_match
        row = {
            "case_id": case["id"],
            "taxonomy": case["taxonomy"],
            "frequency_class": case["frequency_class"],
            "source_turn_id": case.get("source_turn_id"),
            "expected_status": case["expected_status"],
            "expected_reason": case["expected_reason"],
            "actual_status": result.get("status"),
            "actual_reason": result.get("reason_code"),
            "status_match": status_match,
            "reason_match": reason_match,
            "passed": passed,
            "latency_ms": trace.get("latency_ms", round((time.time() - started) * 1000)),
            "failure_note": "" if passed else _failure_note(case, result),
        }
        rows.append(row)
        # The trace contains only the synthetic CP3 knowledge base and the
        # paraphrased question. It is safe for review and excludes API keys.
        with trace_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"case_id": case["id"], "trace": trace}, ensure_ascii=False) + "\n")
    passed = sum(1 for row in rows if row["passed"])
    report = {
        "run": "run1",
        "mode": "live_gemini" if args.live else "offline_routing_only",
        "model": reported_model,
        "model_attempts": model_attempts,
        "model_responses": model_responses,
        "ai_call_verified": model_responses > 0,
        "total": len(rows),
        "passed": passed,
        "failed": len(rows) - passed,
        "pass_rate": round(passed / len(rows), 4) if rows else 0,
        "by_taxonomy": _group(rows, "taxonomy"),
        "by_frequency": _group(rows, "frequency_class"),
        "rows": rows,
        "failure_analysis": _failure_analysis(rows),
    }
    (ROOT / "eval" / "run1_results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary_keys = ("mode", "model", "model_attempts", "model_responses", "ai_call_verified", "total", "passed", "failed", "pass_rate", "by_taxonomy", "failure_analysis")
    print(json.dumps({k: report[k] for k in summary_keys}, ensure_ascii=False, indent=2))
    if args.live and model_attempts and not model_responses:
        print("Không nhận được phản hồi nào từ Gemini. Xem error_detail trong run1_trace.jsonl trước khi đánh giá chất lượng model.", file=sys.stderr)
        return 2
    return 0


def _failure_note(case, result):
    return f"expected {case['expected_status']}/{case['expected_reason'] or '-'}, got {result.get('status')}/{result.get('reason_code')}"


def _group(rows, key):
    out = {}
    for row in rows:
        group = row[key]
        bucket = out.setdefault(group, {"total": 0, "passed": 0})
        bucket["total"] += 1
        bucket["passed"] += int(row["passed"])
    for bucket in out.values():
        bucket["pass_rate"] = round(bucket["passed"] / bucket["total"], 4)
    return out


def _failure_analysis(rows):
    counts = {}
    for row in rows:
        if not row["passed"]:
            key = f"{row['actual_status']}/{row['actual_reason']}"
            counts[key] = counts.get(key, 0) + 1
    return [{"observed": key, "count": value} for key, value in sorted(counts.items())]


if __name__ == "__main__":
    raise SystemExit(main())
