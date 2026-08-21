<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.16.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.16.4** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Both workflow files reference actions using mutable version tags instead of pinned full-length SHA commit digests, making them vulnerable to supply-chain attacks if the tag is moved.

Failing references:
- `actions/checkout@v4.1.0` (tag, not SHA)
- `actions/setup-python@v2` (tag, not SHA)
- `peter-evans/create-pull-request@v3.10.0` (tag, not SHA)

Locations:

- `.github/workflows/tag.yml:11`
- `.github/workflows/update.yml:10`
- `.github/workflows/update.yml:12`
- `.github/workflows/update.yml:24`

### missing-permissions (severity: medium)

Neither workflow file defines a top-level `permissions:` key, and no job in either file defines job-level permissions. Without explicit permissions, the GITHUB_TOKEN is granted its default (potentially broad) permissions, violating the principle of least privilege.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Sub-rule (a) violation: A `${{ ... }}` expression is interpolated directly inside a `run:` shell command string in update.yml. The value `${{ steps.new_pull_request.outputs.pull-request-url }}` is a step output that could contain attacker-influenced content (e.g. a crafted PR URL), and is passed directly to the shell without quoting or sanitization.

Offending line:
  `run: gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`

This allows shell metacharacter injection if the pull-request URL contains special characters.

Locations:

- `.github/workflows/update.yml:32`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:

1. unpinned-uses: Pinned all three action references to full commit SHAs:
   - actions/checkout@v4.1.0 → @8ade135a41bc03ea155e62e844d188df1ea18608 # v4.1.0
   - actions/setup-python@v2 → @e9aba2c848f5ebd159c070c61ea2c4e2b122355e # v2
   - peter-evans/create-pull-request@v3.10.0 → @9825ae65b1cb54b543b938503728b432a0176d29 # v3.10.0

2. missing-permissions: Added top-level `permissions: {}` to both files (deny-all default), plus job-level minimal permissions:
   - tag.yml job: contents: write (needed to push tags)
   - update.yml job: contents: write + pull-requests: write (needed to create/merge PRs)

3. script-injection: Moved `${{ steps.new_pull_request.outputs.pull-request-url }}` out of the run: shell string into the step's env: block as PR_URL, then referenced it safely as "$PR_URL" in the shell command.

