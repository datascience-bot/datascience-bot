# -*- coding: utf-8 -*-
"""Submission Moderator for r/datascience

Identify submissions from under-qualified users and links to spam.
"""
import praw

from .karma_classifier import classify_karma
from .submission_classifier import classify_submission

__version__ = "0.0.1.dev1"


def moderate_submission(submission: praw.models.Submission):
    if submission.approved_by is not None:
        return None

    author = submission.author

    # identify rule violations in user contributions
    user_label = classify_karma(total_karma=_calc_total_karma)
    if user_label == "new user":
        remove_underqualified(submission)
        return None
    elif user_label == "troll":
        remove_troll(submission)
        return None

    # identify rule violations in submission
    submission_label = classify_submission(submission.url)
    if submission_label is None:
        # ignore submissions without labels
        pass
    elif submission_label.reason == "porn":
        remove_porn(submission)
        return None
    elif submission_label.reason == "video hosting site":
        remove_video(submission, submission_label.blacklisted_domain)
        return None
    elif submission_label.reason == "blog aggregator":
        remove_blog(submission, submission_label.blacklisted_domain)
        return None

    submission.mod.approve()


def remove_porn(submission: praw.models.Submission):
    submission.mod.remove(spam=True)


def remove_blog(submission: praw.models.Submission, blacklisted_domain: str):
    text = (
        f"Hi u/{submission.author.name}, I removed your submission. "
        f"r/{submission.subreddit.display_name} receives a lot of spam "
        f"from {blacklisted_domain}. Try sharing the original article in a "
        "text submission and offer context for discussion in the body of "
        "your submission."
    )
    comment = submission.reply(text)
    comment.mod.distinguish(how="yes", sticky=True)
    submission.mod.remove(spam=True)


def remove_video(submission: praw.models.Submission, blacklisted_domain: str):
    text = (
        f"Hi u/{submission.author.name}, I removed your submission. "
        f"Submissions from {blacklisted_domain} are not allowed on "
        f"r/{submission.subreddit.display_name}."
    )
    comment = submission.reply(text)
    comment.mod.distinguish(how="yes", sticky=True)
    submission.mod.remove(spam=True)


def remove_troll(submission: praw.models.Submission):
    submission.mod.remove(spam=True)


def remove_underqualified(submission: praw.models.Submission):
    weekly_thread = "[weekly entering & transitioning thread](https://www.reddit.com/r/datascience/search?q=Weekly%20Entering%20%26%20Transitioning%20Thread&restrict_sr=1&t=week)"
    the_wiki = "[the wiki](https://www.reddit.com/r/datascience/wiki/index)"
    message_the_mods = "[message the mods](https://www.reddit.com/message/compose?to=%2Fr%2Fdatascience)"
    total_karma = _calc_total_karma(submission.author)

    text = (
        f"Hi u/{submission.author.name}, "
        f"I removed your submission to r/{submission.subreddit.display_name}.\n"
        f"\n"
        f"r/{submission.subreddit.display_name} gets a lot of posts from "
        f"new redditors. It's likely your topic or question has been "
        f"discussed at length before, so we remove posts from authors with "
        f"less than 50 karma as a rule. You have {total_karma} "
        f"karma right now.\n"
        f"\n"
        f"The {weekly_thread} is a good place to start. You may also find "
        f"useful resources on {the_wiki}.\n"
        f"\n"
        f"If you believe this is an error, or you're intentionally posting "
        f"with a throwaway account, please {message_the_mods} to approve "
        f"your submission."
    )
    comment = submission.reply(text)
    comment.mod.distinguish(how="yes", sticky=True)
    submission.mod.remove()


def _calc_total_karma(author: praw.models.Redditor):
    return author.link_karma + author.comment_karma
