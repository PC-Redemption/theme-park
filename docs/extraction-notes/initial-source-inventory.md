# Initial Source Inventory

## Scope Reviewed

The initial inventory covered:

- application settings and route file
- `templates/newhome`
- `templates/settings`
- `static/newhome`
- `static/settings`
- `static/shared`

## High-Level Findings

### 1. The private source already separates a modern shell from older settings pages

The `newhome` area is the best extraction target for the first starter because it already has:

- a base template
- a shell template
- component macro files
- partials
- use-case scaffolds
- a dedicated CSS file
- a dedicated JS file

### 2. The shell has a useful framework contract shape

The shell template shows reusable hooks for:

- branding
- breadcrumb navigation
- app switcher groups
- focused navigation
- page heading
- page badges
- page status indicators
- user menu
- system status
- notification status
- audit context
- theme settings

This is a strong fit for a configuration-driven starter framework.

### 3. Theme support is already abstraction-friendly

The CSS and base template reveal a usable token model:

- light and dark modes
- multiple accent color themes
- named surface, text, border, shadow, and state colors
- shell dimensions such as nav width and topbar/footer heights

This should become the starting point for `packages/design-system/tokens/`.

### 4. JS behavior is largely reusable

The `newhome.js` file contains mostly framework-friendly shell behavior:

- theme persistence
- toasts
- action handling
- auto-submit forms
- picker modals
- theme controls
- app switcher
- account menu
- focused-nav collapse and resize behavior
- header status polling and popouts
- live-state handling

Some of these should become generic primitives, while source-service polling details should be pushed behind adapters.

### 5. The route file is heavily business-coupled

The main application file exposes a large mix of:

- shell routes
- app-specific routes
- settings and auth routes
- notification routes
- domain-specific actions
- health and API endpoints

This file should be treated as a reference for page contracts and extension points, not as framework code to copy.

## Proposed Classification

### Extract to shared framework

- token values and theme modes
- topbar, sidebar, footer, content-frame layout
- generic UI components
- generic shell JavaScript
- page scaffolds

### Keep in first starter site

- starter-specific information architecture
- first starter nav tree
- starter-specific scaffold composition
- starter-local static assets and docs

### Discard or replace

- product names
- internal hostnames
- domain-specific routes
- backend workflow logic
- product-specific imagery

## Risks

- the current CSS bundles shell, components, and app-specific styling together, so extraction will require deliberate splitting
- local storage keys and data attributes are product-named and need renaming
- header-status polling is reusable as a pattern but not as a hardcoded endpoint contract
- legacy settings templates may tempt over-extraction; only generic form and table patterns should move

## Recommended Next Build Step

Start implementing the shared token layer and shell contract based on the `newhome` assets, while keeping app-specific pages and service endpoints out of the framework.
