"""Classify a URL as spam
"""
from collections import namedtuple

SubmissionLabel = namedtuple("SubmissionLabel", ("blacklisted_domain", "reason"))

VIDEO_DOMAINS = ("youtube.com", "youtu.be", "vid.me")
BLOG_DOMAINS = ("towardsdatascience.com", "medium.com")
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
BLACKLISTED_DOMAINS = VIDEO_DOMAINS + BLOG_DOMAINS + PORN_DOMAINS


def classify_submission(url: str) -> str:
    """Return the blacklisted URL if spam is detected, else None.

    Args:
        submission (praw.models.Submission)

    Returns:
        str: blacklisted domain if classified as spam
        None: classified as not spam
    """
    if url is None:
        return None

    for domain in PORN_DOMAINS:
        if domain in url:
            return SubmissionLabel(blacklisted_domain=domain, reason="porn")
    for domain in VIDEO_DOMAINS:
        if domain in url:
            return SubmissionLabel(blacklisted_domain=domain, reason="video hosting site")
    for domain in BLOG_DOMAINS:
        if domain in url:
            return SubmissionLabel(blacklisted_domain=domain, reason="blog aggregator")
