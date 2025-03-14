import factory
# from database.factory.equipment_availability_factory import EquipmentAvailabilityFactory
# from database.factory.equipment_image_factory import EquipmentImageFactory
from database.model.equipment import Equipment
from database.postgres.database import PostgresDatabase

class EquipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Equipment
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    category = factory.Faker('random_element', elements=('electronic', 'furniture', 'clothing', 'kitchenware'))
    purchase_date = factory.Faker('date_time_this_year')
    price = factory.Faker('pyfloat', positive=True)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    # equipment_images = factory.RelatedFactoryList(EquipmentImageFactory, size=5)
    # equipment_availabilities = factory.RelatedFactoryList(EquipmentAvailabilityFactory, size=5)