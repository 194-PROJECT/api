from random import choice
import factory
from database.factory.equipment_item_factory import EquipmentItemFactory
from database.model.reservation_equipment import ReservationEquipment
from database.postgres.database import PostgresDatabase
from src.enum.reservation_equipment.mishandle_type_enum import MishandleTypeEnum

class ReservationEquipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ReservationEquipment
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    returned = factory.LazyAttribute(
        lambda obj: obj.reservation.returned if obj.reservation else None
    )
    mishandled = factory.LazyAttribute(
        lambda obj: choice([True, False]) if obj.returned else None
    )
    mishandle_type = factory.LazyAttribute(
        lambda obj: choice([
            MishandleTypeEnum.MINOR_DAMAGE,
            MishandleTypeEnum.NON_FUNCTIONAL,
            MishandleTypeEnum.LOST,
            MishandleTypeEnum.OTHER,
        ]) if obj.mishandled else None
    )
    mishandle_description = factory.Maybe(
        'mishandled',
        yes_declaration=factory.Faker('sentence', nb_words=10),
        no_declaration=None
    )
    data_requested = factory.Maybe(
        'returned',
        yes_declaration=factory.LazyAttribute(lambda obj: choice([True, False]) if not obj.mishandled else False),
        no_declaration=None
    )
    data_received = factory.Maybe(
        'data_requested',
        yes_declaration=factory.Faker('boolean', chance_of_getting_true=50),
        no_declaration=None
    )
    data_request_description = factory.Maybe(
        'data_requested',
        yes_declaration=factory.Faker('sentence', nb_words=10),
        no_declaration=None
    )
    data_request_date = factory.Maybe(
        'data_requested',
        yes_declaration=factory.Faker('date_time_this_year', after_now=True),
        no_declaration=None
    )
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
