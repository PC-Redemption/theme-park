# Theme Park Runbooks

## Runbook 1: Kick Off The Repo

Use when:

- setting up the public repo structure for the first time

Steps:

1. create the top-level directories: `packages/`, `sites/`, and `docs/`
2. create `packages/design-system/`
3. create the first starter directory under `sites/`
4. add a local `README.md` inside each starter-site folder
5. document naming and boundary rules in root docs

Checks:

- shared code is not placed inside a site directory
- site-specific code is not placed inside `packages/design-system/`
- each site directory is self-explanatory by name

## Runbook 1A: Set Up Local Preview Tooling

Use when:

- preparing this repo for local starter previews

Steps:

1. run `scripts/setup-venv.sh` for Python-backed starters
2. use `scripts/preview-jinja.sh` for the Jinja starter
3. use `scripts/preview-static.sh` for the static starter
4. keep `.venv/` local and untracked

Checks:

- do not commit local virtual environment files
- keep preview commands simple and repo-local
- prefer starter-local runtime requirements over a heavy shared toolchain

## Runbook 2: Inventory A Source App

Use when:

- evaluating an internal app for extraction into framework pieces and a starter site

Steps:

1. inspect app settings, templates, static assets, routes, and layout files
2. list repeated tokens and common style patterns
3. list repeated shell structures and interaction patterns
4. mark each artifact as `extract`, `adapt`, or `discard`
5. flag anything tied to business logic, API calls, or product wording

Checks:

- do not move files before the inventory exists
- do not classify product copy as reusable structure
- do not preserve source naming if it leaks product intent

## Runbook 3: Extract Tokens

Use when:

- starting a new extraction

Steps:

1. capture colors, spacing, typography, borders, radii, and shadows
2. normalize them into a shared token system
3. remove product names from token names
4. document any token values that were hard to generalize

Checks:

- tokens represent design decisions, not page-specific hacks
- token names are generic and stable

## Runbook 4: Build Shared Primitives

Use when:

- turning repeated UI behavior into reusable framework code

Steps:

1. build base styles from tokens
2. extract common JS behavior for modals, tabs, accordions, and loading states
3. keep selectors and hooks generic
4. document assumptions about markup shape

Checks:

- primitives should be reusable by more than one starter site
- primitives must not depend on a single deployment's routes or labels

## Runbook 5: Create A Starter Site

Use when:

- publishing a new starter under `sites/`

Steps:

1. create a clearly named directory under `sites/`
2. add local folders for layouts, templates, scaffolds, config, routes, and static assets
3. wire the site to shared framework pieces from `packages/design-system/`
4. replace all original content with placeholders
5. add a local `README.md` explaining the starter's purpose and extension points

Checks:

- the starter should be identifiable without opening shared framework code
- site-local files should stay inside the site directory unless they become broadly reusable
- placeholder content should make the starter safe to publish

## Runbook 6: Decide Shared Vs Site-Local

Use when:

- a file or pattern could live in either the shared framework or a site directory

Decision rule:

- move it to `packages/design-system/` only if at least two starters can use it without renaming or behavior changes

Keep it site-local if:

- it expresses a starter-specific information architecture
- it exists mainly to support one starter's voice or flow
- it requires starter-specific template structure

Promote it to shared if:

- it is a visual primitive
- it is a generic interaction pattern
- it is a layout building block with broad reuse

## Runbook 7: Add Another Starter Site

Use when:

- expanding the public catalog

Steps:

1. create a new directory under `sites/`
2. copy only the minimum site-local structure needed
3. import shared framework pieces rather than duplicating them
4. write starter-specific docs in the new site's `README.md`
5. compare the new starter against existing starters to identify abstractions worth promoting

Checks:

- do not restructure existing starter directories to fit the new one
- do not collapse multiple starters into one mixed folder
- prefer shared abstractions over copy-paste, but not at the cost of clarity

## Runbook 7A: Copy A Starter

Use when:

- a current starter is close to what you need and you want a new site-local variant quickly

Steps:

1. pick the nearest source starter from the control plane
2. run `python3 scripts/theme-park.py starter-copy --source SOURCE_KEY --dest NEW_KEY`
3. pass `--name`, `--summary`, or `--family` if the default carry-over is too generic
4. preview the new starter with `scripts/preview-starter.sh NEW_KEY`
5. refresh the catalog with `python3 scripts/theme-park.py build-catalog`

Checks:

- verify the copied starter manifest points at the new site directory
- verify branding and summary files were rewritten
- keep the starter in its own site directory under `sites/`

## Runbook 7B: Create A Starter Family

Use when:

- you want both static and Jinja variants for a new family without hand-copying two site trees

Steps:

1. choose the closest seed family such as `operations`, `settings`, or `review`
2. run `python3 scripts/theme-park.py family-create --seed-family operations --family NEW_FAMILY --site-slug NEW_SITE`
3. add `--display-name` and `--summary` so the generated family reads well in the catalog
4. preview both generated starters with `scripts/preview-starter.sh`
5. capture live screenshots with `node scripts/capture-previews.mjs --starter NEW_KEY`

Checks:

- both runtime variants should appear under `sites/`
- static preview paths should point at the generated site, not the seed site
- rebuild the catalog after generation so the control plane reflects the new family

## Runbook 8: Sanitize For Public Release

Use when:

- preparing commits or releases for a public repo

Steps:

1. scan for private names, internal URLs, product labels, and environment assumptions
2. replace sensitive labels with generic placeholders
3. verify licenses and ownership for copied assets or snippets
4. confirm the repo runs without private services
5. review docs from the perspective of an outside user

Checks:

- no internal hostnames remain unless intentionally documented as historical source references
- no private credentials, identifiers, or routes remain
- examples are safe to publish and understand

## Runbook 8A: Refresh The Control Plane

Use when:

- starter metadata, screenshots, or generated static pages have changed

Steps:

1. run `python3 scripts/theme-park.py build-static`
2. run `python3 scripts/theme-park.py build-catalog`
3. run `node scripts/capture-previews.mjs` for fresh live renders
4. rerun `python3 scripts/theme-park.py build-catalog` so image references are current
5. preview the launcher with `scripts/preview-catalog.sh`

Checks:

- every starter card should show a live screenshot or an explicit pending state
- workflow builders should reflect currently available families and starters
- starter counts in the launcher should match `catalog/starters.json`

## Runbook 9: Accept A Starter Extraction

Use when:

- deciding whether a starter is done enough to merge

Acceptance checklist:

- shared framework and starter-site boundaries are clear
- no business logic is required to render the starter
- branding is configurable
- nav is configurable
- permissions are configurable or adapter-driven
- product-specific copy has been removed
- the starter has a local `README.md`
- the starter can be extended without changing framework internals

## Runbook 10: Promote Lessons

Use when:

- a durable extraction or repo-structure lesson should be shared

Steps:

1. summarize the reusable lesson in one clear statement
2. check whether the concept already exists in shared lessons
3. update the existing lesson instead of creating a duplicate when possible
4. promote the lesson
5. resync lessons after promotion

Checks:

- only promote durable process knowledge
- avoid one-off project trivia
