import factory
from database.postgres.database import PostgresDatabase
from database.model.program import Program

program_names = [
    'BS Geodetic Engineering',
    'BS Computer Science',
    'BS Information Technology',
    'BS Software Engineering',
    'BS Data Science',
    'BS Cybersecurity',
    'BS Information Systems',
    'BS Computer Engineering',
    'BS Artificial Intelligence',
    'BS Game Development',
    'BS Network Administration',
    'BS Web Development',
    'BS Civil Engineering',
    'BS Mechanical Engineering',
    'BS Electrical Engineering',
    'BS Architecture',
    'BS Biology',
    'BS Chemistry',
    'BS Physics',
    'BS Mathematics',
    'BS Environmental Science',
    'BS Agriculture',
    'BS Forestry',
    'BS Nursing',
    'BS Pharmacy',
    'BS Psychology',
    'BS Education',
    'BS Business Administration',
    'BS Accountancy',
    'BS Tourism Management',
    'BS Hotel and Restaurant Management',
    'BS Fine Arts',
    'BS Music',
    'BS Political Science',
    'BS Sociology',
    'BS Anthropology',
    'BS History',
    'BS Philosophy',
    'BS Economics',
]

class ProgramFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Program
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    title = factory.Faker('random_element', elements=program_names)
    description = factory.Faker('text')
    credits_required = factory.Faker('random_int', min=120, max=180)
    duration = factory.Faker('pyfloat', min_value=2, max_value=4, right_digits=2, positive=True)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    students = factory.RelatedFactoryList(
        'database.factory.student_factory.StudentFactory',
        size=1,
        factory_related_name='program'
    )
    courses = factory.RelatedFactoryList(
        'database.factory.course_factory.CourseFactory',
        size=1,
        factory_related_name='program'
    )
    department = factory.SubFactory('database.factory.department_factory.DepartmentFactory')
