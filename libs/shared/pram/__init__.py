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
        self.comment = mock_comment()
        self.redditor = mock_redditor()
        self.submission = mock_submission()
        self.subreddit = mock_subreddit()

    def tearDown(self):
        del self.comment
        del self.redditor
        del self.submission
        del self.subreddit


def mock_comment() -> Union[Mock, praw.models.Comment]:
    comment = create_autospec(praw.models.Comment)
    comment.author = mock_redditor()

    comment.approved = False
    comment.body = "This comment has body"
    comment.mod = create_autospec(praw.models.reddit.comment.CommentModeration)
    comment.stickied = False
    comment.subreddit = mock_subreddit()

    return comment


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
    submission.stickied = False
    submission.title = "This title is thebomb.com"

    return submission


def mock_subreddit() -> Union[Mock, praw.models.Subreddit]:
    subreddit = create_autospec(praw.models.Subreddit)
    subreddit.display_name = "mock_subreddit"

    return subreddit
