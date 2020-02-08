# -*- coding: utf-8 -*-
"""Test the submission_classifier.py module
"""
from collections import namedtuple
import pytest

from submission_moderator.submission_classifier import (
    classify_submission,
    SubmissionLabel,
)


# fmt: off
@pytest.mark.parametrize(
    "url,label",
    (
        ("https://pornhub.com/some-video", SubmissionLabel("pornhub.com", "porn")),
        ("https://youtu.be/watch?v=dQw4w9WgXcQ", SubmissionLabel("youtu.be", "video hosting site")),
        ("https://youtube.com/watch?v=ewGAmiLuYCw", SubmissionLabel("youtube.com","video hosting site")),
        ("https://www.youtube.com/watch?v=-qstIEHDVRg", SubmissionLabel("youtube.com","video hosting site")),
        ("https://medium.com/the-mission", SubmissionLabel("medium.com", 'blog aggregator')),
        ("https://github.com/pandas-dev/pandas", None),
        (None, None),
    ),
)
# fmt: on
def test__classify_submission(url, label):
    result = classify_submission(url)

    assert isinstance(result, type(label))

    if isinstance(result, SubmissionLabel):
        assert result.blacklisted_domain == label.blacklisted_domain
        assert result.reason == label.reason
