from argparse import ArgumentParser
from database.postgres.seeder import DataSeeder as PostgresDataSeeder

default_exclude_models=[
    "Program",
    "Department",
    "User",
    "Group",
    "Reservation",
    "Equipment",
    "Asset",
    "Semester",
]

def main(database, exclude_models=default_exclude_models):
    seeders = {
        "postgres": PostgresDataSeeder,
    }

    seeder = seeders.get(database)
    if not seeder:
        raise ValueError(f"Unsupported database: {database}")

    print(f"Running seeder for {database} database")
    seeder(
        exclude_models=exclude_models,
    ).seed()

if __name__ == "__main__":
    parser = ArgumentParser(description="Run schema for the specified database.")
    parser.add_argument("database", type=str, help="The database type (e.g., 'postgres')")
    parser.add_argument("--include-models", type=str, nargs="+", help="The models to include in seeding")
    parser.add_argument("--exclude-models", type=str, nargs="+", help="The models to exclude from seeding")
    args = parser.parse_args()

    excluded_models = args.exclude_models if args.exclude_models else default_exclude_models
    main(args.database, exclude_models=excluded_models)