# -*- coding: utf-8 -*-
"""Test authpraw.py module
"""
import pytest

from authpraw import get_datascience_bot, get_substantial_strain6, get_b3405920


@pytest.mark.parametrize(
    "func,user_name",
    [
        (get_datascience_bot, "datascience-bot"),
        (get_substantial_strain6, "SubstantialStrain6"),
        (get_b3405920, "b3405920"),
    ],
)
def test__get_redditor(func, user_name):
    redditor = func()
    assert redditor.user.me() == user_name
