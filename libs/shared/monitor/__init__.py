# -*- coding: utf-8 -*-
"""Monitor activity on a subreddit
"""
from abc import ABC, abstractmethod
from typing import Generator

import praw


class AbstractMonitor(ABC):
    """Abstract class to derive content-specific monitors
    """

    def __init__(self, subreddit: praw.models.Subreddit):
        self.subreddit = subreddit

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
