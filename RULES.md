# Rules & Scoring

## Submission Format

Every submission lives in `submissions/<challenge-id>/<your-handle>/` and must include:

1. **Your solution** (the file(s) specified by the challenge)
2. **`technique.json`** — your technique signature (see below)

### technique.json

```json
{
  "category": "centaur",
  "tools_used": ["claude-code", "pytest", "grep"],
  "tokens_consumed": 12500,
  "wall_seconds": 1800,
  "lines_changed": 45,
  "notes": "Used Claude to explore tokenizer behavior, wrote the calibration logic manually."
}
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | string | Yes | `"human"`, `"llm"`, or `"centaur"` |
| `tools_used` | string[] | Yes | Tools, models, editors used |
| `tokens_consumed` | int | Yes | Total LLM tokens (input+output). `0` for human-only. |
| `wall_seconds` | int | Yes | Total time from start to finish |
| `lines_changed` | int | Yes | Lines added/modified in your solution |
| `notes` | string | No | Brief description of your approach |

**Honor system for token counts.** If using an LLM, report total tokens from your API dashboard or tool logs. For human-only submissions, set to `0`.

## Scoring

### Composite Score (0-100)

```
score = (correctness * 0.40) + (efficiency * 0.30) + (elegance * 0.15) + (speed * 0.15)
```

### Component Breakdown

**Correctness (0-100, weight: 40%)**
- Determined by each challenge's test suite
- Binary pass/fail per test case, percentage of cases passed
- Must score > 0 to appear on leaderboard

**Efficiency (0-100, weight: 30%)**
- `efficiency = 100 * (1 - your_tokens / max_tokens_in_challenge)`
- Human-only submissions (`tokens_consumed = 0`) get 100
- Measures: how much compute did you burn to get here?
- Lower token consumption = higher score

**Elegance (0-100, weight: 15%)**
- `lines_changed` relative to challenge median
- Fewer lines for the same correctness = higher score
- Bonus for solutions under the challenge's "par" line count

**Speed (0-100, weight: 15%)**
- `wall_seconds` relative to challenge median
- Faster = higher score
- Normalized per challenge (some problems are meant to be slow)

### Category Adjustments

Scores are comparable within a category. Cross-category comparison uses an **efficiency ratio**:

```
efficiency_ratio = tokens_consumed / max(lines_changed, 1)
```

Lower ratio = more efficient use of compute per line of output. This lets a human who wrote 20 lines in 30 minutes compare meaningfully against an LLM that consumed 50K tokens to produce the same 20 lines.

## Leaderboard

- Separate rankings per challenge per category
- Overall ranking uses average composite score across all attempted challenges
- Ties broken by efficiency ratio (lower wins)

## Fair Play

1. **No solution sharing** before the challenge closes
2. **Submissions are public** — your code and technique signature are visible to all
3. **One submission per handle per challenge** (you can update by opening a new PR)
4. **Token counts are honor system** — blatant misreporting gets you removed
5. **No gaming the test suite** — solutions must be general, not test-case-specific
6. **Challenge authors may submit** but are marked as `[author]` on the leaderboard

## Disputes

Open an issue. Community resolves by discussion.
