# -*- coding: utf-8 -*-
"""Unit Test SubmissionClassifier
"""
import unittest

from submission_moderator import SubmissionClassifier
from BaseTestCase import BaseTestCase


class SubmissionClassifierTest(BaseTestCase):
    """Unit test expected behavior of SubmissionClassifier
    """

    def setUp(self):
        super().setUp()
        self.classifier = SubmissionClassifier()

    def tearDown(self):
        super().setUp()
        del self.classifier

    def test_classify_blog(self):
        """Unit test expected behavior of SubmissionClassifier.classify
        """
        self.submission.url = "https://medium.com/asdfasdf"
        self.classifier.classify(self.submission)

        assert self.classifier.is_porn is False
        assert self.classifier.is_video is False
        assert self.classifier.is_blog is True

    def test_classify_porn(self):
        """Unit test expected behavior of SubmissionClassifier.classify
        """
        self.submission.url = "https://pornhub.com/asdf"
        self.classifier.classify(self.submission)

        assert self.classifier.is_porn is True
        assert self.classifier.is_video is False
        assert self.classifier.is_blog is False

    def test_classify_video(self):
        """Unit test expected behavior of SubmissionClassifier.classify
        """
        self.submission.url = "https://www.youtube.com/watch?v=-qstIEHDVRg"
        self.classifier.classify(self.submission)

        assert self.classifier.is_porn is False
        assert self.classifier.is_video is True
        assert self.classifier.is_blog is False


if __name__ == "__main__":
    unittest.main()
