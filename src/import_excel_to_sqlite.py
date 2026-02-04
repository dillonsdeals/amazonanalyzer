#!/usr/bin/env python3
"""Import an Excel workbook of Amazon order history into SQLite."""

from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

import pandas as pd


def normalize_column(column_name: str) -> str:
    """Normalize column names to snake_case lowercase strings."""
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", column_name).strip("_")
    return cleaned.lower() or "column"


def load_excel(path: Path, sheet: str | int | None) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = [normalize_column(str(col)) for col in df.columns]
    return df


def write_sqlite(df: pd.DataFrame, output: Path, table: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(output) as connection:
        df.to_sql(table, connection, if_exists="replace", index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import an Excel workbook into a SQLite database."
    )
    parser.add_argument("--excel", required=True, help="Path to the Excel file.")
    parser.add_argument(
        "--output",
        default="amazon_orders.db",
        help="Path to the output SQLite database.",
    )
    parser.add_argument(
        "--table", default="orders", help="Table name for the imported data."
    )
    parser.add_argument(
        "--sheet",
        default=None,
        help=(
            "Worksheet name or index (0-based). Defaults to the first sheet."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    excel_path = Path(args.excel).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    sheet: str | int | None

    if args.sheet is None:
        sheet = 0
    else:
        sheet = int(args.sheet) if str(args.sheet).isdigit() else args.sheet

    dataframe = load_excel(excel_path, sheet)
    write_sqlite(dataframe, output_path, args.table)

    print(
        f"Imported {len(dataframe)} rows into {output_path} (table: {args.table})."
    )


if __name__ == "__main__":
    main()
