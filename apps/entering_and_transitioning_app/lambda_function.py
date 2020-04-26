# -*- coding: utf-8 -*-
"""Entrypoint for AWS Lambda function
"""
import os

from libs.entering_and_transitioning_app import main
from libs.shared.authpraw import get_datascience_bot


SUBREDDIT_NAME: str = os.getenv("SUBREDDIT_NAME")


def lambda_handler(event, context):
    main(reddit=get_datascience_bot(), subreddit_name=SUBREDDIT_NAME)
