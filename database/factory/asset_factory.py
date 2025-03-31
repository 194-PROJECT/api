import factory
from database.factory.asset_image_factory import AssetImageFactory
from database.postgres.database import PostgresDatabase
from database.model.asset import Asset

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
    purchased_by = factory.Faker('name')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    
    asset_images = factory.RelatedFactoryList(
        AssetImageFactory,
        size=5,
        factory_related_name='asset'
    )
