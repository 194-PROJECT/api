from enum import Enum
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey, orm, sql
from core.db_model import Base
from database.model.department import Department

# NOTE: Previously, I used the following code to back reference a table. 
# This was because I did not have to specify the relationship defined in the Department class. 
# However, this approach was a bit confusing.
#
# Old: orm.relationship(Department, backref=orm.backref('program_department', lazy='dynamic'), foreign_keys=[department_id])
# New: orm.relationship(Department, back_populates="programs", foreign_keys=[department_id])

class Program(Base):
    __tablename__ = 'program'

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    credits_required = Column(Integer)
    duration = Column(Float)  # duration in years
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'From' Relationships
    department = orm.relationship(Department, back_populates="programs", foreign_keys=[department_id])
    # 'To' Relationships
    students = orm.relationship("Student", back_populates="program")
    courses = orm.relationship("Course", back_populates="program")

ProgramKeyEnum = Enum('ProgramKeyEnum', {
    column.capitalize(): column for column in Program.__table__.columns.keys()
}, type=str)

ProgramKeyTypes = {
    column.value: Program.__table__.columns[column].type.python_type for column in ProgramKeyEnum
}
