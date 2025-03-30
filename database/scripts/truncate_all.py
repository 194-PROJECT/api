from database.postgres.query import QueryExecutor
import pkgutil
import importlib
import database.model

def execute():
    delete_all_database_tables()

def delete_all_database_tables():
    for _, module_name, _ in pkgutil.iter_modules(database.model.__path__):
        print(f"\033[92mImporting module: database.model.{module_name}\033[0m")
        module = importlib.import_module(f"database.model.{module_name}")
        print(f"\033[92mTruncating table corresponding to database.model.{module_name}\033[0m")
        for name, obj in vars(module).items():
            if isinstance(obj, type) and hasattr(obj, '__table__'):
                if module_name == obj.__table__.name:
                    query = f"TRUNCATE TABLE {obj.__table__.name} CASCADE"
                    print(f"\033[91mTruncating table: {obj.__table__.name}\033[0m")
                    QueryExecutor.execute(query)
                
