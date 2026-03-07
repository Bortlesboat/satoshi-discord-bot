"""Async API client for Satoshi API with TTL caching."""

import time
from typing import Any

import httpx


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class RateLimitError(APIError):
    """Raised when rate limited by the API."""

    def __init__(self, retry_after: float | None = None):
        self.retry_after = retry_after
        super().__init__(
            f"Rate limited. Try again in {retry_after}s" if retry_after else "Rate limited",
            status_code=429,
        )


class APIUnavailableError(APIError):
    """Raised when the API is down or unreachable."""

    def __init__(self):
        super().__init__("Satoshi API is temporarily unavailable", status_code=503)


# TTL defaults in seconds
DEFAULT_TTLS: dict[str, int] = {
    "prices": 30,
    "fees": 60,
    "mempool": 60,
    "blocks": 600,
    "supply": 1800,
    "mining": 300,
    "network": 1800,
    "tx": 600,
}


class CachedEntry:
    __slots__ = ("data", "expires_at")

    def __init__(self, data: Any, ttl: int):
        self.data = data
        self.expires_at = time.monotonic() + ttl


class SatoshiClient:
    """Async client for Satoshi API with per-endpoint TTL caching."""

    def __init__(self, base_url: str, api_key: str = ""):
        headers = {"Accept": "application/json"}
        if api_key:
            headers["X-API-Key"] = api_key
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=10.0,
        )
        self._cache: dict[str, CachedEntry] = {}

    async def close(self):
        await self._client.aclose()

    def _get_ttl(self, path: str) -> int:
        """Determine TTL based on the endpoint path."""
        for key, ttl in DEFAULT_TTLS.items():
            if key in path:
                return ttl
        return 60

    async def get(self, path: str, **params) -> dict[str, Any]:
        """GET an endpoint with caching. Returns the 'data' field from the response."""
        cache_key = f"{path}:{sorted(params.items())}" if params else path

        # Check cache
        entry = self._cache.get(cache_key)
        if entry and time.monotonic() < entry.expires_at:
            return entry.data

        # Make request
        try:
            resp = await self._client.get(f"/api/v1{path}", params=params or None)
        except httpx.TimeoutException:
            raise APIUnavailableError()
        except httpx.ConnectError:
            raise APIUnavailableError()

        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            raise RateLimitError(float(retry_after) if retry_after else None)
        if resp.status_code >= 500:
            raise APIUnavailableError()
        if resp.status_code == 404:
            raise APIError("Resource not found", status_code=404)
        if resp.status_code >= 400:
            detail = resp.json().get("detail", "Bad request") if resp.headers.get("content-type", "").startswith("application/json") else resp.text
            raise APIError(str(detail), status_code=resp.status_code)

        body = resp.json()
        data = body.get("data", body)

        # Cache successful response
        ttl = self._get_ttl(path)
        self._cache[cache_key] = CachedEntry(data, ttl)

        return data
