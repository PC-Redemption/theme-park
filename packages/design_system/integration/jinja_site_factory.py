from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def create_jinja_demo_app(
    *,
    site_dir: Path,
    title: str,
    root_redirect: str,
    sidebar_title: str,
    footer_items: list[str],
    badge_labels: list[dict],
    page_title_builder: Callable[[dict], tuple[str, str]],
) -> FastAPI:
    repo_root = site_dir.parent.parent
    design_system_templates = repo_root / "packages" / "design-system" / "templates"
    site_templates = site_dir
    site_static = site_dir / "static"

    shell_config = load_json(site_dir / "app_config" / "shell.example.json")
    scaffold_contracts = load_json(site_dir / "app_config" / "scaffold_contracts.example.json")
    route_manifest = load_json(site_dir / "routes" / "route_manifest.example.json")

    app = FastAPI(title=title)
    templates = Jinja2Templates(directory=[str(site_templates), str(design_system_templates)])

    app.mount("/site-static", StaticFiles(directory=str(site_static)), name=f"{site_dir.name}_static")
    app.mount("/assets/design-system", StaticFiles(directory=str(repo_root / "packages" / "design-system")), name=f"{site_dir.name}_design_system")

    def page_context(route: dict, scaffold: dict) -> dict:
        heading_title, heading_subtitle = page_title_builder(route)
        frame = shell_config["page_frame"]
        return {
            "kicker": frame["kicker"],
            "title": heading_title,
            "subtitle": heading_subtitle or scaffold["contract"]["summary"],
            "badges": badge_labels,
        }

    def shell_context(active_nav: str) -> dict:
        return {
            "brand": {
                "name": shell_config["branding"]["name"],
                "logo_path": shell_config["branding"]["logo_path"],
                "favicon_path": shell_config["branding"]["favicon_path"],
                "home_url": root_redirect,
            },
            "assets": {
                "shell_css": "/assets/design-system/styles/shell.css",
                "shell_js": "/assets/design-system/scripts/shell.js",
            },
            "breadcrumb": shell_config["navigation"]["breadcrumb"],
            "navigation": shell_config["navigation"]["focused_nav"],
            "sidebar_title": sidebar_title,
            "theme_menu": True,
            "footer_items": footer_items,
        }

    def theme_context() -> dict:
        branding = shell_config["branding"]
        return {
            "modes": ["light", "dark"],
            "colors": ["black", "green", "blue", "plum", "orange", "red"],
            "default_mode": branding["default_theme_mode"],
            "default_color": branding["default_theme_color"],
        }

    @app.get("/")
    def root() -> RedirectResponse:
        return RedirectResponse(url=root_redirect, status_code=307)

    for route in route_manifest["routes"]:
        async def handler(request: Request, route=route):
            key = route["template"].split("/")[-1].removesuffix(".html")
            scaffold = scaffold_contracts[key]
            return templates.TemplateResponse(
                request,
                route["template"],
                {
                    "shell": shell_context(route["key"]),
                    "theme": theme_context(),
                    "page": page_context(route, scaffold),
                    "active_nav": route["key"],
                    "contract": scaffold["contract"],
                    "reference_set": scaffold["reference_set"],
                },
            )

        app.add_api_route(route["path"], handler, methods=["GET"], name=route["key"])

    return app


def create_jinja_demo_app_from_config(*, site_dir: Path) -> FastAPI:
    runtime_config = load_json(site_dir / "app_config" / "runtime.example.json")
    page_titles = runtime_config.get("page_titles", {})

    def page_title_builder(route: dict) -> tuple[str, str]:
        details = page_titles.get(route["key"], {})
        return (
            details.get("title", route.get("nav_label", route["key"].title())),
            details.get("subtitle", ""),
        )

    return create_jinja_demo_app(
        site_dir=site_dir,
        title=runtime_config["app_title"],
        root_redirect=runtime_config["root_redirect"],
        sidebar_title=runtime_config["sidebar_title"],
        footer_items=runtime_config["footer_items"],
        badge_labels=runtime_config["badge_labels"],
        page_title_builder=page_title_builder,
    )
