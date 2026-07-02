# Next Decision Gate

## Why Work Pauses Here

The repo now contains:

- shared tokens
- shared shell CSS and JavaScript
- shared Jinja-style templates and component macros
- a Jinja starter implementation
- a static starter implementation
- example shell and scaffold contracts

The runtime split has been provided both ways, and both preview paths now exist. The earlier workflow question has been resolved in favor of `.venv` plus small preview scripts.

## Decision Made

Chosen workflow:

1. lightweight local workflows using `.venv`, `requirements.txt`, and small preview scripts

## Why This Matters

This choice affects:

- how contributors install dependencies
- how previews are run and verified consistently
- how future runtime-backed starters should onboard into the repo
- how much runtime convenience the public repo promises by default

## Current Assumption

The repo now supports both a Jinja-first path and a static path, and both were smoke-tested locally. Contributor workflow is now standardized around small local scripts.

## Next Blocker

The next blocker is no longer tooling policy. It is deciding how far to take the runnable-example layer:

1. keep previews lightweight and stop at starter demos
2. add a more polished root-level developer experience such as a single launcher or task runner
3. start building a second family of starters to pressure-test the shared design system
