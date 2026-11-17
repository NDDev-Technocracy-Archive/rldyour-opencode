set shell := ["bash", "-euo", "pipefail", "-c"]
set positional-arguments

# List the maintained workflow-source commands.
default:
    @just --list

# Check workflow/command source offline; native validators retain their own jobs.
check:
    just --fmt --check
    actionlint
    zizmor --offline --no-progress .github/workflows/validate.yml .github/workflows/cross-platform.yml .github/workflows/dependency-check.yml .github/workflows/instruction-docs-check.yml .github/workflows/lint.yml .github/workflows/opencode-runtime.yml .github/workflows/typecheck-plugins.yml .github/workflows/security.yml .github/workflows/security-daily.yml .github/dependabot.yml

# Retain exact PR-diff or complete-history source secret scope.
audit-source scope="--all": check
    betterleaks git --no-banner --redact "--log-opts=$1" .

# Format only the owned command source.
fix:
    just --fmt
