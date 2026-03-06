# Challenge 001: Bytes-Per-Token Calibration

## The Problem

The common heuristic `len(text) // 4` estimates token count from byte length. It's wrong by **24%** on average, and the error swings wildly by content type:

| Content Type | Actual bytes/token | `len//4` error |
|-------------|-------------------|---------------|
| Dense code (Python) | 2.42 | +65% overcount |
| Mixed (code + comments) | 3.10 | +29% overcount |
| Technical prose | 3.51 | +14% overcount |
| Natural prose | 3.78 | +6% overcount |

That's a **56% spread** between code and prose. A single heuristic can't cover it.

## Your Task

Implement a single function:

```python
def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens in the given text.

    Must beat len(text) // 4 on mean absolute error across
    a mixed test set of code, prose, and mixed content.

    No external dependencies allowed (no tiktoken, no API calls).
    Pure Python standard library only.
    """
    ...
```

**Constraints:**
- Python 3.11+ standard library only (no pip packages)
- No network calls (the function must work offline)
- Must handle empty strings, single characters, and 100KB+ texts
- Must return a non-negative integer

## Scoring

Your solution is tested against a **hidden test set** of 50 texts (code, prose, mixed) with known token counts (from `cl100k_base` tokenizer).

**Correctness (40%):**
- Mean Absolute Error (MAE) vs the baseline `len(text) // 4`
- Score = `100 * (1 - your_mae / baseline_mae)`, clamped to [0, 100]
- If your MAE is worse than the baseline, correctness = 0

**Efficiency (30%):** From your technique signature (tokens consumed).

**Elegance (15%):** Lines of code in your solution. Par = 30 lines.

**Speed (15%):** Wall time to solve.

## Baseline Data

The `baseline/` directory contains:

- `samples.json` — 20 reference texts with known token counts for calibration
- `baseline_score.json` — the `len//4` baseline's MAE on the hidden test set

Use the reference samples to develop your heuristic. The hidden test set has different texts but similar content-type distribution.

## Running Locally

```bash
# Test your solution against the reference samples
python scoring.py your_solution.py

# Output: MAE, per-sample errors, comparison to baseline
```

## Submission

```
submissions/001/<your-handle>/
  solution.py          # Must contain estimate_tokens(text: str) -> int
  technique.json       # Your technique signature
```

## Why This Matters

Token estimation drives budget allocation in LLM-powered systems. A 24% error compounds through every budget decision — over-allocating wastes money, under-allocating truncates context. The winner's approach gets integrated into a production system.
