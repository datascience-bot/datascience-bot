# -*- coding: utf-8 -*-
"""Base test case - fixtures - for other tests
"""
from abc import ABC
import unittest
from unittest.mock import PropertyMock, create_autospec

import praw


class BaseTestCase(ABC, unittest.TestCase):
    """Base test case with fixtures for all other test cases
    """

    def setUp(self):
        self.redditor = self.get_redditor()
        self.submission = self.get_submission()

    def tearDown(self):
        del self.redditor
        del self.submission

    def get_redditor(self):
        redditor = create_autospec(praw.models.Redditor)
        redditor.name = "not-a-real-user"
        redditor.comment_karma = 100100
        redditor.link_karma = 100100

        return redditor

    def get_submission(self):
        submission = create_autospec(praw.models.Submission)
        submission.approved = False
        submission.approved_by = None
        submission.author = self.redditor
        submission.mod = create_autospec(
            praw.models.reddit.submission.SubmissionModeration
        )
        submission.subreddit = create_autospec(praw.models.Subreddit)
        submission.subreddit.display_name = "not-a-real-subreddit"
        submission.domain = "reddit.com"

        return submission
