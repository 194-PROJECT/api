import factory
from database.postgres.database import PostgresDatabase
from database.model.semester import Semester

class SemesterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Semester
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    start_date = factory.Faker('date_this_year')
    end_date = factory.Faker('date_this_year')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
