"""
Update Microsoft Fabric draw.io libraries.

Runs all steps in sequence:
  1. Download the latest @fabric-msft/svg-icons npm package and organize SVGs
  2. Categorize icons from the generic 'other' bucket into themed folders
  3. Generate draw.io-compatible .xml library files
  4. Regenerate ICONS.md gallery

Usage:
    python update.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

import download_icons
import categorize_icons
import generate_libraries
import generate_showcase


def main() -> None:
    print("Step 1/4: Downloading icons")
    download_icons.main()

    print()
    print("Step 2/4: Categorizing icons")
    categorize_icons.main()

    print()
    print("Step 3/4: Generating draw.io libraries")
    generate_libraries.main()

    print()
    print("Step 4/4: Generating ICONS.md gallery")
    generate_showcase.main()

    print()
    print("All done!")


if __name__ == "__main__":
    main()
