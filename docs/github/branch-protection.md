# Branch protection

The current source contract is `.github/branch-protection/main.json`. Its
required names and producer ID were read from completed GitHub check runs.
Workflow titles do not determine check-run names, and a static workflow
inventory is not evidence that a context exists or is required.

The contract keeps every unconditional native/static/unit/platform/security
check. It covers validation, source-level unit tests, shell rules, plugin
typechecking, lint, instruction docs, three-platform metadata smoke,
JavaScript/TypeScript, Python and Actions CodeQL, dependency review, shared
source auditing and merge stops. All listed contexts use GitHub Actions.

Read the exact contract without reconstructing names:

```bash
bash scripts/print_required_check_contexts.sh
bash scripts/print_required_check_contexts.sh --json
```

After changing a workflow, compare the actual exact-head GitHub check runs and
producer IDs with this file. Update the contract from observed runs, then
reconcile live protection. The reader validates names and prints the contract;
it does not query GitHub, change settings or prove the live state.

Main requires a pull request, strict checks and merge commits. Approvals and
code-owner review are zero, linear history is off, force/deletion are disabled,
and administrator bypass is absent. Repository auto-merge is available only
behind the complete active requirements.

Scorecard and daily reporting remain outside unconditional pull-request
requirements. Path-filtered jobs must be excluded if their filters can prevent
a report. Dependency probes, the explicit runtime/doctor/live-resolver lane,
release and SBOM operators are separately disabled during source-only
maintenance; their unperformed runtime behavior is not source qualification.

Inspect live state with the current repository identity:

```bash
gh api repos/NDDev-Technocracy-Archive/rldyour-opencode/rules/branches/main
gh api repos/NDDev-Technocracy-Archive/rldyour-opencode/rulesets
```

An administrator restores the complete reviewed policy through repository
rulesets or branch protection and verifies it independently by GET. The source
file describes intent; the API response proves enforcement.
