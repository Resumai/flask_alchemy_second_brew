from db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class UserDetails(db.Model):
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    name = Column(String(80), nullable=False)
    surname = Column(String(80), nullable=False)
    address = Column(String(120), nullable=True)


    user_link = relationship("User", back_populates="user_details_link")
