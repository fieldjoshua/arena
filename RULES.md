# Rules & Scoring

## Philosophy: Centaur-First

Arena is built for **centaur competition** — human + AI teams solving real engineering
problems together. The question isn't "can AI code?" (yes) or "can humans code?" (yes).
The question is: **how efficiently can you direct AI to solve the right problem?**

All three categories (human, LLM, centaur) are welcome, but centaur is the primary
competitive format. Pure human and pure LLM submissions provide baselines.

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
  "api_cost_usd": 0.43,
  "human_iterations": 7,
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
| `api_cost_usd` | float | No | Total API cost in USD (self-reported) |
| `human_iterations` | int | No | Number of human-directed iterations/prompts |
| `notes` | string | No | Brief description of your approach |

**Honor system for token counts and costs.** Report totals from your API dashboard
or tool logs. For human-only submissions, set tokens and cost to `0`. In future
versions, verifiable session logs (screen recording hashes, IDE plugin data) will
replace self-reporting.

## Scoring

### Composite Score (0-100)

```
score = (correctness * 0.40) + (token_efficiency * 0.20) + (speed * 0.20) + (solution_size * 0.10) + (cost_efficiency * 0.10)
```

### Component Breakdown

**Correctness (0-100, weight: 40%)**
- Determined by each challenge's test suite
- Binary pass/fail per test case, percentage of cases passed
- Must score > 0 to appear on leaderboard

**Token Efficiency (0-100, weight: 20%)**
- `efficiency = 100 * (1 - your_tokens / max_tokens_in_challenge)`
- Human-only submissions (`tokens_consumed = 0`) get 100
- Lower token consumption = higher score

**Speed (0-100, weight: 20%)**
- `wall_seconds` relative to challenge median
- Faster = higher score
- Normalized per challenge

**Solution Size (0-100, weight: 10%)**
- `lines_changed` relative to challenge par
- Fewer lines for the same correctness = higher score

**Cost Efficiency (0-100, weight: 10%)**
- `api_cost_usd` relative to challenge median
- Lower cost = higher score
- Human-only submissions get 100

### Technique Signatures (Display-Only in v0)

Technique data (tools used, human iterations, session notes) is **displayed on the
leaderboard** but does **not** affect the composite score in v0. This is deliberate —
technique-path scoring is the platform's long-term moat, but premature commitment to
a formula that feels unfair kills community trust.

The community will vote on when and how technique data enters the composite formula.

### Category Adjustments

Scores are comparable within a category. Cross-category comparison uses an **efficiency ratio**:

```
efficiency_ratio = tokens_consumed / max(lines_changed, 1)
```

Lower ratio = more efficient use of compute per line of output.

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
