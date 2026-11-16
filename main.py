# main.py: Entry point for the project; it validates the input paths, initializes the database, loads the data, runs the SQL reports, and exports the results.

import argparse  # Provides command-line argument parsing.
import logging  # Provides application logging.
from pathlib import Path  # Provides cross-platform filesystem paths.

import psycopg2  # Provides PostgreSQL exception types.

from database import DatabaseManager  # Manages the PostgreSQL connection and schema setup.
from extractor import ReportExporter, SQLQueryRunner  # Runs reports and writes their output files.
from loader import DataLoader  # Validates input JSON files and loads their records.


PROJECT_DIRECTORY = Path(__file__).resolve().parent
DEFAULT_ROOMS = PROJECT_DIRECTORY / "files_for_loading" / "rooms.json"
DEFAULT_STUDENTS = PROJECT_DIRECTORY / "files_for_loading" / "students.json"
SCHEMA_FILE = PROJECT_DIRECTORY / "schema.sql"
INDEXES_FILE = PROJECT_DIRECTORY / "indexes.sql"
QUERIES_DIRECTORY = PROJECT_DIRECTORY / "sql_queries"


# Defines the supported command-line options and their defaults.
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Load room and student JSON files into PostgreSQL and export SQL reports."
    )
    parser.add_argument("--students", type=Path, default=DEFAULT_STUDENTS)
    parser.add_argument("--rooms", type=Path, default=DEFAULT_ROOMS)
    parser.add_argument("--format", choices=("json", "xml"), default="json")
    parser.add_argument(
        "--output", type=Path, help="Report path (defaults to query_results.<format>)"
    )
    return parser


# Runs the full input, database, report, and export workflow.
def main() -> int:
    args = build_parser().parse_args()
    output_path = args.output or PROJECT_DIRECTORY / f"query_results.{args.format}"

    try:
        for label, file_path in (("rooms", args.rooms), ("students", args.students)):
            if not file_path.is_file():
                raise FileNotFoundError(
                    f"The {label} input path is not a file: {file_path}"
                )

        with DatabaseManager() as database:
            database.initialize(SCHEMA_FILE, INDEXES_FILE)
            DataLoader().load(database.connection, args.rooms, args.students)
            with database.connection.cursor() as cursor:
                cursor.execute("ANALYZE rooms")
                cursor.execute("ANALYZE students")
            results = SQLQueryRunner(QUERIES_DIRECTORY).execute_all(database.connection)

        ReportExporter().export(results, output_path, args.format)
    except (OSError, ValueError, psycopg2.Error) as error:
        logging.error("%s", error)
        return 1

    logging.info("Report written to %s", output_path)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    raise SystemExit(main())
