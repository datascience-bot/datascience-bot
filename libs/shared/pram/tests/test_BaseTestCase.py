# -*- coding: utf-8 -*-
"""Test testcases.BaseTestCase class
"""
import abc
import unittest

from libs.shared.pram import BaseTestCase


class TestBaseTestCase(BaseTestCase):
    def assertMissingAttributes(self):
        with self.assertRaises(AttributeError):
            self.comment

        with self.assertRaises(AttributeError):
            self.redditor

        with self.assertRaises(AttributeError):
            self.submission

        with self.assertRaises(AttributeError):
            self.subreddit

    def test_is_abc(self):
        self.assertIsInstance(self, abc.ABC)

    def test_is_unittest(self):
        self.assertIsInstance(self, unittest.TestCase)

    def test_mock_comment(self):
        self.comment

    def test_mock_redditor(self):
        self.redditor

    def test_mock_submission(self):
        self.submission

    def test_mock_subreddit(self):
        self.subreddit

    def test_set_up(self):
        test_case = TestBaseTestCase()
        test_case.assertMissingAttributes()

        test_case.setUp()
        try:
            test_case.comment
            test_case.redditor
            test_case.submission
            test_case.subreddit
        except:
            self.fail("Failed to set up required attributes")

    def test_tear_down(self):
        test_case = TestBaseTestCase()
        test_case.setUp()
        test_case.tearDown()
        test_case.assertMissingAttributes()


if __name__ == "__main__":
    unittest.main()
