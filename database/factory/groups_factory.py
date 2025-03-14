import factory
from database.factory.classes_factory import ClassFactory
from database.model.groups import Group
from database.postgres.database import PostgresDatabase

class GroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Group
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    class_ = factory.SubFactory(ClassFactory)
