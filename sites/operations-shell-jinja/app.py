from __future__ import annotations

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from packages.design_system.integration.jinja_site_factory import create_jinja_demo_app  # type: ignore


def page_title_builder(route: dict) -> tuple[str, str]:
    if route["key"] == "dashboard":
        return ("Operations Dashboard", "Jinja-backed starter for summary-first dashboard layouts.")
    return (route["nav_label"], "")


app = create_jinja_demo_app(
    site_dir=BASE_DIR,
    title="Operations Shell Jinja Demo",
    root_redirect="/dashboard",
    sidebar_title="Navigation",
    footer_items=["Starter: operations-shell-jinja", "Runtime: FastAPI + Jinja"],
    badge_labels=[{"label": "Jinja", "tone": "neutral"}],
    page_title_builder=page_title_builder,
)
