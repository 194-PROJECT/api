
import os
import dotenv

# Initialize the environment variables
dotenv.load_dotenv(override=True)

# Load the environment variables
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_SSL_MODE = os.getenv("POSTGRESQL_SSL_MODE", "prefer")

DATABASE_URL = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DATABASE}?sslmode={POSTGRESQL_SSL_MODE}"