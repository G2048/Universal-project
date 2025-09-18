from passlib.context import CryptContext


class PasswordHasher:
    __slots__ = ()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str | bytes, hashed_password: str | bytes):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str | bytes):
        return cls.pwd_context.hash(password)
