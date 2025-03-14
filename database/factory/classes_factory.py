import factory
from database.factory.course_factory import CourseFactory
from database.factory.semester_factory import SemesterFactory
from database.postgres.database import PostgresDatabase
from database.model.classes import Class
from database.factory.users_factory import UserFactory

class ClassFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Class
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    course = factory.SubFactory(CourseFactory)
    instructor = factory.SubFactory(UserFactory)
    semester = factory.SubFactory(SemesterFactory)
