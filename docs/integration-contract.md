# Integration Contract

This document defines how starter sites consume the shared framework.

## Contract Areas

- branding configuration
- navigation schema
- permissions hook
- route registration
- component override points

## Initial Draft

### Branding

Starter sites should provide:

- product or site name
- logo asset path
- favicon asset path
- default theme mode
- default accent theme

### Navigation

Starter sites should provide:

- breadcrumb items
- primary or focused navigation items
- grouped app-switcher items
- active-nav key

### Shell Status

The framework shell should accept injected status summaries for:

- system status
- notification status
- audit or review context
- live connection state

The framework should not hardcode polling endpoints. Sites should register adapters or URLs.

### Page Frame

Starter pages should provide:

- page kicker
- page title
- page subtitle
- page badges
- page status indicators
- page actions

### Permissions

Starter sites should inject a permission context that controls:

- visibility of nav items
- availability of actions
- read-only or blocked states for forms and workflows

### Route Registration

Starter sites should register:

- shell routes
- scaffold routes
- optional site-local partial or action routes

The shared framework should not own product routes.

### Override Points

The framework should expose override-friendly areas for:

- header brand region
- nav configuration
- status-summary data
- footer metadata
- scaffold content blocks

## Status

- initial draft created from first source inventory
