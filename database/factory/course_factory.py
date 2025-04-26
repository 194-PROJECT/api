import factory
from database.factory.classes_factory import ClassFactory
from database.factory.semester_factory import SemesterFactory
from database.postgres.database import PostgresDatabase
from database.model.course import Course

course_names = [
    'BS-301',
    'MA-101',
    'CS-101',
    'ENG-201',
    'PHY-101',
    'CHEM-101',
    'BIO-101',
    'HIST-101',
    'PHIL-101',
    'ART-101',
    'MATH-101',
    'STAT-101',
    'CS-201',
    'ECON-101',
    'PSYCH-101',
    'SOC-101',
    'LAW-101',
    'MED-101',
    'ENG-301',
    'CS-301',
    'PHYS-201',
    'CHEM-201',
    'BIO-201',
    'HIST-201',
    'PHIL-201',
    'ART-201',
    'MATH-201',
    'STAT-201',
    'CS-401',
    'ENG-401',
    'PHY-301',
    'CHEM-301',
    'BIO-301',
    'HIST-301',
    'PHIL-301',
    'ART-301',
    'MATH-301',
    'STAT-301',
    'CS-501',
    'ENG-501',
    'PHY-401',
    'CHEM-401',
    'BIO-401',
    'HIST-401',
    'PHIL-401',
    'ART-401',
    'MATH-401',
    'STAT-401',
]

class CourseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Course
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    # Generate multiple semesters to assign to classes
    _semesters = SemesterFactory.create_batch(3)

    name = factory.Faker('random_element', elements=course_names)
    description = factory.Faker('text')
    credits = factory.Faker('random_int', min=1, max=5)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')

    program = factory.SubFactory('database.factory.program_factory.ProgramFactory')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Create the course first
        instance = super()._create(model_class, *args, **kwargs)

        # Now create the classes and associate them with the course and semesters
        for i in range(5):
            semester = cls._semesters[i % len(cls._semesters)]
            ClassFactory(course=instance, semester=semester)  # Pass course and semester

        return instance

    # @factory.post_generation
    # def set_prerequisites(obj, create, extracted, **kwargs):
    #     if not create:
    #         return

    #     obj.prerequisite_id = obj.id - 1 if obj.id > 1 else None
