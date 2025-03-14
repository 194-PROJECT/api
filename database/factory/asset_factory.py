import factory
from database.postgres.database import PostgresDatabase
from database.model.asset import Asset
from database.factory.users_factory import UserFactory

class AssetFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Asset
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    category = factory.Faker('random_element', elements=('electronic', 'furniture', 'clothing', 'kitchenware'))
    purchase_date = factory.Faker('date_time_this_year')
    price = factory.Faker('pyfloat', positive=True)
    purchased_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    user = factory.SubFactory(UserFactory)
