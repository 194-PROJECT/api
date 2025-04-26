from random import choice
import factory
from database.model.classes import Class
from database.model.groups import Group
from database.postgres.database import PostgresDatabase

group_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Theta', 'Sigma', 'Omega']

class GroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Group
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.LazyAttribute(lambda obj: obj.class_.name + ' ' + choice(group_names))
    description = 'A random group description'
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    users = factory.RelatedFactoryList(
        'database.factory.group_user_factory.GroupUserFactory',
        size=1,
        factory_related_name='group'
    )
    class_ = factory.LazyFunction(
        lambda: choice(PostgresDatabase.get_seed_session().query(Class).all())
    )
