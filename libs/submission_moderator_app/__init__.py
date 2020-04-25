# -*- coding: utf-8 -*-
"""Submission Moderator
"""
import logging

import praw

from libs.shared.monitor import SubmissionMonitor


logger = logging.getLogger(__name__)


class SubmissionClassifier:
    """Classify a submission as one or more of the following:

        1. porn,
        2. a banned video hosting site, or
        3. a banned blog aggregator

    Usage:
        >>> import libs.shared.authpraw
        >>> from libs.submission_moderator_app.submission_classifier import SubmissionClassifier
        >>> reddit = authpraw.get_datascience_bot()
        >>> classifier = SubmissionClassifier(reddit)
        >>> submission = reddit.submission("euot0h")
        >>> classifier.classify(submission)
    """

    VIDEO_DOMAINS = ("youtube.com", "youtu.be", "vid.me")
    BLOG_DOMAINS = ("towardsdatascience.com", "medium.com")
    # TODO: What about valid blogs hosted on medium? e.g. medium.com/netflix-techblog
    PORN_DOMAINS = (
        "porn.com",
        "pornhub.com",
        "porntube.com",
        "redtube.com",
        "socialmunch.com",
        "spankwire.com",
        "xhamster.com",
        "xvideos.com",
        "youjizz.com",
        "youporn.com",
        "extremetube.com",
        "hardsextube.com",
    )
    min_karma = 50

    def __init__(self):
        self.is_blog: bool = False
        self.is_porn: bool = False
        self.is_troll: bool = False
        self.is_video: bool = False

    def classify(self, submission: praw.models.Submission) -> None:
        """Classify a submission as one or more labels

        Args:
            submission (praw.models.Submission): Submission to classify
        """
        self.__init__()
        self.submission = submission

        # for more readable list comprehensions
        author = self.submission.author
        domain = self.submission.domain

        self.is_troll = author.comment_karma + author.link_karma < self.min_karma
        self.is_blog = any(blog_domain == domain for blog_domain in self.BLOG_DOMAINS)
        self.is_porn = any(porn_domain == domain for porn_domain in self.PORN_DOMAINS)
        self.is_video = any(
            video_domain == domain for video_domain in self.VIDEO_DOMAINS
        )


class SubmissionArbiter:
    """Judge submissions for moderator based on ruling from classifier

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
            entering_and_transitioning_thread = "[Entering and Transitioning thread](https://www.reddit.com/r/datascience/search/?q=Weekly%20Entering%20%26%20Transitioning%20Thread&restrict_sr=1&sort=new&t=week)"

            self.removal_reasons.append(
                "**Not enough karma.** "
                "You don't have enough karma to start a new thread on "
                f"r/{submission.subreddit.display_name}, but you can post "
                f"your questions in the {entering_and_transitioning_thread} "
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


class SubmissionModerator:
    """Act as a moderator on a submission

    Moderate submissions from new redditors and links to spam.

    Usage:
        >>> import libs.shared.authpraw
        >>> from libs.submission_moderator_app.submission_moderator import SubmissionModerator
        >>> reddit = authpraw.get_datascience_bot()
        >>> moderator = SubmissionModerator(reddit)
        >>> submission = reddit.submission("euot0h")
        >>> moderator.moderate(submission)
    """

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


def main(reddit: praw.Reddit):
    monitor = SubmissionMonitor(reddit)
    mod = SubmissionModerator(reddit)

    for submission in monitor.new(limit=5):
        msg = (
            f"Moderate '{submission.title}' "
            f"by u/{submission.author.name} "
            f"in r/{submission.subreddit.display_name} "
            f"({submission.url})"
        )
        logger.info(msg)
        mod.moderate(submission)
