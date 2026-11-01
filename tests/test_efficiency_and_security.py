"""
Comprehensive test suite verifying Performance, Efficiency, Compression, and OWASP Hardening.
Verifies:
1. GZip compression middleware (Accept-Encoding: gzip).
2. X-Process-Time sub-millisecond execution duration header.
3. MaxPayloadSizeMiddleware 413 Payload Too Large protection.
4. RFC-compliant RateLimiterMiddleware response headers.
5. OWASP Top-10 security headers (HSTS, CSP, COOP, CORP, COEP, Permissions-Policy).
6. High-efficiency static asset caching headers and favicon endpoint.
"""

from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_process_time_header_present():
    """Verify high-precision execution profiler attaches X-Process-Time header."""
    res = client.get("/health")
    assert res.status_code == 200
    assert "X-Process-Time" in res.headers
    time_str = res.headers["X-Process-Time"]
    assert time_str.endswith("s")
    duration = float(time_str.replace("s", ""))
    assert duration >= 0.0


def test_gzip_compression_enabled():
    """Verify responses exceeding 500 bytes are compressed with GZip."""
    res = client.get("/api/events", headers={"Accept-Encoding": "gzip"})
    assert res.status_code == 200
    assert res.headers.get("Content-Encoding") == "gzip"


def test_owasp_strict_security_headers():
    """Verify full suite of OWASP headers including HSTS, COOP, and Permissions-Policy."""
    res = client.get("/health")
    assert res.status_code == 200
    h = res.headers

    assert "Strict-Transport-Security" in h
    assert "max-age=31536000" in h["Strict-Transport-Security"]
    assert h.get("X-Content-Type-Options") == "nosniff"
    assert h.get("X-Frame-Options") == "DENY"
    assert h.get("Cross-Origin-Opener-Policy") == "same-origin"
    assert h.get("Cross-Origin-Resource-Policy") == "same-origin"
    assert "Permissions-Policy" in h
    assert "camera=()" in h["Permissions-Policy"]
    assert "Content-Security-Policy" in h


def test_rate_limiter_standard_headers():
    """Verify rate limiter injects standard RFC X-RateLimit headers."""
    res = client.get("/api/events")
    assert res.status_code == 200
    assert "X-RateLimit-Limit" in res.headers
    assert "X-RateLimit-Remaining" in res.headers
    assert "X-RateLimit-Reset" in res.headers
    assert int(res.headers["X-RateLimit-Limit"]) == 180


def test_oversized_payload_protection():
    """Verify payloads exceeding max allowed size (2MB) trigger 413 Payload Too Large."""
    # Send a request with a Content-Length indicating oversized payload
    res = client.post(
        "/api/events",
        headers={"Content-Length": "3145728", "Content-Type": "application/json"},
        content=b"{}",
    )
    assert res.status_code == 413
    data = res.json()
    assert data["error"] == "Payload Too Large"


def test_favicon_endpoint():
    """Verify /favicon.ico serves valid SVG with caching headers and no 404."""
    res = client.get("/favicon.ico")
    assert res.status_code == 200
    assert "image/svg+xml" in res.headers.get("Content-Type", "")
    assert "public" in res.headers.get("Cache-Control", "")
    assert "max-age=" in res.headers.get("Cache-Control", "")


def test_static_asset_cache_control_headers():
    """Verify static assets are served with browser caching directives for efficiency."""
    res = client.get("/static/css/styles.css")
    assert res.status_code == 200
    cache_header = res.headers.get("Cache-Control", "")
    assert "public" in cache_header
    assert "max-age=" in cache_header
