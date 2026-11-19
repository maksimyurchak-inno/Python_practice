import json  
from datetime import datetime 
from pathlib import Path 
from typing import Any  

from psycopg2.extensions import connection as Connection  
from psycopg2.extras import execute_values  


# Validates JSON data and loads rooms and students into PostgreSQL.
class DataLoader:
    @staticmethod
    def _read_records(
        file_path: Path, required_fields: set[str]
    ) -> list[dict[str, Any]]:
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON in {file_path}: {error}") from error

        if not isinstance(data, list):
            raise ValueError(f"{file_path} must contain a JSON array")

        for index, record in enumerate(data):
            if not isinstance(record, dict):
                raise ValueError(f"Record {index} in {file_path} must be a JSON object")
            missing = required_fields - record.keys()
            if missing:
                raise ValueError(
                    f"Record {index} in {file_path} is missing: {', '.join(sorted(missing))}"
                )

        return data

    def load(
        self, connection: Connection, rooms_path: Path, students_path: Path
    ) -> None:
        rooms = self._read_records(rooms_path, {"id", "name"})
        students = self._read_records(
            students_path, {"id", "name", "birthday", "room", "sex"}
        )

        student_rows = []
        for index, student in enumerate(students):
            birthday = student["birthday"]
            if not isinstance(birthday, str):
                raise ValueError(f"Student record {index} has a non-string birthday")
            try:
                parsed_birthday = datetime.fromisoformat(birthday)
            except ValueError as error:
                raise ValueError(
                    f"Student record {index} has an invalid ISO birthday: {birthday!r}"
                ) from error

            student_rows.append(
                (
                    student["id"],
                    student["name"],
                    parsed_birthday,
                    student["room"],
                    student["sex"],
                )
            )

        with connection:
            with connection.cursor() as cursor:
                execute_values(
                    cursor,
                    "INSERT INTO rooms (id, name) VALUES %s ON CONFLICT (id) DO NOTHING",
                    [(room["id"], room["name"]) for room in rooms],
                    page_size=1000,
                )
                execute_values(
                    cursor,
                    """
                    INSERT INTO students (id, name, birthday, room, sex)
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
                    """,
                    student_rows,
                    page_size=1000,
                )
