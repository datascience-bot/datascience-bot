# -*- coding: utf-8 -*-
"""Mod Tools: Removal Reasons
"""
import argparse
import logging

from libs.shared.authpraw import get_datascience_bot
from libs.modtools.site_admin import update_settings
import libs.shared.logging


libs.shared.logging.basicConfig()
logger = logging.getLogger(__name__)


ARGS = argparse.ArgumentParser(description="Update the removal reasons on a subreddit")
ARGS.add_argument(
    "subreddit_name",
    metavar="subreddit_name",
    type=str,
    help="Subreddit removal reasons to update",
)


if __name__ == "__main__":
    args = ARGS.parse_args()
    bobby = get_datascience_bot()
    subreddit = bobby.subreddit(args.subreddit_name)
    update_settings(subreddit=subreddit)
