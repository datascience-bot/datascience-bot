# -*- coding: utf-8 -*-
"""Unit Test SubmissionArbiter
"""
import unittest

from libs.shared.pram import BaseTestCase
from libs.submission_moderator_app.submission_arbiter import SubmissionArbiter
from libs.submission_moderator_app.submission_classifier import SubmissionClassifier


class TestSubmissionArbiter(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.classifier = SubmissionClassifier()
        self.classifier.classify(self.submission)
        self.arbiter = SubmissionArbiter(self.classifier)

    def tearDown(self):
        super().tearDown()
        del self.arbiter

    def test_removal_reasons_getter(self):
        self.assertIsInstance(self.arbiter.removal_reasons, list)

    def test_judge_blog(self):
        self.arbiter.classifier.is_blog = True
        self.arbiter.judge_blog()

        self.assertTrue(len(self.arbiter.removal_reasons) == 1)

    def test_judge_porn(self):
        self.arbiter.classifier.is_porn = True
        self.arbiter.judge_porn()

        self.assertTrue(len(self.arbiter.removal_reasons) == 1)

    def test_judge_troll(self):
        self.arbiter.classifier.submission.author.comment_karma = 10
        self.arbiter.classifier.submission.author.link_karma = 10
        self.arbiter.classifier.is_troll = True
        self.arbiter.judge_troll()

        self.assertTrue(len(self.arbiter.removal_reasons) == 1)

    def test_judge_video(self):
        self.arbiter.classifier.is_video = True
        self.arbiter.judge_video()

        self.assertTrue(len(self.arbiter.removal_reasons) == 1)

    def test_judge_multiple_removal_reasons(self):
        self.arbiter.classifier.is_blog = True
        self.arbiter.classifier.is_troll = True
        self.arbiter.judge()

        self.assertTrue(len(self.arbiter.removal_reasons) == 2)

    def test_get_verdict(self):
        verdict = self.arbiter.get_verdict()
        self.assertIsInstance(verdict, str)

    def test_empty_verdict_if_innocent(self):
        verdict = self.arbiter.get_verdict()
        self.assertTrue(verdict == "")


if __name__ == "__main__":
    unittest.main()
