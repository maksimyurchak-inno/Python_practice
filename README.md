# Python_practice repository

This project automates the process of setting up a PostgreSQL database, loading dataset files (`rooms.json` and `students.json`), and executing analytical SQL queries to generate a JSON report.

## Prerequisites

1. **Python 3**: Ensure Python 3 is installed.
2. **PostgreSQL**: A local PostgreSQL server must be running.
3. **psycopg2**: Install the required PostgreSQL driver for Python:

*Note: You need to update the database connection parameters (user, password, host, port) inside `json_db.py` to match your local PostgreSQL setup.*

## Pipeline Overview

The execution script runs the following Python modules in strict sequence:
1. **`json_db.py`**: Initializes the database by creating the necessary tables (`rooms`, `students`) and performance indexes.
2. **`loader.py`**: Reads the local JSON data files and inserts the records into the PostgreSQL database.
3. **`extractor.py`**: Reads SQL query files, executes them on the database side, and saves the analytical output.

## How to Run

You can execute the entire pipeline using the provided Bash script. 

**Using the bash command**
```bash
bash script_db.sh
```

## Output

Upon successful execution, the pipeline will generate a `query_results.json` file in the project directory containing the extracted SQL analytics. The script is configured to safely pause upon completion or abort if any errors are encountered.
