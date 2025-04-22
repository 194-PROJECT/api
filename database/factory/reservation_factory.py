from datetime import timedelta
from random import randint
import factory
from database.factory.users_factory import UserFactory
from database.factory.groups_factory import GroupFactory
from database.postgres.database import PostgresDatabase
from database.model.reservation import Reservation

class ReservationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Reservation
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    start_date = factory.Faker('date_time_this_year', after_now=True, before_now=False)
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(hours=randint(1, 6), minutes=randint(0, 59)))
    accepted = factory.Faker('boolean')
    claimed = factory.Maybe(
        'accepted',
        yes_declaration=factory.Faker('boolean', chance_of_getting_true=50),
        no_declaration=False,
    )
    returned = factory.Maybe(
        'claimed',
        yes_declaration=factory.Faker('boolean', chance_of_getting_true=50),
        no_declaration=False,
    )
    reason = factory.Faker('sentence', nb_words=12, variable_nb_words=True)
    admin_note = factory.Faker('sentence', nb_words=12, variable_nb_words=True)
    return_note = factory.Faker('sentence', nb_words=12, variable_nb_words=True)
    return_date = factory.Maybe(
        'returned',
        yes_declaration=factory.LazyAttribute(lambda obj: obj.end_date + timedelta(hours=randint(1, 24), minutes=randint(0, 59))),
        no_declaration=None,
    )
    created_at = factory.LazyAttribute(lambda obj: obj.start_date - timedelta(hours=randint(1, 24), minutes=randint(0, 59)))
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    user = factory.SubFactory(UserFactory)
    admin = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
