from core.auth_helper import decrypt

def execute(data: str) -> str:
    print(decrypt(data))