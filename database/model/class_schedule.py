from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Time,sql, orm
from core.db_model import Base
from database.model.classes import Class

class ClassSchedule(Base):
    __tablename__ = 'class_schedule'

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False, index=True)
    day = Column(String(10), nullable=False, index=True)
    start_time = Column(Time(timezone=True), nullable=False, index=True)
    end_time = Column(Time(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=sql.func.now())
    # 'From' Relationships
    class_ = orm.relationship(Class, back_populates="class_schedules", foreign_keys=[class_id])

ClassScheduleKeyEnum = Enum('ClassScheduleKeyEnum', {
    column.capitalize(): column for column in ClassSchedule.__table__.columns.keys()
}, type=str)

ClassScheduleKeyTypes = {
    column.value: ClassSchedule.__table__.columns[column].type.python_type for column in ClassScheduleKeyEnum
}
