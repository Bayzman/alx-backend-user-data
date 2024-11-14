#!/usr/bin/env python3

""" Basic authentication module """

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class """
    def __init__(self):
        """ Constructor of the class """
        super().__init__()
