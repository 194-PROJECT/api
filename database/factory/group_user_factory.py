import factory
from database.factory.groups_factory import GroupFactory
from database.postgres.database import PostgresDatabase
from database.model.group_user import GroupUser
from database.factory.users_factory import UserFactory

class GroupUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GroupUser
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    group = factory.SubFactory(GroupFactory)
    users = factory.SubFactory(UserFactory)
