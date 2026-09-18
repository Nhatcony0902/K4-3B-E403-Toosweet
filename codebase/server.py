"""Small local CP3 server: static prototype UI plus POST /api/ask."""

from __future__ import annotations

import json
import mimetypes
import pathlib
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from ai_tutor import answer_question


ROOT = pathlib.Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "prototype"), **kwargs)

    def do_POST(self):  # noqa: N802 - stdlib handler API
        if self.path != "/api/ask":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(body.get("question", "")).strip()
            if not question:
                raise ValueError("question is required")
            trace = answer_question(
                question,
                task_id=body.get("task_id"),
                clarify_count=int(body.get("clarify_count", 0)),
                live=True,
            )
            payload = trace["result"] | {"task_id": trace["task_id"], "trace": trace}
            self._json(200, payload)
        except Exception as exc:  # keep API errors JSON for the UI
            self._json(400, {"status": "NO_SOURCE", "reason_code": "PROCESSING_ERROR", "message": str(exc)[:300]})

    def _json(self, status: int, payload: dict):
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"CP3 tutor: http://127.0.0.1:{port}/?ai=1")
    print("Dừng bằng Ctrl+C")
    server.serve_forever()


if __name__ == "__main__":
    main()
