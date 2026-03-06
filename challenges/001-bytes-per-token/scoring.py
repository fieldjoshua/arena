#!/usr/bin/env python3
"""Auto-scorer for Challenge 001: Bytes-Per-Token Calibration.

Usage:
    python scoring.py path/to/solution.py

The solution module must define: estimate_tokens(text: str) -> int
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

BASELINE_MAE = 28.4  # From baseline_score.json
SAMPLES_PATH = Path(__file__).parent / "baseline" / "samples.json"
PAR_LINES = 30


def load_solution(path: str):
    """Import a solution module from a file path."""
    spec = importlib.util.spec_from_file_location("solution", path)
    if spec is None or spec.loader is None:
        print(f"Error: Cannot load {path}")
        sys.exit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "estimate_tokens"):
        print(f"Error: {path} must define estimate_tokens(text: str) -> int")
        sys.exit(1)
    return module


def score_against_samples(estimate_fn, samples: list[dict]) -> dict:
    """Score an estimator against reference samples."""
    errors = []
    baseline_errors = []
    results = []

    for sample in samples:
        text = sample["text"]
        actual = sample["tokens"]

        predicted = estimate_fn(text)
        baseline = len(text) // 4

        error = abs(predicted - actual)
        b_error = abs(baseline - actual)

        errors.append(error)
        baseline_errors.append(b_error)

        results.append({
            "id": sample["id"],
            "type": sample["type"],
            "actual": actual,
            "predicted": predicted,
            "baseline": baseline,
            "error": error,
            "baseline_error": b_error,
        })

    mae = sum(errors) / len(errors)
    baseline_mae = sum(baseline_errors) / len(baseline_errors)

    # Correctness: how much better than baseline (0-100)
    if baseline_mae > 0:
        improvement = 1.0 - mae / baseline_mae
        correctness = max(0.0, min(100.0, improvement * 100.0))
    else:
        correctness = 100.0 if mae == 0 else 0.0

    return {
        "mae": round(mae, 1),
        "baseline_mae": round(baseline_mae, 1),
        "improvement_pct": round((1.0 - mae / max(baseline_mae, 1)) * 100, 1),
        "correctness_score": round(correctness, 1),
        "per_sample": results,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python scoring.py path/to/solution.py")
        sys.exit(1)

    solution_path = sys.argv[1]
    module = load_solution(solution_path)

    samples = json.loads(SAMPLES_PATH.read_text())
    result = score_against_samples(module.estimate_tokens, samples)

    print(f"\n{'=' * 60}")
    print(f"  Challenge 001: Bytes-Per-Token Calibration")
    print(f"{'=' * 60}")
    print(f"  Your MAE:      {result['mae']:.1f} tokens")
    print(f"  Baseline MAE:  {result['baseline_mae']:.1f} tokens")
    print(f"  Improvement:   {result['improvement_pct']:+.1f}%")
    print(f"  Correctness:   {result['correctness_score']:.1f}/100")
    print(f"{'=' * 60}")

    print(f"\n  Per-sample breakdown:")
    print(f"  {'ID':<25} {'Type':<8} {'Actual':>6} {'Yours':>6} {'Base':>6} {'Err':>5} {'BErr':>5}")
    print(f"  {'-'*25} {'-'*8} {'-'*6} {'-'*6} {'-'*6} {'-'*5} {'-'*5}")
    for r in result["per_sample"]:
        print(
            f"  {r['id']:<25} {r['type']:<8} {r['actual']:>6} "
            f"{r['predicted']:>6} {r['baseline']:>6} {r['error']:>5} {r['baseline_error']:>5}"
        )

    # Write results for CI
    output_path = Path(solution_path).parent / "results.json"
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print(f"\n  Results written to {output_path}")


if __name__ == "__main__":
    main()
