# -*- coding: utf-8 -*-
"""Fetch new submissions and moderate accordingly
"""
import logging

from libs.shared.authpraw import get_datascience_bot
from libs.shared.monitor import SubmissionMonitor
from libs.submission_moderator_app.submission_moderator import SubmissionModerator


logger = logging.getLogger(__name__)


def main():
    reddit = get_datascience_bot()
    monitor = SubmissionMonitor(reddit)
    mod = SubmissionModerator(reddit)

    for submission in monitor.new(limit=5):
        msg = (
            f"Moderate '{submission.title}' "
            f"by u/{submission.author.name} "
            f"in r/{submission.subreddit.display_name} "
            f"({submission.url})"
        )
        logger.info(msg)
        mod.moderate(submission)
