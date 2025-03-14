import factory
from database.factory.program_factory import ProgramFactory
from database.postgres.database import PostgresDatabase
from database.model.course import Course

class CourseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Course
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    description = factory.Faker('text')
    credits = factory.Faker('random_int', min=1, max=5)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    program = factory.SubFactory(ProgramFactory)
    prerequisite = factory.Maybe(
        factory.Faker("boolean", chance_of_getting_true=50),
        factory.SubFactory('database.factory.course_factory.CourseFactory')  # Reference itself
    )
