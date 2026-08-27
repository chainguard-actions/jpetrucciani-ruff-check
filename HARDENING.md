<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.16.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.16.5** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Workflow files reference actions by mutable version tags instead of full 40-character commit SHAs. In tag.yml: `actions/checkout@v4.1.0`. In update.yml: `actions/checkout@v4.1.0`, `actions/setup-python@v2`, and `peter-evans/create-pull-request@v3.10.0`. Any of these tags could be moved to point to a different (potentially malicious) commit without notice.

Locations:

- `.github/workflows/tag.yml:9`
- `.github/workflows/update.yml:9`
- `.github/workflows/update.yml:11`
- `.github/workflows/update.yml:22`

### missing-permissions (severity: medium)

Neither workflow file declares a top-level `permissions:` block, and no job in either file has a job-level `permissions:` block. This means the GITHUB_TOKEN is granted its default (broad) permissions. Both tag.yml and update.yml should declare minimal required permissions (e.g., `contents: write` for tagging, `pull-requests: write` for PR creation).

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Rule (a) violation: update.yml contains a `run:` block that directly interpolates a GitHub Actions expression into a shell command string. The line `run: gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}` embeds `${{ steps.new_pull_request.outputs.pull-request-url }}` directly into the shell command. If the step output contains shell metacharacters, this could lead to command injection. The value should be passed via an `env:` variable and double-quoted in the shell command instead.

Locations:

- `.github/workflows/update.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:
1. unpinned-uses: Pinned all four action references to full commit SHAs — actions/checkout@v4.1.0 → 8ade135a41bc03ea155e62e844d188df1ea18608, actions/setup-python@v2 → e9aba2c848f5ebd159c070c61ea2c4e2b122355e, peter-evans/create-pull-request@v3.10.0 → 9825ae65b1cb54b543b938503728b432a0176d29. Original tags preserved as inline comments.
2. missing-permissions: Added top-level `permissions:` blocks to both files. tag.yml: `contents: write` (for git push --tags). update.yml: `contents: write` and `pull-requests: write` (for PR creation and merge).
3. script-injection: Moved `${{ steps.new_pull_request.outputs.pull-request-url }}` out of the `run:` shell string into a step-level `env:` variable (`PR_URL`) and referenced it as double-quoted `"$PR_URL"` in the shell command.

