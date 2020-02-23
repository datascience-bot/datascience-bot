# -*- coding: utf-8 -*-
"""Test the classify_karma.py lambda function
"""
import praw

import pytest
from unittest.mock import create_autospec, Mock

from submission_moderator import moderate_submission


def mock_submission(url: str) -> Mock:
    submission = create_autospec(praw.models.Submission)
    submission.url = "totally-harmless-url.com"
    submission.url = "pornhub.com"
    submission.approved_by = None
    submission.mod = create_autospec(praw.models.reddit.submission.SubmissionModeration)
    submission.subreddit = create_autospec(praw.models.Subreddit)
    submission.subreddit.display_name = "not-a-real-subreddit"

    return submission


def mock_user(link_karma: int = None, comment_karma: int = None):
    user = create_autospec(praw.models.Redditor)
    # user = MockRedditor(MockReddit())
    user.name = "not-a-real-user"
    user.link_karma = link_karma
    user.comment_karma = comment_karma

    return user


@pytest.mark.parametrize(
    "submission,author,action",
    [
        [
            mock_submission(url="pornhub.com"),
            mock_user(link_karma=137490, comment_karma=72),
            "spam",
        ],
        [
            mock_submission(url="youtube.com"),
            mock_user(link_karma=137490, comment_karma=72),
            "spam",
        ],
        [
            mock_submission(url="medium.com"),
            mock_user(link_karma=137490, comment_karma=72),
            "spam",
        ],
        [
            mock_submission(url="some-safe-url.com"),
            mock_user(link_karma=-10, comment_karma=20),
            "rule violation",
        ],
        [
            mock_submission(url="some-safe-url.com"),
            mock_user(link_karma=-10, comment_karma=-10999),
            "spam",
        ],
    ],
)
def test__moderate_submission(submission, author, action):
    moderate_submission(submission, author)

    if action == "approve":
        submission.mod.approve.assert_called_once_with()
    if action == "spam":
        submission.mod.remove.assert_called_once_with(spam=True)
    if action == "rule violation":
        submission.mod.remove.assert_called_once_with()
        assert submission.reply.call_count == 1

    return submission


def test__moderate_approved_submission():
    submission = mock_submission("not-a-real-url.com")
    submission.approved_by = 'datascience-bot'
    moderate_submission(submission, mock_user())

    assert submission.mod.approve.call_count == 0
    assert submission.mod.remove.call_count == 0

# def main():
#     from pprint import pprint

#     reddit = MockReddit()
#     submission = MockSubmission(reddit)
#     submission.url = "totally-harmless-url.com"
#     submission.url = "pornhub.com"
#     submission.approved_by = None
#     submission.mod = MockSubmissionModeration(submission)

#     author = MockRedditor(reddit)
#     author.link_karma = 0
#     author.comment_karma = 190

#     test__moderate_submission(submission, author)

#     # pprint(submission.__dict__)
#     # submission.mod.approve.assert_called_once_with()
#     submission.mod.remove.assert_called_once_with(spam=True)
#     # pprint(submission.mod.approve.called)
#     # pprint(submission.mod.approve.assert_called_once_with())


# if __name__ == "__main__":
#     main()
#     # submission.mod.remove.assert_called_with(True, key="spam")
