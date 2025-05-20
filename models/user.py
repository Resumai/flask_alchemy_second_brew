from db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)


    user_details_link = relationship("UserDetails", back_populates="user_link")