"""Check the OpenRouter request contract without using a real API key."""

import io
import json
import os
import pathlib
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from codebase.ai_tutor import KNOWLEDGE_BASE, answer_question, call_openrouter  # noqa: E402


class OpenRouterTests(unittest.TestCase):
    def test_request_uses_bearer_header_and_chat_completion_shape(self):
        response = {"choices": [{"message": {"content": '{"status":"NO_SOURCE"}'}}]}
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-secret"}, clear=True):
            with patch("codebase.ai_tutor.urlopen", return_value=io.BytesIO(json.dumps(response).encode())) as opener:
                model, raw = call_openrouter("test prompt")
        request = opener.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(model, "google/gemini-3.6-flash")
        self.assertEqual(raw, '{"status":"NO_SOURCE"}')
        self.assertEqual(request.full_url, "https://openrouter.ai/api/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertNotIn("test-secret", request.full_url)
        self.assertEqual(payload["model"], model)
        self.assertEqual(payload["messages"], [{"role": "user", "content": "test prompt"}])
        self.assertEqual(payload["max_completion_tokens"], 2048)
        self.assertEqual(payload["response_format"], {"type": "json_object"})

    def test_http_error_does_not_expose_key(self):
        error = HTTPError(
            "https://openrouter.ai/api/v1/chat/completions",
            401,
            "Unauthorized",
            {},
            io.BytesIO(b"invalid key: test-secret"),
        )
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-secret"}, clear=True):
            with patch("codebase.ai_tutor.urlopen", side_effect=error):
                with self.assertRaisesRegex(RuntimeError, "HTTP 401") as raised:
                    call_openrouter("test prompt")
        self.assertNotIn("test-secret", str(raised.exception))

    def test_answer_still_passes_through_validator_and_trace(self):
        segment = next(item for item in KNOWLEDGE_BASE if item.segment_id == "S3P1")
        candidate = {
            "status": "GROUNDED",
            "reason_code": "",
            "claims": [{"text": "Embedding biểu diễn ý nghĩa đoạn văn bằng vector số.", "citation_ids": ["c1"]}],
            "citations": [{"id": "c1", "lesson_id": segment.lesson_id, "segment_id": segment.segment_id, "quote": segment.quote}],
        }
        with patch("codebase.ai_tutor.call_openrouter", return_value=("google/gemini-3.6-flash", json.dumps(candidate, ensure_ascii=False))):
            trace = answer_question("Embedding là gì?", source_segments=(segment,))
        self.assertEqual(trace["result"]["status"], "GROUNDED")
        self.assertEqual(trace["model"]["provider"], "openrouter")
        self.assertTrue(trace["model"]["request_attempted"])
        self.assertEqual(trace["model"]["model"], "google/gemini-3.6-flash")


if __name__ == "__main__":
    unittest.main()
