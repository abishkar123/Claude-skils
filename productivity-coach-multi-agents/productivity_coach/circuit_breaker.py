"""Circuit Breaker for MCP connectors.

Implements the CLOSED → OPEN → HALF_OPEN state machine described in the
multi-agent orchestration patterns article. Prevents cascading failures when a
connector is flaky or down by fast-failing after a threshold of consecutive
errors, then probing recovery after a timeout.

States:
  CLOSED     Normal operation. Failures accumulate; threshold trips the breaker.
  OPEN       Fast-fail. All calls return immediately with fallback reason.
  HALF_OPEN  One test call allowed. Success → CLOSED, failure → OPEN again.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    name: str
    failure_threshold: int = 3       # consecutive failures before opening
    recovery_timeout: float = 60.0   # seconds before probing half-open
    _state: State = field(default=State.CLOSED, init=False, repr=False)
    _failures: int = field(default=0, init=False, repr=False)
    _opened_at: float = field(default=0.0, init=False, repr=False)

    # -- state inspection --------------------------------------------------
    @property
    def state(self) -> State:
        if self._state is State.OPEN:
            if time.monotonic() - self._opened_at >= self.recovery_timeout:
                self._state = State.HALF_OPEN
        return self._state

    @property
    def is_open(self) -> bool:
        return self.state is State.OPEN

    @property
    def allows_call(self) -> bool:
        s = self.state
        return s is State.CLOSED or s is State.HALF_OPEN

    # -- outcome recording --------------------------------------------------
    def record_success(self) -> None:
        self._failures = 0
        self._state = State.CLOSED

    def record_failure(self) -> None:
        self._failures += 1
        if self._state is State.HALF_OPEN or self._failures >= self.failure_threshold:
            self._state = State.OPEN
            self._opened_at = time.monotonic()

    # -- call wrapper -------------------------------------------------------
    def call(self, fn, *args, **kwargs):
        """Execute fn under circuit-breaker protection.

        Returns (result, None) on success.
        Returns (None, reason_str) when the circuit is open or the call fails.
        """
        if not self.allows_call:
            return None, (
                f"circuit open for '{self.name}' — "
                f"will retry in {self.recovery_timeout - (time.monotonic() - self._opened_at):.0f}s"
            )
        try:
            result = fn(*args, **kwargs)
            self.record_success()
            return result, None
        except Exception as exc:
            self.record_failure()
            return None, f"connector '{self.name}' error: {exc}"


class BreakerRegistry:
    """Session-scoped registry; one breaker per named connector."""

    def __init__(self):
        self._breakers: dict[str, CircuitBreaker] = {}

    def get(self, name: str) -> CircuitBreaker:
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name=name)
        return self._breakers[name]

    def states(self) -> dict[str, str]:
        return {name: b.state.value for name, b in self._breakers.items()}
