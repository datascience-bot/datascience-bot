"""Moderate (or modify) a subreddit wiki

Usage:
    >>> bobby = get_datascience_bot()
    >>> subreddit = bobby.subreddit("datascience")
    >>> remote_wiki = get_remote_wiki(subreddit)
    >>> local_wiki = get_local_wiki(".")
    >>> update_wiki(remote_wiki, local_wiki)
    wiki/index..............NO CHANGE
    wiki/getting-started....UPDATED
"""
from collections import defaultdict
import logging
import os
import pathlib
from typing import DefaultDict, Optional

import praw


SUBREDDIT_NAME: str = os.getenv("SUBREDDIT_NAME")


logger = logging.getLogger(__name__)


def get_local_wiki(parent_dir: pathlib.Path) -> DefaultDict[str, Optional[str]]:
    """Get the local wiki configuration

    A filename (without the suffix) is interpretted as the wiki page name
    for comparison purposes

    Args:
        parent_dir (pathlib.Path): Local wiki parent directory

    Returns:
        DefaultDict[str, str]: map page names to markdown. Defaults to "".
    """
    parent_dir = pathlib.Path(parent_dir)
    local_wiki = defaultdict(str)

    # TODO what about nested wiki pages? e.g. config directories
    for p in parent_dir.glob("*.md"):
        local_wiki[p.stem] = p.read_text()

    return local_wiki


def content_is_changed(remote_md: str, local_md: str) -> bool:
    """Return whether remote wiki page contents is functionally equivalent
    to the local wiki page contents.

    Args:
        remote_md (str): Remote wiki page content
        local_md (str): Local wiki page content

    Returns:
        bool: True if contents are different, else False.
    """
    return remote_md.strip() != local_md.strip()


def create_missing_wikipages(
    remote_wiki: praw.models.reddit.subreddit.SubredditWiki,
    local_wiki: DefaultDict[str, Optional[str]],
):
    for name, content in local_wiki.items():
        remote_wiki.create(name=name, content=content)


def update_wikipage(remote_wikipage: praw.models.WikiPage, local_md: str) -> None:
    """Update the remote wiki page to match the local markdown

    Args:
        remote_wikipage (praw.models.WikiPage): Wiki page to update
        local_md (str): Local wiki page content as markdown use to update 
            wiki page content.
    """
    if content_is_changed(remote_wikipage.content_md, local_md):
        remote_wikipage.edit(content=local_md)


def update_wiki(
    remote_wiki: praw.models.reddit.subreddit.SubredditWiki,
    local_wiki: DefaultDict[str, Optional[str]],
) -> None:
    """Update the subreddit wiki to the local wiki configuration

    Args:
        remote_wiki (praw.models.reddit.subreddit.SubredditWiki): [description]
        local_wiki (DefaultDict[str, Optional[str]]): [description]
    """
    create_missing_wikipages(remote_wiki, local_wiki)

    for wikipage in remote_wiki:
        logger.info(f"Update wikipage {wikipage.name}")
        content = local_wiki[wikipage.name]
        update_wikipage(wikipage, local_md=content)
