# -*- coding: utf-8 -*-
"""Python Reddit API Mocker

You know, instead of Python Reddit API Wrapper?

Mock praw objects and base test cases with mocked praw fixtures
"""
import abc
from typing import Union
import unittest
from unittest.mock import Mock, create_autospec

import praw


class BaseTestCase(abc.ABC, unittest.TestCase):
    def setUp(self):
        self.redditor = mock_redditor()
        self.submission = mock_submission()
        self.subreddit = mock_subreddit()

    def tearDown(self):
        del self.redditor
        del self.submission
        del self.subreddit


def mock_redditor() -> Union[Mock, praw.models.Redditor]:
    redditor = create_autospec(praw.models.Redditor)
    redditor.name = "mock_redditor"
    redditor.comment_karma = 100100
    redditor.link_karma = 100100

    return redditor


def mock_submission() -> Union[Mock, praw.models.Submission]:
    submission = create_autospec(praw.models.Submission)
    submission.author = mock_redditor()

    submission.approved = False
    submission.mod = create_autospec(praw.models.reddit.submission.SubmissionModeration)
    submission.subreddit = mock_subreddit()
    submission.domain = "thebomb.com"

    return submission


def mock_subreddit() -> Union[Mock, praw.models.Subreddit]:
    subreddit = create_autospec(praw.models.Subreddit)
    subreddit.display_name = "mock_subreddit"

    return subreddit
