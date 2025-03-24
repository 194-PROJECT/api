from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.course.course_dto import CourseDTO
from src.repository.course.course_repository import CourseRepository

class CourseHandler:
    @staticmethod
    def create_course(course: CourseDTO) -> Optional[CourseDTO]:
        return CourseRepository.create_course(course)

    @staticmethod
    def get_course(id: int) -> Optional[CourseDTO]:
        return CourseRepository.get_course(id)

    @staticmethod
    def get_courses(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[list[CourseDTO]]:
        return CourseRepository.get_courses(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def get_course_count(where_clause: Optional[str]) -> int:
        return CourseRepository.get_course_count(where_clause)

    @staticmethod
    def update_course(id: int, course: CourseDTO) -> Optional[CourseDTO]:
        return CourseRepository.update_course(id, course)

    @staticmethod
    def delete_course(id: int) -> None:
        CourseRepository.delete_course(id)

    @staticmethod
    def delete_courses_by_id(ids: List[int]) -> None:
        CourseRepository.delete_courses_by_id(ids)
