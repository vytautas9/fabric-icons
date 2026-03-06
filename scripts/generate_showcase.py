"""
Generate ICONS.md — a visual gallery of all Microsoft Fabric icons organized by library category.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent.parent

SVG_BASE_DIR = ROOT / "icons" / "high_res"
OUTPUT_FILE = ROOT / "ICONS.md"

ICONS_BASE_URL = "icons/high_res"
ICON_SIZE = 48
COLUMNS = 8

# Same order as generate_libraries.py
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


def filename_to_title(filename: str) -> str:
    """Convert e.g. 'Data_Warehouse_64.svg' -> 'Data Warehouse'."""
    base = filename[:-4]
    parts = base.split("_")
    parts = [p for p in parts if not p.isdigit()]
    return " ".join(p.capitalize() for p in parts)


def build_category_section(folder: str, display_name: str) -> str:
    folder_path = SVG_BASE_DIR / folder
    svg_files = sorted(f for f in os.listdir(folder_path) if f.endswith(".svg"))

    rows = []
    for i in range(0, len(svg_files), COLUMNS):
        chunk = svg_files[i:i + COLUMNS]
        cells = ""
        for filename in chunk:
            title = filename_to_title(filename)
            img_url = f"{ICONS_BASE_URL}/{folder}/{filename}"
            cells += (
                f'<td align="center">'
                f'<img src="{img_url}" width="{ICON_SIZE}" height="{ICON_SIZE}" alt="{title}"><br>'
                f'<sub>{title}</sub>'
                f'</td>'
            )
        # Pad the last row so the table stays uniform
        cells += "<td></td>" * (COLUMNS - len(chunk))
        rows.append(f"<tr>{cells}</tr>")

    table = "<table>\n" + "\n".join(rows) + "\n</table>"

    return (
        f"<details>\n"
        f"<summary><b>{display_name}</b> ({len(svg_files)} icons)</summary>\n\n"
        f"{table}\n\n"
        f"</details>\n"
    )


def main() -> None:
    sections = []
    total = 0

    for folder, display_name in FOLDERS.items():
        folder_path = SVG_BASE_DIR / folder
        count = sum(1 for f in os.listdir(folder_path) if f.endswith(".svg"))
        total += count
        sections.append(build_category_section(folder, display_name))
        print(f"  {display_name}: {count} icons")

    content = f"""\
# Microsoft Fabric Icon Gallery

{total} icons across {len(FOLDERS)} categories.
Click a category to expand its full icon set.

> **Tip:** These icons are available as draw.io libraries in [`drawio-libraries/`](drawio-libraries/).

---

{"".join(sections)}
---

*Generated automatically by `scripts/generate_showcase.py`.*
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nWrote {total} icons to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
