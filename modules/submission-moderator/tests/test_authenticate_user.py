# -*- coding: utf-8 -*-
"""Test authenticate_user.py module
"""
from submission_moderator.authenticate_user import get_datascience_bot


def test__get_datascience_bot():
    bob = get_datascience_bot()
    bob.user.me()


if __name__ == "__main__":
    bob = get_datascience_bot()
    print(bob.user.me())
