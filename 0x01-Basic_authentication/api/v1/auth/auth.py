#!/usr/bin/env python3

""" Module of Auth views """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth """
        if path is None:
            return True

        if not excluded_paths:
            return True
        
        if path[-1] != '/':
            path += '/'
        
        for p in excluded_paths:
            if p[-1] != '/':
                p += '/'
            if path == p:
                return False

        return True


    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user """
        return None
