from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])


def hash_password(plain_password: str) -> str:
    return password_context.hash(plain_password)


def check_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)
