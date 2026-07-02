# Operations Shell Jinja

Operations Shell Jinja is the Jinja-first starter implementation in this repo.

Its job is to prove that the shared framework can support a reusable internal-operations style shell with template inheritance, component macros, and route-driven scaffold rendering.

## Local Structure

```text
sites/operations-shell-jinja/
  layouts/
  scaffolds/
  templates/
  app_config/
  routes/
  static/
```

## Rules

- keep site-local templates, assets, and route wiring here
- move code to `packages/design-system/` only when it is reusable by more than one starter
- keep placeholder content generic and safe for public release
- keep runtime-specific template wiring local to this starter

## Planned Configuration Surface

- branding
- navigation
- permissions
- route registration

## Current Starter Assets

- `scaffolds/` for starter-safe Jinja scaffold pages
- `app_config/shell.example.json` for shell-level branding and nav config
- `app_config/scaffold_contracts.example.json` for scaffold-specific placeholder contracts
- `routes/route_manifest.example.json` for starter route registration shape

## Runtime

- templating model: Jinja
- expected backend fit: FastAPI, Flask, or another Jinja-capable runtime

## Local Demo

Install dependencies:

```bash
python3 -m pip install -r sites/operations-shell-jinja/requirements.txt
```

Run:

```bash
uvicorn sites.operations-shell-jinja.app:app --reload
```

If your shell does not support importing from a hyphenated path, run:

```bash
cd sites/operations-shell-jinja
python3 -m uvicorn app:app --reload
```
