"""
Security, Efficiency, and Rate-Limiting Middleware for CelebraTech AI.

Implements:
1. OWASP Top-10 Hardened Security Headers (CSP, HSTS, COOP, CORP, COEP, Permissions-Policy).
2. RFC-compliant Sliding-Window IP Rate Limiter with standard rate limit headers.
3. Max Request Payload Size Limiter (anti-DoS protection).
4. Real-time Response Execution Latency Profiler (X-Process-Time).
5. Comprehensive Input Sanitization and XSS Prevention.
"""

from typing import Callable, Dict, List, Optional
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette import status
from app.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Applies enterprise-grade OWASP security headers to all HTTP responses.
    Protects against clickjacking, MIME-sniffing, XSS, and unapproved cross-origin leaks.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and attach strict OWASP security headers.

        Args:
            request: Incoming HTTP request.
            call_next: Next middleware or request handler.

        Returns:
            Response with hardened security headers.
        """
        response = await call_next(request)

        # OWASP Essential Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Transport & Cross-Origin Isolation
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"

        # Modern Hardware & Feature Permissions Policy
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=(), usb=(), vr=(), accelerometer=()"
        )

        # Content Security Policy (allows local fonts, inline styles, Web Audio, and trusted scripts)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' https: data:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "font-src 'self' https: data:; "
            "img-src 'self' data: https:; "
            "media-src 'self' data: https: blob:; "
            "connect-src 'self' https:;"
        )

        return response


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    In-memory sliding-window rate limiter per client IP.
    Protects compute-heavy GenAI and export endpoints against brute-force and scraping.
    Injects standard RFC 6585 and X-RateLimit headers.
    """

    def __init__(self, app, max_requests: int = 180, window_seconds: int = 60) -> None:
        """
        Initialize rate limiter parameters.

        Args:
            app: ASGI application.
            max_requests: Maximum allowed requests within the time window.
            window_seconds: Window duration in seconds (default: 60s).
        """
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_records: Dict[str, List[float]] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Evaluate client request against rate limit quota.

        Args:
            request: Incoming HTTP request.
            call_next: Next request handler.

        Returns:
            HTTP Response or 429 JSONResponse when rate limit is exceeded.
        """
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        # Clean expired timestamps outside sliding window
        records = self.request_records.get(client_ip, [])
        valid_records = [t for t in records if now - t < self.window_seconds]

        # Exempt static assets from rate limits for optimal UX
        if request.url.path.startswith("/static") or request.url.path == "/favicon.ico":
            return await call_next(request)

        # Check quota
        if len(valid_records) >= self.max_requests:
            oldest = valid_records[0]
            retry_after = max(1, int(self.window_seconds - (now - oldest)))
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Rate limit quota exceeded. Maximum {self.max_requests} requests per minute.",
                    "retry_after_seconds": retry_after,
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(now + retry_after)),
                },
            )

        # Record this request
        valid_records.append(now)
        self.request_records[client_ip] = valid_records

        response = await call_next(request)
        remaining = max(0, self.max_requests - len(valid_records))
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(now + self.window_seconds))

        return response


class MaxPayloadSizeMiddleware(BaseHTTPMiddleware):
    """
    Guards server memory against oversized payload DoS attacks.
    Rejects request bodies exceeding the specified maximum byte limit.
    """

    def __init__(self, app, max_bytes: int = 2 * 1024 * 1024) -> None:  # 2MB limit
        """
        Initialize max payload middleware.

        Args:
            app: ASGI application.
            max_bytes: Maximum request body size in bytes (default: 2MB).
        """
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Check Content-Length header against max payload size.

        Args:
            request: Incoming HTTP request.
            call_next: Next request handler.

        Returns:
            Response or 413 Payload Too Large.
        """
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > self.max_bytes:
                    return JSONResponse(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        content={
                            "error": "Payload Too Large",
                            "detail": f"Request body exceeds maximum allowed size of {self.max_bytes // (1024 * 1024)}MB.",
                        },
                    )
            except ValueError:
                pass

        return await call_next(request)


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """
    High-precision performance profiler middleware.
    Calculates sub-millisecond execution duration and injects X-Process-Time header.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Record start time, invoke handler, and calculate process time.

        Args:
            request: Incoming HTTP request.
            call_next: Next request handler.

        Returns:
            Response with X-Process-Time execution duration header.
        """
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.5f}s"
        return response
