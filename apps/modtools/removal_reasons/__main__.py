# -*- coding: utf-8 -*-
"""Mod Tools: Removal Reasons
"""
import argparse
import logging


logging.basicConfig(
    format=("%(asctime)s.%(msecs)03d UTC | %(levelname)-8s | %(message)s"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


ARGS = argparse.ArgumentParser(description="Update the removal reasons on a subreddit")
ARGS.add_argument(
    "subreddit_name",
    metavar="subreddit_name",
    type=str,
    help="Subreddit removal reasons to update",
)


if __name__ == "__main__":
    from libs.shared.authpraw import get_datascience_bot
    from libs.modtools.removal_reasons import main

    args = ARGS.parse_args()
    bobby = get_datascience_bot()
    subreddit = bobby.subreddit(args.subreddit_name)
    main(subreddit=subreddit)
