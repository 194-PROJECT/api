from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, sql, orm
from core.db_model import Base
from database.model.classes import Class

class Group(Base):
    __tablename__ = 'groups' # keyword
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now(), index=True)
    # 'From' Relationships
    class_ = orm.relationship(Class, back_populates="groups")
    # 'To' Relationships
    reservations = orm.relationship("Reservation", back_populates="group")
    users = orm.relationship("GroupUser", back_populates="group")

GroupKeyEnum = Enum('GroupKeyEnum', {
    column.capitalize(): column for column in Group.__table__.columns.keys()
}, type=str)

GroupKeyTypes = {
    column.value: Group.__table__.columns[column].type.python_type for column in GroupKeyEnum
}