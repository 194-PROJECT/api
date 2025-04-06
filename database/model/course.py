from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, sql, orm
from core.db_model import Base
from database.model.program import Program

class Course(Base):
    __tablename__ = 'course'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    program_id = Column(Integer, ForeignKey('program.id'), nullable=False, index=True)
    # prerequisite_id = Column(Integer, ForeignKey('course.id'))
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    credits = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'From' Relationships
    program = orm.relationship(Program, back_populates="courses", foreign_keys=[program_id])
    # prerequisite = orm.relationship("Course", remote_side=[id], backref="dependent_courses")
    # 'To' Relationships
    classes = orm.relationship("Class", back_populates="course")

CourseKeyEnum = Enum('CourseKeyEnum', {
    column.capitalize(): column for column in Course.__table__.columns.keys()
}, type=str)

CourseKeyTypes = {
    column.value: Course.__table__.columns[column].type.python_type for column in CourseKeyEnum
}