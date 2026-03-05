"""Subagent test runner — spawns Claude subagents at different model tiers.

Maps test files to model tiers per orchestrator.md Model Selection rules:
- Haiku: mechanical tasks, clear instructions, fully specified patterns
- Sonnet: moderate judgment, context awareness, multi-step reasoning
- Opus: deep reasoning, architectural decisions, ambiguous requirements

Each subagent receives a test file, runs pytest, and reports results.
"""

import os
import sys
import json
import subprocess
import anthropic

# Model tier mapping per orchestrator.md (lines 200-219)
MODEL_TIERS = {
    "haiku": "claude-haiku-4-5",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-6",
}

# Test files mapped to model tiers with rationale
TEST_ASSIGNMENTS = [
    {
        "file": "tests/test_parser.py",
        "tier": "haiku",
        "rationale": "Pure input-output assertions, fully specified patterns",
    },
    {
        "file": "tests/test_templates.py",
        "tier": "sonnet",
        "rationale": "Template parsing with includes/conditionals requires moderate judgment",
    },
    {
        "file": "tests/test_builder.py",
        "tier": "sonnet",
        "rationale": "Integration logic across parser/templates/filesystem, context-aware",
    },
    {
        "file": "tests/test_cli.py",
        "tier": "haiku",
        "rationale": "Thin dispatch layer, mechanical exit-code checks",
    },
]

SYSTEM_PROMPT = """You are a test-running subagent for Rogue Guardian Studios.
Your job is to analyze a pytest test file and its test results, then report:
1. Total tests, passed, failed
2. Any failures with brief explanation
3. A one-line verdict: PASS or FAIL

Be concise. No preamble."""


def run_pytest(test_file: str) -> str:
    """Run pytest on a single test file and capture output."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    return result.stdout + result.stderr


def run_subagent(client: anthropic.Anthropic, assignment: dict) -> dict:
    """Spawn a subagent at the assigned model tier to analyze test results."""
    test_file = assignment["file"]
    tier = assignment["tier"]
    model = MODEL_TIERS[tier]

    # Run pytest first to get actual results
    pytest_output = run_pytest(test_file)

    # Read the test file content
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_file)
    with open(test_path) as f:
        test_source = f.read()

    user_message = (
        f"Test file: {test_file}\n"
        f"Model tier: {tier} ({model})\n"
        f"Assignment rationale: {assignment['rationale']}\n\n"
        f"--- Test Source ---\n{test_source}\n\n"
        f"--- Pytest Output ---\n{pytest_output}\n\n"
        f"Analyze the results and give your verdict."
    )

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    response_text = response.content[0].text

    return {
        "file": test_file,
        "tier": tier,
        "model": model,
        "rationale": assignment["rationale"],
        "response": response_text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=" * 60)
        print("RGS Subagent Test Runner — DRY RUN")
        print("Showing model routing without API calls")
        print("=" * 60)
        for assignment in TEST_ASSIGNMENTS:
            tier = assignment["tier"]
            model = MODEL_TIERS[tier]
            print(f"\n[{tier.upper()}] {model} -> {assignment['file']}")
            print(f"  Rationale: {assignment['rationale']}")
            pytest_output = run_pytest(assignment["file"])
            passed = pytest_output.count(" PASSED")
            failed = pytest_output.count(" FAILED")
            print(f"  Pytest: {passed} passed, {failed} failed")
        print("\nDry run complete. Run without --dry-run to call the API.")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("=" * 60)
    print("RGS Subagent Test Runner")
    print("Spawning subagents at different model tiers")
    print("=" * 60)

    results = []
    for assignment in TEST_ASSIGNMENTS:
        tier = assignment["tier"]
        model = MODEL_TIERS[tier]
        print(f"\n[{tier.upper()}] {model} -> {assignment['file']}")
        print(f"  Rationale: {assignment['rationale']}")

        try:
            result = run_subagent(client, assignment)
            results.append(result)
            print(f"  Tokens: {result['input_tokens']} in / {result['output_tokens']} out")
            print(f"  Response:\n    {result['response'].replace(chr(10), chr(10) + '    ')}")
        except anthropic.APIError as e:
            print(f"  ERROR: {e}")
            results.append({
                "file": assignment["file"],
                "tier": tier,
                "model": model,
                "error": str(e),
            })

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for r in results:
        status = "ERROR" if "error" in r else "OK"
        print(f"  [{r['tier'].upper():6s}] {r['model']:25s} {r['file']:30s} {status}")

    # Cost estimate
    total_input = sum(r.get("input_tokens", 0) for r in results)
    total_output = sum(r.get("output_tokens", 0) for r in results)
    # Rough cost calc using per-token rates
    cost = 0
    for r in results:
        if "error" in r:
            continue
        tier = r["tier"]
        inp = r["input_tokens"]
        out = r["output_tokens"]
        if tier == "haiku":
            cost += inp * 1.0 / 1_000_000 + out * 5.0 / 1_000_000
        elif tier == "sonnet":
            cost += inp * 3.0 / 1_000_000 + out * 15.0 / 1_000_000
        elif tier == "opus":
            cost += inp * 5.0 / 1_000_000 + out * 25.0 / 1_000_000

    print(f"\n  Total tokens: {total_input} in / {total_output} out")
    print(f"  Estimated cost: ${cost:.4f}")


if __name__ == "__main__":
    main()
