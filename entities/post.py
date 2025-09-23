from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.core import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String(), nullable=False)

    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(description='{self.description}')>"