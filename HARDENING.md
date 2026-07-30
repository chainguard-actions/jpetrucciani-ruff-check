<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.16.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.16.1** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Both workflow files reference GitHub Actions using mutable version tags instead of pinned 40-character commit SHAs, making them vulnerable to supply-chain attacks if the tag is moved. Failing references: `actions/checkout@v4.1.0` (tag.yml and update.yml), `actions/setup-python@v2` (update.yml), `peter-evans/create-pull-request@v3.10.0` (update.yml).

Locations:

- `.github/workflows/tag.yml:10`
- `.github/workflows/update.yml:8`
- `.github/workflows/update.yml:10`
- `.github/workflows/update.yml:17`

### missing-permissions (severity: medium)

Neither workflow file defines a top-level `permissions:` key, and no job in either file defines job-level permissions. Without explicit permissions, the GITHUB_TOKEN is granted its default (potentially broad) permissions, violating the principle of least privilege.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Sub-rule (a): A `${{ ... }}` expression is interpolated directly inside a `run:` shell command string in update.yml. The offending line is: `run: gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`. The step output value is substituted into the shell command before the shell parses it, allowing an attacker who can influence the pull-request URL (e.g. via a crafted branch name) to inject arbitrary shell commands. The value should be passed via an `env:` variable and double-quoted in the shell script instead.

Locations:

- `.github/workflows/update.yml:22`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:
1. unpinned-uses: Pinned actions/checkout@v4.1.0 → SHA 8ade135a41bc03ea155e62e844d188df1ea18608, actions/setup-python@v2 → SHA e9aba2c848f5ebd159c070c61ea2c4e2b122355e, peter-evans/create-pull-request@v3.10.0 → SHA 9825ae65b1cb54b543b938503728b432a0176d29. Original tags preserved as inline comments.
2. missing-permissions: Added top-level `permissions: {}` to both files (deny-all default), and job-level `permissions: {contents: write}` to tag.yml and `permissions: {contents: write, pull-requests: write}` to update.yml.
3. script-injection: Moved `${{ steps.new_pull_request.outputs.pull-request-url }}` from the run: shell string into an env: variable `PR_URL`, referenced as `"$PR_URL"` in the shell command.

