import factory
from database.factory.asset_factory import AssetFactory
from database.model.asset_image import AssetImage
from database.postgres.database import PostgresDatabase

class AssetImageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AssetImage
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    image_url = factory.Faker('random_element', elements=(
        'https://www.furnituremanila.com.ph/wp-content/uploads/2024/11/Photoroom_000_20241106_003636.jpeg',
        'https://www.level.com.au/blog/wp-content/uploads/2023/12/Untitled-design-10.png',
        'https://upload.wikimedia.org/wikipedia/commons/2/22/3-Tasten-Maus_Microsoft.jpg',
        
    ))
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    asset = factory.SubFactory(AssetFactory)
