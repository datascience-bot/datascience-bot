# -*- coding: utf-8 -*-
"""Test expected behavior of monitors
"""
import abc
from typing import Type
import unittest

import praw

from authpraw import get_datascience_bot
from monitor import CommentMonitor, SubmissionMonitor


class BaseTestCase(abc.ABC):
    # TODO: How to type hint monitor_constructor?
    # This isn't quite right: Union[Type[CommentMonitor], Type[SubmissionMonitor]]
    @abc.abstractmethod
    def setUp(self, monitor_constructor):
        self.monitor = monitor_constructor(get_datascience_bot())

    def tearDown(self):
        del self.monitor

    @abc.abstractmethod
    def test_stream(self, assert_type: Type):
        for i, obj in enumerate(self.monitor.stream()):
            break
        self.assertIsInstance(obj, assert_type)


class TestCommentMonitor(BaseTestCase, unittest.TestCase):
    def setUp(self):
        super().setUp(CommentMonitor)

    def test_stream(self):
        super().test_stream(assert_type=praw.models.Comment)


class TestSubmissionMonitor(BaseTestCase, unittest.TestCase):
    def setUp(self):
        super().setUp(SubmissionMonitor)

    def test_stream(self):
        super().test_stream(assert_type=praw.models.Submission)

    def test_new(self):
        for i, obj in enumerate(self.monitor.new(limit=1)):
            break
        self.assertIsInstance(obj, praw.models.Submission)


if __name__ == "__main__":
    unittest.main()
