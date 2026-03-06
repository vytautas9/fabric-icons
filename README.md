# Microsoft Fabric Icons for draw.io

Pre-built [draw.io](https://app.diagrams.net/) custom libraries containing Microsoft Fabric SVG icons, organized by category. Icons are sourced from the official [`@fabric-msft/svg-icons`](https://www.npmjs.com/package/@fabric-msft/svg-icons) npm package.

Browse all icons by category in [ICONS.md](ICONS.md).

## About

This repository makes it easy to generate and import Microsoft Fabric icon libraries into draw.io. The icons are organized by category so you can quickly find what you need when building Fabric architecture diagrams — whether you're documenting lakehouses, pipelines, real-time intelligence flows, or any other Fabric workload.

## Using the Libraries

1. Open [draw.io](https://app.diagrams.net/) (desktop or web)
2. Go to **File > Open Library from > Device** (or **File > Open Library...**)
3. Select any `.xml` file from the [`drawio-libraries/`](drawio-libraries/) folder
4. Icons appear in a panel on the left

## Available Libraries

| Library file | Contents |
|---|---|
| `Fabric Items.xml` | Workspace item icons (Lakehouse, Notebook, Pipeline, Warehouse, etc.) |
| `Fabric Workloads.xml` | Workload branding icons |
| `Fabric Datatypes.xml` | Data type icons |
| `Fabric Database & Tables.xml` | Database, table, column, and schema icons |
| `Fabric KQL & Real-Time.xml` | KQL and streaming icons |
| `Fabric Visualization.xml` | Chart and visualization icons |
| `Fabric Development.xml` | Code, notebook, SQL, and developer icons |
| `Fabric AI & Intelligence.xml` | AI, ML, and intelligence icons |
| `Fabric Workspace & UI.xml` | General workspace and UI icons |

## Updating the Icons

To regenerate the libraries with the latest icons from Microsoft:

```bash
pip install -r requirements.txt
python update.py
```

This will:
1. Download the latest `@fabric-msft/svg-icons` package from npm
2. Organize and categorize the SVG icons
3. Regenerate all `.xml` library files in `drawio-libraries/`
4. Regenerate the [ICONS.md](ICONS.md) gallery

## Project Structure

```
fabric-icons/
├── scripts/
│   ├── download_icons.py       # Step 1: Download & organize SVGs from npm
│   ├── categorize_icons.py     # Step 2: Sort icons into themed folders
│   ├── generate_libraries.py   # Step 3: Build draw.io XML library files
│   └── generate_showcase.py    # Step 4: Regenerate ICONS.md gallery
├── icons/high_res/             # Committed SVG icons (organized by category)
├── drawio-libraries/           # Ready-to-import draw.io library files
├── update.py                   # Runs all 4 steps in sequence
├── ICONS.md                    # Visual gallery of all icons
├── requirements.txt
└── .gitignore
```

## License

Icons are sourced from [`@fabric-msft/svg-icons`](https://www.npmjs.com/package/@fabric-msft/svg-icons) and subject to Microsoft's licensing terms.

## Acknowledgements

This project was built with the assistance of AI tools.
