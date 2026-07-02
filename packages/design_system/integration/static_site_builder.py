from __future__ import annotations

import html
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _badge(label: str) -> str:
    return f'<span class="tp-badge">{_esc(label)}</span>'


def _card(item: dict) -> str:
    title = _esc(item.get("title", "Card"))
    body = _esc(item.get("body", ""))
    eyebrow = _esc(item.get("eyebrow", ""))
    tone = _esc(item.get("tone", ""))
    return (
        f'<article class="tp-card {tone}">'
        f'<span class="tp-muted">{eyebrow}</span>'
        f"<strong>{title}</strong>"
        f'<p class="tp-subtitle">{body}</p>'
        "</article>"
    )


def _table(section: dict) -> str:
    headers = "".join(f"<th>{_esc(h)}</th>" for h in section.get("headers", []))
    rows = []
    for row in section.get("rows", []):
        cells = "".join(f"<td>{cell}</td>" for cell in [_esc(str(cell)) for cell in row])
        rows.append(f"<tr>{cells}</tr>")
    return (
        '<section class="tp-table-shell">'
        f'<div class="tp-action-bar"><strong>{_esc(section.get("title", "Table"))}</strong>'
        f'<span class="tp-muted">{_esc(section.get("meta", ""))}</span></div>'
        f"<table class=\"tp-data-table\"><thead><tr>{headers}</tr></thead><tbody>{''.join(rows)}</tbody></table>"
        "</section>"
    )


def _form(section: dict) -> str:
    fields = []
    for field in section.get("fields", []):
        label = _esc(field.get("label", "Field"))
        if field.get("type") == "select":
            options = "".join(f"<option>{_esc(opt)}</option>" for opt in field.get("options", []))
            control = f"<select>{options}</select>"
        else:
            value = _esc(str(field.get("value", "")))
            input_type = _esc(field.get("type", "text"))
            control = f'<input type="{input_type}" value="{value}">'
        fields.append(f'<label class="tp-form-field"><span>{label}</span>{control}</label>')
    return (
        '<section class="tp-card">'
        f"<strong>{_esc(section.get('title', 'Form'))}</strong>"
        f'<div class="tp-form-grid">{"".join(fields)}</div>'
        "</section>"
    )


def _status_cards(section: dict) -> str:
    cards = []
    for item in section.get("items", []):
        cards.append(
            f'<article class="tp-card {_esc(item.get("tone", "info"))}">'
            f'<span class="tp-muted">{_esc(item.get("label", ""))}</span>'
            f"<strong>{_esc(item.get('value', ''))}</strong>"
            "</article>"
        )
    return f'<section class="tp-card-grid">{"".join(cards)}</section>'


def _card_grid(section: dict) -> str:
    return f'<section class="tp-card-grid">{"".join(_card(item) for item in section.get("items", []))}</section>'


def _filter_bar(section: dict) -> str:
    return '<div class="tp-action-bar">' + "".join(_badge(item) for item in section.get("items", [])) + "</div>"


SECTION_RENDERERS = {
    "status_cards": _status_cards,
    "card_grid": _card_grid,
    "table": _table,
    "form": _form,
    "filter_bar": _filter_bar,
}


