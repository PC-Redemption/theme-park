# Starter Exports

Theme Park can now export a minimal bundle for a single starter instead of handing consumers the entire repo.

## Export A Starter

```bash
python3 scripts/theme-park.py starter-export --starter release-hub-jinja
```

Default output:

```text
dist/starter-bundles/release-hub-jinja/
```

## What Gets Exported

- `packages/design-system/`
- `packages/design_system/`
- `sites/<starter-key>/`
- `scripts/preview-starter.sh`
- `scripts/setup-venv.sh`
- a bundle-local `README.md`

## Why Use This

- share one starter without exposing the full catalog repo shape
- create smaller review artifacts for outside consumers
- test whether a starter really depends only on shared packages and its own site directory
