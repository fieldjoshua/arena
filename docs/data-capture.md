# Arena Data Capture: Full Workflow Instrumentation

## Vision

Arena doesn't just score solutions — it captures the complete human+AI
problem-solving workflow. Keystrokes, eye movements, AI interactions,
decision points. The richest dataset of human-directed AI engineering
ever collected.

The competition is the funnel. The data is the product.

## Data Layers

### Layer 1: Technique Signature (v0 — live now)

Self-reported YAML/JSON. Honor system.

```yaml
category: centaur
tools_used: [cursor, claude-sonnet-4-5]
tokens_consumed: 14200
api_cost_usd: 0.43
human_iterations: 7
wall_seconds: 847
lines_changed: 32
notes: "Rewrote the diff algorithm after first LLM attempt failed test 3"
```

**Status:** Shipping now. Minimum viable technique data.

### Layer 2: Session Log (v0.5)

Structured, machine-readable log of the AI interaction sequence.

```yaml
session:
  start: "2026-03-06T14:30:00Z"
  end: "2026-03-06T15:01:47Z"

interactions:
  - timestamp: "2026-03-06T14:30:12Z"
    type: prompt
    tool: claude-code
    model: claude-sonnet-4-5
    tokens_in: 2400
    tokens_out: 850
    human_edit_after: true     # did human modify the output?
    accepted: partial          # full | partial | rejected

  - timestamp: "2026-03-06T14:32:45Z"
    type: prompt
    tool: claude-code
    model: claude-sonnet-4-5
    tokens_in: 3100
    tokens_out: 1200
    human_edit_after: false
    accepted: full

decisions:
  - timestamp: "2026-03-06T14:35:00Z"
    description: "Switched from regex approach to AST parsing"
    trigger: "LLM regex solution failed edge case in test 3"

  - timestamp: "2026-03-06T14:48:00Z"
    description: "Manually wrote the boundary check — LLM kept getting it wrong"
    trigger: "Three failed attempts at the off-by-one case"
```

**Captures:** AI interaction sequence, acceptance/rejection patterns,
human decision points, tool-switching moments.

**Implementation:** CLI tool or IDE extension that watches AI tool
API calls and prompts the user to annotate decisions.

### Layer 3: Keystroke & Editor Telemetry (v1)

Full keystroke stream with timing, editor events, file navigation.

```json
{
  "events": [
    {"t": 0, "type": "file_open", "file": "solution.py"},
    {"t": 1200, "type": "keystroke", "key": "d", "mod": []},
    {"t": 1240, "type": "keystroke", "key": "e", "mod": []},
    {"t": 1280, "type": "keystroke", "key": "f", "mod": []},
    {"t": 3400, "type": "paste", "chars": 245, "source": "ai_completion"},
    {"t": 3600, "type": "select", "lines": [12, 18]},
    {"t": 3800, "type": "delete", "chars": 87},
    {"t": 5200, "type": "file_switch", "from": "solution.py", "to": "test.py"},
    {"t": 8900, "type": "terminal_cmd", "cmd": "python scoring.py solution.py"},
    {"t": 12400, "type": "undo", "count": 3},
    {"t": 15000, "type": "ai_prompt", "tool": "cursor", "chars": 120}
  ]
}
```

**Captures:** Typing speed, edit patterns, undo frequency, paste-from-AI
vs manual typing ratio, file navigation paths, terminal usage, search
queries. This is the "technique path" made concrete.

**Key metrics derivable:**
- Human typing vs AI paste ratio
- Edit-after-paste rate (how much do you modify AI output?)
- Undo frequency (false starts, direction changes)
- File switching pattern (breadth vs depth exploration)
- Time-to-first-edit after AI completion (reading/thinking time)
- Terminal test cycle frequency

**Implementation:** VS Code / Cursor extension. Lightweight — logs
events to a local JSONL file, submitted with the solution. No
network calls during the session. All data stays local until
the competitor explicitly submits it.

### Layer 4: Visual & Biometric (v2)

Eye tracking, screen recording, body posture, cognitive load signals.

#### Eye Tracking

```json
{
  "eye_events": [
    {"t": 0, "type": "fixation", "x": 420, "y": 180, "duration_ms": 340, "target": "code_line_12"},
    {"t": 500, "type": "saccade", "from": [420, 180], "to": [100, 340]},
    {"t": 850, "type": "fixation", "x": 100, "y": 340, "duration_ms": 1200, "target": "ai_output"},
    {"t": 2100, "type": "fixation", "x": 600, "y": 90, "duration_ms": 200, "target": "file_tab"},
    {"t": 4500, "type": "regression", "from": "line_25", "to": "line_8"}
  ],
  "gaze_summary": {
    "time_on_own_code_pct": 35,
    "time_on_ai_output_pct": 40,
    "time_on_problem_spec_pct": 20,
    "time_on_other_pct": 5,
    "avg_fixation_ms": 280,
    "regression_count": 12
  }
}
```

