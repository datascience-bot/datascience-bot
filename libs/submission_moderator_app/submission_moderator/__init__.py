# -*- coding: utf-8 -*-
"""Submission Moderator for r/datascience

Identify submissions from under-qualified users and links to spam.

Usage:
    >>> import authpraw
    >>> reddit = authpraw.get_datascience_bot()
    >>> sm = SubmissionModerator(reddit)
    >>> submission = reddit.submission("euot0h")
    >>> sm.moderate(submission)
"""
import praw


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
