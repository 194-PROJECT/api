import factory
from database.factory.semester_factory import SemesterFactory
from database.postgres.database import PostgresDatabase
from database.model.classes import Class
from database.factory.users_factory import UserFactory

class_names = [
    'M-1', 'THX-1', 'WF-1', 'WF-2', 'S-1',
    'M-2', 'THX-2', 'WF-3', 'WF-4', 'S-2',
    'M-3', 'THX-3', 'WF-5', 'WF-6', 'S-3',
    'T-1', 'T-2', 'T-3', 'T-4', 'T-5',
    'W-1', 'W-2', 'W-3', 'W-4', 'W-5',
    'F-1', 'F-2', 'F-3', 'F-4', 'F-5',
    'MW-1', 'MW-2', 'MW-3', 'MW-4', 'MW-5',
    'TR-1', 'TR-2', 'TR-3', 'TR-4', 'TR-5',
]

class ClassFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Class
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('random_element', elements=class_names)
    description = factory.Faker('sentence')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    groups = factory.RelatedFactoryList(
        'database.factory.groups_factory.GroupFactory',
        size=1,
        factory_related_name='class_'
    )
    course = factory.SubFactory('database.factory.course_factory.CourseFactory')
    instructor = factory.SubFactory(UserFactory, is_faculty=True)
    semester = factory.SubFactory(SemesterFactory)
