
import os
import dotenv

# Initialize the environment variables
dotenv.load_dotenv()

# Load the environment variables
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")

DATABASE_URL = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DATABASE}"