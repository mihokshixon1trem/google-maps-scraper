import asyncio
import time
from dataclasses import dataclass


@dataclass
class TokenBucket:
    capacity: int
    refill_per_second: float
    tokens: float
    last_refill: float

    @classmethod
    def create(cls, capacity: int, refill_per_second: float) -> "TokenBucket":
        now = time.monotonic()
        return cls(capacity=capacity, refill_per_second=refill_per_second, tokens=float(capacity), last_refill=now)

    def consume(self, amount: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_second)
        self.last_refill = now
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False


class AsyncRateLimiter:
    def __init__(self, requests_per_second: float, burst: int | None = None):
        burst = burst or max(1, int(requests_per_second))
        self._bucket = TokenBucket.create(capacity=burst, refill_per_second=float(requests_per_second))

    async def acquire(self) -> None:
        while not self._bucket.consume(1.0):
            await asyncio.sleep(0.05)
