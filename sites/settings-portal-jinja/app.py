from __future__ import annotations

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from packages.design_system.integration.jinja_site_factory import create_jinja_demo_app  # type: ignore


def page_title_builder(route: dict) -> tuple[str, str]:
    return (route["nav_label"], "")


app = create_jinja_demo_app(
    site_dir=BASE_DIR,
    title="Settings Portal Jinja Demo",
    root_redirect="/health",
    sidebar_title="Admin Navigation",
    footer_items=["Starter: settings-portal-jinja", "Runtime: FastAPI + Jinja"],
    badge_labels=[{"label": "Jinja", "tone": "neutral"}, {"label": "Admin", "tone": "success"}],
    page_title_builder=page_title_builder,
)
