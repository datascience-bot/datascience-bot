# -*- coding: utf-8 -*-
"""Test authpraw.py module
"""
import pytest

from authpraw import get_datascience_bot


@pytest.mark.parametrize("func,user_name", [(get_datascience_bot, "datascience-bot")])
def test__get_redditor(func, user_name):
    redditor = func()
    assert redditor.user.me() == user_name
