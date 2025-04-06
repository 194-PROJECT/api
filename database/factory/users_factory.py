from random import choice
import factory
from core import auth_helper
from database.postgres.database import PostgresDatabase
from database.model.users import User
from src.enum.user.user_role_enum import UserRoleEnum
from src.enum.user.user_type_enum import UserTypeEnum
from src.handler.user.user_handler import UserHandler

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'
    
    class Params:
        is_faculty = factory.Trait(
            type=UserTypeEnum.FACULTY,
            role=UserRoleEnum.ADMIN,
        )

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.LazyFunction(lambda: auth_helper.hash_password('password'))
    type = factory.LazyFunction(lambda: choice([
                                                UserTypeEnum.MANAGEMENT,
                                                UserTypeEnum.FACULTY,
                                                UserTypeEnum.STAFF,
                                                UserTypeEnum.GUEST,
                                                UserTypeEnum.ALUMNI
                                            ]))
    role = factory.LazyAttribute(lambda obj: UserHandler.user_type_to_role_map[obj.type])
    profile_picture_url = factory.Faker('image_url')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
