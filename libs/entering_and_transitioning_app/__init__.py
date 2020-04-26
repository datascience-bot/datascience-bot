# -*- coding: utf-8 -*-
"""Maintain weekly "Simple Questions" thread

1. Author the new thread
2. Redirect questions with no answers to the new thread
3. Do 1 and 2 exactly once on Sundays
"""
from datetime import datetime, timedelta, timezone
import logging
import os

import praw


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
logger = logging.getLogger(__name__)


class InvalidConditionError(Exception):
    """Raise in case weekday is not Sunday
    """


def validate_time(time: datetime = datetime.utcnow()) -> None:
    """Validate that it's a Sunday UTC time

    Args:
        time (datetime): Time to validate. Defaults to datetime.utcnow()

    Raises:
        InvalidConditionError: Not a Sunday UTC time
    """
    time = time.astimezone(timezone.utc)

    if time.strftime("%A") != "Sunday":
        raise InvalidConditionError(
            "entering_and_transitioning_app only runs on Sundays"
        )


def validate_unique_thread(
    last_thread: praw.models.Submission, time: datetime = datetime.utcnow()
) -> None:
    """Validate that the last Entering & Transitioning thread was posted
    at least 24 hours ago

    Args:
        last_thread (praw.models.Submission): Last Entering & Transitioning thread
        time (datetime, optional): Time to validate. Defaults to datetime.utcnow().

    Raises:
        InvalidConditionError: Last thread posted within 24 hours of `time`
    """
    ts = datetime.fromtimestamp(last_thread.created_utc)
    if ts < time - timedelta(hours=24):
        return None
    else:
        raise InvalidConditionError("The last thread is less than 24 hours old")


def validate_conditions(
    last_thread: praw.models.Submission, time: datetime = datetime.utcnow()
):
    """Validate all conditions to post new Entering & Transitioning thread

    Args:
        last_thread (praw.models.Submission): Last Entering & Transitioning thread
        time (datetime, optional): Time to validate. Defaults to datetime.utcnow().
    """
    validate_time(time)
    validate_unique_thread(last_thread, time)


class SubmissionAuthor:
    """Author the simple questions thread

    Usage:
        >>> from datetime import datetime
        >>> from libs.shared.authpraw import get_datascience_bot
        >>> from libs.entering_and_transitioning_app import SubmissionAuthor
        >>>
        >>> time = datetime.strptime("2019-07-07", "%Y-%m-%d")
        >>> subreddit = get_datascience_bot().subreddit("datascience_bot_dev")
        >>> author = Author(subreddit)
        >>> submission = author.submit_thread(time)
        >>>
        >>> submission.title
        'Weekly Entering & Transitioning Thread | 7 Jul 2019 - 14 Jul 2019'
    """

    title_prefix = "Weekly Entering & Transitioning Thread"
    datefmt = "%d %b %Y"

    def __init__(self, subreddit: praw.models.Subreddit):
        self.subreddit = subreddit

    @classmethod
    def get_last_thread(
        cls, subreddit: praw.models.Subreddit
    ) -> praw.models.Submission:
        """Get the last Entering & Transtioning thread

        Args:
            subreddit (praw.models.Subreddit): Subreddit to parse

        Raises:
            Exception: Found no previous Entering & Transitioning thread

        Returns:
            praw.models.Submission: Last Entering & Transitioning thread
        """
        for submission in subreddit.hot(limit=2):  # max 2 possible stickies
            if (
                submission.title.startswith(cls.title_prefix)
                and submission.stickied == True
                and submission.author == "datascience-bot"
            ):
                return submission
        else:
            raise Exception("Could not find the last stickied thread")

    def get_selftext(self) -> str:
        """Get the selftext for the Entering & Transitioning thread

        Returns:
            str: Entering & Transitioning thread's selftext
        """
        with open("libs/entering_and_transitioning_app/data/selftext.md", "r") as ifile:
            return ifile.read()

    def get_title(self, time: datetime = datetime.utcnow()) -> str:
        """Get the title for the Entering & Transitioning thread.

        Args:
            time (datetime, optional): Defaults to datetime.utcnow().
                Used only for testing.

        Returns:
            str: Formatted title
        """
        start_date = time.strftime(self.datefmt)
        end_date = (time + timedelta(days=7)).strftime(self.datefmt)

        return f"{self.title_prefix} | {start_date} - {end_date}"

    def submit_thread(
        self, time: datetime = datetime.utcnow()
    ) -> praw.models.Submission:
        """Submiss a new Entering & Transitioning thread

        Args:
            time (datetime, optional): Defaults to datetime.utcnow().
                Used only for testing.

        Returns:
            praw.models.Submission: New Entering & Transitioning thread.
        """
        title = self.get_title(time)
        selftext = self.get_selftext()

        submission = self.subreddit.submit(title, selftext, send_replies=False)
        submission.mod.flair(text="Discussion")
        submission.mod.approve()
        submission.mod.distinguish()
        submission.mod.sticky(state=True, bottom=True)
        submission.mod.suggested_sort(sort="new")

        return submission


class CommentRemediator:
    """Offer unanswered questions to repost in new weekly thread

    Usage:
        >>> from libs.shared.authpraw import get_datascience_bot
        >>> from libs.entering_and_transitioning_app import (
        ...     SubmissionAuthor,
        ...     CommentRemediator,
        ... )
        >>> time = datetime.strptime("2019-07-07", "%Y-%m-%d")
        >>> subreddit = get_datascience_bot().subreddit("datascience_bot_dev")
        >>>
        >>> last_thread = Author.get_last_thread(subreddit)
        >>> author = Author(subreddit)
        >>> new_thread = author.submit_thread(time)
        >>>
        >>> remediator = CommentRemediator()
        >>> remediator.remediate_comments(on_thread=last_thread, to_thread=new_thread)
    """

    def remediate_comments(
        self, on_thread: praw.models.Submission, to_thread: praw.models.Submission
    ):
        """Iterate over unanswered comments in old thread and
        direct them to the new Entering & Transitioning thread

        Args:
            on_thread (praw.models.Submission): Thread to parse for unanswered comments
            to_thread (praw.models.Submission): Thread to redirect users to
        """
        for comment in on_thread.comments:
            if len(comment.replies) > 0:
                continue
            self.remediate_comment(comment, to_thread)

    def remediate_comment(
        self, comment: praw.models.Comment, to_thread: praw.models.Submission,
    ):
        """Reply to a comment and direct them to the new thread

        Args:
            comment (praw.models.Comment): Comment to redirect
            to_thread (praw.models.Submission): Thread to redirect them to
        """
        msg = (
            f"Hi u/{comment.author}, I created a "
            f"[new Entering & Transitioning thread]({to_thread.permalink}). "
            "Since you haven't received any replies yet, "
            "please feel free to resubmit your comment in the new thread."
        )
        reply = comment.reply(msg)
        reply.mod.distinguish(how="yes")


def main(subreddit: praw.models.Subreddit, time: datetime = datetime.utcnow(), validate: bool = True):
    last_thread = SubmissionAuthor.get_last_thread(subreddit)

    if validate:
        validate_conditions(last_thread, time)

    author = SubmissionAuthor(subreddit)
    new_thread = author.submit_thread(time)

    remediator = CommentRemediator()
    remediator.remediate_comments(on_thread=last_thread, to_thread=new_thread)

    # TODO move this logic to libs
    last_thread.mod.sticky(state=False)
