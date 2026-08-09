<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.16.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.16.2** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple `uses:` references in workflow files are pinned to mutable version tags rather than immutable 40-character commit SHAs, making them vulnerable to supply-chain attacks if the upstream tag is moved or compromised. Failing references: `actions/checkout@v4.1.0` (tag.yml), `actions/checkout@v4.1.0` (update.yml), `actions/setup-python@v2` (update.yml), `peter-evans/create-pull-request@v3.10.0` (update.yml).

Locations:

- `.github/workflows/tag.yml:10`
- `.github/workflows/update.yml:9`
- `.github/workflows/update.yml:11`
- `.github/workflows/update.yml:24`

### permissions (severity: medium)

missing-permissions: Neither workflow file defines a top-level `permissions:` key, and no job within them defines job-level `permissions:` either. Without explicit permissions, workflows run with the default (potentially broad) token permissions, violating the principle of least privilege.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Sub-rule (a): A `${{ ... }}` expression is interpolated directly inside a `run:` shell command. In update.yml, the final step runs `gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`. The step output `steps.new_pull_request.outputs.pull-request-url` is substituted into the shell command before the shell parses it, allowing an attacker who can influence the pull-request URL to inject arbitrary shell commands. The value should be passed via an `env:` variable and double-quoted: `env: PR_URL: ${{ steps.new_pull_request.outputs.pull-request-url }}` then `run: gh pr merge --auto --squash "$PR_URL"`.

Locations:

- `.github/workflows/update.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:

1. **unpinned-uses**: Pinned all four action references to immutable commit SHAs:
   - `actions/checkout@v4.1.0` → `@8ade135a41bc03ea155e62e844d188df1ea18608 # v4.1.0` (both files)
   - `actions/setup-python@v2` → `@e9aba2c848f5ebd159c070c61ea2c4e2b122355e # v2`
   - `peter-evans/create-pull-request@v3.10.0` → `@9825ae65b1cb54b543b938503728b432a0176d29 # v3.10.0`

2. **permissions**: Added `permissions: {}` at the top level of both workflows (deny-all default), and job-level permissions granting only what's needed:
   - tag.yml job: `contents: write` (needed to push tags)
   - update.yml job: `contents: write` + `pull-requests: write` (needed to create/merge PRs)

3. **script-injection**: In update.yml's final step, moved `${{ steps.new_pull_request.outputs.pull-request-url }}` out of the `run:` shell string into an `env:` block as `PR_URL`, then referenced it as `"$PR_URL"` in the shell command.

