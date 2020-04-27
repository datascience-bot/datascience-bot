# -*- coding: utf-8 -*-
"""wiki_moderator_app binary
"""
import argparse
import logging

from libs.shared.authpraw import get_datascience_bot
import libs.shared.logging
from libs.wiki import main


libs.shared.logging.basicConfig()
logger = logging.getLogger(__name__)


ARGS = argparse.ArgumentParser(description="Update the wiki on a subreddit")
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
