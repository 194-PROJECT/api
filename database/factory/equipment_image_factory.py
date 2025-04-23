import factory
from database.model.equipment_image import EquipmentImage
from database.postgres.database import PostgresDatabase

class EquipmentImageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = EquipmentImage
        sqlalchemy_session_factory = PostgresDatabase.get_seed_session
        sqlalchemy_session_persistence = 'commit'

    image_url = factory.Faker('random_element', elements=(
        'https://images.pexels.com/photos/1078884/pexels-photo-1078884.jpeg?cs=srgb&dl=pexels-rezwan-1078884.jpg&fm=jpg',
        'https://i5.walmartimages.com/seo/SINGER-Multipurpose-Scissor-Set-8-5-Inch-Sewing-Fabric-Scissors-6-5-Craft-4-Mini-Detail-Thread-Scissors-Comfort-Hand-Grip-Pack-3_0cea116d-6f6b-4bc3-9f3b-2527a8a65c64.4696a4cd58b2eb8b4706ab0de9dccb3e.jpeg',
        'https://media.rs-online.com/image/upload/bo_1.5px_solid_white,b_auto,c_pad,dpr_2,f_auto,h_399,q_auto,w_710/c_pad,h_399,w_710/F1846690-01?pgw=1',
        'https://advancedct.com/wp-content/uploads/2016/02/shutterstock_617755751.jpg',
        'https://theparashopmanila.com/cdn/shop/products/s-l640_a70b5130-3782-4509-9c7a-4bbc06396253.jpg?v=1644742381',
        'https://i.ebayimg.com/images/g/S20AAOSwP2ddVtqu/s-l1200.jpg',
        'https://multimedia.3m.com/mws/media/1528005J/J.jpg?width=506',
        'https://down-ph.img.susercontent.com/file/b65ce7990823f5c556f7ef28c2b65bb8',
        'https://merriam-webster.com/assets/mw/images/gallery/gal-wap-slideshow-slide/image1294857992-5173-f5c77f4215a3f8bec22ab164b6e07450@1x.jpg',
        'https://zbga.shopsuki.ph/cdn/shop/files/107504359_800x.png?v=1710211365',
    ))
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.Faker('date_time_this_year')
    # Foreign key and relationship
    equipment = factory.SubFactory('database.factory.equipment_factory.EquipmentFactory')