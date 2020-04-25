import logging
import os
import pathlib

from libs.shared.authpraw import get_datascience_bot
from libs.shared.modwiki import get_local_wiki, update_wiki

WIKI_DIR = pathlib.Path("libs/wiki_moderator_app/wiki")
logger = logging.getLogger(__name__)


def main(subreddit_name: str):
    bobby = get_datascience_bot()
    remote_wiki = bobby.subreddit(subreddit_name).wiki
    local_wiki = get_local_wiki(WIKI_DIR)

    update_wiki(remote_wiki, local_wiki)
