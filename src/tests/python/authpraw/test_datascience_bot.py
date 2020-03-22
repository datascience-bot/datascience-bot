# -*- coding: utf-8 -*-
"""Test authpraw.py module
"""
import pytest

from authpraw import get_datascience_bot


def test__get_redditor():
    redditor = get_datascience_bot()
    assert redditor.user.me() == "datascience-bot"
