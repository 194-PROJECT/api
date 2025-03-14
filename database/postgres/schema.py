from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.db_model import Base
from .config import DATABASE_URL
import pkgutil
import importlib
import database.model

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database_tables():
    '''
    Initializes the database tables by importing all modules in the `database.model` package
    and creating all tables defined in the metadata.
    This function performs the following steps:
    1. Prints the path of the `database.model` package.
    2. Iterates over all modules in the `database.model` package and imports them.
    3. Creates all tables defined in the `Base` metadata using the provided database engine.
    Note:
        Ensure that the `database.model` package and its modules are correctly structured
        and that the `core.db_model.SingletonBase.base` is properly defined.
    Raises:
        ImportError: If there is an issue importing any of the modules in the `database.model` package.
    '''
    print("database.models path:", database.model.__path__)
    for _, module_name, _ in pkgutil.iter_modules(database.model.__path__):
        print(f"\033[92mImporting module: database.model.{module_name}\033[0m")
        importlib.import_module(f"database.model.{module_name}")
    
    Base.metadata.create_all(bind=engine)
