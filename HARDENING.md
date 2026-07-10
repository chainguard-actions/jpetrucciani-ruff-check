<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.15.21

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **jpetrucciani--ruff-check/0.15.21** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Workflow files reference actions using mutable version tags instead of pinned full-length SHA commits. Failing references: tag.yml: `actions/checkout@v4.1.0` (line 11). update.yml: `actions/checkout@v4.1.0` (line 10), `actions/setup-python@v2` (line 12), `peter-evans/create-pull-request@v3.10.0` (line 24). These should be pinned to a full 40-character commit SHA (e.g. `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.1.0`).

Locations:

- `.github/workflows/tag.yml:11`
- `.github/workflows/update.yml:10`
- `.github/workflows/update.yml:12`
- `.github/workflows/update.yml:24`

### missing-permissions (severity: medium)

Neither workflow file has a top-level `permissions:` key, and no job in either file defines job-level permissions. Without explicit permissions, the GITHUB_TOKEN is granted default (often broad) permissions. Both tag.yml and update.yml should declare minimal required permissions (e.g. `contents: write` for tagging, `pull-requests: write` for PR creation).

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Sub-rule (a): A `${{ ... }}` expression is directly interpolated inside a `run:` shell command string. In update.yml line 32: `run: gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`. The value of `steps.new_pull_request.outputs.pull-request-url` flows through YAML template substitution before the shell sees it, allowing shell metacharacter injection. Fix by routing through an env var and quoting: `env: PR_URL: ${{ steps.new_pull_request.outputs.pull-request-url }}` then `run: gh pr merge --auto --squash "$PR_URL"`.

Locations:

- `.github/workflows/update.yml:32`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across tag.yml and update.yml:
1. unpinned-uses: Pinned actions/checkout@v4.1.0 → SHA 8ade135a41bc03ea155e62e844d188df1ea18608 (in both files), actions/setup-python@v2 → SHA e9aba2c848f5ebd159c070c61ea2c4e2b122355e, and peter-evans/create-pull-request@v3.10.0 → SHA 9825ae65b1cb54b543b938503728b432a0176d29.
2. missing-permissions: Added top-level `permissions: contents: write` to tag.yml (for git push --tags), and `permissions: contents: write, pull-requests: write` to update.yml (for PR creation and merge).
3. script-injection: In update.yml line 32, moved `${{ steps.new_pull_request.outputs.pull-request-url }}` into an `env:` block as `PR_URL` and referenced it as `"$PR_URL"` in the shell command.

