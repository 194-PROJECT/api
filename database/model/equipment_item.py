from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, orm, sql

from core.db_model import Base
from database.model.equipment import Equipment  # Assuming you have a Base class in your database module

class EquipmentItem(Base):
    __tablename__ = 'equipment_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_code = Column(String, nullable=False, unique=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'To' Relationships
    reservation_equipments = orm.relationship("ReservationEquipment", back_populates="equipment_item")
    # 'From' Relationships
    equipment = orm.relationship(Equipment, back_populates="equipment_items")

EquipmentItemKeyEnum = Enum('EquipmentItemKeyEnum', {
    column.capitalize(): column for column in EquipmentItem.__table__.columns.keys()
}, type=str)

EquipmentItemKeyTypes = {
    column.value: EquipmentItem.__table__.columns[column].type.python_type for column in EquipmentItemKeyEnum
}