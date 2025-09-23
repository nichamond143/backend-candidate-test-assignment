from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.core import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(name='{self.name}', email={self.email})>"