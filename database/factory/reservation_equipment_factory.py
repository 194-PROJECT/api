import factory
from database.factory.equipment_item_factory import EquipmentItemFactory
from database.model.reservation_equipment import ReservationEquipment
from database.postgres.database import PostgresDatabase

class ReservationEquipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ReservationEquipment
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    returned = True
    mishandled = False
    rating = factory.Faker('random_int', min=1, max=5)
    comment = factory.Faker('sentence', nb_words=10)
    admin_note = factory.Faker('sentence', nb_words=10)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    reservation = factory.SubFactory('database.factory.reservation_factory.ReservationFactory')
    equipment = factory.SubFactory('database.factory.equipment_factory.EquipmentFactory')
    equipment_item = factory.LazyAttribute(
        lambda obj: EquipmentItemFactory(equipment=obj.equipment) if obj.equipment else None
    )
