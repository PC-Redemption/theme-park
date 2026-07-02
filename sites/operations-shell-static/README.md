# Operations Shell Static

Operations Shell Static is the framework-neutral starter implementation in this repo.

Its job is to prove that the shared framework can also be consumed as plain HTML, CSS, and JavaScript without requiring a server-side template runtime.

## Local Structure

```text
sites/operations-shell-static/
  layouts/
  scaffolds/
  templates/
  app_config/
  routes/
  static/
```

## Rules

- keep site-local pages, assets, and navigation examples here
- move code to `packages/design-system/` only when it is reusable by more than one starter
- keep placeholder content generic and safe for public release
- keep runtime-free usage patterns local to this starter

## Current Starter Assets

- `templates/index.html` for the landing shell demo
- `templates/dashboard.html` for dashboard overview
- `templates/records.html` for list/detail
- `templates/review.html` for workflow review
- `templates/settings.html` for settings workspace
- `app_config/site.example.json` for branding, nav, and page metadata
- `routes/route_manifest.example.json` for static route and file mapping

## Runtime

- templating model: none required
- expected fit: static hosting, docs previews, or low-complexity starter delivery

## Local Preview

Run:

```bash
python3 sites/operations-shell-static/preview.py
```

Then open:

```text
http://127.0.0.1:8000/sites/operations-shell-static/templates/index.html
```
