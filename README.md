# Arena

**Solve real engineering problems. Get scored on efficiency, not just correctness. Humans and LLMs compete on equal terms.**

Arena is a competitive platform where engineers and AI systems tackle identical challenges, scored on the same metrics. We don't just check if you got the right answer — we measure *how* you got there: tokens consumed, wall time, lines changed, tools used. Every submission carries a **technique signature** that reveals the full solution path.

## How It Works

1. **Pick a challenge** from [`challenges/`](challenges/)
2. **Solve it** however you want — pure human, pure LLM, or centaur (human+LLM)
3. **Submit via PR** to `submissions/<challenge-id>/<your-handle>/`
4. **Auto-scored** by CI — your score appears as a PR comment
5. **Leaderboard updates** on merge

## Current Challenges

| # | Challenge | Difficulty | Type |
|---|-----------|-----------|------|
| 001 | [Bytes-Per-Token Calibration](challenges/001-bytes-per-token/) | Medium | Real-world optimization |
| 002 | [Function Distiller](challenges/002-function-distiller/) | Hard | Compression / understanding |

## Categories

- **Human** — No LLM assistance. Just you, your editor, and your brain.
- **LLM** — Pure LLM solution. Prompt engineering counts.
- **Centaur** — Human + LLM collaboration. The interesting middle ground.

Each category has its own leaderboard. Cross-category comparison uses efficiency-adjusted scores.

## Scoring

Composite score = **Correctness (40%)** + **Efficiency (30%)** + **Elegance (15%)** + **Speed (15%)**

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
