#!/usr/bin/env python3
"""SQLAlchemy model named User for a database table named users
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """User model for a database table users.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """Returns a string representation of the User object.
        """
        return (
    "<user(email='%s', hashed_password='%s', session_id='%s', reset_token='%s')>" 
    % (self.email, self.hashed_password, self.session_id, self.reset)
    )
