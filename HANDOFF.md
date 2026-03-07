# Arena Handoff Memo

You are picking up a new repo: **Arena** — a gamified competitive engineering platform where human+AI centaur teams compete on real problems, scored on efficiency.

## What Exists (3 commits, all on `main`)

### Live Infrastructure
- **GitHub repo:** https://github.com/fieldjoshua/arena (public)
- **GitHub Pages:** https://fieldjoshua.github.io/arena/ (live, dark monospace landing page)
- **CI:** Two workflows in `.github/workflows/` — `score.yml` (auto-scores PRs to `submissions/`) and `leaderboard.yml` (rebuilds leaderboard on merge to main)

### Scoring Engine (`scoring/`)
- `technique.py` — `TechniqueSignature` dataclass + `score_submission()` composite scorer
- `aggregate.py` — Reads `results.json` from all submissions, builds `leaderboard/data.json`
- **Weights:** Correctness 40%, Token Efficiency 20%, Speed 20%, Solution Size 10%, Cost 10%
- **Technique signatures are display-only in v0** — shown on leaderboard, don't affect composite score. Community votes on when they enter the formula.
- Tested and working locally. No external dependencies.

### Two Challenges Live
- **001: Bytes-Per-Token Calibration** — Beat `len(text) // 4` on token estimation. 20 calibration samples (code/prose/mixed) with real token counts. Self-contained scorer. Par = 30 lines.
- **002: Function Distiller** — Compress 5 Python functions into minimal distillates. LLM-judged (completeness + compression). Has `--dry-run` mode for offline format checks. Requires `OPENROUTER_API_KEY` for live scoring.

### Docs (`docs/`)
- `research.md` — Prior art analysis. 10 closest analogs. Novelty assessment: the four-way combination (efficiency scoring + centaur format + tournament economics + technique paths) is genuinely novel. SWE-rebench + Kaggle together are the strongest prior art threat.
- `business-model.md` — Six revenue streams. Primary: AI lab benchmarking ("your model in real engineers' hands"). The competition is free; the data is the product.
- `data-capture.md` — Four-layer instrumentation spec. Layer 1 (technique.json) is live. Layers 2-4 (session logs, keystrokes, eye tracking) are specced but not built.

### Challenge Submission Format
- `challenges/CHALLENGE_SPEC.md` — Standardized `challenge.yml` schema so anyone can submit problem sets. Machine-readable difficulty, scoring method, bounty terms, entry point.

## Key Design Decisions

1. **Centaur-first.** Human+AI is the primary format, not a third category. Pure human and pure LLM provide baselines. The pitch: "The best engineer isn't the one who writes the most code."
2. **Technique signatures display-only in v0.** Risk mitigation from research — premature scoring formula commitment kills community trust. Collect the data now, let the community decide when it affects scores.
3. **GitHub-native.** Zero infrastructure cost. Submissions via PR, scoring via Actions, leaderboard via Pages. Scales to v0.5 before needing real infra.
4. **No external dependencies in scoring engine.** Pure Python stdlib. Challenge scorers are self-contained.
5. **Honor system for token counts.** Acceptable for v0. Session log verification (screen recording hashes, IDE plugin) planned for v0.5/v1.

## What's NOT Built Yet

| Item | Priority | Notes |
|------|----------|-------|
| Session log format (Layer 2) | v0.5 | YAML schema specced in `data-capture.md`, no CLI tool yet |
| VS Code/Cursor extension (Layer 3) | v1 | Keystroke + editor telemetry capture |
| Eye tracking (Layer 4) | v2 | WebGazer.js + MediaPipe specced, not built |
| Submission CLI (`arena submit`) | v0.5 | Currently manual PR process |
| Sandboxed execution (Judge0/DMOJ) | v0.5 | Currently runs in GH Actions unsandboxed |
| Payment rails (Stripe Connect) | v0.5 | Currently manual PayPal |
| User accounts (GitHub OAuth) | v1 | Currently handle-based |
| Elo ratings | v1 | Currently composite score only |
| Community challenge submission | v0.5 | Spec exists, no review pipeline |
| Hidden test suites | v0.5 | Currently all test data is public |

## File Map

```
arena/
  README.md              # Pitch + quick start
  RULES.md               # Scoring system, centaur-first philosophy
  HANDOFF.md             # This file
  index.html             # GitHub Pages landing page
  LICENSE                # MIT
  scoring/
    technique.py         # TechniqueSignature + score_submission()
    aggregate.py         # Leaderboard builder
  challenges/
    CHALLENGE_SPEC.md    # Standardized format for new challenges
    001-bytes-per-token/
      README.md          # Problem spec
      scoring.py         # Auto-scorer
      baseline/          # 20 samples + baseline MAE
    002-function-distiller/
      README.md          # Problem spec
      scoring.py         # LLM-judged scorer
      starter/           # 5 Python functions to distill
  leaderboard/
    index.html           # Renders from data.json
    data.json            # Empty — updated by CI on merge
  submissions/
    .gitkeep             # PRs land here
  docs/
    research.md          # Prior art, novelty, risks
    business-model.md    # Revenue streams, unit economics
    data-capture.md      # Four-layer instrumentation spec
  .github/workflows/
    score.yml            # Score submissions on PR
    leaderboard.yml      # Rebuild leaderboard on merge
```

## Immediate Next Steps (User's Call)

1. **Submit proof-of-concept entries** — one human, one centaur on challenge 001 to prove the full PR→score→leaderboard loop
2. **Run LLM entries** — Claude, GPT-4, Gemini on both challenges as official baselines
3. **Soft launch** — HN, r/programming, r/LocalLLaMA, Cursor/Aider Discord
4. **Build session log CLI** (Layer 2) — the first step toward verifiable technique data
5. **Add 2-3 more challenges** — using the `CHALLENGE_SPEC.md` format

## Parent Repo

Arena concepts were extracted from `optimize_HUB` (`src/optimize_hub/query/_shared/economics.py`) but Arena has **zero dependency** on HUB. The repos are independent. HUB's `economics.py` stays in HUB — scoring concepts were simplified and adapted, not moved.
