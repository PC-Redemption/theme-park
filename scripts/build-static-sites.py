from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from packages.design_system.integration.static_site_builder import build_static_site

SITES = [
    ROOT / "sites" / "operations-shell-static",
    ROOT / "sites" / "settings-portal-static",
    ROOT / "sites" / "review-studio-static",
]


def main() -> None:
    for site in SITES:
        build_static_site(site)
        print(f"Built {site.name}")


if __name__ == "__main__":
    main()
