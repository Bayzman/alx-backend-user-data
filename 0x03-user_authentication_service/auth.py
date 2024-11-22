#!/usr/bin/env python3

""" Hash Password """

import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ Hash password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generate UUID """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Constructor of the class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register user """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Valid login """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ Create session """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Get user from session ID """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy session """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Get reset password token """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, reset_token=session_id)
            return session_id
        except Exception:
            return ValueError

    def update_password(self, reset_token: str, new_password: str) -> None:
        """ Update password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(new_password),
                                 reset_token=None)
        except Exception:
            raise ValueError
