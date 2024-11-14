#!/usr/bin/env python3

""" Basic authentication module """

from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """ Basic authentication class """
    def __init__(self):
        """ Constructor of the class """
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str):
        """ Base64 authorization header """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str):
        """ Decode base64 authorization header """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            return str(b64decode(base64_authorization_header), "utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header):
        """ Extract user credentials """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        return decoded_base64_authorization_header.split(":")[0], \
            decoded_base64_authorization_header.split(":")[1]
