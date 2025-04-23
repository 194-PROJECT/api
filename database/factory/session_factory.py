import secrets
import factory
from database.factory.users_factory import UserFactory
from database.postgres.database import PostgresDatabase
from database.model.session import Session


class SessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Session
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    token = factory.LazyFunction(lambda: secrets.token_hex(36))
    ip_address = factory.Faker('ipv4')
    user_agent = factory.Faker('user_agent')
    created_at = factory.Faker('date_time_this_year')
    expires_at = factory.Faker('date_time_this_year')
    last_active_at = factory.Faker('date_time_this_year')
    is_active = factory.Faker('boolean')
    device_id = factory.Faker('uuid4')
    location = factory.Faker('city')
    # Foreign key and relationship
    user = factory.SubFactory(UserFactory)