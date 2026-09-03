<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.16.6

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.16.6** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple `uses:` references in workflow files are pinned to version tags instead of full 40-character commit SHAs, making them vulnerable to supply-chain attacks if the tag is moved. Failing references: `actions/checkout@v4.1.0` (tag.yml, update.yml), `actions/setup-python@v2` (update.yml), `peter-evans/create-pull-request@v3.10.0` (update.yml).

Locations:

- `.github/workflows/tag.yml:9`
- `.github/workflows/update.yml:10`
- `.github/workflows/update.yml:12`
- `.github/workflows/update.yml:25`

### missing-permissions (severity: medium)

Neither `tag.yml` nor `update.yml` declares a top-level `permissions:` block, and no job in either file has a job-level `permissions:` block. Without explicit permissions, workflows run with the default (often broad) token permissions, violating the principle of least privilege.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Sub-rule (a): In `update.yml`, the final `run:` step directly interpolates `${{ steps.new_pull_request.outputs.pull-request-url }}` into a shell command (`gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`). This expression is expanded by the Actions template engine before the shell sees it, allowing a malicious pull-request URL value to inject arbitrary shell commands. The value should be passed via an `env:` variable and double-quoted instead.

Locations:

- `.github/workflows/update.yml:31`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across tag.yml and update.yml:
1. unpinned-uses: Pinned actions/checkout@v4.1.0 → SHA 8ade135a41bc03ea155e62e844d188df1ea18608, actions/setup-python@v2 → SHA e9aba2c848f5ebd159c070c61ea2c4e2b122355e, peter-evans/create-pull-request@v3.10.0 → SHA 9825ae65b1cb54b543b938503728b432a0176d29. Original tags preserved as inline comments.
2. missing-permissions: Added top-level `permissions: {}` to both files and job-level permissions granting only what's needed (contents: write for tag.yml; contents: write + pull-requests: write for update.yml).
3. script-injection: Moved `${{ steps.new_pull_request.outputs.pull-request-url }}` out of the shell command in update.yml into an `env:` block as PR_URL, then referenced it as double-quoted `"$PR_URL"` in the run step.

