# -*- coding: utf-8 -*-
"""Unit Test SubmissionClassifier
"""
from hypothesis import given
from hypothesis.strategies import text
import pytest

from submission_moderator import SubmissionClassifier


@pytest.mark.parametrize("url", SubmissionClassifier.PORN_DOMAINS)
def test_submission_classifier_classify_porn(submission, url):
    """Unit test expected failures of SubmissionModerator.__init__
    """
    submission.url = url
    c = SubmissionClassifier()
    c.classify(submission)

    assert c.is_porn is True
    assert c.is_video is False
    assert c.is_blog is False


@pytest.mark.parametrize(
    "url",
    list(SubmissionClassifier.VIDEO_DOMAINS)
    + ["https://www.youtube.com/watch?v=-qstIEHDVRg"],
)
def test_submission_classifier_classify_video(submission, url):
    """Unit test expected failures of SubmissionModerator.__init__
    """
    submission.url = url
    c = SubmissionClassifier()
    c.classify(submission)

    assert c.is_porn is False
    assert c.is_video is True
    assert c.is_blog is False


@pytest.mark.parametrize("url", SubmissionClassifier.BLOG_DOMAINS)
def test_submission_classifier_classify_video(submission, url):
    """Unit test expected failures of SubmissionModerator.__init__
    """
    submission.url = url
    c = SubmissionClassifier()
    c.classify(submission)

    assert c.is_porn is False
    assert c.is_video is False
    assert c.is_blog is True
