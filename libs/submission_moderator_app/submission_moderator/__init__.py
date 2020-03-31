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

    # TODO: consider decoupling removal reasons from moderator to enforce them

    def __init__(self, redditor: praw.models.Redditor) -> None:
        # TODO: Verify redditor is a mod
        self.redditor = redditor
        self._reset_attributes()

    def _reset_attributes(self):
        self.classifier = SubmissionClassifier()
        self.removal_reasons = []
        self.submission = None

    def _format_removal_reasons(self):
        return "\n".join([f"* {rr}" for rr in self.removal_reasons])

    def _handle_troll(self):
        if self.classifier.is_troll:
            min_k = self.classifier.min_karma
            author = self.submission.author
            user_k = author.comment_karma + author.link_karma
            self.removal_reasons.append(
                "**Not enough karma.** "
                "You don't have enough karma to start a new thread on "
                f"{self.submission.subreddit.display_name}, but you can post "
                "your questions in the Entering and Transitioning thread "
                f"until you accumulate at least {min_k} karma. "
                f"Right now you only have {user_k} karma."
            )

    def _handle_porn(self):
        if self.classifier.is_porn:
            self.removal_reasons.append(
                "**NSFW links are not allowed.** "
                f"Porn is not allowed on r/{self.submission.subreddit.display_name}."
            )

    def _handle_blog(self):
        if self.classifier.is_blog:
            self.removal_reasons.append(
                "**Articles from blog aggregators are not allowed.** "
                f"Submissions from {self.submission.domain} are not allowed on "
                f"r/{self.submission.subreddit.display_name}."
            )

    def _handle_video(self):
        if self.classifier.is_video:
            self.removal_reasons.append(
                "**Videos are not allowed.** "
                f"Submissions from {self.submission.domain} are not allowed on "
                f"r/{self.submission.subreddit.display_name}."
            )

    def _handle_rules(self):
        self._handle_blog()
        self._handle_porn()
        self._handle_troll()
        self._handle_video()

    def moderate(self, submission: praw.models.Submission) -> None:
        self._reset_attributes()
        self.submission = submission

        if self.submission.approved is True:
            # assume all approved submissions have already been moderated
            return None

        self.classifier.classify(self.submission)
        self._handle_rules()

        if self.removal_reasons:
            preamble = (
                f"Hi u/{self.submission.author.name}, "
                "I removed your submission for the following removal reasons:"
            )
            text = "\n\n".join([preamble, self._format_removal_reasons()])
            comment = self.submission.reply(text)
            comment.mod.distinguish(how="yes", sticky=True)
            self.submission.mod.remove()
        else:
            self.submission.mod.approve()
