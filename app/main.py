import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

APP_NAME = os.getenv("APP_NAME", "alerts")
APP_PORT = int(os.getenv("APP_PORT", "8087"))
APP_VERSION = os.getenv("APP_VERSION", "v2")
MESSAGE = os.getenv("MESSAGE", "Alerts service v1")


def build_status_payload() -> dict:
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "message": MESSAGE,
        "variant": 7,
        "status": "ok",
    }


class AlertsHandler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self._send_json(200, {"status": "alive"})
        elif self.path == "/readyz":
            self._send_json(200, {"status": "ready"})
        elif self.path == "/":
            self._send_json(200, build_status_payload())
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, format: str, *args) -> None:
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", APP_PORT), AlertsHandler)
    print(f"Starting {APP_NAME} ({APP_VERSION}) on port {APP_PORT}")
    server.serve_forever()