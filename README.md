# ruff-check

GitHub Action for [ruff](https://github.com/charliermarsh/ruff)

## Inputs

### `path`

The path to run ruff on

**Default** `"."`

### `format`

Format to output ruff messages in

**Default** `"github"`

### `flags`

**Optional** Optional ruff flags (refer to `ruff --help`)

**Default** `""`

## Outputs

None

## Example usage

```yaml
uses: jpetrucciani/ruff-check@main

# or specify a path!
uses: jpetrucciani/ruff-check@main
with:
  path: '.'

# or specify more flags!
uses: jpetrucciani/ruff-check@main
with:
  flags: '--exclude ./env/'
```

## Privacy

This Action contacts Chainguard's licensing server to verify authorization. Connection metadata (IP address, GitHub repository identifier, timestamp, and any metadata encoded in the auth token) is transmitted to Chainguard, Inc. even if authorization is denied in accordance with our [Privacy Notice](https://www.chainguard.dev/legal/privacy-notice)
