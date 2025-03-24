from typing import List, Optional

from sqlalchemy import TextClause
from src.dto.program.program_dto import ProgramDTO
from src.repository.program.program_repository import ProgramRepository

class ProgramHandler:
    @staticmethod
    def create_program(program_data: dict) -> Optional[ProgramDTO]:
        program = ProgramDTO(**program_data)
        return ProgramRepository.create_program(program)
    
    @staticmethod
    def get_program(id: int) -> Optional[ProgramDTO]:
        return ProgramRepository.get_program(id)
    
    @staticmethod
    def get_programs(
        limit: int,
        offset: int,
        order_by_clause: TextClause,
        where_clause: Optional[TextClause]
    ) -> Optional[list[ProgramDTO]]:
        return ProgramRepository.get_programs(limit, offset, order_by_clause, where_clause)
    
    @staticmethod
    def get_program_count(where_clause: Optional[str]) -> int:
        return ProgramRepository.get_program_count(where_clause)
    
    @staticmethod
    def update_program(id: int, program: ProgramDTO) -> Optional[ProgramDTO]:
        return ProgramRepository.update_program(id, program)
    
    @staticmethod
    def delete_program(id: int) -> None:
        ProgramRepository.delete_program(id)
    
    @staticmethod
    def delete_programs_by_id(ids: List[int]) -> None:
        ProgramRepository.delete_programs_by_id(ids)
