# -*- coding: utf-8 -*-
"""Entrypoint for AWS Lambda function
"""
import logging
import os

from libs.submission_moderator_app import main
from libs.shared.authpraw import get_datascience_bot
import libs.shared.logging


libs.shared.logging.basicConfig()
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    bobby = get_datascience_bot()
    subreddit_name = os.getenv("SUBREDDIT_NAME")
    subreddit = bobby.subreddit(subreddit_name)
    main(subreddit=subreddit)
