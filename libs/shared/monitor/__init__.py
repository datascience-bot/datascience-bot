# -*- coding: utf-8 -*-
"""Monitor activity on a subreddit
"""
from abc import ABC, abstractmethod
import os
from typing import Generator

import praw


class AbstractMonitor(ABC):
    """Abstract class to derive content-specific monitors
    """

    def __init__(self, reddit: praw.models.reddit):
        subreddit_name = os.getenv("SUBREDDIT_NAME")
        # TODO: error if SUBREDDIT_NAME is not defined
        self.subreddit = reddit.subreddit(subreddit_name)

    @abstractmethod
    def stream(self) -> Generator[praw.models.Submission, None, None]:
        """Stream content-specific activities
        """
        pass


class CommentMonitor(AbstractMonitor):
    """Monitor comments on a subreddit
    """

    def stream(self) -> Generator[praw.models.Submission, None, None]:
        yield from self.subreddit.stream.comments()


class SubmissionMonitor(AbstractMonitor):
    """Monitor submissions on a subreddit
    """

    def new(self, limit: int = 1) -> Generator[praw.models.Submission, None, None]:
        yield from self.subreddit.new(limit=limit)

    def stream(self) -> Generator[praw.models.Submission, None, None]:
        yield from self.subreddit.stream.submissions()
