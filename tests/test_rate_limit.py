import pytest
import asyncio

from app.core.rate_limit import AsyncRateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_acquire():
    limiter = AsyncRateLimiter(requests_per_second=10, burst=2)
    await limiter.acquire()
    await limiter.acquire()
