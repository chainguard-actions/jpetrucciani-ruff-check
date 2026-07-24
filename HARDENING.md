<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.16.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.16.0** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags instead of pinned 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the tag is moved. Failing references:
- .github/workflows/tag.yml: `uses: actions/checkout@v4.1.0`
- .github/workflows/update.yml: `uses: actions/checkout@v4.1.0`, `uses: actions/setup-python@v2`, `uses: peter-evans/create-pull-request@v3.10.0`

Locations:

- `.github/workflows/tag.yml:11`
- `.github/workflows/update.yml:10`
- `.github/workflows/update.yml:12`
- `.github/workflows/update.yml:24`

### missing-permissions (severity: medium)

Neither workflow file defines a top-level `permissions:` block, and no job within either file defines job-level `permissions:`. Without explicit permissions, workflows run with the default (potentially broad) token permissions. Both tag.yml and update.yml are affected.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Rule (a) violation: A GitHub Actions expression is interpolated directly inside a `run:` shell command string. In update.yml line 31, `${{ steps.new_pull_request.outputs.pull-request-url }}` is embedded directly in the shell command `gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`. If the pull-request URL were attacker-influenced, this could allow shell command injection. The value should be passed via an `env:` variable and double-quoted in the shell.

Locations:

- `.github/workflows/update.yml:31`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:
1. unpinned-uses: Pinned actions/checkout@v4.1.0 → @8ade135a41bc03ea155e62e844d188df1ea18608, actions/setup-python@v2 → @e9aba2c848f5ebd159c070c61ea2c4e2b122355e, and peter-evans/create-pull-request@v3.10.0 → @9825ae65b1cb54b543b938503728b432a0176d29, all with original tag preserved as inline comments.
2. missing-permissions: Added `permissions: {}` top-level block to both workflow files to restrict the default GITHUB_TOKEN permissions.
3. script-injection: In update.yml line 31, moved `${{ steps.new_pull_request.outputs.pull-request-url }}` into an `env:` block as `PR_URL` and referenced it as `"$PR_URL"` in the shell command to prevent shell injection.

