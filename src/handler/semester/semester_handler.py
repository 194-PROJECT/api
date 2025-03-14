from typing import Optional
from src.dto.semester.semester_dto import SemesterDTO
from src.repository.semester.semester_repository import SemesterRepository

class SemesterHandler:
    @staticmethod
    def create_semester(semester: SemesterDTO) -> Optional[SemesterDTO]:
        return SemesterRepository.create_semester(semester)

    @staticmethod
    def get_semester(id: int) -> Optional[SemesterDTO]:
        return SemesterRepository.get_semester(id)

    @staticmethod
    def get_semesters(
        limit: int,
        offset: int,
        order_by_clause: Optional[str] = None,
        where_clause: Optional[str] = None,
    ) -> Optional[list[SemesterDTO]]:
        return SemesterRepository.get_semesters(limit, offset, order_by_clause, where_clause)
