# -*- coding: utf-8 -*-
"""Unit test submission_moderator get_submission
"""
from typing import Dict

import praw
import pytest

from submission_moderator import get_submission

# TODO: consider refactoring get_submission such that tests don't depend on a
# live praw.Reddit instance


@pytest.mark.parametrize("submission_id", ["euot0h"])
def test_get_submission(bob, submission_id):
    """Unit test expected behavior of get_submission
    """
    result = get_submission(submission_id, bob)

    assert isinstance(result, praw.models.Submission)
    # only ever test with datascience-bot
    assert result._reddit.user.me() == "datascience-bot"


@pytest.mark.parametrize("submission_id", [1, 4e-96, ("what", "a", "tuple")])
def test_get_submission_501(bob, submission_id):
    """Unit test unexpected usage of get_submission
    """
    with pytest.raises(NotImplementedError):
        result = get_submission(submission_id, bob)
