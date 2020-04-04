# -*- coding: utf-8 -*-
"""Fetch new submissions and moderate accordingly
"""
from datetime import datetime
import logging
import os

from libs.shared.authpraw import get_datascience_bot
from libs.entering_and_transitioning_app import (
    CommentRemediator,
    SubmissionAuthor,
    validate_conditions,
)


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
logger = logging.getLogger(__name__)


def main(time: datetime = datetime.utcnow(), validate: bool = True):
    subreddit = get_datascience_bot().subreddit(SUBREDDIT_NAME)
    last_thread = SubmissionAuthor.get_last_thread(subreddit)

    if validate:
        validate_conditions(last_thread, time)

    author = SubmissionAuthor(subreddit)
    new_thread = author.submit_thread(time)

    remediator = CommentRemediator()
    remediator.remediate_comments(on_thread=last_thread, to_thread=new_thread)

    # TODO move this logic to libs
    last_thread.mod.sticky(state=False)
