from enum import Enum
from sqlalchemy import Column, DateTime, Integer, String, sql, orm
from core.db_model import Base

class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'To' Relationships
    programs = orm.relationship("Program", back_populates="department")

DepartmentKeyEnum = Enum('DepartmentKeyEnum', {
    column.capitalize(): column for column in Department.__table__.columns.keys()
}, type=str)

DepartmentKeyTypes = {
    column.value: Department.__table__.columns[column].type.python_type for column in DepartmentKeyEnum
}
