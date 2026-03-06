"""Technique signature and scoring for Arena submissions.

Extracted and simplified from HUB's economics.py concept —
technique signatures track the full solution path, not just the outcome.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TechniqueSignature:
    """Describes HOW a solution was produced."""

    category: str  # "human" | "llm" | "centaur"
    tools_used: list[str] = field(default_factory=list)
    tokens_consumed: int = 0
    wall_seconds: int = 0
    lines_changed: int = 0
    api_cost_usd: float = 0.0
    human_iterations: int = 0
    notes: str = ""

    def __post_init__(self) -> None:
        if self.category not in ("human", "llm", "centaur"):
            raise ValueError(f"Invalid category: {self.category!r}. Must be human, llm, or centaur.")
        if self.category == "human" and self.tokens_consumed > 0:
            raise ValueError("Human submissions must have tokens_consumed = 0.")
        if self.tokens_consumed < 0:
            raise ValueError("tokens_consumed cannot be negative.")
        if self.wall_seconds < 0:
            raise ValueError("wall_seconds cannot be negative.")
        if self.lines_changed < 0:
            raise ValueError("lines_changed cannot be negative.")

    @property
    def efficiency_ratio(self) -> float:
        """Tokens consumed per line of output. Lower = more efficient."""
        if self.tokens_consumed == 0:
            return 0.0
        return self.tokens_consumed / max(self.lines_changed, 1)

    @classmethod
    def from_json(cls, path: Path) -> TechniqueSignature:
        """Load from a technique.json file."""
        data = json.loads(path.read_text())
        return cls(
            category=data["category"],
            tools_used=data.get("tools_used", []),
            tokens_consumed=data.get("tokens_consumed", 0),
            wall_seconds=data.get("wall_seconds", 0),
            lines_changed=data.get("lines_changed", 0),
            api_cost_usd=data.get("api_cost_usd", 0.0),
            human_iterations=data.get("human_iterations", 0),
            notes=data.get("notes", ""),
        )

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "tools_used": self.tools_used,
            "tokens_consumed": self.tokens_consumed,
            "wall_seconds": self.wall_seconds,
            "lines_changed": self.lines_changed,
            "api_cost_usd": self.api_cost_usd,
            "human_iterations": self.human_iterations,
            "notes": self.notes,
            "efficiency_ratio": round(self.efficiency_ratio, 1),
        }


def score_submission(
    correctness_pct: float,
    technique: TechniqueSignature,
    challenge_max_tokens: int = 100_000,
    challenge_par_lines: int = 50,
    challenge_median_seconds: int = 3600,
    challenge_median_cost: float = 1.0,
) -> dict:
    """Compute composite score for a submission.

    Weights: correctness 40%, token efficiency 20%, speed 20%,
    solution size 10%, cost efficiency 10%.

    Technique signatures (tools, iterations) are included in output
    but do not affect the composite score (display-only in v0).
    """
    # Correctness (40%)
    correctness = max(0.0, min(100.0, correctness_pct))

    # Token efficiency (20%) — fewer tokens = better
    if challenge_max_tokens > 0 and technique.tokens_consumed > 0:
        token_efficiency = 100.0 * (1.0 - technique.tokens_consumed / challenge_max_tokens)
        token_efficiency = max(0.0, min(100.0, token_efficiency))
    else:
        token_efficiency = 100.0  # human-only or no token data

    # Speed (20%) — faster = better
    if technique.wall_seconds <= 0:
        speed = 50.0  # no data
    elif technique.wall_seconds <= challenge_median_seconds:
        speed = 100.0
    else:
        over = technique.wall_seconds - challenge_median_seconds
        speed = max(0.0, 100.0 - (over / challenge_median_seconds) * 100.0)

    # Solution size (10%) — fewer lines = better
    if technique.lines_changed <= challenge_par_lines:
        solution_size = 100.0
    else:
        over = technique.lines_changed - challenge_par_lines
        solution_size = max(0.0, 100.0 - (over / challenge_par_lines) * 100.0)

    # Cost efficiency (10%) — lower API cost = better
    if technique.api_cost_usd <= 0:
        cost_efficiency = 100.0  # human-only or not reported
    elif challenge_median_cost > 0:
        if technique.api_cost_usd <= challenge_median_cost:
            cost_efficiency = 100.0
        else:
            over = technique.api_cost_usd - challenge_median_cost
            cost_efficiency = max(0.0, 100.0 - (over / challenge_median_cost) * 100.0)
    else:
        cost_efficiency = 50.0

    composite = (
        correctness * 0.40
        + token_efficiency * 0.20
        + speed * 0.20
        + solution_size * 0.10
        + cost_efficiency * 0.10
    )

    return {
        "correctness": round(correctness, 1),
        "token_efficiency": round(token_efficiency, 1),
        "speed": round(speed, 1),
        "solution_size": round(solution_size, 1),
        "cost_efficiency": round(cost_efficiency, 1),
        "composite": round(composite, 1),
        "technique": technique.to_dict(),
    }
