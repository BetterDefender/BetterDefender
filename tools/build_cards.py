#!/usr/bin/env python3
"""Generate the featured-project SVG cards for the profile README.

Run from the repository root:
    python3 tools/build_cards.py

Editing the CARDS list below and re-running keeps every card visually in sync.
"""

from __future__ import annotations

import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "cards"

CARDS = [
    {
        "slug": "revshell",
        "index": 1,
        "title": "revshell",
        "stars": 48,
        "lang": "Go",
        "desc": ["Reverse shell generator for 17+ languages,", "packaged as a single CLI binary."],
        "tags": ["CLI", "PAYLOAD"],
    },
    {
        "slug": "awvs-batch-import",
        "index": 2,
        "title": "AwvsBatchImport",
        "stars": 24,
        "lang": "Python",
        "desc": ["Batch-import targets into AWVS 12/13", "through its REST API."],
        "tags": ["AWVS", "API"],
    },
    {
        "slug": "springbootscan",
        "index": 3,
        "title": "SpringBootScan",
        "stars": 19,
        "lang": "Python",
        "desc": ["Detect Spring Boot Actuator leaks and", "Alibaba OSS key exposure at scale."],
        "tags": ["SCANNER", "WEB"],
    },
    {
        "slug": "pentestbox",
        "index": 4,
        "title": "PentestBox",
        "stars": 2,
        "lang": "Toolkit",
        "desc": ["A curated box of day-to-day penetration", "testing utilities and scripts."],
        "tags": ["WINDOWS", "OPS"],
    },
    {
        "slug": "anchorscan",
        "index": 5,
        "title": "anchorScan",
        "stars": 2,
        "lang": "Python",
        "desc": ["Crawl JS-discovered routes, capture", "screenshots, and build HTML reports."],
        "tags": ["RECON", "REPORT"],
    },
    {
        "slug": "api-strike",
        "index": 6,
        "title": "API-Strike",
        "stars": 0,
        "lang": "JavaScript",
        "desc": ["Browser extension that captures and", "maps API endpoints in real time."],
        "tags": ["BROWSER", "RECON"],
    },
]


def pill(x: int, y: int, text: str, accent: bool) -> tuple[str, int]:
    width = round(len(text) * 5.9) + 14
    height = 18
    if accent:
        fill = "#FF2D55"
        fill_opacity = "0.08"
        stroke = "#FF2D55"
        color = "#FF2D55"
    else:
        fill = "#0F1622"
        fill_opacity = "1"
        stroke = "#233145"
        color = "#7D8B9E"
    svg = (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="9" '
        f'fill="{fill}" fill-opacity="{fill_opacity}" stroke="{stroke}"/>'
        f'<text x="{x + 7}" y="{y + 13}" font-size="9" letter-spacing="0.6" '
        f'fill="{color}">{escape(text)}</text>'
    )
    return svg, x + width + 8


def build_card(card: dict) -> str:
    star = (
        f'<text x="438" y="26" text-anchor="end" font-size="10" fill="#FFB020">★ {card["stars"]}</text>'
        if card["stars"] > 0
        else '<text x="438" y="26" text-anchor="end" font-size="8" letter-spacing="1.2" fill="#5E6E84">OPEN SOURCE</text>'
    )

    pills: list[str] = []
    x = 22
    p, x = pill(x, 126, card["lang"].upper(), True)
    pills.append(p)
    for tag in card["tags"]:
        p, x = pill(x, 126, tag, False)
        pills.append(p)
    pills_svg = "".join(pills)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="158" viewBox="0 0 460 158" role="img" aria-labelledby="title desc">
  <title id="title">{escape(card["title"])}</title>
  <desc id="desc">{escape(" ".join(card["desc"]))}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0C121C"/>
      <stop offset="1" stop-color="#070C13"/>
    </linearGradient>
    <radialGradient id="glow" cx="0" cy="0" r="0.9">
      <stop offset="0" stop-color="#FF2D55" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#FF2D55" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
      <path d="M22 0H0V22" fill="none" stroke="#172333" stroke-width="1"/>
    </pattern>
  </defs>

  <rect x="0.5" y="0.5" width="459" height="157" rx="9" fill="url(#bg)" stroke="#1E2B3D"/>
  <rect x="1" y="1" width="458" height="156" rx="9" fill="url(#grid)" opacity="0.25"/>
  <rect x="1" y="1" width="458" height="156" rx="9" fill="url(#glow)"/>
  <rect x="0" y="0" width="3" height="158" rx="1.5" fill="#FF2D55"/>
  <path d="M436 10H450V24" fill="none" stroke="#FF2D55" stroke-width="1" opacity="0.35"/>

  <g font-family="'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace">
    <text x="22" y="26" font-size="9" letter-spacing="1.5" fill="#5E6E84">[{card["index"]:02d}]</text>
    {star}
    <text x="22" y="57" font-size="21" font-weight="700" fill="#F2F6FB">{escape(card["title"])}</text>
    <text x="22" y="82" font-size="11.5" fill="#8B9AAD">{escape(card["desc"][0])}</text>
    <text x="22" y="99" font-size="11.5" fill="#8B9AAD">{escape(card["desc"][1])}</text>
    <path d="M22 116H438" stroke="#172230"/>
    {pills_svg}
    <text x="438" y="139" text-anchor="end" font-size="9" letter-spacing="1.2" fill="#FF2D55">OPEN →</text>
  </g>
</svg>
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        path = OUT / f'{card["slug"]}.svg'
        path.write_text(build_card(card), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
