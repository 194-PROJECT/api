from typing import List, Optional
from src.dto.equipment.equipment_image_dto import EquipmentImageDTO
from src.repository.equipment.equipment_image_repository import EquipmentImageRepository

class EquipmentImageHandler:
    @staticmethod
    def get_images_by_equipment_id(equipment_id: int) -> Optional[List[EquipmentImageDTO]]:
        return EquipmentImageRepository.get_images_by_equipment_id(equipment_id)

    @staticmethod
    def add_image(image: EquipmentImageDTO) -> Optional[EquipmentImageDTO]:
        return EquipmentImageRepository.add_image(image)

    @staticmethod
    def get_image(image_id: int) -> Optional[EquipmentImageDTO]:
        return EquipmentImageRepository.get_image(image_id)

    @staticmethod
    def delete_image(image_id: int) -> None:
        EquipmentImageRepository.delete_image(image_id)
