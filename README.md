# Arena

**The best engineer isn't the one who writes the most code. It's the one who directs AI to write the right code — faster, cheaper, and cleaner than anyone else.**

Arena is the first competitive platform built for **centaur engineering** — human + AI teams solving real problems, scored on efficiency, not just correctness. Use any AI tools you want: Cursor, Claude, Copilot, Aider, all of them. Submit your solution with your session log. Get scored on correctness, speed, token efficiency, and cost. Your **technique signature** — the full record of how you directed AI to solve the problem — is your credential. Free to enter. Paid when you win.

## How It Works

1. **Pick a challenge** from [`challenges/`](challenges/)
2. **Solve it** with any AI tools you want — or go pure human
3. **Submit via PR** to `submissions/<challenge-id>/<your-handle>/`
4. **Auto-scored** by CI — your score appears as a PR comment
5. **Leaderboard updates** on merge

## Current Challenges

| # | Challenge | Difficulty | Type |
|---|-----------|-----------|------|
| 001 | [Bytes-Per-Token Calibration](challenges/001-bytes-per-token/) | Medium | Real-world optimization |
| 002 | [Function Distiller](challenges/002-function-distiller/) | Hard | Compression / understanding |

## Categories

- **Centaur** — Human + AI collaboration. The primary format. Direct AI, make decisions, submit the result.
- **Human** — No LLM assistance. Just you, your editor, and your brain. Provides the baseline.
- **LLM** — Pure LLM solution. Prompt engineering counts. Shows what AI does alone.

Each category has its own leaderboard. Cross-category comparison uses efficiency-adjusted scores.

## Scoring

Composite = **Correctness (40%)** + **Token Efficiency (20%)** + **Speed (20%)** + **Solution Size (10%)** + **Cost (10%)**

Technique signatures (tools, iterations, session notes) are displayed on the leaderboard but don't affect scoring in v0. The community will vote on when technique data enters the formula.

Full details in [RULES.md](RULES.md).

## Quick Start

```bash
# Clone
git clone https://github.com/fieldjoshua/arena.git
cd arena

# Pick a challenge, read the spec
cat challenges/001-bytes-per-token/README.md

# Build your solution
# ...

# Test locally
python challenges/001-bytes-per-token/scoring.py your_solution.py

# Submit
cp your_solution.py submissions/001/your-handle/solution.py
# Write your technique.json (see RULES.md)
git checkout -b submit/001/your-handle
git add submissions/001/your-handle/
git commit -m "Submit: 001 bytes-per-token by your-handle"
# Open PR
```

## Links

- [Rules & Scoring](RULES.md)
- [Leaderboard](leaderboard/)
- [All Challenges](challenges/)

## License

MIT
