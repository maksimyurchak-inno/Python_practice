import psycopg2  # for connecting to the PostgreSQL database

class Json_db:
    def __init__(self):
        # establish a connection to the PostgreSQL database
        # the connection parameters are from my local PostgreSQL database setup
        # for reuse the code you need only change the parameters to your own database setup
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="admin",
            password="admin123",
            host="localhost",
            port="5432"
        )

    def close(self):
        # explicitly close the database connection
        self.connection.close()

# execute the following code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    database = Json_db()
    try:
        # create a cursor object to execute SQL commands
        with database.connection.cursor() as cursor:
            # execute a query to initialize the target table
            # IF NOT EXISTS clause prevents runtime errors if the table is already present
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INT PRIMARY KEY,
                    name VARCHAR(10)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT PRIMARY KEY,
                    name VARCHAR(50),
                    birthday TIMESTAMP,
                    room INT,
                    sex CHAR(1),
                    FOREIGN KEY (room) REFERENCES rooms(id)
                );
            """)
            # create an index on the 'room' column of the 'students' table to optimize the analyzing queries 
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_students_room
                ON students (room)
                INCLUDE (birthday, sex, name);
            """)

        # commit the changes to the database
        database.connection.commit()
    except Exception as e:  # in case of any exception
        print(f"Unexpected error: {e}")
    finally:
        # close the connection after creating the tables
        database.close()
