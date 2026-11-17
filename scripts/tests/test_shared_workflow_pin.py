from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
WORKFLOW_DOC = WORKFLOWS / "README.md"
SHARED_REPO = "NDDev-Technocracy-OpenNetwork/nddev-ci"
PIN_RE = re.compile(
    rf"^\s*(?:-\s*)?uses:\s*{re.escape(SHARED_REPO)}/[^@\s]+@"
    r"(?P<sha>[0-9a-f]{40})\s+#\s*(?P<version>v\d+\.\d+\.\d+)\s*$"
)


def test_all_shared_workflow_callers_use_one_declared_release() -> None:
    callers: list[tuple[Path, int, str]] = []
    for path in sorted(WORKFLOWS.glob("*.yml")):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            assert "NDDev-Technocracy-Standarts/std-0004-ci-cd-workflows/" not in line
            if f"{SHARED_REPO}/" in line:
                callers.append((path, line_number, line))

    assert callers, "no shared CI callers found"
    anchor = next(
        PIN_RE.fullmatch(line)
        for path, _number, line in callers
        if path.name == "validate.yml" and "/recipe.yml@" in line
    )
    assert anchor is not None, "validate.yml must declare an exact release"
    expected = anchor.group("sha", "version")
    drift = []
    for path, line_number, line in callers:
        pin = PIN_RE.fullmatch(line)
        if pin is None or pin.group("sha", "version") != expected:
            drift.append(f"{path.relative_to(ROOT)}:{line_number}: {line.strip()}")
    assert not drift, "shared workflow source drift:\n" + "\n".join(drift)


def test_shared_workflow_source_is_documented() -> None:
    text = WORKFLOW_DOC.read_text(encoding="utf-8")
    assert "validate.yml" in text and SHARED_REPO in text
    assert "actual release identity and native execution" in text
