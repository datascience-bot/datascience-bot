# -*- coding: utf-8 -*-
"""Submission Moderator

Moderate submissions from new redditors and links to spam.

Usage:
    >>> import libs.shared.authpraw
    >>> from libs.submission_moderator_app.submission_moderator import SubmissionModerator
    >>> reddit = authpraw.get_datascience_bot()
    >>> moderator = SubmissionModerator(reddit)
    >>> submission = reddit.submission("euot0h")
    >>> moderator.moderate(submission)
"""
import praw

from libs.submission_moderator_app.submission_classifier import SubmissionClassifier


class SubmissionModerator:
    """Act as a moderator on a submission
    """

    # TODO: Consider aggregating removal reasons and reporting them in a
    # single comment, that way we don't have to write new responses for
    # each reason

    def __init__(self, redditor: praw.models.Redditor) -> None:
        # TODO: Verify redditor is a mod
        self.redditor = redditor
        self.classifier = SubmissionClassifier()

    def moderate(self, submission: praw.models.Submission) -> None:
        self.submission = submission

        if self.submission.approved is True:
            # assume all approved submissions have already been moderated
            return None

        # TODO: What if user doesn't have moderator privileges in the
        # submission's subreddit?
        self.classifier.classify(submission)
        c = self.classifier

        if c.is_troll:
            submission.mod.remove()
            text = (
                f"Hi u/{submission.author.name}, I removed your submission to "
                f"r/{submission.subreddit.display_name}.\n\n"
                "You don't have enough karma to start a new thread, but you "
                "can post your questions in the Entering and Transitioning "
                "thread until you accumulate at least "
                f"{self.classifier.min_karma} karma."
            )
            comment = submission.reply(text)
            comment.mod.distinguish(how="yes", sticky=True)

            return None

        if c.is_porn:
            submission.mod.remove(spam=True)
            # Don't comment; users know porn is inappropriate for the subreddit
            return None

        if c.is_video or c.is_blog:
            submission.mod.remove(spam=True)
            text = (  # TODO: Callout domain explicitly instead of "that domain"
                f"Hi u/{submission.author.name}, I removed your submission. "
                f"Submissions from that domain are not allowed on "
                f"r/{submission.subreddit.display_name}."
            )
            comment = submission.reply(text)
            comment.mod.distinguish(how="yes", sticky=True)
            return None

        self.submission.mod.approve()
