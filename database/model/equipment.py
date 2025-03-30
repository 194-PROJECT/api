from enum import Enum
from sqlalchemy import Column, DateTime, Float, Integer, String, Date, sql, orm
from core.db_model import Base

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, index=True)
    purchase_date = Column(Date, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'To' Relationships
    reservation_equipments = orm.relationship("ReservationEquipment", back_populates="equipment")
    equipment_images = orm.relationship("EquipmentImage", back_populates="equipment")
    equipment_availabilities = orm.relationship("EquipmentAvailability", back_populates="equipment")

EquipmentKeyEnum = Enum('EquipmentKeyEnum', {
    column.capitalize(): column for column in Equipment.__table__.columns.keys()
}, type=str)

EquipmentKeyTypes = {
    column.value: Equipment.__table__.columns[column].type.python_type for column in EquipmentKeyEnum
}