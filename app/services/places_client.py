from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import settings
from app.core.rate_limit import AsyncRateLimiter

logger = logging.getLogger(__name__)


class PlacesClient:
    """Thin client around Google Places API.

    This client uses the classic Places endpoints:
    - textsearch/json
    - details/json

    Docs: https://developers.google.com/maps/documentation/places/web-service/overview
    """

    def __init__(self, *, api_key: str | None = None, requests_per_second: int | None = None):
        self.api_key = api_key or settings.google_api_key
        rps = requests_per_second or settings.default_requests_per_second
        self.limiter = AsyncRateLimiter(requests_per_second=float(rps), burst=max(1, rps))
        self.base = settings.places_base_url.rstrip("/")

    async def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set")

        await self.limiter.acquire()
        params = dict(params)
        params["key"] = self.api_key
        params.setdefault("language", settings.places_language)

        url = f"{self.base}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status")
            if status not in (None, "OK", "ZERO_RESULTS"):
                # Common: OVER_QUERY_LIMIT, REQUEST_DENIED, INVALID_REQUEST
                raise RuntimeError(f"Places API error: {status} ({data.get('error_message', '')})")
            return data

    async def text_search(self, *, query: str, pagetoken: str | None = None, language: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"query": query}
        if pagetoken:
            params["pagetoken"] = pagetoken
        if language:
            params["language"] = language
        return await self._get("textsearch/json", params)

    async def place_details(self, *, place_id: str, fields: str, language: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"place_id": place_id, "fields": fields}
        if language:
            params["language"] = language
        return await self._get("details/json", params)
