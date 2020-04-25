# -*- coding: utf-8 -*-
"""wiki_moderator_app binary
"""
import argparse

from apps.wiki_moderator_app import main


parser = argparse.ArgumentParser(description="Update the wiki on a subreddit")

parser.add_argument(
    "subreddit_name",
    metavar="subreddit_name",
    type=str,
    help="Subreddit wiki to update",
)

args = parser.parse_args()


if __name__ == "__main__":
    main(subreddit_name=args.subreddit_name)
