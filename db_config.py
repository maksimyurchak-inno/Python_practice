# - db_config.py: Loads database settings from environment variables and .env and provides a dictionary for database connection configuration.

import os  # Provides access to environment variables.
from pathlib import Path  # Provides filesystem path utilities.

from dotenv import load_dotenv  # Loads variables from a .env file.


PROJECT_DIRECTORY = Path(__file__).resolve().parent  # Gets this file's containing directory.
load_dotenv(PROJECT_DIRECTORY / ".env")  # Loads environment variables from the project's .env file.

DATABASE_CONFIG = {  # Collects database connection settings.
    "dbname": os.getenv("PGDATABASE", "postgres"),
    "user": os.getenv("PGUSER", "admin"),
    "password": os.getenv("PGPASSWORD"),
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
}

"""
Packages os AND dotenv in this file work together, but each does a different job:

load_dotenv(...) from dotenv reads the .env file and puts its values into the process environment.
os.getenv(...) reads those values from the process environment.
So dotenv loads the settings, and os retrieves them.
"""