def render_page(site: dict, page: dict, pages: dict) -> str:
    nav_items = []
    for nav in site.get("navigation", []):
        active = "active" if nav["key"] == page["key"] else ""
        nav_items.append(f'<a class="{active}" href="./{_esc(nav["file"])}">{_esc(nav["label"])}</a>')

    sections_html = []
    for section in page.get("sections", []):
        renderer = SECTION_RENDERERS[section["type"]]
        sections_html.append(renderer(section))

    return f"""<!doctype html>
<html lang="en" data-theme-mode="{_esc(site['branding']['default_theme_mode'])}" data-theme-color="{_esc(site['branding']['default_theme_color'])}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{_esc(page['title'])}</title>
    <link rel="stylesheet" href="../../../packages/design-system/styles/shell.css">
    <script defer src="../../../packages/design-system/scripts/shell.js"></script>
  </head>
  <body>
    <div class="tp-shell" data-tp-shell>
      <header class="tp-topbar">
        <a class="tp-brand" href="./index.html"><img class="tp-brand-logo" src="{_esc(site['branding']['logo_path'])}" alt="{_esc(site['branding']['name'])} logo"><span>{_esc(site['branding']['name'])}</span></a>
        <nav aria-label="Breadcrumb"><span class="tp-muted">Home / {_esc(page['title'])}</span></nav>
        <div class="tp-action-bar"><button class="tp-button secondary" type="button" data-tp-nav-toggle aria-expanded="true">Toggle nav</button></div>
      </header>
      <div class="tp-shell-grid">
        <aside class="tp-sidebar">
          <div class="tp-sidebar-toolbar"><strong>{_esc(site.get('sidebar_title', 'Navigation'))}</strong></div>
          <nav class="tp-nav-links" aria-label="Primary">{''.join(nav_items)}</nav>
        </aside>
        <main class="tp-main">
          <div class="tp-content-head">
            <div><p class="tp-kicker">{_esc(page['kicker'])}</p><h1>{_esc(page['title'])}</h1><p class="tp-subtitle">{_esc(page['subtitle'])}</p></div>
            <div class="tp-action-bar">{''.join(_badge(item) for item in page.get('badges', []))}</div>
          </div>
          <div class="tp-content-body tp-section-stack">
            {''.join(sections_html)}
          </div>
        </main>
      </div>
      <footer class="tp-footer"><span>Starter: {_esc(site['branding']['name'].lower().replace(' ', '-'))}</span><span>Page: {_esc(page['key'])}</span></footer>
    </div>
  </body>
</html>
"""


def render_index(site: dict, pages: dict) -> str:
    cards = []
    for page in pages["pages"]:
        cards.append(
            _card(
                {
                    "eyebrow": page["label"],
                    "title": page["card_title"],
                    "body": page["card_body"],
                }
            ).replace(
                f"<strong>{_esc(page['card_title'])}</strong>",
                f'<strong><a href="./{_esc(page["file"])}">{_esc(page["card_title"])}</a></strong>',
            )
        )

    return f"""<!doctype html>
<html lang="en" data-theme-mode="{_esc(site['branding']['default_theme_mode'])}" data-theme-color="{_esc(site['branding']['default_theme_color'])}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{_esc(site['branding']['name'])}</title>
    <link rel="stylesheet" href="../../../packages/design-system/styles/shell.css">
    <script defer src="../../../packages/design-system/scripts/shell.js"></script>
  </head>
  <body>
    <div class="tp-shell" data-tp-shell>
      <header class="tp-topbar">
        <a class="tp-brand" href="./index.html"><img class="tp-brand-logo" src="{_esc(site['branding']['logo_path'])}" alt="{_esc(site['branding']['name'])} logo"><span>{_esc(site['branding']['name'])}</span></a>
        <nav aria-label="Breadcrumb"><span class="tp-muted">Home / Starter</span></nav>
        <div class="tp-action-bar"><button class="tp-button secondary" type="button" data-tp-nav-toggle aria-expanded="true">Toggle nav</button></div>
      </header>
      <div class="tp-shell-grid">
        <aside class="tp-sidebar">
          <div class="tp-sidebar-toolbar"><strong>{_esc(site.get('sidebar_title', 'Navigation'))}</strong></div>
          <nav class="tp-nav-links" aria-label="Primary">
            {''.join(f'<a href="./{_esc(item["file"])}">{_esc(item["label"])}</a>' for item in site.get("navigation", []))}
          </nav>
        </aside>
        <main class="tp-main">
          <div class="tp-content-head">
            <div><p class="tp-kicker">Static starter</p><h1>{_esc(site['branding']['name'])}</h1><p class="tp-subtitle">{_esc(site['summary'])}</p></div>
            <div class="tp-action-bar">{_badge("Static")}</div>
          </div>
          <div class="tp-content-body tp-card-grid">
            {''.join(cards)}
          </div>
        </main>
      </div>
      <footer class="tp-footer"><span>Starter: {_esc(site['branding']['name'].lower().replace(' ', '-'))}</span><span>Mode: framework-neutral placeholder</span></footer>
    </div>
  </body>
</html>
"""


def build_static_site(site_dir: Path) -> None:
    site = load_json(site_dir / "app_config" / "site.example.json")
    pages = load_json(site_dir / "app_config" / "pages.example.json")
    templates_dir = site_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    (templates_dir / "index.html").write_text(render_index(site, pages))
    for page in pages["pages"]:
        (templates_dir / page["file"]).write_text(render_page(site, page, pages))
