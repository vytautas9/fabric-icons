"""
Reorganize icons from other/ into themed sub-folders.
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent

SRC = ROOT / "icons" / "high_res" / "other"
BASE = ROOT / "icons" / "high_res"

CATEGORIES = [
    "datatypes",
    "database_tables",
    "kql_realtime",
    "visualization",
    "ai_intelligence",
    "development",
    "workspace_ui",
]

# Ordered prefix lists — first match wins.
# KQL is checked before Database/Table so that e.g. Table_Kql_* lands in kql_realtime.
RULES: list[tuple[str, list[str]]] = [
    ("datatypes", [
        "Datatype_",
    ]),
    ("kql_realtime", [
        # anything with "Kql" in the name, plus Stream icons
        "Stream_",
    ]),
    ("database_tables", [
        "Database_",
        "Table_",
        "Column_",
        "Schema_",
        "Book_Database_",
        "Stack_Key_",
        "Document_Tree_",
        "Folder_Table_",
        "List_Sql_",
        "Lock_Closed_Database_",
        "Lock_Closed_Sql_",
        "My_Location_Database_",
        "Partition_Hint_",
        "Square_Database_",
        "Window_Database_",
        "Window_Relationship_",
    ]),
    ("visualization", [
        "Data_Bar_Vertical_",
        "Data_Graph_",
        "Data_Histogram_",
        "Data_Area_",
        "Data_Tree_",
        "Circle_Chart_",
        "Pie_Double_",
        "Arrow_Trending_",
        "Arrow_Down_Drill_",
        "Bookmark_Data_Bar_",
        "Phone_Data_Bar_",
        "Shopping_Bag_Data_Bar_",
        "Trophy_Data_Bar_",
        "Tooltip_Data_Bar_",
        "Square_Multiple_Data_Bar_",
        "Window_Gauge_",
    ]),
    ("ai_intelligence", [
        "Graph_Intelligence_",
        "Purview_",
        "Beaker_Flash_",
        "Binoculars_",
        "Toggle_Multiple_Sparkles_",
        "Window_Sparkle_",
        "Document_One_Page_Sparkles_",
        "Receipt_Sparkle_",
        "Script_Sparkle_",
        "Developer_Board_Lightning_Sparkle_",
        "Developer_Board_Lightning_Asterisk_",
    ]),
    ("development", [
        "Notebook_",
        "Import_Notebook",
        "Code_Text_Flash_",
        "Window_Code_",
        "Window_Math_Formula_",
        "Window_Tree_",
        "Window_Synapse_Link_",
        "Document_Sql_",
        "Document_Tmdl_",
        "Document_Multiple_Dax_",
        "Document_Pq_",
        "Document_Rdl_",
        "Document_Ssis_",
        "Text_Lambda_",
        "Text_Py_",
        "Text_Abc_",
        "Text_Any_",
        "Text_Byte_",
        "Text_Number_",
        "Calculator_",
        "Number_Function_",
        "Branch_",
        "Diagram_",
        "Commit_",
        "Nodes_",
        "Connector_",
        "Odata_",
        "Developer_Board_",  # catches remaining Lightning_Kql after Sparkle/Asterisk caught above
        "Function_Set_",
        "Bracket_Rectangles_",
        "Pipeline_Note_",
        "Add_Pipeline",
        "Rectangle_Multiple_Diff_",
        "Square_Multiple_Diagram_",
    ]),
]


def classify(filename: str) -> str:
    for category, prefixes in RULES:
        if category == "kql_realtime":
            # Special case: match on substring "Kql" or Stream_ prefix
            if "Kql" in filename or filename.startswith("Stream_"):
                return category
        else:
            for prefix in prefixes:
                if filename.startswith(prefix):
                    return category
    return "workspace_ui"


def main() -> None:
    svgs = [f for f in os.listdir(SRC) if f.endswith(".svg")]

    for cat in CATEGORIES:
        (BASE / cat).mkdir(parents=True, exist_ok=True)

    counts: dict[str, int] = {cat: 0 for cat in CATEGORIES}

    for svg in svgs:
        cat = classify(svg)
        shutil.move(str(SRC / svg), str(BASE / cat / svg))
        counts[cat] += 1

    print("Reorganization complete:")
    for cat, count in counts.items():
        print(f"  {cat:20s}: {count:3d} files")

    remaining = [f for f in os.listdir(SRC) if f.endswith(".svg")]
    if remaining:
        print(f"\nWarning: {len(remaining)} SVGs still in other/:")
        for f in remaining:
            print(f"  {f}")
    else:
        print(f"\nother/ is now empty of SVGs.")


if __name__ == "__main__":
    main()
