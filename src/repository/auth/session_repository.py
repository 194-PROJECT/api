from typing import Optional
from database.model.session import Session
from database.postgres.query import QueryExecutor
from sqlalchemy import insert, select
from sqlalchemy.dialects import postgresql

from src.dto.auth.session_dto import Session as SessionDTO

class SessionRepository:
    @staticmethod
    def create_session(user_id: int, token: str, expires_at) -> SessionDTO:
        query = (
            insert(Session)
            .values(user_id=user_id, token=token, expires_at=expires_at)
            .returning("*")
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        data = QueryExecutor.insert_one(str(query))
        return SessionDTO(**data) if data else None
    
    @staticmethod
    def get_session(user_id: int, token: str) -> Optional[SessionDTO]:
        query = (
            select(Session)
            .where(Session.user_id == user_id)
            .where(Session.token == token)
            .compile(
                compile_kwargs={"literal_binds": True},
                dialect=postgresql.dialect(),
            )
        )
        
        data = QueryExecutor.fetch_one(str(query))
        return SessionDTO(**data) if data else None