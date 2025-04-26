from datetime import datetime, timedelta
import factory
from database.postgres.database import PostgresDatabase
from database.model.semester import Semester

class SemesterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Semester
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    _current_end_date = datetime.today() + timedelta(weeks=2)  # Adjust this as needed
    _semester_counter = 0  # Even = 1st Sem, Odd = 2nd Sem

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        semester_duration = timedelta(weeks=20)  # ~5 months

        # Calculate end and start dates
        end_date = cls._current_end_date
        start_date = end_date - semester_duration

        # Determine semester label
        is_first_sem = cls._semester_counter % 2 == 1
        semester_label = "1st Semester" if is_first_sem else "2nd Semester"

        # Academic year: use start year for label
        acad_year_start = start_date.year
        acad_year_end = acad_year_start + 1
        name = f"{semester_label} {acad_year_start}-{acad_year_end}"

        # Update tracker for next semester
        cls._current_end_date = start_date - timedelta(days=1)
        cls._semester_counter += 1

        # Set fields
        kwargs['start_date'] = start_date
        kwargs['end_date'] = end_date
        kwargs.setdefault('created_at', start_date)
        kwargs.setdefault('updated_at', start_date)
        kwargs.setdefault('name', name)

        return super()._create(model_class, *args, **kwargs)

    # classes = factory.RelatedFactoryList(
    #     'database.factory.classes_factory.ClassFactory',
    #     factory_related_name='semester',  # must match FK field in Class
    #     size=3
    # )
