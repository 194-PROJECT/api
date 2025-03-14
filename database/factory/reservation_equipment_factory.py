import factory
from database.factory.reservation_factory import ReservationFactory
from database.factory.equipment_factory import EquipmentFactory
from database.model.reservation_equipment import ReservationEquipment
from database.postgres.database import PostgresDatabase

class ReservationEquipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ReservationEquipment
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    quantity = factory.Faker('random_int', min=1, max=10)
    start_date = factory.Faker('date_time_this_year')
    end_date = factory.Faker('date_time_this_year')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    reservation = factory.SubFactory(ReservationFactory)
    equipment = factory.SubFactory(EquipmentFactory)