**Key metrics derivable:**
- Time spent reading AI output vs writing own code
- Regression patterns (re-reading = confusion or verification?)
- Problem spec consultation frequency
- Code review depth (line-by-line fixations vs skimming)
- Cognitive load proxy (pupil dilation if hardware supports it)

**Hardware:** WebGazer.js (webcam-based, ~50px accuracy, free) for v2.
Tobii/EyeLink integration for research-grade data in v3.

#### Screen Recording

- Hashed screen recording (SHA256 committed with solution)
- Reviewable on dispute or for research
- Captures everything the other layers might miss
- Privacy: competitor controls the recording, decides what to submit

#### Body/Posture (Research Track)

- Webcam-based posture estimation (MediaPipe)
- Lean-in moments (engagement/focus)
- Lean-back moments (thinking/planning)
- Head movements (looking away = thinking vs distraction)
- This is research-grade — optional track for participants who opt in

## Data Schema (Unified)

All layers feed into a single submission record:

```json
{
  "submission_id": "001-joshfield-2026-03-06",
  "challenge_id": "001",
  "handle": "joshfield",
  "timestamp": "2026-03-06T15:01:47Z",

  "solution": {
    "files": ["solution.py"],
    "lines_changed": 32,
    "correctness_pct": 92.5
  },

  "technique": {
    "category": "centaur",
    "tools_used": ["cursor", "claude-sonnet-4-5"],
    "tokens_consumed": 14200,
    "api_cost_usd": 0.43,
    "wall_seconds": 1897,
    "human_iterations": 7
  },

  "session_log": { "...": "Layer 2 data" },
  "keystrokes": { "...": "Layer 3 data" },
  "eye_tracking": { "...": "Layer 4 data" },
  "screen_hash": "sha256:abc123...",

  "scores": {
    "correctness": 92.5,
    "token_efficiency": 85.8,
    "speed": 78.0,
    "solution_size": 100.0,
    "cost_efficiency": 95.7,
    "composite": 89.2
  },

  "derived_metrics": {
    "human_typing_ratio": 0.35,
    "ai_paste_edit_rate": 0.62,
    "undo_frequency": 0.08,
    "time_reading_ai_output_pct": 40,
    "decision_points": 3,
    "tool_switches": 2
  }
}
```

## Privacy & Consent

- **All data capture is opt-in per layer.** Layer 1 (technique.json) is
  required for scoring. Layers 2-4 are optional — more data = richer
  leaderboard profile, but not required to compete.
- **All data stays local until submission.** No telemetry during the session.
  The competitor reviews their data before committing it.
- **Competitors own their data.** They can request deletion at any time.
  Submitted data is licensed for platform use (leaderboard, research)
  under terms accepted at registration.
- **Biometric data (Layer 4) requires explicit separate consent** and is
  only used in aggregate for research. Individual biometric data is never
  displayed publicly.
- **Data licensing to third parties (AI labs, researchers) uses anonymized
  aggregate data only.** Individual session replays require the competitor's
  explicit permission.

## Implementation Roadmap

| Layer | Version | Effort | Data Richness |
|-------|---------|--------|---------------|
| 1: Technique signature | v0 (now) | Done | Basic |
| 2: Session log | v0.5 | CLI tool, ~1 week | Interaction sequence |
| 3: Keystrokes + editor | v1 | VS Code extension, ~3 weeks | Full workflow |
| 4: Eye + screen + body | v2 | WebGazer + MediaPipe, ~6 weeks | Complete |

## Research Value

This dataset doesn't exist anywhere. No one has:
- Keystroke-level recordings of human+AI collaborative coding
- Eye tracking data showing how engineers read AI-generated code
- Structured decision logs of when humans override AI suggestions
- Comparative efficiency data across different AI tool combinations
- All of the above, on identical problems, from multiple participants

The closest analogs are:
- Keystroke logging in CS education research (no AI component)
- OpenAI process reward models (LLM-only, no human)
- Screen recording studies of pair programming (no AI, small N)

Arena produces this data as a byproduct of competition. The gamification
solves the recruitment problem that kills most research studies.
