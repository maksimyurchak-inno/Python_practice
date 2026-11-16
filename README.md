## Architecture

- `main.py` is the CLI entry point and coordinates the pipeline.
- `loader.py` validates input records and uses `execute_values` for batched
  inserts in a transaction.
- `database.py` manages the PostgreSQL connection and applies `schema.sql` and
  `indexes.sql`.
- `sql_queries/` contains the report queries.
- `extractor.py` Generates the final report.


## Setup

Python 3.10 or later and a running PostgreSQL server are required.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root and set your PostgreSQL connection
values there. The `.env` file is ignored by Git and must not be committed.

```text
PGDATABASE=<postgres>
PGUSER=<admin>
PGPASSWORD=<your-postgresql-password>
PGHOST=<localhost>
PGPORT=<5432>
```

The database must already exist.


## Indexes

`indexes.sql` creates the following indexes:

- `(room, birthday)` starts with the join key and includes the date used by
  the age reports.
- `(room, sex)` starts with with the join and includes the value checked
  by the mixed-sex report.

PostgreSQL may still prefer sequential scans when a report needs most student rows. 
An index is often more useful when a query needs only a small subset.

## Run

```powershell
python main.py
```

To export the reports as XML instead of JSON, run:

```powershell
python main.py --format xml
```
