# Amazon Analyzer

This repository provides a small utility for importing Amazon order history from an Excel workbook into a local SQLite database.

## Usage

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Put your Excel file somewhere you can reference it on disk.

   - You can store it in this repo (for example, create a `data/` folder) or leave it anywhere else on your machine.
   - The import script accepts a full or relative path. A relative path is resolved from your current working directory.

3. Run the import script, pointing to your Excel file:

```bash
python src/import_excel_to_sqlite.py \
  --excel /path/to/amazon-orders.xlsx \
  --output amazon_orders.db \
  --table orders
```

If your Excel file is in the repo, you can do something like:

```bash
python src/import_excel_to_sqlite.py \
  --excel data/amazon-orders.xlsx \
  --output amazon_orders.db \
  --table orders
```

By default the script reads the first worksheet in the workbook and writes it to the specified SQLite database. Column names are normalized to lowercase snake_case to keep them consistent for querying.

## Accessing your data

The database file is created at the path you pass to `--output` (default: `amazon_orders.db`). You can open it with any SQLite client.

Example with the SQLite CLI:

```bash
sqlite3 amazon_orders.db
```

Inside the prompt, run queries like:

```sql
.headers on
.mode column
SELECT * FROM orders LIMIT 5;
```

## Querying

After import, you can query with any SQLite client, for example:

```bash
sqlite3 amazon_orders.db "SELECT * FROM orders LIMIT 5;"
```
