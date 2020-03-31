# -*- coding: utf-8 -*-
"""Unit Test SubmissionClassifier
"""
import unittest

from libs.shared.pram import BaseTestCase
from libs.submission_moderator_app.submission_moderator import SubmissionClassifier


class SubmissionClassifierTest(BaseTestCase):
    """Unit test expected behavior of SubmissionClassifier
    """

    def setUp(self):
        super().setUp()
        self.classifier = SubmissionClassifier()

    def tearDown(self):
        super().tearDown()
        del self.classifier

    def test_classify_blog(self):
        """Unit test expected behavior of SubmissionClassifier.classify
        """
        self.submission.domain = "medium.com"
        self.classifier.classify(self.submission)

        assert self.classifier.is_blog is True
        assert self.classifier.is_porn is False
        assert self.classifier.is_video is False
        assert self.classifier.is_troll is False

    def test_classify_porn(self):
        """Unit test expected behavior of SubmissionClassifier.classify
        """
        self.submission.domain = "pornhub.com"
        self.classifier.classify(self.submission)

        assert self.classifier.is_blog is False
        assert self.classifier.is_porn is True
        assert self.classifier.is_troll is False
        assert self.classifier.is_video is False

    def test_classify_troll(self):
        """Unit test expected behavior of SubmissionClassifier.classify
        """
        self.submission.author.comment_karma = 0
        self.submission.author.link_karma = 0
        self.classifier.classify(self.submission)

        assert self.classifier.is_blog is False
        assert self.classifier.is_troll is True
        assert self.classifier.is_porn is False
        assert self.classifier.is_video is False

    def test_classify_video(self):
        """Unit test expected behavior of SubmissionClassifier.classify
        """
        self.submission.domain = "youtube.com"
        self.classifier.classify(self.submission)

        assert self.classifier.is_blog is False
        assert self.classifier.is_porn is False
        assert self.classifier.is_troll is False
        assert self.classifier.is_video is True

    def test_reusability(self):
        """Unit test expected behavior when class is reused to classify
        multiple submissions
        """
        self.test_classify_blog()
        self.test_classify_porn()
        self.test_classify_video()


if __name__ == "__main__":
    unittest.main()
