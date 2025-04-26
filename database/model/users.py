from enum import Enum
from sqlalchemy import Column, DateTime, Integer, String, orm, sql
from core.db_model import Base

class User(Base):
    __tablename__ = 'users' # keyword

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    username = Column(String(255), nullable=False, index=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    password = Column(String(255), nullable=False)
    type = Column(String(255), index=True)
    role = Column(String(255), index=True)
    profile_picture_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'To' Relationships
    student = orm.relationship("Student", back_populates="user")
    sessions = orm.relationship("Session", back_populates="user")
    instructed_classes = orm.relationship("Class", back_populates="instructor")
    reservations = orm.relationship("Reservation", back_populates="user", foreign_keys="Reservation.user_id")
    reservations_checked_by = orm.relationship("Reservation", back_populates="admin", foreign_keys="Reservation.admin_id")
    groups = orm.relationship("GroupUser", back_populates="user")

UserKeyEnum = Enum('UserKeyEnum', {
    column.upper(): column for column in User.__table__.columns.keys()
}, type=str)

UserKeyTypes = {
    column.value: User.__table__.columns[column].type.python_type for column in UserKeyEnum
}