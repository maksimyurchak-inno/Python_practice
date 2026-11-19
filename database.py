from pathlib import Path  
from types import TracebackType  
from typing import Any

import psycopg2  

# Manages a PostgreSQL connection and applies schema and index scripts.
class DatabaseManager:
    def __init__(self, db_config: dict[str, Any]) -> None:
        self.connection = psycopg2.connect(**db_config)

    def initialize(self, schema_path: Path, indexes_path: Path) -> None:
        with self.connection.cursor() as cursor:
            for sql_path in (schema_path, indexes_path):
                script = sql_path.read_text(encoding="utf-8")
                if script.strip():
                    cursor.execute(script)


    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "DatabaseManager":
        return self

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
