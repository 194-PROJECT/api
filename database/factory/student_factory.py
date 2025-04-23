from random import randint
import factory
from database.factory.users_factory import UserFactory
from database.model.student import Student
from database.postgres.database import PostgresDatabase

def generate_student_id():
        return f"{randint(2000, 2100)}-{str(randint(0, 20000)).zfill(5)}"

class StudentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    student_id = factory.LazyFunction(generate_student_id)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    program = factory.SubFactory('database.factory.program_factory.ProgramFactory')
    user = factory.SubFactory(UserFactory)