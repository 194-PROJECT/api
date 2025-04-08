import factory
from database.model.equipment_item import EquipmentItem
from database.postgres.database import PostgresDatabase


class EquipmentItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = EquipmentItem
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    item_code = factory.Faker('uuid4')  # Generate a unique item code
    available = True
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')

    # Foreign key and relationship
    equipment = factory.SubFactory('database.factory.equipment_factory.EquipmentFactory')
