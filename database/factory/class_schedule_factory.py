
from random import choice
import factory
from database.factory.classes_factory import ClassFactory
from database.model.class_schedule import ClassSchedule
from database.postgres.database import PostgresDatabase
from src.enum.time.day_enum import DayEnum

class ClassScheduleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ClassSchedule
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    day = factory.LazyFunction(lambda: choice(list(DayEnum)))
    start_time = factory.Faker('time')
    end_time = factory.Faker('time')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    class_ = factory.SubFactory(ClassFactory)