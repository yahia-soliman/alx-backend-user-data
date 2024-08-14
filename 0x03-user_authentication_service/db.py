#!/usr/bin/env python3
"""DataBase connection Wrapper"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB connection class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create new user and save it to the data base"""
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception:
            self._session.close()
            raise

    def find_user_by(self, **kw) -> User:
        """Retrieve the first user by keyworded arguments

        Returns: User object, if found
        Raises:
            InvalidRequestError: wrong query arguments are passed
            NoResultFound: no user found with the query arguments
        Example:
        >>> user = db.find_user_by(email="test@gg.ez")
        """
        try:
            filters = [getattr(User, k) == v for k, v in kw.items()]
            return self._session.query(User).filter(*filters).one()
        except AttributeError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kw) -> None:
        """Update the user identified by `user_id`

        Raises:
            ValueError: wrong user attribute is passed
            NoResultFound: no user found with the given `user_id`
        Example:
        >>> user = db.update_user(1, email="test@gg.ez")
        """
        user = self.find_user_by(id=user_id)
        for k, v in kw.items():
            if not hasattr(user, k):
                raise ValueError
            setattr(user, k, v)
        self._session.add(user)
        self._session.commit()
