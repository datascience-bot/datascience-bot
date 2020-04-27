# -*- coding: utf-8 -*-
"""Define subreddit settings

https://mods.reddithelp.com/hc/en-us/articles/360002109931-Subreddit-settings
"""
import logging
from typing import Dict

import praw


logger = logging.getLogger(__name__)


_DESCRIPTION: str = (
    "A place for data science practitioners and professionals "
    "to discuss and debate data science career questions."
)
with open("libs/modtools/site_admin/data/welcome.md", "r") as ifile:
    _WELCOME_MESSAGE: str = ifile.read().strip()


SETTINGS: Dict = {
    # See docs for settings
    # https://www.reddit.com/dev/api/#POST_api_site_admin
    # https://praw.readthedocs.io/en/latest/code_overview/other/subredditmoderation.html#praw.models.reddit.subreddit.SubredditModeration.update
    "all_original_content": False,
    "allow_chat_post_creation": False,
    "allow_discover": True,
    "allow_images": False,
    "allow_polls": True,
    "allow_post_crossposts": True,
    "allow_top": True,
    "allow_videos": False,
    "collapse_deleted_comments": True,
    "comment_score_hide_mins": 30,
    "crowd_control_mode": False,
    "description": _DESCRIPTION,
    "disable_contributor_requests": False,
    "exclude_banned_modqueue": True,
    "free_form_reports": True,
    "header_hover_text": "",
    "key_color": "#32a852",
    "lang": "en",
    "link_type": "any",
    "original_content_tag_enabled": True,
    "over_18": False,
    "public_description": _DESCRIPTION,
    "public_traffic": True,
    "show_media": True,
    "show_media_preview": False,
    "spam_comments": "low",
    "spam_links": "high",
    "spam_selfposts": "high",
    "spoilers_enabled": True,
    "submit_link_label": None,
    "submit_text": (
        "Please direct technical and project questions to the "
        "appropriate subreddit; i.e. r/learnpython, r/learnmachinelearning, etc."
    ),
    "submit_text_label": None,
    "subreddit_type": "public",
    "suggested_comment_sort": "confidence",
    "title": "Data Science",
    "welcome_message_enabled": True,
    "welcome_message_text": _WELCOME_MESSAGE,
    "wikimode": "modonly",
}


def update_settings(
    subreddit: praw.models.Subreddit, settings: Dict = SETTINGS
) -> praw.models.Subreddit:
    logger.info(f"Update r/{subreddit.display_name} settings")
    subreddit.mod.update(**settings)

    return subreddit
