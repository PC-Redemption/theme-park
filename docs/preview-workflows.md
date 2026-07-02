# Preview Workflows

This repo now supports a shared control-plane workflow for all starters, plus a richer root catalog with live screenshots.

## Standard Policy

This repo currently standardizes on:

- an ignored `.venv/` for Python-backed starter previews
- small repo-local preview scripts under `scripts/`
- starter-local runtime files when a starter needs more than static hosting
- Playwright-based screenshot capture for the root catalog

## Shared Preview Entry Point

Run any starter through the same root-level script:

```bash
scripts/preview-starter.sh operations-shell-jinja
scripts/preview-starter.sh settings-portal-static
scripts/preview-starter.sh mission-control-jinja
```

## Jinja Starter

Path:

- `sites/operations-shell-jinja/`
- `sites/settings-portal-jinja/`
- `sites/review-studio-jinja/`

Setup:

```bash
scripts/setup-venv.sh
```

Run:

```bash
scripts/preview-starter.sh operations-shell-jinja
```

Open:

```text
http://127.0.0.1:8000/dashboard
```

Or for settings portal:

```text
http://127.0.0.1:8000/health
```

## Static Starter

Path:

- `sites/operations-shell-static/`
- `sites/settings-portal-static/`
- `sites/review-studio-static/`

Run:

```bash
scripts/preview-starter.sh operations-shell-static
```

Open:

```text
http://127.0.0.1:8000/sites/operations-shell-static/templates/index.html
```

Or for settings portal:

```text
http://127.0.0.1:8000/sites/settings-portal-static/templates/index.html
```

## Catalog Refresh

Build static output, capture live screenshots, and refresh the control-plane catalog:

```bash
npm run catalog:refresh
```

To recapture only a changed family or starter:

```bash
node scripts/capture-previews.mjs --starter mission-control-jinja
node scripts/capture-previews.mjs --starter release-hub-static
```

Prerequisites:

```bash
npm install
npx playwright install chromium
```

## Current State

- Jinja previews verified locally from the shared `scripts/preview-starter.sh` entry point
- static previews verified locally with the Python standard library server
- live starter screenshots captured with Playwright into `catalog/previews/`
- root catalog launcher upgraded into a control plane with search, command builders, and scaffold workflows

## Tooling Decision

Current choice:

- `.venv` plus small preview scripts is the default repo workflow
- Playwright is the default screenshot engine for the catalog

Deferred for later:

- whether to adopt `uv`, Poetry, or another heavier shared toolchain once multiple runtime-backed starters exist
