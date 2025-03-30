from database.postgres.query import QueryExecutor
from database.model.equipment_image import EquipmentImage
from sqlalchemy import delete, insert, select
from sqlalchemy.dialects import postgresql
from typing import Optional, List
from src.dto.equipment.equipment_image_dto import EquipmentImageDTO

class EquipmentImageRepository:
    @staticmethod
    def get_images_by_equipment_id(equipment_id: int) -> Optional[List[EquipmentImageDTO]]:
        query = select(EquipmentImage).where(EquipmentImage.equipment_id == equipment_id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_all(str(query))
        return [EquipmentImageDTO(**image) for image in data] if data else None

    @staticmethod
    def add_image(image: EquipmentImageDTO) -> Optional[EquipmentImageDTO]:
        query = (
            insert(EquipmentImage)
            .values(
                equipment_id=image.equipment_id,
                image_url=image.image_url,
                created_at=image.created_at,
                updated_at=image.updated_at,
            )
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return EquipmentImageDTO(**data) if data else None

    @staticmethod
    def get_image(image_id: int) -> Optional[EquipmentImageDTO]:
        query = select(EquipmentImage).where(EquipmentImage.id == image_id).compile(
            compile_kwargs={"literal_binds": True},
            dialect=postgresql.dialect(),
        )
        data = QueryExecutor.fetch_one(str(query))
        return EquipmentImageDTO(**data) if data else None

    @staticmethod
    def delete_image(image_id: int) -> None:
        query = (
            delete(EquipmentImage)
            .where(EquipmentImage.id == image_id)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        QueryExecutor.delete_one(str(query))
