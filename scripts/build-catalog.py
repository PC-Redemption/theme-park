from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITES_DIR = ROOT / "sites"
CATALOG_DIR = ROOT / "catalog"
OUTPUT = CATALOG_DIR / "starters.json"
PREVIEW_DIR = CATALOG_DIR / "previews"


FAMILY_COLORS = {
    "operations": "#17617f",
    "settings": "#2f7b47",
    "review": "#6652a6",
}


def build_preview_svg(item: dict) -> str:
    accent = FAMILY_COLORS.get(item["family"], "#17617f")
    strengths = item.get("strengths", [])[:3]
    name = html.escape(item["name"])
    family = html.escape(item["family"].title())
    runtime = html.escape(item["runtime"])
    summary = html.escape(item["summary"])
    script = html.escape(item["preview"]["script"])
    url = html.escape(item["preview"]["url"])
    strength_lines = "".join(
        f'<text x="28" y="{140 + index * 18}" fill="#c8d2dc" font-size="12">{html.escape(entry)}</text>'
        for index, entry in enumerate(strengths)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-labelledby="title">
  <title>{name}</title>
  <rect width="640" height="360" rx="28" fill="#0f151b"/>
  <rect x="24" y="24" width="592" height="312" rx="22" fill="#151d24" stroke="#30404d"/>
  <rect x="24" y="24" width="592" height="92" rx="22" fill="{accent}"/>
  <text x="28" y="62" fill="#ffffff" font-size="14" font-family="Arial, Helvetica, sans-serif">{family} / {runtime}</text>
  <text x="28" y="92" fill="#ffffff" font-size="28" font-family="Arial, Helvetica, sans-serif">{name}</text>
  <text x="28" y="126" fill="#edf3f7" font-size="16" font-family="Arial, Helvetica, sans-serif">{summary}</text>
  <rect x="28" y="180" width="180" height="124" rx="18" fill="#1d2730" stroke="#30404d"/>
  <text x="44" y="210" fill="#edf3f7" font-size="16" font-family="Arial, Helvetica, sans-serif">Preview</text>
  <text x="44" y="236" fill="#b5c4cf" font-size="12" font-family="Arial, Helvetica, sans-serif">{script}</text>
  <text x="44" y="258" fill="#b5c4cf" font-size="12" font-family="Arial, Helvetica, sans-serif">{url}</text>
  <rect x="230" y="180" width="356" height="124" rx="18" fill="#1d2730" stroke="#30404d"/>
  <text x="248" y="210" fill="#edf3f7" font-size="16" font-family="Arial, Helvetica, sans-serif">Strengths</text>
  {strength_lines}
</svg>
"""


def main() -> None:
    manifests = []
    for path in sorted(SITES_DIR.glob("*/starter.manifest.json")):
        payload = json.loads(path.read_text())
        preview_path = PREVIEW_DIR / f'{payload["key"]}.svg'
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        preview_path.write_text(build_preview_svg(payload))
        payload["preview"]["image"] = f'./previews/{payload["key"]}.svg'
        manifests.append(payload)

    families = {}
    for item in manifests:
        families.setdefault(item["family"], []).append(item["key"])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(
            {
                "generated_from": "sites/*/starter.manifest.json",
                "starter_count": len(manifests),
                "families": families,
                "starters": manifests,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
