import logging
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.config.limits import (
    MAX_QUERY_LENGTH,
    PIPELINE_ENABLED,
    MAX_CONCURRENT_REQUESTS,
    RATE_LIMIT_PER_MINUTE,
    DAILY_REQUEST_LIMIT,
)

from app.pipeline.research_pipeline import ResearchPipeline


# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ==========================================
# APPLICATION
# ==========================================

app = FastAPI(
    title="Multi-Agent Research Assistant",
    description=(
        "An AI-powered research assistant using "
        "multi-agent orchestration, web search, "
        "fact-checking, and synthesis."
    ),
    version="1.0.0",
)


# ==========================================
# REQUEST MODEL
# ==========================================

class ResearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=MAX_QUERY_LENGTH,
        description="Research question to investigate.",
    )

    model_config = {
        "extra": "forbid",
    }


# ==========================================
# RESPONSE MODEL
# ==========================================

class ResearchResponse(BaseModel):
    status: str
    query: str
    tasks: list[str]
    final_answer: str
    processing_time_seconds: float


# ==========================================
# PIPELINE INSTANCE
# ==========================================

pipeline = ResearchPipeline()


# ==========================================
# RATE LIMITING
# ==========================================

_request_times: dict[str, deque] = defaultdict(deque)
_daily_requests: dict[tuple[str, str], int] = defaultdict(int)

_rate_limit_lock = threading.Lock()


def check_rate_limit(client_ip: str):
    """
    Simple in-memory rate limiter.

    Development limits:
        - 10 requests per minute per IP
        - 100 requests per UTC day per IP

    For production, replace with Redis-backed
    rate limiting.
    """

    now = time.time()

    minute_cutoff = now - 60

    with _rate_limit_lock:

        timestamps = _request_times[client_ip]

        while (
            timestamps
            and timestamps[0] < minute_cutoff
        ):
            timestamps.popleft()

        if len(timestamps) >= RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Rate limit exceeded. "
                    "Please wait before submitting "
                    "another request."
                ),
                headers={
                    "Retry-After": "60",
                },
            )

        today = datetime.now(
            timezone.utc
        ).date().isoformat()

        daily_key = (client_ip, today)

        if _daily_requests[daily_key] >= DAILY_REQUEST_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Daily request limit reached. "
                    "Please try again tomorrow."
                ),
            )

        timestamps.append(now)
        _daily_requests[daily_key] += 1


# ==========================================
# CONCURRENCY PROTECTION
# ==========================================

_pipeline_semaphore = threading.BoundedSemaphore(
    MAX_CONCURRENT_REQUESTS
)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "message": (
            "Welcome to the Multi-Agent "
            "Research Assistant API!"
        ),
        "docs": "/docs",
        "health": "/health",
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "pipeline_enabled": PIPELINE_ENABLED,
    }


# ==========================================
# RESEARCH ENDPOINT
# ==========================================

@app.post(
    "/research",
    response_model=ResearchResponse,
)
def research(
    request: Request,
    data: ResearchRequest,
):
    """
    Run the complete multi-agent research pipeline.
    """

    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    # ------------------------------------------
    # CHECK PIPELINE STATUS
    # ------------------------------------------

    if not PIPELINE_ENABLED:
        raise HTTPException(
            status_code=503,
            detail=(
                "Research service is temporarily disabled."
            ),
        )

    # ------------------------------------------
    # NORMALIZE QUERY
    # ------------------------------------------

    query = data.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail=(
                "Research query cannot be empty."
            ),
        )

    if len(query) > MAX_QUERY_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Research query is too long. "
                f"Maximum allowed length is "
                f"{MAX_QUERY_LENGTH} characters."
            ),
        )

    # ------------------------------------------
    # RATE LIMIT
    # ------------------------------------------

    check_rate_limit(client_ip)

    # ------------------------------------------
    # CONCURRENCY LIMIT
    # ------------------------------------------

    acquired = _pipeline_semaphore.acquire(
        blocking=False
    )

    if not acquired:
        raise HTTPException(
            status_code=503,
            detail=(
                "The research service is currently busy. "
                "Please try again shortly."
            ),
        )

    start_time = time.time()

    try:

        logger.info(
            "Research request received from %s",
            client_ip,
        )

        # --------------------------------------
        # RUN PIPELINE
        # --------------------------------------

        result = pipeline.run(query)

        elapsed = round(
            time.time() - start_time,
            2,
        )

        logger.info(
            "Research completed in %s seconds",
            elapsed,
        )

        # --------------------------------------
        # PUBLIC RESPONSE
        # --------------------------------------

        return {
            "status": "success",
            "query": result["query"],
            "tasks": result["tasks"],
            "final_answer": result["final_answer"],
            "processing_time_seconds": elapsed,
        }

    except ValueError as exc:

        logger.warning(
            "Invalid research request: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except RuntimeError as exc:

        logger.error(
            "Pipeline runtime error: %s",
            exc,
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "Research service is temporarily unavailable."
            ),
        )

    except Exception:

        logger.exception(
            "Unexpected error while processing "
            "research request."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while processing the research request."
            ),
        )

    finally:

        _pipeline_semaphore.release()
