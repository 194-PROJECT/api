from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, sql, orm
from core.db_model import Base
from database.model.groups import Group
from database.model.users import User

class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey('users.id'), index=True)
    group_id = Column(Integer, ForeignKey('groups.id'), index=True)
    accepted = Column(Boolean, nullable=False, default=False, index=True)
    returned = Column(Boolean, nullable=False, default=False, index=True)
    reason = Column(String(255), nullable=False)
    admin_note = Column(String(255))
    return_note = Column(String(255))
    return_date = Column(DateTime(timezone=True), index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now(), index=True)
    # 'From' Relationships
    user = orm.relationship(User, back_populates="reservations", foreign_keys=[user_id])
    admin = orm.relationship(User, back_populates="reservations_checked_by", foreign_keys=[admin_id])
    group = orm.relationship(Group, back_populates="reservations")
    # 'To' Relationships
    reservation_equipments = orm.relationship("ReservationEquipment", back_populates="reservation")

ReservationKeyEnum = Enum('ReservationKeyEnum', {
    column.capitalize(): column for column in Reservation.__table__.columns.keys()
}, type=str)

ReservationKeyTypes = {
    column.value: Reservation.__table__.columns[column].type.python_type for column in ReservationKeyEnum
}