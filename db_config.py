import os  
from pathlib import Path  

from dotenv import load_dotenv  


PROJECT_DIRECTORY = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIRECTORY / ".env")  

password = os.getenv("PGPASSWORD")
if not password or not password.strip():
    raise ValueError(
        "Database password is not configured. Set PGPASSWORD in .env or the environment."
    )

DATABASE_CONFIG = { 
    "dbname": os.getenv("PGDATABASE", "postgres"),
    "user": os.getenv("PGUSER", "admin"),
    "password": password,
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
}
