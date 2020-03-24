# -*- coding: utf-8 -*-
"""Stream submissions and moderate continuously
"""
import logging

from authpraw import get_datascience_bot
from monitor import SubmissionMonitor

from submission_moderator import SubmissionModerator


def main():
    reddit = get_datascience_bot()
    monitor = SubmissionMonitor(reddit)
    mod = SubmissionModerator(reddit)

    for submission in monitor.stream():
        msg = (
            f"Moderate '{submission.title}' "
            f"by u/{submission.author.name} "
            f"in r/{submission.subreddit.display_name} "
            f"({submission.url})"
        )
        logger.info(msg)
        mod.moderate(submission)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main()
