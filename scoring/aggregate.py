"""Leaderboard aggregation — reads scored submissions, builds leaderboard data."""

from __future__ import annotations

import json
from pathlib import Path


def build_leaderboard(submissions_dir: Path) -> dict:
    """Scan all scored submissions and build leaderboard data.

    Expects each submission at:
        submissions/<challenge-id>/<handle>/results.json

    Where results.json is the output of scoring/technique.py:score_submission().

    Returns:
        Dict with per-challenge and overall leaderboards.
    """
    challenges: dict[str, list[dict]] = {}

    if not submissions_dir.exists():
        return {"challenges": {}, "overall": []}

    for challenge_dir in sorted(submissions_dir.iterdir()):
        if not challenge_dir.is_dir() or challenge_dir.name.startswith("."):
            continue

        challenge_id = challenge_dir.name
        entries = []

        for handle_dir in sorted(challenge_dir.iterdir()):
            if not handle_dir.is_dir():
                continue

            results_path = handle_dir / "results.json"
            if not results_path.exists():
                continue

            try:
                result = json.loads(results_path.read_text())
                result["handle"] = handle_dir.name
                result["challenge"] = challenge_id
                entries.append(result)
            except (json.JSONDecodeError, KeyError):
                continue

        # Sort by composite score descending
        entries.sort(key=lambda x: -x.get("composite", 0))

        # Assign ranks
        for i, entry in enumerate(entries, 1):
            entry["rank"] = i

        challenges[challenge_id] = entries

    # Overall: average composite across all challenges per handle
    handle_scores: dict[str, list[float]] = {}
    for entries in challenges.values():
        for entry in entries:
            handle = entry["handle"]
            handle_scores.setdefault(handle, []).append(entry.get("composite", 0))

    overall = []
    for handle, scores in handle_scores.items():
        avg = sum(scores) / len(scores)
        overall.append({
            "handle": handle,
            "challenges_attempted": len(scores),
            "avg_composite": round(avg, 1),
        })

    overall.sort(key=lambda x: -x["avg_composite"])
    for i, entry in enumerate(overall, 1):
        entry["rank"] = i

    return {"challenges": challenges, "overall": overall}


def write_leaderboard(submissions_dir: Path, output_path: Path) -> None:
    """Build and write leaderboard JSON."""
    data = build_leaderboard(submissions_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    import sys

    repo_root = Path(__file__).parent.parent
    submissions = repo_root / "submissions"
    output = repo_root / "leaderboard" / "data.json"

    write_leaderboard(submissions, output)
    print(f"Leaderboard written to {output}")
    data = json.loads(output.read_text())
    total = sum(len(v) for v in data["challenges"].values())
    print(f"  {len(data['challenges'])} challenges, {total} entries")
