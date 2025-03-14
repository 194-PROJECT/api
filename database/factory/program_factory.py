import factory
from database.factory.department_factory import DepartmentFactory
from database.postgres.database import PostgresDatabase
from database.model.program import Program

class ProgramFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Program
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    credits_required = factory.Faker('random_int', min=120, max=180)
    program_duration = factory.Faker('pyfloat', min_value=2, max_value=4)
    is_active = factory.Faker('boolean')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    department = factory.SubFactory(DepartmentFactory)
