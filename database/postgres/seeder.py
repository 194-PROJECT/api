import importlib
import inspect
import pkgutil
import string
import factory

from typing import TypedDict, Dict, Any

import database.model
from database.postgres.database import PostgresDatabase

class ModelMetadata(TypedDict):
    table_name: str
    module_name: str
    model: type

class IncludedModel(TypedDict):
    model: string
    population: int

class DataSeeder:
    def __init__(
        self,
        include_models: list[IncludedModel] = [],
        exclude_models: list[str] = [],
        default_population: int = 10,
    ):
        self.include_models = include_models
        self.exclude_models = exclude_models
        self.default_population = default_population

    def get_model_metadata(self) -> Dict[str, ModelMetadata]:
        model_metadata = {}

        for _, module_name, _ in pkgutil.iter_modules(database.model.__path__):
            module = importlib.import_module(f"database.model.{module_name}")
            for name in dir(module):
                obj = getattr(module, name)
                if hasattr(obj, "__tablename__"):
                    model_metadata[name] = ModelMetadata(
                        table_name=obj.__tablename__,
                        module_name = module.__name__.split(".")[-1],
                        model=obj,
                    )  # type: ignore

        return model_metadata

    def seed_data(self, model_metadata: ModelMetadata) -> list[Any]:
        print(f"\033[92mSeeding {model_metadata['model'].__tablename__}...\033[0m")
        module = importlib.import_module(
            f"database.factory.{model_metadata['module_name']}_factory"
        )
        for name in dir(module):
            obj = getattr(module, name)
            # check if obj is a class

            if inspect.isclass(obj) and issubclass(obj, factory.Factory):
                included_model = next(
                    (
                        included_model
                        for included_model in self.include_models
                        if included_model["model"] == model_metadata["model"].__name__
                    ),
                    IncludedModel(
                        model=model_metadata["model"].__name__,
                        population=self.default_population,
                    ),
                )

                obj.create_batch(size=included_model["population"])

    def seed(self):
        PostgresDatabase.new_seed_session()
        model_metadata = self.get_model_metadata()

        if not self.include_models:
            self.include_models = [
                IncludedModel(
                    model=value["model"].__name__, population=self.default_population
                )
                for value in model_metadata.values()
            ]

        filtered_model_metadata = {
            key: value
            for key, value in model_metadata.items()
            if value["model"].__name__
            in [model["model"] for model in self.include_models]
            and value["model"].__name__ not in self.exclude_models
        }

        for model_metadata in filtered_model_metadata.values():
            self.seed_data(model_metadata)
