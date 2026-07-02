from __future__ import annotations

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from packages.design_system.integration.jinja_site_factory import create_jinja_demo_app_from_config  # type: ignore


app = create_jinja_demo_app_from_config(site_dir=BASE_DIR)
