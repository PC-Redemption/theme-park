# Starter Catalog

This document is the human-readable companion to the manifest-driven root catalog.

For the live launcher view, use:

```bash
scripts/preview-catalog.sh
```

## Operations Family

### `operations-shell-jinja`

- runtime-backed Jinja starter
- strengths: dashboards, list/detail workspaces, workflow review, monitoring, reference browsing, result pages
- preview: `scripts/preview-jinja.sh`

### `operations-shell-static`

- framework-neutral static starter
- strengths: simple shell demos, documentation previews, plain HTML starter delivery
- preview: `scripts/preview-static.sh`

## Settings Family

### `settings-portal-jinja`

- runtime-backed Jinja starter
- strengths: health review, global preferences, user administration, event audit pages
- preview: `scripts/preview-settings-jinja.sh`

### `settings-portal-static`

- framework-neutral static starter
- strengths: admin portal demos, table-heavy settings pages, static previews of configuration surfaces
- preview: `scripts/preview-settings-static.sh`

## Review Family

### `review-studio-jinja`

- runtime-backed Jinja starter
- strengths: review queues, evidence bundles, approval boards, release summaries
- preview: `scripts/preview-review-jinja.sh`

### `review-studio-static`

- framework-neutral static starter
- strengths: queue demos, evidence layouts, approval boards, release summary surfaces
- preview: `scripts/preview-review-static.sh`

## Shared Layer

All four starters consume the shared design system in:

- `packages/design-system/tokens/`
- `packages/design-system/styles/`
- `packages/design-system/scripts/`
- `packages/design-system/templates/`

## Current Pressure-Test Outcome

The shared layer now supports at least three distinct site families:

- operations-oriented shells
- admin/settings-oriented portals
- review and approval-oriented studios

That is enough to start identifying whether future work should prioritize:

- stronger shared abstractions
- more starter families
- a smoother root-level developer experience

## Manifest Source

Starter metadata now lives in:

- `sites/*/starter.manifest.json`

The root launcher data file is built from those manifests by:

- `scripts/build-catalog.py`
