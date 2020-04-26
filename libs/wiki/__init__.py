import logging
import os
import pathlib

import praw

from libs.shared.authpraw import get_datascience_bot
from libs.shared.modwiki import get_local_wiki, update_wiki


WIKI_DIR = pathlib.Path("libs/wiki/data")
logger = logging.getLogger(__name__)


def main(subreddit: praw.models.Subreddit):
    logger.info("Enter wiki deployment")
    remote_wiki = subreddit.wiki
    local_wiki = get_local_wiki(WIKI_DIR)

    update_wiki(remote_wiki, local_wiki)
