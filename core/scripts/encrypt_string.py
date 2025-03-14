from core.auth_helper import encrypt

def execute(data: str) -> str:
    print(encrypt(data))