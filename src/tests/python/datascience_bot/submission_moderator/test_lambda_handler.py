"""Unit test datascience_bot.submission_moderator.__main__
"""
from typing import Dict

import praw
import pytest

from datascience_bot.submission_moderator.__main__ import (
    get_submission,
    lambda_handler,
    main,
)

# TODO: consider refactoring get_submission such that tests don't depend on a
# live praw.Reddit instance


@pytest.mark.parametrize("submission_id", ["euot0h"])
def test_get_submission(bob, submission_id):
    """Unit test expected usage of get_submission
    """
    result = get_submission(submission_id, bob)

    assert isinstance(result, praw.models.Submission)
    assert result._reddit.user.me() == "datascience-bot"
    print(result.title)


@pytest.mark.parametrize("submission_id", [1, 4e-96, ("what", "a", "tuple")])
def test_get_submission_501(bob, submission_id):
    """Unit test unexpected usage of get_submission
    """
    with pytest.raises(NotImplementedError):
        result = get_submission(submission_id, bob)


@pytest.fixture
def context() -> Dict:
    """AWS Lambda Handler `context` argument
    """
    # TODO: Pass a properly configured context object
    # maybe something from aws-lambda-context
    return {}


@pytest.fixture
def event() -> Dict:
    """AWS Lambda Handler `event` argument
    """
    return {"body": {"submission_id": "euot0h"}}


def test_main_200(event, context):
    """Unit test expected usage of lambda handler
    """
    try:
        response = main(event, context)
        assert response["status_code"] == 200
    except KeyError as err:
        pytest.fail(f"{err}; is the response missing a 'status_code' key?")


@pytest.mark.parametrize(
    "bad_event", [{"body": {"submission_id": "bad-submission-id"}}]
)
def test_main_404(bad_event, context):
    """Unit test unexpected usage of lambda handler

    501: Not Implemented Errors
    """
    try:
        response = main(bad_event, context)
        assert response["status_code"] == 404
    except KeyError as err:
        pytest.fail(f"{err}; is the response missing a 'status_code' key?")


def test_lambda_handler(event, context):
    response = lambda_handler(event, context)
    assert isinstance(response, dict)
