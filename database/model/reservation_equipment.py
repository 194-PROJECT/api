from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, sql, orm
from core.db_model import Base
from database.model.equipment import Equipment
from database.model.equipment_item import EquipmentItem
from database.model.reservation import Reservation

class ReservationEquipment(Base):
    __tablename__ = 'reservation_equipment'
    
    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id', ondelete='CASCADE'), nullable=False, index=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id', ondelete='SET NULL'), index=True)
    equipment_item_id = Column(Integer, ForeignKey('equipment_item.id', ondelete='SET NULL'), index=True)
    returned = Column(Boolean, default=False)
    mishandled = Column(Boolean, default=False)
    rating = Column(Integer, nullable=True)
    comment = Column(String(255), nullable=True)
    admin_note = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'From' Relationships
    reservation = orm.relationship(Reservation, back_populates="reservation_equipments")
    equipment = orm.relationship(Equipment, back_populates="reservation_equipments")
    equipment_item = orm.relationship(EquipmentItem, back_populates="reservation_equipments")

ReservationEquipmentKeyEnum = Enum('ReservationEquipmentKeyEnum', {
    column.capitalize(): column for column in ReservationEquipment.__table__.columns.keys()
}, type=str)

ReservationEquipmentKeyTypes = {
    column.value: ReservationEquipment.__table__.columns[column].type.python_type for column in ReservationEquipmentKeyEnum
}