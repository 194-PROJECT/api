from argparse import ArgumentParser
from database.postgres.seeder import DataSeeder as PostgresDataSeeder, IncludedModel

default_population = 10
default_include_models = [
    IncludedModel(
        model="Asset",
        population=5
    ),
    IncludedModel(
        model="Department",
        population=1
    ),
    IncludedModel(
        model="Reservation",
        population=5
    ),
    IncludedModel(
        model="Session",
        population=5
    ),
]

default_exclude_models = []

def main(
    database,
    include_models=default_include_models,
    exclude_models=default_exclude_models,
):
    seeders = {
        "postgres": PostgresDataSeeder,
    }

    seeder = seeders.get(database)
    if not seeder:
        raise ValueError(f"Unsupported database: {database}")

    print(f"Running seeder for {database} database")
    seeder(
        include_models=include_models,
        exclude_models=exclude_models,
    ).seed()


if __name__ == "__main__":
    parser = ArgumentParser(description="Run schema for the specified database.")
    parser.add_argument(
        "database", type=str, help="The database type (e.g., 'postgres')"
    )
    parser.add_argument(
        "--include-models", type=str, nargs="+", help="The models to include in seeding"
    )
    parser.add_argument(
        "--exclude-models",
        type=str,
        nargs="+",
        help="The models to exclude from seeding",
    )
    args = parser.parse_args()

    included_model = (
        args.include_models if args.include_models else default_include_models
    )
    excluded_models = (
        args.exclude_models if args.exclude_models else default_exclude_models
    )

    main(args.database, include_models=included_model, exclude_models=excluded_models)
