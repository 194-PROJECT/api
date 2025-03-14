from typing import Optional
from src.dto.student.student_dto import StudentDTO
from src.repository.student.student_repository import StudentRepository

class StudentHandler:
    @staticmethod
    def create_student(student: StudentDTO) -> Optional[StudentDTO]:
        return StudentRepository.create_student(student)

    @staticmethod
    def get_student(id: int) -> Optional[StudentDTO]:
        return StudentRepository.get_student(id)

    @staticmethod
    def get_students(
        limit: int,
        offset: int,
        order_by_clause: Optional[str] = None,
        where_clause: Optional[str] = None,
    ) -> Optional[list[StudentDTO]]:
        return StudentRepository.get_students(limit, offset, order_by_clause, where_clause)

    @staticmethod
    def update_student(id: int, student: StudentDTO) -> Optional[StudentDTO]:
        return StudentRepository.update_student(id, student)

    @staticmethod
    def delete_student(id: int) -> None:
        StudentRepository.delete_student(id)

    @staticmethod
    def delete_students_by_id(ids: list[int]) -> None:
        StudentRepository.delete_students_by_id(ids)