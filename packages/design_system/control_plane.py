from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUNTIME_ORDER = ("jinja", "static")

FAMILY_ACCENTS = {
    "operations": "#17617f",
    "settings": "#2f7b47",
    "review": "#6652a6",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sites_dir() -> Path:
    return repo_root() / "sites"


def families_dir() -> Path:
    return repo_root() / "families"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def runtime_label(runtime: str) -> str:
    return runtime.replace("-", " ").title()


def title_case_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("_", "-").split("-") if part)


def merge_dict(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge_dict(base[key], value)
        else:
            base[key] = value
    return base


@dataclass
class StarterManifest:
    key: str
    name: str
    family: str
    runtime: str
    summary: str
    strengths: list[str]
    preview: dict[str, Any]
    paths: dict[str, str]
    manifest_path: Path

    @property
    def site_dir(self) -> Path:
        return self.manifest_path.parent

    @property
    def preview_path(self) -> str:
        return self.preview.get("path") or "/"

    def preview_url(self, port: int = 8000, host: str = "127.0.0.1") -> str:
        return f"http://{host}:{port}{self.preview_path}"

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "key": self.key,
            "name": self.name,
            "family": self.family,
            "runtime": self.runtime,
            "summary": self.summary,
            "strengths": self.strengths,
            "preview": dict(self.preview),
            "paths": self.paths,
        }
        payload["preview"]["url"] = self.preview_url()
        payload["preview"]["script"] = self.preview.get("script", f"scripts/preview-starter.sh {self.key}")
        payload["commands"] = {
            "preview": f"scripts/preview-starter.sh {self.key}",
            "copy": f"python3 scripts/theme-park.py starter-copy --source {self.key} --dest your-new-key",
            "screenshot": f"node scripts/capture-previews.mjs --starter {self.key}",
        }
        return payload


def discover_starters() -> list[StarterManifest]:
    manifests = []
    for path in sorted(sites_dir().glob("*/starter.manifest.json")):
        payload = load_json(path)
        manifests.append(StarterManifest(manifest_path=path, **payload))
    manifests.sort(key=lambda item: (item.family, RUNTIME_ORDER.index(item.runtime), item.key))
    return manifests


def starter_by_key(key: str) -> StarterManifest:
    for starter in discover_starters():
        if starter.key == key:
            return starter
    raise ValueError(f"Starter '{key}' was not found.")


