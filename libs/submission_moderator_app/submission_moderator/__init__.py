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

from libs.submission_moderator_app.submission_arbiter import SubmissionArbiter
from libs.submission_moderator_app.submission_classifier import SubmissionClassifier


class SubmissionModerator:
    """Act as a moderator on a submission
    """

    # TODO: consider decoupling removal reasons from moderator to enforce them

    def __init__(self, redditor: praw.models.Redditor) -> None:
        # TODO: Verify redditor is a mod
        self.redditor = redditor

    def moderate(self, submission: praw.models.Submission) -> None:
        self.submission = submission

        if self.submission.approved is True:
            # assume all approved submissions have already been moderated
            return None

        classifier = SubmissionClassifier()
        classifier.classify(self.submission)

        arbiter = SubmissionArbiter(classifier)
        verdict = arbiter.get_verdict()

        if verdict:
            comment = self.submission.reply(verdict)
            comment.mod.distinguish(how="yes", sticky=True)
            self.submission.mod.remove()
        else:
            self.submission.mod.approve()
