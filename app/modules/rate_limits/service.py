"""In-memory anti-spam rate limiting.

MVP implementation: a per-(user, action) sliding window plus a cooldown,
kept in process memory. For multi-process / production, back this with Redis
using the same interface.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass(frozen=True)
class RateDecision:
    allowed: bool
    retry_after: int  # seconds until the next attempt is allowed (0 if allowed)


class RateLimitService:
    def __init__(
        self,
        max_messages: int,
        window_seconds: int,
        cooldown_seconds: int,
    ) -> None:
        self._max = max_messages
        self._window = window_seconds
        self._cooldown = cooldown_seconds
        self._events: dict[tuple[int, str], deque[float]] = defaultdict(deque)
        self._last: dict[tuple[int, str], float] = {}

    def check(self, user_id: int, action: str = "message") -> RateDecision:
        """Check (and record) an attempt for the given user/action."""
        now = time.monotonic()
        key = (user_id, action)

        # Cooldown between consecutive actions.
        last = self._last.get(key)
        if last is not None and (now - last) < self._cooldown:
            return RateDecision(False, max(1, int(self._cooldown - (now - last))))

        # Sliding window.
        events = self._events[key]
        cutoff = now - self._window
        while events and events[0] < cutoff:
            events.popleft()

        if len(events) >= self._max:
            retry = max(1, int(events[0] + self._window - now))
            return RateDecision(False, retry)

        events.append(now)
        self._last[key] = now
        return RateDecision(True, 0)