def family_groups(starters: list[StarterManifest]) -> dict[str, dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for starter in starters:
        family = groups.setdefault(
            starter.family,
            {
                "label": title_case_slug(starter.family),
                "accent": FAMILY_ACCENTS.get(starter.family, "#17617f"),
                "starters": [],
                "runtimes": set(),
                "strengths": set(),
            },
        )
        family["starters"].append(starter.key)
        family["runtimes"].add(starter.runtime)
        family["strengths"].update(starter.strengths[:4])

    for family in groups.values():
        family["runtimes"] = sorted(family["runtimes"], key=RUNTIME_ORDER.index)
        family["strengths"] = sorted(family["strengths"])
    return groups


def build_catalog_payload() -> dict[str, Any]:
    starters = discover_starters()
    families = family_groups(starters)
    starter_payloads = []
    for starter in starters:
        payload = starter.to_payload()
        image_path = repo_root() / "catalog" / "previews" / f"{starter.key}.png"
        if image_path.exists():
            payload["preview"]["image"] = f"./previews/{starter.key}.png"
        else:
            payload["preview"]["image"] = ""
        starter_payloads.append(payload)

    return {
        "generated_from": "sites/*/starter.manifest.json",
        "starter_count": len(starter_payloads),
        "families": families,
        "workflows": {
            "preview": "scripts/preview-starter.sh STARTER_KEY",
            "copy": "python3 scripts/theme-park.py starter-copy --source STARTER_KEY --dest NEW_KEY",
            "family_create": "python3 scripts/theme-park.py family-create --seed-family operations --family NEW_FAMILY --site-slug NEW_SITE",
            "family_sync": "python3 scripts/theme-park.py family-sync --config families/FAMILY.json",
            "export": "python3 scripts/theme-park.py starter-export --starter STARTER_KEY",
            "screenshots": "node scripts/capture-previews.mjs",
        },
        "starters": starter_payloads,
    }


def ensure_unique_starter_key(key: str) -> None:
    site_dir = sites_dir() / key
    if site_dir.exists():
        raise ValueError(f"Starter directory already exists: {site_dir}")


def copy_starter(
    *,
    source_key: str,
    dest_key: str,
    name: str | None = None,
    summary: str | None = None,
    family: str | None = None,
) -> Path:
    source = starter_by_key(source_key)
    ensure_unique_starter_key(dest_key)

    dest_dir = sites_dir() / dest_key
    shutil.copytree(source.site_dir, dest_dir)

    manifest_path = dest_dir / "starter.manifest.json"
    payload = load_json(manifest_path)
    payload["key"] = dest_key
    payload["name"] = name or title_case_slug(dest_key)
    payload["family"] = family or payload["family"]
    payload["summary"] = summary or payload["summary"]
    payload["preview"]["script"] = f"scripts/preview-starter.sh {dest_key}"
    payload["preview"]["path"] = payload["preview"].get("path", "/").replace(source.key, dest_key)
    payload["paths"]["site_dir"] = f"sites/{dest_key}"
    payload["paths"]["config"] = f"sites/{dest_key}/app_config"
    payload["paths"]["routes"] = f"sites/{dest_key}/routes"
    write_json(manifest_path, payload)

    _rewrite_readme(dest_dir / "README.md", source.key, dest_key, source.name, payload["name"])
    _rewrite_branding(dest_dir, payload["name"], payload["summary"], payload["runtime"])
    return dest_dir


def _rewrite_readme(path: Path, source_key: str, dest_key: str, source_name: str, dest_name: str) -> None:
    if not path.exists():
        return
    text = path.read_text()
    text = text.replace(source_key, dest_key).replace(source_name, dest_name)
    path.write_text(text)


def _rewrite_branding(site_dir: Path, starter_name: str, summary: str, runtime: str) -> None:
    if runtime == "static":
        config_path = site_dir / "app_config" / "site.example.json"
        payload = load_json(config_path)
        payload["branding"]["name"] = starter_name
        payload["summary"] = summary
        write_json(config_path, payload)
        return

    shell_path = site_dir / "app_config" / "shell.example.json"
    runtime_path = site_dir / "app_config" / "runtime.example.json"
    if shell_path.exists():
        payload = load_json(shell_path)
        payload["branding"]["name"] = starter_name
        payload["page_frame"]["title"] = starter_name.replace(" Jinja", "")
        payload["page_frame"]["subtitle"] = summary
        write_json(shell_path, payload)
    if runtime_path.exists():
        payload = load_json(runtime_path)
        payload["app_title"] = f"{starter_name} Demo"
        payload["footer_items"][0] = f"Starter: {site_dir.name}"
        write_json(runtime_path, payload)


def apply_family_runtime_overrides(site_dir: Path, runtime: str, overrides: dict[str, Any]) -> None:
    if not overrides:
        return

    if runtime == "static":
        config_path = site_dir / "app_config" / "site.example.json"
        payload = load_json(config_path)
        if "theme_color" in overrides:
            payload["branding"]["default_theme_color"] = overrides["theme_color"]
        if "theme_mode" in overrides:
            payload["branding"]["default_theme_mode"] = overrides["theme_mode"]
        if "sidebar_title" in overrides:
            payload["sidebar_title"] = overrides["sidebar_title"]
        if "summary" in overrides:
            payload["summary"] = overrides["summary"]
        if "navigation_labels" in overrides:
            label_map = overrides["navigation_labels"]
            for item in payload.get("navigation", []):
                if item["key"] in label_map:
                    item["label"] = label_map[item["key"]]
        write_json(config_path, payload)
        return

    shell_path = site_dir / "app_config" / "shell.example.json"
    runtime_path = site_dir / "app_config" / "runtime.example.json"
    shell_payload = load_json(shell_path)
    runtime_payload = load_json(runtime_path)

    if "theme_color" in overrides:
        shell_payload["branding"]["default_theme_color"] = overrides["theme_color"]
    if "theme_mode" in overrides:
        shell_payload["branding"]["default_theme_mode"] = overrides["theme_mode"]
    if "sidebar_title" in overrides:
        runtime_payload["sidebar_title"] = overrides["sidebar_title"]
    if "root_redirect" in overrides:
        runtime_payload["root_redirect"] = overrides["root_redirect"]
    if "badge_labels" in overrides:
        runtime_payload["badge_labels"] = overrides["badge_labels"]
    if "page_titles" in overrides:
        runtime_payload["page_titles"] = overrides["page_titles"]
    if "page_kicker" in overrides:
        shell_payload["page_frame"]["kicker"] = overrides["page_kicker"]
    if "summary" in overrides:
        shell_payload["page_frame"]["subtitle"] = overrides["summary"]
    if "navigation_labels" in overrides:
        label_map = overrides["navigation_labels"]
        for item in shell_payload["navigation"]["focused_nav"]:
            if item["key"] in label_map:
                item["label"] = label_map[item["key"]]

    write_json(shell_path, shell_payload)
    write_json(runtime_path, runtime_payload)


def load_family_spec(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    payload.setdefault("runtime_overrides", {})
    return payload


def apply_family_spec(spec: dict[str, Any]) -> list[Path]:
    updated = []
    site_slug = slugify(spec["site_slug"])
    display_name = spec.get("display_name") or title_case_slug(site_slug)
    summary = spec.get("summary") or f"Starter family derived from {spec['seed_family']}."
    family_slug = slugify(spec["family"])

    for runtime in RUNTIME_ORDER:
        site_dir = sites_dir() / f"{site_slug}-{runtime}"
        if not site_dir.exists():
            continue

        starter_name = f"{display_name} {runtime_label(runtime)}"
        manifest_path = site_dir / "starter.manifest.json"
        manifest = load_json(manifest_path)
        manifest["name"] = starter_name
        manifest["summary"] = summary
        manifest["family"] = family_slug
        write_json(manifest_path, manifest)

        _rewrite_branding(site_dir, starter_name, summary, runtime)
        apply_family_runtime_overrides(site_dir, runtime, spec.get("runtime_overrides", {}).get(runtime, {}))
        updated.append(site_dir)

    return updated


def export_starter_bundle(*, starter_key: str, output_dir: Path) -> Path:
    starter = starter_by_key(starter_key)
    bundle_root = output_dir / starter_key
    if bundle_root.exists():
        shutil.rmtree(bundle_root)

    (bundle_root / "packages").mkdir(parents=True, exist_ok=True)
    (bundle_root / "sites").mkdir(parents=True, exist_ok=True)
    (bundle_root / "scripts").mkdir(parents=True, exist_ok=True)

    shutil.copytree(repo_root() / "packages" / "design-system", bundle_root / "packages" / "design-system")
    shutil.copytree(repo_root() / "packages" / "design_system", bundle_root / "packages" / "design_system")
    shutil.copytree(starter.site_dir, bundle_root / "sites" / starter.key)

    for script_name in ("preview-starter.sh", "setup-venv.sh"):
        shutil.copy2(repo_root() / "scripts" / script_name, bundle_root / "scripts" / script_name)

    (bundle_root / "README.md").write_text(
        "\n".join(
            [
                f"# {starter.name} Export",
                "",
                f"This bundle contains the `{starter.key}` starter and the shared Theme Park packages it depends on.",
                "",
                "## Contents",
                "",
                "- `packages/design-system/` for shared CSS, JS, templates, and tokens",
                "- `packages/design_system/` for shared Python integration helpers",
                f"- `sites/{starter.key}/` for the starter-local site files",
                "- `scripts/preview-starter.sh` for local preview",
                "- `scripts/setup-venv.sh` for Python-backed starter environments",
                "",
                "## Quick Start",
                "",
                "```bash",
                "scripts/setup-venv.sh",
                f"scripts/preview-starter.sh {starter.key}",
                "```",
                "",
            ]
        )
        + "\n"
    )

    return bundle_root


def seed_family_keys(seed_family: str) -> list[str]:
    matches = [starter.key for starter in discover_starters() if starter.family == seed_family]
    if not matches:
        raise ValueError(f"Seed family '{seed_family}' was not found.")
    return matches


def create_family(
    *,
    seed_family: str,
    family: str,
    site_slug: str,
    display_name: str | None = None,
    summary: str | None = None,
    runtime_overrides: dict[str, dict[str, Any]] | None = None,
) -> list[Path]:
    created = []
    family_slug = slugify(family)
    site_slug = slugify(site_slug)
    base_name = display_name or f"{title_case_slug(site_slug)}"
    family_summary = summary or f"Starter family derived from {seed_family} for {title_case_slug(family_slug)} surfaces."
    runtime_overrides = runtime_overrides or {}

    for starter_key in seed_family_keys(seed_family):
        starter = starter_by_key(starter_key)
        runtime_suffix = starter.runtime
        dest_key = f"{site_slug}-{runtime_suffix}"
        runtime_name = f"{base_name} {runtime_label(runtime_suffix)}"
        created.append(
            copy_starter(
                source_key=starter.key,
                dest_key=dest_key,
                name=runtime_name,
                summary=family_summary,
                family=family_slug,
            )
        )
        apply_family_runtime_overrides(created[-1], runtime_suffix, runtime_overrides.get(runtime_suffix, {}))
    return created
