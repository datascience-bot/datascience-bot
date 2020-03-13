"""AWS Lambda Entrypoint
"""
from typing import Dict

import praw
from prawcore.exceptions import NotFound

from authpraw import get_datascience_bot
from . import get_submission, SubmissionModerator


VALID_SUBMISSION: str = "reddit base36 submission ID, e.g., `2gmzqe`"


def main(event: Dict, context: Dict) -> Dict:
    """Implement lambda function

    AWS Lambda Docs:
        https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html

    Args:
        event (Dict): See docs
        context

    Returns:
        Dict: Response to return to application
    """
    # TODO: Track moderator behavior and report in API response

    try:
        submission_id = event["body"]["submission_id"]
    except KeyError:
        response = {
            "status_code": 404,
            "msg": (
                "response missing 'body' and nested 'submission_id' "
                f"mapping to a {VALID_SUBMISSION}."
                "try {'body': {'submission_id': '2gmzqe'} }"
            ),
        }
        return response

    bob = get_datascience_bot()

    try:
        submission = get_submission(submission_id, bob)
    except NotImplementedError:
        response = {
            "status_code": 404,
            "msg": f"{submission_id} is not a {VALID_SUBMISSION}",
        }
        return response

    moderator = SubmissionModerator(bob)
    moderator.moderate(submission)

    return {"status_code": 200}


def lambda_handler(event: Dict, context: Dict) -> Dict:
    """AWS Lambda Handler

    AWS Lambda Docs:
        https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html

    Args:
        event (Dict): See docs
        context

    Returns:
        Dict: Response to return to application
    """
    try:
        return main(event, context)
    except Exception as err:
        # unknown exceptions should not fail silently
        return {"status_code": 501, "msg": err}
