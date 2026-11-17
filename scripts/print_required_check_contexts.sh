#!/usr/bin/env bash
# Print the observed protected-branch context contract without guessing workflow names.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 - "$PROJECT_ROOT/.github/branch-protection/main.json" "$@" <<'PY_CONTEXTS'
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description="Print the protected-branch check contract.")
parser.add_argument("default_policy", type=Path)
parser.add_argument("--json", action="store_true")
parser.add_argument("--policy", type=Path)
args = parser.parse_args()
try:
    policy = json.loads((args.policy or args.default_policy).read_text(encoding="utf-8"))
    names = policy["required_status_checks"]
    app_id = policy["required_status_check_app_id"]
    if not isinstance(names, list) or not names:
        raise ValueError("required_status_checks must be a non-empty list")
    if type(app_id) is not int or app_id <= 0:
        raise ValueError("required_status_check_app_id must be a positive integer")
    if any(
        not isinstance(name, str)
        or not name
        or name != name.strip()
        or any(character in name for character in "\n\r\t\0")
        for name in names
    ):
        raise ValueError("each required context must be one explicit non-empty line")
    if len(set(names)) != len(names):
        raise ValueError("duplicate required context")
except (OSError, ValueError, KeyError, TypeError) as error:
    print(f"[ERR] invalid check contract: {error}", file=sys.stderr)
    raise SystemExit(2) from None

entries = [{"context": name, "integration_id": app_id} for name in names]
if args.json:
    print(json.dumps({"count": len(entries), "contexts": entries}, indent=2))
else:
    print("REQUIRED CHECK CONTEXT (APP)")
    for entry in entries:
        print(f"{entry['context']} ({entry['integration_id']})")
PY_CONTEXTS
