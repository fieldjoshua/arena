"""Merge overlapping intervals.

Given a list of intervals [start, end], merge all overlapping intervals
and return the result sorted by start time.
"""

from __future__ import annotations


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals into non-overlapping intervals.

    Args:
        intervals: List of [start, end] pairs. Start and end are inclusive.
            May be unsorted. May contain duplicates. May be empty.

    Returns:
        Sorted list of merged [start, end] pairs with no overlaps.
        Adjacent intervals (e.g., [1,3] and [4,6]) are NOT merged --
        only overlapping ones are (e.g., [1,4] and [3,6] -> [1,6]).

    Raises:
        ValueError: If any interval has start > end.

    Examples:
        >>> merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
        [[1, 6], [8, 10], [15, 18]]
        >>> merge_intervals([[1, 4], [4, 5]])
        [[1, 5]]
        >>> merge_intervals([])
        []
        >>> merge_intervals([[1, 1]])
        [[1, 1]]
    """
    if not intervals:
        return []

    # Validate
    for interval in intervals:
        if len(interval) != 2:
            raise ValueError(f"Expected [start, end], got {interval}")
        if interval[0] > interval[1]:
            raise ValueError(
                f"Invalid interval: start ({interval[0]}) > end ({interval[1]})"
            )

    # Sort by start time, then by end time descending for equal starts
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))

    merged: list[list[int]] = [sorted_intervals[0][:]]  # copy first

    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  # overlapping
            last[1] = max(last[1], current[1])
        else:
            merged.append(current[:])  # copy to avoid mutation

    return merged


# --- Tests ---

def test_basic_merge():
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6], [8, 10], [15, 18]
    ]

def test_touching_intervals():
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]

def test_empty():
    assert merge_intervals([]) == []

def test_single():
    assert merge_intervals([[1, 1]]) == [[1, 1]]

def test_no_overlap():
    assert merge_intervals([[1, 2], [5, 6], [9, 10]]) == [[1, 2], [5, 6], [9, 10]]

def test_full_overlap():
    assert merge_intervals([[1, 10], [2, 5], [3, 7]]) == [[1, 10]]

def test_unsorted_input():
    assert merge_intervals([[5, 6], [1, 3], [2, 4]]) == [[1, 4], [5, 6]]

def test_duplicates():
    assert merge_intervals([[1, 3], [1, 3], [1, 3]]) == [[1, 3]]

def test_invalid_interval():
    try:
        merge_intervals([[5, 1]])
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
