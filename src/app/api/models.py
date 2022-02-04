from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db import Base


<<<<<<< HEAD
=======

>>>>>>> 881b1c7fc90a1e2862617ccbb668e8de3b115157
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(256))
    created_date = Column(DateTime, default=func.now(), nullable=False)


    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password


class UserSchema(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=256)

class UserDB(UserSchema):
    id: int

    class Config:
        orm_mode = True
