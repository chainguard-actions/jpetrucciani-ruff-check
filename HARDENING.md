<!-- markdownlint-disable -->

# Hardening Report: jpetrucciani--ruff-check/0.15.21

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **jpetrucciani--ruff-check/0.15.21** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Both workflow files reference GitHub Actions using mutable version tags instead of full 40-character commit SHA pins, making them vulnerable to supply-chain attacks if the tag is moved. Failing references:
- .github/workflows/tag.yml: `actions/checkout@v4.1.0`
- .github/workflows/update.yml: `actions/checkout@v4.1.0`, `actions/setup-python@v2`, `peter-evans/create-pull-request@v3.10.0`

Locations:

- `.github/workflows/tag.yml:9`
- `.github/workflows/update.yml:8`
- `.github/workflows/update.yml:10`
- `.github/workflows/update.yml:19`

### missing-permissions (severity: medium)

Neither workflow file defines a top-level `permissions:` block, and no job in either file defines job-level permissions. Without explicit permissions, the GITHUB_TOKEN is granted its default (often broad) permissions, violating the principle of least privilege.

Locations:

- `.github/workflows/tag.yml:1`
- `.github/workflows/update.yml:1`

### script-injection (severity: high)

Rule (a) violation: A `${{ }}` expression is interpolated directly inside a `run:` shell command in update.yml. The offending line is:
  `run: gh pr merge --auto --squash ${{ steps.new_pull_request.outputs.pull-request-url }}`
The value `steps.new_pull_request.outputs.pull-request-url` flows through YAML template substitution before the shell parses it, allowing shell metacharacters in the value to be interpreted. It should be passed via an `env:` variable and double-quoted in the shell command instead.

Locations:

- `.github/workflows/update.yml:27`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, script-injection

**Notes:**

Fixed all three findings across .github/workflows/tag.yml and .github/workflows/update.yml:
1. unpinned-uses: Pinned actions/checkout@v4.1.0 → @8ade135a41bc03ea155e62e844d188df1ea18608, actions/setup-python@v2 → @e9aba2c848f5ebd159c070c61ea2c4e2b122355e, peter-evans/create-pull-request@v3.10.0 → @9825ae65b1cb54b543b938503728b432a0176d29, all with original tag in comment.
2. missing-permissions: Added top-level `permissions: {}` to both files and job-level permissions (contents: write for tag.yml; contents: write + pull-requests: write for update.yml).
3. script-injection: Moved `${{ steps.new_pull_request.outputs.pull-request-url }}` into an env var `PR_URL` and referenced it as `"$PR_URL"` in the shell command.

