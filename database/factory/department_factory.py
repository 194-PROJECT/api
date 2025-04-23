import factory
from database.postgres.database import PostgresDatabase
from database.model.department import Department

department_names = [
    'Department of Computer Science',
    'Department of Biology',
    'Department of Chemistry',
    'Department of Physics',
    'Department of Mathematics',
    'Department of Economics',
    'Department of Psychology',
    'Department of Sociology',
    'Department of Political Science',
    'Department of History',
    'Department of Philosophy',
]

class DepartmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Department
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('random_element', elements=department_names)
    description = factory.Faker('sentence')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    programs = factory.RelatedFactoryList(
        'database.factory.program_factory.ProgramFactory',
        size=1,
        factory_related_name='department'
    )
