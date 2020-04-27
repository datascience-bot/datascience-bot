# -*- coding: utf-8 -*-
import argparse
import logging

from libs.submission_moderator_app import main
from libs.shared.authpraw import get_datascience_bot
import libs.shared.logging


libs.shared.logging.basicConfig()
logger = logging.getLogger(__name__)


ARGS = argparse.ArgumentParser(description="Moderate submissions on a subreddit")
ARGS.add_argument(
    "subreddit_name",
    metavar="subreddit_name",
    type=str,
    help="Subreddit wiki to update",
)


if __name__ == "__main__":
    args = ARGS.parse_args()

    bobby = get_datascience_bot()
    subreddit = bobby.subreddit(args.subreddit_name)
    main(subreddit=subreddit)
