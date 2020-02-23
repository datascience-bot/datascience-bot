# -*- coding: utf-8 -*-
"""Test authpraw.py module
"""
from datascience_bot.submission_moderator.authpraw import get_datascience_bot


def test__get_datascience_bot():
    bob = get_datascience_bot()
    bob.user.me()


if __name__ == "__main__":
    bob = get_datascience_bot()
    print(bob.user.me())
