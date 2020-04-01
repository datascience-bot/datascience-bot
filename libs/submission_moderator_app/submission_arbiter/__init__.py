# -*- coding: utf-8 -*-
"""Submission Arbiter

Judge submissions for moderator based on ruling from classifier

Usage:
    >>> import libs.shared.authpraw
    >>> from libs.submission_moderator_app.submission_arbiter import SubmissionArbiter
    >>> from libs.submission_moderator_app.submission_classifier import SubmissionClassifier
    >>>
    >>> reddit = authpraw.get_datascience_bot()
    >>> classifier = SubmissionClassifier()
    >>> classifier.classify(reddit.submission("euot0h"))
    >>>
    >>> arbiter = SubmissionArbiter(classifier)
    >>> arbiter.get_verdict()
"""
import praw

from libs.submission_moderator_app.submission_classifier import SubmissionClassifier


class SubmissionArbiter:
    """Judge submissions and pass verdict with help of classifier
    """

    def __init__(self, classifier: SubmissionClassifier):
        self.classifier = classifier
        self.removal_reasons = []

    def judge_blog(self):
        if self.classifier.is_blog:
            submission = self.classifier.submission
            self.removal_reasons.append(
                "**Articles from blog aggregators are not allowed.** "
                f"Submissions from {submission.domain} are not allowed on "
                f"r/{submission.subreddit.display_name}."
            )

    def judge_porn(self):
        if self.classifier.is_porn:
            submission = self.classifier.submission
            self.removal_reasons.append(
                "**NSFW links are not allowed.** "
                f"Porn is not allowed on r/{submission.subreddit.display_name}."
            )

    def judge_troll(self):
        if self.classifier.is_troll:
            min_k = self.classifier.min_karma
            submission = self.classifier.submission
            user_k = submission.author.comment_karma + submission.author.link_karma
            self.removal_reasons.append(
                "**Not enough karma.** "
                "You don't have enough karma to start a new thread on "
                f"r/{submission.subreddit.display_name}, but you can post "
                "your questions in the Entering and Transitioning thread "
                f"until you accumulate at least {min_k} karma. "
                f"Right now you only have {user_k} karma."
            )

    def judge_video(self):
        if self.classifier.is_video:
            submission = self.classifier.submission
            self.removal_reasons.append(
                "**Videos are not allowed.** "
                f"Submissions from {submission.domain} are not allowed on "
                f"r/{submission.subreddit.display_name}."
            )

    def judge(self):
        self.removal_reasons = []  # avoid duplicate removal reasons
        self.judge_blog()
        self.judge_porn()
        self.judge_troll()
        self.judge_video()

    def _format_removal_reasons(self) -> str:
        return "\n".join([f"* {rr}" for rr in self.removal_reasons])

    def get_verdict(self) -> str:
        self.judge()
        if self.removal_reasons:
            preamble = (
                f"Hi u/{self.classifier.submission.author.name}, "
                "I removed your submission for the following removal reasons:"
            )
            verdict = "\n\n".join([preamble, self._format_removal_reasons()])
        else:
            verdict = ""
        return verdict
