from enum import Enum
from sqlalchemy import Column, DateTime, Integer, String, Date, sql, orm
from core.db_model import Base

class Semester(Base):
    __tablename__ = 'semester'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now())
    # 'To' Relationships
    classes = orm.relationship("Class", back_populates="semester")

SemesterKeyEnum = Enum('SemesterKeyEnum', {
    column.capitalize(): column for column in Semester.__table__.columns.keys()
}, type=str)

SemesterKeyTypes = {
    column.value: Semester.__table__.columns[column].type.python_type for column in SemesterKeyEnum
}