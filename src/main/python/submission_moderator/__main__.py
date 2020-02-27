"""AWS Lambda Entrypoint
"""
from typing import Dict

import praw
from prawcore.exceptions import NotFound

from authpraw import get_datascience_bot
from . import SubmissionModerator

VALID_SUBMISSION: str = "reddit base36 submission ID, e.g., `2gmzqe`"


def get_submission(
    submission_id: str, redditor: praw.models.Redditor
) -> praw.models.Submission:
    f"""Return a praw Submission from a given ID using u/datascience-bot
    
    Args:
        submission_id (str): A {VALID_SUBMISSION}
    
    Raises:
        NotImplementedError: invalid Submission ID
    
    Returns:
        praw.models.Submission: Submission with corresponding ID
    """
    submission = redditor.submission(submission_id)

    try:
        submission.title
    except NotFound:
        raise NotImplementedError(f"{submission_id} is not a valid submission ID")
    else:
        return submission


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
                f"mapping to a {VALID_SUBMISSION}"
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
        return {"status_code": 501, "msg": err}
