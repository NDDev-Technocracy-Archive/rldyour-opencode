"""The required-context reader prints the observed policy, without name prediction."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "print_required_check_contexts.sh"
POLICY = ROOT / ".github" / "branch-protection" / "main.json"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def test_text_mode_prints_the_policy() -> None:
    result = run()
    assert result.returncode == 0, result.stderr
    assert "REQUIRED CHECK CONTEXT (APP)" in result.stdout
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    for context in policy["required_status_checks"]:
        assert f"{context} ({policy['required_status_check_app_id']})" in result.stdout


def test_json_mode_preserves_exact_names_and_producer() -> None:
    result = run("--json")
    assert result.returncode == 0, result.stderr
    actual = json.loads(result.stdout)
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    assert actual == {
        "count": len(policy["required_status_checks"]),
        "contexts": [
            {"context": name, "integration_id": policy["required_status_check_app_id"]}
            for name in policy["required_status_checks"]
        ],
    }


def test_reader_does_not_invent_a_workflow_prefix(tmp_path: Path) -> None:
    path = tmp_path / "policy.json"
    path.write_text(json.dumps({
        "required_status_checks": ["validate (custom-os)", "caller / nested job"],
        "required_status_check_app_id": 123,
    }), encoding="utf-8")
    result = run("--json", "--policy", str(path))
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["contexts"] == [
        {"context": "validate (custom-os)", "integration_id": 123},
        {"context": "caller / nested job", "integration_id": 123},
    ]


def test_duplicate_required_context_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "policy.json"
    path.write_text(json.dumps({
        "required_status_checks": ["check", "check"],
        "required_status_check_app_id": 15368,
    }), encoding="utf-8")
    result = run("--policy", str(path))
    assert result.returncode == 2
    assert "duplicate required context" in result.stderr
    assert "Traceback" not in result.stderr


def test_missing_contract_is_an_operational_error(tmp_path: Path) -> None:
    result = run("--policy", str(tmp_path / "missing.json"))
    assert result.returncode == 2
    assert "[ERR] invalid check contract" in result.stderr
    assert "Traceback" not in result.stderr
