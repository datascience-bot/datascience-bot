# -*- coding: utf-8 -*-
"""Entrypoint for AWS Lambda function
"""
from datetime import datetime
import os

from libs.entering_and_transitioning_app import main
from libs.shared.authpraw import get_datascience_bot


SUBREDDIT_NAME: str = os.getenv("SUBREDDIT_NAME")


def lambda_handler(event, context):
    # TODO handle what happens if there's not an existing thread
    try:
        time_string = event["body"]["time"]
        validate = event["body"]["validate"]
    except KeyError:
        main(reddit=get_datascience_bot(), subreddit_name=SUBREDDIT_NAME)
    else:
        time = datetime.strptime(time_string, "%Y-%m-%d")
        main(
            reddit=get_datascience_bot(),
            subreddit_name=SUBREDDIT_NAME,
            time=time,
            validate=validate,
        )

    return "200 OK"

