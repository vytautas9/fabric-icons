"""
Download Microsoft Fabric SVG icons from npm and organize them for use in draw.io diagrams.

Source package: https://www.npmjs.com/package/@fabric-msft/svg-icons
"""

import os
import re
import shutil
import tarfile
import urllib.parse
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).parent.parent

PACKAGE_NAME = "@fabric-msft/svg-icons"
EXTRACT_DIR = ROOT / "svg-icons"
SVG_SOURCE_DIR = ROOT / "svg-icons" / "dist" / "svg"
OUTPUT_DIR = ROOT / "icons"

WORKLOAD_KEYWORDS = [
    "copilot", "data_engineering", "data_factory", "data_science",
    "data_warehouse", "databases", "fabric", "industry_solutions",
    "one_lake", "power_bi", "real_time_intelligence",
]


# --- Download ---

def download_npm_package(package_name: str, version: str = "latest", extract_to: Path = Path(".")) -> None:
    encoded_package = urllib.parse.quote(package_name, safe="@/")
    metadata_url = f"https://registry.npmjs.org/{encoded_package}"

    resp = requests.get(metadata_url)
    resp.raise_for_status()

    data = resp.json()
    if version == "latest":
        version = data["dist-tags"]["latest"]

    if version not in data["versions"]:
        raise ValueError(f"Version '{version}' not found for package {package_name}")

    tarball_url = data["versions"][version]["dist"]["tarball"]
    tarball_resp = requests.get(tarball_url)
    tarball_resp.raise_for_status()

    with tarfile.open(fileobj=BytesIO(tarball_resp.content), mode="r:gz") as tar:
        for member in tar.getmembers():
            member.name = os.path.relpath(member.name, "package")
            tar.extract(member, path=extract_to)

    print(f"Downloaded and extracted {package_name}@{version} to {extract_to}")


# --- File renaming ---

def _move_numeric_suffix(filename: str) -> str:
    """Move the size number (e.g. 20, 24, 32) to the end of the base name."""
    base = filename[:-4]
    parts = base.split("_")
    for i, part in enumerate(parts):
        if part.isdigit():
            reordered = parts[:i] + parts[i + 1:] + [part]
            return "_".join(reordered) + ".svg"
    return filename


def rename_svg_files(directory: Path) -> None:
    """Rename all SVG files in directory so the size suffix comes last."""
    for filename in os.listdir(directory):
        if not filename.endswith(".svg"):
            continue
        new_filename = _move_numeric_suffix(filename)
        if new_filename != filename:
            src = directory / filename
            dst = directory / new_filename
            os.replace(src, dst)
            print(f"Renamed: {filename} -> {new_filename}")


# --- Metadata extraction ---

def get_icon_resolution(filename: str) -> str | None:
    base = filename[:-4]
    for part in base.split("_"):
        if part.isdigit():
            return part
    return None


def get_icon_type(filename: str) -> str:
    if "_item_" in filename:
        return "item"
    if any(kw in filename for kw in WORKLOAD_KEYWORDS):
        return "workload"
    return "other"


def get_icon_main(filename: str) -> str:
    base = filename[:-4]
    parts = base.split("_")
    parts = [p for p in parts if p not in ("item", "non-item") and not p.isdigit()]
    return "_".join(parts)


def to_drawio_friendly_name(filename: str) -> str:
    base = filename[:-4]
    parts = base.split("_")
    parts = [p.capitalize() for p in parts if p not in ("item", "non-item")]
    return "_".join(parts) + ".svg"


# --- DataFrame build ---

def build_icons_dataframe(svg_dir: Path) -> pd.DataFrame:
    files = [f for f in os.listdir(svg_dir) if f.endswith(".svg")]
    df = pd.DataFrame(files, columns=["filename"])
    df["icon_resolution"] = df["filename"].apply(get_icon_resolution)
    df["icon_type"] = df["filename"].apply(get_icon_type)
    df["icon_main"] = df["filename"].apply(get_icon_main)
    df["friendly_filename"] = df["filename"].apply(to_drawio_friendly_name)
    return df


# --- Copy / organize ---

def organize_icons(df: pd.DataFrame, source_dir: Path, output_dir: Path) -> None:
    for icon_main, group in df.groupby("icon_main"):
        highest_res = group["icon_resolution"].max()

        for _, row in group.iterrows():
            src = source_dir / row["filename"]
            tier = "high_res" if row["icon_resolution"] == highest_res else "all_sizes"
            dest_dir = output_dir / tier / row["icon_type"]
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / row["friendly_filename"]
            print(f"Copying: {src} -> {dest}")
            shutil.copyfile(src, dest)


# --- Main ---

def main() -> None:
    download_npm_package(PACKAGE_NAME, version="latest", extract_to=EXTRACT_DIR)
    rename_svg_files(SVG_SOURCE_DIR)

    df = build_icons_dataframe(SVG_SOURCE_DIR)
    print(f"\nTotal SVG files: {len(df)}")

    duplicates = df[df.duplicated(subset=["friendly_filename"], keep=False)]
    if not duplicates.empty:
        print(f"\nWarning: {len(duplicates)} files share a friendly filename after renaming:")
        print(duplicates[["filename", "friendly_filename"]].to_string(index=False))

    organize_icons(df, SVG_SOURCE_DIR, OUTPUT_DIR)
    print(f"\nDone. Icons organized in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
