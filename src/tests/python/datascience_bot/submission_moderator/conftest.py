# -*- coding: utf-8 -*-
"""Test fixtures for moderate_submissions module
"""
from unittest.mock import create_autospec, Mock

import praw
import pytest

from datascience_bot.authpraw import get_datascience_bot

@pytest.fixture
def bob():
    return get_datascience_bot()

@pytest.fixture
def redditor():
    user = create_autospec(praw.models.Redditor)
    user.name = "not-a-real-user"

    return user


@pytest.fixture
def submission(redditor):
    submission = create_autospec(praw.models.Submission)
    submission.approved_by = None
    submission.author = redditor
    submission.mod = create_autospec(praw.models.reddit.submission.SubmissionModeration)
    submission.subreddit = create_autospec(praw.models.Subreddit)
    submission.subreddit.display_name = "not-a-real-subreddit"
    submission.url = ""

    return submission
