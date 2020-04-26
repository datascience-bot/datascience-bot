import logging
import os
import pathlib

import praw

from libs.shared.authpraw import get_datascience_bot
from libs.shared.modwiki import get_local_wiki, update_wiki


WIKI_DIR = pathlib.Path("libs/wiki_moderator_app/wiki")
logger = logging.getLogger(__name__)


def main(reddit: praw.Reddit, subreddit_name: str):
    logger.info("Enter wiki_moderator_app")
    remote_wiki = reddit.subreddit(subreddit_name).wiki
    local_wiki = get_local_wiki(WIKI_DIR)

    update_wiki(remote_wiki, local_wiki)
