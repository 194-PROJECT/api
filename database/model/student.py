from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, orm, sql
from core.db_model import Base
from database.model.program import Program
from database.model.users import User

class Student(Base):
    __tablename__ = 'student'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    program_id = Column(Integer, ForeignKey('program.id'), nullable=False, index=True)
    student_id = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now())
    # 'From' Relationships
    program = orm.relationship(Program, back_populates="students", foreign_keys=[program_id])
    user = orm.relationship(User, back_populates="student", foreign_keys=[user_id])

StudentKeyEnum = Enum('StudentKeyEnum', {
    column.capitalize(): column for column in Student.__table__.columns.keys()
}, type=str)

StudentKeyTypes = {
    column.value: Student.__table__.columns[column].type.python_type for column in StudentKeyEnum
}