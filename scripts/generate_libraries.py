"""
Generate draw.io custom library XML files from Microsoft Fabric SVG icons.

Output: one .xml file per category under icons/high_res/
Each XML can be imported into draw.io via File > Open Library from > Device.
"""

import base64
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

SVG_BASE_DIR = ROOT / "icons" / "high_res"
OUTPUT_DIR = ROOT / "drawio-libraries"

# Maps sub-folder name -> display name used for the output .xml filename.
FOLDERS: dict[str, str] = {
    "item":            "Fabric Items",
    "workload":        "Fabric Workloads",
    "datatypes":       "Fabric Datatypes",
    "database_tables": "Fabric Database & Tables",
    "kql_realtime":    "Fabric KQL & Real-Time",
    "visualization":   "Fabric Visualization",
    "development":     "Fabric Development",
    "ai_intelligence": "Fabric AI & Intelligence",
    "workspace_ui":    "Fabric Workspace & UI",
}

# Tight viewBox per folder to crop built-in padding from the SVG canvas.
# item:     64×64 icons, outer shape starts at (6,6) → 6 px padding all sides
# workload: 48×48 icons, content runs y=4→44, x≈2→46 (matches reference file)
# other sub-folders: Fluent icons with variable layouts — leave untouched
FOLDER_VIEWBOX: dict[str, str] = {
    "item":     "6 6 52 52",
    "workload": "2 4 44 40",
}


def svg_to_data_uri(svg_path: Path, viewbox: str | None = None) -> str:
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
    if viewbox:
        content = _apply_viewbox(content, viewbox)
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def _apply_viewbox(svg_content: str, viewbox: str) -> str:
    """Add or replace the viewBox attribute on the root SVG element."""
    if re.search(r'viewBox=', svg_content, re.IGNORECASE):
        return re.sub(r'viewBox="[^"]*"', f'viewBox="{viewbox}"', svg_content, count=1, flags=re.IGNORECASE)
    return svg_content.replace("<svg ", f'<svg viewBox="{viewbox}" ', 1)


def _effective_viewbox(svg_content: str, viewbox: str) -> str | None:
    """Return viewbox if no badge/sub-icon is detected, else None (keep full canvas).

    Badge sub-icons (e.g. the link indicator on External_* items) always render
    a white pill background with fill="#F5F5F5". Detecting that element is simpler
    and more reliable than scanning path coordinates, which contain arc radii and
    decimal values without leading zeros that would produce false positives.
    """
    if re.search(r'fill="#F5F5F5"', svg_content, re.IGNORECASE):
        return None  # badge present — keep full canvas
    return viewbox


def filename_to_title(filename: str) -> str:
    """Convert e.g. 'Data_Warehouse_64.svg' -> 'Data Warehouse'."""
    base = filename[:-4]  # strip .svg
    parts = base.split("_")
    # Drop trailing size number and Filled/Regular variants
    parts = [p for p in parts if not p.isdigit()]
    return " ".join(p.capitalize() for p in parts)


def get_svg_dimensions(svg_path: Path, viewbox: str | None = None) -> tuple[int, int]:
    """Return (w, h) from viewBox if given, otherwise from SVG width/height attributes."""
    if viewbox:
        parts = viewbox.split()
        return round(float(parts[2])), round(float(parts[3]))
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read(512)
    w = re.search(r'width="(\d+)"', content)
    h = re.search(r'height="(\d+)"', content)
    return (int(w.group(1)) if w else 64, int(h.group(1)) if h else 64)


def build_library_entry(svg_path: Path, filename: str, viewbox: str | None = None) -> dict:
    # Resolve the effective viewBox once so dimensions and data URI stay in sync.
    if viewbox:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        viewbox = _effective_viewbox(svg_content, viewbox)
    w, h = get_svg_dimensions(svg_path, viewbox)
    data_uri = svg_to_data_uri(svg_path, viewbox)
    return {
        "data": data_uri,
        "w": w,
        "h": h,
        "title": filename_to_title(filename),
        "aspect": "fixed",
    }


def generate_library(folder: str, display_name: str) -> None:
    folder_path = SVG_BASE_DIR / folder
    svg_files = sorted(f for f in os.listdir(folder_path) if f.endswith(".svg"))

    viewbox = FOLDER_VIEWBOX.get(folder)
    entries = []
    for filename in svg_files:
        svg_path = folder_path / filename
        entry = build_library_entry(svg_path, filename, viewbox)
        entries.append(entry)
        print(f"  [{display_name}] {filename} -> {entry['title']}")

    xml_content = f"<mxlibrary>{json.dumps(entries, separators=(',', ':'))}</mxlibrary>"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{display_name}.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"\nWrote {len(entries)} icons to {output_path}")


def main() -> None:
    for folder, display_name in FOLDERS.items():
        generate_library(folder, display_name)
    print("\nDone. Import each .xml via draw.io > File > Open Library from > Device")


if __name__ == "__main__":
    main()
