# -*- coding: utf-8 -*-
"""Submission Classifier

Classify submissions from under-qualified users and links to spam.

Usage:
    >>> import libs.shared.authpraw
    >>> from libs.submission_moderator_app.submission_classifier import SubmissionClassifier
    >>> reddit = authpraw.get_datascience_bot()
    >>> classifier = SubmissionClassifier(reddit)
    >>> submission = reddit.submission("euot0h")
    >>> classifier.classify(submission)
"""
import praw


class SubmissionClassifier:
    """Classify a submission as one or more of the following:

        1. porn,
        2. a banned video hosting site, or
        3. a banned blog aggregator
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
