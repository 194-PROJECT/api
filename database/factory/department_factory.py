import factory
from database.postgres.database import PostgresDatabase
from database.model.department import Department

class DepartmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Department
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('company')
    description = factory.Faker('sentence')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
