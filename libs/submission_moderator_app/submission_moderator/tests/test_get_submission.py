# -*- coding: utf-8 -*-
"""Unit test submission_moderator.get_submission
"""
from typing import Dict
import unittest

import praw

from authpraw import get_datascience_bot
from submission_moderator import get_submission

# TODO: consider refactoring get_submission such that tests don't depend on a
# live praw.Reddit instance


class GetSubmissionTest(unittest.TestCase):
    """Unit test expected behavior of get_submission
    """

    def setUp(self):
        self.datascience_bot = get_datascience_bot()

    def tearDown(self):
        del self.datascience_bot

    def test_get_submission(self):
        """Unit test expected behavior of get_submission
        """
        result = get_submission(submission_id="euot0h", redditor=self.datascience_bot)

        assert isinstance(result, praw.models.Submission)
        # only ever test with datascience-bot
        assert result._reddit.user.me() == "datascience-bot"

    def test_get_submission_501(self):
        """Unit test unexpected usage of get_submission
        """
        with self.assertRaises(NotImplementedError):
            result = get_submission(4e-96, self.datascience_bot)


if __name__ == "__main__":
    unittest.main()
