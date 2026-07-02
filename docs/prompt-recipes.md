# Prompt Recipes

These prompts are meant to be copied into an AI coding tool with this repo checked out locally.

Adjust the starter keys, family names, and summaries to fit your case.

## Create A New Starter From An Existing Starter

```text
Create a new starter by copying `operations-shell-jinja` into `field-ops-jinja`.
Keep the repo structure intact.
Use the existing control-plane workflows instead of hand-copying files where possible.
Update starter-local branding, summary, and README copy to be public-safe and generic.
Do not change unrelated starters.
Preview the result and report what changed.
```

## Create A New Family From A Spec

```text
Create a new family spec at `families/field-ops.json` using `operations` as the seed family.
Set a distinctive public-safe summary, theme color, sidebar title, and page-title overrides.
Generate the family from that spec, refresh the starter catalog, and capture live screenshots for the new starters.
Do not alter existing families unless the shared generator must change.
```

## Sync Changes Into An Existing Family

```text
Update the family spec at `families/mission-control.json` so the sidebar labels and badge labels better match a coordination dashboard.
Reapply the spec with the family sync workflow.
Refresh only the affected screenshots and rebuild the catalog.
Keep the change limited to that family unless shared code truly needs an update.
```

## Export A Starter Bundle

```text
Export a minimal bundle for `release-hub-jinja` using the repo's starter export workflow.
Verify the exported bundle includes the shared packages and starter-local files it needs.
Do not modify unrelated starter families.
```

## Extract A Shared Abstraction

```text
Compare `mission-control-*` and `release-hub-*` for repeated structural patterns.
If at least two starters share the same non-content pattern, extract it into `packages/`.
Keep family-specific wording and navigation local to each starter.
Rebuild or preview affected starters and summarize the risk of the abstraction.
```
