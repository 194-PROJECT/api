from argparse import ArgumentParser
from database.postgres.schema import initialize_database_tables

def main(database):
    handlers = {
        "postgres": initialize_database_tables,
    }

    handler = handlers.get(database)
    if not handler:
        raise ValueError(f"Unsupported database: {database}")
    
    print(f"Running schema for {database} database")
    handler()

if __name__ == "__main__":
    parser = ArgumentParser(description="Run schema for the specified database.")
    parser.add_argument("database", type=str, help="The database type (e.g., 'postgres')")
    args = parser.parse_args()

    main(args.database)