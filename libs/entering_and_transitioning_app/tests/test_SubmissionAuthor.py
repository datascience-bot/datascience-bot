# -*- coding: utf-8 -*-
"""Test simple questions thread author

Notes:
    1. We're a bit more strict with this test case.
       Consistency is important for the weekly thread, and
       formatting and patterns should not change easily.

    2. There's lot's of implementation details here.
       we can't depend on praw's model-view-controller pattern
       because we aren't testing live praw objects;
       i.e. the model can't update the view because the controller isn't connected.
"""
from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock

import praw

from libs.shared.pram import BaseTestCase, mock_submission, mock_subreddit
from libs.entering_and_transitioning_app import (
    SubmissionAuthor,
    InvalidConditionError,
    validate_time,
    validate_unique_thread,
)


class TestAuthor(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.datefmt = "%Y-%m-%d"
        cls.monday_time = datetime.strptime("2019-07-01", cls.datefmt)
        cls.sunday_time = datetime.strptime("2019-07-07", cls.datefmt)

    def setUp(self):
        super().setUp()
        self.author = SubmissionAuthor(self.subreddit)

    def test_title_prefix(self):
        self.assertIsInstance(self.author.title_prefix, str)
        self.assertTrue(self.author.title_prefix != "")

    def test_datefmt(self):
        self.assertIsInstance(self.author.datefmt, str)
        self.assertTrue(self.author.datefmt != "")

    def test_title_format(self):
        # replicating implementation logic a bit to get the right date formats
        actual_title = self.author.get_title(time=self.sunday_time)
        start_time = self.sunday_time.strftime(self.author.datefmt)
        end_time = (self.sunday_time + timedelta(days=7)).strftime(self.author.datefmt)

        expected_title = (
            f"Weekly Entering & Transitioning Thread | {start_time} - {end_time}"
        )

        self.assertTrue(actual_title == expected_title)

    def test_selftext_source(self):
        with open("libs/entering_and_transitioning_app/data/selftext.md", "r") as ifile:
            expected_selftext = ifile.read()
        actual_selftext = self.author.get_selftext()

        self.assertTrue(expected_selftext == actual_selftext)

    def test_weekly_thread_attributes(self):
        # TODO: Refactor. This test relies too heavily on implementation details
        self.subreddit.submit.return_value = mock_submission()

        submission = self.author.submit_thread(self.sunday_time)

        self.assertIsInstance(submission, praw.models.Submission)
        submission.mod.flair.assert_called_once_with(text="Discussion")
        submission.mod.approve.assert_called_once()
        submission.mod.distinguish.assert_called_once()
        submission.mod.sticky.assert_called_once_with(state=True, bottom=True)
        submission.mod.suggested_sort.assert_called_once_with(sort="new")

    def test_get_last_thread(self):
        last_thread = self.submission
        last_thread.author = "datascience-bot"
        last_thread.created_utc = self.sunday_time
        last_thread.title = self.author.get_title(self.sunday_time)
        last_thread.stickied = True

        subreddit = mock_subreddit()
        subreddit.hot.return_value = (mock_submission(), last_thread)

        submission = self.author.get_last_thread(subreddit=subreddit)

        self.assertIsInstance(submission, praw.models.Submission)


if __name__ == "__main__":
    unittest.main()
