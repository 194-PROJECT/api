from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Time, sql, orm
from core.db_model import Base
from database.model import equipment

class EquipmentAvailability(Base):
    __tablename__ = 'equipment_availability'
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=False, index=True)
    day = Column(String(10), nullable=False, index=True)
    start_time = Column(Time(timezone=True), nullable=False, index=True)
    end_time = Column(Time(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'From' Relationships
    equipment = orm.relationship(equipment.Equipment, back_populates="equipment_availabilities", foreign_keys=[equipment_id])

EquipmentAvailabilityKeyEnum = Enum('EquipmentAvailabilityKeyEnum', {
    column.capitalize(): column for column in EquipmentAvailability.__table__.columns.keys()
}, type=str)

EquipmentAvailabilityKeyTypes = {
    column.value: EquipmentAvailability.__table__.columns[column].type.python_type for column in EquipmentAvailabilityKeyEnum
}