# -*- coding: utf-8 -*-
"""Test authpraw.py module
"""
from datascience_bot.authpraw import get_datascience_bot


def test__get_datascience_bot():
    bob = get_datascience_bot()
    assert bob.user.me() == 'datascience-bot'


