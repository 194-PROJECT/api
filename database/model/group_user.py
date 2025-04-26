from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, sql, orm
from core.db_model import Base
from database.model.users import User
from database.model.groups import Group

class GroupUser(Base):
    __tablename__ = 'group_user'
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'From' Relationships
    group = orm.relationship(Group, back_populates='users', foreign_keys=[group_id])
    user = orm.relationship(User, back_populates='groups', foreign_keys=[user_id])

GroupUserKeyEnum = Enum('GroupUserKeyEnum', {
    column.capitalize(): column for column in GroupUser.__table__.columns.keys()
}, type=str)

GroupUserKeyTypes = {
    column.value: GroupUser.__table__.columns[column].type.python_type for column in GroupUserKeyEnum
}
