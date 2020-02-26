# -*- coding: utf-8 -*-
"""Unit Test SubmissionModerator
"""
from hypothesis import given
from hypothesis.strategies import text
import pytest

from datascience_bot.submission_moderator import (
    SubmissionModerator,
    SubmissionClassifier,
)


@pytest.fixture
def moderator(redditor):
    """Unit test expected usage of SubmissionModerator.__init__
    and make object
    """
    return SubmissionModerator(redditor)


def test_submission_moderator_init_fail():
    """Unit test expected failures of SubmissionModerator.__init__
    """
    with pytest.raises(TypeError):
        SubmissionModerator()


@given(url=text())
def test_submission_moderator_moderate(moderator, submission, url):
    """Unit test expected usage of SubmissionModerator.moderate
    """
    submission.url = url

    result = moderator.moderate(submission)
    assert isinstance(result, type(None))


def test_submission_moderator_moderates_clean(moderator, submission):
    """Unit test expected result of SubmissionModerator.moderate on a
    clean submission
    """
    moderator.moderate(submission)

    submission.mod.approve.assert_called_once()
    assert not submission.mod.remove.called
    assert not submission.reply.called


@pytest.mark.parametrize("url", SubmissionClassifier.PORN_DOMAINS)
def test_submission_moderator_moderates_porn(moderator, submission, url):
    """Unit test expected result of SubmissionModerator.moderate
    """
    submission.url = url
    moderator.moderate(submission)

    assert not submission.mod.approve.called
    submission.mod.remove.assert_called_once_with(spam=True)
    assert not submission.reply.called


@pytest.mark.parametrize("url", SubmissionClassifier.VIDEO_DOMAINS)
def test_submission_moderator_moderates_videos(moderator, submission, url):
    submission.url = url
    moderator.moderate(submission)

    assert not submission.mod.approve.called
    submission.mod.remove.assert_called_once_with(spam=True)
    submission.reply.assert_called_once()


@pytest.mark.parametrize("url", SubmissionClassifier.BLOG_DOMAINS)
def test_submission_moderator_moderates_blogs(moderator, submission, url):
    submission.url = url
    moderator.moderate(submission)

    assert not submission.mod.approve.called
    submission.mod.remove.assert_called_once_with(spam=True)
    submission.reply.assert_called_once()
