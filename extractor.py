# - extractor.py: Runs SQL queries on the PostgreSQL server and exports the results as JSON or XML.

import json  # Provides functions for converting results to JSON text.
import xml.etree.ElementTree as ET  # Provides functions for converting results to XML documents.
from datetime import date, datetime, time, timedelta  # Provides date and time types for checking query results.
from decimal import Decimal  # Imports the type used for checking query results.
from pathlib import Path  # Provides the filesystem path type used in annotations.
from typing import Any  # Provides a flexible type used in annotations.

from psycopg2.extensions import connection as Connection  # For data annotation.
from psycopg2.extras import RealDictCursor  # Makes query rows behave like dictionaries for easy access.


# Runs report queries from a directory and returns their results.
class SQLQueryRunner:
    # Stores the directory containing the SQL report files.
    def __init__(self, query_directory: Path) -> None:
        self.query_directory = query_directory

    # Executes every SQL file and maps each filename to its result rows.
    def execute_all(
        self, connection: Connection
    ) -> dict[str, list[dict[str, Any]]]:
        query_files = sorted(self.query_directory.glob("*.sql"))
        if not query_files:
            raise FileNotFoundError(f"No SQL queries found in {self.query_directory}")

        results = {}
        for query_file in query_files:
            query = query_file.read_text(encoding="utf-8")
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                results[query_file.stem] = [dict(row) for row in cursor.fetchall()]
        return results


# Writes query results to a JSON or XML report file.
class ReportExporter:
    # Converts the results in the requested format and writes them to disk.
    def export(
        self, results: dict[str, list[dict[str, Any]]], output_path: Path, output_format: str
    ) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_format == "json":
            content = json.dumps(
                results, indent=2, ensure_ascii=False, default=self._serialize
            ) + "\n"
        elif output_format == "xml":
            content = self._to_xml(results)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        output_path.write_text(content, encoding="utf-8")

    # Converts database value types that JSON cannot convert by default.
    @staticmethod
    def _serialize(value: Any) -> str | float:
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (date, datetime, time, timedelta)):
            return str(value)
        raise TypeError(f"Cannot convert {type(value).__name__} to JSON")

    # Builds an XML document from the report names, rows, and fields.
    @staticmethod
    def _to_xml(results: dict[str, list[dict[str, Any]]]) -> str:
        root = ET.Element("reports")
        for report_name, rows in results.items():
            report = ET.SubElement(root, "report", name=report_name)
            for row in rows:
                row_element = ET.SubElement(report, "row")
                for field, value in row.items():
                    element = ET.SubElement(row_element, field)
                    element.text = "" if value is None else str(value)
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"
