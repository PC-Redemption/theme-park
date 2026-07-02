from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from packages.design_system.control_plane import discover_starters  # type: ignore
from packages.design_system.integration.static_site_builder import build_static_site  # type: ignore


def main() -> None:
    for starter in discover_starters():
        if starter.runtime != "static":
            continue
        build_static_site(starter.site_dir)
        print(f"Built {starter.site_dir.name}")


if __name__ == "__main__":
    main()
