from datetime import timedelta
from random import choice, randint
import factory
from database.factory.users_factory import UserFactory
from database.factory.groups_factory import GroupFactory
from database.model.classes import Class
from database.postgres.database import PostgresDatabase
from database.model.reservation import Reservation
from src.dto.group.group_user_dto import GroupUserDTO
from src.handler.group.group_user_handler import GroupUserHandler

class ReservationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Reservation
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    start_date = factory.Faker('date_time_this_year', after_now=True, before_now=False)
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(hours=randint(1, 6), minutes=randint(0, 59)))
    accepted = factory.Faker('boolean', chance_of_getting_true=95)
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
        yes_declaration=factory.LazyAttribute(lambda obj: choice([
            obj.end_date + timedelta(hours=randint(1, 24), minutes=randint(0, 59)),
            obj.end_date - timedelta(minutes=randint(0, 5)),
        ])),
        no_declaration=None,
    )
    created_at = factory.LazyAttribute(lambda obj: obj.start_date - timedelta(hours=randint(1, 24), minutes=randint(0, 59)))
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    user = factory.SubFactory(UserFactory)
    admin = factory.SubFactory(UserFactory)
    class_ = factory.LazyFunction(
        lambda: choice(PostgresDatabase.get_seed_session().query(Class).all())
    )
    group = factory.SubFactory(GroupFactory, class_=factory.SelfAttribute('..class_'))
    
    @factory.post_generation
    def after_group_create(self, create, extracted, **kwargs):
        if not create:
            return
        
        if self.group:
            GroupUserHandler.create_group_user(GroupUserDTO(**{
                'user_id': self.user.id,
                'group_id': self.group.id,
            }))
