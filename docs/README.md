# Docs

This directory holds public-facing documentation for consuming and extending Theme Park.

## Start Here

- [preview-workflows.md](./preview-workflows.md) for local preview commands
- [starter-catalog.md](./starter-catalog.md) for the current starter families
- [exports.md](./exports.md) for exporting a single starter bundle
- [integration-contract.md](./integration-contract.md) for shared configuration points
- [ai-workflows.md](./ai-workflows.md) for using AI tools to create or modify starters
- [ai-guardrails.md](./ai-guardrails.md) for safe edit rules when using an AI agent
- [prompt-recipes.md](./prompt-recipes.md) for copy-paste prompts

## Reference Docs

- [reference/README.md](./reference/README.md) for extraction provenance and source-analysis materials

## Repo Shape

- `packages/` contains the shared design system and integration helpers
- `sites/` contains isolated starter implementations
- `families/` contains reusable family-generation specs
- `catalog/` contains the root control plane and live preview catalog

## Package Split

Two similarly named package paths are intentional:

- `packages/design-system/` holds shared front-end assets such as CSS, JavaScript, tokens, and Jinja templates
- `packages/design_system/` holds Python importable integration helpers

The hyphenated path is for repo assets. The underscored path is for Python module imports.
