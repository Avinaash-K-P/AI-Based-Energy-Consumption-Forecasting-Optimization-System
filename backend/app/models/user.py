from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)

    username = Column(String(50),nullable=False, unique=True)

    email = Column(String(50), nullable=False, unique=True)

    password = Column(String(255), nullable=False)
