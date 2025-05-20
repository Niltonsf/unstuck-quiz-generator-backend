from cryptography.fernet import Fernet
from app.config import SECRET_ENCRYPTION_KEY

fernet = Fernet(SECRET_ENCRYPTION_KEY.encode())

def encrypt_answer(answer: str) -> str:
    return fernet.encrypt(answer.encode()).decode()

def decrypt_answer(encrypted_answer: str) -> str:
    return fernet.decrypt(encrypted_answer.encode()).decode()