from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, sql, orm
from core.db_model import Base

class EquipmentImage(Base):
    __tablename__ = 'equipment_image'

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=False, index=True)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now())
    # 'From' Relationships
    equipment = orm.relationship("Equipment", back_populates="equipment_images", foreign_keys=[equipment_id])

EquipmentImageKeyEnum = Enum('EquipmentImageKeyEnum', {
    column.capitalize(): column for column in EquipmentImage.__table__.columns.keys()
}, type=str)

EquipmentImageKeyTypes = {
    column.value: EquipmentImage.__table__.columns[column].type.python_type for column in EquipmentImageKeyEnum
}