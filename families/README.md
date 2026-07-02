# Family Specs

This directory holds reusable family-generation specs for the Theme Park control plane.

Use these files when you want to stamp out a new starter family with runtime-specific overrides instead of cloning a seed family by hand.

## Create A Spec Template

```bash
python3 scripts/theme-park.py family-spec-init --output families/my-family.json
```

## Generate A Family From A Spec

```bash
python3 scripts/theme-park.py family-create --config families/my-family.json
```

## Rules

- keep family specs public-safe
- treat them as reusable starter-generation inputs, not site content
- prefer generic labels and summaries that can ship in a public repo
