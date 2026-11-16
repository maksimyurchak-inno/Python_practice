# database.py: Manages PostgreSQL connections and initializes the database schema.
from pathlib import Path  # Provides filesystem path utilities.
from types import TracebackType  # For handling exceptions used by the context manager.

import psycopg2  # Provides the PostgreSQL database connection.

from db_config import DATABASE_CONFIG  # Imports the database connection settings.


# Manages a PostgreSQL connection and applies schema and index scripts.
class DatabaseManager:
    # Opens a connection using the configured database settings.
    def __init__(self) -> None:
        self.connection = psycopg2.connect(**DATABASE_CONFIG)

    # Executes the schema and index SQL scripts.
    def initialize(self, schema_path: Path, indexes_path: Path) -> None:
        with self.connection.cursor() as cursor:
            for sql_path in (schema_path, indexes_path):
                script = sql_path.read_text(encoding="utf-8")
                if script.strip():
                    cursor.execute(script)

    # Closes the database connection.
    def close(self) -> None:
        self.connection.close()

    # Allows the manager to be used in a with statement.
    def __enter__(self) -> "DatabaseManager":
        return self

    # Commits on success, rolls back on error, and always closes the connection.
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self.close()
