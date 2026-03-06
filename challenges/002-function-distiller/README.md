# Challenge 002: Function Distiller

## The Problem

You have a Python function: 50-200 lines, with docstring, type hints, and tests. Your job is to produce a **distillate** -- a compressed representation that preserves the function's behavior, intent, and edge cases in minimal tokens.

The best distillate lets someone **reconstruct the function** from it alone. The best compression uses the fewest tokens to do so.

## Your Task

For each of the 5 functions in `starter/`, produce a distillate file:

```
distillate_001.md  # Distillate for function 001
distillate_002.md  # Distillate for function 002
...
```

Each distillate is free-form text (markdown, pseudocode, bullet points, whatever works). There is no template. The only constraint: **fewer tokens is better**.

**Constraints:**
- No code copying -- your distillate cannot contain >50% of the original source lines verbatim
- Must be self-contained -- no references to "the original function" or "see line 42"
- Must cover: purpose, inputs, outputs, algorithm, edge cases
- Maximum 500 tokens per distillate (hard cap)

## Scoring

Each distillate is judged by an LLM on two axes:

**Completeness (0-10):** Could someone reconstruct the function from just this distillate?
- 10: Perfect reconstruction possible
- 7-9: Minor details missing but structure and logic clear
- 4-6: Major gaps -- algorithm or edge cases missing
- 1-3: Only surface-level understanding possible
- 0: Useless

**Compression (0-10):** How efficiently was information packed?
- 10: Remarkable density -- every token carries meaning
- 7-9: Tight, minimal waste
- 4-6: Some redundancy or unnecessary explanation
- 1-3: Verbose, could be half the length
- 0: Longer than the original (automatic 0)

**Final score per function:** `completeness * 0.6 + compression * 0.4`

**Challenge score:** Average across all 5 functions, scaled to 0-100 for the composite calculation.

### Technique Bonus

Your technique signature affects the efficiency component:
- **Human distillation** — you read the function, wrote the distillate by hand
- **LLM distillation** — you prompted an LLM to summarize
- **Hybrid** — you used an LLM draft and edited it down

All approaches are valid. The question is: who compresses better?

## Starter Functions

The `starter/` directory contains 5 Python files, each with one function:

| # | Function | Lines | Domain |
|---|----------|-------|--------|
| 001 | `merge_intervals` | 55 | Algorithms |
| 002 | `parse_cron_expression` | 85 | Parsing |
| 003 | `retry_with_backoff` | 70 | Infrastructure |
| 004 | `diff_objects` | 120 | Data processing |
| 005 | `render_markdown_table` | 95 | Text formatting |

## Running Locally

```bash
# Score your distillates (requires OPENROUTER_API_KEY for LLM judge)
python scoring.py path/to/your/distillates/

# Or dry-run without LLM (checks format and token count only)
python scoring.py path/to/your/distillates/ --dry-run
```

## Submission

```
submissions/002/<your-handle>/
  distillate_001.md
  distillate_002.md
  distillate_003.md
  distillate_004.md
  distillate_005.md
  technique.json
```

## Why This Matters

Compression is the core skill of knowledge systems. A good distillate preserves what matters and discards what doesn't. This is what humans do when they take notes, what LLMs do when they summarize, and what knowledge engines do when they pack context windows. The question: who does it best, and how do they do it differently?
