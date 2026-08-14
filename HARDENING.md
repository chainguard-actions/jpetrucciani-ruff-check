<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.16.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.16.3** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Both workflow files reference GitHub Actions using mutable version tags instead of full 40-character SHA commit digests. This exposes the workflow to supply-chain attacks if the referenced tag is moved or overwritten. Failing references: tag.yml: `actions/checkout@v4.1.0`; update.yml: `actions/checkout@v4.1.0`, `actions/setup-python@v2`, `peter-evans/create-pull-request@v3.10.0`.

Locations:

- `.github/workflows/tag.yml:9`
- `.github/workflows/update.yml:11`
- `.github/workflows/update.yml:13`
- `.github/workflows/update.yml:24`

### missing-permissions (severity: medium)

Neither workflow file defines a top-level `permissions:` key, and no job in either file defines its own `permissions:` block. Without explicit permissions, the GITHUB_TOKEN is granted default (potentially broad) permissions. Each workflow should declare minimal required permissions.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Sub-rule (a): In update.yml, a `run:` block directly interpolates a GitHub Actions expression into the shell command string: `gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`. The expression `${{ steps.new_pull_request.outputs.pull-request-url }}` is substituted into the shell command before the shell parses it, allowing an attacker who can influence the pull-request URL output to inject arbitrary shell commands.

Locations:

- `.github/workflows/update.yml:31`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:
1. unpinned-uses: Pinned all four action references to full 40-char SHAs with tag comments: actions/checkout@v4.1.0 → 8ade135a41bc03ea155e62e844d188df1ea18608, actions/setup-python@v2 → e9aba2c848f5ebd159c070c61ea2c4e2b122355e, peter-evans/create-pull-request@v3.10.0 → 9825ae65b1cb54b543b938503728b432a0176d29.
2. missing-permissions: Added top-level `permissions: {}` to both files and minimal job-level permissions (contents: write for tag.yml; contents: write + pull-requests: write for update.yml).
3. script-injection: Moved `${{ steps.new_pull_request.outputs.pull-request-url }}` out of the run: shell string into the step's env: block as PR_URL, then referenced it as "$PR_URL" in the shell command.

