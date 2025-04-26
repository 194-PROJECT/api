import factory
from database.postgres.database import PostgresDatabase
from database.model.group_user import GroupUser
from database.factory.users_factory import UserFactory
from src.enum.user.user_type_enum import UserTypeEnum
from src.handler.user.user_handler import UserHandler

class GroupUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GroupUser
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    group = factory.SubFactory('database.factory.group_factory.GroupFactory')
    user = factory.SubFactory(
        UserFactory,
        type=UserTypeEnum.STUDENT,
        role=UserHandler.user_type_to_role_map[UserTypeEnum.STUDENT]
    )
