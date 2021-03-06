# -*- coding: utf-8 -*-
"""Test behavior of top level functions in testcases module
"""
import unittest
from unittest.mock import Mock

import praw

from libs.shared.pram import (
    mock_comment,
    mock_redditor,
    mock_submission,
    mock_subreddit,
)


class TestTopLevelFunctions(unittest.TestCase):
    def assertIsMock(self, obj):
        self.assertIsInstance(obj, Mock)

    def test_mock_comment(self):
        comment = mock_comment()

        self.assertIsMock(comment)
        self.assertIsInstance(comment, praw.models.Comment)

        self.test_mock_redditor(comment.author)

        self.assertIsInstance(comment.approved, bool)

        self.assertIsInstance(comment.mod, praw.models.reddit.comment.CommentModeration)

        self.assertIsInstance(comment.body, str)
        self.assertTrue(comment.body != "")

        self.assertIsInstance(comment.stickied, bool)
        self.assertTrue(comment.stickied is False)

        self.test_mock_subreddit(comment.subreddit)

    def test_mock_redditor(self, redditor=None):
        if redditor is None:
            redditor = mock_redditor()

        self.assertIsMock(redditor)
        self.assertIsInstance(redditor, praw.models.Redditor)

        self.assertIsInstance(redditor.name, str)
        self.assertTrue(redditor.name != "")

        self.assertIsInstance(redditor.comment_karma, int)
        self.assertIsInstance(redditor.link_karma, int)

    def test_mock_submission(self):
        submission = mock_submission()

        self.assertIsMock(submission)
        self.assertIsInstance(submission, praw.models.Submission)

        self.test_mock_redditor(submission.author)

        self.assertIsInstance(submission.approved, bool)

        self.assertIsInstance(
            submission.mod, praw.models.reddit.submission.SubmissionModeration
        )

        self.assertIsInstance(submission.title, str)
        self.assertTrue(submission.title != "")

        self.assertIsInstance(submission.domain, str)
        self.assertTrue(submission.domain != "")

        self.assertIsInstance(submission.stickied, bool)
        self.assertTrue(submission.stickied is False)

        self.test_mock_subreddit(submission.subreddit)

    def test_mock_subreddit(self, subreddit=None):
        if subreddit is None:
            subreddit = mock_subreddit()

        self.assertIsMock(subreddit)
        self.assertIsInstance(subreddit, praw.models.Subreddit)

        self.assertIsInstance(subreddit.display_name, str)


if __name__ == "__main__":
    unittest.main()
