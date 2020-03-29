# -*- coding: utf-8 -*-
"""Unit Test SubmissionModerator
"""
import unittest

from submission_moderator import SubmissionModerator

from BaseTestCase import BaseTestCase


class SubmissionModeratorTest(BaseTestCase):
    """Unit test expected behavior of SubmissionModerator
    """

    def setUp(self):
        super().setUp()
        self.submission_moderator = SubmissionModerator(self.redditor)

    def tearDown(self):
        super().setUp()
        del self.submission_moderator

    def test_approves_submissions(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which don't break the rules
        """
        self.assertFalse(self.submission.approved is True)
        self.assertTrue(len(self.submission.url) > 0)

        self.submission_moderator.moderate(self.submission)

        self.submission.mod.approve.assert_called_once()
        self.assertTrue(self.submission.mod.remove.called == 0)
        self.assertTrue(self.submission.reply.called == 0)

    def test_ignores_approved(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which have already been approved
        """
        self.submission.approved = True
        self.submission_moderator.moderate(self.submission)

        # don't classify anything if the post has been approved
        self.assertTrue(self.submission.mod.approve.called == 0)
        self.assertTrue(self.submission.mod.remove.called == 0)
        self.assertTrue(self.submission.reply.called == 0)

    def test_moderates_porn(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which link to banned porn domains
        """
        self.submission.url = "http://pornhub.com"
        self.submission_moderator.moderate(self.submission)

        self.assertTrue(self.submission.mod.approve.called == 0)
        self.submission.mod.remove.assert_called_once_with(spam=True),
        self.assertTrue(self.submission.reply.called == 0)

    def test_moderates_videos(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which link to banned video hosting domains
        """
        self.submission.url = "http://youtube.com"
        self.submission_moderator.moderate(self.submission)

        self.assertTrue(self.submission.mod.approve.called == 0)
        self.submission.mod.remove.assert_called_once_with(spam=True),
        self.submission.reply.assert_called_once()

    def test_moderates_blogs(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which link to banned blog aggregator domains
        """
        self.submission.url = "http://medium.com"
        self.submission_moderator.moderate(self.submission)

        self.assertTrue(self.submission.mod.approve.called == 0)
        self.submission.mod.remove.assert_called_once_with(spam=True)
        self.submission.reply.assert_called_once()


if __name__ == "__main__":
    unittest.main()
