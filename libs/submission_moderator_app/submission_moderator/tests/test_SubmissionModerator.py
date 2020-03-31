# -*- coding: utf-8 -*-
"""Unit Test SubmissionModerator
"""
import unittest

from libs.shared.pram import BaseTestCase
from libs.submission_moderator_app.submission_moderator import SubmissionModerator


class SubmissionModeratorTest(BaseTestCase):
    """Unit test expected behavior of SubmissionModerator
    """

    def assertReplyAndRemove(self):
        self.assertTrue(self.submission.mod.approve.called == 0)
        self.assertTrue(self.submission.mod.remove.called == 1)
        self.assertTrue(self.submission.reply.called == 1)

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

        self.assertTrue(self.submission.mod.approve.called == 1)
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

    def test_moderates_banned_link_submissions(self):
        for domain in ("medium.com", "youtube.com", "pornhub.com"):
            self.submission.domain = domain
            self.moderator.moderate(self.submission)

            self.assertReplyAndRemove()

    def test_moderates_trolls(self):
        """Unit test expected behavior of SubmissionModerator.moderate
        on submissions by trolls or new redditors
        """
        self.submission.author.comment_karma = 10
        self.submission.author.link_karma = 10
        self.moderator.moderate(self.submission)

        self.assertReplyAndRemove()

    def test_multiple_removal_reasons(self):
        self.submission.author.comment_karma = 10
        self.submission.author.link_karma = 10
        self.submission.domain = "medium.com"

        self.moderator.moderate(self.submission)

        self.assertReplyAndRemove()
        self.assertTrue(len(self.moderator.removal_reasons) == 2)


if __name__ == "__main__":
    unittest.main()
