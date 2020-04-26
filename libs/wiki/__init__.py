# -*- coding: utf-8 -*-
"""Deploy wiki to a subreddit
"""
import logging
import pathlib

import praw

from libs.wiki.modwiki import get_local_wiki, update_wiki


WIKI_DIR = pathlib.Path("libs/wiki/data")
logger = logging.getLogger(__name__)


def main(subreddit: praw.models.Subreddit):
    logger.info(f"Enter wiki deployment for r/{subreddit.display_name}")
    remote_wiki = subreddit.wiki
    local_wiki = get_local_wiki(WIKI_DIR)

    update_wiki(remote_wiki, local_wiki)
