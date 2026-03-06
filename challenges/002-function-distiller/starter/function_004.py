"""Deep diff two nested Python objects.

Produces a structured diff showing additions, removals, and changes
at every level of nesting.
"""

from __future__ import annotations

from typing import Any


def diff_objects(
    old: Any,
    new: Any,
    path: str = "$",
    ignore_order: bool = False,
) -> list[dict[str, Any]]:
    """Compute a structured diff between two nested Python objects.

    Supports dicts, lists, sets, and primitive values. Produces a flat
    list of change records, each with a JSON-path-style location.

    Args:
        old: The original object.
        new: The updated object.
        path: Current path prefix (used in recursion, start with "$").
        ignore_order: If True, treat lists as sets for comparison.

    Returns:
        List of change dicts, each with:
        - "path": str — JSON-path-style location (e.g., "$.users[0].name")
        - "type": str — "added", "removed", "changed", or "type_changed"
        - "old_value": Any — previous value (absent for "added")
        - "new_value": Any — new value (absent for "removed")

    Examples:
        >>> diff_objects({"a": 1}, {"a": 2})
        [{"path": "$.a", "type": "changed", "old_value": 1, "new_value": 2}]
        >>> diff_objects({"a": 1}, {"b": 1})
        [{"path": "$.a", "type": "removed", "old_value": 1},
         {"path": "$.b", "type": "added", "new_value": 1}]
    """
    changes: list[dict[str, Any]] = []

    # Type mismatch at this level
    if type(old) is not type(new):
        changes.append({
            "path": path,
            "type": "type_changed",
            "old_value": _summarize(old),
            "new_value": _summarize(new),
            "old_type": type(old).__name__,
            "new_type": type(new).__name__,
        })
        return changes

    # Dicts
    if isinstance(old, dict):
        all_keys = set(old.keys()) | set(new.keys())
        for key in sorted(all_keys, key=str):
            child_path = f"{path}.{key}"
            if key not in old:
                changes.append({
                    "path": child_path,
                    "type": "added",
                    "new_value": new[key],
                })
            elif key not in new:
                changes.append({
                    "path": child_path,
                    "type": "removed",
                    "old_value": old[key],
                })
            else:
                changes.extend(
                    diff_objects(old[key], new[key], child_path, ignore_order)
                )
        return changes

    # Lists
    if isinstance(old, list):
        if ignore_order:
            return _diff_unordered(old, new, path)
        return _diff_ordered_lists(old, new, path, ignore_order)

    # Sets
    if isinstance(old, set):
        added = new - old
        removed = old - new
        for item in sorted(removed, key=str):
            changes.append({
                "path": f"{path}{{}}",
                "type": "removed",
                "old_value": item,
            })
        for item in sorted(added, key=str):
            changes.append({
                "path": f"{path}{{}}",
                "type": "added",
                "new_value": item,
            })
        return changes

    # Primitives
    if old != new:
        changes.append({
            "path": path,
            "type": "changed",
            "old_value": old,
            "new_value": new,
        })

    return changes


def _diff_ordered_lists(
    old: list, new: list, path: str, ignore_order: bool
) -> list[dict[str, Any]]:
    """Diff two lists preserving order."""
    changes: list[dict[str, Any]] = []
    max_len = max(len(old), len(new))

    for i in range(max_len):
        child_path = f"{path}[{i}]"
        if i >= len(old):
            changes.append({
                "path": child_path,
                "type": "added",
                "new_value": new[i],
            })
        elif i >= len(new):
            changes.append({
                "path": child_path,
                "type": "removed",
                "old_value": old[i],
            })
        else:
            changes.extend(
                diff_objects(old[i], new[i], child_path, ignore_order)
            )

    return changes


def _diff_unordered(
    old: list, new: list, path: str
) -> list[dict[str, Any]]:
    """Diff two lists ignoring order (treat as multisets)."""
    changes: list[dict[str, Any]] = []

    # Simple approach: convert to string representations for matching
    old_strs = [repr(item) for item in old]
    new_strs = [repr(item) for item in new]

    old_remaining = list(old_strs)
    for i, s in enumerate(new_strs):
        if s in old_remaining:
            old_remaining.remove(s)
        else:
            changes.append({
                "path": f"{path}[+]",
                "type": "added",
                "new_value": new[i],
            })

    new_remaining = list(new_strs)
    for i, s in enumerate(old_strs):
        if s in new_remaining:
            new_remaining.remove(s)
        else:
            changes.append({
                "path": f"{path}[-]",
                "type": "removed",
                "old_value": old[i],
            })

    return changes


def _summarize(value: Any) -> str:
    """Summarize a complex value for display in type_changed records."""
    if isinstance(value, (dict, list, set)):
        return f"{type(value).__name__}({len(value)} items)"
    return repr(value)


# --- Tests ---

def test_simple_change():
    result = diff_objects({"a": 1}, {"a": 2})
    assert len(result) == 1
    assert result[0]["type"] == "changed"
    assert result[0]["old_value"] == 1
    assert result[0]["new_value"] == 2

def test_addition_and_removal():
    result = diff_objects({"a": 1}, {"b": 1})
    types = {r["type"] for r in result}
    assert types == {"added", "removed"}

def test_nested_dict():
    old = {"user": {"name": "Alice", "age": 30}}
    new = {"user": {"name": "Bob", "age": 30}}
    result = diff_objects(old, new)
    assert len(result) == 1
    assert result[0]["path"] == "$.user.name"

def test_list_diff():
    result = diff_objects([1, 2, 3], [1, 2, 4])
    assert len(result) == 1
    assert result[0]["path"] == "$[2]"

def test_list_length_change():
    result = diff_objects([1, 2], [1, 2, 3])
    assert any(r["type"] == "added" for r in result)

def test_type_change():
    result = diff_objects({"a": [1, 2]}, {"a": "string"})
    assert result[0]["type"] == "type_changed"

def test_identical():
    assert diff_objects({"a": 1, "b": [2, 3]}, {"a": 1, "b": [2, 3]}) == []

def test_set_diff():
    result = diff_objects({1, 2, 3}, {2, 3, 4})
    assert len(result) == 2  # removed 1, added 4

def test_ignore_order():
    result = diff_objects([3, 1, 2], [1, 2, 3], ignore_order=True)
    assert result == []

def test_deeply_nested():
    old = {"a": {"b": {"c": {"d": 1}}}}
    new = {"a": {"b": {"c": {"d": 2}}}}
    result = diff_objects(old, new)
    assert result[0]["path"] == "$.a.b.c.d"
