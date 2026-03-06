# Arena Research: Prior Art & Novelty Assessment

Source: centaur research analysis, March 2026.

## Novelty Claim

The four-way combination is genuinely novel:
1. Efficiency scoring beyond correctness (technique signatures track full path)
2. Same scoring for humans and LLMs (direct comparison on identical tasks)
3. Free to play, paid on win (tournament economics)
4. Observable technique paths (HOW you solved it, not just THAT you solved it)

No existing platform combines all four. Closest threats: SWE-rebench (efficiency scoring) + Kaggle (prize model + community).

## Centaur-First Thesis

The centaur format is not a third category — it IS the competition. Three reasons:
1. **Durability** — "human vs LLM" ages out. "How efficiently can you wield AI?" has longer shelf life.
2. **Tractable scoring** — human+LLM workflow logs are structurally comparable.
3. **Economic signal** — first live price-discovery mechanism for human-directed AI engineering labor.

## 10 Closest Analogs

| Platform | What It Has | What It Lacks |
|----------|------------|---------------|
| CodeElo | Elo on competitive problems | No centaur, no live platform |
| AtCoder WTF 2025 | Human vs AI event | One-off, not persistent |
| Meta Hacker Cup AI Track | AI track alongside human | No centaur, annual only |
| Kaggle | Prizes, community, infrastructure | No centaur track, ML-focused |
| Topcoder | Prize money, speed scoring | No AI track, stagnated |
| SWE-rebench | Cost/token tracking | Benchmark only, no humans |
| Code.golf | Efficiency scoring (brevity) | Single dimension, no AI |
| OpenAI PRMs / FunPRM | Process evaluation | Research only, LLM-only |
| Codeforces | Dominant competitive platform | Explicitly bans AI |
| HackerOne / Bugcrowd | Real bounties, real problems | Security-only, no scoring |

## Key Risks & Mitigations

1. **Human-in-loop ungovernable** — v0: honor system. v0.5: screen recording hash. v1: IDE plugin.
2. **Ghost town before network effect** — Launch on reputation (Elo, leaderboard), not bounties.
3. **Technique scoring too early** — v0: outcome-only scoring. Technique as display-only column.

## Sources

See full research document for 12 cited sources including CodeElo (arXiv 2501.01257),
SWE-bench, FunPRM (arXiv 2601.22249), HackerOne data, tournament theory.
