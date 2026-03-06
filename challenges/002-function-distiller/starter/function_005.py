"""Render data as a formatted markdown table.

Handles column alignment, truncation, header formatting, and edge cases
like missing keys, mixed types, and empty data.
"""

from __future__ import annotations

from typing import Any


def render_markdown_table(
    rows: list[dict[str, Any]],
    columns: list[str] | None = None,
    align: dict[str, str] | None = None,
    max_width: int = 40,
    truncation_marker: str = "...",
    empty_cell: str = "-",
    title: str | None = None,
) -> str:
    """Render a list of dicts as a GitHub-flavored markdown table.

    Args:
        rows: List of row dicts. Keys are column names.
        columns: Explicit column order. If None, inferred from all row keys
            in order of first appearance.
        align: Dict mapping column name to alignment ("left", "right", "center").
            Defaults to "left" for strings, "right" for numbers.
        max_width: Maximum cell width in characters. Longer values are truncated.
        truncation_marker: String appended to truncated values.
        empty_cell: Placeholder for missing values.
        title: Optional table title (rendered as ## heading above table).

    Returns:
        Formatted markdown table string.

    Raises:
        ValueError: If rows is empty and columns is None (can't infer columns).
    """
    if not rows and columns is None:
        raise ValueError("Cannot infer columns from empty rows. Provide columns explicitly.")

    # Determine columns
    if columns is None:
        seen: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.append(key)
        columns = seen

    if not columns:
        return ""

    # Auto-detect alignment from first row with data
    if align is None:
        align = {}
    resolved_align: dict[str, str] = {}
    for col in columns:
        if col in align:
            resolved_align[col] = align[col]
        else:
            # Check first non-None value
            for row in rows:
                val = row.get(col)
                if val is not None:
                    resolved_align[col] = "right" if isinstance(val, (int, float)) else "left"
                    break
            else:
                resolved_align[col] = "left"

    # Format cell values
    def format_cell(value: Any) -> str:
        if value is None:
            return empty_cell
        text = str(value)
        if len(text) > max_width:
            return text[: max_width - len(truncation_marker)] + truncation_marker
        return text

    # Build header
    header_cells = [format_cell(col) for col in columns]

    # Build separator with alignment markers
    sep_cells: list[str] = []
    for col in columns:
        a = resolved_align.get(col, "left")
        if a == "right":
            sep_cells.append("---:")
        elif a == "center":
            sep_cells.append(":---:")
        else:
            sep_cells.append("---")

    # Build data rows
    data_rows: list[list[str]] = []
    for row in rows:
        cells = [format_cell(row.get(col)) for col in columns]
        data_rows.append(cells)

    # Assemble table
    lines: list[str] = []
    if title:
        lines.append(f"## {title}")
        lines.append("")

    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(sep_cells) + " |")
    for data_row in data_rows:
        lines.append("| " + " | ".join(data_row) + " |")

    return "\n".join(lines)


# --- Tests ---

def test_basic_table():
    rows = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    result = render_markdown_table(rows)
    assert "| name | age |" in result
    assert "| Alice | 30 |" in result

def test_explicit_columns():
    rows = [{"a": 1, "b": 2, "c": 3}]
    result = render_markdown_table(rows, columns=["c", "a"])
    lines = result.strip().split("\n")
    assert "c" in lines[0]
    assert "b" not in lines[0]

def test_missing_keys():
    rows = [{"a": 1}, {"a": 2, "b": 3}]
    result = render_markdown_table(rows)
    assert "-" in result  # empty_cell for missing 'b' in first row

def test_truncation():
    rows = [{"text": "a" * 100}]
    result = render_markdown_table(rows, max_width=10)
    assert "..." in result

def test_numeric_alignment():
    rows = [{"name": "X", "score": 95}]
    result = render_markdown_table(rows)
    lines = result.strip().split("\n")
    assert "---:" in lines[1]  # right-aligned for numeric

def test_empty_rows_with_columns():
    result = render_markdown_table([], columns=["a", "b"])
    assert "| a | b |" in result

def test_empty_rows_without_columns():
    try:
        render_markdown_table([])
        assert False
    except ValueError:
        pass

def test_title():
    rows = [{"x": 1}]
    result = render_markdown_table(rows, title="My Table")
    assert result.startswith("## My Table")

def test_custom_alignment():
    rows = [{"a": 1, "b": 2}]
    result = render_markdown_table(rows, align={"a": "center", "b": "left"})
    assert ":---:" in result
