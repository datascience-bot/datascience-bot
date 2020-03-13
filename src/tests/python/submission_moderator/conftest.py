# -*- coding: utf-8 -*-
"""Test fixtures for moderate_submissions module
"""
from typing import Dict
from unittest.mock import create_autospec, Mock

import praw
import pytest

from authpraw import get_datascience_bot

# we'll borrow from the implementation for now to ensure full test coverage
from submission_moderator import SubmissionClassifier


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
    submission.approved = False
    submission.approved_by = None
    submission.author = redditor
    submission.mod = create_autospec(praw.models.reddit.submission.SubmissionModeration)
    submission.subreddit = create_autospec(praw.models.Subreddit)
    submission.subreddit.display_name = "not-a-real-subreddit"
    submission.url = ""

    return submission


@pytest.fixture(params=list(SubmissionClassifier.BLOG_DOMAINS))
def blog_submission(submission, request):
    submission.url = request.param
    return submission


@pytest.fixture(params=list(SubmissionClassifier.VIDEO_DOMAINS))
def video_submission(submission, request):
    submission.url = request.param
    return submission


@pytest.fixture(params=list(SubmissionClassifier.PORN_DOMAINS))
def porn_submission(submission, request):
    submission.url = request.param
    return submission

