import factory
from database.factory.equipment_factory import EquipmentFactory
from database.model.equipment_image import EquipmentImage
from database.postgres.database import PostgresDatabase

class EquipmentImageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = EquipmentImage
        sqlalchemy_session_factory = PostgresDatabase.get_session
        sqlalchemy_session_persistence = 'commit'

    image_url = factory.Faker('random_element', elements=(
        'https://images.pexels.com/photos/1078884/pexels-photo-1078884.jpeg?cs=srgb&dl=pexels-rezwan-1078884.jpg&fm=jpg',
        'https://i5.walmartimages.com/seo/SINGER-Multipurpose-Scissor-Set-8-5-Inch-Sewing-Fabric-Scissors-6-5-Craft-4-Mini-Detail-Thread-Scissors-Comfort-Hand-Grip-Pack-3_0cea116d-6f6b-4bc3-9f3b-2527a8a65c64.4696a4cd58b2eb8b4706ab0de9dccb3e.jpeg',
        'https://media.rs-online.com/image/upload/bo_1.5px_solid_white,b_auto,c_pad,dpr_2,f_auto,h_399,q_auto,w_710/c_pad,h_399,w_710/F1846690-01?pgw=1'
    ))
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    equipment = factory.SubFactory(EquipmentFactory)