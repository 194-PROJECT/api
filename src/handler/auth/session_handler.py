import secrets
from src.dto.auth.session_dto import Session
from src.repository.auth.session_repository import SessionRepository
from datetime import datetime, timedelta

class SessionHandler:
    __TOKEN_LENGTH = 36
    __EXPIRATION_TIME = 3600
    
    @staticmethod
    def create_session(user_id: int, expire_duration: int = __EXPIRATION_TIME) -> Session:
        token = SessionHandler.__generate_token()
        expiration_time = datetime.now() + timedelta(seconds=expire_duration)
        return SessionRepository.create_session(user_id, token, expiration_time)
    
    @staticmethod
    def get_session(user_id: int, token: str) -> Session:
        return SessionRepository.get_session(user_id, token)
    
    @staticmethod
    def verify_session(user_id: int, token: str) -> bool:
        session = SessionHandler.get_session(user_id, token)
        return session and session.expires_at > datetime.now()
    
    @staticmethod
    def __generate_token() -> str:
        return secrets.token_hex(SessionHandler.__TOKEN_LENGTH)


def authenticated(func):
    """_summary_

    Args:
        func (_type_): _description_
    """
    def wrapper(user_id, token, role, *args, **kwargs):
        if not SessionHandler.verify_session(user_id, token):
            raise PermissionError("Invalid or expired session.")
        return func(user_id, token, *args, **kwargs)
    return wrapper