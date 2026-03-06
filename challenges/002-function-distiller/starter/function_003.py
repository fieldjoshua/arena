"""Retry decorator with exponential backoff.

Retries a function on specified exceptions with configurable backoff,
jitter, and maximum attempts.
"""

from __future__ import annotations

import logging
import random
import time
from functools import wraps
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[Exception, int, float], None] | None = None,
) -> Callable[[F], F]:
    """Decorator that retries a function with exponential backoff.

    Args:
        max_attempts: Total attempts (including first). Must be >= 1.
        base_delay: Initial delay in seconds before first retry.
        max_delay: Maximum delay cap in seconds.
        backoff_factor: Multiplier applied to delay after each retry.
        jitter: If True, adds random jitter (0-100% of delay) to prevent thundering herd.
        retryable_exceptions: Tuple of exception types to catch and retry.
        on_retry: Optional callback(exception, attempt_number, next_delay) called before each retry.

    Returns:
        Decorated function that retries on failure.

    Raises:
        The last exception if all attempts are exhausted.
        ValueError if max_attempts < 1.

    Example:
        @retry_with_backoff(max_attempts=3, retryable_exceptions=(ConnectionError, TimeoutError))
        def fetch_data(url: str) -> dict:
            return requests.get(url).json()
    """
    if max_attempts < 1:
        raise ValueError(f"max_attempts must be >= 1, got {max_attempts}")

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            delay = base_delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    last_exception = exc

                    if attempt == max_attempts:
                        logger.warning(
                            "All %d attempts exhausted for %s: %s",
                            max_attempts,
                            func.__name__,
                            exc,
                        )
                        raise

                    actual_delay = min(delay, max_delay)
                    if jitter:
                        actual_delay *= (0.5 + random.random() * 0.5)

                    if on_retry is not None:
                        on_retry(exc, attempt, actual_delay)

                    logger.info(
                        "Retry %d/%d for %s after %.1fs: %s",
                        attempt,
                        max_attempts,
                        func.__name__,
                        actual_delay,
                        exc,
                    )
                    time.sleep(actual_delay)
                    delay *= backoff_factor

            # Should not reach here, but just in case
            raise last_exception  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator


# --- Tests ---

def test_succeeds_first_try():
    call_count = 0

    @retry_with_backoff(max_attempts=3, base_delay=0.01)
    def always_works():
        nonlocal call_count
        call_count += 1
        return "ok"

    assert always_works() == "ok"
    assert call_count == 1


def test_retries_then_succeeds():
    call_count = 0

    @retry_with_backoff(max_attempts=3, base_delay=0.01, jitter=False)
    def fails_twice():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("not yet")
        return "finally"

    assert fails_twice() == "finally"
    assert call_count == 3


def test_exhausts_all_attempts():
    @retry_with_backoff(max_attempts=2, base_delay=0.01, retryable_exceptions=(ValueError,))
    def always_fails():
        raise ValueError("nope")

    try:
        always_fails()
        assert False, "Should have raised"
    except ValueError:
        pass


def test_non_retryable_exception_propagates():
    @retry_with_backoff(max_attempts=3, base_delay=0.01, retryable_exceptions=(ValueError,))
    def raises_type_error():
        raise TypeError("wrong type")

    try:
        raises_type_error()
        assert False
    except TypeError:
        pass


def test_on_retry_callback():
    retries = []

    @retry_with_backoff(
        max_attempts=3, base_delay=0.01, jitter=False,
        on_retry=lambda exc, attempt, delay: retries.append(attempt),
    )
    def fails_then_works():
        if len(retries) < 2:
            raise RuntimeError("not yet")
        return "done"

    assert fails_then_works() == "done"
    assert retries == [1, 2]
