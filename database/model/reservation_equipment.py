from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, sql, orm
from core.db_model import Base
from database.model.equipment import Equipment
from database.model.reservation import Reservation

class ReservationEquipment(Base):
    __tablename__ = 'reservation_equipment'
    
    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'), nullable=False, index=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now())
    # 'From' Relationships
    reservation = orm.relationship(Reservation, back_populates="reservation_equipments")
    equipment = orm.relationship(Equipment, back_populates="reservation_equipments")

ReservationEquipmentKeyEnum = Enum('ReservationEquipmentKeyEnum', {
    column.capitalize(): column for column in ReservationEquipment.__table__.columns.keys()
}, type=str)

ReservationEquipmentKeyTypes = {
    column.value: ReservationEquipment.__table__.columns[column].type.python_type for column in ReservationEquipmentKeyEnum
}