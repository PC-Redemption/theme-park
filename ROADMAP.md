# Theme Park Roadmap

## Purpose

Build a public repo of reusable starter web site layouts with:

- a shared design system
- isolated starter-site directories
- a documented integration contract
- repeatable extraction and publishing workflows

This repo should become the single place to point people to when they need a starter web shell or layout.

## North Star

A contributor should be able to:

1. choose a starter site from `sites/`
2. understand its purpose from its local `README.md`
3. swap branding, nav, permissions, and content without editing framework internals
4. add a new starter site without disturbing existing ones

## Principles

- shared framework code lives in `packages/`
- each starter site lives in its own clearly named folder under `sites/`
- product content and business logic never enter the shared framework
- starter sites prove the framework, but do not define it
- extraction decisions favor reusable abstractions over source-layout fidelity

## Target Shape

```text
theme_park/
  packages/
    design-system/
  sites/
    operations-shell-jinja/
    operations-shell-static/
    settings-portal-jinja/
    settings-portal-static/
    review-studio-jinja/
    review-studio-static/
    admin-dashboard/
    review-workflow/
  docs/
```

## Roadmap Phases

### Phase 0: Repo foundation

Goal:

- create the public repo structure and contribution rules

Outputs:

- baseline directory structure
- root `README.md`
- contribution guidance
- naming rules for starter sites
- starter documentation format

Exit criteria:

- repo structure is committed
- docs explain the split between `packages/` and `sites/`
- at least one empty starter-site slot is defined by convention

### Phase 1: Source inventory and extraction map

Goal:

- understand the source app and classify everything before extraction

Outputs:

- component inventory
- token inventory
- layout inventory
- extraction map marking `extract`, `adapt`, or `discard`

Exit criteria:

- source artifacts are categorized by framework, shell, content, or discard
- risky coupling points are documented
- repeated patterns are identified before code moves

### Phase 2: Design-system core

Goal:

- establish reusable framework primitives

Outputs:

- theme tokens
- base styles
- shared interaction scripts
- core components

Exit criteria:

- buttons, cards, badges, tables, forms, alerts, and empty states exist as reusable primitives
- tokens are centralized and documented
- framework primitives contain no product wording

### Phase 3: First starter-site extraction

Goal:

- turn the first extracted private source shell into the first publishable starter pair

Outputs:

- `sites/operations-shell-jinja/`
- `sites/operations-shell-static/`
- generic layouts and scaffolds
- branding, nav, permissions, and route config hooks

Exit criteria:

- the starters run without original product code
- product-specific labels are removed
- framework and site boundaries are obvious in the filesystem

### Phase 4: Integration contract

Goal:

- make the framework usable without reading internal implementation details

Outputs:

- integration docs
- starter-site authoring rules
- extension and override points

Exit criteria:

- a new contributor can wire a starter site from docs alone
- the contract for branding, nav, permissions, and routes is stable enough to reuse

### Phase 5: Multi-starter expansion

Goal:

- prove the repo supports multiple distinct starters cleanly

Outputs:

- at least one additional starter family with separate site directories
- shared abstractions refined from real reuse
- starter comparison docs

Exit criteria:

- adding a second or third starter does not require restructuring the repo
- starter-specific code stays local to each site
- framework reuse increases while duplicated site code decreases

### Phase 6: Public release hardening

Goal:

- prepare the repo for public consumption

Outputs:

- sanitization pass
- licensing and attribution review
- onboarding docs
- example screenshots or demos

Exit criteria:

- no private content remains
- naming is generic and publishable
- docs are strong enough for outside users

## Workstreams

- Framework: tokens, primitives, component APIs, JS helpers
- Site Extraction: source review, scaffold creation, generic rewrites
- Documentation: runbooks, contracts, starter-site READMEs
- Publishing: sanitization, licensing, release packaging

## Risks

- source templates may mix content and structure too tightly
- visual patterns may look generic until a stronger design language is established
- framework APIs may become too source-shaped if extraction moves too fast
- future starter sites may diverge unless directory and contract rules stay strict

## Success Measures

- one shared framework can support multiple site starters
- each starter site is identifiable by folder, docs, and purpose
- branding and nav changes happen through config
- no product code is required to use a starter
- new starters can be added with low friction
