# Preview Workflows

This repo currently supports two preview styles for the first starter pair.

## Standard Policy

This repo currently standardizes on:

- an ignored `.venv/` for Python-backed starter previews
- small repo-local preview scripts under `scripts/`
- starter-local runtime files when a starter needs more than static hosting

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
scripts/preview-jinja.sh
```

Or:

```bash
scripts/preview-settings-jinja.sh
```

Or:

```bash
scripts/preview-review-jinja.sh
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
scripts/preview-static.sh
```

Or:

```bash
scripts/preview-settings-static.sh
```

Or:

```bash
scripts/preview-review-static.sh
```

Open:

```text
http://127.0.0.1:8000/sites/operations-shell-static/templates/index.html
```

Or for settings portal:

```text
http://127.0.0.1:8000/sites/settings-portal-static/templates/index.html
```

## Current State

- Jinja preview verified locally after installing FastAPI, Uvicorn, and Jinja2 in an ignored `.venv`
- static preview verified locally with the Python standard library server
- second starter family added to pressure-test forms, tables, and admin-heavy layouts
- root catalog launcher added for starter discovery and preview guidance

## Tooling Decision

Current choice:

- `.venv` plus small preview scripts is the default repo workflow

Deferred for later:

- whether to adopt `uv`, Poetry, or another heavier shared toolchain once multiple runtime-backed starters exist
