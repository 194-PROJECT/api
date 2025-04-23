import factory
from database.model.groups import Group
from database.postgres.database import PostgresDatabase

group_names = [
    'Group A',
    'Group B',
    'Group C',
    'Group D',
    'Group E',
]

class GroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Group
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('random_element', elements=group_names)
    description = 'A random group description'
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    users = factory.RelatedFactoryList(
        'database.factory.group_user_factory.GroupUserFactory',
        size=1,
        factory_related_name='group'
    )
    class_ = factory.SubFactory('database.factory.classes_factory.ClassFactory')
