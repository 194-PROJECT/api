from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, orm, sql
from core.db_model import Base
from database.model.users import User

class Session(Base):
    __tablename__ = 'session'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), index=True)
    last_active_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    is_active = Column(Boolean, server_default='1')
    device_id = Column(String(255))
    location = Column(String(255))
    # 'From' Relationships
    user = orm.relationship(User, back_populates="sessions", foreign_keys=[user_id])
    
SessionKeyEnum = Enum('SessionKeyEnum', {
    column.capitalize(): column for column in Session.__table__.columns.keys()
}, type=str)

SessionKeyTypes = {
    column.value: Session.__table__.columns[column].type.python_type for column in SessionKeyEnum
}