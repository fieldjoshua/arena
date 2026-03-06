"""Parse cron expressions into human-readable schedules.

Supports standard 5-field cron: minute hour day-of-month month day-of-week.
Supports wildcards (*), ranges (1-5), steps (*/15), and lists (1,3,5).
"""

from __future__ import annotations

FIELD_NAMES = ["minute", "hour", "day_of_month", "month", "day_of_week"]
FIELD_RANGES = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day_of_month": (1, 31),
    "month": (1, 12),
    "day_of_week": (0, 6),  # 0 = Sunday
}

DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def parse_cron_expression(expression: str) -> dict[str, list[int]]:
    """Parse a cron expression into expanded value lists.

    Args:
        expression: Standard 5-field cron string, e.g. "*/15 9-17 * * 1-5"

    Returns:
        Dict mapping field names to sorted lists of valid values.
        Example: {"minute": [0, 15, 30, 45], "hour": [9,10,...,17], ...}

    Raises:
        ValueError: If expression is malformed or values out of range.
    """
    fields = expression.strip().split()
    if len(fields) != 5:
        raise ValueError(
            f"Expected 5 fields, got {len(fields)}: {expression!r}"
        )

    result: dict[str, list[int]] = {}
    for field_str, name in zip(fields, FIELD_NAMES):
        lo, hi = FIELD_RANGES[name]
        values = _parse_field(field_str, lo, hi)
        if not values:
            raise ValueError(f"Empty value set for {name}: {field_str!r}")
        result[name] = values

    return result


def _parse_field(field: str, lo: int, hi: int) -> list[int]:
    """Parse a single cron field into a sorted list of integers."""
    values: set[int] = set()

    for part in field.split(","):
        if "/" in part:
            range_part, step_str = part.split("/", 1)
            step = int(step_str)
            if step <= 0:
                raise ValueError(f"Step must be positive: {part!r}")
            start, end = _parse_range(range_part, lo, hi)
            values.update(range(start, end + 1, step))
        elif "-" in part:
            start, end = _parse_range(part, lo, hi)
            values.update(range(start, end + 1))
        elif part == "*":
            values.update(range(lo, hi + 1))
        else:
            val = int(part)
            if val < lo or val > hi:
                raise ValueError(f"Value {val} out of range [{lo}, {hi}]")
            values.add(val)

    return sorted(values)


def _parse_range(range_str: str, lo: int, hi: int) -> tuple[int, int]:
    """Parse a range like '1-5' or '*' into (start, end)."""
    if range_str == "*":
        return lo, hi
    parts = range_str.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid range: {range_str!r}")
    start, end = int(parts[0]), int(parts[1])
    if start < lo or end > hi:
        raise ValueError(f"Range {start}-{end} out of bounds [{lo}, {hi}]")
    if start > end:
        raise ValueError(f"Range start ({start}) > end ({end})")
    return start, end


# --- Tests ---

def test_every_15_minutes_business_hours_weekdays():
    result = parse_cron_expression("*/15 9-17 * * 1-5")
    assert result["minute"] == [0, 15, 30, 45]
    assert result["hour"] == list(range(9, 18))
    assert result["day_of_month"] == list(range(1, 32))
    assert result["day_of_week"] == [1, 2, 3, 4, 5]

def test_midnight_daily():
    result = parse_cron_expression("0 0 * * *")
    assert result["minute"] == [0]
    assert result["hour"] == [0]

def test_specific_values():
    result = parse_cron_expression("30 8 1,15 * *")
    assert result["minute"] == [30]
    assert result["hour"] == [8]
    assert result["day_of_month"] == [1, 15]

def test_every_minute():
    result = parse_cron_expression("* * * * *")
    assert result["minute"] == list(range(0, 60))

def test_invalid_field_count():
    try:
        parse_cron_expression("* * *")
        assert False
    except ValueError:
        pass

def test_out_of_range():
    try:
        parse_cron_expression("60 * * * *")
        assert False
    except ValueError:
        pass
