<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.15.20

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.15.20** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags instead of pinned 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the tag is moved to a malicious commit. Failing references: tag.yml: `actions/checkout@v4.1.0`; update.yml: `actions/checkout@v4.1.0`, `actions/setup-python@v2`, `peter-evans/create-pull-request@v3.10.0`.

Locations:

- `.github/workflows/tag.yml:11`
- `.github/workflows/update.yml:10`
- `.github/workflows/update.yml:12`
- `.github/workflows/update.yml:23`

### permissions (severity: medium)

missing-permissions: Neither workflow file defines a top-level `permissions:` key, and no job within either file defines a job-level `permissions:` key. Without explicit permissions, workflows inherit the repository's default token permissions (often `write-all`), granting unnecessarily broad access.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Sub-rule (a): A `${{ }}` expression is directly interpolated inside a `run:` shell command in update.yml. The offending line is: `run: gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`. The value of `steps.new_pull_request.outputs.pull-request-url` flows through YAML template substitution before the shell parses it, allowing an attacker who can influence the PR URL (e.g. via a crafted branch name) to inject shell metacharacters. The expression should be moved to an `env:` variable and the shell variable double-quoted instead.

Locations:

- `.github/workflows/update.yml:31`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:

1. unpinned-uses: Pinned all four action references to full 40-char SHAs:
   - actions/checkout@v4.1.0 → @8ade135a41bc03ea155e62e844d188df1ea18608 (both files)
   - actions/setup-python@v2 → @e9aba2c848f5ebd159c070c61ea2c4e2b122355e
   - peter-evans/create-pull-request@v3.10.0 → @9825ae65b1cb54b543b938503728b432a0176d29
   Original tags preserved as inline comments.

2. missing-permissions: Added top-level `permissions:` blocks to both files:
   - tag.yml: `contents: write` (needed for git push --tags)
   - update.yml: `contents: write` + `pull-requests: write` (needed for PR creation and merge)

3. script-injection: Moved `${{ steps.new_pull_request.outputs.pull-request-url }}` out of the `run:` shell command in update.yml into an `env:` block as `PR_URL`, then referenced it as `"$PR_URL"` in the shell script.

