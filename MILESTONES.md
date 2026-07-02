# Theme Park Milestones

## Milestone 1: Public repo skeleton

Outcome:

- create the repo structure for `packages/`, `sites/`, and `docs/`

Tasks:

- define naming convention for starter sites
- define README template for each site
- define design-system package boundary

Done when:

- the repo reads like a framework project rather than an extracted app

## Milestone 2: Extraction inventory complete

Outcome:

- produce a complete map of what to extract, adapt, or discard from the source app

Tasks:

- inspect `settings_app.py`, templates, static assets, and site code
- classify artifacts into token, primitive, component, layout, scaffold, content, or discard
- note coupling to routes, permissions, backend logic, or deployment assumptions

Done when:

- the team can point to a written extraction map instead of making ad hoc decisions

## Milestone 3: Design tokens and primitives

Outcome:

- establish a stable shared visual and interaction base

Tasks:

- extract colors, spacing, typography, borders, radii, and shadows
- create shared CSS primitives
- create reusable JS helpers for tabs, modals, accordions, and loading states

Done when:

- starter-site pages can be assembled from shared primitives without source-product imports

## Milestone 4: Core components

Outcome:

- ship the first reusable component set

Tasks:

- build buttons, badges, cards, tables, forms, alerts, and empty states
- document expected inputs and override points
- normalize component names to generic terms

Done when:

- repeated UI fragments in the source app are represented as reusable components

## Milestone 5: First starter implementations

Outcome:

- publish the first isolated starter implementations under `sites/operations-shell-jinja/` and `sites/operations-shell-static/`

Tasks:

- build shell layout
- create generic page scaffolds
- wire branding, nav, permissions, and routes through config
- replace source content with placeholders

Done when:

- each implementation feels like a reusable starter rather than a cleaned copy of the source app

## Milestone 6: Integration contract

Outcome:

- document how people consume the framework and build new starters

Tasks:

- document branding contract
- document nav schema
- document permissions hook
- document route registration
- document extension rules for site-specific assets

Done when:

- another Codex or contributor can build a second starter site without reverse-engineering the first one

## Milestone 7: Second and third starter sites

Outcome:

- prove the repo supports a growing catalog of starters

Tasks:

- create two more starter sites from either extracted or newly authored shells
- reuse framework pieces aggressively
- keep site-local assets and docs within each site directory

Done when:

- the multi-site repo structure holds up under real variation

Current evidence:

- `operations-shell-jinja`
- `operations-shell-static`
- `settings-portal-jinja`
- `settings-portal-static`

## Milestone 8: Public launch

Outcome:

- make the repo safe and useful for outside consumers

Tasks:

- run final sanitization
- review licensing
- improve root docs and examples
- add screenshots or demo references

Done when:

- you can confidently share the repo as the default starting point for starter web layouts

## Sequencing

1. Milestone 1
2. Milestone 2
3. Milestone 3
4. Milestone 4
5. Milestone 5
6. Milestone 6
7. Milestone 7
8. Milestone 8

## Decision Gates

- Gate A after Milestone 2: confirm the source is extractable without private leakage
- Gate B after Milestone 4: confirm the design-system API is generic enough
- Gate C after Milestone 5: confirm the first starter is truly isolated
- Gate D after Milestone 7: confirm the repo structure scales to multiple starters
