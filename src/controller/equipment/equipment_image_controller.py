from flask import request
from core.api import Api, response

from src.dto.equipment.equipment_image_dto import EquipmentImageDTO
from src.handler.equipment.equipment_image_handler import EquipmentImageHandler

app = Api.application

@app.route('/equipment/image/<int:id>', methods=['GET'])
def get_equipment_image(id: int):
    image = EquipmentImageHandler.get_image(id)

    if not image:
        return response(
            message="Image not found",
            code=404,
            errors=["Failed to retrieve the requested image"],
        )

    return response(
        message="Image found",
        code=200,
        data=image.model_dump()
    )

@app.route('/equipment/<int:equipment_id>/image', methods=['GET'])
def get_equipment_images(equipment_id: int):
    images = EquipmentImageHandler.get_images_by_equipment_id(equipment_id)

    if images is None:
        return response(
            message="No images found for the specified equipment",
            code=404,
            errors=["Failed to retrieve images for the equipment"],
        )

    return response(
        message="Equipment images found",
        code=200,
        data=[image.model_dump() for image in images]
    )

@app.route('/equipment/<int:equipment_id>/image', methods=['POST'])
def add_equipment_image(equipment_id: int):
    image_data = EquipmentImageDTO(**request.json)
    image_data.equipment_id = equipment_id
    image = EquipmentImageHandler.add_image(image_data)

    if not image:
        return response(
            message="Failed to add image to equipment",
            code=400,
            errors=["Failed to add image with the provided data"],
        )

    return response(
        message="Image added to equipment",
        code=201,
        data=image.model_dump()
    )

@app.route('/equipment/image/<int:image_id>', methods=['DELETE'])
def delete_equipment_image(image_id: int):
    image = EquipmentImageHandler.get_image(image_id)

    if not image:
        return response(
            message="Image not found",
            code=404,
            errors=["Failed to retrieve the requested image for deletion"],
        )

    EquipmentImageHandler.delete_image(image_id)

    return response(
        message="Image deleted",
        code=200
    )

