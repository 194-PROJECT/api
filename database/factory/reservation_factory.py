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

    start_date = factory.Faker('date_time_this_year')
    end_date = factory.Faker('date_time_this_year')
    accepted = factory.Faker('boolean')
    returned = factory.Faker('boolean')
    reason = factory.Faker('sentence', nb_words=12, variable_nb_words=True)
    admin_note = factory.Faker('sentence')
    return_note = factory.Faker('sentence')
    return_date = factory.Faker('date_time_this_year')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    user = factory.SubFactory(UserFactory)
    admin = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
