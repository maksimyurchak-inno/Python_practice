import json
import json_db  # for connecting to the PostgreSQL database
from pathlib import Path  # for handling file paths


class Extractor:
    def __init__(self, query_file):
        self.query_file = query_file


    def read_sql_query(self, cursor):
        with self.query_file.open("r", encoding="utf-8") as file:  # opens the SQL file in read mode
            query = file.read()  # reads the entire content of the SQL file into a string variable
        cursor.execute(query)  # Sends the SQL query string over the active database connection to the PostgreSQL server for execution
        columns = [column[0] for column in cursor.description]  # column[0] accesses the first item of each descriptor, which is the column name as a string
        return [
            dict(zip(columns, row))  # pairs each column header with its corresponding cell value
            for row in cursor.fetchall()  # cursor.fetchall() retrieves all remaining rows of the query result as a list of tuples
        ]  # list comprehension wraps all these row dictionaries into a single list


# execute the following code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    # Base directory where extractor.py lives
    BASE_DIR = Path(__file__).resolve().parent / "sql queries"
    # Resolves accurately regardless of where terminal was opened
    query_1 = BASE_DIR / "List of rooms and the number of students in each of them.sql"
    query_2 = BASE_DIR / "5 rooms with the smallest average age of students.sql"
    query_3 = BASE_DIR / "5 rooms with the largest difference in the age of students.sql"
    query_4 = BASE_DIR / "List of rooms where different-sex students live.sql"

    database = json_db.Json_db()
    try:
        with database.connection.cursor() as cursor:
            # creates a connection to the PostgreSQL database and executes the queries defined in the SQL files
            results = {
                "List of rooms and the number of students in each of them.sql": Extractor(query_1).read_sql_query(cursor),
                "5 rooms with the smallest average age of students.sql": Extractor(query_2).read_sql_query(cursor),
                "5 rooms with the largest difference in the age of students.sql": Extractor(query_3).read_sql_query(cursor),
                "List of rooms where different-sex students live.sql": Extractor(query_4).read_sql_query(cursor),
            }

        # write the results to a JSON file in the same directory as extractor.py
        analytical_file = Path(__file__).resolve().parent / "query_results.json"
        analytical_file.write_text( 
            json.dumps(results, indent=4, default=str),
            encoding="utf-8",
        )
    except Exception as e:  # in case of any exception
        print(f"Unexpected error: {e}")
    finally:
        database.close()  # close the database connection
