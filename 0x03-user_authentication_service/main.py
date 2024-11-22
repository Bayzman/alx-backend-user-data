#!/usr/bin/env python3

""" Main module """

import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Register user """
    r = requests.post("http://localhost:5000/users",
                      data={"email": email, "password": password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Log in with wrong password """
    r = requests.post("http://localhost:5000/sessions",
                      data={"email": email, "password": password})
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Log in """
    r = requests.post("http://localhost:5000/sessions",
                      data={"email": email, "password": password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    session_id = r.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """ Profile unlogged """
    r = requests.get("http://localhost:5000/profile")
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Profile logged """
    r = requests.get("http://localhost:5000/profile",
                     cookies={"session_id": session_id})
    assert r.status_code == 200
    assert r.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ Log out """
    r = requests.delete("http://localhost:5000/sessions",
                        cookies={"session_id": session_id})
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ Reset password token """
    r = requests.post("http://localhost:5000/reset_password",
                      data={"email": email})
    assert r.status_code == 200
    token = r.json()["reset_token"]
    assert token is not None
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update password """
    r = requests.put("http://localhost:5000/reset_password",
                     data={"email": email, "reset_token": reset_token,
                           "new_password": new_password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
