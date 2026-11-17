set shell := ["bash", "-euo", "pipefail", "-c"]
set positional-arguments

# List the maintained workflow-source commands.
default:
    @just --list

# Check workflow/command source offline; native validators retain their own jobs.
check:
    just --fmt --check
    actionlint
    zizmor --offline --no-progress .github

# Retain exact PR-diff or complete-history source secret scope.
audit-source scope="--all": check
    betterleaks git --no-banner --redact "--log-opts=$1" .

# Format only the owned command source.
fix:
    just --fmt
