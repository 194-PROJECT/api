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

    @staticmethod
    def get_semester_count(where_clause: Optional[str]) -> int:
        return SemesterRepository.get_semester_count(where_clause)

    @staticmethod
    def update_semester(id: int, semester: SemesterDTO) -> Optional[SemesterDTO]:
        return SemesterRepository.update_semester(id, semester)

    @staticmethod
    def delete_semester(id: int) -> None:
        SemesterRepository.delete_semester(id)

    @staticmethod
    def delete_semesters_by_id(ids: list[int]) -> None:
        SemesterRepository.delete_semesters_by_id(ids)
