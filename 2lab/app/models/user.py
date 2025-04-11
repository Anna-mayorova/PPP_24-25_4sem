from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base  # Импорт из db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'user_entities'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_secret = Column(String(255))
    is_active = Column(Boolean, default=True)

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_secret)

    def generate_hash(self, password: str):
        return pwd_context.hash(password)