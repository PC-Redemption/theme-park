# Theme Park

Theme Park is a public-facing starter-site framework repo for reusable web layouts.

License: [MIT](./LICENSE)

The repo is organized around two boundaries:

- `packages/` for shared design-system and framework code
- `sites/` for clearly separated starter sites, each with its own local identity and documentation
- `catalog/` for the root-level control plane and starter discovery experience

Current starter implementations:

- `sites/operations-shell-jinja/` for a Jinja-first runtime-backed starter
- `sites/operations-shell-static/` for a framework-neutral static starter
- `sites/settings-portal-jinja/` for a Jinja-first admin and settings starter
- `sites/settings-portal-static/` for a framework-neutral admin and settings starter
- `sites/review-studio-jinja/` for a review and approvals starter
- `sites/review-studio-static/` for a framework-neutral review starter
- `sites/mission-control-jinja/` for a generated proof family created from the new scaffold workflow
- `sites/mission-control-static/` for the matching framework-neutral generated proof family
- `sites/release-hub-jinja/` for a release-readiness and approvals starter generated from a family spec
- `sites/release-hub-static/` for the matching framework-neutral release starter

Default local workflow:

- use an ignored `.venv/` for Python-backed starter previews
- use small repo-local preview scripts under `scripts/`
- use the root control-plane commands in `scripts/theme-park.py`
- use Playwright for live screenshot capture
- store reusable starter-family specs under `families/`

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
- [docs/exports.md](./docs/exports.md)

## Preview Commands

```bash
scripts/setup-venv.sh
scripts/preview-starter.sh operations-shell-jinja
scripts/preview-starter.sh settings-portal-static
scripts/preview-catalog.sh
```

## Control Plane Commands

```bash
python3 scripts/theme-park.py build-static
python3 scripts/theme-park.py build-catalog
python3 scripts/theme-park.py starter-copy --source operations-shell-jinja --dest your-new-starter
python3 scripts/theme-park.py family-spec-init --output families/your-family.json
python3 scripts/theme-park.py family-create --config families/your-family.json
python3 scripts/theme-park.py family-sync --config families/your-family.json
python3 scripts/theme-park.py starter-export --starter release-hub-jinja
npm install
npx playwright install chromium
npm run catalog:refresh
```

## Repo Rules

- anything tracked here should be safe for public consumption
- do not commit private hostnames, internal paths, credentials, or environment-specific secrets
- keep shared framework code out of starter-site directories unless it is truly site-local
- keep each starter site in its own clearly named folder under `sites/`

## Next Steps

1. keep pressure-testing family generation against more distinct information architectures
2. add starter onboarding templates for non-Python runtimes beyond static HTML
3. promote more repeated site scaffolds into explicit shared contracts
4. add publish-ready remote and release automation once the public repo destination is chosen
