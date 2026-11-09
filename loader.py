import json  # for loading JSON files
import json_db  # for connecting to the PostgreSQL database
from pathlib import Path  # for handling file paths in a cross-platform way



class Loader:
    def __init__(self, file_name):
        self.file_name = file_name

    # open and read the JSON file safely.
    def load_file(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: File is not found")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in the file.")
        except Exception as e:  # in case of any exception
            print(f"Unexpected error: {e}")

        return None



# execute the following code only if this script is run directly, not when imported as a module
if __name__ == "__main__":  
    # Base directory where json_db.py lives
    BASE_DIR = Path(__file__).resolve().parent / "files for loading"
    # Resolves accurately regardless of where terminal was opened
    path_rooms = BASE_DIR / "rooms.json"
    path_students = BASE_DIR / "students.json"

    # load json files using the Loader class
    rooms = Loader(path_rooms)
    rooms_data = rooms.load_file()

    students = Loader(path_students)
    students_data = students.load_file()

    # create an instance of the json_db class to establish a connection to the PostgreSQL database
    database = json_db.Json_db()
    try:
        with database.connection.cursor() as cursor:
            # create a template for the insert query to load data into the target table
            # the %s placeholders rely on psycopg2’s parameter binding to handle SQL injection and data type conversion
            insert_query_rooms = "INSERT INTO rooms (id, name) VALUES (%s, %s);"
            for room in rooms_data:
                cursor.execute(insert_query_rooms, (room["id"], room["name"]))

            insert_query_students = (
                "INSERT INTO students (id, name, birthday, room, sex) "
                "VALUES (%s, %s, %s, %s, %s);"
            )
            for student in students_data:
                cursor.execute(
                    insert_query_students,
                    (
                        student["id"],
                        student["name"],
                        student["birthday"],
                        student["room"],
                        student["sex"],
                    ),
                )

        database.connection.commit()
    except Exception as e:  # in case of any exception
        print(f"Unexpected error: {e}")
    finally:  # close the database connection in the finally block to ensure it is closed even if an error occurs
        database.close()


