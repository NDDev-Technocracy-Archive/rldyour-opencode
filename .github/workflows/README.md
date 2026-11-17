# GitHub Actions Workflows

Eleven workflows provide the public CI surface. Every workflow stays on
standard GitHub-hosted runners and third-party actions stay pinned to full SHAs.

## Shared source caller

The workflow-audit job in `validate.yml` declares the exact published
`NDDev-Technocracy-OpenNetwork/nddev-ci` revision. Its source recipe runs
`just audit-source`: offline workflow checks and the original PR-diff or
complete-history secret scope. The same declared release supplies merge stops
and the daily security report. The ordinary updater owns these pins.

`scripts/tests/test_shared_workflow_pin.py` rejects mixed source SHAs or
version comments and any retired provider. This checks source consistency;
actual release identity and native execution require their own CI evidence.

## Retained checks

| Workflow | Purpose |
| --- | --- |
| `validate.yml` | Static config/schema/MCP/index and source-unit validation, shell contract, shared source audit and merge stops. |
| `cross-platform.yml` | Ubuntu, Windows and macOS metadata/path smoke. |
| `instruction-docs-check.yml` | Instruction-document presence and drift. |
| `lint.yml` | Python maintenance-script lint. |
| `typecheck-plugins.yml` | Strict plugin TypeScript checks. |
| `opencode-runtime.yml` | Installed-runtime smoke, operator doctor report and live resolver tests; separately disabled. |
| `security.yml` | Retained CodeQL, dependency review and Scorecard. |
| `security-daily.yml` | Shared daily security report. |
| `dependency-check.yml` | Dependency and MCP freshness. |
| `sbom.yml` | Dependency SBOM evidence. |
| `release.yml` | Numeric-tag/manual release validation and publication. |

The static validate jobs retain their blocking validators and source-level
unit checks. Live resolver collection and the operator doctor report belong
to the separate runtime lane. JavaScript/TypeScript, Python and Actions retain
real CodeQL analysis. Application, SDK and lock selectors remain unchanged. Source checking
does not launch the runtime, MCP providers, browsers, model calls or installers.
The live/native checks remain independent requirements and are not qualified by
a source-only result. Artifacts retain their declared bounded lifetime.

## Cost policy

- Public CI uses standard GitHub-hosted runners only; no self-hosted, larger,
  runner-group, ARC, private-organization or paid-size labels.
- Keep the lightweight Ubuntu/Windows/macOS smoke workflow. Runtime-heavy and
  release jobs may remain Ubuntu-only when their tools require it.
- Artifact retention is explicit and at most 30 days.
- Path-filtered and scheduled jobs preserve the full declared coverage.

The shared source caller declares its actionlint, Zizmor and Betterleaks release
archives in `.github/ci-tools.json`. Archive and executable size/hash checks
prepare the hosted job without relying on an editor machine's installed tools.
