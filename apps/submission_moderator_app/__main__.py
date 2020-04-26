# -*- coding: utf-8 -*-
import logging

from libs.submission_moderator_app import main
from libs.shared.authpraw import get_datascience_bot
import libs.shared.logging


libs.shared.logging.basicConfig()
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    reddit = get_datascience_bot()
    # TODO pass subreddit to main
    main(reddit=reddit)
