# -*- coding: utf-8 -*-
"""Test the classify_karma.py module
"""
import pytest

from datascience_bot.submission_moderator.karma_classifier import classify_karma


@pytest.mark.parametrize(
    "total_karma,label",
    (
        (-1240, "troll"),
        (-10, "troll"),
        (-9, "new user"),
        (1, "new user"),
        (49, "new user"),
        (50, None),
        (74890, None),
    ),
)
def test__classify_karma(total_karma, label):
    result = classify_karma(total_karma)

    assert isinstance(result, type(label))

    if isinstance(result, str):
        assert result == label
