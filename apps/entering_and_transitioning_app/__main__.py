# -*- coding: utf-8 -*-
"""Fetch new submissions and moderate accordingly

Usage:
    $ python apps/entering_and_transitioning_app datascience_bot_dev
"""
import argparse
from datetime import datetime
import logging


logging.basicConfig(
    format=("%(asctime)s.%(msecs)03d UTC | %(levelname)-8s | %(message)s"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


ARGS = argparse.ArgumentParser(description="Create the entering & transitioning thread")
ARGS.add_argument(
    "subreddit_name",
    type=str,
    default="datascience_bot_dev",
    help="Subreddit to act on",
)
ARGS.add_argument(
    "--fake-sunday",
    dest="fake_sunday",
    action="store_true",
    help="Whether to fake a Sunday on Sun, 7 Jul 2019",
)
ARGS.add_argument(
    "--no-validate",
    dest="no_validate",
    action="store_true",
    help="Whether validate prerequisite conditions",
)


if __name__ == "__main__":
    from libs.entering_and_transitioning_app import main
    from libs.shared.authpraw import get_datascience_bot

    args = ARGS.parse_args()

    subreddit = get_datascience_bot().subreddit(args.subreddit_name)
    if args.fake_sunday is True:
        time = datetime.strptime("2019-07-07", "%Y-%m-%d")
    else:
        time = datetime.utcnow()

    main(subreddit=subreddit, time=time, validate=not args.no_validate)
