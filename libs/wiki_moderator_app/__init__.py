import os
import pathlib

from libs.shared.authpraw import get_datascience_bot
from libs.shared.modwiki import get_local_wiki, update_wiki


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
WIKI_DIR = pathlib.Path("libs/wiki_moderator_app/wiki")


def main():
    bobby = get_datascience_bot()
    remote_wiki = bobby.subreddit(SUBREDDIT_NAME).wiki
    local_wiki = get_local_wiki(WIKI_DIR)

    update_wiki(remote_wiki, local_wiki)
