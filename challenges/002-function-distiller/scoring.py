#!/usr/bin/env python3
"""Auto-scorer for Challenge 002: Function Distiller.

Usage:
    python scoring.py path/to/distillates/ [--dry-run]

Expects distillate_001.md through distillate_005.md in the given directory.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

FUNCTIONS_DIR = Path(__file__).parent / "starter"
NUM_FUNCTIONS = 5
MAX_TOKENS_PER_DISTILLATE = 500

# Rough token estimate (no external deps)
def _estimate_tokens(text: str) -> int:
    """Rough token count: words * 1.3 (accounts for subword tokenization)."""
    return max(1, int(len(text.split()) * 1.3))


def _check_verbatim_copy(distillate: str, source: str, threshold: float = 0.5) -> bool:
    """Check if distillate contains >threshold fraction of source lines verbatim."""
    source_lines = {line.strip() for line in source.splitlines() if len(line.strip()) > 10}
    if not source_lines:
        return False
    distillate_lines = {line.strip() for line in distillate.splitlines() if len(line.strip()) > 10}
    overlap = len(source_lines & distillate_lines)
    return overlap / len(source_lines) > threshold


def _judge_distillate_dry_run(distillate: str, source: str) -> dict:
    """Dry-run judge: checks format and token count only."""
    tokens = _estimate_tokens(distillate)
    return {
        "completeness": "N/A (dry-run)",
        "compression": "N/A (dry-run)",
        "tokens": tokens,
        "within_limit": tokens <= MAX_TOKENS_PER_DISTILLATE,
    }


def _judge_distillate_llm(distillate: str, source: str) -> dict:
    """Use LLM to judge distillate quality. Requires OPENROUTER_API_KEY."""
    try:
        import urllib.request
    except ImportError:
        return {"error": "urllib not available"}

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return {"error": "OPENROUTER_API_KEY not set. Use --dry-run for format check only."}

    prompt = f"""You are judging a code distillate. Rate it on two axes:

COMPLETENESS (0-10): Could someone reconstruct the original function from just this distillate?
10 = perfect reconstruction possible, 0 = useless.

COMPRESSION (0-10): How efficiently was information packed?
10 = remarkable density, every token carries meaning. 0 = longer than the original.

ORIGINAL FUNCTION:
```python
{source}
```

DISTILLATE:
{distillate}

Respond with ONLY a JSON object: {{"completeness": <0-10>, "compression": <0-10>, "reasoning": "<1 sentence>"}}"""

    body = json.dumps({
        "model": "google/gemini-flash-1.5",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }).encode()

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        content = data["choices"][0]["message"]["content"]
        # Extract JSON from response
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(content[start:end])
            result["tokens"] = _estimate_tokens(distillate)
            return result
        return {"error": f"Could not parse judge response: {content[:200]}"}
    except Exception as e:
        return {"error": str(e)}


def score_distillates(distillates_dir: Path, dry_run: bool = False) -> dict:
    """Score all distillates in a directory."""
    results = []

    for i in range(1, NUM_FUNCTIONS + 1):
        func_id = f"{i:03d}"
        distillate_path = distillates_dir / f"distillate_{func_id}.md"
        source_path = FUNCTIONS_DIR / f"function_{func_id}.py"

        if not distillate_path.exists():
            results.append({"function": func_id, "error": f"Missing {distillate_path.name}"})
            continue

        if not source_path.exists():
            results.append({"function": func_id, "error": f"Missing source {source_path.name}"})
            continue

        distillate = distillate_path.read_text()
        source = source_path.read_text()

        # Check constraints
        tokens = _estimate_tokens(distillate)
        if tokens > MAX_TOKENS_PER_DISTILLATE:
            results.append({
                "function": func_id,
                "error": f"Exceeds token limit: {tokens} > {MAX_TOKENS_PER_DISTILLATE}",
            })
            continue

        if _check_verbatim_copy(distillate, source):
            results.append({
                "function": func_id,
                "error": "Too much verbatim copying from source (>50%)",
            })
            continue

        # Judge
        if dry_run:
            judge_result = _judge_distillate_dry_run(distillate, source)
        else:
            judge_result = _judge_distillate_llm(distillate, source)

        judge_result["function"] = func_id
        results.append(judge_result)

    # Compute aggregate score
    scored = [r for r in results if "completeness" in r and isinstance(r["completeness"], (int, float))]
    if scored:
        avg_completeness = sum(r["completeness"] for r in scored) / len(scored)
        avg_compression = sum(r["compression"] for r in scored) / len(scored)
        challenge_score = (avg_completeness * 0.6 + avg_compression * 0.4) * 10  # scale to 0-100
    else:
        avg_completeness = 0
        avg_compression = 0
        challenge_score = 0

    return {
        "per_function": results,
        "avg_completeness": round(avg_completeness, 1),
        "avg_compression": round(avg_compression, 1),
        "correctness_score": round(challenge_score, 1),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python scoring.py path/to/distillates/ [--dry-run]")
        sys.exit(1)

    distillates_dir = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv

    if not distillates_dir.is_dir():
        print(f"Error: {distillates_dir} is not a directory")
        sys.exit(1)

    result = score_distillates(distillates_dir, dry_run=dry_run)

    print(f"\n{'=' * 60}")
    print(f"  Challenge 002: Function Distiller {'(DRY RUN)' if dry_run else ''}")
    print(f"{'=' * 60}")

    for r in result["per_function"]:
        func_id = r.get("function", "???")
        if "error" in r:
            print(f"  Function {func_id}: ERROR - {r['error']}")
        elif dry_run:
            status = "OK" if r.get("within_limit") else "OVER LIMIT"
            print(f"  Function {func_id}: {r['tokens']} tokens [{status}]")
        else:
            print(f"  Function {func_id}: completeness={r.get('completeness')}/10, "
                  f"compression={r.get('compression')}/10")

    print(f"\n  Challenge Score: {result['correctness_score']:.1f}/100")
    print(f"{'=' * 60}")

    # Write results
    output_path = distillates_dir / "results.json"
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print(f"\n  Results written to {output_path}")


if __name__ == "__main__":
    main()
