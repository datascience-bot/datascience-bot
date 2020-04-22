"""Unit test dataset creation

1. Only include submissions from r/datascience
2. Only removed submissions can be labeled True
3. Only approved submissions can be labeled False
4. Novice submissions must have a mod distinguished, stickied comment 
   that matches "I removed your submission" and "Entering (&|and) Transitioning"
5. Dataset columns are
   - id (str): The submission ID
   - title (str)
   - selftext (str)
   - author_name (str)
   - author_link_karma (int)
   - author_comment_karma (int)

TODO: Testing labels (True, False, None) can be improved
    generating possible edge cases for testing is a bit overblown at time of writing
TODO: Harden the rules. We don't follow them strictly right now.
"""
import unittest
from unittest.mock import Mock

import pandas.api.types as ptypes

from libs.shared.authpraw import get_datascience_bot
from libs.shared.pram import BaseTestCase, mock_submission, mock_comment
from libs.shared.models.novice_submission_classifier.dataset import (
    DATASET_SCHEMA,
    label_submission,
    make_dataset,
)


class TestMakeDataset(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bob = get_datascience_bot()
        # note: we aren't guaranteed to get results,
        # but it's more likely the higher the limit is.
        # limit=5 turns out to be a good balance
        cls.dataset = make_dataset(bob, limit=5)

    def test_dataset_schema(self):
        dataset = self.dataset.reset_index()
        for colname, coltype in DATASET_SCHEMA.items():
            result = None
            if issubclass(coltype, (float, int)):
                result = ptypes.is_numeric_dtype(dataset[colname])
            elif issubclass(coltype, str):
                result = ptypes.is_string_dtype(dataset[colname])

            self.assertTrue(result is True)

    def test_handle_moderator_submissions(self):
        submission = mock_submission()
        submission.author.is_mod = True

        result = label_submission(submission)
        self.assertTrue(result is None)

    # some duplicate logic incoming, but necessary to mock praw locally
    def test_label_submission_true(self):
        comment = mock_comment()
        comment.distinguished = "moderator"
        comment.stickied = True
        comment.subreddit.display_name = "datascience"
        comment.body = (
            "I removed your submission. "
            "Please use the weekly entering & transitioning thread.\n\n"
            "Thanks."
        )

        submission = mock_submission()
        submission.author.is_mod = False
        submission.approved = False
        submission.comments = [comment]
        submission.subreddit.display_name = comment.subreddit.display_name

        result = label_submission(submission)
        self.assertTrue(result is True)

    def test_label_submission_false(self):
        submission = mock_submission()
        submission.approved = True
        submission.author.is_mod = False

        result = label_submission(submission)
        self.assertTrue(result is False)

    def test_label_submission_none(self):
        submission = mock_submission()
        submission.approved = False
        submission.author.is_mod = False

        result = label_submission(submission)
        self.assertTrue(result is None)


if __name__ == "__main__":
    unittest.main()
