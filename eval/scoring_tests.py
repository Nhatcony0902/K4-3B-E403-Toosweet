"""Guard against counting a failed AI request as a successful NO_SOURCE answer."""

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from eval.run_eval import score_case  # noqa: E402


class ScoreCaseTests(unittest.TestCase):
    def setUp(self):
        self.case = {
            "id": "G04",
            "taxonomy": "01_source_truth",
            "frequency_class": "common",
            "expected_status": "NO_SOURCE",
            "expected_reason": "",
        }

    def test_api_failure_cannot_pass_by_matching_no_source(self):
        trace = {
            "model": {"request_attempted": True, "raw_response": None},
            "result": {"status": "NO_SOURCE", "reason_code": "PROCESSING_ERROR"},
        }
        row = score_case(self.case, trace)
        self.assertTrue(row["status_match"])
        self.assertTrue(row["reason_match"])
        self.assertTrue(row["infrastructure_error"])
        self.assertFalse(row["passed"])

    def test_valid_no_source_still_passes(self):
        trace = {
            "model": {"request_attempted": True, "raw_response": '{"status":"NO_SOURCE"}'},
            "result": {"status": "NO_SOURCE", "reason_code": "INSUFFICIENT_CONTENT"},
        }
        row = score_case(self.case, trace)
        self.assertFalse(row["infrastructure_error"])
        self.assertTrue(row["passed"])

    def test_missing_response_fails_even_if_reason_changes(self):
        trace = {
            "model": {"request_attempted": True, "raw_response": None},
            "result": {"status": "NO_SOURCE", "reason_code": "INSUFFICIENT_CONTENT"},
        }
        self.assertFalse(score_case(self.case, trace)["passed"])


if __name__ == "__main__":
    unittest.main()
