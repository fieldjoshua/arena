# Challenge Specification Format

Every challenge lives in `challenges/<id>-<slug>/` and must include these files.

## Required Files

### `challenge.yml` — Machine-readable spec

```yaml
id: "003"
slug: "api-rate-limiter"
title: "Build an API Rate Limiter"
version: 1

# Classification
difficulty: medium          # easy | medium | hard | extreme
domain: infrastructure      # algorithms | parsing | infrastructure | data | compression | systems
estimated_time_minutes: 90  # expected median solve time
tags: ["concurrency", "distributed-systems", "python"]

# Problem definition
language: python            # python | javascript | rust | any
python_version: ">=3.11"
external_deps_allowed: false  # true = pip packages allowed, false = stdlib only
network_allowed: false       # can the solution make network calls?

# Entry point
solution_file: "solution.py"
entry_function: "rate_limit"  # function the scorer will import and call
signature: "rate_limit(key: str, max_requests: int, window_seconds: int) -> bool"

# Scoring parameters
par_lines: 40               # "par" line count for solution_size scoring
max_tokens: 100000           # normalization cap for token efficiency
median_seconds: 5400         # expected median wall time (seconds)
median_cost_usd: 1.00       # expected median API cost

# Bounty (optional)
bounty_usd: 0               # 0 = no bounty
bounty_window_days: 7        # days after publish before bounty is awarded
sponsor: ""                  # who's paying

# Test suite
test_cases_public: 10        # number of test cases in starter/
test_cases_hidden: 40        # number of test cases in hidden suite
scoring_method: "correctness_pct"  # correctness_pct | mae_vs_baseline | llm_judge

# Author
author: "fieldjoshua"
author_competing: false      # is the author submitting a solution?
published: "2026-03-06"
```

### `README.md` — Human-readable problem spec

Must include:
1. **The Problem** — what and why (real-world context)
2. **Your Task** — exact function signature, constraints, what to implement
3. **Scoring** — how correctness is measured for this specific challenge
4. **Baseline Data** — reference inputs/outputs for local development
5. **Constraints** — language, deps, network, time limits
6. **Submission Format** — expected files in the submission directory

### `scoring.py` — Auto-scorer

Must implement:
```python
def score(solution_path: str) -> dict:
    """Score a submission.

    Returns:
        {
            "correctness_pct": float,  # 0-100
            "details": {...},          # challenge-specific breakdown
        }
    """
```

Invoked by CI as: `python scoring.py path/to/solution.py`
Must exit 0 on success, non-zero on invalid submission.
Must write `results.json` to the solution directory.

### `baseline/` — Reference data

Public test cases, sample inputs/outputs, baseline scores.
Competitors use this for local development.

### `starter/` (optional)

Starter code, test harness, boilerplate. Reduces friction for competitors.

## Optional Files

### `hidden/` — Hidden test suite (private branch)

Not in the public repo. Stored in a private branch or separate scoring repo.
CI checks out the hidden branch during scoring.

### `editorial.md` — Post-competition writeup

Published after the bounty window closes. Explains the intended approach,
interesting submissions, and technique signature analysis.

## Submitting a New Challenge

1. Fork the repo
2. Create `challenges/<id>-<slug>/` with all required files
3. Open a PR with the `challenge-submission` label
4. Maintainers review for:
   - Clear, unambiguous problem statement
   - Working scorer that handles edge cases
   - Reasonable difficulty rating and time estimate
   - No dependency on proprietary data or services
   - Hidden test suite is fair (no gotchas beyond the stated constraints)
5. On merge, challenge goes live

## Challenge IDs

Sequential three-digit IDs: 001, 002, 003, ...
Assigned by maintainers on merge (proposers use `XXX` in their PR).
