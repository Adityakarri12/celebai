"""
FastAPI application entry point for CelebraTech AI Event Planner.
Integrates performance gzip compression, OWASP security, rate limiting,
static asset caching, API routers, and health monitoring.
"""

import mimetypes
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, JSONResponse

from app.config import settings
from app.api.middleware import (
    SecurityHeadersMiddleware,
    RateLimiterMiddleware,
    MaxPayloadSizeMiddleware,
    ProcessTimeMiddleware,
)
from app.api.routes_events import router as events_router
from app.api.routes_ai import router as ai_router

# Ensure browser receives proper JavaScript MIME types for JSX & JS
mimetypes.add_type("application/javascript", ".jsx")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "Enterprise-grade celebration & event planning assistant. "
        "Provides GenAI recommendations, budget tracking, milestone timelines, "
        "vendor checklists, guest seating, dietary rosters, and interactive 3D idea cards "
        "for weddings, birthdays, and community events."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# 1. Performance Profiling (outermost to capture total lifecycle)
app.add_middleware(ProcessTimeMiddleware)

# 2. GZip Response Compression (slashes network transfer sizes by up to 80%)
app.add_middleware(GZipMiddleware, minimum_size=500)

# 3. Payload Size Guardrail (rejects requests > 2MB to prevent memory exhaustion)
app.add_middleware(MaxPayloadSizeMiddleware, max_bytes=2 * 1024 * 1024)

# 4. OWASP Top-10 Security Headers
app.add_middleware(SecurityHeadersMiddleware)

# 5. RFC-Compliant Rate Limiting (180 requests/minute per client IP)
app.add_middleware(RateLimiterMiddleware, max_requests=180, window_seconds=60)

# 6. Cross-Origin Resource Sharing (CORS)
if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

# Include Modular API Routers
app.include_router(events_router)
app.include_router(ai_router)


# Performance-Optimized Static Files Handler with HTTP Cache-Control Headers
class CachedStaticFiles(StaticFiles):
    """StaticFiles handler with aggressive browser caching headers for performance."""

    def file_response(self, *args, **kwargs) -> Response:
        response = super().file_response(*args, **kwargs)
        # 1-day browser cache with stale-while-revalidate for instant subsequent loads
        response.headers["Cache-Control"] = "public, max-age=86400, stale-while-revalidate=3600"
        return response


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", CachedStaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_index() -> FileResponse:
    """Serve the single-page application with caching headers."""
    index_path = STATIC_DIR / "index.html"
    response = FileResponse(str(index_path))
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    return response


@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon() -> Response:
    """Serve an inline festive SVG favicon to prevent 404 network overhead."""
    svg_icon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<text y=".9em" font-size="90">🎪</text>'
        '</svg>'
    )
    return Response(
        content=svg_icon,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=604800, immutable"},
    )


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for liveness, monitoring, and AI provider status.

    Returns:
        JSON status object confirming service health and active GenAI provider.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "genai_provider": "Gemini API" if settings.gemini_api_key else "Offline Curated Engine",
        "efficiency": "gzip-compressed",
        "security": "owasp-hardened",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global sanitized exception handler to prevent leaking internal stack traces.

    Args:
        request: Failed HTTP request.
        exc: Raised exception.

    Returns:
        Structured 500 error response.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred while processing the event planning request.",
        },
    )
