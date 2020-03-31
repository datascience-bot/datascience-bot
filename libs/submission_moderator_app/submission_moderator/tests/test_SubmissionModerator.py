# -*- coding: utf-8 -*-
"""Unit Test SubmissionModerator
"""
import unittest

from libs.shared.pram import BaseTestCase
from libs.submission_moderator_app.submission_moderator import SubmissionModerator


class SubmissionModeratorTest(BaseTestCase):
    """Unit test expected behavior of SubmissionModerator
    """

    def setUp(self):
        super().setUp()
        self.moderator = SubmissionModerator(self.redditor)

    def tearDown(self):
        super().setUp()
        del self.moderator

    def test_approves_submissions(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which don't break the rules
        """
        self.assertFalse(self.submission.approved is True)
        self.assertTrue(len(self.submission.domain) > 0)

        self.moderator.moderate(self.submission)

        self.submission.mod.approve.assert_called_once()
        self.assertTrue(self.submission.mod.remove.called == 0)
        self.assertTrue(self.submission.reply.called == 0)

    def test_ignores_approved(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which have already been approved
        """
        self.submission.approved = True
        self.moderator.moderate(self.submission)

        # don't classify anything if the post has been approved
        self.assertTrue(self.submission.mod.approve.called == 0)
        self.assertTrue(self.submission.mod.remove.called == 0)
        self.assertTrue(self.submission.reply.called == 0)

    def test_moderates_porn(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which link to banned porn domains
        """
        self.submission.domain = "pornhub.com"
        self.moderator.moderate(self.submission)

        self.assertTrue(self.submission.mod.approve.called == 0)
        self.submission.mod.remove.assert_called_once_with(spam=True),
        self.assertTrue(self.submission.reply.called == 0)

    def test_moderates_videos(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which link to banned video hosting domains
        """
        self.submission.domain = "youtube.com"
        self.moderator.moderate(self.submission)

        self.assertTrue(self.submission.mod.approve.called == 0)
        self.submission.mod.remove.assert_called_once_with(spam=True),
        self.submission.reply.assert_called_once()

    def test_moderates_blogs(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions which link to banned blog aggregator domains
        """
        self.submission.domain = "medium.com"
        self.moderator.moderate(self.submission)

        self.assertTrue(self.submission.mod.approve.called == 0)
        self.submission.mod.remove.assert_called_once_with(spam=True)
        self.submission.reply.assert_called_once()

    def test_moderates_trolls(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions by trolls or new redditors
        """
        self.submission.author.comment_karma = 10
        self.submission.author.link_karma = 10
        self.moderator.moderate(self.submission)

        self.assertTrue(self.submission.mod.approve.called == 0)
        self.submission.mod.remove.assert_called_once()
        self.submission.reply.assert_called_once()


if __name__ == "__main__":
    unittest.main()
