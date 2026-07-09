from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import parse_qs, urlparse

from .service import AuthError, SuperkateSyncService, failure
from .validation import ValidationError


class SuperkateRequestHandler(BaseHTTPRequestHandler):
    service = SuperkateSyncService()

    def do_GET(self) -> None:  # noqa: N802 - stdlib API
        parsed = urlparse(self.path)
        if parsed.path == "/api/superkate/health":
            self._json(self.service.health())
            return
        if parsed.path == "/api/superkate/sync/bootstrap":
            self._with_errors(lambda: self.service.bootstrap(authorization=self.headers.get("Authorization")))
            return
        if parsed.path == "/api/superkate/sync/pull":
            params = parse_qs(parsed.query)
            business_slug = params.get("businessSlug", [""])[0]
            after_version = int(params.get("afterVersion", ["0"])[0])
            self._with_errors(
                lambda: self.service.pull(
                    business_slug=business_slug,
                    after_version=after_version,
                    authorization=self.headers.get("Authorization"),
                )
            )
            return
        self._json(failure("NOT_FOUND", "Route not found."), status=404)

    def do_POST(self) -> None:  # noqa: N802 - stdlib API
        parsed = urlparse(self.path)
        if parsed.path == "/api/superkate/sync/push":
            payload = self._read_json()
            self._with_errors(lambda: self.service.push(payload, authorization=self.headers.get("Authorization")))
            return
        if parsed.path == "/api/superkate/sync/reset-test-data":
            self._with_errors(lambda: self.service.reset_test_data(authorization=self.headers.get("Authorization")))
            return
        self._json(failure("NOT_FOUND", "Route not found."), status=404)

    def _with_errors(self, callback) -> None:
        try:
            self._json(callback())
        except AuthError as exc:
            self._json(failure("UNAUTHORIZED", str(exc)), status=401)
        except ValidationError as exc:
            self._json(failure("VALIDATION_ERROR", exc.message, {exc.field or "request": exc.message}), status=400)
        except ValueError:
            self._json(failure("BAD_REQUEST", "Request could not be parsed."), status=400)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _json(self, payload: dict, *, status: int = 200) -> None:
        encoded = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args) -> None:
        # Keep local scaffold logs from dumping request payloads or customer data.
        return


def run(host: str = "127.0.0.1", port: int = 8787) -> None:
    server = ThreadingHTTPServer((host, port), SuperkateRequestHandler)
    print(f"Hair by Superkate local backend listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
