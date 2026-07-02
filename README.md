# Theme Park

Theme Park is a public-facing starter-site framework repo for reusable web layouts.

The repo is organized around two boundaries:

- `packages/` for shared design-system and framework code
- `sites/` for clearly separated starter sites, each with its own local identity and documentation

Current starter implementations:

- `sites/operations-shell-jinja/` for a Jinja-first runtime-backed starter
- `sites/operations-shell-static/` for a framework-neutral static starter
- `sites/settings-portal-jinja/` for a Jinja-first admin and settings starter
- `sites/settings-portal-static/` for a framework-neutral admin and settings starter

Default local workflow:

- use an ignored `.venv/` for Python-backed starter previews
- use small repo-local preview scripts under `scripts/`

## Goals

- provide reusable starter web shells
- keep starter sites isolated and easy to identify
- make branding, navigation, permissions, and routes configurable
- support adding more starters without restructuring the repo

## Current Contents

- [STARTER_BRIEF.md](./STARTER_BRIEF.md)
- [ROADMAP.md](./ROADMAP.md)
- [MILESTONES.md](./MILESTONES.md)
- [RUNBOOKS.md](./RUNBOOKS.md)
- [docs/preview-workflows.md](./docs/preview-workflows.md)
- [docs/starter-catalog.md](./docs/starter-catalog.md)

## Preview Commands

```bash
scripts/setup-venv.sh
scripts/preview-jinja.sh
scripts/preview-settings-jinja.sh
scripts/preview-review-jinja.sh
scripts/preview-static.sh
scripts/preview-settings-static.sh
scripts/preview-review-static.sh
scripts/preview-catalog.sh
```

## Repo Rules

- anything tracked here should be safe for public consumption
- do not commit private hostnames, internal paths, credentials, or environment-specific secrets
- keep shared framework code out of starter-site directories unless it is truly site-local
- keep each starter site in its own clearly named folder under `sites/`

## Next Steps

1. create the repo skeleton under `packages/`, `sites/`, and `docs/`
2. inspect the private source app in a safe execution environment
3. extract shared design tokens and primitives
4. publish the first isolated starter implementations
