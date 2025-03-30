import factory
# from database.factory.equipment_availability_factory import EquipmentAvailabilityFactory
# from database.factory.equipment_image_factory import EquipmentImageFactory
from database.model.equipment import Equipment
from database.postgres.database import PostgresDatabase

names = (
    'Laptop', 'Projector', 'Whiteboard', 'Printer', 'Scanner', 'Tablet', 'Camera', 
    'Monitor', 'Keyboard', 'Mouse', 'Notebook', 'Pen', 'Eraser', 'Ruler', 'Marker', 
    'Stapler', 'Paper Clips', 'Highlighter', 'Glue Stick', 'Scissors'
)
name_to_description = {
    'Laptop': 'A portable computer for personal use.',
    'Projector': 'A device that projects images or videos onto a screen.',
    'Whiteboard': 'A smooth white surface for writing or drawing.',
    'Printer': 'A device that prints documents and images.',
    'Scanner': 'A device that converts physical documents into digital format.',
    'Tablet': 'A portable touchscreen computer.',
    'Camera': 'A device for capturing images or videos.',
    'Monitor': 'A screen for displaying computer output.',
    'Keyboard': 'An input device for typing.',
    'Mouse': 'A pointing device for computer navigation.',
    'Notebook': 'A small book for writing notes.',
    'Pen': 'A tool for writing with ink.',
    'Eraser': 'An item used to remove pencil marks.',
    'Ruler': 'A tool for measuring and drawing straight lines.',
    'Marker': 'A pen with a broad tip for marking.',
    'Stapler': 'A device for fastening papers together.',
    'Paper Clips': 'Small devices for holding sheets of paper together.',
    'Highlighter': 'A pen for marking text with translucent color.',
    'Glue Stick': 'A solid adhesive in a twistable tube.',
    'Scissors': 'A tool for cutting paper or other materials.',
}
name_to_category = {
    'Laptop': 'electronic',
    'Projector': 'electronic',
    'Whiteboard': 'school supplies',
    'Printer': 'utility',
    'Scanner': 'utility',
    'Tablet': 'electronic',
    'Camera': 'electronic',
    'Monitor': 'electronic',
    'Keyboard': 'utility',
    'Mouse': 'utility',
    'Notebook': 'school supplies',
    'Pen': 'school supplies',
    'Eraser': 'school supplies',
    'Ruler': 'school supplies',
    'Marker': 'school supplies',
    'Stapler': 'office supplies',
    'Paper Clips': 'office supplies',
    'Highlighter': 'school supplies',
    'Glue Stick': 'school supplies',
    'Scissors': 'utility',
}

class EquipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Equipment
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('random_element', elements=('Laptop', 'Projector', 'Whiteboard', 'Printer', 'Scanner'))
    description = factory.LazyAttribute(lambda obj: name_to_description[obj.name])
    category = factory.LazyAttribute(lambda obj: name_to_category[obj.name])
    purchase_date = factory.Faker('date_time_this_year')
    price = factory.Faker('pyfloat', positive=True, right_digits=2, min_value=100, max_value=1000)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    # equipment_images = factory.RelatedFactoryList(EquipmentImageFactory, size=5)
    # equipment_availabilities = factory.RelatedFactoryList(EquipmentAvailabilityFactory, size=5)