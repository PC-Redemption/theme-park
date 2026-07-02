# AI Guardrails

Use these rules when an AI agent edits Theme Park.

## Safe Boundaries

AI should treat the repo like this:

- `packages/` is for shared framework code
- `sites/` is for site-local starter code
- `families/` is for reusable family-generation specs
- `catalog/` is for the root control plane and preview experience
- `docs/` is for public-facing documentation

## What AI Should Avoid

- do not add private credentials, hostnames, tokens, or internal paths
- do not mix one starter's files into another starter directory
- do not move site-local copy or information architecture into shared packages unless it is clearly reused
- do not invent business logic, backend APIs, or database coupling
- do not rewrite working starter families just to make them structurally uniform

## Preferred Edit Rules

- prefer `scripts/theme-park.py` workflows over hand-copying starter trees
- prefer editing family specs in `families/` over ad hoc changes when a family is meant to be repeatable
- prefer `sites/<starter-key>/README.md` for starter-local explanation
- prefer shared abstractions only when at least two starters benefit without awkward renaming

## Public Safety Rules

Everything tracked in git should be safe for a public repository.

AI should:

- use placeholder content
- keep examples generic
- avoid product-specific language unless it is intentionally part of a starter theme
- check generated docs for operator-only assumptions

## When To Put Code In `packages/`

Put code in `packages/` only when it is:

- visual infrastructure
- shared interaction logic
- shared template primitives
- shared integration helpers

Keep it site-local when it is:

- a family-specific workflow shell
- a family-specific navigation model
- a starter-specific content scaffold
- a one-off layout variation not yet reused elsewhere
