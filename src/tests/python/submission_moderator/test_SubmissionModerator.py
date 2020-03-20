# -*- coding: utf-8 -*-
"""Unit Test SubmissionModerator
"""
from unittest.mock import PropertyMock

import pytest

from submission_moderator import SubmissionClassifier, SubmissionModerator


@pytest.fixture
def moderator(redditor):
    """Unit test expected behavior of SubmissionModerator.__init__
    and make object
    """
    return SubmissionModerator(redditor)


def test_submission_moderator_approves_submissions(moderator, submission):
    """Unit test expected behavior of SubmissionModerator.moderate
    on submissions which don't break the rules
    """
    assert not (submission.approved is True)
    moderator.moderate(submission)
    assert submission.mod.approve.called
    assert not submission.mod.remove.called
    assert not submission.reply.called


def test_submission_moderator_ignores_approved(moderator, submission):
    """Unit test expected behavior of SubmissionModerator.moderate
    on submissions which have already been approved
    """
    submission.approved = True
    moderator.moderate(submission)
    # don't classify anything if the post has been approved
    assert not submission.mod.approve.called
    assert not submission.mod.remove.called
    assert not submission.reply.called


def test_submission_moderator_moderates_porn(moderator, porn_submission):
    """Unit test expected behavior of SubmissionModerator.moderate
    on submissions which link to banned porn domains
    """
    moderator.moderate(porn_submission)

    assert not porn_submission.mod.approve.called
    porn_submission.mod.remove.assert_called_once_with(spam=True)
    assert not porn_submission.reply.called


def test_submission_moderator_moderates_videos(moderator, video_submission):
    """Unit test expected behavior of SubmissionModerator.moderate
    on submissions which link to banned video hosting domains
    """
    moderator.moderate(video_submission)

    assert not video_submission.mod.approve.called
    video_submission.mod.remove.assert_called_once_with(spam=True)
    video_submission.reply.assert_called_once()


def test_submission_moderator_moderates_blogs(moderator, blog_submission):
    """Unit test expected behavior of SubmissionModerator.moderate
    on submissions which link to banned blog aggregator domains
    """
    moderator.moderate(blog_submission)

    assert not blog_submission.mod.approve.called
    blog_submission.mod.remove.assert_called_once_with(spam=True)
    blog_submission.reply.assert_called_once()
