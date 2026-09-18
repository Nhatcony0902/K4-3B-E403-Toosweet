"""Run CP3 golden set and write a privacy-safe structured report."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from codebase.ai_tutor import KNOWLEDGE_BASE, Segment, answer_question  # noqa: E402


def _case_sources(case):
    if "source_fixture" in case:
        return tuple(
            Segment(
                lesson_id=source["lesson_id"],
                segment_id=source["segment_id"],
                title=source["title"],
                quote=source["quote"],
                keywords=tuple(source["keywords"]),
                quality=source.get("quality", "OK"),
            )
            for source in case["source_fixture"]
        )
    if "allowed_source_ids" not in case:
        return None
    index = {segment.segment_id: segment for segment in KNOWLEDGE_BASE}
    return tuple(index[segment_id] for segment_id in case["allowed_source_ids"])


def score_case(case, trace):
    """Score the delivered result; an API failure is never a successful answer."""
    result = trace["result"]
    status_match = result.get("status") == case["expected_status"]
    reason_match = not case["expected_reason"] or result.get("reason_code") == case["expected_reason"]
    model = trace.get("model", {})
    infrastructure_error = result.get("reason_code") == "PROCESSING_ERROR" or bool(
        model.get("request_attempted") and not model.get("raw_response")
    )
    passed = status_match and reason_match and not infrastructure_error
    return {
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
        "infrastructure_error": infrastructure_error,
        "passed": passed,
        "latency_ms": trace.get("latency_ms"),
        "failure_note": "" if passed else _failure_note(case, result, infrastructure_error),
    }


def _load_existing_traces(path, cases):
    """Read the saved run without issuing requests or changing its evidence."""
    traces = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        case_id = entry["case_id"]
        if case_id in traces:
            raise ValueError(f"duplicate case in trace: {case_id}")
        traces[case_id] = entry["trace"]
    for case in cases:
        if case["id"] not in traces or traces[case["id"]].get("question") != case["input"]:
            raise ValueError(f"trace is missing or does not match current case: {case['id']}")
    return traces


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="make a real OpenRouter call per academic case")
    parser.add_argument("--rescore", action="store_true", help="recalculate from saved trace; make no API calls")
    parser.add_argument("--run-name", default="run1", help="file stem for this run, such as run2")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.live and args.rescore:
        parser.error("--live and --rescore cannot be combined")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_name):
        parser.error("--run-name may contain only letters, digits, underscores and hyphens")
    dataset = json.loads((ROOT / "eval" / "golden_set.json").read_text(encoding="utf-8"))
    cases = dataset["cases"][: args.limit]
    rows = []
    reported_model = None
    reported_provider = None
    model_attempts = 0
    model_responses = 0
    trace_path = ROOT / "eval" / f"{args.run_name}_trace.jsonl"
    results_path = ROOT / "eval" / f"{args.run_name}_results.json"
    if not args.rescore and (trace_path.exists() or results_path.exists()):
        parser.error(f"{args.run_name} already exists; choose a new --run-name to preserve its trace")
    existing_traces = _load_existing_traces(trace_path, cases) if args.rescore else None
    if not args.rescore:
        trace_path.write_text("", encoding="utf-8")
    for case in cases:
        if existing_traces is None:
            trace = answer_question(
                case["input"],
                task_id=case["id"],
                clarify_count=1 if case["grid_values"]["interaction_history"] == "one_clarification_used" else 0,
                live=args.live,
                source_segments=_case_sources(case),
            )
            # The trace contains only the synthetic CP3 knowledge base and the
            # paraphrased question. It is safe for review and excludes API keys.
            with trace_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"case_id": case["id"], "trace": trace}, ensure_ascii=False) + "\n")
        else:
            trace = existing_traces[case["id"]]
        reported_model = reported_model or trace.get("model", {}).get("model")
        reported_provider = reported_provider or trace.get("model", {}).get("provider")
        model_attempts += bool(trace.get("model", {}).get("request_attempted"))
        model_responses += bool(trace.get("model", {}).get("raw_response"))
        rows.append(score_case(case, trace))
    passed = sum(1 for row in rows if row["passed"])
    mode = "offline_routing_only"
    if model_attempts:
        mode = "live_openrouter" if args.live or reported_provider == "openrouter" else "live_gemini"
    report = {
        "run": args.run_name,
        "dataset_version": dataset["version"],
        "mode": mode,
        "model": reported_model,
        "model_attempts": model_attempts,
        "model_responses": model_responses,
        "ai_call_verified": model_responses > 0,
        "total": len(rows),
        "passed": passed,
        "failed": len(rows) - passed,
        "infrastructure_errors": sum(row["infrastructure_error"] for row in rows),
        "pass_rate": round(passed / len(rows), 4) if rows else 0,
        "by_taxonomy": _group(rows, "taxonomy"),
        "by_frequency": _group(rows, "frequency_class"),
        "rows": rows,
        "failure_analysis": _failure_analysis(rows),
    }
    results_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary_keys = ("mode", "model", "model_attempts", "model_responses", "ai_call_verified", "total", "passed", "failed", "infrastructure_errors", "pass_rate", "by_taxonomy", "failure_analysis")
    print(json.dumps({k: report[k] for k in summary_keys}, ensure_ascii=False, indent=2))
    if args.live and model_attempts and not model_responses:
        print(f"Không nhận được phản hồi nào từ OpenRouter. Xem error_detail trong {trace_path.name} trước khi đánh giá chất lượng model.", file=sys.stderr)
        return 2
    return 0


def _failure_note(case, result, infrastructure_error=False):
    if infrastructure_error:
        return "API/model processing failed; no valid answer was produced"
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
