#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from packages.design_system.control_plane import (  # type: ignore
    build_catalog_payload,
    copy_starter,
    create_family,
    discover_starters,
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
    created = create_family(
        seed_family=args.seed_family,
        family=args.family,
        site_slug=args.site_slug,
        display_name=args.display_name,
        summary=args.summary,
    )
    for path in created:
        print(f"Created {path}")
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
    family_create.add_argument("--seed-family", required=True, help="Existing family slug to clone from")
    family_create.add_argument("--family", required=True, help="New family slug")
    family_create.add_argument("--site-slug", required=True, help="Base site slug for new starter keys")
    family_create.add_argument("--display-name", help="Display name prefix for the new family")
    family_create.add_argument("--summary", help="Summary to apply to generated starters")
    family_create.set_defaults(func=cmd_family_create)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
