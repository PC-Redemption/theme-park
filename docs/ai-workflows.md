# AI Workflows

This repo works well with AI agents because the boundaries are explicit:

- shared framework code lives in `packages/`
- starter-local code lives in `sites/<starter-key>/`
- family-generation inputs live in `families/`
- root workflows live in `scripts/theme-park.py`

Use this document when you want an AI tool to help create, modify, or export starters without breaking the repo structure.

## Good AI Tasks

- create a new starter from an existing starter
- create a new family spec from an existing family
- reskin a starter with new branding, colors, and labels
- add placeholder pages to a starter
- refine starter-local README files
- update shared docs when workflows change
- extract repeated patterns from multiple starters into shared code

## Best Starting Points

For a new starter variant:

```bash
python3 scripts/theme-park.py starter-copy --source operations-shell-jinja --dest your-new-starter
```

For a new family:

```bash
python3 scripts/theme-park.py family-spec-init --output families/your-family.json
python3 scripts/theme-park.py family-create --config families/your-family.json
```

For a changed family spec:

```bash
python3 scripts/theme-park.py family-sync --config families/your-family.json
```

For updated screenshots and catalog data:

```bash
npm run catalog:refresh
```

## Recommended AI Loop

1. choose the closest existing starter or family
2. tell the AI which files it may change
3. tell it whether the change belongs in `packages/` or `sites/`
4. have it run the relevant control-plane command
5. have it preview or rebuild the affected starter
6. have it refresh screenshots if catalog cards changed

## Example Workflow: New Family

Use AI to:

1. create `families/field-ops.json`
2. choose a seed family such as `operations`
3. set public-safe summary, theme color, sidebar labels, and page title overrides
4. run `python3 scripts/theme-park.py family-create --config families/field-ops.json`
5. run `node scripts/capture-previews.mjs --starter field-ops-jinja`
6. run `node scripts/capture-previews.mjs --starter field-ops-static`
7. run `python3 scripts/theme-park.py build-catalog`

## Example Workflow: Shared Abstraction Extraction

Use AI to:

1. compare two or more site families
2. identify repeated site-local HTML, config, or behavior
3. move only broadly reusable structure into `packages/`
4. keep family-specific wording and information architecture inside `sites/`
5. rebuild affected starters and verify previews still work

## Verification Checklist

After any AI-assisted change:

- preview the changed starter with `scripts/preview-starter.sh`
- rebuild static starters if static templates changed
- refresh the catalog if starter metadata changed
- confirm tracked files are still public-safe
- confirm the AI did not move site-specific files into `packages/` unnecessarily
