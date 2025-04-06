import random
import factory
from database.postgres.database import PostgresDatabase
from database.model.semester import Semester

def random_semester_name():
    """Generate a random semester name."""
    semesters = ['1st Semester', '2nd Semester', 'Midyear']
    year = random.randint(2000, 2025)  # Random year between 2000 and 2025
    return f"A.Y. {year}-{year+1}, {random.choice(semesters)}"

class SemesterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Semester
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.LazyFunction(random_semester_name)
    start_date = factory.Faker('date_this_year')
    end_date = factory.Faker('date_this_year')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
