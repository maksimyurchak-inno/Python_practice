import json  
import xml.etree.ElementTree as ET  
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import date, datetime, time, timedelta  
from decimal import Decimal  
from pathlib import Path  
from typing import Any  

from psycopg2.extensions import connection as Connection  
from psycopg2.extras import RealDictCursor  


# Runs report queries from a directory and returns their results.
class SQLQueryRunner:
    def __init__(self, query_directory: Path) -> None:
        self.query_directory = query_directory

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


class BaseExporter(ABC):
    def export(
        self, results: dict[str, list[dict[str, Any]]], output_path: Path
    ) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        content = self.serialize(results)
        output_path.write_text(content, encoding="utf-8")

    @abstractmethod
    def serialize(self, results: dict[str, list[dict[str, Any]]]) -> str:
        raise NotImplementedError


class JsonExporter(BaseExporter):
    def serialize(self, results: dict[str, list[dict[str, Any]]]) -> str:
        return json.dumps(
            results, indent=2, ensure_ascii=False, default=self._serialize
        ) + "\n"

    @staticmethod
    def _serialize(value: Any) -> str | float:
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (date, datetime, time, timedelta)):
            return str(value)
        raise TypeError(f"Cannot convert {type(value).__name__} to JSON")


class XmlExporter(BaseExporter):
    def serialize(self, results: dict[str, list[dict[str, Any]]]) -> str:
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


class ExporterFactory:
    _exporters: dict[str, type[BaseExporter]] = {
        "json": JsonExporter,
        "xml": XmlExporter,
    }

    @classmethod
    def create(cls, output_format: str) -> BaseExporter:
        try:
            exporter_class = cls._exporters[output_format]
        except KeyError:
            raise ValueError(f"Unsupported output format: {output_format}") from None
        return exporter_class()


class ReportExporter:
    def __init__(
        self,
        exporter_factory: Callable[[str], BaseExporter] = ExporterFactory.create,
    ) -> None:
        self._exporter_factory = exporter_factory

    def export(
        self, results: dict[str, list[dict[str, Any]]], output_path: Path, output_format: str
    ) -> None:
        self._exporter_factory(output_format).export(results, output_path)
