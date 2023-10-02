from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, DateTime, Float
from sqlalchemy.orm import relationship, Mapped

from database import Base


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(Integer, ForeignKey("users.id"), index=True)
    receiver = Column(Integer, ForeignKey("users.id"), index=True)
    accepted = Column(Boolean, default=False)


class Pin(Base):
    __tablename__ = "pins"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    session_start_time = Column(DateTime(timezone=True), default=func.now())
    session_end_time = Column(DateTime(timezone=True))
    location_long = Column(Float)
    location_lat = Column(Float)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    joiner_list = List[Integer]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    friends = relationship("User",
                           secondary="friends",
                           primaryjoin=id == Friend.sender,
                           secondaryjoin=id == Friend.receiver)
    pin_id = Column(Integer)
    joined_pin_id = Column(Integer)


