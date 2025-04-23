import factory
# from database.factory.equipment_availability_factory import EquipmentAvailabilityFactory
# from database.factory.equipment_image_factory import EquipmentImageFactory
from database.factory.equipment_image_factory import EquipmentImageFactory
from database.factory.reservation_equipment_factory import ReservationEquipmentFactory
from database.model.equipment import Equipment
from database.postgres.database import PostgresDatabase
from src.enum.equipment.equipment_category_enum import EquipmentCategoryEnum

names = (
    'Laptop', 'Projector', 'Whiteboard', 'Printer', 'Scanner', 'Tablet', 'Camera', 
    'Monitor', 'Keyboard', 'Mouse', 'Notebook', 'Pen', 'Eraser', 'Ruler', 'Marker', 
    'Stapler', 'Paper Clips', 'Highlighter', 'Glue Stick', 'Scissors'
)
name_to_description = {
    'Laptop': 'A portable computer designed for personal use, equipped with a screen, keyboard, and various hardware components to perform a wide range of tasks efficiently.',
    'Projector': 'A device that projects images, videos, or presentations onto a large screen or surface, commonly used in classrooms, offices, and home theaters.',
    'Whiteboard': 'A smooth, glossy white surface used for writing or drawing with erasable markers, often found in classrooms, offices, and meeting rooms.',
    'Printer': 'A machine that produces physical copies of digital documents or images on paper, widely used in homes, schools, and businesses.',
    'Scanner': 'An electronic device that converts physical documents, photos, or objects into digital format for storage, editing, or sharing.',
    'Tablet': 'A portable touchscreen device that combines the functionality of a smartphone and a laptop, ideal for browsing, reading, and entertainment.',
    'Camera': 'A device used for capturing high-quality images or videos, available in various types such as digital, DSLR, or mirrorless cameras.',
    'Monitor': 'A display screen that shows visual output from a computer or other devices, available in various sizes and resolutions for different purposes.',
    'Keyboard': 'An input device featuring a set of keys for typing text, executing commands, and interacting with computers or other electronic devices.',
    'Mouse': 'A handheld pointing device used to navigate and interact with graphical user interfaces on a computer screen, often equipped with buttons and a scroll wheel.',
    'Notebook': 'A small, portable book with blank or lined pages, commonly used for jotting down notes, ideas, or sketches.',
    'Pen': 'A writing instrument that uses ink to create marks on paper, available in various styles such as ballpoint, fountain, or gel pens.',
    'Eraser': 'A small tool made of rubber or similar material, designed to remove pencil marks from paper or other surfaces.',
    'Ruler': 'A straight-edged tool marked with measurements, used for drawing straight lines or measuring lengths accurately.',
    'Marker': 'A pen with a broad, felt tip that produces bold, colorful marks, often used for labeling, highlighting, or artistic purposes.',
    'Stapler': 'A mechanical device used to fasten sheets of paper together by driving metal staples through them, commonly found in offices and schools.',
    'Paper Clips': 'Small, metal or plastic devices used to hold sheets of paper together temporarily without causing damage.',
    'Highlighter': 'A pen filled with translucent, brightly colored ink, used to emphasize or mark important text in books, documents, or notes.',
    'Glue Stick': 'A solid adhesive packaged in a twistable tube, used for bonding paper, cardboard, or other lightweight materials in crafts and projects.',
    'Scissors': 'A handheld tool with two sharp blades, pivoted together, used for cutting paper, fabric, or other materials with precision.',
}

name_to_category = {
    'Laptop': EquipmentCategoryEnum.INSTRUMENT,
    'Projector': EquipmentCategoryEnum.INSTRUMENT,
    'Whiteboard': EquipmentCategoryEnum.TOOL,
    'Printer': EquipmentCategoryEnum.INSTRUMENT,
    'Scanner': EquipmentCategoryEnum.INSTRUMENT,
    'Tablet': EquipmentCategoryEnum.INSTRUMENT,
    'Camera': EquipmentCategoryEnum.INSTRUMENT,
    'Monitor': EquipmentCategoryEnum.INSTRUMENT,
    'Keyboard': EquipmentCategoryEnum.ACCESSORY,
    'Mouse': EquipmentCategoryEnum.ACCESSORY,
    'Notebook': EquipmentCategoryEnum.TOOL,
    'Pen': EquipmentCategoryEnum.TOOL,
    'Eraser': EquipmentCategoryEnum.TOOL,
    'Ruler': EquipmentCategoryEnum.TOOL,
    'Marker': EquipmentCategoryEnum.TOOL,
    'Stapler': EquipmentCategoryEnum.TOOL,
    'Paper Clips': EquipmentCategoryEnum.TOOL,
    'Highlighter': EquipmentCategoryEnum.TOOL,
    'Glue Stick': EquipmentCategoryEnum.TOOL,
    'Scissors': EquipmentCategoryEnum.TOOL,
}

class EquipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Equipment
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('random_element', elements=names)
    description = factory.LazyAttribute(lambda obj: name_to_description[obj.name])
    category = factory.LazyAttribute(lambda obj: name_to_category[obj.name])
    purchase_date = factory.Faker('date_time_this_year')
    price = factory.Faker('pyfloat', positive=True, right_digits=2, min_value=100, max_value=1000)
    purchased_by = factory.Faker('name')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    equipment_images = factory.RelatedFactoryList(
        EquipmentImageFactory,
        size=10,
        factory_related_name='equipment'
    )
    reservation_equipments = factory.RelatedFactoryList(
        ReservationEquipmentFactory,
        size=10,
        factory_related_name='equipment'
    )
    # equipment_availabilities = factory.RelatedFactoryList(EquipmentAvailabilityFactory, size=5)