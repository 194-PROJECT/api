from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, sql, orm
from core.db_model import Base
from database.model.course import Course
from database.model.semester import Semester
from database.model.users import User

class Class(Base):
    __tablename__ = 'classes' # keyword

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('course.id'), index=True)
    instructor_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), index=True)
    semester_id = Column(Integer, ForeignKey('semester.id', ondelete='SET NULL'), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now(), onupdate=sql.func.now())
    # 'From' Relationships
    course = orm.relationship(Course, back_populates="classes", foreign_keys=[course_id])
    instructor = orm.relationship(User, back_populates="instructed_classes", foreign_keys=[instructor_id])
    semester = orm.relationship(Semester, back_populates="classes", foreign_keys=[semester_id])
    # 'To' Relationships
    groups = orm.relationship("Group", back_populates="class_")
    class_schedules = orm.relationship("ClassSchedule", back_populates="class_")

ClassKeyEnum = Enum('ClassKeyEnum', {
    column.capitalize(): column for column in Class.__table__.columns.keys()
}, type=str)

ClassKeyTypes = {
    column.value: Class.__table__.columns[column].type.python_type for column in ClassKeyEnum
}