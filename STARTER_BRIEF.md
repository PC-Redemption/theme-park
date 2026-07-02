# Reusable UI Framework Extraction Brief

## Objective

Build a public reusable starter-site repo by extracting the non-content parts of a private internal home site into a framework/design-system package plus a clearly separated starter site.

The resulting repo should preserve reusable structure and interaction patterns while removing product-specific content, business logic, and deployment-specific coupling.

The repo must be organized so that each starter site remains separate, identifiable, and easy to extend without mixing its files into other starters.

Treat the source app as three layers:

1. framework
2. app shell
3. product content

Extract only layers `1` and `2`.

## Scope

Include:

- theme tokens: colors, spacing, typography, borders, shadows, radii
- reusable UI components: buttons, badges, cards, tables, forms, alerts, empty states
- layout shell: header, sidebar, footer, page container, section header, action bar
- behavior patterns: modals, tabs, accordions, loading states, confirmation states
- page scaffolds: dashboard, list/detail, settings, review workflow shells
- config hooks for nav, branding, permissions, and route registration

Do not include:

- site-specific content
- product-specific routes
- business logic
- app-specific database/API coupling
- hardcoded labels that belong to one deployment

## Source Of Truth

Study these source-app areas:

- reverse proxy configuration
- application settings
- templates
- static assets
- site/application code

## Current Constraint

The private source tree is not mounted in the current environment, so extraction work cannot be validated from this workspace yet.

Before implementation starts, confirm that the source tree is available in the execution environment or provide an alternate mounted path.

## Expected Outcome

Produce:

- a standalone public repo for reusable starter web site layouts
- a clear separation between framework assets and app content
- a starter/example site proving the shell works without the original product code
- app configuration points for branding, nav, and permissions
- a file structure where each site lives in its own clearly named directory

## Extraction Order

Follow this order:

1. theme tokens
2. shared CSS/JS primitives
3. reusable templates/components
4. shell layout
5. page scaffolds
6. app integration contract

## Design Rule

Optimize for reusable structure, not for preserving the original file layout. The output should feel like a framework, not like a copied app with content removed.

## Implementation Guidance For The Next Codex

### Primary job

Reverse-engineer the source app into a reusable shell package, then prove the abstraction with a minimal example app.

### What to preserve

- visual system primitives
- layout composition patterns
- generic interaction patterns
- template/component ergonomics
- extensibility points for apps consuming the shell

### What to strip out aggressively

- deployment naming
- product nouns
- one-off page copy
- workflow-specific decisions that are not reusable
- direct API, ORM, or backend assumptions

## Suggested Target Repo Shape

Use a framework-oriented structure rather than mirroring the source app, and keep every starter site isolated in its own directory:

```text
theme_park/
  packages/
    design-system/
      tokens/
      styles/
      scripts/
      components/
      integration/
  sites/
    operations-shell-jinja/
      layouts/
      templates/
      scaffolds/
      app_config/
      routes/
      static/
      README.md
    operations-shell-static/
      layouts/
      templates/
      scaffolds/
      app_config/
      routes/
      static/
      README.md
    future-site-name/
      layouts/
      templates/
      scaffolds/
      app_config/
      routes/
      templates/
      static/
      README.md
  docs/
    extraction-notes/
    integration-contract.md
    component-inventory.md
```

Each site directory should be recognizable on sight and should contain only what is needed for that starter.

If the stack suggests a better packaging layout after inspection, keep the same conceptual split:

- shared framework package
- separate starter-site directories
- docs describing the integration contract

## Concrete Deliverables

### 1. Framework package

Create a reusable package containing:

- design tokens
- shared CSS primitives
- shared JS behavior helpers
- reusable templates/components
- shell layout primitives
- scaffold pages with placeholder content only

### 2. Starter site

Create thin starter implementations that demonstrate:

- branding injection
- nav registration
- permission-aware navigation or actions
- route registration
- replacement of placeholder page content without modifying framework internals

Each starter implementation should live in its own top-level site directory rather than inside the framework package.

### 3. Integration contract

Document the contract for consumers:

- branding configuration
- navigation schema
- permission hook/interface
- route registration expectations
- component override or extension points

## Required Separation

The next Codex should make the separation explicit in code:

- framework code must not import product code
- scaffold pages must use fake or placeholder content only
- configuration must drive branding, labels, and nav
- permissions must be injected through config or adapter hooks
- each starter site must be isolated in its own directory with its own templates, static assets, and config surface

## Review Checklist

Use this as the acceptance gate:

- no product-specific copy remains in framework assets
- no source-app business logic is required to render the shell
- nav can be changed by configuration
- branding can be changed by configuration
- permissions can be changed by configuration or adapter
- starter site runs independently of the original product code
- reusable components are extracted into stable primitives rather than page-specific fragments
- page scaffolds are generic and reusable
- a new starter site can be added without restructuring existing starter directories

## Working Notes

- Start with an inventory pass before moving files.
- Build a mapping from source artifact to destination category: token, primitive, component, shell, scaffold, or discard.
- Rename aggressively toward generic terminology when source names leak product intent.
- Prefer creating smaller stable abstractions over preserving large source templates.
- Keep placeholders obviously generic so future apps can replace them cleanly.
- Keep starter-site boundaries obvious in the filesystem so contributors can tell shared framework code from site-specific starter code immediately.

## First Steps When Source Is Available

1. Inspect the source tree and inventory templates, static assets, and settings.
2. Classify each artifact as framework, shell, content, or discard.
3. Extract tokens and primitives first.
4. Build reusable components from repeated patterns.
5. Recompose the shell layout around configuration hooks.
6. Build scaffold pages using placeholders only.
7. Wire a minimal example app to prove the contract.
8. Document the integration surface and extraction decisions.
