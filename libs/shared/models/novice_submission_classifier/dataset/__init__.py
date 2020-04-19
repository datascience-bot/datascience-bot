# -*- coding: utf-8 -*-
"""Build labeled dataset of novice submissions

TODO: should we cache submissions between runs?

Notes:
    The full dataset can take 30-60 minutes to create. This is due to the 
    PRAW API rate limits of 30 requests per 60 seconds. 
"""
from collections import namedtuple
from datetime import datetime
import json as jsonlib
from typing import Dict, List, Type
import pathlib
import re

import pandas as pd
import praw

from libs.shared.authpraw import get_datascience_bot


SUBREDDIT_NAME = "datascience"
DATASET_SCHEMA: Dict[str, Type] = {
    "id": str,
    "label": bool,
    "title": str,
    "selftext": str,
    "author_name": str,
    "author_link_karma": int,
    "author_comment_karma": int,
    "author_created_utc": float,
    "dataset_created_utc": float,
}
JSON_CACHE = ".cache/novice_submission_labels/"


def _cache_submissions(func):
    def wrapper(submission: praw.models.Submission):
        p = pathlib.Path(JSON_CACHE) / f"{submission.id}.json"
        if p.exists():
            return jsonlib.load(p.open("r"))

        entry = func(submission)

        p.parent.mkdir(parents=True, exist_ok=True)
        jsonlib.dump(entry, p.open("w"))

        return entry

    return wrapper


def label_submission(submission: praw.models.Submission) -> bool:
    """Label a submission for the dataset

    Args:
        submission (praw.models.Submission): [description]

    Returns:
        bool: Whether the submission is a novice submission.
            None if unknown. Defaults to None.
    """
    if submission.subreddit.display_name != SUBREDDIT_NAME:
        # ignore submissions to other subreddits
        return None

    try:
        if submission.author.is_mod is True:
            # ignore moderator submissions
            return None
    except AttributeError:
        # if the user deleted their post or deleted their account,
        # then we'll see an AttributeError
        return None

    try:
        if submission.approved is True:
            return False
    except AttributeError:
        # sometimes submissions can flat-out disappear (Reddit gives a 500 error)
        # TODO: Why?
        return None

    if submission.num_comments >= 50 or submission.score >= 100:
        return False

    try:
        top_comment = submission.comments[0]
    except IndexError:
        # in case submission has no comments
        return None

    if (
        submission.approved is False
        and top_comment.stickied is True
        and top_comment.distinguished == "moderator"
    ):
        text = top_comment.body.lower()
        has_declared_action = re.search("i removed your (submission|post)", text)
        mentions_thread = re.search("entering (&|and) transitioning", text)
        if has_declared_action and mentions_thread:
            return True

        if mentions_thread and top_comment.author.name == "vogt4nick":
            # a special case to catch old (but still novice) submissions
            return True

    return None


@_cache_submissions
def _map_praw_submission_to_colnames(submission: praw.models.Submission) -> Dict:
    entry = {  # TODO: don't duplicate dataset schema here
        "id": submission.id,
        "title": submission.title,
        "selftext": submission.selftext,
    }
    try:
        user_data = {
            "author_name": submission.author.name,
            "author_link_karma": submission.author.link_karma,
            "author_comment_karma": submission.author.comment_karma,
            "author_created_utc": submission.author.created_utc,
        }
    except:
        # If user deletes account or the submission, we'll get an
        # AttributeError 'NoneType' object has no attribute 'name'
        # but we can also fail for other reasons...
        user_data = {
            "author_name": None,
            "author_link_karma": None,
            "author_comment_karma": None,
            "author_created_utc": None,
        }
    finally:
        entry.update(user_data)

    try:
        label = label_submission(submission)
    except:
        label = None
    finally:
        entry["label"] = label

    return entry


def _crawl_moderator_comments(reddit: praw.Reddit, limit: int) -> List[Dict]:
    """The best place to find novice submissions is in mods' comments
    
    Args:
        reddit (praw.Reddit):
        limit (int):
    
    Returns:
        List[Dict]: [description]
    """
    entries = []
    mods = {
        "__compactsupport__",
        "Omega037",
        "dfphd",
        "patrickSwayzeNU",
        "vogt4nick",
    }

    for mod in mods:
        user = reddit.redditor(mod)
        for i, comment in enumerate(user.comments.new(limit=limit)):
            entry = _map_praw_submission_to_colnames(comment.submission)
            if entry["label"] is True or entry["label"] is False:
                entries.append(entry)
            print(f"{i+1} | u/{mod} | {comment.submission.id} | {entry['label']}")

    return entries


def _crawl_submissions(reddit: praw.Reddit, limit: int):
    entries = []
    subreddit = reddit.subreddit(SUBREDDIT_NAME)

    for i, submission in enumerate(subreddit.new(limit=limit)):
        entry = _map_praw_submission_to_colnames(submission)
        if entry["label"] is False:
            entries.append(entry)
        try:
            print(
                f"{i+1} | u/{submission.author.name} | {submission.id} | {entry['label']}"
            )
        except:
            pass

    return entries


def make_dataset(reddit: praw.Reddit, limit: int = None) -> pd.DataFrame:
    """Make dataset of labeled submissions

    label=True if submission is a novice submission, else False

    Args:
        limit (int, optional): Max depth to search. Defaults to None.

    Returns:
        pd.DataFrame
    """
    entries = []
    entries += _crawl_moderator_comments(reddit, limit=limit)
    entries += _crawl_submissions(reddit, limit=limit)

    # deduplicate dicts
    Entry = namedtuple("Entry", sorted(entries[0]))
    entries = {Entry(**d) for d in entries}

    df = pd.DataFrame(entries)
    df["dataset_created_utc"] = datetime.utcnow().timestamp()
    df = df[list(DATASET_SCHEMA.keys())]  # reorder columns
    df = df.set_index("id").sort_values("id")

    return df

