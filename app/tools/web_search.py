import logging
import os

import requests


logger = logging.getLogger(__name__)


class SearXNGSearch:
    """
    Search interface using a SearXNG instance.

    The search layer is intentionally resilient:
    temporary search-engine failures should not crash
    the entire multi-agent research pipeline.
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 20,
    ):
        base_url = base_url or os.getenv(
            "SEARXNG_URL",
            "http://localhost:8080",
        )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict]:
        """
        Search SearXNG and return normalized results.

        Returns an empty list when SearXNG temporarily fails,
        allowing the research agent to handle the missing evidence.
        """

        try:
            response = requests.get(
                f"{self.base_url}/search",
                params={
                    "q": query,
                    "format": "json",
                    "categories": "general",
                },
                headers={
                    "User-Agent": "Mozilla/5.0",
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as exc:
            logger.warning(
                "SearXNG search failed for query '%s': %s",
                query,
                exc,
            )

            return []

        except ValueError as exc:
            logger.warning(
                "Invalid JSON response from SearXNG: %s",
                exc,
            )

            return []

        results = []

        for result in data.get("results", [])[:max_results]:
            results.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                }
            )

        logger.info(
            "SearXNG returned %d results for query: %s",
            len(results),
            query,
        )

        return results
