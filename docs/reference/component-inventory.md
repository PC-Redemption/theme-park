# Component Inventory

This document tracks reusable components and source patterns discovered during extraction.

## Status

- initial source inventory complete for the private home-shell surface

## Reusable Component Candidates

| Source artifact | Category | Reuse candidate | Action | Notes |
| --- | --- | --- | --- | --- |
| `templates/newhome/components/badges.html` | badge | yes | extract | generic label and tone pattern |
| `templates/newhome/components/buttons.html` | button | yes | extract | action-button primitive needs generic naming |
| `templates/newhome/components/cards.html` | card | yes | extract | includes status and contract-card variants |
| `templates/newhome/components/tables.html` | table | yes | extract | data-view and empty-row patterns |
| `templates/newhome/components/alerts.html` | alert | yes | extract | tone-based alert primitive |
| `templates/newhome/components/status.html` | status | yes | extract | compact and full status indicators |
| `templates/newhome/components/modals.html` | modal | yes | extract | placeholder modal shell is reusable |
| `templates/newhome/components/icons.html` | icon set | yes | adapt | keep generic icons, drop brand- or product-only shapes |
| `templates/newhome/partials/empty_state.html` | empty state | yes | extract | good candidate for starter-safe placeholder UI |
| `templates/newhome/partials/error_panel.html` | error panel | yes | extract | reusable failure-state presentation |
| `templates/newhome/partials/foundation_status.html` | status panel | yes | adapt | likely reusable after removing source wording |
| `templates/newhome/components/use_cases.html` | scaffold helper | yes | adapt | useful for starter scaffolds, not low-level component API |

## Layout And Shell Candidates

| Source artifact | Category | Reuse candidate | Action | Notes |
| --- | --- | --- | --- | --- |
| `templates/newhome/base.html` | app base | yes | extract | document head contract, theme initialization, and static hooks |
| `templates/newhome/shell.html` | app shell | yes | adapt | header, nav, content frame, footer, menus, and popouts |
| `static/newhome/newhome.css` | shell styles | yes | extract | contains token seed data plus shell, component, and scaffold styling |
| `static/newhome/newhome.js` | shell behavior | yes | extract | theme controls, nav collapse, app switcher, account menu, toasts, header status |

## Scaffold Candidates

| Source artifact | Category | Reuse candidate | Action | Notes |
| --- | --- | --- | --- | --- |
| `templates/newhome/use_cases/overview_dashboard.html` | dashboard scaffold | yes | adapt | becomes a generic operations dashboard starter |
| `templates/newhome/use_cases/master_detail.html` | list-detail scaffold | yes | adapt | core split-pane browsing pattern |
| `templates/newhome/use_cases/workflow_procedure.html` | workflow scaffold | yes | adapt | maps to guided review or approval flows |
| `templates/newhome/use_cases/setup_configuration.html` | settings scaffold | yes | adapt | useful as admin/settings starter shell |
| `templates/newhome/use_cases/live_monitor.html` | monitoring scaffold | yes | adapt | can seed live status or monitoring layouts |
| `templates/newhome/use_cases/results_report.html` | results scaffold | maybe | review later | may belong in a later starter rather than the first shell |
| `templates/newhome/use_cases/reference_library.html` | reference scaffold | maybe | review later | likely useful once the docs surface is clearer |
| `templates/newhome/use_cases/admin_maintenance.html` | maintenance scaffold | maybe | review later | likely overlaps with settings/admin shell |

## Site-Local Or Business-Coupled Areas

| Source artifact | Category | Reuse candidate | Action | Notes |
| --- | --- | --- | --- | --- |
| `templates/newhome/apps/labview_ingest.html` | app page | no | keep site-local or discard | deeply tied to source workflows |
| `templates/newhome/apps/probe_maps.html` | app page | no | keep site-local or discard | source-specific domain UI |
| `templates/newhome/apps/thermoscopestorm.html` | app page | no | keep site-local or discard | product-specific monitoring surface |
| `templates/settings/*.html` | admin app templates | partial | selective extraction | mine only generic table/form/layout patterns |
| `static/shared/specops*.css/js` | shared legacy assets | partial | inspect later | likely mixed generic and product-specific concerns |
| `settings_app.py` app routes and handlers | backend logic | no | discard from framework | use only as contract reference |

## Immediate Extraction Priorities

1. lift tokens from `static/newhome/newhome.css`
2. isolate shell behaviors from `static/newhome/newhome.js`
3. extract component macros under `templates/newhome/components/`
4. adapt `base.html` and `shell.html` into starter-safe framework templates
5. convert use-case templates into generic starter scaffolds
