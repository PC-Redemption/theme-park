#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from packages.design_system.control_plane import (  # type: ignore
    apply_family_spec,
    build_catalog_payload,
    copy_starter,
    create_family,
    discover_starters,
    export_starter_bundle,
    families_dir,
    load_family_spec,
    write_json,
)
from packages.design_system.integration.static_site_builder import build_static_site  # type: ignore


def cmd_build_catalog(_: argparse.Namespace) -> int:
    catalog_dir = ROOT / "catalog"
    output = catalog_dir / "starters.json"
    output.write_text(json.dumps(build_catalog_payload(), indent=2) + "\n")
    print(f"Wrote {output}")
    return 0


def cmd_build_static(args: argparse.Namespace) -> int:
    starters = discover_starters()
    for starter in starters:
        if starter.runtime != "static":
            continue
        if args.starter and starter.key != args.starter:
            continue
        build_static_site(starter.site_dir)
        print(f"Built {starter.site_dir.name}")
    return 0


def cmd_starter_copy(args: argparse.Namespace) -> int:
    created = copy_starter(
        source_key=args.source,
        dest_key=args.dest,
        name=args.name,
        summary=args.summary,
        family=args.family,
    )
    print(f"Created {created}")
    return 0


def cmd_family_create(args: argparse.Namespace) -> int:
    config = {}
    if args.config:
        config = load_family_spec(Path(args.config))

    created = create_family(
        seed_family=args.seed_family or config["seed_family"],
        family=args.family or config["family"],
        site_slug=args.site_slug or config["site_slug"],
        display_name=args.display_name or config.get("display_name"),
        summary=args.summary or config.get("summary"),
        runtime_overrides=config.get("runtime_overrides"),
    )
    for path in created:
        print(f"Created {path}")
    return 0


def cmd_family_spec_init(args: argparse.Namespace) -> int:
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "seed_family": args.seed_family,
        "family": args.family,
        "site_slug": args.site_slug,
        "display_name": args.display_name,
        "summary": "Describe the new family in public-safe terms.",
        "runtime_overrides": {
            "jinja": {
                "theme_color": "blue",
                "sidebar_title": "Primary Navigation",
                "page_kicker": "Jinja starter",
                "badge_labels": [
                    {"label": "Jinja", "tone": "neutral"},
                    {"label": "Custom", "tone": "success"},
                ],
                "page_titles": {},
            },
            "static": {
                "theme_color": "blue",
                "sidebar_title": "Primary Navigation",
            },
        },
    }
    write_json(output, payload)
    print(f"Wrote {output}")
    return 0


def cmd_family_sync(args: argparse.Namespace) -> int:
    config = load_family_spec(Path(args.config))
    updated = apply_family_spec(config)
    for path in updated:
        print(f"Updated {path}")
    return 0


def cmd_starter_export(args: argparse.Namespace) -> int:
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    bundle = export_starter_bundle(starter_key=args.starter, output_dir=output)
    print(f"Exported {bundle}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Theme Park control-plane workflows")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_catalog = subparsers.add_parser("build-catalog", help="Build the starter catalog JSON")
    build_catalog.set_defaults(func=cmd_build_catalog)

    build_static = subparsers.add_parser("build-static", help="Build one or all static starters")
    build_static.add_argument("--starter", help="Starter key to build")
    build_static.set_defaults(func=cmd_build_static)

    starter_copy = subparsers.add_parser("starter-copy", help="Copy an existing starter into a new site folder")
    starter_copy.add_argument("--source", required=True, help="Existing starter key")
    starter_copy.add_argument("--dest", required=True, help="New starter key")
    starter_copy.add_argument("--name", help="New starter display name")
    starter_copy.add_argument("--summary", help="New starter summary")
    starter_copy.add_argument("--family", help="Override family slug")
    starter_copy.set_defaults(func=cmd_starter_copy)

    family_create = subparsers.add_parser("family-create", help="Create a new starter family from an existing seed family")
    family_create.add_argument("--config", help="Path to a family spec JSON file")
    family_create.add_argument("--seed-family", help="Existing family slug to clone from")
    family_create.add_argument("--family", help="New family slug")
    family_create.add_argument("--site-slug", help="Base site slug for new starter keys")
    family_create.add_argument("--display-name", help="Display name prefix for the new family")
    family_create.add_argument("--summary", help="Summary to apply to generated starters")
    family_create.set_defaults(func=cmd_family_create)

    family_spec_init = subparsers.add_parser("family-spec-init", help="Write a family spec template JSON file")
    family_spec_init.add_argument("--output", default=str(families_dir() / "new-family.json"), help="Output path for the generated spec")
    family_spec_init.add_argument("--seed-family", default="operations", help="Seed family for the template")
    family_spec_init.add_argument("--family", default="new-family", help="Family slug for the template")
    family_spec_init.add_argument("--site-slug", default="new-family", help="Site slug for the template")
    family_spec_init.add_argument("--display-name", default="New Family", help="Display name for the template")
    family_spec_init.set_defaults(func=cmd_family_spec_init)

    family_sync = subparsers.add_parser("family-sync", help="Apply a family spec to an existing generated family")
    family_sync.add_argument("--config", required=True, help="Path to a family spec JSON file")
    family_sync.set_defaults(func=cmd_family_sync)

    starter_export = subparsers.add_parser("starter-export", help="Export a minimal bundle for a single starter")
    starter_export.add_argument("--starter", required=True, help="Starter key to export")
    starter_export.add_argument("--output", default="dist/starter-bundles", help="Directory that will receive the exported starter bundle")
    starter_export.set_defaults(func=cmd_starter_export)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
