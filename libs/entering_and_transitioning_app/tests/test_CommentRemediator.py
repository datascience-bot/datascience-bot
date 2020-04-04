# -*- coding: utf-8 -*-
"""Test Entering & Transitioning thread comment remediator
"""
import unittest
from unittest.mock import Mock

import praw

from libs.shared.pram import BaseTestCase, mock_comment, mock_submission
from libs.entering_and_transitioning_app import CommentRemediator


class TestCommentRemediator(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.submission.permalink = "reddit.com/not-a-real-link"
        self.remediator = CommentRemediator()

    def test_remediate_unanswered_comments(self):
        self.comment.replies = []
        self.submission.comments = [self.comment]

        self.remediator.remediate_comments(
            on_thread=self.submission, to_thread=self.submission
        )

        self.comment.reply.assert_called_once()

    def test_ignore_answered_comments(self):
        self.comment.replies = Mock(praw.models.comment_forest.CommentForest)
        self.comment.replies.__len__ = Mock(return_value=2)
        self.submission.comments = [self.comment]

        # doesn't matter that we're sending mocks to the same thread
        self.remediator.remediate_comments(
            on_thread=self.submission, to_thread=self.submission
        )

        self.assertTrue(self.comment.reply.called == 0)


if __name__ == "__main__":
    unittest.main()
