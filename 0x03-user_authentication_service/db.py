#!/usr/bin/env python3
"""DB ,module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Any
import bcrypt

from user import Base, User


class DB:
    """Database class that implements add_user method.
    """

    def __init__(self) -> None:
        """Initialize  a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds user and returns a User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs: Any) -> str:
        """Returns the first row found in the users table
        as filtered by the method's input arguments
        
        try:
             Query db using filter_by with ** kwargs
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound()

            return user

        except AttributeError:
             Raised if an invalid field is passed in kwargs
            raise InvalidRequestError()
        """
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """method that updates a user and return None
        """
        try:
            # locate user by id using the find_user_by method
            user = self.find_user_by(id=user_id)

            # iterate thru keyword arguments
            for key, value in kwargs.items():
                # check for user object attribute
                if not hasattr(user, key):
                    raise ValueError()

                # update attribute
                setattr(user, key, value)

            # commit changes to the database
            self._session.commit()

        except NoResultFound:
            raise ValueError()
